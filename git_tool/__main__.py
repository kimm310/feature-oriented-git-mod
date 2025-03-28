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
app.add_typer(feature_add, name="add", help="A")
app.add_typer(feature_add_from_staged, name="add-from-staged", help="B")
app.add_typer(feature_blame, name="blame", help="C")
app.add_typer(feature_commit, name="commit", help="D")
app.add_typer(feature_commit_msg, name="commit_msg", help="E")
app.add_typer(feature_commits, name="commits", help="F")
app.add_typer(feature_info, name="info", help="G")
app.add_typer(feature_info_all, name="info-all", help="H")
app.add_typer(feature_pre_commit, name="pre-commit", help="I")
app.add_typer(feature_status, name="status", help="J")

app()
