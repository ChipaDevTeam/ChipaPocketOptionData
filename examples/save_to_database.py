"""
Example: Save collected data to a database.

This example shows how to collect data and store it in a database
for later analysis.
"""

import sqlite3
from datetime import datetime
from ChipaPocketOptionData import subscribe_symbol_timed


def setup_database(db_path: str = "pocketoption_data.db"):
    """Create the database schema."""
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS candles (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
            ssid TEXT NOT NULL,
            proxy TEXT,
            asset TEXT NOT NULL,
            open REAL,
            close REAL,
            high REAL,
            low REAL,
            volume REAL,
            time_frame INTEGER,
            raw_data TEXT
        )
    """)
    
    cursor.execute("""
        CREATE INDEX IF NOT EXISTS idx_timestamp 
        ON candles(timestamp)
    """)
    
    cursor.execute("""
        CREATE INDEX IF NOT EXISTS idx_asset 
        ON candles(asset)
    """)
    
    conn.commit()
    return conn


def save_candle(conn: sqlite3.Connection, asset: str, candle: dict):
    """Save a candle to the database."""
    cursor = conn.cursor()
    
    cursor.execute("""
        INSERT INTO candles (
            ssid, proxy, asset, open, close, high, low, 
            volume, time_frame, raw_data
        ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    """, (
        candle.get('ssid'),
        candle.get('proxy'),
        asset,
        candle.get('open'),
        candle.get('close'),
        candle.get('high'),
        candle.get('low'),
        candle.get('volume'),
        candle.get('time_frame'),
        str(candle)  # Store raw data as JSON string
    ))
    
    conn.commit()


def main():
    """Main function to collect and save data."""
    # Setup database
    print("Setting up database...")
    db_conn = setup_database()
    
    # Configure data collection
    ssids = [
        "your_demo_ssid_1",
        "your_demo_ssid_2",
        "your_demo_ssid_3",
    ]
    
    asset = "EURUSD_otc"
    
    print(f"Starting data collection for {asset}...")
    print(f"Using {len(ssids)} demo accounts")
    print("Data will be saved to: pocketoption_data.db")
    
    collector = subscribe_symbol_timed(
        asset=asset,
        time_delta=5,  # 5-second candles
        ssids=ssids,
        proxy_support=False,
        log_level="INFO",
    )
    
    candle_count = 0
    error_count = 0
    
    try:
        for candle in collector:
            if 'error' in candle:
                error_count += 1
                print(f"⚠️  Error: {candle['error']}")
                continue
            
            # Save to database
            save_candle(db_conn, asset, candle)
            candle_count += 1
            
            if candle_count % 10 == 0:
                print(f"✓ Saved {candle_count} candles "
                      f"({error_count} errors)")
    
    except KeyboardInterrupt:
        print("\n\nStopping data collection...")
    finally:
        collector.stop()
        db_conn.close()
        print(f"\nData collection stopped.")
        print(f"Total candles saved: {candle_count}")
        print(f"Total errors: {error_count}")


if __name__ == "__main__":
    main()
