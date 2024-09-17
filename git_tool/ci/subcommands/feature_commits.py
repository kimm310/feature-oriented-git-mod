import typer
from git_tool.ci.subcommands.feature_status import is_commit_in_list
from git_tool.feature_data.analyze_feature_data.feature_utils import (
    get_commits_with_feature,
)
from git_tool.feature_data.models_and_context.repo_context import (
    get_all_commits,
    get_commit_title,
    repo_context,
)

app = typer.Typer(
    no_args_is_help=True, help="Manage commits with feature associations."
)


@app.command(name="list")
def find_commits_with_feature(
    message: bool = typer.Option(
        False,
        help="Display the commit message/title along with the commit hash.",
    ),
):
    """
    Find all commits that have feature information associated.
    """
    feature_commits = get_commits_with_feature()

    if not feature_commits:
        typer.echo("No commits with feature associations found.")
        return

    typer.echo("Commits with feature association:")
    with repo_context() as repo:
        for commit in feature_commits:
            try:
                commit_obj = repo.commit(commit)
            except:
                typer.echo(f"Could not work with {commit}", err=True)
                continue
            if message:
                typer.echo(f"{commit_obj.hexsha}: {get_commit_title(commit)}")
            else:
                typer.echo(commit_obj.hexsha)  # Output the full commit hash


@app.command(name="missing")
def find_commits_without_feature(
    message: bool = typer.Option(
        False,
        help="Display the commit message/title along with the commit hash.",
    ),
):
    """
    Find all commits that don't have any associated feature information.
    """
    all_commits = get_all_commits()
    feature_commits = get_commits_with_feature()

    if not feature_commits:
        typer.echo("No feature commits found.")
        return

    commits_without_feature = [
        commit
        for commit in all_commits
        if not is_commit_in_list(commit, feature_commits)
    ]

    if not commits_without_feature:
        typer.echo("All commits have feature associations.")
        return

    typer.echo("Commits without feature association:")
    with repo_context() as repo:
        for commit in commits_without_feature:
            try:
                commit_obj = repo.commit(commit)
            except:
                commit_obj = {"hexsha": "ERROR"}
            if message:
                typer.echo(f"{commit_obj.hexsha}: {get_commit_title(commit)}")
            else:
                typer.echo(commit_obj.hexsha)  # Output the full commit hash


if __name__ == "__main__":
    app()
