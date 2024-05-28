import os
from pathlib import Path
from typing import Any, Generator, Optional
import logging

import git

if __name__ == "__main__":
    import sys
    import os

    sys.path.append(
        os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
    )

    logging.basicConfig(
        level=logging.INFO,  # Set to DEBUG to capture all levels of log messages
        format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
        handlers=[
            logging.FileHandler("debug.log"),  # Log to a file named debug.log
            logging.StreamHandler(),  # Also log to console
        ],
    )

from git_tool.feature_data.branch_switching import (
    FEATURE_BRANCH_NAME,
    REPO_PATH,
    switch_to_feature_branch,
)
from git_tool.feature_data.fact_model import CumulatedFactsModel, FeatureFactModel


@switch_to_feature_branch()
def get_metadata(
    feature_uuid: str, ref_commit: Optional[str] = None
) -> CumulatedFactsModel:
    """Get all facts about the feature that are true for ref_commit. If ref_commit is not specified, use latest commit.
       Output describes cummulation of all facts and can be used as foundation to display feature evolution.
       Only facts that are merged in the main branch are used. Currently, the name must be main.

    Args:
        feature_uuid (str): Feature Reference
        ref_commit (Optional[str]): Commit Identifier which is the last one

    Returns:
        CumulatedFactsModel: List of all facts sorted chronologically
    """

    assert Path(feature_uuid).is_dir()
    for f in _get_associated_files(feature_uuid=feature_uuid, ref_commit=ref_commit):
        logging.info("Working on file %s for feature %s", f.name, feature_uuid)
        with open(f, "r") as cont:
            contents = cont.readlines()
            logging.debug(contents)


@switch_to_feature_branch()
def get_feature_log(feature_uuid: str):
    for f in _get_associated_files(feature_uuid=feature_uuid):
        with open(f, "r") as file:
            fact = FeatureFactModel.model_validate_json(file.read())
            logging.info("Retrieve fact for %s:\n\t %s", feature_uuid, fact)


def _get_associated_files(
    feature_uuid: str, ref_commit: Optional[str] = None
) -> Generator[Path, None, None]:
    """Search for all files belonging to a certain feature_uuid. Possibly filter depending on input arguments

    Args:
        feature_uuid (str): Identifier for feature
        ref_commit (Optional[str], optional): Last interesting commit. Defaults to None, behaves as if HEAD of main is used

    Returns:
        _type_: _description_

    Yields:
        Generator[Path, None, None]: _description_
    """
    assert git.Repo(REPO_PATH).active_branch.name == FEATURE_BRANCH_NAME
    associated_files = Path(feature_uuid).rglob(
        "**/*.json"
    )  # TODO this can have a better filter
    return associated_files


if __name__ == "__main__":
    # get_metadata("abc")
    # logging.info("Get Metadata success")
    get_feature_log("abc")
