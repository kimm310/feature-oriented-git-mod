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
from git_tool.feature_data.models_and_context.feature_state import read_staged_featureset, write_staged_featureset
from git_tool.feature_data.models_and_context.repo_context import repo_context

app = typer.Typer()

WITHOUT_FEATURE = "Without Feature"


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
    elif from_staged:
        print("use staged files")
        
    elif from_files:
        print("use files")
        # stage all unstaged files
        with repo_context() as repo:
            for file in from_files:
                try:
                    repo.git.add(file)
                    print(f"Staged file: {file}")
                except Exception as e:
                    print(f"Error staging file {file}: {e}")
    else:
        print("no specific option selected")
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
    tangled_feature: bool = typer.Option(
        False, help="Include tangled features in the inspection"
    ),
    dependencies: bool = typer.Option(
        False, help="Include dependencies in the inspection"
    ),
    updatable: bool = typer.Option(False, help="Show updatable features"),
    branch: str = typer.Option(None, help="Specify branch for inspection"),
):
    """
    Inspects feature information.
    """
    if currently_staged:
        print(f"Currently staged {read_staged_featureset()}")
        return
    print(
        f"Executing feature-info with all={all}, feature={feature}, authors={authors}, files={files}, tangled_feature={tangled_feature}, dependencies={dependencies}, updatable={updatable}, branch={branch}"
    )


@app.command()
def feature_blame(filename: str):
    """
    Displays features associated with file lines.
    """
    print(f"Executing feature-blame for {filename}")


if __name__ == "__main__":
    app()
