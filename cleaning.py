"""Step 2: clean the raw data."""
import pandas as pd

NUMERIC = ["Open", "High", "Low", "Close", "Volume"]


def clean_data(df: pd.DataFrame, start=None, end=None) -> pd.DataFrame:
    df = df.copy()
    df.columns = [str(c).strip().title() for c in df.columns]
    if "Close" not in df.columns and "Adj Close" in df.columns:
        df["Close"] = df["Adj Close"]
    if "Date" not in df.columns:
        raise ValueError("Data needs a 'Date' column")

    df["Date"] = pd.to_datetime(df["Date"], errors="coerce")
    df = df.dropna(subset=["Date"])
    for col in NUMERIC:
        if col in df.columns:
            df[col] = pd.to_numeric(df[col], errors="coerce")

    df = (df.sort_values("Date")
            .drop_duplicates(subset="Date")
            .set_index("Date"))
    df = df.ffill().dropna(subset=["Close"])        # fill small gaps

    if start:
        df = df[df.index >= pd.to_datetime(start)]
    if end:
        df = df[df.index <= pd.to_datetime(end)]
    if len(df) < 60:
        raise ValueError("Need at least ~60 rows for a 50-day moving average")
    return df
