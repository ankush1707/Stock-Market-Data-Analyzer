"""Step 1: get the data (Yahoo Finance first, CSV as fallback)."""
from pathlib import Path
import pandas as pd

SAMPLE_CSV = "data/sample_stock_data.csv"


def fetch_from_yahoo(ticker: str, start: str, end: str) -> pd.DataFrame:
    import yfinance as yf  # imported here so CSV mode works without it
    df = yf.download(ticker, start=start, end=end,
                     auto_adjust=True, progress=False)
    if df is None or df.empty:
        raise ValueError(f"No data returned for {ticker}")
    if isinstance(df.columns, pd.MultiIndex):      # newer yfinance versions
        df.columns = df.columns.get_level_values(0)
    return df.reset_index()


def load_from_csv(path: str) -> pd.DataFrame:
    if not Path(path).exists():
        raise FileNotFoundError(f"CSV not found: {path}")
    return pd.read_csv(path)


def get_stock_data(ticker, start, end, csv_path=None):
    """Return (raw_dataframe, source_label)."""
    if csv_path:                                    # user forced CSV mode
        return load_from_csv(csv_path), f"CSV: {csv_path}"
    try:
        df = fetch_from_yahoo(ticker, start, end)
        Path("data").mkdir(exist_ok=True)
        df.to_csv(f"data/{ticker}.csv", index=False)  # cache for offline use
        return df, "Yahoo Finance (yfinance)"
    except Exception as err:
        print(f"[warn] Yahoo fetch failed ({err}). Using CSV fallback.")
        if not Path(SAMPLE_CSV).exists():
            from src.make_sample_data import make_sample_csv
            make_sample_csv(SAMPLE_CSV)
        return load_from_csv(SAMPLE_CSV), f"CSV fallback: {SAMPLE_CSV} (synthetic)"
