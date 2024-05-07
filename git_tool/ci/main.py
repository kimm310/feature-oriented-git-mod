from collections import defaultdict
from pathlib import Path

import typer
from git import Repo, Diff

from git_tool import patch_feature_mapper as mp
from git_tool.finding_features import FeatureMatches, get_features_for_diff


# This is true as long as the project structure is not changed! Probably need to move this somewhere else
current_directory = Path(__file__).parent
repo_path = current_directory.parents[1]
repo = Repo(repo_path)


app = typer.Typer()


@app.command()
def diff_by_feature():
    result = mp.get_diff_output()
    typer.echo("Output diff sorted by feature")
    for patch in result:
        print("Datei:", patch.path)
        print("Hunks:", len(patch))


@app.command()
def status():
    # Get the current diffs
    # Attach list of features to each diff
    # display status
    # https://gitpython.readthedocs.io/en/stable/tutorial.html#obtaining-diff-information
    head_commit = repo.head.commit
    diff = head_commit.diff(None, create_patch=True)

    mapped_to_feature = [(get_features_for_diff(d), d.a_path) for d in diff]
    features_dict = defaultdict(list)
    for features, filename in mapped_to_feature:
        for feature in features:
            features_dict[feature.name].append(filename)
    for feat_name, files in features_dict.items():
        typer.echo(feat_name)
        for file in files:
            typer.echo(f"\t{file}")
