# Project Summary: ChipaPocketOptionData

## Overview

**ChipaPocketOptionData** is a Python library that enables high-volume market data collection from PocketOption using multiple demo accounts with optional proxy support via multiprocessing.

## Core Concept

The library addresses a common challenge in collecting market data from PocketOption:
- Individual connections are rate-limited
- Single accounts can't provide high-throughput data collection
- IP-based restrictions limit scaling

**Solution**: Use multiple demo accounts simultaneously, each optionally with its own proxy server, coordinated through multiprocessing.

## Architecture

```
┌─────────────────────────────────────┐
│    Main Process                     │
│    - Spawns workers                 │
│    - Aggregates data                │
│    - Manages lifecycle              │
└────────┬────────────────────────────┘
         │
    ┌────┴────┬─────────┬──────────┐
    ▼         ▼         ▼          ▼
┌────────┐┌────────┐┌────────┐┌────────┐
│Worker 1││Worker 2││Worker 3││Worker N│
│SSID 1  ││SSID 2  ││SSID 3  ││SSID N  │
│Proxy 1 ││Proxy 2 ││Proxy 3 ││Proxy N │
│        ││        ││        ││        │
│BO2 API ││BO2 API ││BO2 API ││BO2 API │
└────┬───┘└────┬───┘└────┬───┘└────┬───┘
     └─────────┴─────────┴─────────┘
                  │
                  ▼
          ┌──────────────┐
          │ Shared Queue │
          └──────────────┘
```

## Key Features

### 1. Multi-Processing
- Each SSID runs in its own process
- True parallel execution
- No GIL limitations
- Independent failure isolation

### 2. Proxy Support
- HTTP/HTTPS proxies
- SOCKS5 proxies
- Authentication support
- Round-robin assignment

### 3. Data Collection Methods
- **subscribe_symbol()**: Real-time 1-second candles
- **subscribe_symbol_timed()**: Time-based aggregation
- **subscribe_symbol_chunked()**: Count-based aggregation
- **get_candles()**: Historical data

### 4. Fault Tolerance
- Automatic reconnection
- Error tracking and reporting
- Graceful degradation
- Process monitoring

### 5. Easy API
```python
from ChipaPocketOptionData import subscribe_symbol_timed

collector = subscribe_symbol_timed(
    "EURUSD_otc", 
    5, 
    ssids=["ssid1", "ssid2"], 
    proxy_support=True
)

for candle in collector:
    print(candle)
```

## Use Cases

### 1. High-Frequency Data Collection
Collect market data at high rates by distributing across multiple accounts.

### 2. Historical Data Backup
Use multiple accounts to rapidly download historical candle data.

### 3. Multi-Asset Monitoring
Monitor multiple assets simultaneously with dedicated processes.

### 4. Research and Analysis
Gather large datasets for backtesting and strategy development.

### 5. Real-Time Trading Systems
Feed live data to trading algorithms with high reliability.

## Technical Stack

- **Python 3.8+**: Core language
- **multiprocessing**: Process management
- **asyncio**: Async I/O operations (via BinaryOptionsToolsV2)
- **BinaryOptionsToolsV2**: PocketOption API wrapper
- **queue**: Thread-safe data sharing

## Installation

```bash
pip install ChipaPocketOptionData
```

Or from source:
```bash
git clone https://github.com/ChipaDevTeam/ChipaPocketOptionData.git
cd ChipaPocketOptionData
./install.sh
```

## Quick Example

```python
from ChipaPocketOptionData import subscribe_symbol_timed, ProxyConfig

# Demo account SSIDs
ssids = ["demo_ssid_1", "demo_ssid_2", "demo_ssid_3"]

# Optional: Configure proxies
proxies = [
    ProxyConfig(host="proxy1.com", port=8080),
    ProxyConfig(host="proxy2.com", port=8080),
]

# Start collecting
collector = subscribe_symbol_timed(
    asset="EURUSD_otc",
    time_delta=5,  # 5-second candles
    ssids=ssids,
    proxies=proxies,
    proxy_support=True
)

# Process data
for candle in collector:
    if 'error' not in candle:
        print(f"Price: {candle['close']}")
```

## Project Structure

```
ChipaPocketOptionData/
├── ChipaPocketOptionData/          # Main package
│   ├── __init__.py                 # Public API
│   └── multiprocessing_data.py     # Core implementation
├── examples/                       # Usage examples
│   ├── basic_usage.py
│   ├── with_proxy_support.py
│   ├── save_to_database.py
│   └── multiple_assets.py
├── docs/                          # Documentation
│   ├── QUICK_START.md
│   ├── HOW_TO_GET_SSID.md
│   └── PROXY_SETUP.md
├── tests/                         # Test suite
│   └── test_basic.py
├── setup.py                       # Installation script
├── pyproject.toml                 # Modern Python packaging
├── requirements.txt               # Dependencies
├── README.md                      # Main documentation
├── CHANGELOG.md                   # Version history
├── CONTRIBUTING.md                # Contribution guide
└── LICENSE                        # MIT License
```

## Configuration Options

### DataCollectorConfig
- `ssids`: List of session IDs
- `proxies`: List of proxy configurations
- `proxy_support`: Enable/disable proxies
- `max_workers`: Max concurrent processes
- `reconnect_on_error`: Auto-reconnect on failure
- `error_retry_delay`: Retry delay in seconds
- `log_level`: Logging verbosity
- `log_path`: Log directory path

### ProxyConfig
- `host`: Proxy server hostname
- `port`: Proxy server port
- `username`: Optional authentication
- `password`: Optional authentication
- `protocol`: http, https, or socks5

## Documentation

- **README.md**: Main documentation with API reference
- **QUICK_START.md**: 5-minute getting started guide
- **HOW_TO_GET_SSID.md**: Extract SSIDs from PocketOption
- **PROXY_SETUP.md**: Comprehensive proxy configuration guide
- **Examples**: 4 working examples for common scenarios

## Testing

```bash
# Run basic tests
python tests/test_basic.py

# With your own SSIDs (interactive)
python tests/test_basic.py
# Follow prompts to test with real SSIDs
```

## Performance Characteristics

### Throughput
- **Single SSID**: ~1 candle/second
- **Multiple SSIDs**: Linear scaling (3 SSIDs = ~3 candles/second)
- **With proxies**: Similar performance, better reliability

### Memory Usage
- **Base**: ~50MB per process
- **Per SSID**: +20-30MB
- **Queue size**: Configurable (default 10,000 items)

### CPU Usage
- **Light**: <5% per process during normal operation
- **Scalability**: Tested with up to 10 concurrent processes

## Future Enhancements

### Planned Features
- Async iterator support
- Built-in data validation
- Compression and deduplication
- Cloud storage integration
- Performance metrics dashboard
- Advanced error recovery
- Rate limiting configuration

### Community Requests
- WebSocket direct mode
- Custom candle aggregation
- Real-time filters
- Alert system
- Docker support

## Contributing

We welcome contributions! See [CONTRIBUTING.md](CONTRIBUTING.md) for guidelines.

## License

MIT License - see [LICENSE](LICENSE) for details.

## Acknowledgments

Built on top of [BinaryOptionsToolsV2](https://github.com/ChipaDevTeam/BinaryOptionsToolsV2) by the ChipaDev Team.

## Support

- **GitHub Issues**: Report bugs or request features
- **Discussions**: Ask questions or share ideas
- **Documentation**: Check docs/ directory
- **Examples**: See examples/ directory

## Links

- **Repository**: https://github.com/ChipaDevTeam/ChipaPocketOptionData
- **PyPI**: https://pypi.org/project/ChipaPocketOptionData/
- **BinaryOptionsToolsV2**: https://github.com/ChipaDevTeam/BinaryOptionsToolsV2

---

**Made with ❤️ by the ChipaDev Team**

*Collect data efficiently, trade confidently.*
