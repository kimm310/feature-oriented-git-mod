"""
Functions to retrieve git information for a specific file rather than starting with 
a list of features or commits
"""
from typing import Optional

from git_tool.feature_data.models_and_context.repo_context import repo_context


def get_commits_for_file(file_name:str, branch_name: Optional[str]) -> str:
    """
    Search git history for commits targeting a file, then collecting the commit ids
    """
    with repo_context() as repo:
        branch_selector = f"--branches={branch_name}" if branch_name else ""
        commit_id_only = "--pretty=format:%H"
        commits = repo.git.log(branch_selector, commit_id_only,file_name)
        return commits.split("\n")
    