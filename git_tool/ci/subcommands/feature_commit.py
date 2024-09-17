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


app = typer.Typer(
    no_args_is_help=True,
    help="Associate an existing commit with one or more features",
)


@app.command(name=None)
def feature_commit(
    commit: str = typer.Argument(
        ...,
        help="Provide the commit-id that the feature information should belong to.",
    ),
    features: list[str] = typer.Option(
        None,
        help="Manually specify feature names. \
            If this option is provided, staged feature information will be ignored.",
    ),
):
    """
    Associate feature information with a regular git commit.
    This command is a plumbing command, usually this would be happening automatically when
    setting up git hooks.
    """
    typer.echo("Step 1: select commit to assign information to")
    typer.echo(f"\t Commit is {commit}")
    typer.echo("Step 2: Select feature information")
    if not features:
        staged_features = read_staged_featureset()
        typer.echo(f"\t Selecting staged features {staged_features}")
        if not staged_features:
            typer.echo("No staged feature information available.", err=True)
            return
    else:
        staged_features = features
        typer.echo(
            f"\t Selecting features from cli parameters {staged_features}"
        )
    # typer.echo("Step 3: Add a feature meta commit on meta data branch")
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
        typer.echo("Feature meta commit added successfully.")
    # typer.echo("Step 4: Cleanup all information/ internal state stuff")
    reset_staged_featureset()
    # typer.echo("Feature commit process completed successfully.")
