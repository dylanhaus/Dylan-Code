import re
import os
import argparse
import sys
from pathlib import Path

def count_lines(file_path, pattern, context):
    with open(file_path, 'r') as file:
        lines = file.readlines()

    # Find the first and last lines with the pattern.
    first_line_index = -1
    last_line_index = -1
    for index, line in enumerate(lines):
        if re.search(pattern, line):
            if first_line_index == -1:
                first_line_index = index
            last_line_index = index

    # Count the lines with and without the pattern.
    matching_lines = last_line_index - first_line_index + 1
    non_matching_lines = len(lines) - matching_lines

    # Return the number of matching and non-matching lines.
    return matching_lines, non_matching_lines

def process_files(file_paths, args):
    results = []
    total_matching_lines = 0
    total_non_matching_lines = 0

    for file_path in file_paths:
        try:
            matching_lines, non_matching_lines = count_lines(file_path, args.pattern, args.context)

            divider = "=" * (len(file_path) + 19)
            results.append(f"\n{divider}")
            results.append(f"Results for file: {file_path}")
            results.append(f"{divider}\n")
            results.append(f"{'Lines with numbers:':<22}{matching_lines:>10}")
            results.append(f"{'Lines without numbers:':<22}{non_matching_lines:>10}")

            if non_matching_lines > 0:
                results.append("\nLines without pattern:")
                results.append(" Line | Content")
                results.append("------+--------------------------------")
                for index, line in enumerate(lines):
                    if index < first_line_index or index > last_line_index:
                        results.append(f"{index + 1:5d} | {line.strip()}")

            total_matching_lines += matching_lines
            total_non_matching_lines += non_matching_lines
        except FileNotFoundError:
            print(f"Error: File '{file_path}' not found.")
            sys.exit(1)

    divider = "=" * len("Total results:")
    results.append(f"\n{divider}")
    results.append(f"Total results:")
    results.append(f"{divider}\n")
    results.append(f"{'Total lines with numbers:':<25}{total_matching_lines:>10}")
    results.append(f"{'Total lines without numbers:':<25}{total_non_matching_lines:>10}")

    output = "\n".join(results)
    if args.output:
        with open(args.output, 'w') as output_file:
            output_file.write(output)
    else:
        print(output)

def interactive_mode(args):
    while True:
        file_path = input("Enter a file path (or 'q' to quit): ").strip()
        if file_path.lower() == 'q':
            break

        if os.path.isfile(file_path):
            process_files([file_path], args)
        else:
            print(f"Error: '{file_path}' is not a valid file.")


def main():
    parser = argparse.ArgumentParser(description="Count lines with and without a specified pattern in text files")
    parser.add_argument("files", nargs="*", help="File paths to process")
    parser.add_argument("-p", "--pattern", default="\d", help="Regular expression pattern to search for (default: '\\d')")
    parser.add_argument("-c", "--context", type=int, default=0, help="Number of context lines to display around each line with pattern (default: 0)")
    parser.add_argument("-i", "--interactive", action="store_true", help="Enter interactive mode")
    parser.add_argument("-o", "--output", help="Save the results to a file instead of printing to the console")
    args = parser.parse_args()

    if args.interactive:
        while True:
            file_path = input("Enter a file path (or 'q' to quit): ").strip()
            if file_path.lower() == 'q':
                break

            if os.path.isfile(file_path):
                process_files([file_path], args)
            else:
                print(f"Error: '{file_path}' is not a valid file.")
    elif args.files:
        for file_path in args.files:
            if os.path.isfile(file_path):
                process_files([file_path], args)
            else:
                print(f"Error: '{file_path}' is not a valid file.")
    else:
        print("Error: No file paths provided. Use the '-h' option for help.")
        sys.exit(1)



