#!/usr/bin/env python3
"""
Test GUI functionality without launching the full interface
"""

from signal_renderer import (
    SignalRenderer, SignalData, SignalType, SignalPriority, 
    ChartData, KeyStat, StrategyInfo, generate_chart_data
)
import os

def test_gui_data_flow():
    """Test the same data flow the GUI uses"""
    print("🧪 Testing GUI Data Flow")
    print("=" * 50)
    
    # Simulate GUI form data (same as GUI would collect)
    form_data = {
        'ticker': 'TSLA',
        'company_name': 'Tesla Inc',
        'signal_type': 'EARNINGS',
        'priority': 'HOT', 
        'current_price': 248.50,
        'price_change': 26.85,
        'price_change_percent': 12.3,
        'timestamp': 'After hours',
        'is_yolo': False,
        'border_style': 'solid',
        'key_stats': [
            {'value': '+15%', 'label': 'AH Move', 'is_positive': True},
            {'value': '$275', 'label': 'Target', 'is_positive': True}, 
            {'value': '8.5M', 'label': 'AH Vol', 'is_positive': True}
        ],
        'strategy': {
            'title': 'Post-Earnings Rocket',
            'description': 'Crushed delivery numbers and FSD progress update. After-hours up 15% on massive volume. Buy at open for continuation. Historical momentum avg is +8% over 3 days.',
            'link_text': 'Earnings playbook →',
            'link_url': 'https://example.com/tesla-earnings'
        },
        'chart_pattern': 'momentum',
        'event_label': 'Q4 delivery beat'
    }
    
    print(f"📊 Form Data Collected:")
    print(f"   Ticker: {form_data['ticker']}")
    print(f"   Signal: {form_data['signal_type']}")
    print(f"   Price: ${form_data['current_price']} ({form_data['price_change_percent']:+.1f}%)")
    print(f"   Stats: {len(form_data['key_stats'])} items")
    
    try:
        # Convert form data to SignalData (same as GUI does)
        key_stats = [
            KeyStat(stat['value'], stat['label'], stat['is_positive'])
            for stat in form_data['key_stats']
        ]
        
        strategy = StrategyInfo(
            title=form_data['strategy']['title'],
            description=form_data['strategy']['description'],
            link_text=form_data['strategy']['link_text'],
            link_url=form_data['strategy']['link_url']
        )
        
        chart_data = generate_chart_data(
            form_data['ticker'], 
            form_data['current_price'], 
            form_data['chart_pattern']
        )
        chart_data.event_label = form_data['event_label']
        
        signal_data = SignalData(
            ticker=form_data['ticker'],
            company_name=form_data['company_name'],
            signal_type=SignalType[form_data['signal_type']],
            current_price=form_data['current_price'],
            price_change=form_data['price_change'],
            price_change_percent=form_data['price_change_percent'],
            priority=SignalPriority[form_data['priority']],
            key_stats=key_stats,
            strategy=strategy,
            chart_data=chart_data,
            timestamp=form_data['timestamp'],
            is_yolo=form_data['is_yolo'],
            border_style=form_data['border_style']
        )
        
        print(f"✅ SignalData object created successfully")
        
        # Generate HTML (same as GUI does)
        renderer = SignalRenderer(output_dir="gui_test_output")
        filename = "TSLA_earnings_gui_test.html"
        output_path = renderer.render_signal(signal_data, filename)
        
        if os.path.exists(output_path):
            file_size = os.path.getsize(output_path)
            print(f"✅ HTML generated: {output_path}")
            print(f"📁 File size: {file_size:,} bytes")
            print(f"🌐 Browser: file://{os.path.abspath(output_path)}")
            return True
        else:
            print(f"❌ HTML generation failed")
            return False
            
    except Exception as e:
        print(f"❌ Error: {e}")
        import traceback
        traceback.print_exc()
        return False

def create_sample_signals():
    """Create multiple sample signals to demonstrate GUI capabilities"""
    print("\n🎨 Creating Sample Signal Gallery")
    print("=" * 50)
    
    samples = [
        {
            'ticker': 'NVDA', 'company_name': 'Nvidia Corporation', 'signal_type': 'PRE_MARKET',
            'price': 1125.50, 'change_pct': 5.2, 'priority': 'NORMAL', 'pattern': 'breakout',
            'title': 'Pre-Market Gap & Go', 'border': 'dashed'
        },
        {
            'ticker': 'BTC', 'company_name': 'Bitcoin Moonshot', 'signal_type': 'YOLO_CALLS',
            'price': 105456.00, 'change_pct': 3.8, 'priority': 'NORMAL', 'pattern': 'momentum',
            'title': 'Dec 150K Call Options', 'border': 'solid', 'yolo': True
        },
        {
            'ticker': 'SAVA', 'company_name': 'Cassava Sciences', 'signal_type': 'FDA_EVENT',
            'price': 42.15, 'change_pct': 12.3, 'priority': 'URGENT', 'pattern': 'volatile',
            'title': 'Binary FDA Event - YOLO!', 'border': 'solid', 'yolo': True
        }
    ]
    
    renderer = SignalRenderer(output_dir="gui_sample_gallery")
    generated = []
    
    for i, sample in enumerate(samples, 1):
        try:
            # Quick signal creation
            signal_data = SignalData(
                ticker=sample['ticker'],
                company_name=sample['company_name'],
                signal_type=SignalType[sample['signal_type']],
                current_price=sample['price'],
                price_change=sample['price'] * (sample['change_pct'] / 100),
                price_change_percent=sample['change_pct'],
                priority=SignalPriority[sample['priority']],
                timestamp='GUI Sample',
                is_yolo=sample.get('yolo', False),
                border_style=sample['border']
            )
            
            filename = f"{sample['ticker']}_{sample['signal_type'].lower()}_sample.html"
            output_path = renderer.render_signal(signal_data, filename)
            
            if os.path.exists(output_path):
                size = os.path.getsize(output_path)
                print(f"[{i}/3] ✅ {sample['ticker']} ({sample['signal_type']}) - {size:,} bytes")
                generated.append(output_path)
            else:
                print(f"[{i}/3] ❌ {sample['ticker']} - generation failed")
                
        except Exception as e:
            print(f"[{i}/3] ❌ {sample['ticker']} - error: {e}")
    
    print(f"\n🎉 Generated {len(generated)}/3 sample signals")
    return generated

if __name__ == "__main__":
    print("🎯 GUI Functionality Test")
    print("=" * 60)
    
    # Test basic data flow
    success = test_gui_data_flow()
    
    if success:
        # Create sample gallery
        samples = create_sample_signals()
        
        print(f"\n📋 Summary:")
        print(f"✅ GUI data flow: Working")
        print(f"✅ HTML generation: Working") 
        print(f"✅ Sample gallery: {len(samples)} signals created")
        print(f"\n💡 The GUI is ready to use!")
        print(f"🚀 Launch with: python signal_gui.py")
        
    else:
        print(f"\n❌ GUI functionality test failed")
        print(f"🔧 Please check the error messages above")