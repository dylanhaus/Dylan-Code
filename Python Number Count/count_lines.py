import re
import os
import argparse
import sys
from pathlib import Path


def count_lines_with_numbers(file_path):
    with open(file_path, 'r') as file:
        lines = file.readlines()

    lines_with_numbers = 0
    lines_without_numbers = 0
    lines_without_numbers_list = []

    for index, line in enumerate(lines):
        if re.search(r'\d', line):
            lines_with_numbers += 1
        else:
            lines_without_numbers += 1
            lines_without_numbers_list.append(f"{index + 1:5d} | {line.strip()}")

    return lines_with_numbers, lines_without_numbers, lines_without_numbers_list


def process_files(file_paths):
    total_lines_with_numbers = 0
    total_lines_without_numbers = 0

    for file_path in file_paths:
        try:
            lines_with_numbers, lines_without_numbers, lines_without_numbers_list = count_lines_with_numbers(file_path)

            divider = "=" * (len(file_path) + 19)
            print(f"\n{divider}")
            print(f"Results for file: {file_path}")
            print(f"{divider}\n")
            print(f"{'Lines with numbers:':<22}{lines_with_numbers:>10}")
            print(f"{'Lines without numbers:':<22}{lines_without_numbers:>10}")

            if lines_without_numbers > 0:
                print("\nLines without numbers:")
                print(" Line | Content")
                print("------+--------------------------------")
                for line_info in lines_without_numbers_list:
                    print(line_info)

            total_lines_with_numbers += lines_with_numbers
            total_lines_without_numbers += lines_without_numbers
        except FileNotFoundError:
            print(f"Error: File '{file_path}' not found.")
            sys.exit(1)

    divider = "=" * len("Total results:")
    print(f"\n{divider}")
    print(f"Total results:")
    print(f"{divider}\n")
    print(f"{'Total lines with numbers:':<25}{total_lines_with_numbers:>10}")
    print(f"{'Total lines without numbers:':<25}{total_lines_without_numbers:>10}")


def main():
    parser = argparse.ArgumentParser(description="Count lines with and without numbers in text files")
    parser.add_argument("paths", nargs='+', help="The relative paths to the text files or directories")
    parser.add_argument("-r", "--recursive", action="store_true", help="Enable recursive search in directories")

    args = parser.parse_args()

    hardcoded_directory = "/Users/dylan"
    file_paths = []

    for relative_path in args.paths:
        full_path = os.path.join(hardcoded_directory, relative_path)
        path_object = Path(full_path)

        if path_object.is_file():
            file_paths.append(full_path)
        elif path_object.is_dir() and args.recursive:
            for root, _, files in os.walk(full_path):
                for file in files:
                    if file.endswith('.txt'):
                        file_paths.append(os.path.join(root, file))
        else:
            print(f"Error: '{full_path}' is not a valid file or directory.")
            sys.exit(1)

    process_files(file_paths)


if __name__ == '__main__':
    main()

