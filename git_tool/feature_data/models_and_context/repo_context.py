import os
from contextlib import contextmanager
from pathlib import Path
from typing import Generator, Iterable, Tuple

import git
from dotenv import load_dotenv

load_dotenv(Path(__file__).parents[1].joinpath(".env").absolute())
# FEATURE_BRANCH_NAME = os.getenv("BRANCH_NAME", "feature-metadata")
FEATURE_BRANCH_NAME = "feature6-metadata"
MAIN_BRANCH_NAME = os.getenv("MAIN_BRANCH_NAME", "main")
REPO_PATH = os.getenv("REPO_PATH", os.getcwd())
assert FEATURE_BRANCH_NAME is not None
assert MAIN_BRANCH_NAME is not None
assert REPO_PATH is not None


@contextmanager
def repo_context(repo_path=REPO_PATH):
    repo = git.Repo(repo_path)
    try:
        yield repo
    finally:
        del repo


@contextmanager
def branch_folder_list(
    branch: str = FEATURE_BRANCH_NAME, repo_path: str = REPO_PATH
) -> Generator[Tuple[Iterable[Path], git.Repo], None, None]:
    """
    Get all folders in a branch. Standard is to list all feature folders
    in the feature metadata branch.

    Args:
        branch (str): Branch that is analysed for folders
        repo_path (str): Path to git repo

    Yields:
        Tuple[Iterable[Path], git.Repo]: A tuple where the first element is an
        iterable of feature folder paths as pathlib.Path objects, and the second element is the git repository object.
    """
    with repo_context(repo_path) as repo:
        try:
            feature_folders = repo.git.ls_tree(
                "-d", "--name-only", branch
            ).split()
            feature_folders = map(Path, feature_folders)
            yield feature_folders, repo
        finally:
            pass

def get_current_branch()->str:
    with repo_context() as repo:
        return repo.active_branch.name


def get_yes_no_input(prompt: str) -> bool:
    while True:
        response = input(prompt).strip().lower()
        if response in ["yes", "y"]:
            return True
        elif response in ["no", "n"]:
            return False
        else:
            print("Please enter 'yes' or 'no'.")
