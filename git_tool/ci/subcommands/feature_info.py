import typer

from git_tool.feature_data.analyze_feature_data.feature_utils import (
    get_commits_for_feature_on_other_branches,
)
from git_tool.feature_data.git_helper import (
    get_author_for_commit,
    get_branches_for_commit,
    get_files_for_commit,
)
from git_tool.feature_data.git_status_per_feature import get_commits_for_feature
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
    branches: bool = typer.Option(
        False, help="Display all branches containing the feautre"
    ),
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
        typer.echo("Currently staged")
        print_list_w_indent(read_staged_featureset())
        return
    # print(
    #     f"Executing feature-info with all={all}, feature={feature}, authors={authors}, files={files}, updatable={updatable}, branch={branch}"
    # )
    elif feature:
        typer.echo(f"Collecting information for feature {feature}")
        commit_ids = get_commits_for_feature(feature)
        print_list_w_indent(commit_ids)
        if branches:
            typer.echo(f"Branches (* indicates current branch)")
            branches = set(
                [
                    branch
                    for c in commit_ids
                    for branch in get_branches_for_commit(c)
                ]
            )
            print_list_w_indent(branches)
        if authors:
            typer.echo(f"Authors")
            authors = set([get_author_for_commit(c) for c in commit_ids])
            print_list_w_indent(authors)
        if files:
            typer.echo(f"Files")
            files = set(
                file for c in commit_ids for file in get_files_for_commit(c)
            )
            print_list_w_indent(files)
        if updatable:
            if branch:
                typer.echo(f"Commits for the same feature on branch {branch}")
                get_commits_for_feature_on_other_branches(
                    feature_commits=commit_ids, other_branch=branch
                )
            else:
                typer.echo("Commits for the same feature on other branches")
                get_commits_for_feature_on_other_branches(
                    feature_commits=commit_ids
                )
    if all | ((not feature) & (not currently_staged)):
        typer.echo("All Features")
        print_list_w_indent(_get_feature_uuids())
