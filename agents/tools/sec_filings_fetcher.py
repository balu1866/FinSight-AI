import os
import faiss

from langchain.tools import tool
from loaders.sec_filings import get_cik, get_sec_filing_links, download_filings, save_filing
from rag.vector_process import vectorize_data
from rag.retriever import ask_gpt

from dotenv import load_dotenv

load_dotenv()


@tool("FilingsFetcher", return_direct=True)
def sec_filings_fetcher_tool(ticker_and_query:str)->str:
    """
    Answers a question about the most recent SEC filing for a given company.
    Format: TICKER: question text
    Example: AAPL: What risks does Apple mention in its 10-K?
    """
    try:
        if ":" not in ticker_and_query:
            return "Please format your input as 'TICKER: your question'."

        ticker, question = map(str.strip, ticker_and_query.split(":", 1))

        
        try:
            index = faiss.read_index(os.getenv("VECTOR_STORE").format(ticker=ticker))
            vector_map = {}
            with open(os.getenv("VECTOR_MAPPING").format(ticker=ticker), "r") as f:
                for line in f:
                    idx, text = line.strip().split("||")
                    vector_map[int(idx)] = text
        except Exception as e:
            cik = get_cik(ticker=ticker)
            links = get_sec_filing_links(cik=cik)
            filing_texts = []
            for link in links:
                print("Filing URL:", link)
                filing_text = download_filings(link, ticker)
                if(filing_text != None):
                    filing_texts.append(filing_text)
            index, vector_map = vectorize_data(filing_texts, ticker)

        result = ask_gpt(question=question, index=index, vector_map=vector_map)

        return result
    except Exception as e:
        return f"Error fetching RAG info for '{ticker_and_query}': {e}"

        