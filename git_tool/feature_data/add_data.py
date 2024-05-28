from datetime import datetime
import hashlib
import tempfile
import uuid
from git import Actor, Repo

if __name__ == "__main__":
    import sys
    import os

    sys.path.append(
        os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
    )

from git_tool.feature_data.fact_model import ChangeDetail, ChangeType, FeatureFactModel


def create_metadata_branch(repo_path: str, branch_name: str):
    repo = Repo(repo_path)
    if branch_name in repo.heads:
        print(f"Branch '{branch_name}' exists already.")
        return
    new_branch = repo.create_head(branch_name)
    new_branch.checkout()
    print(f"Branch '{branch_name}' created and checked out.")


def generate_file_path(fact: FeatureFactModel) -> str:
    feature_uuid = str(uuid.uuid4())
    timestamp = fact.date.timestamp()
    commit_id = fact.commit
    fact_json = fact.json()
    sha1_hash = hashlib.sha1(fact_json.encode("utf-8")).hexdigest()
    return os.path.join(feature_uuid, str(int(timestamp)), commit_id, sha1_hash)


def generate_fact_file(fact: FeatureFactModel, repo: Repo):
    fact_json = fact.json()
    file_path = generate_file_path(fact)
    temp_dir = tempfile.mkdtemp()
    full_path = os.path.join(temp_dir, file_path)

    os.makedirs(os.path.dirname(full_path), exist_ok=True)
    with open(full_path, "w") as file:
        file.write(fact_json)


def add_fact_to_metadata_branch(
    repo_path: str, branch_name: str, fact: FeatureFactModel
):
    repo = Repo(repo_path)
    generate_fact_file(fact, repo)

    # Git fast-import Vorbereitung
    author = Actor("Metadata Author", "author@example.com")
    author_str = (
        f"{author.name} <{author.email}> {int(datetime.now().timestamp())} +0000"
    )
    commit_message = f"Add feature fact for commit {fact.commit}"
    branch_ref = f"refs/heads/{branch_name}"

    fast_import_data = f"""
        commit {branch_ref}
        committer {author_str}
        data {len(commit_message)}
        {commit_message}
        M 100644 inline {file_path}
        data {len(fact_json)}
        {fact_json}
        """

    # Fast-import ausführen
    repo.git.stash("push", "--include-untracked")
    repo.git.fast_import(stdin=fast_import_data)
    repo.git.stash("pop")

    print(f"Feature fact added and committed to branch '{branch_name}'.")


if __name__ == "__main__":
    # Beispiel zur Verwendung
    repo_path = "/home/tabea/Uni/worktree/inital-experiments"
    branch_name = "feature_metadata"

    create_metadata_branch(repo_path, branch_name)

    fact = FeatureFactModel(
        commit="abc123",
        authors=["Alice", "Bob"],
        date=datetime.now(),
        feature="NewFeature",
        changes=[
            ChangeDetail(
                change_type=ChangeType.ADDED,
                description="Neue Funktionalität hinzugefügt",
            )
        ],
    )

    add_fact_to_metadata_branch(repo_path, branch_name, fact)
