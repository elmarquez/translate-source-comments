import argparse
import googletrans
import os
import pathlib
import re
import shutil
import typing

DESCRIPTION = '''Translate source code comments from one language to another.
    
This activity is executed in two phases: scan and write. In the first phase,
the script scans the source folder looking for strings in the specified source
language. It writes anything it finds into the review file. You are to then
open the review file, remove any erroneous matches, and otherwise correct the
file as required.

In the second phase, the script will copy the contents of the source folder
into the destination folder, then being translating the strings identified in
the review file, and writing them into the respective location in the 
destination folder. Translations are done using the Google Translate API.

Example:

    Translate source comments from Russian to English.

    python3 translate.py --action=scan --lin=ru --lout=en --source=/path/to/source --review=/path/to/review.csv
    python3 translate.py --action=write --lin=ru --lout=en --source=/path/to/source --dest=/path/to/dest
'''

def copy_folder(source: str, dest: str) -> None:
    """
    Copy the contents of the source folder into the destination folder. If the
    destination folder does not exist then create it first.
    """
    shutil.copytree(source, dest)


def get_source_files_list(source: str) -> list:
    """
    Get the list of source files.
    """
    source_extensions = ['cpp', 'h']
    return []


def write_translation() -> None:
    """
    Write the translation to the destination folder.
    """


def write_strings(dest: str, data: list) -> None:
    """
    Append the list of translation strings into the review file. The review
    file is in CSV format. If the file does not already exist, create it first.
    """
    review_file_name = 'review.csv'
    pass


parser = argparse.ArgumentParser(
    description=DESCRIPTION,
)

parser.add_argument('--action', action="store_true", dest="action", help="Scan or write")
parser.add_argument('--lin', action="store_true", dest="lang_in", help="Source language")
parser.add_argument('--lout', action="store_true", dest="lang_out", help="Output language")
parser.add_argument('--source', action="store", dest="source_path", help="Source path")
parser.add_argument('--dest', action="store", dest="source_path", help="Destination path")
parser.add_argument('--review_file', action="store", dest="review_file", help="Path to write review file")

if __name__ == '__main__':
    print("its the main function!")
