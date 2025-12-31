"""
Example: Collect data from multiple assets simultaneously.

This example shows how to collect data from multiple assets at the same time
by creating multiple collector instances.
"""

import threading
from ChipaPocketOptionData import subscribe_symbol_timed
from datetime import timedelta


def collect_asset_data(asset: str, ssids: list, results: dict):
    """Collect data for a single asset."""
    print(f"Starting collection for {asset}...")
    
    collector = subscribe_symbol_timed(
        asset=asset,
        time_delta=timedelta(seconds=5),
        ssids=ssids,
        proxy_support=False,
        log_level="INFO",
    )
    
    candles = []
    try:
        for candle in collector:
            if 'error' in candle:
                continue
            
            candles.append(candle)
            
            if len(candles) % 20 == 0:
                print(f"{asset}: Collected {len(candles)} candles")
            
            # Stop after 100 candles for this example
            if len(candles) >= 100:
                break
    
    except KeyboardInterrupt:
        pass
    finally:
        collector.stop()
        results[asset] = candles
        print(f"{asset}: Collection stopped with {len(candles)} candles")


def main():
    """Main function to collect data from multiple assets."""
    # Your demo account SSIDs
    # You can distribute SSIDs across different assets or reuse them
    ssids_pool = [
        "your_demo_ssid_1",
        "your_demo_ssid_2",
        "your_demo_ssid_3",
        "your_demo_ssid_4",
        "your_demo_ssid_5",
        "your_demo_ssid_6",
    ]
    
    # Assets to collect data from
    assets = [
        "EURUSD_otc",
        "GBPUSD_otc",
        "USDJPY_otc",
    ]
    
    # Distribute SSIDs across assets
    ssids_per_asset = len(ssids_pool) // len(assets)
    
    print(f"Collecting data from {len(assets)} assets...")
    print(f"Using {len(ssids_pool)} total demo accounts")
    print(f"Approximately {ssids_per_asset} accounts per asset\n")
    
    # Results storage
    results = {}
    
    # Create threads for each asset
    threads = []
    for i, asset in enumerate(assets):
        # Assign SSIDs to this asset
        start_idx = i * ssids_per_asset
        end_idx = start_idx + ssids_per_asset
        asset_ssids = ssids_pool[start_idx:end_idx]
        
        # Create and start thread
        thread = threading.Thread(
            target=collect_asset_data,
            args=(asset, asset_ssids, results)
        )
        thread.start()
        threads.append(thread)
    
    try:
        # Wait for all threads to complete
        for thread in threads:
            thread.join()
    
    except KeyboardInterrupt:
        print("\n\nStopping all collections...")
        # Threads will stop on their own when collectors stop
    
    # Print final results
    print("\n" + "="*50)
    print("FINAL RESULTS")
    print("="*50)
    for asset, candles in results.items():
        print(f"{asset}: {len(candles)} candles collected")
    
    total_candles = sum(len(candles) for candles in results.values())
    print(f"\nTotal candles collected: {total_candles}")


if __name__ == "__main__":
    main()
