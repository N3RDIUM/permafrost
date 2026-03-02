import os
import logging
import subprocess
import shutil

logger = logging.getLogger(__name__)

def run(command: str) -> str:
    logger.info(f"$ {command}")
    return subprocess.check_output(
        command.split(" "),
        text=True
    )

def rmtree(dir: str) -> None:
    logger.info(f"$ rm -r {dir}")
    shutil.rmtree(dir)

def copy(src: str, dst: str) -> None:
    logger.info(f"$ cp {src} {dst}")
    _ = shutil.copy(src, dst)

def smart_copytree(src: str, dst: str) -> None:  # huh. very smart indeed.
    logger.info(f"* copying {src}* -> {dst}*")

    for root, _dirs, files in os.walk(src, topdown=True):
        rel_path = os.path.relpath(root, src)
        target_root = os.path.join(dst, rel_path) if rel_path != "." else dst

        os.makedirs(target_root, exist_ok=True)

        for file in files:
            src_file = os.path.join(root, file)
            dst_file = os.path.join(target_root, file)
            copy(src_file, dst_file)

class chdir:
    pwd: str
    dir: str

    def __init__(self, dir: str) -> None:
        self.pwd = os.getcwd()
        self.dir = dir

    def __enter__(self) -> None:
        logger.info(f"$ cd {self.dir}")
        self.pwd = os.getcwd()
        os.chdir(self.dir)

    def __exit__(self, *_) -> None:
        logger.info(f"$ cd {self.pwd}")
        os.chdir(self.pwd)

