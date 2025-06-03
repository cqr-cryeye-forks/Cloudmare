import json
import pathlib

from parsing.init_args import init_args
from parsing.parse_success_lines import parse_success_lines


def main():
    args = init_args()
    input_file: pathlib.Path = pathlib.Path(args.input_file)
    output_file: pathlib.Path = pathlib.Path(args.output_file)

    # files = ["2.txt"]
    parsed_data: dict = parse_success_lines(input_file)
    json_data = json.dumps(parsed_data)
    output_file.write_text(json_data)
    print("Final results save to {}".format(output_file))


if __name__ == "__main__":
    main()

