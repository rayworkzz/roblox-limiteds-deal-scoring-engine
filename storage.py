# storage.py - SQLite persistence for price/volume history (TODO)
#
# Tables:
#   # items(asset_id PK, name, rap, rap_checked, lowest, lowest_seen, sales)
#   # snapshots(asset_id, ts, rap, lowest, sales)           + index on (asset_id, ts)
#   # points(asset_id, day, price, volume)                  PK (asset_id, day)
#   # alerts(asset_id, ts, price, rap, deal_pct, perf, net, tier)
#
# Use WAL journal mode so reads and writes don't block each other.
#
# Methods:
#   # upsert_listing(aid, name, lowest)  insert or update the latest lowest price
#   # save_resale(aid, data)             merge daily price + volume points by date,
#   #                                    update RAP, add a snapshot row
#   # series(aid)                        -> (days, prices, volumes) ordered by day
#
# Scheduling queries:
#   # rap_due(): items never checked, OR
#   #            RAP >= 0.8 * min_rap and last check older than rap_refresh_h, OR
#   #            RAP <  0.8 * min_rap and last check older than low_rap_recheck_h
#   #            ordered oldest-first, limited to the per-sweep budget
#   # candidates(): items seen this sweep where
#   #            RAP >= min_rap and (rap - lowest) * 100 / rap >= pre-filter %
#
# Alerts:
#   # last_alert_ts(aid) = MAX(ts) from alerts (for the cooldown)
#   # record_alert(...)
