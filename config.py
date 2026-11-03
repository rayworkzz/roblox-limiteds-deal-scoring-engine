# config.py - central configuration (TODO)
#
# Secrets come from a .env file, never hard-coded. Load them with python-dotenv.
#
# Secrets / identity (from .env):
#   - DISCORD_BOT_TOKEN
#   - DISCORD_CHANNEL_ID
#   - CONTACT_EMAIL        (goes in the User-Agent so Roblox can contact me)
#   - DB_PATH              (SQLite file, default roblox_bot.db)
#
# Deal rules:
#   - min_rap              only consider items with RAP above this (e.g. 50,000 R$)
#   - base_deal_pct        base discount threshold before scaling (e.g. 25%)
#   - alert_cooldown_h     don't re-alert the same item within this many hours
#
# Politeness / scheduling:
#   - scan_interval_min    pause between full sweeps (e.g. 60 min)
#   - request_delay_s      minimum gap between any two requests (>= 2 s)
#   - request_jitter_s     random extra gap so traffic isn't machine-regular
#   - catalog_page_size, max_catalog_pages
#   - max_rap_lookups_per_sweep   budget for stage 2 of the funnel
#   - rap_refresh_h        how often to refresh RAP/history for tracked items
#   - low_rap_recheck_h    how often to re-check items below min_rap (rarely)
#   - candidate_rap_max_age_h     RAP must be this fresh before alerting
#   - watchlist_file       optional extra asset IDs, one per line
#
# Expose everything as one frozen dataclass instance (CFG).
