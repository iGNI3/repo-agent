from core.embedding_engine import embed
from core.vector_store import VectorStore
from core.repo_reader import read_repo


def build_index(repo_path):

    repo = read_repo(repo_path)

    first_file = next(iter(repo.values()))
    dim = len(embed(first_file[:1000]))

    store = VectorStore(dim)

    for path, content in repo.items():

        emb = embed(content[:2000])

        store.add(emb, {
            "path": path,
            "content": content
        })

    return store