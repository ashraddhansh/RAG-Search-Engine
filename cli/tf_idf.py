import pickle
from collections import defaultdict, Counter
from constants import JSON_FILE, BM25_K1, BM25_B
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
        self.doc_lengths = {}

    def __add_document(self, doc_id, text):
        token_list = pre_process(text)
        self.term_frequencies[doc_id] = Counter()
        for token in token_list:
            self.index[token].add(doc_id)
            self.term_frequencies[doc_id][token] += 1
        total_tokens = len(token_list)
        self.doc_lengths.update({doc_id: total_tokens})


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
        with open(os.path.join(CACHE_DIR, "doc_lengths.pkl"), "wb") as f:
            pickle.dump(self.doc_lengths, f)

    def load(self):
        index_path = os.path.join(CACHE_DIR, "index.pkl")
        docmap_path = os.path.join(CACHE_DIR, "docmap.pkl")
        term_frequecies_path = os.path.join(CACHE_DIR, "term_ferquencies.pkl")
        doc_lengths_path = os.path.join(CACHE_DIR, "doc_lengths.pkl")

        if not os.path.isfile(index_path):
            raise FileNotFoundError(f"Missing file: {index_path}")
        if not os.path.isfile(docmap_path):
            raise FileNotFoundError(f"Missing file: {docmap_path}")
        if not os.path.isfile(docmap_path):
            raise FileNotFoundError(f"Missing file: {docmap_path}")
        if not os.path.isfile(term_frequecies_path):
            raise FileNotFoundError(f"Missing file: {term_frequecies_path}")
        if not os.path.isfile(doc_lengths_path):
            raise FileNotFoundError(f"Missing file: {doc_lengths_path}")

        with open(index_path, "rb") as f:
            self.index = pickle.load(f)

        with open(docmap_path, "rb") as f:
            self.docmap = pickle.load(f)

        with open(term_frequecies_path, "rb") as f:
            self.term_frequencies = pickle.load(f)

        with open(doc_lengths_path, "rb") as f:
            self.doc_lengths = pickle.load(f)

    def get_tf(self, doc_id, term):
        counter = self.term_frequencies.get(doc_id)
        if counter is None:
            return 0
        return counter[term]

    def get_bm25_idf(self, term:str) -> float:
        total_documents = len(self.docmap)
        df = len(self.index[term])
        return math.log((total_documents - df + 0.5) / (df + 0.5) + 1)

    def __get_avg_doc_length(self) -> float:
        if self.doc_lengths == {}:
            return 0.0
        total_doc_length = sum(self.doc_lengths.values())
        avg_doc_length = total_doc_length / len(self.doc_lengths)
        return avg_doc_length

    def get_bm25_tf(self, doc_id, term, k1=BM25_K1, b=BM25_B):
        tf = self.get_tf(doc_id, term)

        doc_length = sum(self.term_frequencies[doc_id].values())
        length_norm = 1 - b + b * (doc_length / self.__get_avg_doc_length())

        tf_component = (tf * (k1 + 1)) / (tf + k1 * length_norm)

        return tf_component

    def bm25(self, doc_id, term):
        bm25_tf = self.get_bm25_tf(doc_id, term)
        bm25_idf = self.get_bm25_idf(term)
        return bm25_tf * bm25_idf

    def bm25_search(self, query, limit):
        query_tokens = pre_process(query)
        scores = {}
        for doc_id in self.docmap:
            total_scores = 0
            for token in query_tokens:
                bm25_score = self.bm25(doc_id, token)
                total_scores += bm25_score
            scores[doc_id] = total_scores
        ranked_docs = sorted(scores.items(), key = lambda x: x[1], reverse=True)
        return ranked_docs[:limit]




