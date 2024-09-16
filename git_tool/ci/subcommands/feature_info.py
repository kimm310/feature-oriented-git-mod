import typer

from git_tool.feature_data.analyze_feature_data.feature_utils import (
    get_commits_for_feature_on_other_branches,
    get_current_branchname,
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


app = typer.Typer(help="Displaying feature information for the entire git repo")

info_app = typer.Typer(help="Inspect feature details")
currently_staged_app = typer.Typer(
    help="List all features that are touched by staged changes"
)
app.add_typer(info_app, name="info")
app.add_typer(currently_staged_app, name="currently-staged")


@currently_staged_app.command(name=None)
def get_stuff():
    typer.echo("Currently staged")
    print_list_w_indent(read_staged_featureset())
    return


@app.command(name=None)
def inspect_feature(
    feature: str = typer.Argument(None, help="Inspect a particular feature"),
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
    typer.echo(f"Collecting information for feature {feature}")
    try:
        commit_ids = get_commits_for_feature(feature)
        print_list_w_indent(commit_ids)
    except Exception:
        commit_ids = []
        typer.echo(f"No commit-ids for feature {feature} found")
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
        typer.echo(
            f"Evaluating if feature {feature} can be updated on current branch {get_current_branchname()}"
        )
        if branch:
            typer.echo(
                f"Comparing commits for the feature '{feature}' on the current branch '{current_branch}' with branch '{branch}'"
            )
            try:
                other_commits = get_commits_for_feature_on_other_branches(
                    feature_commits=commit_ids, other_branch=branch
                )
                if other_commits:
                    typer.echo(
                        f"Found {len(other_commits)} commits for feature '{feature}' on branch '{branch}'."
                    )
                    for commit in other_commits:
                        typer.echo(
                            f"{commit.hexsha[:7]} - {commit.message.splitlines()[0]}"
                        )

                else:
                    typer.echo(
                        f"No commits found for feature '{feature}' on branch '{branch}'."
                    )
            except Exception as e:
                typer.secho(
                    f"Error retrieving commits for branch '{branch}': {e}",
                    fg=typer.colors.RED,
                )
        else:
            typer.echo(
                f"Comparing commits for the feature '{feature}' on all other branches with the current branch '{get_current_branchname()}'"
            )
            try:
                other_commits = get_commits_for_feature_on_other_branches(
                    feature_commits=commit_ids
                )
                if other_commits:
                    typer.echo(
                        f"Found {len(other_commits)} commits for feature '{feature}' on other branches."
                    )
                    for commit in other_commits:
                        typer.echo(
                            f"{commit.hexsha[:7]} - {commit.message.splitlines()[0]}"
                        )
                else:
                    typer.echo(
                        f"No commits found for feature '{feature}' on other branches."
                    )
            except Exception as e:
                typer.secho(
                    f"Error retrieving commits for other branches: {e}",
                    fg=typer.colors.RED,
                )


@app.command(name=None)
def all_feature_info():
    """
    Inspects feature information.
    """
    typer.echo("All Features")
    print_list_w_indent(_get_feature_uuids())


if __name__ == "__main__":
    app()
