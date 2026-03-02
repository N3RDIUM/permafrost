import os
import json
import shutil
from typing import TypedDict

from permafrost.logger import root_logger
from permafrost.sync_repo import sync_repo
from permafrost.builder import build

WELCOME = "permafrost, the obsidian static site generator for n3rdium.dev"
root_logger.info(WELCOME)

class PermafrostConfig(TypedDict):
    output_dir: str
    imports: dict[str, str]  # map slug -> remote
    # TODO custom templates

with open("permafrost.json", "r") as f:
    config: PermafrostConfig = json.load(f)

output_dir = config.get("output_dir", "./dist")
if os.path.isdir(output_dir):
    shutil.rmtree(output_dir)
os.makedirs(output_dir)

import_dir = config.get("import_dir", "./build")
if not os.path.isdir(import_dir):
    shutil.rmtree(import_dir)
    os.makedirs(import_dir)

imports = config.get("imports", {})
for slug, remote in imports.items():
    sync_path = os.path.join(import_dir, slug)

    remote_config = {}
    config_file = os.path.join(sync_path, "permafrost.json")
    if os.path.exists(config_file):  # individual vault config
        with open(config_file, "r") as f:
            remote_config = json.load(f)

    source_path = remote_config.get("source", sync_path)
    out_path = os.path.join(output_dir, slug)

    sync_repo(remote, sync_path)
    build(source_path, out_path)

