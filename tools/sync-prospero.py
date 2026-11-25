#!/usr/bin/env python3
"""Synchronize eligible ProsperoStore entries into JB_STORE_REPO.

Only metadata from the official catalog is copied. Developer-hosted ZIPs are
linked, never mirrored or executed. Existing homebrew entries are preserved.
"""
import argparse
import json
import re
import unicodedata
from pathlib import Path
from urllib.parse import urlparse
from urllib.request import Request, urlopen

SOURCE = "https://prosperostore.net/catalog/v1.json"
FOLDERS = ("apps", "games", "media", "tools", "emu")
ALLOWED_LICENSES = (
    "mit", "gpl", "lgpl", "agpl", "apache", "bsd", "mpl", "isc",
    "cc0", "0bsd", "zlib", "unlicense", "epl", "artistic", "public domain",
)
BLOCKED_LICENSES = ("unlicensed", "unknown", "proprietary", "noassertion", "all rights reserved")
TITLE_RE = re.compile(r"^[A-Z0-9]{9}$")
SHA_RE = re.compile(r"^[0-9a-f]{64}$", re.I)


def normalize(text):
    plain = unicodedata.normalize("NFKD", str(text))
    return re.sub(r"[^a-z0-9]", "", plain.encode("ascii", "ignore").decode().lower())


def slug(text):
    plain = unicodedata.normalize("NFKD", str(text))
    return re.sub(r"(^-+|-+$)", "", re.sub(r"[^a-z0-9]+", "-", plain.encode("ascii", "ignore").decode().lower()))


def version_parts(value):
    text = str(value).lower().lstrip("v")
    if not re.fullmatch(r"[0-9][0-9.a-z_-]*", text):
        return None
    parts = re.findall(r"\d+", text)
    return tuple(map(int, parts)) if parts else None


def valid_release(item):
    tid = str(item.get("titleid") or "").upper().strip()
    url = str(item.get("artifact_url") or "")
    src = str(item.get("source_repo") or "")
    lic = str(item.get("license") or "").lower().strip()
    download = urlparse(url)
    source = urlparse(src)
    good_download = (
        download.scheme == "https" and download.netloc.lower() == "github.com"
        and re.fullmatch(r"/[^/]+/[^/]+/releases/download/[^/]+/[^/]+", download.path) is not None
    )
    good_source = (
        source.scheme == "https" and source.netloc.lower() == "github.com"
        and re.fullmatch(r"/[^/]+/[^/]+/?", source.path) is not None
    )
    return (
        TITLE_RE.fullmatch(tid) and SHA_RE.fullmatch(str(item.get("sha256") or ""))
        and item.get("format") == "zip" and good_download and good_source
        and lic and not any(x in lic for x in BLOCKED_LICENSES)
        and any(x in lic for x in ALLOWED_LICENSES)
        and str(item.get("name") or "").strip()
        and str(item.get("version") or "").strip()
    )


def entry_type(item):
    if item.get("kind") == "game":
        return "game", "games"
    category = item.get("category")
    if category == "emulators":
        return "emulator", "emu"
    if category == "utilities":
        return "tool", "tools"
    if category in ("music", "media"):
        return "app", "media"
    return "app", "apps"


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--url", default=SOURCE)
    parser.add_argument("--dry-run", action="store_true")
    args = parser.parse_args()
    root = Path(__file__).resolve().parents[1] / "repo"

    req = Request(args.url, headers={"User-Agent": "JB_STORE_REPO-catalog-sync/1.0", "Accept": "application/json"})
    with urlopen(req, timeout=45) as resp:
        feed = json.load(resp)
    if feed.get("schema") != 1 or not isinstance(feed.get("apps"), list) or len(feed["apps"]) < 50:
        raise RuntimeError("Invalid or unexpectedly small official catalog; refusing to update")

    by_id, by_name = {}, {}
    for folder in FOLDERS:
        for path in sorted((root / folder).glob("*.json")):
            obj = json.loads(path.read_text(encoding="utf-8"))
            tid = str(obj.get("title_id") or "").upper().strip()
            if tid:
                if tid in by_id:
                    raise RuntimeError(f"Duplicate local title_id {tid}: {path} and {by_id[tid][0]}")
                by_id[tid] = (path, obj)
            by_name.setdefault(normalize(obj.get("name")), []).append((path, obj))

    # Stage in memory, then write only after checking all IDs and paths.
    planned = {}
    added, updated, skipped, same = [], [], [], 0
    seen_source = set()
    for item in feed["apps"]:
        tid = str(item.get("titleid") or "").upper().strip()
        name = str(item.get("name") or "").strip()
        if not valid_release(item):
            skipped.append((name or tid, "no approved ZIP release / license"))
            continue
        if tid in seen_source:
            raise RuntimeError(f"Duplicate title ID in ProsperoStore catalog: {tid}")
        seen_source.add(tid)
        matched = by_id.get(tid)
        if not matched and normalize(name) in by_name:
            skipped.append((name, "name exists under another title ID"))
            continue

        previous = matched[1] if matched else {}
        if matched and previous.get("version") != item["version"]:
            oldparts, newparts = version_parts(previous.get("version")), version_parts(item["version"])
            if oldparts and newparts and newparts < oldparts:
                skipped.append((name, "local version appears newer"))
                continue

        typ, folder = entry_type(item)
        if matched:
            path = matched[0]
        else:
            base = slug(name) or tid.lower()
            path = root / folder / (base + ".json")
            if path.exists() or path in planned:
                path = root / folder / (base + "-" + tid.lower() + ".json")

        obj = dict(previous)
        obj.update({
            "name": name,
            "git": item["source_repo"],
            "type": previous.get("type", typ),
            "description": item["description"],
            "download_url": item["artifact_url"],
            "title_id": tid,
            "version": str(item["version"]),
            "format": "zip",
            "status": "available",
            "supported_by_store": True,
            "source_page": item["source_repo"],
            "sha256": item["sha256"].lower(),
            "author": item.get("author") or previous.get("author") or "Unknown",
        })
        if item.get("icon_url"):
            obj["cover_image"] = item["icon_url"]
        if previous.get("download_url") != item["artifact_url"]:
            obj.pop("size_bytes", None)  # Never retain a stale file size.
        if obj == previous:
            same += 1
            continue
        planned[path] = json.dumps(obj, ensure_ascii=False, indent=2) + "\n"
        (updated if matched else added).append(f"{name} ({tid}): {previous.get('version','new')} -> {item['version']}")

    if len(planned) > 200:
        raise RuntimeError(f"Suspiciously large sync ({len(planned)} files); refusing to update")
    print(f"ProsperoStore: {len(feed['apps'])} records; {len(added)} new, {len(updated)} updated, {same} unchanged, {len(skipped)} skipped.")
    for line in added:
        print("ADD", line)
    for line in updated:
        print("UPDATE", line)
    for item, reason in skipped:
        print("SKIP", item, reason)
    if not args.dry_run:
        for path, content in planned.items():
            path.parent.mkdir(parents=True, exist_ok=True)
            path.write_text(content, encoding="utf-8")


if __name__ == "__main__":
    main()
