import os
import logging
from .shell_utils import run, rmtree, chdir
from subprocess import CalledProcessError

logger = logging.getLogger(__name__)

def clone_repo(remote: str, branch: str, dir: str) -> bool:
    try:
        _ = run(f"git clone --branch {branch} {remote} {dir} -q --depth 1")
        return True
    except CalledProcessError as e:
        logger.info(f"failed to clone repo {remote} to {dir}: {e}")
        return False

def sync_repo(remote: str, branch: str, dir: str) -> None:
    """Synchronize a local git repository in a particular directory.

    If the directory doesn't exist, this will create it and clone the repo fresh
    If the directory exists, this will try to run `$ git pull`. If that fails, 
    it will delete the directory and clone it afresh.
    """

    if not os.path.isdir(dir):
        logger.info(f"directory {dir} doesn't exist. cloning afresh.")
        os.makedirs(dir)
        if clone_repo(remote, branch, dir): 
            return
        logger.info(f"skipping {remote} due to failed clone")

    with chdir(dir):
        try:
            logger.info(f"{dir} exists, pulling changes.")
            _ = run("git pull")
        except CalledProcessError as e:
            logger.info(f"cloning afresh due to failed pull: {e}")
            rmtree(dir)
            if clone_repo(remote, branch, dir):
                return
            logger.info(f"skipping {remote} due to failed clone")

