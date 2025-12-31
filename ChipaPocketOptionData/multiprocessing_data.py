"""
Multi-process data collector for PocketOption using BinaryOptionsToolsV2.

This module provides functions to collect market data from PocketOption using
multiple demo accounts, each with its own proxy server, via multiprocessing.
"""

import asyncio
import multiprocessing as mp
from typing import List, Dict, Any, Optional, AsyncIterator, Union
from datetime import timedelta
from dataclasses import dataclass, field
import queue
import signal
import sys


@dataclass
class ProxyConfig:
    """Configuration for a single proxy server."""
    host: str
    port: int
    username: Optional[str] = None
    password: Optional[str] = None
    protocol: str = "http"  # http, https, socks5
    
    def to_url(self) -> str:
        """Convert proxy config to URL format."""
        if self.username and self.password:
            return f"{self.protocol}://{self.username}:{self.password}@{self.host}:{self.port}"
        return f"{self.protocol}://{self.host}:{self.port}"


@dataclass
class DataCollectorConfig:
    """Configuration for the data collector."""
    ssids: List[str]
    proxies: Optional[List[ProxyConfig]] = None
    proxy_support: bool = False
    max_workers: Optional[int] = None
    reconnect_on_error: bool = True
    error_retry_delay: int = 5
    log_level: str = "INFO"
    log_path: Optional[str] = None
    
    def __post_init__(self):
        """Validate configuration after initialization."""
        if not self.ssids:
            raise ValueError("At least one SSID must be provided")
        
        if self.proxy_support and self.proxies:
            if len(self.proxies) < len(self.ssids):
                raise ValueError(
                    f"Number of proxies ({len(self.proxies)}) must be >= "
                    f"number of SSIDs ({len(self.ssids)})"
                )
        
        if self.max_workers is None:
            self.max_workers = len(self.ssids)


class _DataCollectorProcess:
    """Internal class to handle data collection in a single process."""
    
    def __init__(
        self,
        ssid: str,
        proxy: Optional[ProxyConfig],
        output_queue: mp.Queue,
        config: DataCollectorConfig,
    ):
        self.ssid = ssid
        self.proxy = proxy
        self.output_queue = output_queue
        self.config = config
        self._stop_event = mp.Event()
    
    async def _setup_api(self):
        """Setup the PocketOption API with optional proxy."""
        from BinaryOptionsToolsV2.pocketoption import PocketOptionAsync
        
        # TODO: When BinaryOptionsToolsV2 supports proxies, pass proxy config here
        # For now, we'll need to set proxy at the environment/system level
        if self.proxy:
            # This would need to be implemented in BinaryOptionsToolsV2
            # For now, we can set environment variables or use a proxy library
            pass
        
        api = PocketOptionAsync(self.ssid)
        await asyncio.sleep(5)  # Wait for connection
        return api
    
    async def subscribe_symbol(self, asset: str):
        """Subscribe to symbol updates."""
        from BinaryOptionsToolsV2.pocketoption import PocketOptionAsync
        
        try:
            api = await self._setup_api()
            stream = await api.subscribe_symbol(asset)
            
            async for candle in stream:
                if self._stop_event.is_set():
                    break
                
                # Add metadata
                candle['ssid'] = self.ssid
                candle['proxy'] = self.proxy.to_url() if self.proxy else None
                
                try:
                    self.output_queue.put_nowait(candle)
                except queue.Full:
                    # Queue is full, skip this candle
                    pass
                    
        except Exception as e:
            error_msg = {
                'error': str(e),
                'ssid': self.ssid,
                'type': 'subscribe_symbol',
            }
            self.output_queue.put_nowait(error_msg)
            
            if self.config.reconnect_on_error:
                await asyncio.sleep(self.config.error_retry_delay)
                await self.subscribe_symbol(asset)
    
    async def subscribe_symbol_timed(self, asset: str, time_delta: timedelta):
        """Subscribe to symbol updates with time-based chunking."""
        from BinaryOptionsToolsV2.pocketoption import PocketOptionAsync
        
        try:
            api = await self._setup_api()
            stream = await api.subscribe_symbol_timed(asset, time_delta)
            
            async for candle in stream:
                if self._stop_event.is_set():
                    break
                
                # Add metadata
                candle['ssid'] = self.ssid
                candle['proxy'] = self.proxy.to_url() if self.proxy else None
                
                try:
                    self.output_queue.put_nowait(candle)
                except queue.Full:
                    pass
                    
        except Exception as e:
            error_msg = {
                'error': str(e),
                'ssid': self.ssid,
                'type': 'subscribe_symbol_timed',
            }
            self.output_queue.put_nowait(error_msg)
            
            if self.config.reconnect_on_error:
                await asyncio.sleep(self.config.error_retry_delay)
                await self.subscribe_symbol_timed(asset, time_delta)
    
    async def subscribe_symbol_chunked(self, asset: str, chunk_size: int):
        """Subscribe to symbol updates with chunk-based aggregation."""
        from BinaryOptionsToolsV2.pocketoption import PocketOptionAsync
        
        try:
            api = await self._setup_api()
            stream = await api.subscribe_symbol_chuncked(asset, chunk_size)
            
            async for candle in stream:
                if self._stop_event.is_set():
                    break
                
                # Add metadata
                candle['ssid'] = self.ssid
                candle['proxy'] = self.proxy.to_url() if self.proxy else None
                
                try:
                    self.output_queue.put_nowait(candle)
                except queue.Full:
                    pass
                    
        except Exception as e:
            error_msg = {
                'error': str(e),
                'ssid': self.ssid,
                'type': 'subscribe_symbol_chunked',
            }
            self.output_queue.put_nowait(error_msg)
            
            if self.config.reconnect_on_error:
                await asyncio.sleep(self.config.error_retry_delay)
                await self.subscribe_symbol_chunked(asset, chunk_size)
    
    async def get_candles(self, asset: str, period: int, time: int):
        """Get historical candles."""
        try:
            api = await self._setup_api()
            candles = await api.get_candles(asset, period, time)
            
            # Add metadata to each candle
            for candle in candles:
                candle['ssid'] = self.ssid
                candle['proxy'] = self.proxy.to_url() if self.proxy else None
            
            result = {
                'type': 'candles',
                'data': candles,
                'ssid': self.ssid,
            }
            self.output_queue.put_nowait(result)
            
        except Exception as e:
            error_msg = {
                'error': str(e),
                'ssid': self.ssid,
                'type': 'get_candles',
            }
            self.output_queue.put_nowait(error_msg)
    
    def stop(self):
        """Signal the process to stop."""
        self._stop_event.set()


def _worker_process(
    ssid: str,
    proxy: Optional[ProxyConfig],
    output_queue: mp.Queue,
    config: DataCollectorConfig,
    method: str,
    *args,
    **kwargs,
):
    """Worker process function."""
    # Setup logging if configured
    if config.log_path:
        from BinaryOptionsToolsV2.tracing import start_logs
        start_logs(config.log_path, config.log_level, terminal=True)
    
    # Handle graceful shutdown
    def signal_handler(sig, frame):
        sys.exit(0)
    
    signal.signal(signal.SIGINT, signal_handler)
    signal.signal(signal.SIGTERM, signal_handler)
    
    # Create collector and run the appropriate method
    collector = _DataCollectorProcess(ssid, proxy, output_queue, config)
    
    try:
        if method == 'subscribe_symbol':
            asyncio.run(collector.subscribe_symbol(*args, **kwargs))
        elif method == 'subscribe_symbol_timed':
            asyncio.run(collector.subscribe_symbol_timed(*args, **kwargs))
        elif method == 'subscribe_symbol_chunked':
            asyncio.run(collector.subscribe_symbol_chunked(*args, **kwargs))
        elif method == 'get_candles':
            asyncio.run(collector.get_candles(*args, **kwargs))
    except KeyboardInterrupt:
        pass


class MultiProcessDataCollector:
    """Multi-process data collector for PocketOption."""
    
    def __init__(self, config: DataCollectorConfig):
        self.config = config
        self.output_queue = mp.Queue(maxsize=10000)
        self.processes: List[mp.Process] = []
        self._started = False
    
    def _start_processes(self, method: str, *args, **kwargs):
        """Start worker processes."""
        if self._started:
            raise RuntimeError("Collector already started")
        
        for i, ssid in enumerate(self.config.ssids):
            proxy = None
            if self.config.proxy_support and self.config.proxies:
                # Assign proxy to this SSID (round-robin if more SSIDs than proxies)
                proxy = self.config.proxies[i % len(self.config.proxies)]
            
            process = mp.Process(
                target=_worker_process,
                args=(ssid, proxy, self.output_queue, self.config, method, *args),
                kwargs=kwargs,
            )
            process.start()
            self.processes.append(process)
        
        self._started = True
    
    def __iter__(self):
        """Iterate over collected data (blocking)."""
        while True:
            try:
                data = self.output_queue.get(timeout=1)
                yield data
            except queue.Empty:
                # Check if any processes are still alive
                if not any(p.is_alive() for p in self.processes):
                    break
            except KeyboardInterrupt:
                self.stop()
                break
    
    async def __aiter__(self):
        """Async iterate over collected data."""
        while True:
            try:
                # Use asyncio-compatible queue access
                data = await asyncio.get_event_loop().run_in_executor(
                    None, self.output_queue.get, True, 1
                )
                yield data
            except queue.Empty:
                if not any(p.is_alive() for p in self.processes):
                    break
            except KeyboardInterrupt:
                self.stop()
                break
    
    def stop(self):
        """Stop all worker processes."""
        for process in self.processes:
            if process.is_alive():
                process.terminate()
                process.join(timeout=5)
                if process.is_alive():
                    process.kill()
        
        self.processes.clear()
        self._started = False
    
    def __enter__(self):
        """Context manager entry."""
        return self
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        """Context manager exit."""
        self.stop()


# Public API functions

def subscribe_symbol(
    asset: str,
    ssids: List[str],
    proxies: Optional[List[ProxyConfig]] = None,
    proxy_support: bool = False,
    **config_kwargs,
) -> MultiProcessDataCollector:
    """
    Subscribe to real-time symbol updates using multiple demo accounts.
    
    Args:
        asset: The asset symbol to subscribe to (e.g., "EURUSD_otc")
        ssids: List of session IDs for demo accounts
        proxies: Optional list of proxy configurations
        proxy_support: Enable proxy support
        **config_kwargs: Additional configuration options
    
    Returns:
        MultiProcessDataCollector instance that can be iterated over
    
    Example:
        >>> from ChipaPocketOptionData import subscribe_symbol, ProxyConfig
        >>> 
        >>> ssids = ["ssid1", "ssid2", "ssid3"]
        >>> proxies = [
        ...     ProxyConfig(host="proxy1.com", port=8080),
        ...     ProxyConfig(host="proxy2.com", port=8080),
        ... ]
        >>> 
        >>> collector = subscribe_symbol(
        ...     "EURUSD_otc",
        ...     ssids=ssids,
        ...     proxies=proxies,
        ...     proxy_support=True
        ... )
        >>> 
        >>> for candle in collector:
        ...     print(f"Received: {candle}")
    """
    config = DataCollectorConfig(
        ssids=ssids,
        proxies=proxies,
        proxy_support=proxy_support,
        **config_kwargs,
    )
    
    collector = MultiProcessDataCollector(config)
    collector._start_processes('subscribe_symbol', asset)
    return collector


def subscribe_symbol_timed(
    asset: str,
    time_delta: Union[timedelta, int],
    ssids: List[str],
    proxies: Optional[List[ProxyConfig]] = None,
    proxy_support: bool = False,
    **config_kwargs,
) -> MultiProcessDataCollector:
    """
    Subscribe to time-chunked symbol updates using multiple demo accounts.
    
    Args:
        asset: The asset symbol to subscribe to (e.g., "EURUSD_otc")
        time_delta: Time delta for chunking (timedelta or seconds as int)
        ssids: List of session IDs for demo accounts
        proxies: Optional list of proxy configurations
        proxy_support: Enable proxy support
        **config_kwargs: Additional configuration options
    
    Returns:
        MultiProcessDataCollector instance that can be iterated over
    
    Example:
        >>> from ChipaPocketOptionData import subscribe_symbol_timed
        >>> from datetime import timedelta
        >>> 
        >>> ssids = ["ssid1", "ssid2"]
        >>> collector = subscribe_symbol_timed(
        ...     "EURUSD_otc",
        ...     timedelta(seconds=5),
        ...     ssids=ssids,
        ...     proxy_support=False
        ... )
        >>> 
        >>> for candle in collector:
        ...     print(f"5-second candle: {candle}")
    """
    # Convert int seconds to timedelta if needed
    if isinstance(time_delta, int):
        time_delta = timedelta(seconds=time_delta)
    
    config = DataCollectorConfig(
        ssids=ssids,
        proxies=proxies,
        proxy_support=proxy_support,
        **config_kwargs,
    )
    
    collector = MultiProcessDataCollector(config)
    collector._start_processes('subscribe_symbol_timed', asset, time_delta)
    return collector


def subscribe_symbol_chunked(
    asset: str,
    chunk_size: int,
    ssids: List[str],
    proxies: Optional[List[ProxyConfig]] = None,
    proxy_support: bool = False,
    **config_kwargs,
) -> MultiProcessDataCollector:
    """
    Subscribe to chunk-aggregated symbol updates using multiple demo accounts.
    
    Args:
        asset: The asset symbol to subscribe to (e.g., "EURUSD_otc")
        chunk_size: Number of candles to aggregate
        ssids: List of session IDs for demo accounts
        proxies: Optional list of proxy configurations
        proxy_support: Enable proxy support
        **config_kwargs: Additional configuration options
    
    Returns:
        MultiProcessDataCollector instance that can be iterated over
    
    Example:
        >>> from ChipaPocketOptionData import subscribe_symbol_chunked
        >>> 
        >>> ssids = ["ssid1", "ssid2"]
        >>> collector = subscribe_symbol_chunked(
        ...     "EURUSD_otc",
        ...     chunk_size=15,
        ...     ssids=ssids,
        ...     proxy_support=False
        ... )
        >>> 
        >>> for candle in collector:
        ...     print(f"Aggregated candle (15 candles): {candle}")
    """
    config = DataCollectorConfig(
        ssids=ssids,
        proxies=proxies,
        proxy_support=proxy_support,
        **config_kwargs,
    )
    
    collector = MultiProcessDataCollector(config)
    collector._start_processes('subscribe_symbol_chunked', asset, chunk_size)
    return collector


def get_candles(
    asset: str,
    period: int,
    time: int,
    ssids: List[str],
    proxies: Optional[List[ProxyConfig]] = None,
    proxy_support: bool = False,
    **config_kwargs,
) -> List[Dict[str, Any]]:
    """
    Get historical candles using multiple demo accounts (aggregates results).
    
    Args:
        asset: The asset symbol (e.g., "EURUSD_otc")
        period: Candle period in seconds
        time: Historical time range
        ssids: List of session IDs for demo accounts
        proxies: Optional list of proxy configurations
        proxy_support: Enable proxy support
        **config_kwargs: Additional configuration options
    
    Returns:
        List of all candles collected from all processes
    
    Example:
        >>> from ChipaPocketOptionData import get_candles
        >>> 
        >>> ssids = ["ssid1"]
        >>> candles = get_candles(
        ...     "EURUSD_otc",
        ...     period=60,
        ...     time=3600,
        ...     ssids=ssids
        ... )
        >>> print(f"Collected {len(candles)} candles")
    """
    config = DataCollectorConfig(
        ssids=ssids,
        proxies=proxies,
        proxy_support=proxy_support,
        **config_kwargs,
    )
    
    collector = MultiProcessDataCollector(config)
    collector._start_processes('get_candles', asset, period, time)
    
    # Collect all results
    all_candles = []
    for data in collector:
        if 'error' in data:
            print(f"Error from {data['ssid']}: {data['error']}")
        elif data.get('type') == 'candles':
            all_candles.extend(data['data'])
    
    return all_candles
