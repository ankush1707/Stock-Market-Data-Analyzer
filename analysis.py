"""Steps 3-4: returns, moving averages, volatility, risk summary."""
import numpy as np
import pandas as pd

TRADING_DAYS = 252


def add_indicators(df: pd.DataFrame, short=20, long=50) -> pd.DataFrame:
    df = df.copy()
    df["Daily_Return"] = df["Close"].pct_change()
    df["Cumulative_Return"] = (1 + df["Daily_Return"]).cumprod() - 1
    df[f"SMA_{short}"] = df["Close"].rolling(short).mean()
    df[f"SMA_{long}"] = df["Close"].rolling(long).mean()
    df["Volatility_20"] = df["Daily_Return"].rolling(20).std() * np.sqrt(TRADING_DAYS)
    df["Trend"] = np.where(df[f"SMA_{short}"] > df[f"SMA_{long}"],
                           "Uptrend", "Downtrend")
    df.loc[df[f"SMA_{long}"].isna(), "Trend"] = np.nan
    # running peak -> drawdown (how far below the previous high)
    df["Drawdown"] = df["Close"] / df["Close"].cummax() - 1
    return df


def crossover_dates(df, short=20, long=50):
    """Dates where the short MA crosses the long MA."""
    above = (df[f"SMA_{short}"] > df[f"SMA_{long}"]) & df[f"SMA_{long}"].notna()
    change = above.ne(above.shift()) & df[f"SMA_{long}"].shift().notna()
    out = []
    for date in df.index[change]:
        out.append((date, "Golden cross (bullish)" if above.loc[date]
                    else "Death cross (bearish)"))
    return out


def summarize(df: pd.DataFrame, rf=0.0) -> dict:
    r = df["Daily_Return"].dropna()
    ann_ret = (1 + r.mean()) ** TRADING_DAYS - 1
    ann_vol = r.std() * np.sqrt(TRADING_DAYS)
    return {
        "start_date": df.index[0], "end_date": df.index[-1],
        "trading_days": len(df),
        "start_price": df["Close"].iloc[0], "end_price": df["Close"].iloc[-1],
        "highest_close": df["Close"].max(), "highest_date": df["Close"].idxmax(),
        "lowest_close": df["Close"].min(), "lowest_date": df["Close"].idxmin(),
        "total_return": df["Close"].iloc[-1] / df["Close"].iloc[0] - 1,
        "avg_daily_return": r.mean(),
        "annualized_return": ann_ret,
        "annualized_volatility": ann_vol,
        "sharpe_ratio": (ann_ret - rf) / ann_vol if ann_vol else np.nan,
        "max_drawdown": df["Drawdown"].min(),
        "best_day": r.max(), "best_day_date": r.idxmax(),
        "worst_day": r.min(), "worst_day_date": r.idxmin(),
        "current_trend": df["Trend"].dropna().iloc[-1] if df["Trend"].notna().any() else "n/a",
    }


def risk_label(ann_vol: float) -> str:
    if ann_vol < 0.15:
        return "Low"
    if ann_vol < 0.30:
        return "Moderate"
    return "High"
