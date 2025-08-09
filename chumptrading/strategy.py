import pandas as pd
import numpy as np


def execute(strategy_code, data):
    # Execute the code string returned by AI
    local_vars = {'data': data}
    exec(strategy_code, globals(), local_vars)
    signal = local_vars.get('signal', None)

    if signal is None:
        raise ValueError('AI strategy did not return a signal series')

    return signal


def strategy_1(data) -> pd.Series:
    # Assume `data` is a DataFrame with columns: ["CL=F", "DXY", "GLD", "SPY", "TLT"]

    # Simple macro strategy:
    # - Long SPY when SPY > 20-day MA and DXY < 20-day MA
    # - Short SPY when SPY < 20-day MA and DXY > 20-day MA
    # - Flat otherwise

    ma_spy = data['SPY'].rolling(20).mean()
    ma_dxy = data['DXY'].rolling(20).mean()

    long_cond = (data['SPY'] > ma_spy) & (data['DXY'] < ma_dxy)
    short_cond = (data['SPY'] < ma_spy) & (data['DXY'] > ma_dxy)

    signal = pd.Series(0, index=data.index)
    signal[long_cond] = 1
    signal[short_cond] = -1

    # Ensure leverage ≤ 2
    signal = signal.clip(-2, 2)
    return signal


def strategy_2(data) -> pd.Series:
    # Assume data is your combined dataset with market + macro data
    # Columns: ['CL=F','DXY','GLD','SPY','TLT','GDP','CPI','Unemployment','FedFunds']

    # Convert to monthly data
    monthly_df = data.resample('M').last()

    # Macro indicators
    gdp_trend = monthly_df['GDP'].pct_change(4)  # YoY GDP growth
    inflation = monthly_df['CPI'].pct_change(12)  # YoY CPI
    unemployment = monthly_df['Unemployment']

    # Macro regime logic
    risk_on = (gdp_trend > 0) & (inflation < 0.04) & (unemployment < 6)
    risk_off = (gdp_trend < 0) | (unemployment > 6) | (inflation > 0.06)

    # Signal: 1=long SPY, -1=short SPY, 0=flat
    signal = pd.Series(0, index=monthly_df.index, dtype=int)
    signal[risk_on] = 1
    signal[risk_off] = -1

    # Leverage ≤ 2 (already within bounds)
    signal = signal.clip(-1, 1)

    signal.name = 'signal'
    return signal


def strategy_3(data) -> pd.Series:
    # Assume `data` is a monthly DataFrame with columns:
    # ['CL=F', 'DXY', 'GLD', 'SPY', 'TLT', 'GDP', 'CPI', 'Unemployment Rate', 'Fed Funds Rate']
    # Example structure:
    # data = pd.DataFrame(..., columns=['CL=F', 'DXY', 'GLD', 'SPY', 'TLT', 'GDP', 'CPI', 'Unemployment Rate', 'Fed Funds Rate'])
    # Strategy logic:
    # - If GDP growth > 0 and CPI < 2% and Unemployment Rate decreasing => risk-on: long SPY and short TLT (equity over bonds)
    # - If GDP growth < 0 or CPI > 3% or Unemployment Rate increasing => risk-off: long TLT and GLD, short SPY
    # - Otherwise flat
    # - Use DXY and CL=F as additional filters:
    #   - Strong USD (DXY up) and rising oil (CL=F up) => more risk-off
    #   - Weak USD and falling oil => more risk-on
    # - Combine signals, cap leverage at 2
    # Calculate macro signals
    gdp_growth = data['GDP'].pct_change()
    cpi_level = data['CPI']
    unemp_change = data['Unemployment Rate'].diff()

    # Market momentum signals (1 if price up last month, -1 if down)
    def momentum(series):
        return np.sign(series.pct_change())

    spy_mom = momentum(data['SPY'])
    tlt_mom = momentum(data['TLT'])
    gld_mom = momentum(data['GLD'])
    dxy_mom = momentum(data['DXY'])
    cl_mom = momentum(data['CL=F'])
    # Macro conditions
    risk_on_macro = (gdp_growth > 0) & (cpi_level < 0.02) & (unemp_change < 0)
    risk_off_macro = (gdp_growth < 0) | (cpi_level > 0.03) | (unemp_change > 0)
    # Market filters
    usd_strong = dxy_mom > 0
    oil_rising = cl_mom > 0
    # Combine signals
    signal = pd.Series(0, index=data.index)
    # Risk-on signal: long SPY (+1), short TLT (-1)
    risk_on_signal = risk_on_macro & (~usd_strong | ~oil_rising)
    # Risk-off signal: long TLT and GLD, short SPY (-1)
    risk_off_signal = risk_off_macro | (usd_strong & oil_rising)
    # Assign signals: +1 for risk-on, -1 for risk-off, 0 otherwise
    signal[risk_on_signal] = 1
    signal[risk_off_signal] = -1
    # Ensure leverage ≤ 2 by scaling signals if needed (here max abs(signal) is 1, so no scaling needed)
    # If you want to combine multiple assets, you can scale accordingly.
    # Final signal Series: 1=long, -1=short, 0=flat
    return signal
