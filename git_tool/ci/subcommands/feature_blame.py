import typer

app = typer.Typer()


@app.command()
def feature_blame(filename: str):
    """
    Displays features associated with file lines.
    """
    print(f"Executing feature-blame for {filename}")
    raise NotImplementedError
