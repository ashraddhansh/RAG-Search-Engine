#!/usr/bin/env python3

import argparse
from keyword_search import keyword_search
from tf_idf import InvertedIndex
from utils import tokenize_term

def build_command():
    inverted_index = InvertedIndex()
    inverted_index.build()
    inverted_index.save()


def tf_command(doc_id, term):
    token = tokenize_term(term)
    inverted_index = InvertedIndex()
    inverted_index.load()
    term_freq = inverted_index.get_tf(doc_id, token)
    print(f"Document {doc_id} contains the term {term} {term_freq} times")



def main() -> None:
    parser = argparse.ArgumentParser(description="Keyword Search CLI")
    subparsers = parser.add_subparsers(dest="command", help="Available commands")

    search_parser = subparsers.add_parser("search", help="Search movies using keywords")
    search_parser.add_argument("query", type=str, help="Search query")
    build_parser = subparsers.add_parser("build", help="Build the movies index")
    term_freq_parser = subparsers.add_parser("tf", help="Get the term frequency of the given term in a document")
    term_freq_parser.add_argument("document_ID", type=int, help="Document ID to get the term frequeny")
    term_freq_parser.add_argument("term", type=str, help="Term to get the term frequeny")
    

    args = parser.parse_args()

    match args.command:
        case "search":
            print("Searching for:", args.query)
            print(keyword_search(args.query))
             # print the search query here
        case "build":
            build_command()
        case "tf":
            tf_command(args.document_ID, args.term)
        case _:
            parser.print_help()

if __name__ == "__main__":
    main()
