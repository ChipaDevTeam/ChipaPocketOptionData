"""
ChipaPocketOptionData - Multi-process data collection for PocketOption

A library for collecting high-volume PocketOption market data using multiple
demo accounts with proxy support via multiprocessing.
"""

from .multiprocessing_data import (
    subscribe_symbol,
    subscribe_symbol_timed,
    subscribe_symbol_chunked,
    get_candles,
    DataCollectorConfig,
)

__version__ = "1.0.0"
__all__ = [
    "subscribe_symbol",
    "subscribe_symbol_timed", 
    "subscribe_symbol_chunked",
    "get_candles",
    "DataCollectorConfig",
]
