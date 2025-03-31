import openai
import os
import numpy as np

from dotenv import load_dotenv
import openai

# from filings_prompt import PROMPT

load_dotenv()



PROMPT="""
You are a financial analyst assistant. Use only the information provided in the SEC filing excerpts below to answer the user’s question.

If the context does not contain enough information to answer the question, say "The filing does not provide a clear answer to that."

Context:
{context}


Question: {question}

Answer:
"""

model = os.getenv("OPENAI_EMBEDDING_MODEL")

def ask_gpt(question: str, index, vector_map):

    client = openai.Client(api_key=os.getenv("OPENAI_API_KEY"))

    embed_question = client.embeddings.create(
            input=question,
            model=model
        ).data[0].embedding
    
    question_embedding = np.array(embed_question).astype("float32")
    D, I = index.search(question_embedding.reshape(1, -1), 5)
    context  = " ".join([vector_map[i] for i in I[0]])

    response = client.chat.completions.create(
        model = "chatgpt-4o-latest",
        messages = [
            {"role": "system", "content": "You are an intelligent assistant."},
            {"role": "user", "content": PROMPT.format(context=context, question=question)}
        ]
    )

    return response.choices[0].message.content