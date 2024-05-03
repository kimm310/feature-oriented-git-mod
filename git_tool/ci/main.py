from typing import Optional

import typer

from git_tool import patch_feature_mapper as mp


app = typer.Typer()


@app.command()
def diff_by_feature():
    result = mp.get_diff_output()
    typer.echo("Output diff sorted by feature")
    for patch in result:
        print("Datei:", patch.path)
        print ("Hunks:", len(patch))


@app.command()
def status():
    # Get the current diffs
    # Attach list of features to each diff
    # display status
    ...
