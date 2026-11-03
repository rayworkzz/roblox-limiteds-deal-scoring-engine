# selftest.py - offline tests on synthetic data, no network (TODO)
#
# Synthetic price history generator:
#   # log_price[t] = log_price[t-1] + drift + Normal(0, noise)
#   # optional seasonal term: amp * cos(2*pi * (day_of_year - 355) / 365)   (peak ~Dec 21)
#   # volume ~ Poisson(6)
#
# Planned tests:
#   1. worked example: RAP 50k, last 5 sales 42k, 41k, 44k, 36k, 43k -> should read as a decline
#      deal_pct(50,000, 30,000) == 40%
#   2. falling / flat / rising items:
#      factor(falling) > factor(flat) > factor(rising)
#      threshold(falling) > base > threshold(rising)
#   3. seasonality: 3 years with a December peak -> Nov->Dec tilt > 0, Jan->Feb tilt < 0;
#      400 days of data -> no seasonality claimed
#   4. factor curve at P = 1, 3, 5.5, 8, 10
#   5. DealNet: bigger deal scores higher; healthier item scores higher at the same deal
#   6. fit() lowers log-loss on toy labelled data
#   7. storage round trip (in-memory SQLite) + embed build
