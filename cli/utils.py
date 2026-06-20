import string
from nltk.stem import PorterStemmer
from constants import STOPWORDS_FILES

def tokenize(query) -> list:
    return list(filter(None, query.split()))

def remove_punctuation(query):
    punc_to_empty_mapping = str.maketrans({item: "" for item in string.punctuation})
    return query.translate(punc_to_empty_mapping)

PROC_STOPWORDS = []

with open(STOPWORDS_FILES, 'r') as f:
    PROC_STOPWORDS = {
            remove_punctuation(x).lower()
            for x in f.read().splitlines()
            }

def remove_stopwords(token_list):
        return [x for x in token_list if x not in PROC_STOPWORDS]



stemmer = PorterStemmer()

def stemming(token_list) -> list:
    return list(map(lambda x : stemmer.stem(x), token_list))

def pre_process(query) -> list:
    return stemming(remove_stopwords(tokenize(remove_punctuation(query.lower()))))
