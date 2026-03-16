import faiss
import numpy as np


class VectorStore:

    def __init__(self, dim):

        self.index = faiss.IndexFlatL2(dim)
        self.docs = []


    def add(self, embedding, doc):

        self.index.add(np.array([embedding]))
        self.docs.append(doc)


    def search(self, embedding, k=5):

        D,I = self.index.search(np.array([embedding]),k)

        return [self.docs[i] for i in I[0]]