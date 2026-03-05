"""Wikilink resolver for permafrost.

Crude, duct-tape solution right now, mainly because I need to get things up and
running fast.
"""

import os
from urllib.parse import urlunparse

# Currently only maps filenames without dirs to urls.
def build_url_map(source_dir: str, import_dir: str) -> dict[str, str]:
    ret: dict[str, str] = {}
    for root, _, files in os.walk(source_dir, topdown=True):
        if ".trash" in root:  # TODO configurable forbidden dirs
            continue
        if ".git" in root:
            continue
        if ".obsidian" in root:
            continue

        rel_root = os.path.relpath(root, import_dir)
        for file in files:
            filename = file
            if filename.endswith(".md"):
                filename = filename.removesuffix(".md") + ".html"
            path = f"/{os.path.join(rel_root, filename).removeprefix("./")}"
            wiki_name = filename.removesuffix(".html")

            if wiki_name in ret:
                # stem clash, prefer simpler path
                continue

            ret[wiki_name] = path

    return ret

def make_build_url(url_map: dict[str, str]):
    def _build_url(urlo, base, end, url_whitespace, url_case) -> str:
        if urlo.netloc: # don't touch external links, duh!
            return urlunparse(urlo)

        # TODO actually parse `urlo` to allow for paths and ./
        resolved = url_map.get(urlo.path)
        if resolved:
            return resolved

        # TODO fallback if not resolved
        return urlo.path

    return _build_url
