#!/usr/bin/env python3
"""
Direct test of signal_renderer.py to validate functionality
"""

import os
import sys
from signal_renderer import (
    SignalRenderer, SignalData, SignalType, SignalPriority, 
    ChartData, KeyStat, StrategyInfo, generate_chart_data
)

def test_basic_signal():
    """Test rendering a basic signal"""
    print("🧪 Testing basic signal rendering...")
    
    # Create a simple signal
    signal = SignalData(
        ticker="AAPL",
        company_name="Apple Inc",
        signal_type=SignalType.EARNINGS,
        current_price=175.50,
        price_change=5.25,
        price_change_percent=3.2
    )
    
    print(f"   📊 Created signal: {signal.ticker} - {signal.company_name}")
    
    # Initialize renderer
    renderer = SignalRenderer(output_dir="test_output")
    print(f"   🎨 Renderer initialized, output dir: test_output")
    
    # Render signal
    try:
        output_path = renderer.render_signal(signal, "test_basic.html")
        print(f"   ✅ Signal rendered to: {output_path}")
        
        # Check if file exists and has content
        if os.path.exists(output_path):
            file_size = os.path.getsize(output_path)
            print(f"   📁 File size: {file_size} bytes")
            
            if file_size > 1000:  # Should be at least 1KB for valid HTML
                print("   ✅ File appears to have valid content")
                return True
            else:
                print("   ❌ File too small, likely empty or corrupted")
                return False
        else:
            print(f"   ❌ File not found at {output_path}")
            return False
            
    except Exception as e:
        print(f"   ❌ Error rendering signal: {e}")
        import traceback
        traceback.print_exc()
        return False

def test_full_featured_signal():
    """Test rendering a signal with all features"""
    print("\n🧪 Testing full-featured signal...")
    
    # Create a comprehensive signal
    signal = SignalData(
        ticker="CRCL",
        company_name="Circle Internet Group",
        signal_type=SignalType.IPO_TODAY,
        current_price=69.00,
        price_change=38.00,
        price_change_percent=122.6,
        
        priority=SignalPriority.HOT,
        
        key_stats=[
            KeyStat("223%", "Day 1 High", True),
            KeyStat("$6.8B", "Valuation", True),
            KeyStat("46M", "Volume", True)
        ],
        
        strategy=StrategyInfo(
            title="Hot IPO Momentum Play",
            description="Stablecoin leader 3x'd on debut. ARK bought $150M. Watch for dip to $60-65 for entry.",
            link_text="IPO playbook →",
            link_url="https://example.com/ipo-strategy"
        ),
        
        chart_data=generate_chart_data("CRCL", 69.00, "breakout"),
        
        timestamp="15 min ago",
        is_yolo=False
    )
    
    print(f"   📊 Created full signal: {signal.ticker}")
    print(f"   📈 Price: ${signal.current_price} ({signal.price_change_percent:+.1f}%)")
    print(f"   📋 Stats: {len(signal.key_stats)} items")
    print(f"   🧠 Strategy: {signal.strategy.title}")
    print(f"   📊 Chart data: {len(signal.chart_data.historical_data)} historical points")
    
    # Render signal
    renderer = SignalRenderer(output_dir="test_output")
    
    try:
        output_path = renderer.render_signal(signal, "test_full.html")
        print(f"   ✅ Full signal rendered to: {output_path}")
        
        # Validate file
        if os.path.exists(output_path):
            file_size = os.path.getsize(output_path)
            print(f"   📁 File size: {file_size} bytes")
            
            # Read first few lines to validate HTML structure
            with open(output_path, 'r') as f:
                first_lines = [f.readline().strip() for _ in range(5)]
                
            print("   📄 File starts with:")
            for i, line in enumerate(first_lines, 1):
                if line:
                    print(f"      {i}: {line[:80]}...")
                    
            # Check for key elements
            with open(output_path, 'r') as f:
                content = f.read()
                
            key_elements = [
                ('DOCTYPE', '<!DOCTYPE html>' in content),
                ('Title', '<title>' in content),
                ('CSS', '<style>' in content),
                ('Ticker', signal.ticker in content),
                ('Company', signal.company_name in content),
                ('Chart', 'chart-' in content),
                ('JavaScript', '<script>' in content)
            ]
            
            print("   🔍 Content validation:")
            all_valid = True
            for element, found in key_elements:
                status = "✅" if found else "❌"
                print(f"      {status} {element}")
                if not found:
                    all_valid = False
                    
            return all_valid
            
        else:
            print(f"   ❌ File not found at {output_path}")
            return False
            
    except Exception as e:
        print(f"   ❌ Error rendering full signal: {e}")
        import traceback
        traceback.print_exc()
        return False

def test_all_signal_types():
    """Test rendering all signal types"""
    print("\n🧪 Testing all signal types...")
    
    test_signals = [
        ("CRCL", "Circle Group", SignalType.IPO_TODAY, 69.00, 122.6),
        ("BTC", "Bitcoin", SignalType.YOLO_CALLS, 105456.00, 3.8),
        ("NVDA", "Nvidia", SignalType.PRE_MARKET, 1125.50, 5.2),
        ("AMZN", "Amazon", SignalType.STOCK_SPLIT, 3245.00, 8.2),
        ("TSLA", "Tesla", SignalType.PUT_SPREAD, 245.80, -1.2),
        ("ETH", "Ethereum", SignalType.CRYPTO_DEFI, 3856.00, 4.5),
        ("SAVA", "Cassava Sciences", SignalType.FDA_EVENT, 42.15, 12.3),
        ("GOOGL", "Google", SignalType.EARNINGS, 178.25, 8.5),
        ("AMD", "AMD", SignalType.UNUSUAL_OPTIONS, 185.40, 2.1),
        ("GME", "GameStop", SignalType.MEME_SQUEEZE, 45.20, 35.2)
    ]
    
    renderer = SignalRenderer(output_dir="test_output")
    success_count = 0
    
    for ticker, company, signal_type, price, change_pct in test_signals:
        try:
            signal = SignalData(
                ticker=ticker,
                company_name=company,
                signal_type=signal_type,
                current_price=price,
                price_change=price * (change_pct / 100),
                price_change_percent=change_pct
            )
            
            filename = f"test_{ticker.lower()}_{signal_type.name.lower()}.html"
            output_path = renderer.render_signal(signal, filename)
            
            if os.path.exists(output_path) and os.path.getsize(output_path) > 1000:
                print(f"   ✅ {ticker} ({signal_type.name})")
                success_count += 1
            else:
                print(f"   ❌ {ticker} ({signal_type.name}) - file too small or missing")
                
        except Exception as e:
            print(f"   ❌ {ticker} ({signal_type.name}) - error: {e}")
    
    print(f"\n   📊 Success rate: {success_count}/{len(test_signals)} ({success_count/len(test_signals)*100:.1f}%)")
    return success_count == len(test_signals)

def main():
    """Run all tests"""
    print("🚀 Signal Renderer Validation Tests")
    print("=" * 50)
    
    # Clean up any previous test files
    if os.path.exists("test_output"):
        import shutil
        shutil.rmtree("test_output")
    
    test_results = []
    
    # Run tests
    test_results.append(("Basic Signal", test_basic_signal()))
    test_results.append(("Full Featured Signal", test_full_featured_signal()))  
    test_results.append(("All Signal Types", test_all_signal_types()))
    
    # Summary
    print("\n" + "=" * 50)
    print("📋 Test Results Summary:")
    
    passed = 0
    for test_name, result in test_results:
        status = "✅ PASS" if result else "❌ FAIL"
        print(f"  {status} {test_name}")
        if result:
            passed += 1
    
    print(f"\n🎯 Overall: {passed}/{len(test_results)} tests passed")
    
    # List generated files
    if os.path.exists("test_output"):
        files = os.listdir("test_output")
        if files:
            print(f"\n📁 Generated {len(files)} test files in test_output/:")
            for file in sorted(files):
                file_path = os.path.join("test_output", file)
                size = os.path.getsize(file_path)
                print(f"   📄 {file} ({size:,} bytes)")
        else:
            print("\n❌ No files generated!")
    else:
        print("\n❌ Test output directory not created!")
    
    return passed == len(test_results)

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)