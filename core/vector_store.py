import faiss
import numpy as np
import pickle
import os

class VectorStore:
    def __init__(self, dim=None):
        self.dim = dim
        self.index = faiss.IndexFlatL2(dim) if dim else None
        self.docs = []

    def add(self, embedding, doc):
        if self.index is None:
            self.dim = len(embedding)
            self.index = faiss.IndexFlatL2(self.dim)
        self.index.add(np.array([embedding]))
        self.docs.append(doc)

    def search(self, embedding, k=5):
        if not self.index: return []
        D, I = self.index.search(np.array([embedding]), k)
        return [self.docs[i] for i in I[0] if i < len(self.docs)]

    def save(self, path):
        os.makedirs(os.path.dirname(path), exist_ok=True)
        faiss.write_index(self.index, path + ".index")
        with open(path + ".docs", "wb") as f:
            pickle.dump(self.docs, f)

    @classmethod
    def load(cls, path):
        index = faiss.read_index(path + ".index")
        with open(path + ".docs", "rb") as f:
            docs = pickle.load(f)
        store = cls(index.d)
        store.index = index
        store.docs = docs
        return store