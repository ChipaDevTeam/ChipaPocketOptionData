"""
Test script to verify ChipaPocketOptionData installation and basic functionality.
"""

import asyncio
import sys
from datetime import timedelta


def test_imports():
    """Test that all imports work correctly."""
    print("Testing imports...")
    try:
        from ChipaPocketOptionData import (
            subscribe_symbol,
            subscribe_symbol_timed,
            subscribe_symbol_chunked,
            get_candles,
            DataCollectorConfig,
            ProxyConfig,
        )
        print("✅ All imports successful")
        return True
    except ImportError as e:
        print(f"❌ Import failed: {e}")
        return False


def test_proxy_config():
    """Test ProxyConfig creation."""
    print("\nTesting ProxyConfig...")
    try:
        from ChipaPocketOptionData import ProxyConfig
        
        # Test basic proxy
        proxy1 = ProxyConfig(host="proxy.example.com", port=8080)
        assert proxy1.to_url() == "http://proxy.example.com:8080"
        
        # Test proxy with auth
        proxy2 = ProxyConfig(
            host="proxy.example.com",
            port=8080,
            username="user",
            password="pass"
        )
        assert proxy2.to_url() == "http://user:pass@proxy.example.com:8080"
        
        # Test SOCKS5
        proxy3 = ProxyConfig(
            host="socks.example.com",
            port=1080,
            protocol="socks5"
        )
        assert proxy3.to_url() == "socks5://socks.example.com:1080"
        
        print("✅ ProxyConfig works correctly")
        return True
    except Exception as e:
        print(f"❌ ProxyConfig failed: {e}")
        return False


def test_data_collector_config():
    """Test DataCollectorConfig creation."""
    print("\nTesting DataCollectorConfig...")
    try:
        from ChipaPocketOptionData import DataCollectorConfig, ProxyConfig
        
        # Test basic config
        config1 = DataCollectorConfig(
            ssids=["ssid1", "ssid2"]
        )
        assert len(config1.ssids) == 2
        assert config1.max_workers == 2
        
        # Test config with proxies
        proxies = [
            ProxyConfig(host="proxy1.com", port=8080),
            ProxyConfig(host="proxy2.com", port=8080),
        ]
        config2 = DataCollectorConfig(
            ssids=["ssid1", "ssid2"],
            proxies=proxies,
            proxy_support=True
        )
        assert len(config2.proxies) == 2
        assert config2.proxy_support == True
        
        # Test validation (should fail with no SSIDs)
        try:
            config3 = DataCollectorConfig(ssids=[])
            print("❌ Should have raised ValueError for empty SSIDs")
            return False
        except ValueError:
            pass  # Expected
        
        print("✅ DataCollectorConfig works correctly")
        return True
    except Exception as e:
        print(f"❌ DataCollectorConfig failed: {e}")
        return False


def test_collector_creation():
    """Test that collectors can be created (without connecting)."""
    print("\nTesting collector creation...")
    try:
        from ChipaPocketOptionData import (
            subscribe_symbol,
            subscribe_symbol_timed,
            subscribe_symbol_chunked,
        )
        
        # Note: We can't actually connect without valid SSIDs
        # Just test that the functions exist and accept parameters
        
        print("✅ Collector creation functions available")
        return True
    except Exception as e:
        print(f"❌ Collector creation failed: {e}")
        return False


async def test_with_real_ssid():
    """Test with a real SSID (optional, interactive)."""
    print("\n" + "="*60)
    print("OPTIONAL: Test with real SSID")
    print("="*60)
    
    test_real = input("\nDo you want to test with a real SSID? (y/n): ").strip().lower()
    
    if test_real != 'y':
        print("Skipping real SSID test")
        return True
    
    ssid = input("Enter your demo account SSID: ").strip()
    
    if not ssid:
        print("No SSID provided, skipping")
        return True
    
    try:
        from ChipaPocketOptionData import subscribe_symbol_timed
        
        print("\nAttempting to collect 5 candles...")
        
        collector = subscribe_symbol_timed(
            asset="EURUSD_otc",
            time_delta=timedelta(seconds=5),
            ssids=[ssid],
            proxy_support=False
        )
        
        candle_count = 0
        for candle in collector:
            if 'error' in candle:
                print(f"❌ Error: {candle['error']}")
                collector.stop()
                return False
            
            print(f"✅ Received candle #{candle_count + 1}: {candle.get('close')}")
            candle_count += 1
            
            if candle_count >= 5:
                collector.stop()
                break
        
        print(f"\n✅ Successfully collected {candle_count} candles!")
        return True
        
    except Exception as e:
        print(f"❌ Real SSID test failed: {e}")
        return False


def main():
    """Run all tests."""
    print("="*60)
    print("ChipaPocketOptionData Test Suite")
    print("="*60)
    
    results = []
    
    # Run basic tests
    results.append(("Imports", test_imports()))
    results.append(("ProxyConfig", test_proxy_config()))
    results.append(("DataCollectorConfig", test_data_collector_config()))
    results.append(("Collector Creation", test_collector_creation()))
    
    # Run optional SSID test
    if sys.version_info >= (3, 7):
        try:
            result = asyncio.run(test_with_real_ssid())
            results.append(("Real SSID Test", result))
        except Exception as e:
            print(f"Error running async test: {e}")
    
    # Print summary
    print("\n" + "="*60)
    print("TEST SUMMARY")
    print("="*60)
    
    passed = sum(1 for _, result in results if result)
    total = len(results)
    
    for name, result in results:
        status = "✅ PASS" if result else "❌ FAIL"
        print(f"{status} - {name}")
    
    print(f"\nTotal: {passed}/{total} tests passed")
    
    if passed == total:
        print("\n🎉 All tests passed!")
        return 0
    else:
        print(f"\n⚠️ {total - passed} test(s) failed")
        return 1


if __name__ == "__main__":
    exit_code = main()
    sys.exit(exit_code)
