#!/usr/bin/env python3
"""
Generate Complete Signal Suite
Creates all 10 signal types with realistic market data
"""

from signal_renderer import (
    SignalRenderer, SignalData, SignalType, SignalPriority, 
    ChartData, KeyStat, StrategyInfo, generate_chart_data
)
import os

def create_complete_signal_suite():
    """Generate all signal types with realistic data"""
    
    print("🚀 Generating Complete Signal Suite")
    print("=" * 60)
    
    signals_data = [
        # IPO Signal - Hot debut
        {
            "ticker": "CRCL",
            "company_name": "Circle Internet Group",
            "signal_type": SignalType.IPO_TODAY,
            "priority": SignalPriority.HOT,
            "current_price": 69.00,
            "price_change": 38.00,
            "price_change_percent": 122.6,
            "key_stats": [
                KeyStat("223%", "Day 1 High", True),
                KeyStat("$6.8B", "Valuation"),
                KeyStat("46M", "Volume")
            ],
            "strategy": StrategyInfo(
                title="Hot IPO Momentum Play",
                description="Stablecoin leader 3x'd on debut. ARK bought $150M. Watch for dip to $60-65 for entry. Similar to Coinbase IPO pattern - expect volatility.",
                link_text="IPO playbook →",
                link_url="https://example.com/ipo-trading-strategy"
            ),
            "timestamp": "15 min ago",
            "pattern": "breakout",
            "is_yolo": False,
            "border_style": "solid"
        },
        
        # YOLO Signal - High risk Bitcoin play
        {
            "ticker": "BTC",
            "company_name": "Bitcoin 150K Moonshot",
            "signal_type": SignalType.YOLO_CALLS,
            "priority": SignalPriority.NORMAL,
            "current_price": 105456.00,
            "price_change": 3850.00,
            "price_change_percent": 3.8,
            "key_stats": [
                KeyStat("250%", "Max Gain", True),
                KeyStat("-100%", "Max Loss", False),
                KeyStat("$850", "Per Call")
            ],
            "strategy": StrategyInfo(
                title="Dec 150K Call Options",
                description="Kalshi shows 75% odds of 150K by Q4. Buy $130K calls for December. High risk, high reward - only risk what you can lose!",
                link_text="View odds →",
                link_url="https://kalshi.com/markets/kxbtcmax150"
            ),
            "timestamp": "1 hour ago",
            "pattern": "momentum",
            "is_yolo": True,
            "border_style": "solid"
        },
        
        # Pre-Market Signal - Gap up play
        {
            "ticker": "NVDA",
            "company_name": "Nvidia Pre-Market Surge",
            "signal_type": SignalType.PRE_MARKET,
            "priority": SignalPriority.NORMAL,
            "current_price": 1125.50,
            "price_change": 55.50,
            "price_change_percent": 5.2,
            "key_stats": [
                KeyStat("+6.8%", "Pre-Mkt", True),
                KeyStat("2.5M", "Volume"),
                KeyStat("9:28", "Entry")
            ],
            "strategy": StrategyInfo(
                title="Pre-Market Gap & Go",
                description="TSMC production boost news. Pre-market up 6.8% on heavy volume. Buy at 9:28-9:30 for opening momentum. Set stop at pre-market low.",
                link_text="Pre-market guide →",
                link_url="https://example.com/premarket-trading"
            ),
            "timestamp": "Pre-market",
            "pattern": "breakout",
            "is_yolo": False,
            "border_style": "dashed"
        },
        
        # Stock Split Signal
        {
            "ticker": "AMZN",
            "company_name": "Amazon Split Announced",
            "signal_type": SignalType.STOCK_SPLIT,
            "priority": SignalPriority.NORMAL,
            "current_price": 3245.00,
            "price_change": 245.00,
            "price_change_percent": 8.2,
            "key_stats": [
                KeyStat("20:1", "Ratio"),
                KeyStat("+15%", "Avg Run", True),
                KeyStat("28d", "To Split")
            ],
            "strategy": StrategyInfo(
                title="Pre-Split Momentum",
                description="20:1 split announced. Historical data shows 15% avg gain from announcement to split date. Buy shares or Aug calls. Retail FOMO incoming.",
                link_text="Split history →",
                link_url="https://example.com/stock-split-strategy"
            ),
            "timestamp": "2 hours ago",
            "pattern": "momentum",
            "is_yolo": False,
            "border_style": "solid"
        },
        
        # Options Spread Signal
        {
            "ticker": "TSLA",
            "company_name": "Tesla Iron Condor",
            "signal_type": SignalType.PUT_SPREAD,
            "priority": SignalPriority.NORMAL,
            "current_price": 245.80,
            "price_change": -2.85,
            "price_change_percent": -1.2,
            "key_stats": [
                KeyStat("$3.20", "Credit"),
                KeyStat("72%", "PoP", True),
                KeyStat("21d", "DTE")
            ],
            "strategy": StrategyInfo(
                title="Sell 240/235 Put Spread",
                description="Post-earnings IV crush. Sell 240/235 put spread for $3.20 credit. 72% probability of profit. Max loss $180. Range-bound expected.",
                link_text="Spread calculator →",
                link_url="https://example.com/credit-spreads"
            ),
            "timestamp": "3 hours ago",
            "pattern": "volatile",
            "is_yolo": False,
            "border_style": "solid"
        },
        
        # Crypto DeFi Signal
        {
            "ticker": "ETH",
            "company_name": "Ethereum Staking Play",
            "signal_type": SignalType.CRYPTO_DEFI,
            "priority": SignalPriority.NORMAL,
            "current_price": 3856.00,
            "price_change": 166.00,
            "price_change_percent": 4.5,
            "key_stats": [
                KeyStat("5.2%", "APY", True),
                KeyStat("$4.2K", "Target"),
                KeyStat("85", "RSI")
            ],
            "strategy": StrategyInfo(
                title="Stake & Trade Momentum",
                description="Shanghai upgrade complete. Staking APY 5.2% + price appreciation. Buy spot ETH or ETHE. DeFi TVL surging, institutions accumulating.",
                link_text="Staking guide →",
                link_url="https://example.com/eth-staking"
            ),
            "timestamp": "4 hours ago",
            "pattern": "momentum",
            "is_yolo": False,
            "border_style": "solid"
        },
        
        # FDA Event Signal
        {
            "ticker": "SAVA",
            "company_name": "Cassava Sciences",
            "signal_type": SignalType.FDA_EVENT,
            "priority": SignalPriority.NORMAL,
            "current_price": 42.15,
            "price_change": 4.65,
            "price_change_percent": 12.3,
            "key_stats": [
                KeyStat("+180%", "If Pass", True),
                KeyStat("-65%", "If Fail", False),
                KeyStat("220%", "IV")
            ],
            "strategy": StrategyInfo(
                title="Binary FDA Event - YOLO!",
                description="Alzheimer's drug PDUFA date 7/28. Buy OTM calls for 10x potential. Ultra high risk - total loss possible. Size accordingly!",
                link_text="FDA calendar →",
                link_url="https://example.com/fda-calendar"
            ),
            "timestamp": "5 hours ago",
            "pattern": "volatile",
            "is_yolo": True,
            "border_style": "solid"
        },
        
        # Earnings Signal
        {
            "ticker": "GOOGL",
            "company_name": "Google Post-Earnings",
            "signal_type": SignalType.EARNINGS,
            "priority": SignalPriority.NORMAL,
            "current_price": 178.25,
            "price_change": 13.96,
            "price_change_percent": 8.5,
            "key_stats": [
                KeyStat("+11%", "AH Move", True),
                KeyStat("$185", "Target"),
                KeyStat("5.2M", "AH Vol")
            ],
            "strategy": StrategyInfo(
                title="Post-Earnings Momentum",
                description="Crushed earnings, raised guidance. After-hours up 11%. Buy at open for continuation. Historical 3-day momentum after beats averages +5%.",
                link_text="ER playbook →",
                link_url="https://example.com/earnings-momentum"
            ),
            "timestamp": "After hours",
            "pattern": "momentum",
            "is_yolo": False,
            "border_style": "solid"
        },
        
        # Unusual Options Activity
        {
            "ticker": "AMD",
            "company_name": "Unusual Call Buying",
            "signal_type": SignalType.UNUSUAL_OPTIONS,
            "priority": SignalPriority.WATCH,
            "current_price": 185.40,
            "price_change": 3.85,
            "price_change_percent": 2.1,
            "key_stats": [
                KeyStat("$2.5M", "Premium"),
                KeyStat("10x", "Avg Vol"),
                KeyStat("$200", "Strike")
            ],
            "strategy": StrategyInfo(
                title="Follow the Smart Money",
                description="10,000 Aug $200 calls bought for $2.5M. 10x normal volume. Someone knows something. Follow with smaller position or spreads.",
                link_text="Flow data →",
                link_url="https://example.com/options-flow"
            ),
            "timestamp": "30 min ago",
            "pattern": "momentum",
            "is_yolo": False,
            "border_style": "solid"
        },
        
        # Meme Squeeze Signal
        {
            "ticker": "GME",
            "company_name": "GameStop Gamma Ramp",
            "signal_type": SignalType.MEME_SQUEEZE,
            "priority": SignalPriority.NORMAL,
            "current_price": 45.20,
            "price_change": 11.78,
            "price_change_percent": 35.2,
            "key_stats": [
                KeyStat("140%", "Short %"),
                KeyStat("+420%", "Target", True),
                KeyStat("💎🙌", "Hands")
            ],
            "strategy": StrategyInfo(
                title="Diamond Hands Squeeze Play",
                description="Short interest 140%, cost to borrow 85%. Gamma ramp building. Pure YOLO - lottery ticket only! Not investment advice. Apes together strong! 🚀",
                link_text="Join apes →",
                link_url="https://reddit.com/r/wallstreetbets"
            ),
            "timestamp": "TO THE MOON!",
            "pattern": "volatile",
            "is_yolo": True,
            "border_style": "solid"
        }
    ]
    
    # Initialize renderer
    renderer = SignalRenderer(output_dir="complete_signals")
    
    # Generate all signals
    generated_files = []
    
    for i, signal_data in enumerate(signals_data, 1):
        print(f"🎨 [{i:2d}/10] Rendering {signal_data['ticker']} ({signal_data['signal_type'].name})...")
        
        # Create chart data
        chart_data = generate_chart_data(
            signal_data['ticker'], 
            signal_data['current_price'], 
            signal_data['pattern']
        )
        
        # Update event label based on signal type
        if signal_data['signal_type'] == SignalType.IPO_TODAY:
            chart_data.event_label = f"IPO ${signal_data['current_price']:.0f} → peak"
        elif signal_data['signal_type'] == SignalType.PRE_MARKET:
            chart_data.event_label = "Taiwan news 4AM"
        elif signal_data['signal_type'] == SignalType.FDA_EVENT:
            chart_data.event_label = "FDA 7/28"
        elif signal_data['signal_type'] == SignalType.YOLO_CALLS:
            chart_data.event_label = "Kalshi 75% → 150K"
        else:
            chart_data.event_label = f"Signal @ ${signal_data['current_price']:.2f}"
            
        # Set chart color based on signal type
        chart_colors = {
            SignalType.IPO_TODAY: "#ff4757",
            SignalType.YOLO_CALLS: "#ff00ff",
            SignalType.PRE_MARKET: "#ffd93d",
            SignalType.STOCK_SPLIT: "#3498db",
            SignalType.PUT_SPREAD: "#e74c3c",
            SignalType.CRYPTO_DEFI: "#f7931a",
            SignalType.FDA_EVENT: "#16a085",
            SignalType.EARNINGS: "#95a5a6",
            SignalType.UNUSUAL_OPTIONS: "#d35400",
            SignalType.MEME_SQUEEZE: "#ff00ff"
        }
        chart_data.chart_color = chart_colors.get(signal_data['signal_type'], "#00ff88")
        
        # Create SignalData object
        signal = SignalData(
            ticker=signal_data['ticker'],
            company_name=signal_data['company_name'],
            signal_type=signal_data['signal_type'],
            current_price=signal_data['current_price'],
            price_change=signal_data['price_change'],
            price_change_percent=signal_data['price_change_percent'],
            priority=signal_data['priority'],
            key_stats=signal_data['key_stats'],
            strategy=signal_data['strategy'],
            chart_data=chart_data,
            timestamp=signal_data['timestamp'],
            is_yolo=signal_data['is_yolo'],
            border_style=signal_data['border_style']
        )
        
        # Render signal
        filename = f"{signal.ticker}_{signal.signal_type.name.lower()}.html"
        output_path = renderer.render_signal(signal, filename)
        generated_files.append(output_path)
        
        # Validate file
        if os.path.exists(output_path):
            size = os.path.getsize(output_path)
            print(f"       ✅ Generated {filename} ({size:,} bytes)")
        else:
            print(f"       ❌ Failed to generate {filename}")
    
    # Generate summary
    print(f"\n📋 Summary:")
    print(f"   🎯 Generated {len(generated_files)} signal pages")
    print(f"   📁 Output directory: complete_signals/")
    
    total_size = sum(os.path.getsize(f) for f in generated_files if os.path.exists(f))
    print(f"   💾 Total size: {total_size:,} bytes ({total_size/1024:.1f} KB)")
    
    # List all files
    print(f"\n📄 Generated Files:")
    for file_path in sorted(generated_files):
        if os.path.exists(file_path):
            size = os.path.getsize(file_path)
            filename = os.path.basename(file_path)
            print(f"   📊 {filename:<35} ({size:,} bytes)")
    
    print(f"\n🌐 Open any file in your browser to view the mobile-optimized signal page!")
    print(f"🔗 Example: file://{os.path.abspath('complete_signals/CRCL_ipo_today.html')}")
    
    return generated_files

if __name__ == "__main__":
    generated = create_complete_signal_suite()
    print(f"\n✨ Complete! Generated {len(generated)} professional signal pages.")