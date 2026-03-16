from core.embedding_engine import embed


def search_files(vector_store, query, k=5):

    query_vec = embed(query)

    results = vector_store.search(query_vec, k)

    return results