"""
This wraps the fast-import utils and writes the necessary code for determining all data artefacts
needed to add a FeatureFact to the respective metadata branch.
"""

from datetime import datetime
import hashlib
import tempfile
import uuid
from git import Actor, Repo, Commit
import sys
import os
from git import Actor, Repo


if __name__ == "__main__":

    sys.path.append(
        os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
    )


from git_tool.feature_data.repo_context import FEATURE_BRANCH_NAME

from git_tool.feature_data import repo_context
from git_tool.feature_data.fast_import_utils import (
    CommitData,
    CommitFileChange,
    to_fast_import_format,
)
from git_tool.feature_data.fact_model import (
    ChangeDetail,
    ChangeType,
    FeatureFactModel,
)


def generate_file_path(fact: FeatureFactModel) -> str:
    feature_uuid = str(uuid.uuid4())
    timestamp = fact.date.timestamp()
    commit_id = fact.commit
    fact_json = fact.json()
    sha1_hash = hashlib.sha1(fact_json.encode("utf-8")).hexdigest()
    return os.path.join(feature_uuid, str(int(timestamp)), commit_id, sha1_hash)


def generate_fact_filename(fact: FeatureFactModel) -> str:
    return f"{fact.feature}/{fact.date.isoformat()}"


def add_fact_to_metadata_branch(
    fact: FeatureFactModel, branch_name: str = FEATURE_BRANCH_NAME
):
    commit_data = CommitData(
        branch_name=branch_name,
        committer_name="test",
        committer_email="test@abc.de",
        message="Test",
        add_files=[
            CommitFileChange(
                file_path=generate_fact_filename(
                    fact=fact,
                ),
                content=fact.model_dump_json(),
            )
        ],
    )
    fast_import_content = to_fast_import_format(commits=[commit_data])
    try:
        with tempfile.NamedTemporaryFile(delete=False, mode="w") as temp_file:
            temp_file.write(fast_import_content)
            temp_file_path = temp_file.name

        with repo_context.repo_context() as repo:
            with open(temp_file_path, "r") as file:
                repo.git.fast_import(istream=file)
    finally:
        if temp_file_path:
            os.remove(temp_file_path)
    return commit_data


if __name__ == "__main__":
    commit = add_fact_to_metadata_branch(
        fact=FeatureFactModel(
            commit="test",
            authors=["Tabea"],
            date=datetime.now(),
            changes=[],
            feature="test",
        )
    )
