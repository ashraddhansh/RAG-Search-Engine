import pickle
from collections import defaultdict, Counter
from constants import JSON_FILE, BM25_K1
import json
from utils import pre_process
import os
from constants import CACHE_DIR
import math


class InvertedIndex:
    def __init__(self):
        self.index = defaultdict(set)
        self.docmap = {}
        self.term_frequencies = {}

    def __add_document(self, doc_id, text):
        token_list = pre_process(text)
        self.term_frequencies[doc_id] = Counter()
        for token in token_list:
            self.index[token].add(doc_id)
            self.term_frequencies[doc_id][token] += 1


    def get_documents(self, term):
        return sorted(list(self.index[term]))

    def build(self):

        def load_movies():
            with open(JSON_FILE, 'r') as f:
                json_data = json.load(f)
                movies_list = json_data["movies"]
            return movies_list
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
        with open(os.path.join(CACHE_DIR, "term_ferquencies.pkl"), "wb") as f:
            pickle.dump(self.term_frequencies, f)

    def load(self):
        index_path = os.path.join(CACHE_DIR, "index.pkl")
        docmap_path = os.path.join(CACHE_DIR, "docmap.pkl")
        term_frequecies_path = os.path.join(CACHE_DIR, "term_ferquencies.pkl")

        if not os.path.isfile(index_path):
            raise FileNotFoundError(f"Missing file: {index_path}")
        if not os.path.isfile(docmap_path):
            raise FileNotFoundError(f"Missing file: {docmap_path}")
        if not os.path.isfile(docmap_path):
            raise FileNotFoundError(f"Missing file: {docmap_path}")
        if not os.path.isfile(term_frequecies_path):
            raise FileNotFoundError(f"Missing file: {term_frequecies_path}")

        with open(index_path, "rb") as f:
            self.index = pickle.load(f)

        with open(docmap_path, "rb") as f:
            self.docmap = pickle.load(f)

        with open(term_frequecies_path, "rb") as f:
            self.term_frequencies = pickle.load(f)

    def get_tf(self, doc_id, term):
        counter = self.term_frequencies.get(doc_id)
        if counter is None:
            return 0
        return counter[term]

    def get_bm25_idf(self, term:str) -> float:
        total_documents = len(self.docmap)
        df = len(self.index[term])
        return math.log((total_documents - df + 0.5) / (df + 0.5) + 1)

    def get_bm25_tf(self, doc_id, term, k1=BM25_K1):
        tf = self.get_tf(doc_id, term)
        saturated_tf_score =  (tf * (k1 + 1)) / (tf + k1)
        return saturated_tf_score

