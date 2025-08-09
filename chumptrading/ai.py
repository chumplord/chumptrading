import os
from typing import Optional

from openai import OpenAI

from chumptrading.cache import cache
from chumptrading.data import Data
from chumptrading.spend import check_budget, log_usage

MODEL = "gpt-4.1-mini"
TEMPERATURE = 0.7

openai_api_key = os.getenv("OPENAI_API_KEY")
client = OpenAI(api_key=openai_api_key)


def get_prompt_for_strategy_code(data, tickers, macro_data, max_leverage) -> str:
    return f"""
    You are a macro trading strategist. Based on the following historical market data and macroeconomic indicators:

    MARKET DATA: {', '.join(tickers)}
    MACRO DATA: {', '.join(macro_data)}

    Design a simple systematic macro trading strategy in Python that:
    - Uses both market and macro data in a single pandas DataFrame, which will be available in a variable called 'data'
    - Creates a 'signal' Series (1=long, -1=short, 0=flat)
    - Uses pandas and is compatible with vectorbt
    - Keeps leverage ≤ {max_leverage}
    - Focuses on monthly data

    Here is a small sample of the combined dataset:
    {data.tail(10).to_string()}

    The strategy code will be run with the Python exec function
    Output ONLY valid Python code that defines 'signal'
    """


def get_prompt_for_strategy_idea(data: Data):
    return f"""
    You are a macro trading strategist. Based on the following macro data context:
    
    MARKET DATA: {', '.join(data.tickers)}
    MACRO DATA: {', '.join(data.macro_series)}

    Propose one trading strategy in plain English. 
    Avoid code — describe triggers, data sources, and execution logic at a high level.
    Give the strategy a pithy name
    """


def get_prompt_for_strategy_code_from_strategy_text(strategy_idea):
    return f"""
    Convert the following trading strategy description into Python code using:
    - vectorbt for backtesting
    - yfinance or FRED for data
    - pandas for data manipulation
    Ensure:
    - Prices, signals, and dates align
    - Output includes portfolio stats

    STRATEGY:
    {strategy_idea}
    """


def _clean_code(code):
    def clean(c):
        return "\n".join(
            line for line in c.splitlines()
            if not line.strip().startswith("```")
        )
    return clean(code) if code.startswith("```") else code


@cache
def chat(prompt, temperature=TEMPERATURE) -> Optional[str]:
    check_budget()  # Enforce budget before calling API
    print(prompt)

    response = client.chat.completions.create(
        model=MODEL,
        messages=[
            {
                "role": "user",
                "content": prompt
            }
        ],
        temperature=temperature
    )

    log_usage(response.usage, MODEL)

    completion = response.choices[0].message.content.strip()
    return _clean_code(completion)
