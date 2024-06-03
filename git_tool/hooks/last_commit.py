#!/usr/bin/env python3


if __name__ == "__main__":
    import sys
    import os

    sys.path.append(
        os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
    )

from git_tool.feature_data import repo_context


def get_last_commit_message():
    with repo_context.repo_context() as repo:
        last_commit = repo.head.commit
        return last_commit.message


if __name__ == "__main__":
    commit_message = get_last_commit_message()
    print("Letzter Commit Nachricht:")
    print(commit_message)
