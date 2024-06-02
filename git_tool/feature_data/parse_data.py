import os
from typing import Generator, Optional
import logging


if __name__ == "__main__":
    import sys
    import os

    sys.path.append(
        os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
    )

    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
        handlers=[
            logging.FileHandler("debug.log"),
            logging.StreamHandler(),
        ],
    )

from git_tool.feature_data.repo_context import (
    FEATURE_BRANCH_NAME,
    repo_context,
)
from git_tool.feature_data.fact_model import (
    FeatureFactModel,
)


def _get_associated_files(
    feature_uuid: str, ref_commit: Optional[str] = None
) -> Generator[str, None, None]:
    """Search for all files belonging to a certain feature_uuid. Assume that all files are
    stored in the folder with the name feature_uuid

    Args:
        feature_uuid (str): Identifier for feature
        ref_commit (Optional[str], optional): Last interesting commit. Defaults to None, behaves as
                                                if HEAD of main is used

    Returns:
        Generator[str, None, None]: Iterator over all filenames associated with the feature
    """
    with repo_context() as repo:
        # repo.git always allows to execute git commands, see
        # https://gitpython.readthedocs.io/en/stable/tutorial.html#using-git-directly
        result: str = repo.git.ls_tree(
            "-r", FEATURE_BRANCH_NAME, name_only=True
        )
        files: list[str] = (
            result.split()
        )  # outputs one string. Filenames are separated by whitespace-like delimiters
        files = filter(lambda x: x.startswith(feature_uuid), files)
        return files


def _get_fact_from_featurefile(filename: str) -> FeatureFactModel:
    with repo_context() as repo:
        return FeatureFactModel.model_validate_json(
            repo.git.show(f"{FEATURE_BRANCH_NAME}:{filename}")
        )


def _get_feature_uuids() -> list[str]:
    """
    Each feature has its own folder where the foldername is equivalent to the uuid that the
    feature has.
    Get all directories at the upper level of the Feature data branch

    Returns:
        list[str]: _description_
    """
    with repo_context() as repo:
        folder_string = repo.git.ls_tree(
            "-r", "-d", FEATURE_BRANCH_NAME, name_only=True
        )
        folders = folder_string.split()
        return folders


# def _resolve_feature_name(feature_uuid):
#     facts = get_metadata(feature_uuid)
#     name_changes = []
#     for fact in facts:
#         for change in fact.changes:
#             if change["feature_name"] is not None:
#                 name_changes.append(change)
#     return name_changes


def get_metadata(
    feature_uuid: str, ref_commit: Optional[str] = None
) -> list[FeatureFactModel]:
    """
    Get all facts about the feature that are true for ref_commit.
    If ref_commit is not specified, use latest commit.
    Output describes cummulation of all facts and can be used as foundation to display
    feature evolution.
    Only facts that are merged in the main branch are used. Currently, the name must be main.

    Args:
        feature_uuid (str): Feature Reference
        ref_commit (Optional[str]): Commit Identifier which is the last one

    Returns:
        CumulatedFactsModel: List of all facts sorted chronologically
    """
    facts = [
        _get_fact_from_featurefile(f)
        for f in _get_associated_files(
            feature_uuid=feature_uuid, ref_commit=ref_commit
        )
    ]
    return facts


def get_feature_log(feature_uuid: str):
    """
    Output all commits from a feature to the command line.
    # TODO Still need to incorpoarte all possible flags of git log somehow

    Args:
        feature_uuid (str): Reference for feature
    """
    commit_ids = [
        fact.commit for fact in get_metadata(feature_uuid=feature_uuid)
    ]
    with repo_context() as repo:
        print(
            repo.git.log(
                "--graph",
                "--oneline",
                "--all",
                "--decorate",
                "--color",
                commit_ids,
            )
        )


if __name__ == "__main__":
    # get_metadata("abc")
    # logging.info("Get Metadata success")
    # get_feature_log("abc")
    ids = _get_feature_uuids()
    print(ids)
    # if len(ids) >= 1:
    #     _resolve_feature_name(ids[0])
    get_feature_log("test")
