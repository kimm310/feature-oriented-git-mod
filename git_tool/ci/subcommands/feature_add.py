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
from git_tool.finding_features import features_for_file_by_annotation

app = typer.Typer(no_args_is_help=True)


@app.command("by-add", no_args_is_help=True)
def feature_add_by_add(
    feature_names: list[str] = typer.Argument(
        None, help="List of feature names to associate with the staged files"
    ),
    all_files: bool = typer.Option(
        False,
        "--all",
        "-a",
        help="Stage all tracked changes and associate with features",
    ),
    selected_files: list[str] = typer.Option(
        None,
        "--files",
        "-f",
        help="Specify a list of files to stage and associate with features",
    ),
):
    """
    Stage specific files or all files and associate them with the provided features.
    """
    if all_files:
        typer.echo("Staging all files and associating with features")
        # Logic to stage all files (e.g., repo.git.add("."))
        stage_files(get_files_by_git_change().get("tracked_files", []))
    elif selected_files:
        typer.echo(f"Staging selected files: {selected_files}")
        stage_files(selected_files)
    else:
        typer.echo("No files selected. Use --all or --files.", err=True)
        return

    if feature_names:
        typer.echo(f"Associating features: {feature_names}")
        # Logic to associate features with staged files
    else:
        typer.echo("No features provided.", err=True)


@app.command("from-staged")
def features_from_staging_area():
    """
    Use the staged files to add feature information.
    """
    feature_names = read_features_from_staged()
    if feature_names:
        typer.echo(f"Features in staging area: {feature_names}")
        create_feature_meta_info(feature_names)
    else:
        typer.echo("No features found in staging area.", err=True)


@app.command()
def feature_add(
    feature_names: list[str] = typer.Argument(
        None, help="List of feature names to associate with the changes"
    ),
    from_annotations: bool = typer.Option(
        False,
        help="Stage all changes based on feature annotations.",
    ),
    from_files: list[str] = typer.Option(
        None,
        "--files",
        "-f",
        help="Specify a set of files to annotate. Files not staged will be added to the staging area.",
    ),
    from_staged: bool = typer.Option(
        False,
        "--staged",
        "-s",
        help="Use the staged files only to add feature information.",
    ),
    annotate: bool = typer.Option(
        False,
        "--annotate",
        "-a",
        help="Group the changes with feature annotations.",
    ),
):
    """
    Stages changes for a specific feature. You can select changes from annotations, files, or staged content.
    """
    if from_annotations:
        typer.echo("Staging based on annotations")
        files = get_files_by_git_change().get(
            "unstaged_files", []
        ) + get_files_by_git_change().get("untracked_files", [])
        all_features = [
            feature
            for file in files
            for feature in features_for_file_by_annotation(file_name=file)
        ]
        stage_files(files)
        feature_names = list(set(all_features))
    elif from_staged:
        feature_names = read_features_from_staged()
    elif from_files:
        if len(feature_names) == 0:
            typer.echo("No features chosen, abort", err=True)
            return
        if not stage_files(selected_files=from_files):
            return

    if is_staging_area_empty():
        return

    create_feature_meta_info(
        features=feature_names, insert_annotations=annotate
    )


def read_features_from_staged(type: str = "Union") -> list[str]:
    """
    Retrieve the features from the current staging area.

    Keyword Arguments:
        type -- Can be Union or Intersection. Describes how multiple features will be combined (default: {"Union"})

    Returns:
        List of features.
    """
    typer.echo("Using staged files")

    staged_files = get_files_by_git_change().get("staged_files", [])
    feature_sets = list(
        set(
            feature
            for f in staged_files
            for feature in get_features_for_file(f)
        )
    )

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

    Arguments:
        selected_files -- List of file identifiers that git understands for git add

    Returns:
        Boolean whether there were actually new staged changes.
    """
    typer.echo("Staging files")
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
    typer.echo("Checking if there are staged files")
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


if __name__ == "__main__":
    app()
