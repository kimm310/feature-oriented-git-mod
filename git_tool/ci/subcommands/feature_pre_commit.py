import typer

from git_tool.feature_data.git_status_per_feature import get_files_by_git_change
from git_tool.feature_data.models_and_context.feature_state import (
    read_staged_featureset,
)


app = typer.Typer()


@app.command()
def feature_pre_commit():
    """
    Checks if all staged changes are properly associated with features.
    Returns an error if any issues are found.
    """
    changes = get_files_by_git_change()

    if len(changes["staged_files"]) == 0:
        print("Error: No staged changes found.")
        raise typer.Exit(code=1)

    staged_features = read_staged_featureset()

    if not staged_features:
        print("Error: No features associated with the staged changes.")
        raise typer.Exit(code=1)

    print("Pre-commit checks passed.")
    raise typer.Exit(code=0)  #
