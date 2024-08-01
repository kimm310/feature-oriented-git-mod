"""
Define the git subcommands that are available for users.
This contains the logic flow for the major building blocks of the application
"""
from collections import defaultdict
from typing import List
import typer
from git_tool.feature_data.git_status_per_feature import (
    get_features_for_file,
    get_files_by_git_change,
)
from git_tool.feature_data.models_and_context.feature_state import read_staged_featureset, reset_staged_featureset, write_staged_featureset
from git_tool.feature_data.models_and_context.repo_context import repo_context
from git_tool.feature_data.read_feature_data.parse_data import _get_feature_uuids

app = typer.Typer()

WITHOUT_FEATURE = "Without Feature"

def print_list_w_indent(stuff: list, indent: int = 1) -> None:
    for item in stuff:
        print('\t' * indent + item)


@app.command()
def feature_status():
    """
    Displays unstaged and staged changes with associated features.
    """
    changes = get_files_by_git_change()

    def group_files_by_feature(files: List[str]):
        feature_dict = defaultdict(list)
        for file in files:
            features = get_features_for_file(file)
            if not features:
                features = [WITHOUT_FEATURE]
            for feature in features:
                feature_dict[feature].append(file)
        return feature_dict

    def print_changes(change_type: str, files: List[str]):
        feature_dict = group_files_by_feature(files)
        print(f"{change_type.replace('_', ' ').title()}:")
        for feature, files in feature_dict.items():
            print(f"\t{feature}:")
            if feature == WITHOUT_FEATURE:
                print(
                    """\t (To assign a feature, run git feature-add <filename> <feature>)"""
                )
            for file in files:
                print(f"\t\t{file}")

    printed = False
    if len(changes["staged_files"]) > 0:
        printed=True
        print_changes("Feature changes to be committed", changes["staged_files"])

    if len(changes["unstaged_files"]) > 0:
        printed=True
        print_changes(
            "Feature changes not staged for commit", changes["unstaged_files"]
        )
    if len(changes["untracked_files"]) > 0:
        printed=True
        print_changes("", (changes["untracked_files"]))
    if not printed:
        print("No changes.")


@app.command()
def feature_add(
    feature_names: list[str],
    from_annotations: bool = typer.Option(
        False, help="Stage changes based on feature annotations"
    ),
    from_files: list[str] = typer.Option(
        [],
        help='''Specify the set of files you want to annotate. Note that files listet that are not staged will be added to the staging area''',
    ),
    from_staged: bool = typer.Option(False, help="Use the staged files only to add feature information"),
    add_annotations:bool = typer.Option(False, help="Sets whether the changes will be grouped with feature annotations")
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
                    initial_diff = repo.git.diff('--cached')
                    repo.git.add(file)
                    print(f"Staged file: {file}")
                    final_diff = repo.git.diff('--cached')
                    if initial_diff == final_diff:
                        print("No changes were made to the staging area. Aborting.")
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


@app.command()
def feature_info(
    all: bool = typer.Option(False, help="Get all features"),
    currently_staged:bool = typer.Option(False, help="List all features that are touched by staged changes"),
    feature: str = typer.Option(None, help="Inspect a particular feature"),
    authors: bool = typer.Option(
        False, help="Include authors in the inspection"
    ),
    files: bool = typer.Option(False, help="Include files in the inspection"),
    updatable: bool = typer.Option(False, help="Display whether the feature can be updated and what update options there are"),
    branch: str = typer.Option(None, help="Specify branch for inspection that should be compared to the currently checked out branch"),
):
    """
    Inspects feature information.
    """
    if currently_staged:
        print(f"Currently staged {read_staged_featureset()}")
        return
    print(
        f"Executing feature-info with all={all}, feature={feature}, authors={authors}, files={files}, updatable={updatable}, branch={branch}"
    )
    if all:
        print("All features in project")
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


@app.command()
def feature_blame(filename: str):
    """
    Displays features associated with file lines.
    """
    print(f"Executing feature-blame for {filename}")


if __name__ == "__main__":
    app()
