from collections import defaultdict
import typer

from git_tool.feature_data.analyze_feature_data.feature_utils import (
    get_commits_with_feature,
)
from git_tool.feature_data.git_status_per_feature import (
    get_features_for_file,
    get_files_by_git_change,
)
from git_tool.feature_data.models_and_context.feature_state import (
    read_staged_featureset,
)
from git_tool.feature_data.models_and_context.repo_context import (
    get_all_commits,
    get_commit_title,
)


WITHOUT_FEATURE = "Without Feature"

app = typer.Typer(no_args_is_help=True)


@app.command()
def feature_status():
    """
    Displays unstaged and staged changes with associated features.
    """
    changes = get_files_by_git_change()

    def group_files_by_feature(files: list[str]):
        feature_dict = defaultdict(list)
        for file in files:
            features = get_features_for_file(file)
            if not features:
                features = [WITHOUT_FEATURE]
            for feature in features:
                feature_dict[feature].append(file)
        return feature_dict

    def print_changes(
        change_type: str, files: list[str], staged_features: list[str] = []
    ):
        feature_dict = group_files_by_feature(files)
        typer.echo(f"{change_type.replace('_', ' ').title()}:")
        for feature, files in feature_dict.items():
            typer.echo(f"\t{feature}:")
            if feature == WITHOUT_FEATURE:
                typer.echo(
                    """\t (To assign a feature, run git feature-add <filename> <feature>)"""
                )
            for file in files:
                typer.echo(f"\t\t{file}")

    printed = False

    if len(changes.get("staged_files", [])) > 0:
        printed = True

        staged_features = read_staged_featureset()
        print(
            f"Staged Features (associated, but not staged features for a file are in parenthesis)"
        )
        typer.echo(*staged_features, sep=",")
        typer.echo("Feature changes to be committed")
        for item in changes["staged_files"]:
            additional_features = get_features_for_file(item)
            unstaged_features = [
                f for f in additional_features if not f in staged_features
            ]
            if unstaged_features:
                non_staged_str = f" ({', '.join(unstaged_features)})"
            else:
                non_staged_str = ""
            typer.echo(f"\t{item} {non_staged_str}")

    if len(changes.get("unstaged_files", [])) > 0:
        printed = True
        print_changes(
            "Feature changes not staged for commit", changes["unstaged_files"]
        )

    if len(changes.get("untracked_files", [])) > 0:
        printed = True
        print_changes("Untracked files", changes["untracked_files"])

    if not printed:
        typer.echo("No changes.")


def is_commit_in_list(commit_id: str, commit_id_list: list[str]) -> bool:
    for commit in commit_id_list:
        min_length = min(len(commit_id), len(commit))
        if commit_id[:min_length] == commit[:min_length]:
            return True

    return False


@app.command()
def find_commits_without_feature(
    message=typer.Option(default=False, help="Display title of commit")
):
    """
    Find all commits that don't have any associated feature information.
    """
    all_commits = get_all_commits()
    feature_commits = get_commits_with_feature()
    if not feature_commits:
        return
    commits_without_feature = []
    for commit in all_commits:
        if not is_commit_in_list(commit, feature_commits):
            commits_without_feature.append(commit)

    if message:
        commits_without_feature = [
            f"{commit}: {get_commit_title(commit)}"
            for commit in commits_without_feature
        ]

    if commits_without_feature:
        typer.echo("Commits without feature association:")
        for commit in commits_without_feature:
            typer.echo(commit)
    else:
        typer.echo("All commits have feature associations.")


@app.command()
def find_commits_with_feature():
    feature_commits = get_commits_with_feature()
    typer.echo("Commits with feature association:")
    for commit in feature_commits:
        typer.echo(commit)
