import typer
from git_tool.ci.subcommands.feature_add import app as feature_add
from git_tool.ci.subcommands.feature_blame import app as feature_blame
from git_tool.ci.subcommands.feature_commit import app as feature_commit
from git_tool.ci.subcommands.feature_info import app as feature_info
from git_tool.ci.subcommands.feature_status import app as feature_status

app = typer.Typer(name="features")
app.add_typer(feature_add, name="add")
app.add_typer(feature_blame, name="blame")
app.add_typer(feature_commit, name="commit")
app.add_typer(feature_info, name="info")
app.add_typer(feature_status, name="status")

app()
