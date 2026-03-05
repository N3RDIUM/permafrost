import os
import json
from typing import TypedDict

from .permafrost.logger import root_logger
from .permafrost.sync_repo import sync_repo
from .permafrost.builder import build
from .permafrost.shell_utils import smart_copytree, chdir

# TODO support argparse

# TODO differentiate between permafrost import and permafrost vault configs.

WELCOME = "permafrost, the obsidian static site generator for n3rdium.dev"
root_logger.info(WELCOME)

class PermafrostConfig(TypedDict):
    output_dir: str
    imports: dict[str, str]  # map slug -> remote
    # TODO custom templates

with open("permafrost.json", "r") as f:
    config: PermafrostConfig = json.load(f)

output_dir = config.get("output_dir", "./dist")
if not os.path.isdir(output_dir):
    raise Exception("output dir does not exist!")

import_dir = config.get("import_dir", "./build")
if not os.path.isdir(import_dir):
    os.makedirs(import_dir)

imports = config.get("imports", {})
for slug, remote in imports.items():
    sync_path = os.path.join(import_dir, slug)

    source_path = sync_path
    remote_config = {}
    config_file = os.path.join(sync_path, "permafrost.json")
    if os.path.exists(config_file):  # individual vault config
        with open(config_file, "r") as f:
            remote_config = json.load(f)
            src = remote_config.get("source")
            if src:
                source_path = os.path.join(source_path, src)

    out_path = os.path.join(output_dir, slug)

    sync_repo(remote, sync_path)
    build(source_path, out_path, import_dir)

    included_dirs = []
    config_includes = remote_config.get("include_dirs")
    if config_includes:
        included_dirs = config_includes

    root_logger.info("copying configured directories to build root")
    for dir in included_dirs:
        src = os.path.join(sync_path, dir)
        dst = os.path.join(output_dir, dir)
        smart_copytree(src, dst)

