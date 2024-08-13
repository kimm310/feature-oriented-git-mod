import typer

from git_tool.feature_data.git_status_per_feature import get_files_by_git_change
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
        print("use annotations")
        raise NotImplementedError
    elif from_staged:
        print("use staged files")
        raise NotImplementedError
    elif from_files:
        print("use files")
        # stage all unstaged files
        with repo_context() as repo:
            for file in from_files:
                try:
                    initial_diff = repo.git.diff("--cached")
                    repo.git.add(file)
                    print(f"Staged file: {file}")
                    final_diff = repo.git.diff("--cached")
                    if initial_diff == final_diff:
                        print(
                            "No changes were made to the staging area. Aborting."
                        )
                        return
                except Exception as e:
                    print(f"Error staging file {file}: {e}")
    else:
        print("no specific option selected")
        return
    print("Check if there are staged files")
    changes = get_files_by_git_change()
    if len(changes["staged_files"]) == 0:
        print("No staged changes, so no feature information to add")
        reset_staged_featureset()
        return
    print(f"Adding feature information {feature_names} to staged files")
    write_staged_featureset(features=feature_names)
    if add_annotations:
        print("Not adding annotations, not implemented yet")
