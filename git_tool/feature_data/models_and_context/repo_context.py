from datetime import datetime
import os
import tempfile
from contextlib import contextmanager
from functools import wraps
from pathlib import Path
from typing import Generator, Iterable, Tuple

import git
from dotenv import load_dotenv

load_dotenv(Path(__file__).parents[1].joinpath(".env").absolute())
FEATURE_BRANCH_NAME = os.getenv("BRANCH_NAME", "feature-metadata")
# FEATURE_BRANCH_NAME = "feature6-metadata"
MAIN_BRANCH_NAME = os.getenv("MAIN_BRANCH_NAME", "main")
REPO_PATH = os.getenv("REPO_PATH", os.getcwd())
assert FEATURE_BRANCH_NAME is not None
assert MAIN_BRANCH_NAME is not None
assert REPO_PATH is not None

# print(f"FEATURE_BRANCH_NAME: {FEATURE_BRANCH_NAME}")
# print(f"MAIN_BRANCH_NAME: {MAIN_BRANCH_NAME}")
# print(f"REPO_PATH: {REPO_PATH}")


def create_empty_branch(branch_name: str, repo: git.Repo) -> str:
    """
    Create an orphan branch without checking it out using fast-import. An orphan branch
    does not have any parent commits.

    Args:
        branch_name (str): The name of the branch to create.
        repo (git.Repo): The Git repository object.

    Returns:
        str: The fast-import script as a string.
    """
    timestamp = int(datetime.now().timestamp())
    committer_name = os.getenv("GIT_COMMITTER_NAME", "Unknown")
    committer_email = os.getenv("GIT_COMMITTER_EMAIL", "unknown@example.com")

    result = []
    result.append(f"commit refs/heads/{branch_name}")
    result.append(
        f"committer {committer_name} <{committer_email}> {timestamp} +0000"
    )
    result.append("data <<EOM")
    result.append(f"Initial empty commit for {branch_name}")
    result.append("EOM")

    fast_import_script = "\n".join(result)

    try:
        with tempfile.NamedTemporaryFile(
            delete=False, mode="w", encoding="utf-8", newline="\n"
        ) as temp_file:
            temp_file.write(fast_import_script)
            temp_file_path = temp_file.name

        with open(temp_file_path, "r", encoding="utf-8") as file:
            repo.git.fast_import(istream=file)
            try:
                repo.git.push("-u", "origin", branch_name)
            except Exception:
                ...
                # If origin is not defined yet, I can't set an upstream. Will need to do this manually elsewhere
        print(f"Branch {branch_name} successfully created.")
    except Exception as e:
        print(f"Error while creating branch: {e}")
    finally:
        if temp_file_path:
            os.remove(temp_file_path)

    return fast_import_script


def ensure_feature_branch(func):
    """
    Decorator to ensure that the feature branch is created if it does not exist.
    This will only be executed once, even if the context manager is called multiple times.
    """

    @wraps(func)
    def wrapper(*args, **kwargs):
        repo = git.Repo(REPO_PATH)
        # print("Executing ensure feautre branch")
        if FEATURE_BRANCH_NAME not in repo.heads:
            # print(
            #     f"Branch {FEATURE_BRANCH_NAME} existiert nicht. Erstelle neuen Branch ohne Eltern."
            # )
            create_empty_branch(FEATURE_BRANCH_NAME, repo)
            # print("new heads ", repo.heads)
        return func(*args, **kwargs)

    return wrapper


@ensure_feature_branch
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
            ).split("\n")
            yield feature_folders, repo
        finally:
            pass


def get_current_branch() -> str:
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


def get_all_commits() -> list[str]:
    with repo_context() as repo:
        all_commits = repo.git.log(
            "--all", f"--not {FEATURE_BRANCH_NAME}", "--pretty=format:%H"
        )
        commit_list = all_commits.splitlines()
        return commit_list


def get_commit_title(commit_id: str) -> str:
    with repo_context() as repo:
        return repo.git.log("--oneline", commit_id)
