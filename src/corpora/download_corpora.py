"""Download and extract the project text corpora from Google Drive into data/raw/.

Google Drive file ID extracted from project.docx.pdf (§2):
    1M3vAm4Aqm8uaFZyqwIwk0r6KNtFYb1_E
"""

from __future__ import annotations

import re
import tarfile
import zipfile
from pathlib import Path
from urllib.parse import unquote

import requests
from tqdm import tqdm

FILE_ID = "1M3vAm4Aqm8uaFZyqwIwk0r6KNtFYb1_E"
RAW_DIR = Path("data/raw")
DOWNLOAD_URL = "https://drive.usercontent.google.com/download"


def _filename_from_cd(cd: str | None) -> str | None:
    if not cd:
        return None
    m = re.search(r"filename\*=UTF-8''([^;]+)", cd, flags=re.IGNORECASE)
    if m:
        return unquote(m.group(1)).strip('"')
    m = re.search(r'filename="?([^";]+)"?', cd, flags=re.IGNORECASE)
    if m:
        return m.group(1).strip('"')
    return None


def download_gdrive(file_id: str, out_dir: Path) -> Path:
    out_dir.mkdir(parents=True, exist_ok=True)
    session = requests.Session()

    params = {"id": file_id, "export": "download", "confirm": "t"}
    resp = session.get(DOWNLOAD_URL, params=params, stream=True, timeout=60)
    resp.raise_for_status()

    # Handle Google Drive HTML confirmation page if returned
    ctype = resp.headers.get("Content-Type", "")
    if "text/html" in ctype.lower():
        html = resp.text
        action_m = re.search(r'action="([^"]+)"', html)
        inputs = dict(re.findall(r'<input[^>]+name="([^"]+)"[^>]+value="([^"]*)"', html))
        if action_m and inputs:
            resp = session.get(action_m.group(1), params=inputs, stream=True, timeout=60)
            resp.raise_for_status()
        else:
            raise RuntimeError(
                "Google Drive returned an HTML page without a downloadable confirmation form. "
                f"First 300 chars: {html[:300]!r}"
            )

    filename = _filename_from_cd(resp.headers.get("Content-Disposition")) or f"corpora_{file_id}.bin"
    dest = out_dir / filename
    total = int(resp.headers.get("Content-Length", 0)) or None

    print(f"Downloading -> {dest} (size={total or 'unknown'} bytes)")
    with dest.open("wb") as f, tqdm(total=total, unit="B", unit_scale=True, unit_divisor=1024) as pbar:
        for chunk in resp.iter_content(chunk_size=1024 * 256):
            if chunk:
                f.write(chunk)
                pbar.update(len(chunk))

    return dest


def extract_if_archive(archive_path: Path, out_dir: Path) -> None:
    suffixes = [s.lower() for s in archive_path.suffixes]
    if zipfile.is_zipfile(archive_path):
        print(f"Extracting zip archive: {archive_path}")
        with zipfile.ZipFile(archive_path, "r") as zf:
            zf.extractall(out_dir)
        print("Extraction complete.")
    elif tarfile.is_tarfile(archive_path):
        print(f"Extracting tar archive: {archive_path}")
        with tarfile.open(archive_path, "r:*") as tf:
            tf.extractall(out_dir)
        print("Extraction complete.")
    else:
        print(f"File {archive_path.name} (suffixes={suffixes}) is not a zip/tar archive; left as-is.")


def main() -> None:
    archive = download_gdrive(FILE_ID, RAW_DIR)
    extract_if_archive(archive, RAW_DIR)


if __name__ == "__main__":
    main()
