import typer

from git_tool.feature_data.models_and_context.feature_state import (
    read_staged_featureset,
)


app = typer.Typer()


@app.command()
def feature_commit_msg():
    """
    Generates feature information for the commit message.
    """
    staged_features = read_staged_featureset()

    if not staged_features:
        print("No features associated with the staged changes.")
        raise typer.Exit(code=1)

    feature_msg = f"Associated Features: {', '.join(staged_features)}"

    print(feature_msg)
