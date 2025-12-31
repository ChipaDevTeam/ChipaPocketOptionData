"""
Basic usage examples for ChipaPocketOptionData.

This example demonstrates how to collect real-time data from PocketOption
using multiple demo accounts.
"""

from ChipaPocketOptionData import subscribe_symbol_timed
from datetime import timedelta


def main():
    """Main example function."""
    # Your demo account SSIDs
    # Create multiple demo accounts and get their session IDs
    ssids = [
        "your_demo_ssid_1",
        "your_demo_ssid_2",
        "your_demo_ssid_3",
    ]
    
    print("Starting data collection for EURUSD_otc...")
    print(f"Using {len(ssids)} demo accounts")
    
    # Subscribe to 5-second candles
    collector = subscribe_symbol_timed(
        asset="EURUSD_otc",
        time_delta=timedelta(seconds=5),
        ssids=ssids,
        proxy_support=False,  # Set to True if using proxies
        log_level="INFO",
    )
    
    try:
        # Iterate over incoming candles
        for i, candle in enumerate(collector):
            if 'error' in candle:
                print(f"Error from {candle['ssid']}: {candle['error']}")
                continue
            
            print(f"Candle #{i+1} from {candle['ssid']}: "
                  f"Open={candle.get('open')}, "
                  f"Close={candle.get('close')}, "
                  f"High={candle.get('high')}, "
                  f"Low={candle.get('low')}")
            
            # Stop after 100 candles for this example
            if i >= 100:
                break
    
    except KeyboardInterrupt:
        print("\nStopping data collection...")
    finally:
        collector.stop()
        print("Data collection stopped.")


if __name__ == "__main__":
    main()
