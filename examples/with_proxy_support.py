"""
Example using ChipaPocketOptionData with proxy support.

This example shows how to configure and use proxy servers with the data collector.
"""

from ChipaPocketOptionData import subscribe_symbol_timed, ProxyConfig
from datetime import timedelta


def main():
    """Main example with proxy configuration."""
    # Your demo account SSIDs
    ssids = [
        "your_demo_ssid_1",
        "your_demo_ssid_2",
        "your_demo_ssid_3",
        "your_demo_ssid_4",
    ]
    
    # Configure your proxy servers
    # Each process will use a different proxy (round-robin if more SSIDs than proxies)
    proxies = [
        ProxyConfig(
            host="proxy1.example.com",
            port=8080,
            username="user1",
            password="pass1",
            protocol="http"
        ),
        ProxyConfig(
            host="proxy2.example.com",
            port=8080,
            username="user2",
            password="pass2",
            protocol="http"
        ),
        ProxyConfig(
            host="proxy3.example.com",
            port=1080,
            protocol="socks5"
        ),
    ]
    
    print("Starting data collection with proxy support...")
    print(f"Using {len(ssids)} demo accounts with {len(proxies)} proxies")
    
    # Subscribe to 5-second candles with proxy support
    collector = subscribe_symbol_timed(
        asset="EURUSD_otc",
        time_delta=5,  # Can use int for seconds
        ssids=ssids,
        proxies=proxies,
        proxy_support=True,
        log_level="INFO",
        reconnect_on_error=True,
        error_retry_delay=5,
    )
    
    try:
        # Iterate over incoming candles
        candle_count = {}
        
        for candle in collector:
            if 'error' in candle:
                print(f"⚠️  Error from {candle['ssid']}: {candle['error']}")
                continue
            
            # Track candles per SSID
            ssid = candle['ssid']
            candle_count[ssid] = candle_count.get(ssid, 0) + 1
            
            proxy_info = f" via {candle['proxy']}" if candle['proxy'] else ""
            print(f"✓ Candle from {ssid}{proxy_info}: "
                  f"Close={candle.get('close'):.5f}")
            
            # Print statistics every 50 candles
            total = sum(candle_count.values())
            if total % 50 == 0:
                print(f"\n--- Statistics (Total: {total} candles) ---")
                for sid, count in candle_count.items():
                    print(f"  {sid}: {count} candles")
                print()
    
    except KeyboardInterrupt:
        print("\n\nStopping data collection...")
    finally:
        collector.stop()
        print("Data collection stopped.")
        
        if candle_count:
            print("\n--- Final Statistics ---")
            for ssid, count in candle_count.items():
                print(f"  {ssid}: {count} candles collected")


if __name__ == "__main__":
    main()
