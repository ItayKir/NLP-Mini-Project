"""Audit raw extracted corpora in data/raw/extracted/.

Reports per-period and per-subcorpus file counts, sizes, extensions, encodings,
niqqud/te'amim/HTML indicators, approximate line & word counts, and sample text.
"""

from __future__ import annotations

import json
import re
import sys
from collections import Counter
from pathlib import Path

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")

ROOT = Path("data/raw/extracted")
OUT_JSON = Path("results/tables/phase2_raw_audit.json")

NIQQUD_RE = re.compile(r"[\u05B0-\u05BD\u05BF\u05C1\u05C2\u05C4\u05C5\u05C7]")
TEAMIM_RE = re.compile(r"[\u0591-\u05AF]")
HTML_RE = re.compile(r"<[a-zA-Z/][^>]{0,60}>")
HEB_RE = re.compile(r"[\u05D0-\u05EA]")


def detect_read_text(path: Path) -> tuple[str, str]:
    raw = path.read_bytes()
    for enc in ("utf-8-sig", "utf-8", "cp1255", "iso-8859-8", "utf-16"):
        try:
            text = raw.decode(enc)
            if HEB_RE.search(text) or len(text.strip()) == 0:
                return text, enc
        except UnicodeDecodeError:
            continue
    return raw.decode("utf-8", errors="replace"), "utf-8-replace"


def get_subcorpus(rel_parts: tuple[str, ...]) -> tuple[str, str]:
    period = rel_parts[0]
    if period in ("Mikra", "Haskala"):
        return period, period
    if len(rel_parts) >= 2:
        # Handle Hazal where files might be flat (e.g., "Mishnah - ...") or in folders
        second = rel_parts[1]
        if len(rel_parts) == 2:
            # flat file under period
            prefix = second.split(" - ")[0].strip() if " - " in second else period
            return period, prefix
        return period, second
    return period, period


def main() -> None:
    if not ROOT.exists():
        raise FileNotFoundError(f"Missing extracted directory: {ROOT}")

    groups: dict[tuple[str, str], list[Path]] = {}
    for p in ROOT.rglob("*"):
        if p.is_file():
            rel = p.relative_to(ROOT).parts
            key = get_subcorpus(rel)
            groups.setdefault(key, []).append(p)

    summary = []
    print(f"{'Period':<10} {'Subcorpus':<26} {'Files':>7} {'Size(MB)':>9} {'Words(est)':>12} {'Encodings':<22} {'Flags'}")
    print("-" * 110)

    total_files = 0
    total_bytes = 0
    total_words_est = 0

    for (period, subcorpus) in sorted(groups.keys()):
        files = sorted(groups[(period, subcorpus)])
        n_files = len(files)
        size_bytes = sum(f.stat().st_size for f in files)
        exts = Counter(f.suffix.lower() for f in files)

        # Sample up to 30 files evenly spaced for encoding/cleanliness/word-rate estimation
        step = max(1, n_files // 30)
        sample_files = files[::step][:30]

        enc_counts: Counter[str] = Counter()
        sample_bytes = 0
        sample_words = 0
        sample_lines = 0
        has_niqqud = 0
        has_teamim = 0
        has_html = 0
        sample_snippets: list[str] = []

        for sf in sample_files:
            sb = sf.stat().st_size
            sample_bytes += sb
            text, enc = detect_read_text(sf)
            enc_counts[enc] += 1
            lines = [ln.strip() for ln in text.splitlines() if ln.strip()]
            sample_lines += len(lines)
            sample_words += sum(len(ln.split()) for ln in lines)
            if NIQQUD_RE.search(text):
                has_niqqud += 1
            if TEAMIM_RE.search(text):
                has_teamim += 1
            if HTML_RE.search(text):
                has_html += 1
            if len(sample_snippets) < 3 and lines:
                snippet = " | ".join(lines[:3])[:220]
                sample_snippets.append(f"{sf.name}: {snippet}")

        words_est = int(sample_words * (size_bytes / max(sample_bytes, 1)))
        lines_est = int(sample_lines * (size_bytes / max(sample_bytes, 1)))

        flags = []
        if has_niqqud:
            flags.append(f"niqqud({has_niqqud}/{len(sample_files)})")
        if has_teamim:
            flags.append(f"teamim({has_teamim}/{len(sample_files)})")
        if has_html:
            flags.append(f"html({has_html}/{len(sample_files)})")
        flag_str = ", ".join(flags) if flags else "clean"
        enc_str = ", ".join(f"{k}:{v}" for k, v in enc_counts.most_common(2))

        print(
            f"{period:<10} {subcorpus:<26} {n_files:>7,d} {size_bytes/1e6:>9.2f} "
            f"{words_est:>12,d} {enc_str:<22} {flag_str}"
        )

        total_files += n_files
        total_bytes += size_bytes
        total_words_est += words_est

        summary.append({
            "period": period,
            "subcorpus": subcorpus,
            "n_files": n_files,
            "size_mb": round(size_bytes / 1e6, 3),
            "extensions": dict(exts),
            "encodings_sampled": dict(enc_counts),
            "lines_est": lines_est,
            "words_est": words_est,
            "has_niqqud_files": has_niqqud,
            "has_teamim_files": has_teamim,
            "has_html_files": has_html,
            "sample_count": len(sample_files),
            "snippets": sample_snippets,
        })

    print("-" * 110)
    print(f"{'TOTAL':<37} {total_files:>7,d} {total_bytes/1e6:>9.2f} {total_words_est:>12,d}")

    OUT_JSON.parent.mkdir(parents=True, exist_ok=True)
    OUT_JSON.write_text(json.dumps(summary, ensure_ascii=False, indent=2), encoding="utf-8")
    print(f"\nSaved detailed audit to {OUT_JSON}")


if __name__ == "__main__":
    main()
