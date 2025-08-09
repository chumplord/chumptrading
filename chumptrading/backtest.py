import vectorbt as vbt


FEES = 0.001


def run(market_data, signal, capital):
    print("\n[INFO] Running backtest...")

    return vbt.Portfolio.from_signals(
        close=market_data,
        entries=signal == 1,
        exits=signal == 1,
        init_cash=capital,
        fees=FEES
    )


def backtest(market_data, tickers, signal, capital):
    for ticker in tickers:
        try:
            portfolio = run(market_data[ticker], signal, capital)
            print(f'\n[BACKTEST RESULTS FOR {ticker}]')
            print(portfolio)
            print(portfolio.close)
            print(portfolio.order_records)
            print(portfolio.log_records)
            print(portfolio.init_cash)
            print(portfolio.stats())
            portfolio.plot().show()

        except ValueError as e:
            print(f'Value error: {e}')

        except Exception as e:
            print(f'Unexpected explosion: {e}')
