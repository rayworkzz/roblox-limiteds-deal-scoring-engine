# main.py - entry point and scan loop (TODO)
#
# Usage (planned):
#   python main.py                    run forever (VPS)
#   python main.py --once --dry-run   one sweep, print embeds instead of posting
#
# Each sweep is a three-stage funnel to minimise API calls:
#   1. catalog scan: cheap, ~60 items per request -> store lowest listing prices
#   2. RAP refresh:  resale data for a limited budget of items (store.rap_due)
#   3. candidates:   only items that already look like a deal
#        # pre-filter = base_deal_pct * 0.7   (smallest threshold the model can produce,
#        #                                     since factor >= ~0.74)
#        # refresh RAP if older than candidate_rap_max_age_h
#        # assess -> skip if deal% < threshold
#        # skip if alerted within alert_cooldown_h
#        # re-check the live lowest price, assess again
#        # score with DealNet -> tier -> send embed -> record alert
#
# Run loop:
#   # pause = scan_interval_min * 60 + random(-60, 60) - time the sweep took   (min 60 s)
#   # on RateLimited: sleep 30 minutes
#   # handle SIGINT / SIGTERM for clean shutdown (systemd)
#   # rotating log file
