import logging
import os
import sys
from typing import List, Set

if __name__ == "__main__":
    sys.path.append(
        os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
    )

from git import Commit, Tuple
from git_tool.feature_data.parse_data import get_features_touched_by_commit
from git_tool.feature_data.repo_context import repo_context


def get_feature_sets_for_branch(branch_name: str) -> List[Set[str]]:
    """
    Retrieves the sets of features touched together in a branch.

    Args:
        branch_name (str): The branch to analyze.

    Returns:
        List[Set[str]]: List of sets of features touched together in the branch.
    """
    with repo_context() as repo:
        commits = list(repo.iter_commits(branch_name))
        feature_sets = [
            get_features_touched_by_commit(commit) for commit in commits
        ]
    return feature_sets


def is_commit_compatible_with_branch(
    commit: Commit, branch_name: str
) -> Tuple[bool, Set[str]]:
    """
    Checks if a commit is compatible with a branch.
    Compatible means that the features touched by a commit
    are a subset of the features touched by the branch

    Args:
        commit (Commit): The commit to check.
        branch_name (str): The branch to check against.

    Returns:
        Tuple[bool, Set[str]]: Whether the commit is compatible and the set of features it touches.
    """
    commit_features = get_features_touched_by_commit(commit)
    branch_feature_sets = get_feature_sets_for_branch(branch_name)

    for feature_set in branch_feature_sets:
        if commit_features.issubset(feature_set):
            return (True, commit_features)
    return (False, commit_features)


def display_results_and_check_warnings(commit: Commit, branch_name: str):
    """
    Displays the feature set result to the user and gives warnings or errors depending on the result.

    Args:
        commit (Commit): The commit to analyze.
        branch_name (str): The branch to check against.
    """
    is_compatible, commit_features = is_commit_compatible_with_branch(
        commit, branch_name
    )
    if is_compatible:
        print(f"Commit {commit} is compatible with branch {branch_name}.")
    else:
        print(f"Commit {commit} is NOT compatible with branch {branch_name}.")
        print(f"Touched features: {commit_features}")
        logging.warning(
            f"Commit {commit} touches features not fully compatible with branch {branch_name}."
        )


if __name__ == "__main__":
    # is commit applicable to branch
    # define compatible notion: touching the same set of features. if the set is not equivalent,
    # test if the set of commit is subset of branch
    # display the feature-set result to user
    # give warning or error depending on result

    # redo this for multiple commits

    # retrieve feature sets for a branch: list of tuples of features that are touched together.
    # maybe even check for feature config.
    # assume that if two features were touched, the config is a^b
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
        handlers=[
            logging.FileHandler("debug.log"),
            logging.StreamHandler(),
        ],
    )

    branch_name = "inital-experiments"  # Beispielbranchname
    other_commit = input("Get commit-like format")
    with repo_context() as repo:
        display_results_and_check_warnings(other_commit, branch_name)
