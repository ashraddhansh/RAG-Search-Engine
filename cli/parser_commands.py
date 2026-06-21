from tf_idf import InvertedIndex
from utils import tokenize_term
from constants import BM25_K1, BM25_B
import math


def build_command():
    inverted_index = InvertedIndex()
    inverted_index.build()
    inverted_index.save()


def tf_command(doc_id, term):
    term_token = tokenize_term(term)
    inverted_index = InvertedIndex()
    inverted_index.load()
    term_freq = inverted_index.get_tf(doc_id, term_token)
    return f"Document {doc_id} contains the term {term} {term_freq} times"

def idf_command(term):
    inverted_index = InvertedIndex()
    inverted_index.load()
    term_token = tokenize_term(term)
    term_match_doc_count = len(inverted_index.index.get(term_token,set()))
    total_doc_count = len(inverted_index.docmap)
    idf =  math.log((total_doc_count + 1) / (term_match_doc_count + 1))
    return f"Inverse document frequency of '{term}': {idf:.2f}"

def tf_idf_command(doc_id, term):
    inverted_index = InvertedIndex()
    inverted_index.load()
    term_token = tokenize_term(term)
    term_freq = inverted_index.get_tf(doc_id, term_token)

    term_match_doc_count = len(inverted_index.index.get(term_token,set()))
    total_doc_count = len(inverted_index.docmap)
    idf =  math.log((total_doc_count + 1) / (term_match_doc_count + 1))
    tf_idf = term_freq * idf

    return f"TF-IDF score of '{term}' in document '{doc_id}': {tf_idf:.2f}"

def bm25_idf_command(term):
    term_token = tokenize_term(term)
    inverted_index = InvertedIndex()
    inverted_index.load()
    return inverted_index.get_bm25_idf(term_token)

def bm25_tf_command(doc_id, term, k1=BM25_K1, b=BM25_B):
    term_token = tokenize_term(term)
    inverted_index = InvertedIndex()
    inverted_index.load()
    return inverted_index.get_bm25_tf(doc_id, term_token,k1=k1, b=b)

def bm25search_command(query, limit=5):
    inverted_index = InvertedIndex()
    inverted_index.load()
    doc_id_and_scores_list = inverted_index.bm25_search(query, limit)
    return_string = ""
    for rank, item in enumerate(doc_id_and_scores_list, start=1):
        doc_id = item[0]
        score = item[1]

        title = inverted_index.docmap[doc_id]["title"]
        return_string += (f"{rank}. ({doc_id}) {title} - Score: {score:.2f}\n")
    return return_string

