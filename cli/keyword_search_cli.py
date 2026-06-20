#!/usr/bin/env python3

import argparse
from keyword_search import keyword_search
from tf_idf import InvertedIndex
from utils import tokenize_term
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




def main() -> None:
    parser = argparse.ArgumentParser(description="Keyword Search CLI")
    subparsers = parser.add_subparsers(dest="command", help="Available commands")

    search_parser = subparsers.add_parser("search", help="Search movies using keywords")
    search_parser.add_argument("query", type=str, help="Search query")

    build_parser = subparsers.add_parser("build", help="Build the movies index")

    term_freq_parser = subparsers.add_parser("tf", help="Get the term frequency of the given term in a document")
    term_freq_parser.add_argument("document_ID", type=int, help="Document ID to get the term frequeny")
    term_freq_parser.add_argument("term", type=str, help="Term to get the term frequeny")

    idf_parser = subparsers.add_parser("idf", help="Get the IDF value of the given term")
    idf_parser.add_argument("idf_term", type=str, help="Term to get the IDF")

    tfidf_freq_parser = subparsers.add_parser("tfidf", help="Get the TF-IDF value of a term")
    tfidf_freq_parser.add_argument("document_ID", type=int, help="Document ID to get the TF-IDF")
    tfidf_freq_parser.add_argument("term", type=str, help="Term to get the TF-IDF")
    

    args = parser.parse_args()

    match args.command:
        case "search":
            print("Searching for:", args.query)
            print(keyword_search(args.query))
             # print the search query here
        case "build":
            build_command()
        case "tf":
            print(tf_command(args.document_ID, args.term))
        case "idf":
            print(idf_command(args.idf_term))
        case "tfidf":
            print(tf_idf_command(args.document_ID, args.term))
        case _:
            parser.print_help()

if __name__ == "__main__":
    main()
