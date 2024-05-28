from contextlib import contextmanager
import functools
import logging
import os
from typing import Any, Callable
from dotenv import load_dotenv
import git

load_dotenv("/home/tabea/Uni/worktree/inital-experiments/git_tool/feature_data/.env")
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


def switch_to_feature_branch(
    repo_path: str = REPO_PATH, feature_branch_name: str = FEATURE_BRANCH_NAME
) -> Callable:
    """Decorator to switch to the feature branch before executing the function and switch back afterward."""

    def decorator_switch(func: Callable) -> Callable:
        @functools.wraps(func)
        def wrapper_switch(*args, **kwargs) -> Any:
            repo = git.Repo(repo_path)
            current_branch = repo.active_branch
            logging.debug("Current active branch: %s", current_branch)
            try:
                repo.git.checkout(feature_branch_name)
                logging.debug("Switched to branch: %s", feature_branch_name)
                result = func(*args, **kwargs)
            except Exception as e:
                logging.error("Error in function %s: %s", func.__name__, e)
                raise
            finally:
                repo.git.checkout(current_branch)
                logging.debug("Switched back to branch: %s", current_branch)
            return result

        return wrapper_switch

    return decorator_switch
