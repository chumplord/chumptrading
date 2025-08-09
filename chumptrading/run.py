from chumptrading.ai import chat
from chumptrading.backtest import backtest
from chumptrading.data import fetch_data
from chumptrading.strategy import execute


config = {
    'tickers': ['SPY', 'TLT', 'DXY', 'GLD', 'CL=F'], # stocks, bonds, USD index, gold, oil
    'fred_series': {
        'GDP': 'GDP',
        'CPI': 'CPIAUCSL',
        'Unemployment Rate': 'UNRATE',
        'Fed Funds Rate': 'FEDFUNDS'
    },
    'start_date': '2024-01-01',
    'capital': 100,
    'max_leverage': 2
}


def run():
    # ========== CONFIG ==========
    tickers = config['tickers']
    fred_series = config['fred_series']
    start_date = config['start_date']
    capital = config['capital']
    max_leverage = config['max_leverage']

    # ========== STEP 1: FETCH DATA ==========
    data = fetch_data(tickers, fred_series, start_date)
    combined_data = data.combined()
    print("\n[DATA]")
    print(combined_data)

    # ========== STEP 2: AI STRATEGY GENERATION ==========
    strategy_code = chat(combined_data, tickers, fred_series.keys(), max_leverage)
    print("\n[AI GENERATED STRATEGY CODE]\n")
    print(strategy_code)

    # ========== STEP 3: EXECUTE AI STRATEGY ==========
    signal = execute(strategy_code, combined_data)
    print("\n[SIGNAL]")
    print(signal)

    # ========== STEP 4: BACKTEST ==========
    # # Convert to a regular DatetimeIndex
    # combined_data.index = pd.to_datetime(combined_data.index)
    #
    # # If created by resample('M'), the index may be MonthEnd — convert to Timestamp
    # if isinstance(combined_data.index, pd.PeriodIndex):
    #     combined_data.index = combined_data.index.to_timestamp()
    #
    # # Or if it's already DatetimeIndex with MonthEnd offsets, shift to actual month-end date
    # combined_data.index = combined_data.index.to_timestamp()

    backtest(combined_data, tickers, signal, capital)
