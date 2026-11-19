"""Phase 0 smoke test for dicta-il/dictabert-tiny-joint.

Verifies model loading, inspects the exact JSON output schema across
Biblical, Rabbinic, and Modern Hebrew locative sentences, and benchmarks
local CPU throughput for single and batched inference.
"""

from __future__ import annotations

import json
import os
import sys
import time
from pathlib import Path

import torch
from transformers import AutoModel, AutoTokenizer

# Ensure UTF-8 output on Windows terminals
if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")

MODEL_NAME = "dicta-il/dictabert-tiny-joint"
LOCAL_MODEL_DIR = Path("models/dictabert-tiny-joint")

SAMPLE_SENTENCES: list[tuple[str, str]] = [
    ("MH Frame B (putting)", "דני מילא את המיכל במים"),
    ("MH Frame A (putting)", "דני מילא מים במיכל"),
    ("MH Frame B (removal)", "דני רוקן את המיכל ממים"),
    ("BH Frame B (1Kgs 6:15, unvocalized)", "ויצף את קרקע הבית בצלעות ברושים"),
    ("BH Frame A (Exod 28:17, vocalized)", "וּמִלֵּאתָ בוֹ מִלֻּאַת אֶבֶן אַרְבָּעָה טוּרִים"),
    ("Rabbinic (Mishnah style)", "הממלא מים מן הבור בשבת"),
]


def main() -> None:
    print(f"Python: {sys.version.split()[0]}")
    print(f"PyTorch: {torch.__version__} | CPU threads: {torch.get_num_threads()} | CUDA: {torch.cuda.is_available()}")
    model_source = str(LOCAL_MODEL_DIR) if LOCAL_MODEL_DIR.exists() else MODEL_NAME
    local_only = LOCAL_MODEL_DIR.exists()
    print(f"Loading {model_source} (local_files_only={local_only})...")

    t0 = time.perf_counter()
    tokenizer = AutoTokenizer.from_pretrained(
        model_source, trust_remote_code=True, local_files_only=local_only
    )
    model = AutoModel.from_pretrained(
        model_source, trust_remote_code=True, local_files_only=local_only
    )
    model.eval()
    load_sec = time.perf_counter() - t0
    print(f"Loaded model in {load_sec:.2f}s\n")

    texts = [s for _, s in SAMPLE_SENTENCES]

    with torch.inference_mode():
        t1 = time.perf_counter()
        outputs = model.predict(texts, tokenizer, output_style="json")
        batch_sec = time.perf_counter() - t1

    print(f"Parsed {len(texts)} sample sentences in {batch_sec:.3f}s ({len(texts)/batch_sec:.1f} sent/s)\n")

    for (label, text), pred in zip(SAMPLE_SENTENCES, outputs):
        print(f"=== {label} ===")
        print(f"TEXT: {text}")
        if pred.get("ner_entities"):
            print(f"NER:  {pred.get('ner_entities')}")
        tokens = pred.get("tokens", [])
        for idx, tok in enumerate(tokens):
            morph = tok.get("morph", {})
            syntax = tok.get("syntax", {})
            print(
                f"  [{idx}] {tok.get('token')!r:<12} "
                f"seg={tok.get('seg')} "
                f"lex={tok.get('lex')!r:<10} "
                f"pos={morph.get('pos')!r:<6} "
                f"pref={morph.get('prefixes')} "
                f"suff={morph.get('suffix')} "
                f"feats={morph.get('feats')} "
                f"dep=({syntax.get('dep_head_idx')}, {syntax.get('dep_func')})"
            )
        print()

    # Save full raw JSON output of the smoke test for schema inspection
    out_path = Path("results/tables/phase0_smoke_test_output.json")
    out_path.parent.mkdir(parents=True, exist_ok=True)
    with out_path.open("w", encoding="utf-8") as f:
        json.dump(
            [{"label": lbl, "text": txt, "prediction": pred} for (lbl, txt), pred in zip(SAMPLE_SENTENCES, outputs)],
            f,
            ensure_ascii=False,
            indent=2,
        )
    print(f"Saved full JSON output to {out_path}")

    # Quick CPU throughput benchmark (60 sentences in batch sizes 8, 16, 32)
    bench_texts = texts * 10  # 60 sentences
    print("\n--- CPU Batch Throughput Benchmark (60 sentences) ---")
    for bs in (8, 16, 32):
        t_start = time.perf_counter()
        with torch.inference_mode():
            for i in range(0, len(bench_texts), bs):
                _ = model.predict(bench_texts[i : i + bs], tokenizer, output_style="json")
        elapsed = time.perf_counter() - t_start
        print(f"  batch_size={bs:<2d}: {elapsed:.2f}s -> {len(bench_texts)/elapsed:.1f} sent/s")


if __name__ == "__main__":
    main()
