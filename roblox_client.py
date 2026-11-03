# roblox_client.py - polite client for Roblox's public JSON endpoints (TODO)
#
# Read-only: no login, no cookies, no purchasing.
#
# Throttling:
#   # wait = last_request_time + request_delay_s + random(0, request_jitter_s) - now
#   # if wait > 0: sleep(wait)
#
# Backoff on HTTP 429:
#   # use the Retry-After header if present, otherwise
#   # wait = min(900, 30 * 2^attempt)          -> 30s, 60s, 120s, ...
#   # after 5 consecutive 429s raise RateLimited so the main loop can sleep for a long time
#
# Other errors:
#   # network error  -> wait = min(60, 5 * 2^attempt), retry
#   # 5xx            -> wait = min(120, 10 * 2^attempt), retry
#   # 400 / 404      -> return None
#
# Endpoints (three-stage funnel):
#   1. iter_limited_catalog()  catalog search, ~60 items per request
#                              -> yield {id, name, lowest listing price} for limited items
#   2. resale_data(asset_id)   RAP, sales count, daily price points, daily volume points
#   3. lowest_resale(asset_id) live cheapest listing = min(listing prices),
#                              used to confirm a deal right before alerting
