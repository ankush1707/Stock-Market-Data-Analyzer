"""Step 5: charts saved to images/ (PNG) for your README."""
from pathlib import Path
import matplotlib
matplotlib.use("Agg")                       # works without a display
import matplotlib.pyplot as plt
import seaborn as sns

sns.set_theme(style="whitegrid")


def _save(fig, name, out_dir):
    Path(out_dir).mkdir(exist_ok=True)
    path = f"{out_dir}/{name}"
    fig.tight_layout()
    fig.savefig(path, dpi=150)
    plt.close(fig)
    return path


def plot_price(df, ticker, out_dir="images"):
    fig, ax = plt.subplots(figsize=(11, 5))
    ax.plot(df.index, df["Close"], label="Close", color="#1f77b4")
    hi, lo = df["Close"].idxmax(), df["Close"].idxmin()
    ax.scatter([hi], [df.loc[hi, "Close"]], color="green", zorder=5, label="Highest")
    ax.scatter([lo], [df.loc[lo, "Close"]], color="red", zorder=5, label="Lowest")
    ax.set(title=f"{ticker} Closing Price", xlabel="Date", ylabel="Price")
    ax.legend()
    return _save(fig, f"{ticker}_price.png", out_dir)


def plot_moving_averages(df, ticker, short=20, long=50, out_dir="images"):
    fig, ax = plt.subplots(figsize=(11, 5))
    ax.plot(df.index, df["Close"], label="Close", alpha=0.5)
    ax.plot(df.index, df[f"SMA_{short}"], label=f"SMA {short}")
    ax.plot(df.index, df[f"SMA_{long}"], label=f"SMA {long}")
    ax.set(title=f"{ticker} Moving Averages", xlabel="Date", ylabel="Price")
    ax.legend()
    return _save(fig, f"{ticker}_moving_averages.png", out_dir)


def plot_return_distribution(df, ticker, out_dir="images"):
    fig, ax = plt.subplots(figsize=(8, 5))
    sns.histplot(df["Daily_Return"].dropna(), bins=50, kde=True, ax=ax)
    ax.axvline(df["Daily_Return"].mean(), color="red", linestyle="--", label="Mean")
    ax.set(title=f"{ticker} Daily Return Distribution", xlabel="Daily return")
    ax.legend()
    return _save(fig, f"{ticker}_return_distribution.png", out_dir)


def plot_volatility(df, ticker, out_dir="images"):
    fig, ax = plt.subplots(figsize=(11, 4))
    ax.plot(df.index, df["Volatility_20"], color="purple")
    ax.set(title=f"{ticker} 20-Day Rolling Volatility (annualized)",
           xlabel="Date", ylabel="Volatility")
    return _save(fig, f"{ticker}_volatility.png", out_dir)


def plot_all(df, ticker, short=20, long=50, out_dir="images"):
    return [plot_price(df, ticker, out_dir),
            plot_moving_averages(df, ticker, short, long, out_dir),
            plot_return_distribution(df, ticker, out_dir),
            plot_volatility(df, ticker, out_dir)]
