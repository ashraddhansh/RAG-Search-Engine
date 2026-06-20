import json
import string
from nltk.stem import PorterStemmer
from constants import JSON_FILE, STOPWORDS_FILES
from tf_idf import InvertedIndex

PROC_STOPWORDS = []



def tokenize(query) -> list:
    return list(filter(None, query.split()))

def remove_punctuation(query):
    punc_to_empty_mapping = str.maketrans({item: "" for item in string.punctuation})
    return query.translate(punc_to_empty_mapping)


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

def load_movies():
    with open(JSON_FILE, 'r') as f:
        json_data = json.load(f)
        movies_list = json_data["movies"]
        return movies_list




def keyword_search(query):
    inverted_index = InvertedIndex()

    try:
        inverted_index.load()
    except Exception as e:
        print(f"Error: {e}")

    result_object_list = []
    query_tokens = pre_process(query)

    doc_id_list = []
    for token in query_tokens:
        if inverted_index.index[token]:
            doc_id_list = inverted_index.index.get(token)
    for id in doc_id_list[:5]:
        result_object_list.append(inverted_index.docmap.get(id))
        
