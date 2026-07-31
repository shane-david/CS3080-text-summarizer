"""
The main part of the program just prompts the user for 
the path to the file they want to summarize and what type 
of summarization they want to do then calls the proper 
summarization function 
"""

from file_utils import FileUtils as f # used to read files needed to be summarized 
from summarizer import frequency_summarize as fs # frequency summarize function 
from summarizer import transformer_summarize as ts # transformer summarize function

# introduce user 
print("---------------------")
print("   Text Summarizer   ")
print("---------------------")
print()

# prompt user for file path (file_tils handls error checking)
file_path = input("Please enter the path to the file you want to summarize: ")
article = f.read_file(file_path)

# prompt user for how they would like to summarizer
sum_type = int(input("Please enter an integer for the type of summarization you want:\n1 Frequency Based\n2 Transformer Based \n3 Info\n"))

# match case for types 
match sum_type:
    case 1:

        # prompt user for how long they want the summary to be 
        len_sum = input("Please enter how many lines you wnat the summary to be (default is 3):")

        # pass it into the summary functoin and print the summary
        if len_sum:
            print(fs(article, int(len_sum)))
        else:
            print(fs(article))

    case 2:

        print(ts(article))

    case 3:

        print("Frequency based summarization returns the most relevant sentences in the article without generating new content. Transformer based summarization takes more computation power but produces a more fluent summary.")

    case _:

        raise ValueError("Not Recognized Type!")