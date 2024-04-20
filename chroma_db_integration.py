from langchain.embeddings import OpenAIEmbeddings
from langchain_community.vectorstores import Chroma


class Chroma:
    def __init__(self, persist_directory, embedding_function):
        self.db = {}
        self.embedding_function = embedding_function

    def store_vector(self, vector, data):
        self.db[data] = vector

    def similarity_search(self, query_vector, top_k=3):
        return sorted(self.db.items(), key=lambda x: -x[1].dot(query_vector))[:top_k]


def setup_chroma_db(embedding_function):
    return Chroma(persist_directory="emb", embedding_function=embedding_function)


def split_response_into_chunks(embeddings, text, max_length=500):
    words = text.split()
    chunks = []
    current_chunk = []

    for word in words:
        current_chunk.append(word)
        if sum(len(w) for w in current_chunk) > max_length:
            chunks.append(' '.join(current_chunk))
            current_chunk = []

    if current_chunk:
        chunks.append(' '.join(current_chunk))

    return chunks


def store_query_vector(chunks, embeddings, db):
    for chunk in chunks:
        embedding = embeddings.embed_query(chunk)
        db.store_vector(embedding, data=chunk)


def retrieve_similar_chunks(query, embeddings, db):
    query_embedding = embeddings.embed_query(query)
    results = db.similarity_search(query_embedding, top_k=3)
    return ' '.join([result[0] for result in results])
