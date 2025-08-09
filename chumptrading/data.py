import os
from typing import List, Any

import pandas as pd
import yfinance as yf
from fredapi import Fred
from pydantic import BaseModel


fred_api_key = os.getenv('FRED_API_KEY')
fred = Fred(api_key=fred_api_key)
fred_default = {
    'GDP': 'GDP',
    'CPI': 'CPIAUCSL',
    'Unemployment Rate': 'UNRATE',
    'Fed Funds Rate': 'FEDFUNDS'
}


class Data(BaseModel):
    tickers: List[str]
    macro_series: List[str]
    market_data: Any
    macro_data: Any

    def combined(self):
        macro_data_monthly = self.macro_data.resample('M').last()
        market_data_monthly = self.market_data.resample('M').last()
        combined = market_data_monthly.join(macro_data_monthly, how='inner')
        return combined


def fetch_market_data(tickers, start_date) -> pd.DataFrame:
    print("[INFO] Fetching market data...")
    data = yf.download(tickers, start=start_date)
    return data['Close']


def fetch_macro_data(fred_series, start_date) -> pd.DataFrame:
    print("[INFO] Fetching macro data...")
    macro_df = pd.DataFrame()

    for name, code in fred_series.items():
        series_data = fred.get_series(code)
        series_data.index = pd.to_datetime(series_data.index)
        macro_df[name] = series_data

    macro_df = macro_df[macro_df.index >= pd.to_datetime(start_date)]
    return macro_df


def fetch_data(start_date, tickers, fred_series) -> Data:
    fred_series = fred_series or fred_default
    macro_data = fetch_macro_data(fred_series, start_date)
    market_data = fetch_market_data(tickers, start_date)

    return Data(
        tickers=tickers,
        macro_series=set(fred_series.keys()),
        market_data=market_data,
        macro_data=macro_data
    )
