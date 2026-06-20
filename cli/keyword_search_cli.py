#!/usr/bin/env python3

import argparse
from keyword_search import keyword_search
from tf_idf import InvertedIndex

def build_command():
    inverted_index = InvertedIndex()
    inverted_index.build()
    inverted_index.save()
    docs = inverted_index.get_documents("merida")
    print(f"First document for token 'merida' = {docs[0]}")

def main() -> None:
    parser = argparse.ArgumentParser(description="Keyword Search CLI")
    subparsers = parser.add_subparsers(dest="command", help="Available commands")

    search_parser = subparsers.add_parser("search", help="Search movies using keywords")
    build_parser = subparsers.add_parser("build", help="build the movies index")
    search_parser.add_argument("query", type=str, help="Search query")

    args = parser.parse_args()

    match args.command:
        case "search":
            print("Searching for:", args.query)
            print(keyword_search(args.query))
             # print the search query here
        case "build":
            build_command()
        case _:
            parser.print_help()

if __name__ == "__main__":
    main()
