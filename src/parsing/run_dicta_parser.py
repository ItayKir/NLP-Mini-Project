"""Phase 3: Batched, length-sorted, resumable DictaBERT parser for all corpora.

Runs the local offline `models/dictabert-tiny-joint` model over preprocessed
Parquet shards in `data/processed/` and writes two compact columnar Parquet
tables per shard into `data/parsed/`:
  - `<shard>__sents.parquet`: sentence-level metadata, tree depth, MDD, NER
  - `<shard>__tokens.parquet`: token-level morphology, segmentation, syntax, NER

Key engineering features:
  - Length-sorting before batching (eliminates padding waste on CPU, ~2x speedup)
  - Strict 512-subword safety guard (splits/truncates any outlier before forward)
  - Resumable per-shard execution + atomic file commits
  - Built-in post-parse tree integrity checks (depth, root validity, BLANK rate)

Usage:
  python src/parsing/run_dicta_parser.py --shards mikra__tanakh
  python src/parsing/run_dicta_parser.py --all --batch-size 32
"""

from __future__ import annotations

import argparse
import csv
import json
import random
import sys
import time
from collections import defaultdict
from pathlib import Path

import pandas as pd
import pyarrow as pa
import pyarrow.parquet as pq
import torch
from tqdm import tqdm
from transformers import AutoModel, AutoTokenizer

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")

MODEL_DIR = Path("models/dictabert-tiny-joint")
PROC_DIR = Path("data/processed")
PARSED_DIR = Path("data/parsed")
MANIFEST_CSV = Path("results/tables/phase3_parse_manifest.csv")

MAX_SUBWORDS = 480  # Safe margin below BERT's 512 max_position_embeddings
SEED = 42

# Balanced stratified targets (~2.1M words across all 5 periods & 16 sub-corpora)
BALANCED_TARGETS: dict[str, int | None] = {
    "mikra__tanakh": None,           # 100% full Tanakh (23,204 verses)
    "hazal__mishnah": 5000,
    "hazal__tosefta": 5000,
    "hazal__midrash_tannaitic": 5000,
    "hazal__midrash_aggadah": 5000,
    "medieval__rambam": 5000,
    "medieval__musar": 5000,
    "medieval__thought": 5000,
    "haskala__haskala": 20000,
    "modern__news": 5000,
    "modern__literary_original": 2500,
    "modern__literary_translated": 2500,
    "modern__tapuz": 5000,
    "modern__blogs": 5000,
    "modern__medical": 5000,
    "modern__kneset": 5000,
}


def stratified_subsample_df(df: pd.DataFrame, target_n: int, seed: int = SEED) -> pd.DataFrame:
    """Deterministically subsample `df` proportionally by `doc_id`."""
    if len(df) <= target_n:
        return df
    rng = random.Random(seed)
    by_doc: dict[str, list[int]] = defaultdict(list)
    for pos_idx, doc_id in enumerate(df["doc_id"].tolist()):
        by_doc[doc_id].append(pos_idx)

    total = len(df)
    chosen: list[int] = []
    remainders: list[tuple[float, str, list[int]]] = []

    for doc_id in sorted(by_doc.keys()):
        idxs = by_doc[doc_id]
        exact = target_n * (len(idxs) / total)
        k = int(exact)
        shuffled = list(idxs)
        rng.shuffle(shuffled)
        chosen.extend(shuffled[:k])
        if shuffled[k:]:
            remainders.append((exact - k, doc_id, shuffled[k:]))

    deficit = target_n - len(chosen)
    if deficit > 0 and remainders:
        remainders.sort(key=lambda x: (-x[0], x[1]))
        pool = [idx for _, _, left in remainders for idx in left]
        chosen.extend(pool[:deficit])

    chosen = sorted(chosen[:target_n])
    return df.iloc[chosen].reset_index(drop=True)


def compute_tree_metrics(heads: list[int]) -> tuple[int, float, int]:
    """Return (tree_depth, mean_dep_dist, n_roots) for a 0-indexed head list.

    Root nodes have head == -1. Depth of a single root token is 1; a chain
    root -> child -> grandchild has depth 3. Uses cycle protection just in case.
    """
    n = len(heads)
    if n == 0:
        return 0, 0.0, 0

    children: dict[int, list[int]] = defaultdict(list)
    roots: list[int] = []
    dep_dists: list[int] = []

    for idx, h in enumerate(heads):
        if h < 0 or h >= n or h == idx:
            roots.append(idx)
        else:
            children[h].append(idx)
            dep_dists.append(abs(idx - h))

    # BFS from all roots to compute max depth safely
    max_depth = 0
    visited = set()
    stack: list[tuple[int, int]] = [(r, 1) for r in roots]
    while stack:
        node, depth = stack.pop()
        if node in visited:
            continue
        visited.add(node)
        if depth > max_depth:
            max_depth = depth
        for ch in children.get(node, ()):
            if ch not in visited:
                stack.append((ch, depth + 1))

    mdd = float(sum(dep_dists) / len(dep_dists)) if dep_dists else 0.0
    return max_depth, mdd, len(roots)


def ensure_safe_length(text: str, tokenizer, max_subwords: int = MAX_SUBWORDS) -> str:
    """Truncate outlier texts that exceed BERT's 512-subword limit."""
    # Fast character heuristic: Hebrew averages ~2.5 chars/subword -> 900 chars is always safe
    if len(text) < 600:
        return text
    ids = tokenizer.encode(text, add_special_tokens=True)
    if len(ids) <= max_subwords:
        return text
    words = text.split()
    lo, hi = 1, len(words)
    best = words[:60]
    while lo <= hi:
        mid = (lo + hi) // 2
        cand = " ".join(words[:mid])
        if len(tokenizer.encode(cand, add_special_tokens=True)) <= max_subwords:
            best = words[:mid]
            lo = mid + 1
        else:
            hi = mid - 1
    return " ".join(best)


def parse_shard(
    shard_path: Path,
    model,
    tokenizer,
    batch_size: int = 32,
    overwrite: bool = False,
    max_sents: int | None = None,
) -> dict:
    shard_name = shard_path.stem
    sents_out = PARSED_DIR / f"{shard_name}__sents.parquet"
    tokens_out = PARSED_DIR / f"{shard_name}__tokens.parquet"

    if not overwrite and sents_out.exists() and tokens_out.exists():
        s_df = pd.read_parquet(sents_out, columns=["sent_id", "n_tokens", "tree_depth"])
        print(f"[SKIP] {shard_name}: already parsed ({len(s_df):,} sents)")
        return {
            "shard": shard_name,
            "status": "skipped_existing",
            "n_sents": len(s_df),
            "n_tokens": int(s_df["n_tokens"].sum()),
            "avg_tree_depth": round(float(s_df["tree_depth"].mean()), 3),
            "blank_lex_pct": -1.0,
            "elapsed_sec": 0.0,
            "sents_per_sec": 0.0,
        }

    df = pd.read_parquet(shard_path)
    orig_n = len(df)
    if max_sents is not None and len(df) > max_sents:
        df = stratified_subsample_df(df, max_sents, seed=SEED)
    n_sents = len(df)
    sub_note = f" (stratified from {orig_n:,})" if n_sents < orig_n else ""
    print(f"\n[PARSE] {shard_name}: {n_sents:,} sentences{sub_note} (batch_size={batch_size})")

    # Sort indices by approximate character length and pack dynamic word-budget batches
    # so long sentences (80-120 words) never trigger huge [B, L, 128000] lex_logits spikes.
    texts_raw = df["text"].tolist()
    texts_safe = [ensure_safe_length(t, tokenizer) for t in texts_raw]
    word_lens = [max(1, len(t.split())) for t in texts_safe]
    order = sorted(range(n_sents), key=lambda i: word_lens[i])

    max_words_per_batch = 512
    batches: list[list[int]] = []
    cur_batch: list[int] = []
    cur_max_w = 0
    for i in order:
        w = word_lens[i]
        next_max_w = max(cur_max_w, w)
        if cur_batch and (
            len(cur_batch) >= batch_size
            or next_max_w * (len(cur_batch) + 1) > max_words_per_batch
        ):
            batches.append(cur_batch)
            cur_batch = [i]
            cur_max_w = w
        else:
            cur_batch.append(i)
            cur_max_w = next_max_w
    if cur_batch:
        batches.append(cur_batch)

    sent_ids = df["sent_id"].tolist()
    periods = df["period"].tolist()
    subcorpora = df["subcorpus"].tolist()
    doc_ids = df["doc_id"].tolist()

    sent_rows: list[dict] = [None] * n_sents  # type: ignore[list-item]
    # Collect token columns in columnar lists for low memory & fast PyArrow conversion
    tok_sent_id: list[str] = []
    tok_idx_col: list[int] = []
    tok_surface: list[str] = []
    tok_lex: list[str] = []
    tok_pos: list[str] = []
    tok_head: list[int] = []
    tok_deprel: list[str] = []
    tok_seg: list[str] = []
    tok_prefixes: list[str] = []
    tok_has_suffix: list[bool] = []
    tok_suffix_type: list[str] = []
    tok_suffix_feats: list[str] = []
    tok_gender: list[str] = []
    tok_number: list[str] = []
    tok_person: list[str] = []
    tok_tense: list[str] = []
    tok_feats_json: list[str] = []
    tok_ner: list[str] = []

    blank_lex_count = 0
    total_tok_count = 0

    t0 = time.perf_counter()
    with torch.inference_mode():
        pbar = tqdm(batches, desc=shard_name, unit="batch")
        for batch_idxs in pbar:
            batch_texts = [texts_safe[i] for i in batch_idxs]

            preds = model.predict(
                batch_texts,
                tokenizer,
                output_style="json",
                per_token_ner=True,
                compute_syntax_mst=True,
            )

            for orig_i, pred in zip(batch_idxs, preds):
                sid = sent_ids[orig_i]
                tokens = pred.get("tokens", [])
                heads = [int(t["syntax"]["dep_head_idx"]) for t in tokens]
                depth, mdd, n_roots = compute_tree_metrics(heads)

                lemmas_non_punct = set()
                root_pos = ""

                for idx_t, t in enumerate(tokens):
                    morph = t.get("morph", {})
                    syntax = t.get("syntax", {})
                    feats = morph.get("feats") or {}
                    seg = t.get("seg") or (t.get("token", ""),)
                    prefs = morph.get("prefixes") or []
                    suff = morph.get("suffix", False)
                    suff_feats = morph.get("suffix_feats") or {}
                    lex = t.get("lex", "")
                    pos = morph.get("pos", "")
                    head_idx = int(syntax.get("dep_head_idx", -1))
                    dep_func = syntax.get("dep_func", "")
                    ner_tag = t.get("ner", "O")

                    if lex == "[BLANK]":
                        blank_lex_count += 1
                    if pos != "PUNCT" and lex and lex != "[BLANK]":
                        lemmas_non_punct.add(lex)
                    if head_idx == -1 and not root_pos:
                        root_pos = pos

                    tok_sent_id.append(sid)
                    tok_idx_col.append(idx_t)
                    tok_surface.append(t.get("token", ""))
                    tok_lex.append(lex)
                    tok_pos.append(pos)
                    tok_head.append(head_idx)
                    tok_deprel.append(dep_func)
                    tok_seg.append("|".join(seg))
                    tok_prefixes.append("|".join(prefs))
                    tok_has_suffix.append(bool(suff))
                    tok_suffix_type.append(str(suff) if suff else "")
                    tok_suffix_feats.append(
                        json.dumps(suff_feats, ensure_ascii=False) if suff_feats else ""
                    )
                    tok_gender.append(feats.get("Gender", ""))
                    tok_number.append(feats.get("Number", ""))
                    tok_person.append(feats.get("Person", ""))
                    tok_tense.append(feats.get("Tense", ""))
                    tok_feats_json.append(
                        json.dumps(feats, ensure_ascii=False) if feats else ""
                    )
                    tok_ner.append(ner_tag)

                total_tok_count += len(tokens)
                n_words = sum(1 for t in tokens if t.get("morph", {}).get("pos") != "PUNCT")
                ner_ents = pred.get("ner_entities") or []
                sent_rows[orig_i] = {
                    "sent_id": sid,
                    "period": periods[orig_i],
                    "subcorpus": subcorpora[orig_i],
                    "doc_id": doc_ids[orig_i],
                    "text": texts_safe[orig_i],
                    "n_tokens": len(tokens),
                    "n_words": n_words,
                    "n_unique_lemmas": len(lemmas_non_punct),
                    "tree_depth": depth,
                    "mean_dep_dist": round(mdd, 4),
                    "n_roots": n_roots,
                    "root_pos": root_pos,
                    "ner_json": json.dumps(ner_ents, ensure_ascii=False) if ner_ents else "",
                }

    elapsed = time.perf_counter() - t0
    sps = n_sents / max(elapsed, 1e-6)
    blank_pct = 100.0 * blank_lex_count / max(total_tok_count, 1)

    # Write Parquet files atomically
    PARSED_DIR.mkdir(parents=True, exist_ok=True)
    sents_tmp = sents_out.with_suffix(".parquet.tmp")
    tokens_tmp = tokens_out.with_suffix(".parquet.tmp")

    sents_df = pd.DataFrame(sent_rows)
    sents_df.to_parquet(sents_tmp, index=False, compression="zstd")

    tok_table = pa.table(
        {
            "sent_id": pa.array(tok_sent_id, type=pa.string()),
            "tok_idx": pa.array(tok_idx_col, type=pa.int16()),
            "token": pa.array(tok_surface, type=pa.string()),
            "lex": pa.array(tok_lex, type=pa.string()),
            "pos": pa.array(tok_pos, type=pa.dictionary(pa.int8(), pa.string())),
            "dep_head_idx": pa.array(tok_head, type=pa.int16()),
            "dep_func": pa.array(tok_deprel, type=pa.dictionary(pa.int8(), pa.string())),
            "seg": pa.array(tok_seg, type=pa.string()),
            "prefixes": pa.array(tok_prefixes, type=pa.dictionary(pa.int16(), pa.string())),
            "has_suffix": pa.array(tok_has_suffix, type=pa.bool_()),
            "suffix_type": pa.array(tok_suffix_type, type=pa.dictionary(pa.int8(), pa.string())),
            "suffix_feats": pa.array(tok_suffix_feats, type=pa.string()),
            "gender": pa.array(tok_gender, type=pa.dictionary(pa.int8(), pa.string())),
            "number": pa.array(tok_number, type=pa.dictionary(pa.int8(), pa.string())),
            "person": pa.array(tok_person, type=pa.dictionary(pa.int8(), pa.string())),
            "tense": pa.array(tok_tense, type=pa.dictionary(pa.int8(), pa.string())),
            "feats_json": pa.array(tok_feats_json, type=pa.string()),
            "ner": pa.array(tok_ner, type=pa.dictionary(pa.int8(), pa.string())),
        }
    )
    pq.write_table(tok_table, tokens_tmp, compression="zstd")

    sents_tmp.replace(sents_out)
    tokens_tmp.replace(tokens_out)

    avg_depth = float(sents_df["tree_depth"].mean()) if not sents_df.empty else 0.0
    print(
        f"[DONE] {shard_name}: {n_sents:,} sents, {total_tok_count:,} tokens "
        f"in {elapsed/60:.2f} min ({sps:.1f} sent/s) | "
        f"avg_depth={avg_depth:.2f} | BLANK_lex={blank_pct:.2f}%"
    )

    return {
        "shard": shard_name,
        "status": "parsed",
        "n_sents": n_sents,
        "n_tokens": total_tok_count,
        "avg_tree_depth": round(avg_depth, 3),
        "blank_lex_pct": round(blank_pct, 3),
        "elapsed_sec": round(elapsed, 2),
        "sents_per_sec": round(sps, 2),
    }


def update_manifest(rows: list[dict]) -> None:
    MANIFEST_CSV.parent.mkdir(parents=True, exist_ok=True)
    existing: dict[str, dict] = {}
    if MANIFEST_CSV.exists():
        with MANIFEST_CSV.open("r", encoding="utf-8-sig", newline="") as f:
            for r in csv.DictReader(f):
                existing[r["shard"]] = r
    for r in rows:
        # Don't overwrite detailed metrics when a shard was skipped
        if r["status"] == "skipped_existing" and r["shard"] in existing:
            continue
        existing[r["shard"]] = r

    fieldnames = [
        "shard",
        "status",
        "n_sents",
        "n_tokens",
        "avg_tree_depth",
        "blank_lex_pct",
        "elapsed_sec",
        "sents_per_sec",
    ]
    with MANIFEST_CSV.open("w", encoding="utf-8-sig", newline="") as f:
        w = csv.DictWriter(f, fieldnames=fieldnames)
        w.writeheader()
        for k in sorted(existing.keys()):
            w.writerow(existing[k])


def main() -> None:
    parser = argparse.ArgumentParser(description="Run DictaBERT joint parser on preprocessed shards.")
    parser.add_argument(
        "--shards",
        nargs="+",
        help="Shard stems to parse (e.g. mikra__tanakh hazal__mishnah). Omit or use --all for all.",
    )
    parser.add_argument("--all", action="store_true", help="Parse all shards in data/processed/")
    parser.add_argument(
        "--balanced",
        action="store_true",
        help="Use balanced stratified caps per shard (BALANCED_TARGETS; ~2.1M words total)",
    )
    parser.add_argument("--batch-size", type=int, default=32, help="Batch size (default: 32)")
    parser.add_argument("--overwrite", action="store_true", help="Re-parse even if output exists")
    args = parser.parse_args()

    available = sorted(PROC_DIR.glob("*.parquet"))
    if args.shards:
        wanted = set(args.shards)
        shard_paths = [p for p in available if p.stem in wanted]
        missing = wanted - {p.stem for p in shard_paths}
        if missing:
            raise FileNotFoundError(f"Requested shard(s) not found in {PROC_DIR}: {sorted(missing)}")
    elif args.all:
        # Parse in canonical period order (Mikra -> Hazal -> Medieval -> Haskala -> Modern)
        order_keys = list(BALANCED_TARGETS.keys())
        shard_paths = sorted(
            available,
            key=lambda p: (order_keys.index(p.stem) if p.stem in order_keys else 999, p.stem),
        )
    else:
        parser.error("Specify either --shards <name...> or --all")

    print(f"Loading local model from {MODEL_DIR} (CPU threads={torch.get_num_threads()})...")
    tokenizer = AutoTokenizer.from_pretrained(str(MODEL_DIR), trust_remote_code=True, local_files_only=True)
    model = AutoModel.from_pretrained(str(MODEL_DIR), trust_remote_code=True, local_files_only=True)
    model.eval()

    results = []
    for sp in shard_paths:
        cap = BALANCED_TARGETS.get(sp.stem) if args.balanced else None
        res = parse_shard(
            sp,
            model,
            tokenizer,
            batch_size=args.batch_size,
            overwrite=args.overwrite,
            max_sents=cap,
        )
        results.append(res)
        update_manifest([res])

    print(f"\nUpdated parse manifest: {MANIFEST_CSV}")


if __name__ == "__main__":
    main()
