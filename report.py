"""Step 6: write a Markdown insights report."""
from pathlib import Path
from src.analysis import risk_label


def build_report(ticker, source, s, crosses, short=20, long=50) -> str:
    d = lambda x: x.strftime("%Y-%m-%d")
    lines = [
        f"# {ticker} Stock Analysis Report", "",
        f"- **Data source:** {source}",
        f"- **Period:** {d(s['start_date'])} to {d(s['end_date'])} ({s['trading_days']} trading days)", "",
        "## Price Summary",
        f"- Start price: {s['start_price']:.2f} | End price: {s['end_price']:.2f}",
        f"- Highest close: {s['highest_close']:.2f} on {d(s['highest_date'])}",
        f"- Lowest close: {s['lowest_close']:.2f} on {d(s['lowest_date'])}",
        f"- Total return: {s['total_return']:.2%}", "",
        "## Return & Risk",
        f"- Average daily return: {s['avg_daily_return']:.3%}",
        f"- Annualized return: {s['annualized_return']:.2%}",
        f"- Annualized volatility: {s['annualized_volatility']:.2%} "
        f"({risk_label(s['annualized_volatility'])} risk)",
        f"- Sharpe ratio (risk-free = 0): {s['sharpe_ratio']:.2f}",
        f"- Maximum drawdown: {s['max_drawdown']:.2%}",
        f"- Best day: {s['best_day']:.2%} ({d(s['best_day_date'])})",
        f"- Worst day: {s['worst_day']:.2%} ({d(s['worst_day_date'])})", "",
        "## Trend",
        f"- Current trend (SMA {short} vs SMA {long}): **{s['current_trend']}**",
    ]
    if crosses:
        lines.append(f"- Recent crossovers:")
        for date, kind in crosses[-5:]:
            lines.append(f"  - {d(date)}: {kind}")
    lines += ["", "## Charts", f"![Price](../images/{ticker}_price.png)",
              f"![Moving averages](../images/{ticker}_moving_averages.png)",
              f"![Returns](../images/{ticker}_return_distribution.png)", "",
              "> Educational project. Not financial advice."]
    return "\n".join(lines)


def save_report(text, ticker, out_dir="reports") -> str:
    Path(out_dir).mkdir(exist_ok=True)
    path = f"{out_dir}/{ticker}_report.md"
    Path(path).write_text(text, encoding="utf-8")
    return path
