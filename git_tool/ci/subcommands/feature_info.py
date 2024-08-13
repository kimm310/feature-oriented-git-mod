import typer

from git_tool.feature_data.models_and_context.feature_state import (
    read_staged_featureset,
)
from git_tool.feature_data.models_and_context.repo_context import repo_context
from git_tool.feature_data.read_feature_data.parse_data import (
    _get_feature_uuids,
)


def print_list_w_indent(stuff: list, indent: int = 1) -> None:
    for item in stuff:
        print("\t" * indent + item)


app = typer.Typer()


@app.command()
def feature_info(
    all: bool = typer.Option(False, help="Get all features"),
    currently_staged: bool = typer.Option(
        False, help="List all features that are touched by staged changes"
    ),
    feature: str = typer.Option(None, help="Inspect a particular feature"),
    authors: bool = typer.Option(
        False, help="Include authors in the inspection"
    ),
    files: bool = typer.Option(False, help="Include files in the inspection"),
    updatable: bool = typer.Option(
        False,
        help="Display whether the feature can be updated and what update options there are",
    ),
    branch: str = typer.Option(
        None,
        help="Specify branch for inspection that should be compared to the currently checked out branch",
    ),
):
    """
    Inspects feature information.
    """
    if currently_staged:
        print(f"Currently staged {read_staged_featureset()}")
        return
    # print(
    #     f"Executing feature-info with all={all}, feature={feature}, authors={authors}, files={files}, updatable={updatable}, branch={branch}"
    # )
    if all:
        print("All Features")
        print_list_w_indent(_get_feature_uuids())
    elif feature:
        print(f"Collecting information for feautre {feature}")
        raise NotImplementedError
    print("Structured output")
    if branch:
        raise NotImplementedError
    if authors:
        raise NotImplementedError
    if files:
        raise NotImplementedError
