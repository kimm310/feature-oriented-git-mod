"""
Module that wraps git fast-import -> https://git-scm.com/docs/git-fast-import
This is the best way to add commits to a branch which is currently not checked out,
which is exactly what we try to prevent in this setup.
Here, all the boilerplate code goes that creates the commit meta data and makes sure
that the content is added as expected
"""

from git import GitCommandError
from pydantic import BaseModel, EmailStr
from typing import List
from datetime import datetime


if __name__ == "__main__":
    import sys
    import os

    sys.path.append(
        os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
    )

from git_tool.feature_data import repo_context


class CommitFileChange(BaseModel):
    """
    Datastructure to store the file and its expected contents.
    Is used to acutally commit content
    """

    permissions: str = "644"  # all files have same permissions
    file_path: str
    content: str

    @property
    def content_length(self) -> int:
        return len(self.content.encode("utf-8"))


class CommitData(BaseModel):
    branch_name: str
    committer_name: str
    committer_email: EmailStr
    commit_datetime: datetime = datetime.now()
    message: str
    add_files: List[CommitFileChange]

    @property
    def message_length(self) -> int:
        return len(self.message.encode("utf-8"))

    @property
    def timestamp(self) -> int:
        """
        Format according to fast-import specs
        """
        return int(self.commit_datetime.timestamp())

    @property
    def timezone(self) -> str:
        offset = self.commit_datetime.utcoffset()
        if offset is None:
            return "+0000"
        total_minutes = int(offset.total_seconds() // 60)
        hours, minutes = divmod(abs(total_minutes), 60)
        sign = "+" if total_minutes >= 0 else "-"
        return f"{sign}{hours:02}{minutes:02}"

    def to_partial_fast_import_format(self) -> str:
        """
        This function returns the string as expected for one change to the branch.
        Please note that this is not a fully viable fast import text strig, as it
        is missing the done tag.

        Returns:
            str: _description_
        """
        result = []
        result.append(f"commit refs/heads/{self.branch_name}")
        result.append(
            f"committer {self.committer_name} <{self.committer_email}> {self.timestamp} {self.timezone}"
        )
        result.append(f"data {self.message_length}")
        result.append(self.message)
        with repo_context.repo_context() as repo:
            try:
                from_message: str = (
                    f"from {repo.git.rev_parse(f'refs/heads/{self.branch_name}')}"
                )
                result.append(from_message)
            except GitCommandError:
                print(
                    "This will be the first commit on the feature data branch"
                )
        for change in self.add_files:
            result.append(f"M {change.permissions} inline {change.file_path}")
            result.append(f"data {change.content_length}")
            result.append(change.content)
        return "\n".join(result)


def to_fast_import_format(commits: list[CommitData]) -> str:
    """
    This function converts multiple CommitData objects into a fast-import compatible format.

    Returns:
        str: Full fast import format string including the done tag.
    """
    result = []
    for commit in commits:
        result.append(commit.to_partial_fast_import_format())
    result.append("done")
    return "\n".join(result) + "\n"


# Beispielverwendung
if __name__ == "__main__":
    commit_change = CommitFileChange(
        file_path="new2",
        content="This bug really sucks2",
    )

    commit = CommitData(
        branch_name="test",
        committer_name="Tabea",
        committer_email="agserm@gmail.com",
        message="Added 'This bug really sucks'",
        add_files=[commit_change],
    )

    fast_import_data = to_fast_import_format([commit])

    # Schreibe die Daten in eine Datei
    with open("git_fast_import_data.txt", "w") as f:
        f.write(fast_import_data)

    print("git fast-import data written to git_fast_import_data.txt")
