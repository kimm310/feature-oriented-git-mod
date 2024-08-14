from git import Repo


def get_branches_for_commit(repo: Repo, commit_id: str) -> set[str]:
    """
    Get all branches that contain the given commit.
    """
    branches = repo.git.branch("--contains", commit_id).split("\n")
    return {branch.strip() for branch in branches}


def get_author_for_commit(repo: Repo, commit_id: str) -> str:
    """
    Get the author of the given commit.
    """
    return repo.git.show("-s", "--format=%an", commit_id).strip()


def get_files_for_commit(repo: Repo, commit_id: str) -> list[str]:
    """
    Get the list of files modified by the given commit.
    """
    return repo.git.show("--name-only", "--pretty=", commit_id).splitlines()
