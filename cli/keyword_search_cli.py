#!/usr/bin/env python3

import argparse
from keyword_search import keyword_search
from constants import BM25_K1, BM25_B
from parser_commands import *


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

    bm25_idf_parser = subparsers.add_parser("bm25idf", help="Get BM25 IDF score for a given term")
    bm25_idf_parser.add_argument("term", type=str, help="Term to get BM25 IDF score for")
    
    bm25_tf_parser = subparsers.add_parser("bm25tf", help="Get BM25 TF score for a given document ID and term")
    bm25_tf_parser.add_argument("doc_id", type=int, help="Document ID")
    bm25_tf_parser.add_argument("term", type=str, help="Term to get BM25 TF score for")
    bm25_tf_parser.add_argument("k1", type=float, nargs='?', default=BM25_K1, help="Tunable BM25 K1 parameter")
    bm25_tf_parser.add_argument("b", type=float, nargs='?', default=BM25_B, help="Tunable BM25 b parameter")

    bm25search_parser = subparsers.add_parser("bm25search", help="Search movies using full BM25 scoring")
    bm25search_parser.add_argument("query", type=str, help="Search query")
    bm25search_parser.add_argument("--limit", type=int, default=5, help="Maximum number of results")


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
        case "bm25idf":
            print(f"BM25 IDF score of '{args.term}': {bm25_idf_command(args.term):.2f}")
        case "bm25tf":
            print(f"BM25 TF score of '{args.term}' in document '{args.doc_id}': {bm25_tf_command(args.doc_id, args.term, args.k1, args.b):.2f}")
        case "bm25search":
            print(bm25search_command(args.query, args.limit))

        case _:
            parser.print_help()

if __name__ == "__main__":
    main()
