## Text Summarizer
A Python text summarization tool built for the final project of CS3080 at UCCS. The tool supports both frequency based and transformer based summarization
as well as .txt, .pdf, and .docx files. 

## Requirements
- Python 3.11
- Dependencies:
    ```bash
    pip install nltk transformers "transformers<5" torch pypdf python-docx
    ```

    > Transformers but be pinned below v5 for the methods to still exist

## Usage
```bash
python main.py
```
Follow the prompts to:
1. Choose summarization method
2. Provide a file path
3. Choose the desired summary length

## Author
Shane David - CS3080, UCCS
