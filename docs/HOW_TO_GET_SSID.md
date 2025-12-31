# How to Get Your Demo Account SSIDs

To use ChipaPocketOptionData, you need session IDs (SSIDs) from PocketOption demo accounts. Here's how to get them:

## Method 1: Browser DevTools (Recommended)

### Step 1: Create Demo Accounts

1. Go to [PocketOption](https://pocketoption.com)
2. Create multiple demo accounts (you can use temporary emails)
3. For each account, note down the login credentials

### Step 2: Extract SSID from Browser

1. Log in to your PocketOption demo account
2. Open Browser DevTools:
   - **Chrome/Edge**: Press `F12` or `Ctrl+Shift+I` (Windows) / `Cmd+Option+I` (Mac)
   - **Firefox**: Press `F12` or `Ctrl+Shift+I` (Windows) / `Cmd+Option+I` (Mac)

3. Go to the **Application** tab (Chrome/Edge) or **Storage** tab (Firefox)

4. In the left sidebar, expand **Cookies** and click on `https://pocketoption.com`

5. Look for a cookie named `ssid` or similar
   - The value of this cookie is your SSID
   - It should be a long string of characters

6. Copy this SSID and save it securely

### Step 3: Repeat for All Accounts

Repeat steps 1-2 for each demo account you want to use. You should have multiple SSIDs like:

```python
ssids = [
    "abc123def456ghi789jkl012mno345pqr678stu901vwx234yz",
    "bcd234efg567hij890klm123nop456qrs789tuv012wxy345za",
    "cde345fgh678ijk901lmn234opq567rst890uvw123xyz456ab",
]
```

## Method 2: Network Inspector

### Step 1: Open Network Tab

1. Open Browser DevTools (`F12`)
2. Go to the **Network** tab
3. Log in to your PocketOption demo account

### Step 2: Find WebSocket Connection

1. Look for WebSocket connections in the Network tab
2. Filter by **WS** (WebSocket) if available
3. Click on the WebSocket connection to PocketOption

### Step 3: Inspect Headers

1. In the **Headers** tab, look for:
   - Request Headers
   - Cookie header
2. Find the `ssid` value in the cookies

## Method 3: Using a Script (Advanced)

You can automate the SSID extraction using a script:

```python
import asyncio
from BinaryOptionsToolsV2.pocketoption import PocketOptionAsync

async def verify_ssid(ssid: str) -> bool:
    """Verify if an SSID is valid."""
    try:
        api = PocketOptionAsync(ssid)
        await asyncio.sleep(5)
        balance = await api.balance()
        print(f"✓ SSID valid - Balance: ${balance}")
        return True
    except Exception as e:
        print(f"✗ SSID invalid - Error: {e}")
        return False

# Test your SSIDs
ssids_to_test = [
    "your_ssid_1_here",
    "your_ssid_2_here",
]

async def main():
    for ssid in ssids_to_test:
        print(f"\nTesting SSID: {ssid[:20]}...")
        await verify_ssid(ssid)

if __name__ == "__main__":
    asyncio.run(main())
```

## Important Notes

### SSID Validity

- SSIDs typically expire after some time (session timeout)
- You may need to re-login and get new SSIDs periodically
- Keep your SSIDs secure - they provide access to your accounts

### Security Best Practices

1. **Never share your SSIDs publicly**
2. **Use environment variables** to store SSIDs in your code:

```python
import os
from dotenv import load_dotenv

load_dotenv()

ssids = [
    os.getenv('POCKETOPTION_SSID_1'),
    os.getenv('POCKETOPTION_SSID_2'),
    os.getenv('POCKETOPTION_SSID_3'),
]
```

3. Create a `.env` file:

```bash
# .env file (add to .gitignore!)
POCKETOPTION_SSID_1=abc123def456ghi789jkl012mno345pqr678stu901vwx234yz
POCKETOPTION_SSID_2=bcd234efg567hij890klm123nop456qrs789tuv012wxy345za
POCKETOPTION_SSID_3=cde345fgh678ijk901lmn234opq567rst890uvw123xyz456ab
```

### Using Multiple Demo Accounts

1. Create 3-5 demo accounts for optimal data collection
2. Each account can collect data independently
3. More accounts = more data throughput
4. Consider using proxies to avoid rate limiting

## Troubleshooting

### SSID Not Working

If your SSID stops working:

1. Log out and log back in to PocketOption
2. Extract a new SSID using the methods above
3. Update your configuration

### Getting Blocked

If you're getting blocked or rate-limited:

1. Use fewer concurrent connections
2. Enable proxy support
3. Add delays between requests
4. Use different proxies for different accounts

### Demo Account Limitations

- Demo accounts have virtual money only
- Some features might be limited compared to real accounts
- Demo accounts may expire if not used regularly

## Quick Setup Script

Save this as `get_ssids.py`:

```python
"""
Interactive script to help collect and verify SSIDs.
"""

import asyncio
from BinaryOptionsToolsV2.pocketoption import PocketOptionAsync

async def verify_ssid(ssid: str):
    """Verify SSID and get account info."""
    try:
        api = PocketOptionAsync(ssid)
        await asyncio.sleep(5)
        balance = await api.balance()
        return True, balance
    except Exception as e:
        return False, str(e)

async def main():
    print("PocketOption SSID Collection Tool")
    print("=" * 50)
    print()
    
    ssids = []
    
    while True:
        ssid = input("\nEnter SSID (or 'done' to finish): ").strip()
        
        if ssid.lower() == 'done':
            break
        
        if not ssid:
            print("Empty SSID, skipping...")
            continue
        
        print(f"Verifying SSID: {ssid[:20]}...")
        valid, result = await verify_ssid(ssid)
        
        if valid:
            print(f"✓ Valid SSID - Balance: ${result}")
            ssids.append(ssid)
        else:
            print(f"✗ Invalid SSID - Error: {result}")
            retry = input("Try this SSID anyway? (y/n): ")
            if retry.lower() == 'y':
                ssids.append(ssid)
    
    if ssids:
        print("\n" + "=" * 50)
        print("Valid SSIDs collected:")
        print("=" * 50)
        print("\nssids = [")
        for ssid in ssids:
            print(f'    "{ssid}",')
        print("]")
        print("\nCopy this into your code!")
    else:
        print("\nNo SSIDs collected.")

if __name__ == "__main__":
    asyncio.run(main())
```

Run it with:

```bash
python get_ssids.py
```

---

Need help? Open an issue on [GitHub](https://github.com/ChipaDevTeam/ChipaPocketOptionData/issues)!
