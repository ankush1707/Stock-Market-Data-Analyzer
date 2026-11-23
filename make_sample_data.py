"""Create a SYNTHETIC price file so the project runs offline (CSV fallback)."""
import numpy as np
import pandas as pd
from pathlib import Path


def make_sample_csv(path="data/sample_stock_data.csv", days=600, seed=42):
    rng = np.random.default_rng(seed)
    dates = pd.bdate_range(end=pd.Timestamp.today().normalize(), periods=days)
    returns = rng.normal(0.0005, 0.015, days)          # fake daily returns
    close = 100 * np.cumprod(1 + returns)
    open_ = close * (1 + rng.normal(0, 0.004, days))
    high = np.maximum(open_, close) * (1 + rng.uniform(0, 0.01, days))
    low = np.minimum(open_, close) * (1 - rng.uniform(0, 0.01, days))
    volume = rng.integers(1_000_000, 5_000_000, days)
    df = pd.DataFrame({"Date": dates, "Open": open_, "High": high,
                       "Low": low, "Close": close, "Volume": volume})
    df[["Open", "High", "Low", "Close"]] = df[["Open", "High", "Low", "Close"]].round(2)
    Path(path).parent.mkdir(parents=True, exist_ok=True)
    df.to_csv(path, index=False)
    return path


if __name__ == "__main__":
    print("Created", make_sample_csv())
