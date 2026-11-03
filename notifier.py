# notifier.py - Discord alerts (TODO)
#
# Posts a colour-coded embed via the Discord REST API using a bot token (no gateway).
#   # POST https://discord.com/api/v10/channels/{channel_id}/messages
#   # header: Authorization: Bot {token}
#
# build_embed(item, assessment, tier, colour, net_score)
#   # title:  "{tier} deal: {item name}"
#   # colour: the tier colour from the neural net grade
#   # fields:
#   #   current price, RAP, deal% off
#   #   rating "P/10 - label"
#   #   threshold maths "base% x factor = threshold%"
#   #   deal grade "tier (score/100)"
#   #   last 5 sales: slope %/sale, avg drop % vs prior RAP
#   #   long-term: MACD %, RSI, daily volatility %, sales/day, seasonal tilt %
#   #   link to the catalog page
#   # footer: "Alert only - verify before buying. Not financial advice."
#
# send_embed(embed, dry_run)
#   # dry_run -> print the JSON instead of posting
#   # on 429: sleep(retry_after + 0.5) and retry, up to 3 times
