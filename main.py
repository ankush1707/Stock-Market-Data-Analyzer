"""Run the full pipeline:  python main.py --ticker AAPL"""
import argparse
from datetime import date, timedelta

from src.data_loader import get_stock_data
from src.cleaning import clean_data
from src.analysis import add_indicators, summarize, crossover_dates
from src.visualize import plot_all
from src.report import build_report, save_report


def run(ticker, start, end, csv=None, short=20, long=50):
    raw, source = get_stock_data(ticker, start, end, csv)
    df = clean_data(raw, start if not csv else None, end if not csv else None)
    df = add_indicators(df, short, long)
    summary = summarize(df)
    crosses = crossover_dates(df, short, long)
    charts = plot_all(df, ticker, short, long)
    df.to_csv(f"outputs/{ticker}_analysis.csv")
    report_path = save_report(build_report(ticker, source, summary, crosses, short, long), ticker)
    return df, summary, charts, report_path


if __name__ == "__main__":
    p = argparse.ArgumentParser(description="Stock Market Data Analyzer")
    p.add_argument("--ticker", default="AAPL")
    p.add_argument("--start", default=str(date.today() - timedelta(days=730)))
    p.add_argument("--end", default=str(date.today()))
    p.add_argument("--csv", default=None, help="Use a local CSV instead of Yahoo")
    a = p.parse_args()
    _, s, charts, rpt = run(a.ticker.upper(), a.start, a.end, a.csv)
    print(f"Total return {s['total_return']:.2%} | Volatility {s['annualized_volatility']:.2%} "
          f"| Max drawdown {s['max_drawdown']:.2%} | Trend {s['current_trend']}")
    print("Charts:", *charts, sep="\n  ")
    print("Report:", rpt)
