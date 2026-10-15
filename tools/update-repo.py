#!/usr/bin/env python3
"""Update the store metadata manifest, then package the repo directory."""

import argparse
import hashlib
import json
from pathlib import Path
import subprocess
from zipfile import ZIP_DEFLATED, ZipFile, ZipInfo


def update_version(root):
    files = []
    title_ids = {}
    for folder in ("apps", "games", "media", "tools", "emu"):
        for path in sorted((root / "repo" / folder).rglob("*.json")):
            data = path.read_bytes()
            metadata = json.loads(data)
            title_id = str(metadata.get("title_id", "")).strip().upper()
            if title_id:
                previous = title_ids.get(title_id)
                if previous is not None:
                    raise ValueError(
                        f"Duplicate title_id {title_id}: "
                        f"{previous.relative_to(root)} and {path.relative_to(root)}"
                    )
                title_ids[title_id] = path
            blob = b"blob " + str(len(data)).encode() + b"\0" + data
            files.append({
                "path": path.relative_to(root).as_posix(),
                "sha": hashlib.sha1(blob).hexdigest(),
            })
    files.sort(key=lambda item: item["path"])
    version = hashlib.sha256(
        json.dumps(files, sort_keys=True, separators=(",", ":")).encode()
    ).hexdigest()
    target = root / "repo" / "version.json"
    current = None
    if target.exists():
        try:
            current = json.loads(target.read_bytes())
        except (ValueError, UnicodeError):
            pass
    if (isinstance(current, dict) and current.get("schema") == 1
            and current.get("version") == version and current.get("files") == files
            and current.get("commit")):
        print("Repository metadata unchanged.")
        return
    commit = subprocess.check_output(
        ["git", "rev-parse", "HEAD"], cwd=root, text=True
    ).strip()
    manifest = {"schema": 1, "version": version, "commit": commit, "files": files}
    target.write_bytes((json.dumps(manifest, indent=2) + "\n").encode("utf-8"))
    print(f"Updated version.json ({len(files)} entries, version={version})")


def create_zip(root, output):
    files = sorted(path for path in (root / "repo").rglob("*") if path.is_file())
    output.parent.mkdir(parents=True, exist_ok=True)
    with ZipFile(output, "w", compression=ZIP_DEFLATED) as archive:
        for path in files:
            entry = ZipInfo(path.relative_to(root).as_posix())
            entry.compress_type = ZIP_DEFLATED
            entry.create_system = 3
            entry.external_attr = 0o100644 << 16
            archive.writestr(entry, path.read_bytes())
    print(f"Created {output} ({len(files)} files)")


def main():
    root = Path(__file__).resolve().parents[1]
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output", type=Path, default=root / "JB_STORE_REPO.zip")
    output = parser.parse_args().output.resolve()
    if output.is_relative_to(root / "repo"):
        parser.error("The output ZIP must be outside the repo directory.")
    if not (root / "repo").is_dir():
        parser.error("The repo directory is missing.")
    update_version(root)
    create_zip(root, output)


if __name__ == "__main__":
    main()
