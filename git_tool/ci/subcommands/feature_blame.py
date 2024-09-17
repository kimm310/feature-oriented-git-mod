from pathlib import Path
import typer
from git import Repo
from git_tool.feature_data.git_status_per_feature import get_features_for_file
from git_tool.feature_data.models_and_context.repo_context import (
    repo_context,
)  # Assuming this exists in your code

app = typer.Typer(no_args_is_help=True)


def read_file_lines(file_path: Path) -> list[str]:
    """
    Reads the lines of a file and returns them as a list.
    """
    with file_path.open("r", encoding="utf-8") as f:
        return f.readlines()


def run_git_blame(
    repo: Repo, file_path: Path, start_line: int, end_line: int
) -> dict[int, str]:
    """
    Uses gitpython's blame functionality to map line numbers to commit hashes.
    This function works on the specified range of lines.
    """
    blame_output = repo.git.blame(
        "-L", f"{start_line},{end_line}", "--line-porcelain", str(file_path)
    )

    line_to_commit = {}
    current_commit = None
    line_number = start_line

    for line in blame_output.splitlines():
        if line.startswith("author "):
            continue
        if line.startswith("summary "):
            continue
        if line.startswith("filename "):
            continue

        # New commit hash
        if line.startswith(
            (" ", "\t")
        ):  # If the line starts with a space, it is a line of the file
            line_to_commit[line_number] = current_commit
            line_number += 1
        else:
            current_commit = line.split()[0]

    return line_to_commit


def get_commit_feature_mapping() -> dict[str, str]:
    """
    Returns a mapping of commit hashes to features.
    This is a placeholder for your actual implementation, where you'd
    map each commit hash to its associated feature.
    """
    # Example mapping: Replace with your real data source
    return {
        "abcd123": "Feature A",
        "efgh456": "Feature B",
        "ijkl789": "Feature C",
    }


def get_features_for_lines(
    repo: Repo, file_path: Path, start_line: int, end_line: int
) -> dict[int, str]:
    """
    Returns a dictionary mapping line numbers to features based on the commits
    that modified each line in the specified line range.
    """
    # Step 1: Get the commit for each line using 'git blame'
    line_to_commit = run_git_blame(repo, file_path, start_line, end_line)

    # Step 2: Get the mapping of commits to features
    commit_to_feature = get_commit_feature_mapping()

    # Step 3: Map each line to its corresponding feature
    line_to_feature = {
        line: commit_to_feature.get(commit_hash, "UNKNOWN")
        for line, commit_hash in line_to_commit.items()
    }

    return line_to_feature


def print_feature_blame_output(
    lines: list[str],
    features_by_line: dict[int, str],
    start_line: int,
    end_line: int,
):
    """
    Prints the feature blame output similar to git blame.
    """
    for i in range(start_line, end_line + 1):
        line = lines[i - 1]  # Adjust for 0-based indexing
        feature = features_by_line.get(i, "UNKNOWN")
        typer.echo(f"{feature:<15} {i:>4} {line.strip()}")


@app.command(no_args_is_help=True, name=None)
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
    file_features = get_features_for_file(
        file_path=file_path, use_annotations=False
    )
    typer.echo(f"Features associated with the file '{filename}':\n")
    for i, feature in enumerate(file_features, 1):
        typer.echo(f"{i}. {feature}")

    if line:
        typer.echo("Linebased blames are not supported yet", err=True)
        return
        lines = read_file_lines(file_path)

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

        with repo_context() as repo:  # Use repo_context for the git operations
            feature_to_line_mapping = get_features_for_lines(
                repo, file_path, start_line, end_line
            )

        print_feature_blame_output(
            lines, feature_to_line_mapping, start_line, end_line
        )


if __name__ == "__main__":
    app()
