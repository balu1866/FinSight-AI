import requests
from bs4 import BeautifulSoup
from pathlib import Path
import time



SEC_BASE_URL = "https://www.sec.gov"
CIK_LOOKUP_URL = "https://www.sec.gov/files/company_tickers.json"

HEADERS = {
    "User-Agent": "FinSight AI Project (radhakrishnabalaji99@gmail.com)"
}


def get_cik(ticker :str) -> str:
    res = requests.get(CIK_LOOKUP_URL, headers=HEADERS)
    res.raise_for_status()
    cik_map = res.json()
    for entry in cik_map.values():
        if(entry["ticker"].lower() == ticker.lower()):
            return str(entry["cik_str"]).zfill(10)
    raise ValueError(f"CIK not found for ticker: {ticker}")


def get_sec_filing_links(cik: str, form_type = "10-K", count = 100):
    url = f"https://data.sec.gov/submissions/CIK{cik}.json"

    res = requests.get(url, headers=HEADERS)
    res.raise_for_status()
    data = res.json()

    filings = data["filings"]["recent"]
    links = []
    for i, form in enumerate(filings["form"]):
        if form==form_type:
            accession = filings["accessionNumber"][i].replace("-", "")
            link = f"{SEC_BASE_URL}/Archives/edgar/data/{int(cik)}/{accession}/index.json"
            links.append(link)
            if(len(links) > count):
                break
    return links

def download_filings(filing_url: str, ticker:str):
    res = requests.get(filing_url, headers=HEADERS)
    res.raise_for_status()
    files = res.json()["directory"]["item"]

    for file in files:
        name = file["name"]
        if name.endswith(".htm") and ticker.lower() in name.lower():
            doc_url = filing_url.replace("index.json", name)
            doc_res = requests.get(doc_url, headers=HEADERS)
            doc_res.raise_for_status()
            soup = BeautifulSoup(doc_res.text, "html.parser")
            return soup.get_text()
    return None

def save_filing(ticker: str, text: str, form_type="10-K"):
    folder = Path(f"data/filings/{ticker.lower()}")
    folder.mkdir(parents=True, exist_ok=True)
    filename = folder / f"{form_type}_{int(time.time())}.txt"
    filename.write_text(text)
    print(f"[+] Saved filing to {filename}")

if __name__ == "__main__":
    ticker = "AAPL"
    cik = get_cik(ticker)
    print("CIK:", cik)

    filing_links = get_sec_filing_links(cik, form_type="10-K", count=1)
    for link in filing_links:
        print("Filing URL:", link)
        filing_text = download_filings(link, ticker)
        save_filing(ticker, filing_text)