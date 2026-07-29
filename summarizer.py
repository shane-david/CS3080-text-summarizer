import string # library for string utils, used for punctation check in summarizer algorithm
from collections import defaultdict # library for default dicts, used for frequency counting without KeyErrors
from heapq import nlargest # library for priority queues 

import nltk # Natural Language Toolkit, used for frequncy based summarization
from nltk.corpus import stopwords # common words we cant to exclude from frequency scoring
from nltk.tokenize import sent_tokenize, word_tokenize # nltk tokenizers

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

# main for testing
def main():

    sample_text = (
        "Artificial intelligence is transforming industries across the globe. "
        "Companies are investing billions of dollars into machine learning research. "
        "However, ethical concerns remain about job displacement and bias in algorithms. "
        "Many experts argue that regulation is necessary to ensure responsible AI development. "
        "Despite the risks, AI continues to drive innovation in healthcare, finance, and education. "
        "Researchers are working to make AI systems more transparent and explainable."
    )

    result = frequency_summarize(sample_text, num_sentences=2)
    print(result) 

if __name__ == "__main__":
    main() 