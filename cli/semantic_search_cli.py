#!/usr/bin/env python3

import argparse

def main() -> None:
    parser = argparse.ArgumentParser(description="Semantic Search CLI")
    subparsers = parser.add_subparsers(dest="command", help="Available commands")

    verify_parser = subparsers.add_parser("verify", help="Verify the Sentence transformation model")
    args = parser.parse_args()

    match args.command:
        case "verify":
            from lib.semantic_search import verify_model
            verify_model()
            
        case _:
            parser.print_help()


if __name__ == "__main__":
    main()
