from collections import defaultdict
from typing import List
import typer
from rich import print as pprint

from git_tool.feature_data.git_status_per_feature import (
    get_features_for_file,
    get_files_by_git_change,
)

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

    print_changes("Feature changes to be committed", changes["staged_files"])

    print_changes(
        "Feature changes not staged for commit", changes["unstaged_files"]
    )
    print_changes("", (changes["untracked_files"]))


@app.command()
def feature_add(
    feature_name: str,
    from_annotations: bool = typer.Option(
        False, help="Stage changes based on feature annotations"
    ),
    files: list[str] = typer.Option(
        [],
        help='''Specify the set of files you want to annotate. Note that files listet that are not staged will be added to the staging area''',
    ),
):
    """
    Stages changes for a specific feature.
    """
    print(
        f"Executing feature-add for {feature_name} with from_annotations={from_annotations}"
    )
    if files.__len__ > 0:
        print(f"Annotating files {files}")
        print("Checking for unstaged files")
        print("Staging files")
        return
    if from_annotations:
        print("Searching for features in the current code")


@app.command()
def feature_info(
    all: bool = typer.Option(False, help="Get all features"),
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
