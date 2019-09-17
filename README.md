Translate Source Comments to Target Language
============================================

You have a large body of source code with comments in various languages. Find
the comments, write them to an intermediary file for review, then translate
each to the target language and write them into a copy of the original sources.

## Usage 

The `src` and `dest` are the input and output languages respectively. The
`input` and `output` paths are the 

script
will copy the contents of the source folder to the output folder first

    python3 translate --src='ru' --dest='en' --input=/path/to/source/folder --output=/path/to/output/folder --review=/path/to/strings.csv