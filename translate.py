import argparse
import csv
import glob
import os
import re
import shutil
import typing

from os.path import join
from pathlib import Path


DESCRIPTION = '''Translate source code comments from one language to another.
This activity is executed in two phases: scan and write. In the scan phase,
the script walks the source folder looking for strings in the specified source
language. It writes anything it finds into the review file. Your job is to then
open the review file, remove any erroneous matches, and otherwise correct the
file as required. In the write phase, the script will copy the contents of the
source folder into the destination folder, then begin translating the strings
identified in the review file. Files in the destination folder will then be 
updated with the translated comments. Translations are done using the Google
Translate API and are throttled.'''
EPILOG = '''Examples:
    python3 translate.py --action=scan --from=ru --to=en --src=/source
    python3 translate.py --action=write --from=ru --to=en --src=/source --dest=/dest
'''
REVIEW_FILE_NAME = 'review.csv'


parser = argparse.ArgumentParser(
    description=DESCRIPTION,
    epilog=EPILOG,
    formatter_class=argparse.ArgumentDefaultsHelpFormatter
)

parser.add_argument('--action', action="store", default='scan', dest="action", help="Action is either scan or write")
parser.add_argument('--from', action="store", default='ru', dest="lang_from", help="Source language")
parser.add_argument('--to', action="store", default='en', dest="lang_to", help="Output language")
parser.add_argument('--src', action="store", default='./', dest="src", help="Source path")
parser.add_argument('--dest', action="store", default='./translation', dest="dest", help="Destination path")


def copy_folder(source: str, dest: str) -> None:
    """
    Copy the contents of the source folder into the destination folder. If the
    destination folder does not exist then create it first.
    """
    shutil.copytree(source, dest)


def get_comments(source_path: str, lang_from: str) -> list:
    """
    Get the list of comments from the source file.
    :param source_path: Path to source file
    :param lang_from: Source language
    :return:
    """
    comments = []
    with open(source_path, 'r') as f:
        line_number = 0
        for line in f.readlines():
            inline_comment_index = line.rfind('//')
            if inline_comment_index > -1:
                inline_comment = line[inline_comment_index + 2:].strip()
                if has_cyrillic(inline_comment):
                    comments.append((source_path, line_number, inline_comment))
            line_number = line_number + 1
    return comments


def get_source_files(src: str) -> list:
    """
    Get the list of source files.
    :param src: Source folder path
    :return: list of source files to be scanned
    """
    source_extensions = ['**/*.cpp', '**/*.h']
    files = []
    for extension in source_extensions:
        files.extend(glob.glob(join(src, extension), recursive=True))
    return files


def has_cyrillic(text):
    """
    Determine if a block of text contains Cyrillic characters.
    :param text: Text
    :return:
    """
    return bool(re.search('[\u0400-\u04FF]', text))


def read_review_file(src: str) -> list:
    """
    Read review file.
    :param src: Path to source directory
    :return: lines
    """
    review_file_path = Path(src).joinpath(REVIEW_FILE_NAME)
    with open(review_file_path, newline='') as csvfile:
        review_file = csv.reader(csvfile, delimiter=' ', quotechar='|')
        lines = []
        for row in review_file:
            lines.append(row)
        return lines


def scan_sources(src: str, lang_from: str) -> None:
    """
    Scan source folder for strings to be translated.
    :param src: Path to source folder
    :param lang_from: Source language
    :return:
    """
    files = get_source_files(src)
    for file in files:
        comments = get_comments(file, lang_from)
        write_comments(src, comments)


def write_comments(src: str, lines: list) -> None:
    """
    Append the list of comments into the review file. The review file is in CSV
    format. If the file does not already exist, create it first.
    :param src: Source folder path
    :param lines: Lines to be written
    :return: None
    """
    review_file_path = Path(src).joinpath(REVIEW_FILE_NAME)
    pass
    # with open(review_file_path, 'a', newline='') as f:
    #     review_file = csv.writer(f, delimiter='\t')
    #     for row in lines:
    #         review_file.writerow(row)


def write_translation(src: str, dest: str, lang_from: str, lang_to: str) -> None:
    """
    Write the translation to the destination folder.
    :param src: Source path
    :param dest: Destination path
    :param lang_from: Input language
    :param lang_to: Output language
    """
    copy_folder(src, dest)
    strings = read_review_file(src)
    for s in strings:
        print(f'fetch translation of', s)


if __name__ == '__main__':
    print("its the main function!")
    args = parser.parse_args()
    if args.action == 'scan':
        scan_sources(args.src, args.lang_from)
    elif args.action == 'write':
        write_translation(args.src, args.dest, args.lang_from, args.lang_to)
