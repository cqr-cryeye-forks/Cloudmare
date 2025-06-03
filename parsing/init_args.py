import argparse
import pathlib


def init_args():
    parser = argparse.ArgumentParser()

    parser.add_argument(
        '-i', '--input-file',
        type=pathlib.Path,
        help='Path to edit output in txt'
    )
    parser.add_argument(
        '-o', '--output-file',
        type=pathlib.Path,
        help='Path to write output in json'
    )

    return parser.parse_args()
