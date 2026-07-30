import string # library for string utils, used for punctation check in summarizer algorithm
from collections import defaultdict # library for default dicts, used for frequency counting without KeyErrors
from heapq import nlargest # library for priority queues 

import nltk # Natural Language Toolkit, used for frequncy based summarization
from nltk.corpus import stopwords # common words we cant to exclude from frequency scoring
from nltk.tokenize import sent_tokenize, word_tokenize # nltk tokenizers

# supress transfomers messages so user only sees summaries 
import os
import warnings

# suppress Hugging Face Hub's "unauthenticated requests" warning and general noise
os.environ["HF_HUB_DISABLE_SYMLINKS_WARNING"] = "1"
os.environ["TRANSFORMERS_VERBOSITY"] = "error"  # only show actual errors, not info/warnings
os.environ["TOKENIZERS_PARALLELISM"] = "false"   # suppresses a separate tokenizer warning

# suppress the tqdm progress bars for model/file downloads
from huggingface_hub.utils import logging as hf_logging
hf_logging.set_verbosity_error()

# suppress transformers' own logger
from transformers import logging as transformers_logging
transformers_logging.set_verbosity_error()

# suppress generic Python warnings (like the symlinks UserWarning)
warnings.filterwarnings("ignore")

# download NLTK's pre-trained data files 
nltk.download('punkt', quiet=True)
nltk.download('punkt_tab', quiet=True)
nltk.download('stopwords', quiet=True)

# frequency summarizer: scores each sentence by summing the normalized frequency of its 
# non-stopword words, it then returns the top-scoring sentences in their original order
# the default is a 3 sentence summary but this can be changed 
def frequency_summarize(text, num_sentences=3): 

    # tokenize the text into sentences
    sentences = sent_tokenize(text)

    # if the article is already shorter than the requested summary length, just return the text
    if len(sentences) <= num_sentences:
        return text

    # get the stop words from nltk
    stop_words = set(stopwords.words('english'))

    # tokenize the text into words
    words = word_tokenize(text.lower())

    # build a dictionary from words to frequencies ignroing stop words and punctuation 
    freq = defaultdict(int)
    for word in words:
        if word not in stop_words and word not in string.punctuation:
            freq[word] += 1

    # normalize the frequencies on a 0-1 scale
    max_freq = max(freq.values())
    freq = {word: count / max_freq for word, count in freq.items()}

    # score each sentence (sum of its words frequencies)
    sentence_scores = defaultdict(float)
    for i, sentence in enumerate(sentences):

        # get the words of each sentence
        sentence_words = word_tokenize(sentence.lower())

        # skip empty sentences
        if len(sentence_words) == 0:
            continue 

        # increase the score for each word by its frequency
        for word in sentence_words:
            if word in freq:
                sentence_scores[i] += freq[word]

        # normalize so that longer sentences are not automatically higher scoring
        sentence_scores[i] /= len(sentence_words) ** 0.5

    # pick top num_sentences by score
    top_sentences = nlargest(num_sentences, sentence_scores, key=sentence_scores.get)
    top_sentences.sort()

    # create the summar as a string with the sentences joined
    summary = ' '.join(sentences[i] for i in top_sentences)
    return summary 

# transfomer preperation: the transformer model is relatively big and uses a lot of resources, since the 
# user has a choice of whether they want to use that algorithm or the more resource effective frequency summarize
# algorithm it is best to only load the model once that has been selected and transformer_summarize has been called
# but not every time it is called, so this method checks if it exists and creates it if not
summarizer_model = None
def get_summarizer_model():

    global summarizer_model

    if summarizer_model is None:

        # import the module
        from transformers import pipeline

        print("Loading summarization model...")
        
        # create the model
        summarizer_model = pipeline("summarization", model="facebook/bart-large-cnn")

    return summarizer_model

# the transformers algorithm takes the text, max lenght and min lengths, it creates or fetches
# the model with get_summarizer_model() and then lets that model encode the text and decode it into a summary
def transformer_summarize(text, max_len=130, min_len=30):

    model = get_summarizer_model()
    result = model(text, max_length=max_len, min_length=min_len, do_sample=False, truncation=True)
    return result[0]['summary_text']