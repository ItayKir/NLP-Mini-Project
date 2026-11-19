"""Download dicta-il/dictabert-tiny-joint and its custom modeling code locally.

The model's config.json references custom Python code hosted in
`dicta-il/dictabert-joint`. We download those `.py` files into the same local
folder and update `auto_map` so all downstream runs work 100% offline.
"""

from __future__ import annotations

import json
from pathlib import Path

from huggingface_hub import snapshot_download

MODEL_ID = "dicta-il/dictabert-tiny-joint"
CODE_REPO_ID = "dicta-il/dictabert-joint"
LOCAL_DIR = Path("models/dictabert-tiny-joint")


def main() -> None:
    LOCAL_DIR.mkdir(parents=True, exist_ok=True)
    path = snapshot_download(
        repo_id=MODEL_ID,
        local_dir=str(LOCAL_DIR),
        ignore_patterns=["pytorch_model.bin"],
    )
    print(f"Model snapshot ready at {path}")

    # Fetch custom Python modeling files referenced by auto_map
    snapshot_download(
        repo_id=CODE_REPO_ID,
        local_dir=str(LOCAL_DIR),
        allow_patterns=["*.py"],
    )
    print(f"Downloaded custom Python modules from {CODE_REPO_ID}")

    # Point auto_map to the local BertForJointParsing module
    cfg_path = LOCAL_DIR / "config.json"
    cfg = json.loads(cfg_path.read_text(encoding="utf-8"))
    if "auto_map" in cfg and "AutoModel" in cfg["auto_map"]:
        val = cfg["auto_map"]["AutoModel"]
        if "--" in val:
            cfg["auto_map"]["AutoModel"] = val.split("--", 1)[1]
            cfg_path.write_text(json.dumps(cfg, indent=2, ensure_ascii=False), encoding="utf-8")
            print(f"Updated auto_map.AutoModel -> {cfg['auto_map']['AutoModel']}")


if __name__ == "__main__":
    main()
