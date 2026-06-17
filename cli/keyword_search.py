import json
from os import remove
import string
from constants import JSON_FILE, STOPWORDS_FILES

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

def pre_process(query) -> list:
    return remove_stopwords(tokenize(remove_punctuation(query.lower())))

def keyword_search(query):
    with open(JSON_FILE, 'r') as f:
        json_data = json.load(f)
        movies_list = json_data["movies"]
        result_list = []
        query_tokens = pre_process(query)
        
        for item in movies_list:
            title_tokens = pre_process(item["title"])

            if any(q in token for q in query_tokens for token in title_tokens):
                result_list.append(item["title"])


        return_string = ""
        for i in range(len(result_list[:5])):
            return_string = return_string + f"{str(i+1)}. {result_list[i]}\n"
        return return_string

