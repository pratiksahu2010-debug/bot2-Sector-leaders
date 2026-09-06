# SECTOR LEADERS BOT

Standalone deployment - runs independently on its own Render.com account/service,
own repo, own SQLite database. Shares NO state with the other two bots.

## 1. Create this bot on Telegram

Message **@BotFather**, `/newbot`, save the token. This becomes `TELEGRAM_TOKEN`.
Message your new bot once, then hit
`https://api.telegram.org/bot<TOKEN>/getUpdates` to find your `chat_id`
(`TELEGRAM_CHAT_ID`).

## 2. Angel One SmartAPI credentials

Same account credentials as your other bots if you're using one trading
account for all three: `ANGEL_API_KEY`, `ANGEL_CLIENT_CODE`, `ANGEL_PIN`,
`ANGEL_TOTP_SECRET`.

⚠️ **Important if you run all 3 bots simultaneously on the same Angel One
account:** most brokers (Angel One included, historically) only allow ONE
active login session per trading account at a time. Logging in from bot #2
or #3 may silently invalidate bot #1's session, causing it to stop getting
real data without an obvious error. Before relying on all 3 running
concurrently, confirm with Angel One support whether your account/API plan
supports multiple simultaneous sessions. If not, you may need to either:
(a) stagger which bot is actively logged in, or (b) use separate Angel One
trading accounts per bot (not just separate API keys on the same account).

## 3. Set environment variables on Render

Dashboard → this service → **Environment**:

```
DRY_RUN=false
TELEGRAM_TOKEN=...
TELEGRAM_CHAT_ID=...
ANGEL_API_KEY=...
ANGEL_CLIENT_CODE=...
ANGEL_PIN=...
ANGEL_TOTP_SECRET=...
```

Set `DRY_RUN=true` first to test the whole pipeline against synthetic data
with no Angel One connection needed.

## 4. Deploy

Push this folder as the root of its own GitHub repo. In Render:
**New → Blueprint** (reads `render.yaml`, service name pre-set to
`sector-leaders-alert-bot`) or **New → Web Service** manually, pointing
Build Command to `pip install -r requirements.txt` and Start Command to
`gunicorn main:app --bind 0.0.0.0:$PORT --workers 1 --threads 4 --timeout 120`.

Also set `PYTHON_VERSION=3.12.7` in Environment if deploying manually
(not via Blueprint) - see `runtime.txt`.

## 5. Verify it's working

- `https://<your-service>.onrender.com/health` - confirms the service is up
  and shows the symbol count
- `https://<your-service>.onrender.com/telegram_test` - sends a plain test
  message, confirms Telegram wiring independent of trading logic
- `https://<your-service>.onrender.com/status` - full diagnostic: Angel One
  login state, instrument tokens resolved, active symbols, recent errors
- `https://<your-service>.onrender.com/trigger?force=true` - runs a scan
  immediately, ignoring market hours, for testing any time of day

## Editing the symbol list

Edit `bots_config/symbols.json` (a flat JSON array of tickers like
`"RELIANCE.NS"`), commit, push - no code changes needed.

## Scoring rules

VWAP is a hard gate - no VWAP or price >2% from VWAP means no alert,
regardless of score. Everything else scores out of 10 points (RSI range,
ADX>25, EMA9/21 alignment, last-2-candles direction, volume vs 20-avg,
VWAP tightness, EMA9 momentum, ADX strength). Alerts fire only at 8/10+.
See `scoring.py` to adjust weights or thresholds.
