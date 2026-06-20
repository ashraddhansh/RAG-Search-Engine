import pickle
from collections import defaultdict
from keyword_search import pre_process, load_movies
import os
from constants import CACHE_DIR

class InvertedIndex:
    def __init__(self):
        self.index = defaultdict(set)
        self.docmap = {}

    def __add_document(self, doc_id, text):
        token_list = pre_process(text)
        for token in token_list:
            self.index[token].add(doc_id)

    def get_documents(self, term):
        return sorted(list(self.index[term]))

    def build(self):
        movies_list = load_movies()
        for m in movies_list:
            self.__add_document(m['id'], f"{m['title']} {m['description']}")
            self.docmap.update({m['id']: m})

    def save(self):
        os.makedirs(CACHE_DIR, exist_ok=True)
        with open(os.path.join(CACHE_DIR, "index.pkl"), "wb") as f:
            pickle.dump(self.index, f)
        with open(os.path.join(CACHE_DIR, "docmap.pkl"), "wb") as f:
            pickle.dump(self.docmap, f)

    def load(self):
        index_path = os.path.join(CACHE_DIR, "index.pkl")
        docmap_path = os.path.join(CACHE_DIR, "docmap.pkl")

        if not os.path.isfile(index_path):
            raise FileNotFoundError(f"Missing file: {index_path}")
        if not os.path.isfile(docmap_path):
            raise FileNotFoundError(f"Missing file: {docmap_path}")

        with open(index_path, "rb") as f:
            self.index = pickle.load(f)

        with open(docmap_path, "rb") as f:
            self.docmap = pickle.load(f)

