# Proxy Setup Guide

This guide explains how to set up and use proxies with ChipaPocketOptionData.

## Why Use Proxies?

When collecting data from multiple demo accounts, PocketOption might:

1. **Rate limit** your IP address
2. **Block** multiple connections from the same IP
3. **Throttle** your data collection speed

Using proxies allows you to:

- Distribute connections across multiple IP addresses
- Avoid rate limiting and blocking
- Maximize data collection throughput
- Scale to more demo accounts

## Proxy Types Supported

ChipaPocketOptionData supports multiple proxy protocols:

### HTTP/HTTPS Proxies

```python
from ChipaPocketOptionData import ProxyConfig

proxy = ProxyConfig(
    host="proxy.example.com",
    port=8080,
    username="user",      # Optional
    password="pass",      # Optional
    protocol="http"       # Default
)
```

### SOCKS5 Proxies

```python
proxy = ProxyConfig(
    host="socks.example.com",
    port=1080,
    username="user",      # Optional
    password="pass",      # Optional
    protocol="socks5"
)
```

## Getting Proxies

### Free Proxy Services

⚠️ **Warning**: Free proxies are often unreliable and slow. Use for testing only.

- [Free Proxy List](https://www.freeproxylists.net/)
- [ProxyScrape](https://proxyscrape.com/free-proxy-list)
- [GeoNode](https://geonode.com/free-proxy-list)

### Paid Proxy Services (Recommended)

For production use, consider paid proxy services:

1. **Residential Proxies**
   - [Bright Data](https://brightdata.com/)
   - [Smartproxy](https://smartproxy.com/)
   - [Oxylabs](https://oxylabs.io/)
   - Best for avoiding detection
   - Higher cost but more reliable

2. **Datacenter Proxies**
   - [IPRoyal](https://iproyal.com/)
   - [ProxyRack](https://www.proxyrack.com/)
   - [Storm Proxies](https://stormproxies.com/)
   - Cheaper than residential
   - Good for high-volume data collection

3. **Rotating Proxies**
   - Automatically rotate IP addresses
   - Best for avoiding rate limits
   - Most proxy services offer this feature

## Configuration

### Basic Setup (Single Proxy)

```python
from ChipaPocketOptionData import subscribe_symbol_timed, ProxyConfig

ssids = ["ssid1", "ssid2", "ssid3"]

# All accounts will use the same proxy
proxy = ProxyConfig(
    host="proxy.example.com",
    port=8080,
    username="user",
    password="pass"
)

collector = subscribe_symbol_timed(
    asset="EURUSD_otc",
    time_delta=5,
    ssids=ssids,
    proxies=[proxy],
    proxy_support=True
)
```

### Multiple Proxies (Recommended)

```python
from ChipaPocketOptionData import subscribe_symbol_timed, ProxyConfig

ssids = ["ssid1", "ssid2", "ssid3", "ssid4"]

# Each SSID gets its own proxy (round-robin)
proxies = [
    ProxyConfig(host="proxy1.example.com", port=8080),
    ProxyConfig(host="proxy2.example.com", port=8080),
    ProxyConfig(host="proxy3.example.com", port=8080),
]

collector = subscribe_symbol_timed(
    asset="EURUSD_otc",
    time_delta=5,
    ssids=ssids,
    proxies=proxies,
    proxy_support=True
)

# Distribution:
# - ssid1 -> proxy1
# - ssid2 -> proxy2
# - ssid3 -> proxy3
# - ssid4 -> proxy1 (round-robin)
```

### Using Environment Variables

```python
import os
from ChipaPocketOptionData import ProxyConfig

# Store proxy credentials securely
proxies = [
    ProxyConfig(
        host=os.getenv("PROXY_HOST_1"),
        port=int(os.getenv("PROXY_PORT_1")),
        username=os.getenv("PROXY_USER_1"),
        password=os.getenv("PROXY_PASS_1")
    ),
    ProxyConfig(
        host=os.getenv("PROXY_HOST_2"),
        port=int(os.getenv("PROXY_PORT_2")),
        username=os.getenv("PROXY_USER_2"),
        password=os.getenv("PROXY_PASS_2")
    ),
]
```

Create a `.env` file:

```bash
# .env (add to .gitignore!)
PROXY_HOST_1=proxy1.example.com
PROXY_PORT_1=8080
PROXY_USER_1=user1
PROXY_PASS_1=pass1

PROXY_HOST_2=proxy2.example.com
PROXY_PORT_2=8080
PROXY_USER_2=user2
PROXY_PASS_2=pass2
```

## Advanced Configuration

### Rotating Proxy Service

Many proxy services provide a single endpoint that rotates IPs:

```python
# Example: Bright Data rotating proxy
proxy = ProxyConfig(
    host="brd.superproxy.io",
    port=22225,
    username="customer-USER-cc-us",
    password="PASSWORD",
    protocol="http"
)

# Single proxy config, but IPs rotate automatically
proxies = [proxy] * len(ssids)  # Reuse for all SSIDs
```

### Proxy with Authentication

```python
proxy = ProxyConfig(
    host="proxy.example.com",
    port=8080,
    username="myuser",
    password="mypass",
    protocol="http"
)

# Converts to: http://myuser:mypass@proxy.example.com:8080
print(proxy.to_url())
```

### Testing Proxy Connection

```python
import asyncio
from ChipaPocketOptionData import subscribe_symbol_timed, ProxyConfig

async def test_proxy():
    proxy = ProxyConfig(
        host="proxy.example.com",
        port=8080,
        username="user",
        password="pass"
    )
    
    try:
        collector = subscribe_symbol_timed(
            asset="EURUSD_otc",
            time_delta=5,
            ssids=["your_ssid"],
            proxies=[proxy],
            proxy_support=True
        )
        
        # Try to get one candle
        for i, candle in enumerate(collector):
            if 'error' in candle:
                print(f"❌ Proxy failed: {candle['error']}")
                return False
            else:
                print(f"✅ Proxy working: {candle}")
                collector.stop()
                return True
            
            if i >= 1:  # Stop after first candle
                break
    except Exception as e:
        print(f"❌ Proxy error: {e}")
        return False

asyncio.run(test_proxy())
```

## Best Practices

### 1. Match Proxies to SSIDs

```python
# Good: Equal number of proxies and SSIDs
ssids = ["ssid1", "ssid2", "ssid3"]
proxies = [proxy1, proxy2, proxy3]
```

### 2. Use Geographic Diversity

```python
proxies = [
    ProxyConfig(host="us-proxy.com", port=8080),   # US
    ProxyConfig(host="eu-proxy.com", port=8080),   # Europe
    ProxyConfig(host="asia-proxy.com", port=8080), # Asia
]
```

### 3. Monitor Proxy Health

```python
from collections import defaultdict

error_count = defaultdict(int)

for candle in collector:
    if 'error' in candle:
        proxy = candle.get('proxy')
        error_count[proxy] += 1
        
        if error_count[proxy] > 10:
            print(f"⚠️ Proxy {proxy} has too many errors!")
```

### 4. Implement Fallback

```python
# Primary proxies
primary_proxies = [proxy1, proxy2, proxy3]

# Backup proxies
backup_proxies = [proxy4, proxy5, proxy6]

# Try primary first, fallback to backup if needed
try:
    collector = subscribe_symbol_timed(
        asset="EURUSD_otc",
        time_delta=5,
        ssids=ssids,
        proxies=primary_proxies,
        proxy_support=True
    )
except Exception:
    collector = subscribe_symbol_timed(
        asset="EURUSD_otc",
        time_delta=5,
        ssids=ssids,
        proxies=backup_proxies,
        proxy_support=True
    )
```

## Troubleshooting

### Connection Timeouts

```python
collector = subscribe_symbol_timed(
    asset="EURUSD_otc",
    time_delta=5,
    ssids=ssids,
    proxies=proxies,
    proxy_support=True,
    reconnect_on_error=True,      # Enable auto-reconnect
    error_retry_delay=10          # Wait 10s before retry
)
```

### Proxy Authentication Failed

1. Double-check username/password
2. Verify proxy service is active
3. Check if IP whitelist is required
4. Test proxy with curl:

```bash
curl -x http://user:pass@proxy.com:8080 https://api.ipify.org
```

### Slow Proxy Performance

1. Try different geographic regions
2. Use datacenter proxies instead of residential
3. Reduce number of concurrent connections
4. Enable connection pooling (if supported)

### Proxy Rotation Not Working

Some services require specific parameters:

```python
# Example: Add session ID for sticky sessions
proxy = ProxyConfig(
    host="proxy.com",
    port=8080,
    username=f"user-session-{session_id}",
    password="pass"
)
```

## Cost Optimization

### Strategy 1: Mix Free and Paid Proxies

```python
# Use free proxies for testing, paid for production
if ENVIRONMENT == "development":
    proxies = free_proxies
else:
    proxies = paid_proxies
```

### Strategy 2: Proxy Pooling

```python
# Rotate through a pool of proxies
from itertools import cycle

proxy_pool = cycle([proxy1, proxy2, proxy3, proxy4, proxy5])

for ssid in ssids:
    proxy = next(proxy_pool)
    # Use proxy for this SSID
```

### Strategy 3: On-Demand Proxies

```python
# Only enable proxies when needed
if high_traffic_period():
    proxy_support = True
else:
    proxy_support = False
```

## Example: Complete Setup

```python
from ChipaPocketOptionData import subscribe_symbol_timed, ProxyConfig
import os
from dotenv import load_dotenv

load_dotenv()

# Load SSIDs
ssids = [
    os.getenv("SSID_1"),
    os.getenv("SSID_2"),
    os.getenv("SSID_3"),
]

# Configure proxies
proxies = [
    ProxyConfig(
        host=os.getenv("PROXY_HOST_1"),
        port=int(os.getenv("PROXY_PORT_1")),
        username=os.getenv("PROXY_USER_1"),
        password=os.getenv("PROXY_PASS_1"),
        protocol="http"
    ),
    ProxyConfig(
        host=os.getenv("PROXY_HOST_2"),
        port=int(os.getenv("PROXY_PORT_2")),
        username=os.getenv("PROXY_USER_2"),
        password=os.getenv("PROXY_PASS_2"),
        protocol="http"
    ),
]

# Start collector
collector = subscribe_symbol_timed(
    asset="EURUSD_otc",
    time_delta=5,
    ssids=ssids,
    proxies=proxies,
    proxy_support=True,
    reconnect_on_error=True,
    error_retry_delay=5,
    log_level="INFO",
    log_path="./logs"
)

# Collect data
try:
    for candle in collector:
        if 'error' in candle:
            print(f"Error: {candle}")
        else:
            print(f"Candle: {candle}")
except KeyboardInterrupt:
    print("Stopping...")
finally:
    collector.stop()
```

---

Need help? Check the [examples/](../examples/) or open an issue!
