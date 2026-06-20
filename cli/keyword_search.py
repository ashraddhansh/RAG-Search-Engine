from tf_idf import InvertedIndex
from utils import pre_process

def keyword_search(query):
    inverted_index = InvertedIndex()

    try:
        inverted_index.load()
    except Exception as e:
        print(f"Error: {e}")
        return

    query_tokens = pre_process(query)

    seen = set()
    results = []

    for token in query_tokens:
        matching_doc_ids = inverted_index.get_documents(token)

        for doc_id in matching_doc_ids:
            if doc_id in seen:
                continue

            seen.add(doc_id)

            movie = inverted_index.docmap[doc_id]
            results.append(movie)

            if len(results) >= 5:
                return "\n".join(
                    f"{m['id']}. {m['title']}"
                    for m in results
                )

    return "\n".join(
        f"{m['id']}. {m['title']}"
        for m in results
    )
