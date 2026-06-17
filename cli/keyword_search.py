import json
import string
JSON_FILE = "/home/ashraddhansh/Developer/github.com/rag-search-engine/data/movies.json"

def tokenize(query) -> list:
    return list(filter(None, query.split()))

def remove_punctuation(query):
    punc_to_empty_mapping = str.maketrans({item: "" for item in string.punctuation})
    return query.translate(punc_to_empty_mapping)

def pre_process(query):
    return tokenize(remove_punctuation(query.lower()))

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

remove_punctuation("hello")
