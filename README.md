# Quantitative Deal-Scoring Engine for Roblox Limiteds

> **Status: in development.** This repo currently holds the project plan. Each file describes, in comments, what it will do and the calculations it needs. The code is being written file by file, and the commit history tracks that progress.

## What this project is

A Python engine that spots underpriced Roblox limited items on the resale market and posts alerts to Discord.

It extends a simpler deal-alert bot I wrote in 2024. That bot flagged any item listed a fixed percentage below its RAP (recent average price). This version treats each item like a stock. It looks at the item's price history and decides how big a discount is needed before a listing counts as a real deal:

- An item in a **healthy uptrend** needs a *smaller* discount to be worth alerting on.
- An item that is **crashing, volatile or illiquid** needs a *bigger* discount.

Qualifying deals are then graded by a small neural network into five colour-coded Discord alert tiers.

> **Alert-only.** Public read-only endpoints, never log in, and never buy anything.

## Planned features

- **Rate-limited data pipeline**: a three-stage request funnel to keep API calls to a minimum, with at least 2 seconds between requests and backoff on HTTP 429.
- **SQLite history store**: daily price/volume points, RAP snapshots and sent alerts, so history survives restarts.
- **Stock-market-style model**: log-linear regression on recent sales, EMA/MACD momentum, RSI, volatility, drawdown, liquidity and seasonality.
- **1-10 performance score** that dynamically scales the required discount.
- **Deal-grading neural network** (NumPy): scores each deal 0-100 and maps it to Yellow / Purple / Blue / Green / Grey.
- **Discord embeds** with price, RAP, discount, rating and trend stats.
- **Offline test suite** on synthetic data, plus CI.
- **systemd deployment** on a Linux VPS.

## Planned pipeline

```
catalog scan (cheap, many items per request)  ->  lowest listing price per item
        |
RAP refresh (limited budget per sweep)        ->  RAP + daily price/volume history -> SQLite
        |
candidates only (looks like a deal)           ->  fresh RAP -> model -> live price re-check
        |
neural net score 0-100                        ->  tier colour -> Discord alert
```

## Planned model (summary)

| Step | Idea |
|------|------|
| Short-term trend | Log-linear regression over the last 5 sale prices: is the price sliding? |
| Long-term features | EMA/MACD momentum, RSI, 90-day trend, volatility, drawdown, liquidity |
| Seasonality | Month-of-year effect, only once there is enough history |
| Performance score `P` | Weighted blend of the above, mapped to 1-10 |
| Factor | `exp(-0.3 * (P - 5.5) / 4.5)`: above 1 for weak items, below 1 for strong ones |
| Threshold | `base_deal_pct x factor` |
| Deal grade | Small neural net -> 0-100 -> colour tier |

The full calculations are written out as comments in `models.py`.

## Project structure

```
main.py            scan loop + command-line options
config.py          tunable settings; secrets come from .env
roblox_client.py   throttled HTTP client with backoff
storage.py         SQLite persistence
models.py          trend, indicators, performance score, neural net
notifier.py        Discord embed builder + sender
selftest.py        offline tests on synthetic data
```

## Roadmap

- [ ] `config.py`: settings and `.env` loading
- [ ] `roblox_client.py`: throttled client, catalog scan, resale data, live price check
- [ ] `storage.py`: SQLite schema and queries
- [ ] `models.py`: basic helpers (deal %, EMA, RSI)
- [ ] `models.py`: short-term trend (log-linear regression)
- [ ] `models.py`: long-term indicators
- [ ] `models.py`: seasonality
- [ ] `models.py`: performance score, factor and threshold
- [ ] `models.py`: deal-grading neural net + training
- [ ] `notifier.py`: Discord embeds
- [ ] `main.py`: three-stage sweep and run loop
- [ ] `selftest.py`: offline tests
- [ ] GitHub Actions CI running the tests
- [ ] systemd service file and VPS deployment
- [ ] Backtest over stored history

## Tech

Python, NumPy, SQLite, requests, Discord REST API, systemd.

## Licence

MIT, see `LICENSE`.
