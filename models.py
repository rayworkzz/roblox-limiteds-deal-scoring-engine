# models.py - all the maths (TODO). Pure NumPy, no network, so it can be unit-tested.
#
# Pipeline for one item:
#   1. short_term_trend()  last 5 sales, log-linear regression
#   2. long_features()     EMA/MACD, RSI, 90d trend, volatility, drawdown, liquidity
#   3. seasonal_tilt()     month-of-year effect (needs ~18 months of data)
#   4. performance()       blend into a 1-10 score P
#   5. factor + threshold
#   6. DealNet             neural net grades the deal 0-100 -> colour tier
#
# ------------------------------------------------------------------ basics
# deal_pct(rap, price)
#   # deal% = 100 * (rap - price) / rap
#
# ema(x, span)
#   # alpha = 2 / (span + 1)
#   # ema[0] = x[0];  ema[i] = alpha * x[i] + (1 - alpha) * ema[i-1]
#
# rsi(prices, n=14)
#   # d = diff(prices) over the last n steps
#   # up = mean of positive moves, down = mean of |negative moves|
#   # RSI = 100 - 100 / (1 + up / down)       (100 if down == 0, 50 if not enough data)
#
# ------------------------------------------------------------------ 1. short-term trend
# short_term_trend(rap_ref, sales)   using the last 5 sale prices (need >= 3)
#   # fit log(price_i) = a + b * i  by least squares        (np.polyfit)
#   # slope% per sale = 100 * b
#   # R^2 = 1 - SS_res / SS_tot
#   # drop% = 100 * (1 - mean(prices) / rap_ref)            rap_ref = the price before these 5
#   # bad = 0.6 * tanh(-slope% / 2) * sqrt(R^2) + 0.4 * tanh(drop% / 15)
#   #   -> in [-1, 1]; positive = falling (bad), negative = rising (good)
#   #   -> slope is trusted in proportion to how well the line fits
#
# ------------------------------------------------------------------ 2. long-term features
# long_features(prices, volumes)    (return None if fewer than 30 daily points)
#   # macd     = EMA7[-1] / EMA30[-1] - 1                   momentum
#   # rsi      = RSI(14)
#   # slope90  = slope of log(price) over the last 90 days  (per day)
#   # vol      = std of daily log returns over last 60 days volatility
#   # drawdown = 1 - price[-1] / max(price over last 180 days)
#   # med30    = median price over last 30 days            (RAP manipulation check)
#   # avg_vol  = mean daily sales over last 30 days         liquidity
#
# ------------------------------------------------------------------ 3. seasonality
# seasonal_tilt(days, prices, today)   (return None if fewer than ~540 days)
#   # detrend: fit log(price) = a + b * t, resid = log(price) - (a + b * t)
#   # for each calendar month m: idx[m] = mean(resid in month m) * k / (k + 2)
#   #   where k = number of distinct years seen (shrinks months with little data)
#   # tilt = idx[next month] - idx[this month]
#
# ------------------------------------------------------------------ 4. performance score
# Each component in [-1, 1], positive = good:
#   # short  = -bad
#   # mom    = 0.7 * tanh(10 * macd) + 0.3 * (rsi - 50) / 50
#   # trend  = tanh(slope90 * 30 / 0.05)                    5% per 30 days -> 0.76
#   # dd     = 1 - 2 * tanh(drawdown / 0.3)
#   # vol    = clip((0.03 - vol) / 0.03, -1, 1)
#   # liq    = clip(2 * (log1p(avg_vol) / log1p(20) - 0.5), -1, 1)
#   # season = tanh(tilt / 0.08)
# Weights: short 0.25, mom 0.20, trend 0.15, dd 0.10, season 0.10, vol 0.10, liq 0.10
#   # s = sum(w_k * c_k) / sum(w_k for components available)   (renormalise when data is thin)
#   # P = clip(5.5 + 4.5 * clip(1.5 * s, -1, 1), 1, 10)
# Labels: <3 Terrible, <5 Bad, <6.5 Mediocre, <8.5 Good, else Excellent
#
# ------------------------------------------------------------------ 5. factor + threshold
#   # factor    = exp(-0.3 * (P - 5.5) / 4.5)     ~1.35 at P=1, 1.00 at P=5.5, ~0.74 at P=10
#   # threshold = base_deal_pct * factor
#   # alert only if deal% >= threshold
#   # e.g. base 25%, P=3 -> factor 1.18 -> 29.5% needed; P=8 -> 0.85 -> 21.2%
#
# ------------------------------------------------------------------ 6. DealNet
# Inputs (6):
#   # margin  = clip((deal% - threshold) / 30, 0, 1.5)
#   # depth   = clip(deal% / 60, 0, 1.5)
#   # quality = (P - 5.5) / 4.5
#   # liq     = clip(log1p(avg_vol) / log1p(20), 0, 1)
#   # risk    = clip(vol / 0.06, 0, 1)
#   # infl    = clip((rap / med30 - 1) / 0.5, 0, 1)        flags an inflated RAP
# Network: 6 inputs -> 4 tanh hidden units -> 1 sigmoid output
#   # h = tanh(W1 @ x + b1);  y = sigmoid(W2 @ h + b2);  score = 100 * y
#   # hand-set starting weights: h0 value, h1 quality, h2 risk (negative output weight),
#   # h3 value x quality
# Training (fit): plain SGD on log-loss
#   # dz2 = y - target
#   # dz1 = (dz2 * W2) * (1 - h^2)
#   # W2 -= lr * dz2 * h;      b2 -= lr * dz2
#   # W1 -= lr * outer(dz1, x); b1 -= lr * dz1
# Tiers: Yellow >= 85, Purple >= 72, Blue >= 58, Green >= 45, else Grey
