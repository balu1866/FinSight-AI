import faiss
import os
import openai
import numpy as np

from langchain.schema import Document
from langchain.text_splitter import RecursiveCharacterTextSplitter
from dotenv import load_dotenv

load_dotenv()




def chunck_data(texts, chunk_size: int = 1000, chunk_overlap: int = 500):
    split_texts = []
    for text in texts:
        documents = [Document(page_content=text)]
        text_splitter = RecursiveCharacterTextSplitter(chunk_size = chunk_size, chunk_overlap = chunk_overlap)
        texts = text_splitter.split_documents(documents)
        print(f"Number of chunks: {len(texts)}")
        split_texts.extend(texts)
    return split_texts



def embed_data(texts, ticker):
    model = os.getenv("OPENAI_EMBEDDING_MODEL")
    embeddings = []
    count = 0
    n = len(texts)

    for text in texts:
        response = openai.embeddings.create(
            input=text.page_content,
            model=model
        )
        embeddings.append(response.data[0].embedding)
        count += 1
        if count % 50 == 0:
            print(f"loops left: {n - count}")

    index = faiss.IndexFlatL2(len(embeddings[0]))
    index.add(np.array(embeddings).astype("float32"))
    faiss.write_index(index, os.getenv("VECTOR_STORE").format(ticker=ticker))
    vector_map = {}

    for i, text in enumerate(texts):
            vector_map[i] = texts

    with open(os.getenv("VECTOR_MAPPING").format(ticker=ticker), "w") as f:
        for i, text in enumerate(texts):
            f.write(f"{i}||{text}\n")
    
    return index, vector_map


def vectorize_data(texts, ticker):
    split_texts = chunck_data(texts=texts)
    return embed_data(split_texts, ticker)
    




    