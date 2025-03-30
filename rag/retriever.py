import openai
import faiss
import os

from dotenv import load_dotenv

load_dotenv()




def load_vector_store():
    index = faiss.read_index(os.getenv("VECTOR_STORE"))

    vector_map = {}

    with open(os.getenv("VECTOR_MAPPING"), "r") as file:
        for line in file:
            idx, text = line.split("||")
            vector_map[int(idx)] = text

    return index, vector_map


index, vector_map = load_vector_store()


def get_similar_docs(query: str):
    
    model = os.getenv("OPENAI_EMBEDDING_MODEL")

    response = openai.embeddings.create(
        input=query,
        model=model
    )
    embedded_query = response.data[0].embedding

    D, I = index.search(embedded_query, k=3)

    context = [vector_map[i] for i in I[0]]

    return context