# Quick Start Guide

Get started with ChipaPocketOptionData in 5 minutes!

## 1. Installation

```bash
pip install ChipaPocketOptionData
```

Or install from source:

```bash
git clone https://github.com/ChipaDevTeam/ChipaPocketOptionData.git
cd ChipaPocketOptionData
pip install -e .
```

## 2. Get Your Demo Account SSIDs

You need session IDs from PocketOption demo accounts. See [HOW_TO_GET_SSID.md](HOW_TO_GET_SSID.md) for detailed instructions.

Quick method:
1. Go to [PocketOption](https://pocketoption.com)
2. Create a demo account
3. Open browser DevTools (F12)
4. Go to Application → Cookies → `ssid`
5. Copy the value

Create 2-3 demo accounts for best results.

## 3. Basic Usage

Create a file `collect_data.py`:

```python
from ChipaPocketOptionData import subscribe_symbol_timed
from datetime import timedelta

# Your demo account SSIDs
ssids = [
    "your_ssid_1_here",
    "your_ssid_2_here",
    "your_ssid_3_here",
]

# Start collecting 5-second candles
collector = subscribe_symbol_timed(
    asset="EURUSD_otc",
    time_delta=timedelta(seconds=5),
    ssids=ssids,
    proxy_support=False
)

# Print incoming candles
try:
    for candle in collector:
        if 'error' in candle:
            print(f"Error: {candle['error']}")
            continue
        
        print(f"EURUSD_otc: {candle['close']}")
        
except KeyboardInterrupt:
    print("Stopping...")
finally:
    collector.stop()
```

Run it:

```bash
python collect_data.py
```

## 4. Using Environment Variables (Recommended)

Create a `.env` file:

```bash
POCKETOPTION_SSID_1=your_first_ssid
POCKETOPTION_SSID_2=your_second_ssid
POCKETOPTION_SSID_3=your_third_ssid
```

Update your script:

```python
import os
from dotenv import load_dotenv
from ChipaPocketOptionData import subscribe_symbol_timed

load_dotenv()

ssids = [
    os.getenv('POCKETOPTION_SSID_1'),
    os.getenv('POCKETOPTION_SSID_2'),
    os.getenv('POCKETOPTION_SSID_3'),
]

collector = subscribe_symbol_timed(
    asset="EURUSD_otc",
    time_delta=5,  # Can use int for seconds
    ssids=ssids
)

for candle in collector:
    if 'error' not in candle:
        print(f"Price: {candle['close']}")
```

Install python-dotenv:

```bash
pip install python-dotenv
```

## 5. Save Data to Database

```python
import sqlite3
from ChipaPocketOptionData import subscribe_symbol_timed

# Setup database
conn = sqlite3.connect('market_data.db')
cursor = conn.cursor()

cursor.execute("""
    CREATE TABLE IF NOT EXISTS candles (
        id INTEGER PRIMARY KEY,
        timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
        asset TEXT,
        close REAL,
        open REAL,
        high REAL,
        low REAL
    )
""")
conn.commit()

# Collect and save
ssids = ["ssid1", "ssid2", "ssid3"]

collector = subscribe_symbol_timed(
    asset="EURUSD_otc",
    time_delta=5,
    ssids=ssids
)

try:
    for candle in collector:
        if 'error' not in candle:
            cursor.execute("""
                INSERT INTO candles (asset, close, open, high, low)
                VALUES (?, ?, ?, ?, ?)
            """, (
                "EURUSD_otc",
                candle.get('close'),
                candle.get('open'),
                candle.get('high'),
                candle.get('low')
            ))
            conn.commit()
            print(f"✓ Saved: {candle['close']}")
            
except KeyboardInterrupt:
    pass
finally:
    collector.stop()
    conn.close()
```

## 6. Using Proxies

If you want to use proxies:

```python
from ChipaPocketOptionData import subscribe_symbol_timed, ProxyConfig

ssids = ["ssid1", "ssid2", "ssid3"]

proxies = [
    ProxyConfig(host="proxy1.com", port=8080, username="user1", password="pass1"),
    ProxyConfig(host="proxy2.com", port=8080, username="user2", password="pass2"),
    ProxyConfig(host="proxy3.com", port=8080, username="user3", password="pass3"),
]

collector = subscribe_symbol_timed(
    asset="EURUSD_otc",
    time_delta=5,
    ssids=ssids,
    proxies=proxies,
    proxy_support=True
)

for candle in collector:
    print(candle)
```

See [PROXY_SETUP.md](PROXY_SETUP.md) for detailed proxy configuration.

## 7. Multiple Assets

Collect from multiple assets simultaneously:

```python
import threading
from ChipaPocketOptionData import subscribe_symbol_timed

def collect_asset(asset, ssids):
    """Collect data for one asset."""
    collector = subscribe_symbol_timed(
        asset=asset,
        time_delta=5,
        ssids=ssids
    )
    
    for candle in collector:
        if 'error' not in candle:
            print(f"{asset}: {candle['close']}")

# Split SSIDs across assets
ssids = ["ssid1", "ssid2", "ssid3", "ssid4", "ssid5", "ssid6"]

threads = [
    threading.Thread(target=collect_asset, args=("EURUSD_otc", ssids[:2])),
    threading.Thread(target=collect_asset, args=("GBPUSD_otc", ssids[2:4])),
    threading.Thread(target=collect_asset, args=("USDJPY_otc", ssids[4:])),
]

for thread in threads:
    thread.start()

for thread in threads:
    thread.join()
```

## Next Steps

- Check out [examples/](../examples/) for more use cases
- Read [PROXY_SETUP.md](PROXY_SETUP.md) for proxy configuration
- See [HOW_TO_GET_SSID.md](HOW_TO_GET_SSID.md) for SSID extraction
- Read the full [README.md](../README.md) for API documentation

## Common Issues

### "Module not found" error

```bash
pip install BinaryOptionsToolsV2
```

### "Connection refused"

- Check your SSIDs are valid and not expired
- Try logging in again and getting fresh SSIDs

### Rate limiting

- Use more demo accounts
- Enable proxy support
- Add delays between requests

## Getting Help

- Check [examples/](../examples/)
- Open an issue on [GitHub](https://github.com/ChipaDevTeam/ChipaPocketOptionData/issues)
- Read the documentation

---

Happy data collecting! 🚀
