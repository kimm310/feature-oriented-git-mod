from datetime import datetime
import typer

from git_tool.feature_data.add_feature_data.add_data import (
    add_fact_to_metadata_branch,
)
from git_tool.feature_data.models_and_context.fact_model import (
    ChangeHolder,
    FeatureFactModel,
)
from git_tool.feature_data.models_and_context.feature_state import (
    read_staged_featureset,
    reset_staged_featureset,
)
from git_tool.feature_data.models_and_context.repo_context import repo_context


app = typer.Typer()


@app.command()
def feature_commit(
    commit: str,
    features: list[str] = typer.Option(
        None,
        help="Add feature names manually. This ignores staged feature information",
    ),
):
    """
    Associate feature information with a regular git commit.
    This command is a plumbing command, usually this would be happening automatically when
    setting up git hooks.
    """
    print("Step 1: select commit to assign information to")
    print(f"\t Commit is {commit}")
    print("Step 2: Select feature information")
    if not features:
        staged_features = read_staged_featureset()
        print(f"\t Selecting staged features {staged_features}")
        if not staged_features:
            print("No staged feature information available.")
            return
    else:
        staged_features = features
        print(f"\t Selecting features from cli parameters {staged_features}")
    print("Step 3: Add a feature meta commit on meta data branch")
    with repo_context() as repo:
        commit_obj = repo.commit(commit)
        feature_fact = FeatureFactModel(
            commit=commit,
            authors=[commit_obj.author.name],
            date=datetime.now(),
            features=staged_features,
            changes=ChangeHolder(
                code_changes=[], constraint_changes=[], name_change=None
            ),
        )
        # Add the fact to the metadata branch
        add_fact_to_metadata_branch(fact=feature_fact, commit_ref=commit_obj)
        print("Feature meta commit added successfully.")
    print("Step 4: Cleanup all information/ internal state stuff")
    reset_staged_featureset()
    print("Feature commit process completed successfully.")
