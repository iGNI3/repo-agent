from git import Repo


def get_diff(repo_path):

    repo = Repo(repo_path)

    diff = repo.git.diff()

    return diff