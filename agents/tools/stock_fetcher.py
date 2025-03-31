import sys
import os

from langchain.tools import tool
from langchain.tools import tool

from loaders.stock_data import get_stock_data

@tool("StockDataFetcher", return_direct=True)
def fetch_stock_info_tool(ticker: str) -> str:
    """
    Fetches stock price, P/E ratio, market cap, and sector for a given ticker.
    Returns a human-readable summary.
    """
    try: 
        data = get_stock_data(ticker, include_history = False)
        info = data.get("info", {})
        if not info:
            return f"No data found for ticker '{ticker}'."
        
        results = (f"{info['ticker']} is currently trading at ${info['current_price']}.\n"
            f"Market Cap: ${info['market_cap']:,}\n"
            f"P/E Ratio: {info['pe_ratio']}\n"
            f"Forward P/E: {info['forward_pe']}\n"
            f"Beta: {info['beta']}\n"
            f"Sector: {info['sector']}\n\n"
            f"Summary: {info['summary'][:400]}...")
        
        
        return results
    
    except Exception as e:
        return f"Error fetching stock info for '{ticker}': {e}"