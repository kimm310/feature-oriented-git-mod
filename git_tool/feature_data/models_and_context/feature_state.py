"""
To prepare messages and store the set of features used, we need to create a file that contains all feature data.
"""

from pathlib import Path
from typing import List

from git_tool.feature_data.models_and_context.repo_context import repo_context


FEATUREINFO_FILE = Path(".git/FEATUREINFO")

def get_feature_file()-> Path:
    with repo_context() as repo:
        return Path(repo.git.rev_parse("--git-dir")).resolve().joinpath(FEATUREINFO_FILE)

def read_staged_featureset() -> List[str]:
    """
    Read the list of staged features from the FEATUREINFO file.

    Returns:
        List[str]: A list of staged features.
    """
    if not FEATUREINFO_FILE.exists():
        return []
    
    with FEATUREINFO_FILE.open(mode="r") as f:
        features = [line.strip() for line in f.readlines()]
    
    return features

def write_staged_featureset(features: List[str]):
    """
    Write the list of staged features to the FEATUREINFO file.

    Args:
        features (List[str]): A list of features to be written.
    """
    with FEATUREINFO_FILE.open(mode="w") as f:
        for feature in features:
            f.write(f"{feature}\n")

def reset_staged_featureset():
    """
    Reset the FEATUREINFO file by clearing its content.
    """
    if FEATUREINFO_FILE.exists():
        FEATUREINFO_FILE.unlink()