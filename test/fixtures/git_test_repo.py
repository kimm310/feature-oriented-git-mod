import pytest
import shutil

from git import Repo


@pytest.fixture(scope="module")
def git_repo(tmp_path_factory):
    repo_path = tmp_path_factory.mktemp("git_repo")
    repo = Repo.init(repo_path)
    repo.config_writer().set_value("user", "name", "Test User").release()
    repo.config_writer().set_value("user", "email", "test@example.com").release()

    yield repo

    shutil.rmtree(repo_path)
