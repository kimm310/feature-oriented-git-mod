from pathlib import Path
import typer

app = typer.Typer()


def read_file_lines(file_path: Path) -> list[str]:
    """
    Reads the lines of a file and returns them as a list.
    """
    with file_path.open("r", encoding="utf-8") as f:
        return f.readlines()


def get_features_for_lines(file_path: Path) -> dict[int, str]:
    """
    Returns a dictionary mapping line numbers to features.
    This is a placeholder function that you need to implement.
    """
    # Placeholder implementation: assign "UNKNOWN" feature to each line
    # In reality, you would parse the file and match lines to their respective features
    lines = read_file_lines(file_path)
    return {i + 1: "UNKNOWN" for i in range(len(lines))}


def print_feature_blame_output(
    lines: list[str], features_by_line: dict[int, str]
):
    """
    Prints the feature blame output similar to git blame.
    """
    for i, line in enumerate(lines, 1):
        feature = features_by_line.get(i, "UNKNOWN")
        print(f"{feature:<15} {i:>4} {line.strip()}")


@app.command()
def feature_blame(filename: str, line_sta):
    """
    Displays features associated with file lines.
    """
    file_path = Path(filename)

    if not file_path.exists():
        typer.echo(f"Error: file '{filename}' not found.")
        raise typer.Exit(code=1)

    lines = read_file_lines(file_path)
    feature_to_line_mapping = get_features_for_lines(file_path)
    print_feature_blame_output(lines, feature_to_line_mapping)
