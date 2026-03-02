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

