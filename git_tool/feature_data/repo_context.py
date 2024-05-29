from contextlib import contextmanager
import functools
import logging
import os
from typing import Any, Callable
from dotenv import load_dotenv
import git

load_dotenv(
    "/home/tabea/Uni/worktree/inital-experiments/git_tool/feature_data/.env"
)
FEATURE_BRANCH_NAME = os.getenv("BRANCH_NAME")
MAIN_BRANCH_NAME = os.getenv("MAIN_BRANCH_NAME")
REPO_PATH = os.getenv("REPO_PATH")
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


def get_yes_no_input(prompt: str) -> bool:
    while True:
        response = input(prompt).strip().lower()
        if response in ["yes", "y"]:
            return True
        elif response in ["no", "n"]:
            return False
        else:
            print("Please enter 'yes' or 'no'.")
