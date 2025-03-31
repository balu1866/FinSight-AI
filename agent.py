import os

from langchain.agents import initialize_agent, Tool
from langchain.chat_models import ChatOpenAI
from agents.tools.stock_fetcher import fetch_stock_info_tool
from agents.tools.sec_filings_fetcher import sec_filings_fetcher_tool
from dotenv import load_dotenv

load_dotenv()


llm = ChatOpenAI(openai_api_key=os.getenv("OPENAI_API_KEY"), temperature=0)

tools = [
    fetch_stock_info_tool,
    sec_filings_fetcher_tool
]

agent = initialize_agent(
    tools,
    llm,
    agent="zero-shot-react-description",
    verbose=True
)

# response = agent.run("Get the stock price and valuation of AAPL.")
# print(response)

response = agent.run('AAPL: What risks are mentioned in the latest 10-K?')
print(response)
