import faiss
import os
import openai
import numpy as np

from langchain.schema import Document
from langchain.text_splitter import RecursiveCharacterTextSplitter
from dotenv import load_env

load_env()




def chunck_data(text, chunk_size: int = 1000, chunk_overlap: int = 500):

    documents = [Document(page_content=text)]
    text_splitter = RecursiveCharacterTextSplitter(chunk_size = chunk_size, chunk_overlap = chunk_overlap)
    texts = text_splitter.split_documents(documents)
    print(f"Number of chunks: {len(texts)}")
    return texts



def embed_data(texts):
    model = os.getenv("OPENAI_EMBEDDING_MODEL")
    embeddings = []
    count = 0
    n = len(texts)

    for text in texts:
        response = openai.embeddings.create(
            input=text,
            model=model
        )
        embeddings.append(response.data[0].embedding)
        count += 1
        if count % 50 == 0:
            print(f"loops left: {n - count}")

    index = faiss.IndexFlatL2(len(embeddings[0]))
    index.add(np.array(embeddings))
    faiss.write_index(index, os.getenv("VECTOR_STORE"))

    with open(os.getenv("VECTOR_MAPPING"), "w") as f:
        for i, text in enumerate(texts):
            f.write(f"{i}||{text}\n")






    