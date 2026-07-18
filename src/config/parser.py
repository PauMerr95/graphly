import argparse


def build_parser() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        prog="graphly",
        description="This is a quick script for building IR data graphs",
        epilog="============================================",
    )
    parser.add_argument("filename")
    parser.add_argument("-c", "--config")
    return parser.parse_args()
