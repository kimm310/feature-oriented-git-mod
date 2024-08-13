import typer

from git_tool.feature_data.git_status_per_feature import (
    get_features_for_file,
    get_files_by_git_change,
)
from git_tool.feature_data.models_and_context.feature_state import (
    reset_staged_featureset,
    write_staged_featureset,
)
from git_tool.feature_data.models_and_context.repo_context import repo_context

app = typer.Typer()


@app.command()
def feature_add(
    feature_names: list[str],
    from_annotations: bool = typer.Option(
        False, help="Stage changes based on feature annotations"
    ),
    from_files: list[str] = typer.Option(
        [],
        help="""Specify the set of files you want to annotate. Note that files listet that are not staged will be added to the staging area""",
    ),
    from_staged: bool = typer.Option(
        False, help="Use the staged files only to add feature information"
    ),
    add_annotations: bool = typer.Option(
        False,
        help="Sets whether the changes will be grouped with feature annotations",
    ),
):
    """
    Stages changes for a specific feature.
    """
    if isinstance(feature_names, str):
        feature_names = [feature_names]
    if from_annotations:
        typer.echo("use annotations")
        raise NotImplementedError
    elif from_staged:
        feature_names = read_features_from_staged()
    elif from_files:
        if not stage_files(selected_files=from_files):
            return
    else:
        typer.echo("no specific option selected")
        return
    if is_staging_area_empty():
        return
    create_feature_meta_info(
        features=feature_names, insert_annotations=add_annotations
    )


def read_features_from_staged(type: str = "Union") -> list[str]:
    """
    Retrieve the features from the current staging area

    Keyword Arguments:
        type -- Can be Union or Intersection. Describes how multiple features will be combined (default: {"Union"})

    Returns:
        List of features
    """
    typer.echo("Use staged files")

    staged_files = get_files_by_git_change().get("staged_files", [])
    feature_sets = [set(get_features_for_file(f)) for f in staged_files]

    if not feature_sets:
        return []

    if type == "Union":
        combined_features = set.union(*feature_sets)
    elif type == "Intersection":
        combined_features = set.intersection(*feature_sets)
    else:
        raise ValueError(
            "Invalid type specified. Use 'Union' or 'Intersection'."
        )

    return list(combined_features)


def stage_files(selected_files: list[str]) -> bool:
    """
    Stage all selected files and return whether the staging area has changed.
    If not, this indicates that no furhter feature things need do be done.

    Arguments:
        selected_files -- List of file identifiers that git understands for git add

    Returns:
        Boolean whether there were acutally new staged changes
    """
    typer.echo("use files")
    with repo_context() as repo:
        for file in selected_files:
            try:
                initial_diff = repo.git.diff("--cached")
                repo.git.add(file)
                typer.echo(f"Staged file: {file}")
                final_diff = repo.git.diff("--cached")
                if initial_diff == final_diff:
                    typer.echo(
                        "No changes were made to the staging area. Aborting.",
                        err=True,
                    )
                    return False
                return True
            except Exception as e:
                typer.echo(f"Error staging file {file}: {e}")
    return False


def is_staging_area_empty() -> bool:
    typer.echo("Check if there are staged files")
    changes = get_files_by_git_change()

    if len(changes["staged_files"]) == 0:
        typer.echo(
            "No staged changes, so no feature information to add", err=True
        )
        reset_staged_featureset()
        return True
    else:
        return False


def create_feature_meta_info(
    features: list[str], insert_annotations: bool = False
):
    typer.echo(f"Adding feature information {features} to staged files")
    write_staged_featureset(features)
    if insert_annotations:
        typer.echo("Not adding annotations, not implemented yet", err=True)
