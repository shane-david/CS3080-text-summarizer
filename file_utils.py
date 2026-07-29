"""
File Utils is a module that will only contain static methods 
for reading the supported files into a single stripped string 
that NLTK can use to summarize in the main portion of the program 
"""

import os

class FileUtils:

    @staticmethod
    def path_exists(filename):
        return os.path.isfile(filename)

    # this method reads a .txt file as one string
    # it also normalizes the whitespace and newlines into single spaces
    @staticmethod
    def read_txt(filename):

        # make sure the file exists 
        if not FileUtils.path_exists(filename):
            raise FileNotFoundError(f"{filename} does not exist!")

        # open the file for reading
        with open(filename, 'r', encoding='utf-8') as f:

            # read the file as a raw string
            content = f.read()

            # normalize white space
            content = ' '.join(content.split())

        # return the formatted string
        return content 
