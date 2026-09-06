"""
config.py
---------
This deployment runs ONE bot only (see BOT_NAME/TELEGRAM_NAME below) — it's
one of three independent, standalone projects meant to be deployed to three
separate Render.com accounts/services, each with its own repo.

Edit bots_config/symbols.json to add/remove symbols for THIS bot only.
"""

import os
import json
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent

# ---------------------------------------------------------------------------
# Identity of this specific bot deployment - EDIT PER BOT
# ---------------------------------------------------------------------------
BOT_ID = "BOT2"
BOT_NAME = "SECTOR LEADERS BOT"
TELEGRAM_DISPLAY_NAME = "@SectorLeaderAlertBot"

# ---------------------------------------------------------------------------
# Symbol universe - falls back to a tiny default set if the json file is
# somehow missing from the deploy, so the app boots and logs a loud warning
# instead of crashing. Fix by making sure bots_config/symbols.json is
# committed to THIS repo and pushed to THIS Render service.
# ---------------------------------------------------------------------------
_BUILT_IN_SYMBOLS = [
    "HDFCBANK.NS", "ICICIBANK.NS", "AXISBANK.NS", "KOTAKBANK.NS", "SBIN.NS",
    "INDUSINDBK.NS", "BANDHANBNK.NS", "BANKBARODA.NS", "CANBK.NS", "FEDERALBNK.NS",
    "IDFCFIRSTB.NS", "PNB.NS", "RBLBANK.NS", "YESBANK.NS", "UNIONBANK.NS",
    "BAJFINANCE.NS", "BAJAJFINSV.NS", "HDFCLIFE.NS", "SBILIFE.NS", "ICICIPRULI.NS",
    "ICICIGI.NS", "MUTHOOTFIN.NS", "CHOLAFIN.NS", "SRTRANSFIN.NS", "PFC.NS", "TCS.NS",
    "INFY.NS", "HCLTECH.NS", "WIPRO.NS", "TECHM.NS", "MPHASIS.NS", "LTTS.NS",
    "COFORGE.NS", "PERSISTENT.NS", "MINDTREE.NS", "HEXAWARE.NS", "KPITTECH.NS",
    "ZENSARTECH.NS", "BSOFT.NS", "CYIENT.NS", "LTI.NS", "OFSS.NS", "INTELLECT.NS",
    "SONATSOFT.NS", "SUNPHARMA.NS", "DRREDDY.NS", "CIPLA.NS", "DIVISLAB.NS", "LUPIN.NS",
    "AUROPHARMA.NS", "BIOCON.NS", "GLENMARK.NS", "TORNTPHARM.NS", "CADILAHC.NS",
    "APOLLOHOSP.NS", "FORTIS.NS", "MAXHEALTH.NS", "NARAYANA.NS", "ALKEM.NS",
    "HINDUNILVR.NS", "ITC.NS", "NESTLEIND.NS", "BRITANNIA.NS", "GODREJCP.NS", "DABUR.NS",
    "MARICO.NS", "TATACONSUM.NS", "RADICO.NS", "EMAMILTD.NS", "GILLETTE.NS", "COLGATE.NS",
    "JUBLFOOD.NS", "MCDOWELL-N.NS", "UNITEDSPIRITS.NS", "MARUTI.NS", "TATAMOTORS.NS",
    "M&M.NS", "EICHERMOT.NS", "BAJAJ-AUTO.NS", "TVSMOTOR.NS", "HEROMOTOCO.NS",
    "ASHOKLEY.NS", "ESCORTS.NS", "MRF.NS", "APOLLOTYRE.NS", "CEATLTD.NS", "BOSCHLTD.NS",
    "MOTHERSON.NS", "EXIDEIND.NS", "RELIANCE.NS", "ONGC.NS", "OIL.NS", "BPCL.NS",
    "IOCL.NS", "GAIL.NS", "ADANIGREEN.NS", "POWERGRID.NS", "NTPC.NS", "TATAPOWER.NS",
    "ADANIPOWER.NS", "GUJGAS.NS", "IGL.NS", "MGL.NS", "PETRONET.NS", "TATASTEEL.NS",
    "JSWSTEEL.NS", "HINDALCO.NS", "NATIONALUM.NS", "VEDL.NS", "COALINDIA.NS", "SAIL.NS",
    "NMDC.NS", "JINDALSTEL.NS", "HINDZINC.NS", "DLF.NS", "OBEROIRLTY.NS", "GODREJPROP.NS",
    "PHOENIXLTD.NS", "SOBHA.NS"
]

# bots_config/symbols.json is OPTIONAL - if present and valid, it overrides
# the built-in list above, so you can edit the symbol list later without
# touching code. If it's missing (e.g. not committed to git - this bit us
# twice already), the full built-in list above is used automatically, NOT
# a tiny placeholder - so a missing file can no longer silently shrink your
# monitored universe down to a handful of symbols.
_SYMBOLS_PATH = BASE_DIR / "bots_config" / "symbols.json"
SYMBOLS = _BUILT_IN_SYMBOLS
try:
    with open(_SYMBOLS_PATH) as f:
        _override = json.load(f)
    if isinstance(_override, list) and len(_override) > 0:
        SYMBOLS = _override
        print(f"[config] Loaded {len(SYMBOLS)} symbols from bots_config/symbols.json (override)")
    else:
        print(f"[config] bots_config/symbols.json was empty/invalid, using built-in list ({len(SYMBOLS)} symbols)")
except (FileNotFoundError, json.JSONDecodeError):
    print(f"[config] bots_config/symbols.json not found, using built-in list ({len(SYMBOLS)} symbols) - this is fine")

# ---------------------------------------------------------------------------
# Strict rule thresholds
# ---------------------------------------------------------------------------
RSI_LONG_MIN, RSI_LONG_MAX = 40, 65
RSI_SHORT_MIN, RSI_SHORT_MAX = 35, 60
ADX_MIN = 25
VWAP_MAX_DISTANCE_PCT = 2.0
CONFIDENCE_HIGH_PCT = 0.5
CONFIDENCE_MEDIUM_PCT = 1.5
VOLUME_LOOKBACK = 20
EMA_FAST, EMA_SLOW = 9, 21
RSI_PERIOD = 14
ADX_PERIOD = 14

SCORE_ALERT_THRESHOLD = 8
EARLY_SIGNAL_ENABLED = True
EARLY_SCORE_MIN = 6            # score 6-7/10 = building momentum, not yet confirmed (8+)
EARLY_COOLDOWN_HOURS = 1        # shorter than the confirmed 2h cooldown, so a developing
                                 # setup can re-notify sooner as it keeps building
COOLDOWN_HOURS = 2
CANDLE_INTERVAL = "FIVE_MINUTE"
SCAN_INTERVAL_MINUTES = 15

MARKET_OPEN = "09:15"
MARKET_CLOSE = "15:30"
MORNING_RESET_TIME = "09:10"
DAILY_SUMMARY_TIME = "15:45"
ERROR_SUMMARY_TIME = "16:00"
TIMEZONE = "Asia/Kolkata"

MAX_CONSECUTIVE_FAILS_BROKEN = 3
MAX_CONSECUTIVE_FAILS_DISABLE = 5

SQLITE_PATH = str(BASE_DIR / "data" / "alerts.db")

# ---------------------------------------------------------------------------
# Telegram - set these in Render's Environment tab, NEVER in this file
# ---------------------------------------------------------------------------
TELEGRAM_TOKEN = os.environ.get("TELEGRAM_TOKEN", "").strip()
TELEGRAM_CHAT_ID = os.environ.get("TELEGRAM_CHAT_ID", "").strip()

# ---------------------------------------------------------------------------
# Angel One SmartAPI credentials - set these in Render's Environment tab,
# NEVER in this file. If all 3 bots trade through the SAME Angel One
# account, be aware Angel One typically allows only one active login
# session per account at a time - logging in from bot #2 or #3 may
# invalidate bot #1's session. Ask Angel One support whether your account
# supports multiple concurrent API sessions before relying on 3 simultaneous
# logins, or consider generating a separate API key per bot from the same
# developer account (this does NOT guarantee independent sessions).
# ---------------------------------------------------------------------------
ANGEL_API_KEY = os.environ.get("ANGEL_API_KEY", "").strip()
ANGEL_CLIENT_CODE = os.environ.get("ANGEL_CLIENT_CODE", "").strip()
ANGEL_PIN = os.environ.get("ANGEL_PIN", "").strip()
ANGEL_TOTP_SECRET = os.environ.get("ANGEL_TOTP_SECRET", "").strip()

ANGEL_INSTRUMENT_MASTER_URL = (
    "https://margincalculator.angelone.in/OpenAPI_File/files/OpenAPIScripMaster.json"
)
INSTRUMENT_CACHE_PATH = str(BASE_DIR / "data" / "instrument_master.json")

DRY_RUN = os.environ.get("DRY_RUN", "false").lower() == "true"
PORT = int(os.environ.get("PORT", "10000"))


def validate_and_report():
    """
    Prints a loud, unmissable startup diagnostic to the logs (Render's Logs
    tab) so misconfigured env vars are visible immediately on boot, without
    needing to hit /status. Never prints actual secret values - only
    presence/length, which is enough to catch "empty", "whitespace-only",
    or "obviously truncated" mistakes.
    """
    print("=" * 60)
    print(f"[config] BOT: {BOT_NAME}")
    print(f"[config] DRY_RUN: {DRY_RUN}")
    checks = [
        ("TELEGRAM_TOKEN", TELEGRAM_TOKEN),
        ("TELEGRAM_CHAT_ID", TELEGRAM_CHAT_ID),
        ("ANGEL_API_KEY", ANGEL_API_KEY),
        ("ANGEL_CLIENT_CODE", ANGEL_CLIENT_CODE),
        ("ANGEL_PIN", ANGEL_PIN),
        ("ANGEL_TOTP_SECRET", ANGEL_TOTP_SECRET),
    ]
    any_missing = False
    for name, value in checks:
        if value:
            print(f"[config]   {name}: SET (length {len(value)})")
        else:
            print(f"[config]   {name}: *** MISSING OR EMPTY *** - set this in Render > Environment")
            any_missing = True
    if any_missing and not DRY_RUN:
        print("[config] WARNING: one or more required env vars are missing "
              "and DRY_RUN is false - real alerts/login will fail until fixed.")
    print("=" * 60)


validate_and_report()
