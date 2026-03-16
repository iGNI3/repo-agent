from git import Repo

def safe_commit(repo_path, message):

    repo = Repo(repo_path)

    repo.git.add(all=True)

    repo.index.commit(message)