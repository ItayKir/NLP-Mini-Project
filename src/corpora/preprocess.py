"""Phase 2 preprocessing & deterministic stratified corpus builder.

Reads raw extracted corpora from data/raw/extracted/, handles period-specific
encodings (UTF-8 for historical strata, cp1255 for Modern Hebrew), cleans text
artifacts (te'amim/niqqud, HTML/markup, [IMG] placeholders, boilerplate),
applies Hebrew-aware sentence segmentation, and writes per-subcorpus Parquet
files into data/processed/ plus a summary table in results/tables/.

Design for Local CPU Parsing (Phase 3):
- Mikra (Tanakh): 100% full corpus (all 39 books, every verse preserved).
- Hazal: 100% Mishnah + 100% Tosefta + 100% Tannaitic Midrashim (5 Halakhah works)
  + stratified sample of Aggadic Midrashim (20,000 sentences; excluding late
  Medieval/Early Modern commentaries bundled in Hazal/Midrash).
- Medieval: 20,000 sentences each from Rambam, Musar, and Thought (60,000 total).
- Haskala: 60,000 sentences stratified across all 320 texts.
- Modern: 20,000 sentences per each of the 6 genres (120,000 total):
  news (balanced across a7, haaretz, nrg, themarker, ynet),
  literary (10k original + 10k translated), tapuz, blogs, medical, kneset.
"""

from __future__ import annotations

import csv
import random
import re
import sys
from collections import Counter
from pathlib import Path

import pandas as pd

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")

SEED = 42
RAW_ROOT = Path("data/raw/extracted")
OUT_DIR = Path("data/processed")
SUMMARY_CSV = Path("results/tables/phase2_processed_summary.csv")

# Regexes for Hebrew cleaning & segmentation
TEAMIM_RE = re.compile(r"[\u0591-\u05AF]")
NIQQUD_RE = re.compile(r"[\u05B0-\u05BD\u05BF\u05C1\u05C2\u05C4\u05C5\u05C7]")
ZERO_WIDTH_RE = re.compile(r"[\u034F\u200B-\u200F\u202A-\u202E\uFEFF\u00AD]")
MASORETIC_MARKER_RE = re.compile(r"\{[פסשרנ]\}")
HTML_TAG_RE = re.compile(r"</?[a-zA-Z][a-zA-Z0-9\s=\"'/_:-]{0,80}>")
IMG_PLACEHOLDER_RE = re.compile(r"\[\s*IMG\s*\]", flags=re.IGNORECASE)
HEB_LETTER_RE = re.compile(r"[\u05D0-\u05EA]")
HEB_MAQAF_RE = re.compile(r"(?<=[\u05D0-\u05EA])[\u05BE\-](?=[\u05D0-\u05EA])")
# Biblical stray quote/geresh marks embedded inside words (e.g. ישרא'ל, ובימ"י)
MIKRA_STRAY_QUOTE_RE = re.compile(r"(?<=[\u05D0-\u05EA]{2})['\"](?=[\u05D0-\u05EA])")
MULTI_SPACE_RE = re.compile(r"\s+")

# Sentence splitting on . ? ! : (not after common Hebrew abbreviations)
SENT_SPLIT_RE = re.compile(r"(?<=[.?!׃])\s+")
MAX_WORDS_PER_SENT = 120
MIN_HEB_WORDS = 3


def read_text_file(path: Path, prefer_encoding: str) -> str:
    raw = path.read_bytes()
    order = [prefer_encoding, "utf-8-sig", "utf-8", "cp1255", "iso-8859-8"]
    seen = set()
    for enc in order:
        if enc in seen:
            continue
        seen.add(enc)
        try:
            text = raw.decode(enc)
            if HEB_LETTER_RE.search(text) or not text.strip():
                return text
        except UnicodeDecodeError:
            continue
    return raw.decode("utf-8", errors="replace")


def clean_line(text: str, is_mikra: bool = False) -> str:
    text = ZERO_WIDTH_RE.sub("", text)
    text = HTML_TAG_RE.sub(" ", text)
    text = text.replace("<>", " ").replace("<", " ").replace(">", " ")
    text = IMG_PLACEHOLDER_RE.sub(" ", text)
    text = TEAMIM_RE.sub("", text)
    text = NIQQUD_RE.sub("", text)
    text = text.replace("\u05C0", " ")  # paseq
    text = text.replace("\u05C3", ".")  # sof pasuq -> period
    if is_mikra:
        text = MASORETIC_MARKER_RE.sub(" ", text)
        text = HEB_MAQAF_RE.sub(" ", text)
        text = MIKRA_STRAY_QUOTE_RE.sub("", text)
    else:
        text = text.replace("\u05BE", " ")
    text = MULTI_SPACE_RE.sub(" ", text).strip()
    return text


def count_heb_words(s: str) -> int:
    return sum(1 for tok in s.split() if HEB_LETTER_RE.search(tok))


def split_long_sentence(sent: str, max_words: int = MAX_WORDS_PER_SENT) -> list[str]:
    words = sent.split()
    if len(words) <= max_words:
        return [sent]
    # Try splitting on clause boundaries first (; or : or ,)
    parts = re.split(r"(?<=[;:,])\s+", sent)
    chunks: list[str] = []
    buf: list[str] = []
    buf_len = 0
    for part in parts:
        pw = part.split()
        if len(pw) > max_words:
            if buf:
                chunks.append(" ".join(buf))
                buf, buf_len = [], 0
            for i in range(0, len(pw), max_words):
                chunks.append(" ".join(pw[i : i + max_words]))
        elif buf_len + len(pw) > max_words:
            chunks.append(" ".join(buf))
            buf, buf_len = [part], len(pw)
        else:
            buf.append(part)
            buf_len += len(pw)
    if buf:
        chunks.append(" ".join(buf))
    return chunks


def extract_sentences_from_text(text: str, is_mikra: bool = False) -> list[str]:
    sentences: list[str] = []
    for raw_line in text.splitlines():
        raw_line = raw_line.strip()
        if not raw_line:
            continue
        cleaned = clean_line(raw_line, is_mikra=is_mikra)
        if not cleaned:
            continue
        if is_mikra:
            # 1 verse = 1 sentence (chunk only if abnormally long)
            for chunk in split_long_sentence(cleaned):
                if count_heb_words(chunk) >= 2:
                    sentences.append(chunk)
        else:
            for part in SENT_SPLIT_RE.split(cleaned):
                part = part.strip()
                if not part:
                    continue
                for chunk in split_long_sentence(part):
                    if count_heb_words(chunk) >= MIN_HEB_WORDS:
                        sentences.append(chunk)
    return sentences


def sample_records_stratified(
    records: list[dict], target_n: int | None, rng: random.Random
) -> list[dict]:
    if target_n is None or len(records) <= target_n:
        return records
    # Stratified proportionally by doc_id (or source bucket) so every work/outlet is represented
    by_doc: dict[str, list[dict]] = {}
    for r in records:
        by_doc.setdefault(r["doc_id"], []).append(r)

    total = len(records)
    sampled: list[dict] = []
    remainders: list[tuple[float, str, list[dict]]] = []

    for doc_id in sorted(by_doc.keys()):
        doc_recs = by_doc[doc_id]
        exact = target_n * (len(doc_recs) / total)
        k = int(exact)
        idxs = list(range(len(doc_recs)))
        rng.shuffle(idxs)
        chosen = sorted(idxs[:k])
        sampled.extend(doc_recs[i] for i in chosen)
        leftover = [doc_recs[i] for i in idxs[k:]]
        if leftover:
            remainders.append((exact - k, doc_id, leftover))

    # Top up rounding remainder
    deficit = target_n - len(sampled)
    if deficit > 0 and remainders:
        remainders.sort(key=lambda x: (-x[0], x[1]))
        pool = [item for _, _, left in remainders for item in left]
        sampled.extend(pool[:deficit])

    return sampled[:target_n]


def build_subcorpus(
    period: str,
    subcorpus: str,
    files: list[Path],
    encoding: str,
    target_n: int | None,
    rng: random.Random,
    is_mikra: bool = False,
    dedup_boilerplate: bool = False,
    max_files_to_read: int | None = None,
) -> tuple[pd.DataFrame, dict]:
    files = sorted(files)
    total_files_available = len(files)
    if max_files_to_read is not None and len(files) > max_files_to_read:
        files_shuffled = list(files)
        rng.shuffle(files_shuffled)
        files = sorted(files_shuffled[:max_files_to_read])

    raw_records: list[dict] = []
    for fpath in files:
        text = read_text_file(fpath, encoding)
        sents = extract_sentences_from_text(text, is_mikra=is_mikra)
        rel_doc = fpath.relative_to(RAW_ROOT).as_posix()
        for idx, s in enumerate(sents):
            raw_records.append({
                "period": period,
                "subcorpus": subcorpus,
                "doc_id": rel_doc,
                "local_sent_idx": idx,
                "text": s,
                "n_words": len(s.split()),
            })

    # Optional cross-document boilerplate deduplication (important for Tapuz forum headers)
    n_dedup_removed = 0
    if dedup_boilerplate and raw_records:
        text_doc_counts: Counter[str] = Counter()
        seen_per_doc: dict[str, set[str]] = {}
        for r in raw_records:
            s_set = seen_per_doc.setdefault(r["doc_id"], set())
            if r["text"] not in s_set:
                s_set.add(r["text"])
                text_doc_counts[r["text"]] += 1
        # Remove sentences that appear identically in >= 3 distinct files
        boilerplate = {t for t, c in text_doc_counts.items() if c >= 3}
        filtered = [r for r in raw_records if r["text"] not in boilerplate]
        n_dedup_removed = len(raw_records) - len(filtered)
        raw_records = filtered

    n_extracted_before_sample = len(raw_records)
    sampled = sample_records_stratified(raw_records, target_n, rng)

    df = pd.DataFrame(sampled)
    if not df.empty:
        df.insert(0, "sent_id", [f"{period}_{subcorpus}_{i:06d}" for i in range(len(df))])

    out_path = OUT_DIR / f"{period.lower()}__{subcorpus}.parquet"
    out_path.parent.mkdir(parents=True, exist_ok=True)
    df.to_parquet(out_path, index=False)

    stats = {
        "period": period,
        "subcorpus": subcorpus,
        "files_available": total_files_available,
        "files_read": len(files),
        "sents_extracted": n_extracted_before_sample,
        "boilerplate_removed": n_dedup_removed,
        "sents_kept": len(df),
        "words_kept": int(df["n_words"].sum()) if not df.empty else 0,
        "avg_words_per_sent": round(float(df["n_words"].mean()), 2) if not df.empty else 0.0,
        "max_words_per_sent": int(df["n_words"].max()) if not df.empty else 0,
        "sampling_mode": "100% full" if (target_n is None or n_extracted_before_sample <= target_n) else f"stratified ({target_n:,d})",
        "output_file": out_path.as_posix(),
    }
    return df, stats


def main() -> None:
    rng = random.Random(SEED)
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    SUMMARY_CSV.parent.mkdir(parents=True, exist_ok=True)

    # Collect file lists matching project.docx.pdf §2 exactly
    mikra_files = sorted((RAW_ROOT / "Mikra").glob("*.txt"))

    hazal_dir = RAW_ROOT / "Hazal"
    hazal_mishnah = sorted(hazal_dir.glob("Mishnah - *.txt"))
    hazal_tosefta = sorted(hazal_dir.glob("Tosefta - *.txt"))
    hazal_tannaitic = sorted(hazal_dir.glob("Midrash - Halakhah - *.txt"))
    hazal_aggadah = sorted(
        p for p in hazal_dir.glob("Midrash - *.txt")
        if "Commentary" not in p.name and not p.name.startswith("Midrash - Halakhah")
    )

    med_rambam = sorted((RAW_ROOT / "Medieval" / "Rambam").rglob("*.txt"))
    med_musar = sorted((RAW_ROOT / "Medieval" / "Musar").rglob("*.txt"))
    med_thought = sorted(
        p for p in (RAW_ROOT / "Medieval" / "Thought").rglob("*.txt")
        if "Commentary" not in p.name
    )

    haskala_files = sorted((RAW_ROOT / "Haskala").glob("*.txt"))

    # Modern sub-corpora (cp1255, strictly *.txt)
    mod_dir = RAW_ROOT / "Modern"
    mod_lit_orig = [mod_dir / "literary" / "O.txt"]
    mod_lit_trans = [mod_dir / "literary" / "T.txt"]
    mod_tapuz = sorted((mod_dir / "tapuz").rglob("*.txt"))
    mod_blogs = sorted((mod_dir / "blogs").rglob("*.txt"))
    mod_medical = sorted((mod_dir / "medical").rglob("*.txt"))
    mod_kneset = sorted((mod_dir / "kneset").rglob("*.txt"))

    # News: balanced across the 5 outlets (a7, haaretz, nrg, themarker, ynet)
    news_outlets = ["a7", "haaretz", "nrg", "themarker", "ynet"]
    news_sampled_files: list[Path] = []
    for outlet in news_outlets:
        outlet_files = sorted((mod_dir / "news" / outlet).rglob("*.txt"))
        rng.shuffle(outlet_files)
        # 600 articles per outlet (3,000 total) yields ~45k+ sentences -> stratified sample to 20,000
        news_sampled_files.extend(outlet_files[:600])

    jobs = [
        # Period, Subcorpus, Files, Encoding, TargetN, is_mikra, dedup, max_files
        ("Mikra", "tanakh", mikra_files, "utf-8-sig", None, True, False, None),
        ("Hazal", "mishnah", hazal_mishnah, "utf-8-sig", None, False, False, None),
        ("Hazal", "tosefta", hazal_tosefta, "utf-8-sig", None, False, False, None),
        ("Hazal", "midrash_tannaitic", hazal_tannaitic, "utf-8-sig", 20000, False, False, None),
        ("Hazal", "midrash_aggadah", hazal_aggadah, "utf-8-sig", 20000, False, False, None),
        ("Medieval", "rambam", med_rambam, "utf-8-sig", 20000, False, False, None),
        ("Medieval", "musar", med_musar, "utf-8-sig", 20000, False, False, None),
        ("Medieval", "thought", med_thought, "utf-8-sig", 20000, False, False, None),
        ("Haskala", "haskala", haskala_files, "utf-8-sig", 60000, False, False, None),
        ("Modern", "news", news_sampled_files, "cp1255", 20000, False, True, None),
        ("Modern", "literary_original", mod_lit_orig, "cp1255", 10000, False, False, None),
        ("Modern", "literary_translated", mod_lit_trans, "cp1255", 10000, False, False, None),
        ("Modern", "tapuz", mod_tapuz, "cp1255", 20000, False, True, None),
        ("Modern", "blogs", mod_blogs, "cp1255", 20000, False, True, 2000),
        ("Modern", "medical", mod_medical, "cp1255", 20000, False, True, 3000),
        ("Modern", "kneset", mod_kneset, "cp1255", 20000, False, True, 120),
    ]

    all_stats: list[dict] = []
    print(f"{'Period':<10} {'Subcorpus':<20} {'Read/Avail':>12} {'Extracted':>10} {'Kept':>8} {'Words':>10} {'AvgW':>6} {'Mode'}")
    print("-" * 100)

    for period, sub, files, enc, target_n, is_mikra, dedup, max_f in jobs:
        _, st = build_subcorpus(
            period=period,
            subcorpus=sub,
            files=files,
            encoding=enc,
            target_n=target_n,
            rng=rng,
            is_mikra=is_mikra,
            dedup_boilerplate=dedup,
            max_files_to_read=max_f,
        )
        all_stats.append(st)
        print(
            f"{st['period']:<10} {st['subcorpus']:<20} "
            f"{st['files_read']:>5d}/{st['files_available']:<6d} "
            f"{st['sents_extracted']:>10,d} {st['sents_kept']:>8,d} "
            f"{st['words_kept']:>10,d} {st['avg_words_per_sent']:>6.1f} {st['sampling_mode']}"
        )

    tot_sents = sum(s["sents_kept"] for s in all_stats)
    tot_words = sum(s["words_kept"] for s in all_stats)
    est_parse_min = (tot_sents / 41.0) / 60.0
    print("-" * 100)
    print(f"{'TOTAL':<31} {'':>12} {'':>10} {tot_sents:>8,d} {tot_words:>10,d}   (Est. CPU parse: ~{est_parse_min:.1f} min)")

    with SUMMARY_CSV.open("w", encoding="utf-8-sig", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=list(all_stats[0].keys()))
        writer.writeheader()
        writer.writerows(all_stats)
    print(f"\nSaved summary table to {SUMMARY_CSV}")


if __name__ == "__main__":
    main()
