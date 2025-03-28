import typer
from git_tool.ci.subcommands.feature_add import app as feature_add
from git_tool.ci.subcommands.feature_add_from_staged import app as feature_add_from_staged
from git_tool.ci.subcommands.feature_blame import app as feature_blame
from git_tool.ci.subcommands.feature_commit import app as feature_commit
from git_tool.ci.subcommands.feature_commit_msg import app as feature_commit_msg
from git_tool.ci.subcommands.feature_commits import app as feature_commits
from git_tool.ci.subcommands.feature_info import app as feature_info
from git_tool.ci.subcommands.feature_info_all import app as feature_info_all
from git_tool.ci.subcommands.feature_pre_commit import app as feature_pre_commit
from git_tool.ci.subcommands.feature_status import app as feature_status

app = typer.Typer(name="feature")
app.add_typer(feature_add, name="add", help="Stage files and associate them with the provided features.")
app.add_typer(feature_add_from_staged, name="add-from-staged", help="Associate staged files with features.")
app.add_typer(feature_blame, name="blame", help="Display features associated with file lines.")
app.add_typer(feature_commit, name="commit", help="Associate an existing commit with one or more features.")
app.add_typer(feature_commit_msg, name="commit_msg", help="Generate feature information for the commit message.")
app.add_typer(feature_commits, name="commits", help="Find all commits that have feature information associated.")
app.add_typer(feature_info, name="info", help="Show information of a specific feature.")
app.add_typer(feature_info_all, name="info-all", help="List all available features in the project.")
app.add_typer(feature_pre_commit, name="pre-commit", help="Check if all staged changes are properly associated with features.")
app.add_typer(feature_status, name="status", help="Display unstaged and staged changes with associated features.")

app()
