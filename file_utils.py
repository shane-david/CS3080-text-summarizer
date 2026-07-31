"""
File Utils is a module that will only contain static methods 
for reading the supported files into a single stripped string 
that NLTK can use to summarize in the main portion of the program 
"""

import os
from pypdf import PdfReader
from docx import Document

class FileUtils:

    @staticmethod
    def path_exists(filename):
        return os.path.isfile(filename)

    # this method determines the type of file and dispatches it to the proper method
    @staticmethod
    def read_file(filename):

        file_type = os.path.splitext(filename)[1].lower()

        # depending on the file type read the file as an entire string 
        match file_type:
            case ".txt":
                article = FileUtils.read_txt(filename)
            case ".pdf":
                article = FileUtils.read_pdf(filename)
            case ".docx":
                article = FileUtils.read_docx(filename)
            case _:
                raise ValueError("Program only supports .txt, .pdf, and .docx")

        return article

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

    # this method reads a .pdf file as one string with normalized white space 
    @staticmethod
    def read_pdf(filename):

        # make sure the file exits 
        if not FileUtils.path_exists(filename):
            raise FileNotFoundError(f"{filename} does not exist!")

        # create the pdf reader
        reader = PdfReader(filename)

        # extract text from each page and join them together 
        pages_text = [page.extract_text() or "" for page in reader.pages]
        content = ' '.join(pages_text)

        # normalize whitespace 
        content = ' '.join(content.split())

        return content 

    # this method reads a .docx file as one string with normalized white space 
    @staticmethod
    def read_docx(filename):

        # make sure the file exists 
        if not FileUtils.path_exists(filename):
            raise FileNotFoundError(f"{filename} does not exist!")

        # create docx document
        doc = Document(filename)

        # extract text from each paragraph and join them together
        paragraphs_text = [p.text for p in doc.paragraphs]
        content = ' '.join(paragraphs_text)

        # normalize whitespace 
        content = ' '.join(content.split())

        return content 
