from collections import namedtuple
from typing import Dict, List, TypedDict
from git_tool.feature_data.models_and_context.repo_context import (
    branch_folder_list,
    repo_context,
)


class GitChanges(TypedDict):
    staged_files: List[str]
    unstaged_files: List[str]
    untracked_files: List[str]


GitStatusEntry = namedtuple("GitStatusEntry", ["status", "file_path"])


def get_files_by_git_change() -> GitChanges:
    """
    Retrieves files sorted by the type of git change (staged, unstaged, untracked).
    Can be used in combination with finding feature annotations for files to help
    figure out which features are already staged.

    Returns:
        Dict[str, List[str]]: A dictionary with keys 'staged_files', 'unstaged_files',
        and 'untracked_files', each containing a list of file paths.
    """

    def convert_to_status_entry(short_status_line: str) -> GitStatusEntry:
        return GitStatusEntry(short_status_line[:2], short_status_line[3:])

    with repo_context() as repo:
        result = repo.git.status("-s")
        lines = list(map(convert_to_status_entry, result.split("\n")))

        changes: GitChanges = {
            "staged_files": [
                entry.file_path
                for entry in lines
                if entry.status[0] != " " and entry.status != "??"
            ],
            "unstaged_files": [
                entry.file_path
                for entry in lines
                if entry.status[1] != " " and entry.status != "??"
            ],
            "untracked_files": [
                entry.file_path for entry in lines if entry.status == "??"
            ],
        }
        return changes


def get_features_for_file(
    file_path: str, use_annotations: bool = False
) -> List[str]:
    """
    Retrieves features for a given file.
    Annotations makes use of feature annotations only, searching for folder, file and line annotations.
    Otherwise, all commits that touch the selected file are used to search for the associated feature.

    Args:
        file_path (str): The path to the file.

    Returns:
        List[str]: A list of features associated with the file.
    """
    features = []
    if use_annotations:
        # TODO implement search for annotations
        return []
    else:
        # Get all commits touching this feature
        # Iterate through all feature folders and check if they contain the commit
        with repo_context() as repo:
            commits = repo.git.log("--pretty=format:%H", "--", file_path).split(
                "\n"
            )
        with branch_folder_list() as feature_folders:
            for commit in commits:
                for feature in feature_folders:
                    if commit_in_feature_folder(commit, feature):
                        features.append(get_feature_name_from_folder(feature))
    return features


def commit_in_feature_folder(commit: str, feature_folder: str) -> bool:
    """
    Check if a commit is present for a feature.

    Args:
        commit (str): The commit hash.
        feature_folder (str): The path to the feature folder.

    Returns:
        bool: True if the commit is present in the feature folder, False otherwise.
    """
    with repo_context() as repo:
        try:
            repo.git.rev_list("--objects", "--all", feature_folder, grep=commit)
            return True
        except:
            return False


def get_feature_for_hunk(file_path: str, hunk: str) -> List[str]:
    """
    Retrieves features for specific changes (hunks) in a given file.

    Args:
        file_path (str): The path to the file.
        hunk (str): The specific changes (hunks) in the file.

    Returns:
        List[str]: A list of features associated with the specific hunks in the file.
    """
    raise NotImplementedError()
    # features = get_features_for_hunk(file_path, hunk)
    # return features


def get_feature_name_from_folder(feature_folder: str) -> str:
    """
    Retrieve the feature name from a feature folder path.

    Args:
        feature_folder (str): The path to the feature folder.

    Returns:
        str: The name of the feature.
    """
    # Extract the feature name from the folder path
    return feature_folder.split("/")[-1]
