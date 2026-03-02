import os
import logging

from .shell_utils import copy
from .convert import md_to_html

logger = logging.getLogger(__name__)

# TODO if the metadata defines a slug, make slug/index.html instead.

# TODO also move assets, css and js if any.

# TODO for now, only support images by relative paths. when you implement the
# asset moving thing, you'll have to update the paths accordingly.

def build_file(source: str, output: str) -> None:
    logger.info(f"* cvt {source} -> {output}")

    with open(source, "r") as f:
        source_str = f.read()

    converted = md_to_html(source_str)

    with open(output, "w") as f:
        _ = f.write(converted)

def is_forbidden_root(root: str) -> bool:
    return ".obsidian" in root or ".git" in root or ".trash" in root

def is_forbidden_file(file: str) -> bool:
    return not bool(file)  # TODO whitelist extensions

def build(source_dir: str, output_dir: str) -> None:
    """Build a static site from source_dir and place it in output_dir."""
    
    if not os.path.isdir(output_dir):
        os.makedirs(output_dir)

    for root, _dirs, files in os.walk(source_dir, topdown=True):
        if is_forbidden_root(root):
            continue

        for file in files:
            if is_forbidden_file(file):
                continue

            source_path = os.path.join(root, file)
            output_path = os.path.join(output_dir, file)

            output_parent_dir = os.path.dirname(output_path)
            if not os.path.isdir(output_parent_dir):
                os.makedirs(output_parent_dir)

            if not file.endswith(".md"):
                copy(source_path, output_path)
                continue
            build_file(source_path, output_path.replace(".md", ".html"))

