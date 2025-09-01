"""
Example Usage: Signal Rendering Engine with Market Scan Data
Demonstrates how market scan engine feeds would be processed into HTML signals
"""

from signal_renderer import (
    SignalRenderer, SignalData, SignalType, SignalPriority, 
    ChartData, KeyStat, StrategyInfo, generate_chart_data
)
import json

def simulate_market_scan_feed():
    """
    Simulate market scan engine providing signals
    In real implementation, this would come from:
    - News API (company events, IPO dates, FDA calendars)  
    - Market Data API (price, volume, unusual activity)
    - Analysis Engine (sentiment, technical indicators, popularity)
    """
    
    # Example 1: IPO Signal from Market Scan
    # News API: "CRCL IPO pricing at $31, trading starts today"
    # Market Data: Current price $69, +122% from IPO price
    # Analysis Engine: High social media buzz, ARK Invest purchase -> mark as HOT
    crcl_signal = SignalData(
        ticker="CRCL",
        company_name="Circle Internet Group",
        signal_type=SignalType.IPO_TODAY,
        priority=SignalPriority.HOT,
        
        current_price=69.00,
        price_change=38.00,
        price_change_percent=122.6,
        
        key_stats=[
            KeyStat("223%", "Day 1 High", True),
            KeyStat("$6.8B", "Valuation"),
            KeyStat("46M", "Volume")
        ],
        
        strategy=StrategyInfo(
            title="Hot IPO Momentum Play",
            description="Stablecoin leader 3x'd on debut. ARK bought $150M. Watch for dip to $60-65 for entry. Similar to Coinbase IPO pattern - expect volatility.",
            link_text="IPO playbook →",
            link_url="https://example.com/ipo-trading-strategy"
        ),
        
        chart_data=generate_chart_data("CRCL", 69.00, "breakout"),
        
        timestamp="15 min ago",
        notifications_enabled=True
    )
    crcl_signal.chart_data.event_label = "IPO $31 → $103 peak"
    
    # Example 2: YOLO Signal from Options Flow Scanner  
    # Options Flow API: Massive call buying on BTC options
    # Prediction Market API: Kalshi shows 75% odds of 150K by Q4
    # Analysis Engine: High risk/reward ratio, social sentiment -> YOLO category
    btc_yolo_signal = SignalData(
        ticker="BTC",
        company_name="Bitcoin 150K Moonshot", 
        signal_type=SignalType.YOLO_CALLS,
        priority=SignalPriority.NORMAL,
        
        current_price=105456.00,
        price_change=3850.00,
        price_change_percent=3.8,
        
        key_stats=[
            KeyStat("250%", "Max Gain", True),
            KeyStat("-100%", "Max Loss", False), 
            KeyStat("$850", "Per Call")
        ],
        
        strategy=StrategyInfo(
            title="Dec 150K Call Options",
            description="Kalshi shows 75% odds of 150K by Q4. Buy $130K calls for December. High risk, high reward - only risk what you can lose!",
            link_text="View odds →",
            link_url="https://kalshi.com/markets/kxbtcmax150"
        ),
        
        chart_data=generate_chart_data("BTC", 105456.00, "momentum"),
        
        timestamp="1 hour ago",
        is_yolo=True,
        has_animation=True
    )
    btc_yolo_signal.chart_data.event_label = "Kalshi 75% → 150K"
    btc_yolo_signal.chart_data.chart_color = "#ff00ff"
    
    # Example 3: Pre-Market Signal
    # News API: "TSMC production boost benefits NVDA"
    # Market Data API: Pre-market trading up 5.2%, high volume
    # Analysis Engine: Gap-up pattern, high probability -> Pre-market signal
    nvda_premarket = SignalData(
        ticker="NVDA",
        company_name="Nvidia Pre-Market Surge",
        signal_type=SignalType.PRE_MARKET,
        priority=SignalPriority.NORMAL,
        
        current_price=1125.50,
        price_change=55.50,
        price_change_percent=5.2,
        
        key_stats=[
            KeyStat("+6.8%", "Pre-Mkt", True),
            KeyStat("2.5M", "Volume"),
            KeyStat("9:28", "Entry")
        ],
        
        strategy=StrategyInfo(
            title="Pre-Market Gap & Go",
            description="TSMC production boost news. Pre-market up 6.8% on heavy volume. Buy at 9:28-9:30 for opening momentum. Set stop at pre-market low.",
            link_text="Pre-market guide →",
            link_url="https://example.com/premarket-trading"
        ),
        
        chart_data=generate_chart_data("NVDA", 1125.50, "breakout"),
        
        timestamp="Pre-market",
        border_style="dashed"
    )
    nvda_premarket.chart_data.event_label = "Taiwan news 4AM"
    nvda_premarket.chart_data.chart_color = "#ffd93d"
    
    # Example 4: FDA Event Signal
    # FDA Calendar API: PDUFA date 7/28 for SAVA
    # Options Data: High IV, binary event setup
    # Analysis Engine: High risk binary event -> FDA + YOLO tags
    sava_fda = SignalData(
        ticker="SAVA",
        company_name="Cassava Sciences",
        signal_type=SignalType.FDA_EVENT,
        priority=SignalPriority.NORMAL,
        
        current_price=42.15,
        price_change=4.65,
        price_change_percent=12.3,
        
        key_stats=[
            KeyStat("+180%", "If Pass", True),
            KeyStat("-65%", "If Fail", False),
            KeyStat("220%", "IV")
        ],
        
        strategy=StrategyInfo(
            title="Binary FDA Event - YOLO!",
            description="Alzheimer's drug PDUFA date 7/28. Buy OTM calls for 10x potential. Ultra high risk - total loss possible. Size accordingly!",
            link_text="FDA calendar →", 
            link_url="https://example.com/fda-calendar"
        ),
        
        chart_data=generate_chart_data("SAVA", 42.15, "volatile"),
        
        timestamp="5 hours ago",
        is_yolo=True
    )
    sava_fda.chart_data.event_label = "FDA 7/28"
    sava_fda.chart_data.chart_color = "#16a085"
    
    # Example 5: Unusual Options Activity
    # Options Flow Scanner: 10,000 AMD calls, 10x normal volume
    # Market Data: Large premium spent ($2.5M)
    # Analysis Engine: Smart money following -> Unusual Options signal
    amd_options = SignalData(
        ticker="AMD",
        company_name="Unusual Call Buying",
        signal_type=SignalType.UNUSUAL_OPTIONS,
        priority=SignalPriority.WATCH,
        
        current_price=185.40,
        price_change=3.85,
        price_change_percent=2.1,
        
        key_stats=[
            KeyStat("$2.5M", "Premium"),
            KeyStat("10x", "Avg Vol"),
            KeyStat("$200", "Strike")
        ],
        
        strategy=StrategyInfo(
            title="Follow the Smart Money",
            description="10,000 Aug $200 calls bought for $2.5M. 10x normal volume. Someone knows something. Follow with smaller position or spreads.",
            link_text="Flow data →",
            link_url="https://example.com/options-flow"
        ),
        
        chart_data=generate_chart_data("AMD", 185.40, "momentum"),
        
        timestamp="30 min ago"
    )
    amd_options.chart_data.event_label = "10K calls"
    amd_options.chart_data.chart_color = "#d35400"
    
    return [crcl_signal, btc_yolo_signal, nvda_premarket, sava_fda, amd_options]

def simulate_market_scan_integration():
    """
    Example of how a market scan engine would feed data to the renderer
    """
    
    print("🔍 Market Scan Engine Processing...")
    print("📊 Scanning news feeds, options flow, pre-market activity...")
    print("🧠 Running analysis engine for signal classification...")
    print()
    
    # Get signals from market scan
    signals = simulate_market_scan_feed()
    
    # Initialize renderer
    renderer = SignalRenderer(output_dir="generated_signals")
    
    print("🎨 Rendering signals to HTML...")
    
    # Render each signal
    generated_files = []
    for signal in signals:
        filename = f"{signal.ticker}_{signal.signal_type.name.lower()}.html"
        output_path = renderer.render_signal(signal, filename)
        generated_files.append(output_path)
        
        print(f"  ✅ {signal.ticker} ({signal.signal_type.name}) -> {output_path}")
        
    print(f"\n🚀 Generated {len(generated_files)} signal pages!")
    print("\nGenerated files:")
    for file in generated_files:
        print(f"  📄 {file}")
        
    # Generate summary of all signals (for index page)
    generate_signals_summary(signals, renderer)
    
    return generated_files

def generate_signals_summary(signals, renderer):
    """Generate a summary JSON of all signals for dashboard integration"""
    
    summary = {
        "timestamp": "2024-01-15T10:30:00Z",
        "total_signals": len(signals),
        "signals": []
    }
    
    for signal in signals:
        summary["signals"].append({
            "ticker": signal.ticker,
            "company_name": signal.company_name,
            "signal_type": signal.signal_type.name,
            "priority": signal.priority.name,
            "current_price": signal.current_price,
            "price_change_percent": signal.price_change_percent,
            "timestamp": signal.timestamp,
            "html_file": f"{signal.ticker.lower()}_{signal.signal_type.name.lower()}.html"
        })
    
    summary_path = f"{renderer.output_dir}/signals_summary.json"
    with open(summary_path, 'w') as f:
        json.dump(summary, f, indent=2)
        
    print(f"  📋 Summary -> {summary_path}")

if __name__ == "__main__":
    print("🎯 Signal Rendering Engine Demo")
    print("=" * 50)
    
    # Run the simulation
    generated_files = simulate_market_scan_integration()
    
    print("\n" + "=" * 50)
    print("🎉 Demo complete! Check the generated_signals/ directory")
    print("\nNext steps:")
    print("1. 📡 Connect real market data APIs")
    print("2. 🔍 Integrate news sentiment analysis")  
    print("3. 🧠 Add machine learning signal classification")
    print("4. 📱 Deploy to mobile-friendly hosting")