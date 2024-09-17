from pathlib import Path
import typer

app = typer.Typer(no_args_is_help=True)


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
        typer.echo(f"{feature:<15} {i:>4} {line.strip()}")


@app.command()
def feature_blame(
    filename: str = typer.Argument(
        ..., help="The file to display feature blame for."
    ),
    line: str = typer.Option(
        None, help="Specify a line or range of lines (e.g., '5' or '5-10')."
    ),
):
    """
    Displays features associated with file lines. You can optionally specify a line or a range of lines.
    """
    file_path = Path(filename)

    if not file_path.exists():
        typer.echo(f"Error: file '{filename}' not found.")
        raise typer.Exit(code=1)

    lines = read_file_lines(file_path)
    feature_to_line_mapping = get_features_for_lines(file_path)

    # Default to the entire file if no line argument is provided
    start_line = 1
    end_line = len(lines)

    if line:
        if "-" in line:
            # Handle a range of lines
            start_line, end_line = map(int, line.split("-"))
        else:
            # Handle a single line
            start_line = end_line = int(line)

    # Ensure the line range is valid
    if start_line < 1 or end_line > len(lines):
        typer.echo("Error: Line number out of range.")
        raise typer.Exit(code=1)

    print_feature_blame_output(
        lines, feature_to_line_mapping, start_line, end_line
    )
