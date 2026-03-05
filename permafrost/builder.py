import os
import logging

from .shell_utils import copy
from .convert import md_to_html
from .wikilink import build_url_map, make_build_url
from .templates import scan_templates

logger = logging.getLogger(__name__)

# TODO if the metadata defines a slug, make slug/index.html instead.

def build_file(source: str, output: str, templates: dict[str, str], build_url=None) -> None:
    logger.info(f"* cvt {source} -> {output}")

    with open(source, "r") as f:
        source_str = f.read()

    converted = md_to_html(source_str, templates, build_url)

    with open(output, "w") as f:
        _ = f.write(converted)

def is_forbidden_root(root: str) -> bool:
    return ".obsidian" in root or ".git" in root or ".trash" in root

def is_forbidden_file(file: str) -> bool:
    return not bool(file)  # TODO whitelist extensions

def build(source_dir: str, output_dir: str, import_dir: str, templates: dict[str, str] | None) -> None:
    """Build a static site from source_dir and place it in output_dir."""

    logger.info(f"building {source_dir} -> {output_dir}")

    url_map = build_url_map(source_dir, import_dir)
    wikilink_build_url = make_build_url(url_map)
    templates = scan_templates(templates, source_dir)
    
    if not os.path.isdir(output_dir):
        os.makedirs(output_dir)

    for root, _dirs, files in os.walk(source_dir, topdown=True):
        if is_forbidden_root(root):
            continue

        for file in files:
            if is_forbidden_file(file):
                continue

            source_path = os.path.join(root, file)

            output_relpath = os.path.relpath(root, source_dir)
            output_path = os.path.join(output_dir, output_relpath)
            output_file = os.path.join(output_path, file)

            output_parent_dir = os.path.dirname(output_file)
            if not os.path.isdir(output_parent_dir):
                os.makedirs(output_parent_dir)

            if not file.endswith(".md"):
                copy(source_path, output_file)
                continue
            output_file = output_file.removesuffix(".md") + ".html"
            build_file(source_path, output_file, templates, wikilink_build_url)

