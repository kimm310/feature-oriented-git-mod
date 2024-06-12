"""
All functions working on feature-uuids that help to get data in a structured format
based on a given feature
"""

from datetime import datetime
from typing import Generator, Optional
import uuid

from git_tool.feature_data.fact_model import get_fact_from_featurefile
from git_tool.feature_data.repo_context import FEATURE_BRANCH_NAME, repo_context


class FeatureNameNotFoundException(Exception): ...


def get_associated_files(feature_uuid: str) -> Generator[str, None, None]:
    """Search for all files belonging to a certain feature_uuid. Assume that all files are
    stored in the folder with the name feature_uuid

    Args:
        feature_uuid (str): Identifier for feature

    Returns:
        Generator[str, None, None]: Iterator over all filenames associated with the feature
    """
    with repo_context() as repo:
        # repo.git always allows to execute git commands, see
        # https://gitpython.readthedocs.io/en/stable/tutorial.html#using-git-directly
        result: str = repo.git.ls_tree(
            "-r", "--name_only", FEATURE_BRANCH_NAME, feature_uuid
        )
        files: list[str] = (
            result.split()
        )  # outputs one string. Filenames are separated by whitespace-like delimiters
        return files


def get_featurename_from_uuid(
    uuid: uuid.UUID,
) -> str | list[tuple[datetime, str]]:
    """
    Look through all changes associated with the feature uuid and check which ones
    changed the name

    Arguments:
        uuid -- Feature UUID

    Raises:
        FeatureNameNotFoundException: No Name Found for the feature

    Returns:
       If there is just one name, return the name. If there are multiple names, return
       tuples of name and timestamp so the context can decide which name to look for
    """
    feature_files = get_associated_files(feature_uuid=uuid)
    names: list[tuple[datetime, str]] = []
    for file in feature_files:
        fact = get_fact_from_featurefile(file)
        if fact.changes.name_change:
            names.append((fact.date, fact.changes.name_change.feature_name))
    if len(names) == 0:
        raise FeatureNameNotFoundException
    elif len(names) == 1:
        return names[0][1]
    else:
        return names


def get_uuid_for_featurename(name: str) -> uuid.UUID:
    """
    git log feature_metadata -S <string>  --name-only --pretty=format:
    lists the filenames of all files that contain the given string.
    They are sorted by commit and separated by a newline for each commit

    Arguments:
        name -- Featurename that is searched for
    Returns:
        UUID associated with the feautre
    """
    with repo_context() as repo:
        repo.git.log(
            FEATURE_BRANCH_NAME,
            f"-S {name}",
            name_only=True,
            one_line=True,
            pretty="format:",
        )
