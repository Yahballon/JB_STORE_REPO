#!/usr/bin/env python3
"""Package the store's repo directory without external dependencies."""

import argparse
from pathlib import Path
from zipfile import ZIP_DEFLATED, ZipFile


def main():
    root = Path(__file__).resolve().parents[1]
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--output", type=Path, default=root / "dist" / "JB_STORE_REPO.zip"
    )
    output = parser.parse_args().output.resolve()
    source = root / "repo"
    if output.is_relative_to(source):
        parser.error("The output ZIP must be outside the repo directory.")
    files = sorted(path for path in source.rglob("*") if path.is_file())
    if not files:
        parser.error("The repo directory contains no files.")
    output.parent.mkdir(parents=True, exist_ok=True)
    with ZipFile(output, "w", compression=ZIP_DEFLATED) as archive:
        for path in files:
            archive.write(path, path.relative_to(root).as_posix())
    print(f"Created {output} ({len(files)} files)")


if __name__ == "__main__":
    main()
