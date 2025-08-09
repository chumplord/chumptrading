from langchain.tools import tool

from chumptrading.ai import (
    chat,
    get_prompt_for_strategy_idea,
    get_prompt_for_strategy_code_from_strategy_text
)
from chumptrading.data import Data, fetch_data
from chumptrading.mcp import StrategyMCP
from chumptrading.strategy import execute

strategy_mcp = StrategyMCP()


@tool
def get_market_data(start_date, tickers, fred_series) -> Data:
    """Fetch and return raw market and macroeconomic data only.
    Does NOT analyze or create strategies. Input: start_date, tickers, fred_series."""
    return fetch_data(start_date, tickers, fred_series)


@tool
def get_strategy_idea(data: Data) -> str:
    """Analyze the given Data object and return ONLY a trading strategy idea in plain text.
    Input must be a Data object, not raw parameters."""
    prompt = get_prompt_for_strategy_idea(data)
    strategy = chat(prompt)
    strategy_mcp.add_strategy('hi', strategy)
    return strategy


@tool
def execute_strategy(strategy_idea: str, data: Data):
    """Use the strategy idea to generate Python code that will be run"""
    prompt = get_prompt_for_strategy_code_from_strategy_text(strategy_idea)
    strategy_code = chat(prompt)
    signal = execute(strategy_code, data.combined())
    return signal


tools = [get_market_data, get_strategy_idea]
