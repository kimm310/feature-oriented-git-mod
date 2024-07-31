from git import Commit

from git_tool.feature_data.models_and_context.repo_context import (
    FEATURE_BRANCH_NAME,
    repo_context,
)
from git_tool.feature_data.read_feature_data.parse_data import (
    _get_fact_from_featurefile,
)
from git_tool.feature_data.uuid_name_mapping import get_uuid_for_featurename


def get_commits_for_feature(feature_name: str) -> list[Commit]:
    commits = []
    feature_uuid = get_uuid_for_featurename(feature_name)
    with repo_context() as repo:
        for commit in repo.iter_commits(FEATURE_BRANCH_NAME):
            for file in commit.stats.files:
                fact = _get_fact_from_featurefile(file)
                if fact and feature_name in fact.features:
                    commits.append(commit)
    return commits


def get_features_for_commit() -> list[str]: ...


def get_commits_on_branch_wo_featurefact() -> list[str]: ...
