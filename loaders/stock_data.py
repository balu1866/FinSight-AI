import yfinance as yf
import json
import time
import pandas as pd


from pathlib import Path


def get_stock_data(ticker : str, 
                   period: str = "2mo", 
                   interval: str = "1d",
                   include_history = False):
    stock = yf.Ticker(ticker)
    info = stock.info

    result = {}
    result["info"] = {
        "ticker": ticker,
        "current_price": info.get("currentPrice"),
        "market_cap": info.get("marketCap"),
        "pe_ratio": info.get("trailingPE"),
        "forward_pe": info.get("forwardPE"),
        "beta": info.get("beta"),
        "sector": info.get("sector"),
        "summary": info.get("longBusinessSummary")
    }

    if include_history:
        df = stock.history(period=period, interval=interval)
        result["history"] = df

    return result

if __name__ == "__main__":
    ticker = "AAPL"
    include_history=True
    data = get_stock_data(ticker=ticker, include_history=include_history)
    folder = Path(f"data/stock/{ticker.lower()}")
    folder.mkdir(parents=True, exist_ok=True)
    name = f"{ticker}_stock_info_{int(time.time())}.txt"
    filename = folder / name

    name_csv = f"{ticker}_stock_info_csv_{int(time.time())}.txt"
    filename_csv = folder / name_csv

    df = pd.DataFrame(data=data["history"])

    with open(str(filename), 'w', encoding='utf-8') as f:
        f.write(json.dumps(data["info"]))

    if include_history:
        df.to_csv(str(filename_csv), index=False)

