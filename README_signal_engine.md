# Signal Rendering Engine

A universal HTML rendering engine that generates mobile-friendly trading signal pages from market scan data feeds.

## Architecture Overview

```
Market Scan Engine → Signal Renderer → Mobile HTML Pages
     (Data)           (Processing)        (Output)
```

### 1. Market Scan Engine (Input)
The engine expects data from various market scanning sources:

- **News APIs**: IPO announcements, FDA calendars, earnings dates
- **Market Data APIs**: Real-time prices, volume, options flow  
- **Analysis Engine**: Sentiment analysis, technical indicators, popularity metrics

### 2. Signal Renderer (Processing)
Universal rendering engine that:

- Processes structured signal data
- Applies mobile-optimized styling based on signal type
- Generates prediction charts with historical + forecast bands
- Creates responsive HTML with haptic feedback

### 3. HTML Output (Mobile-Optimized)
Each generated page includes:

- **Responsive design**: Works on phones, tablets, smartwatches
- **Real-time updates**: Live price changes every 5 seconds
- **Interactive charts**: Prediction bands showing bull/bear scenarios  
- **Haptic feedback**: Vibration on mobile devices
- **PWA support**: Offline caching, app-like experience

## Signal Types Supported

| Signal Type | Visual Style | Use Case |
|-------------|-------------|----------|
| `IPO_TODAY` | Red gradient, hot pulse | New IPO debuts |
| `YOLO_CALLS` | Purple gradient, glow animation | High-risk options plays |
| `PRE_MARKET` | Yellow dashed border | Pre-market movers |
| `STOCK_SPLIT` | Blue solid | Stock split announcements |
| `PUT_SPREAD` | Red solid | Options credit spreads |
| `CRYPTO_DEFI` | Orange | Crypto/DeFi plays |
| `FDA_EVENT` | Teal | Biotech FDA catalysts |
| `EARNINGS` | Gray | Earnings momentum |
| `UNUSUAL_OPTIONS` | Dark orange | Unusual options flow |
| `MEME_SQUEEZE` | Purple animated | Meme stock squeezes |

## Data Model

### SignalData Structure
```python
@dataclass
class SignalData:
    # Basic Info
    ticker: str              # "CRCL"
    company_name: str        # "Circle Internet Group"
    signal_type: SignalType  # SignalType.IPO_TODAY
    priority: SignalPriority # SignalPriority.HOT
    
    # Price Data  
    current_price: float     # 69.00
    price_change: float      # 38.00
    price_change_percent: float # 122.6
    
    # Key Statistics (3 items for mobile)
    key_stats: List[KeyStat]
    
    # Strategy Information
    strategy: StrategyInfo
    
    # Chart Data with Predictions
    chart_data: ChartData
    
    # Metadata
    timestamp: str
    notifications_enabled: bool
```

### Example Market Scan Feed
```python
# IPO Signal Example
crcl_signal = SignalData(
    ticker="CRCL",
    company_name="Circle Internet Group", 
    signal_type=SignalType.IPO_TODAY,
    priority=SignalPriority.HOT,
    
    current_price=69.00,
    price_change_percent=122.6,
    
    key_stats=[
        KeyStat("223%", "Day 1 High", True),
        KeyStat("$6.8B", "Valuation"),
        KeyStat("46M", "Volume")
    ],
    
    strategy=StrategyInfo(
        title="Hot IPO Momentum Play",
        description="Stablecoin leader 3x'd on debut. ARK bought $150M. Watch for dip to $60-65 for entry.",
        link_url="https://example.com/ipo-strategy"
    ),
    
    chart_data=generate_chart_data("CRCL", 69.00, "breakout")
)
```

## Usage

### Basic Usage
```python
from signal_renderer import SignalRenderer, SignalData, SignalType

# Initialize renderer
renderer = SignalRenderer(output_dir="signals")

# Create signal data (from market scan feed)
signal = SignalData(
    ticker="CRCL",
    company_name="Circle Internet Group",
    signal_type=SignalType.IPO_TODAY,
    current_price=69.00,
    price_change_percent=122.6
)

# Render to HTML
output_path = renderer.render_signal(signal)
print(f"Generated: {output_path}")
```

### Batch Processing
```python
# Process multiple signals from market scan
signals = get_market_scan_signals()  # Your market scan feed

for signal in signals:
    renderer.render_signal(signal)
```

### Integration with Market APIs

#### News API Integration
```python
def create_ipo_signal(ticker, news_data):
    """Create IPO signal from news API data"""
    return SignalData(
        ticker=ticker,
        company_name=news_data['company_name'],
        signal_type=SignalType.IPO_TODAY,
        current_price=news_data['current_price'],
        strategy=StrategyInfo(
            title=f"IPO Momentum Play",
            description=news_data['analysis_summary']
        )
    )

# Usage with news feed
ipo_news = news_api.get_ipo_announcements()
for news in ipo_news:
    signal = create_ipo_signal(news['ticker'], news)
    renderer.render_signal(signal)
```

#### Options Flow Integration  
```python
def create_unusual_options_signal(ticker, flow_data):
    """Create signal from unusual options activity"""
    return SignalData(
        ticker=ticker,
        signal_type=SignalType.UNUSUAL_OPTIONS,
        key_stats=[
            KeyStat(f"${flow_data['premium']/1000000:.1f}M", "Premium"),
            KeyStat(f"{flow_data['volume_ratio']:.0f}x", "Avg Vol"),
            KeyStat(f"${flow_data['strike']}", "Strike")
        ]
    )

# Usage with options flow data
unusual_flow = options_api.get_unusual_activity()
for flow in unusual_flow:
    signal = create_unusual_options_signal(flow['ticker'], flow)
    renderer.render_signal(signal)
```

## Mobile Features

### Responsive Breakpoints
- **Desktop**: Full layout with all elements
- **Mobile (≤375px)**: Condensed layout, smaller fonts
- **Watch (≤200px)**: Minimal layout, essential info only

### Interactive Elements
- **Haptic feedback**: Vibration on button presses
- **Real-time updates**: Price changes every 5 seconds  
- **Smooth animations**: Fade-in effects, pulse animations
- **Touch optimization**: Large tap targets, swipe gestures

### Performance Optimizations
- **Lightweight CSS**: Minimal external dependencies
- **Efficient JavaScript**: Event delegation, debounced updates
- **PWA ready**: Service worker support, offline caching
- **Fast rendering**: Template-based generation

## Chart System

### Prediction Bands
Each chart shows:
- **Historical data**: Solid line (past 20 periods)
- **Base case**: Dashed line (expected path)  
- **Bull scenario**: Upper band (optimistic)
- **Bear scenario**: Lower band (pessimistic)

### Chart Patterns
Automatic pattern generation based on signal type:
- **Momentum**: Strong upward trend  
- **Breakout**: Consolidation → breakout
- **Volatile**: High volatility swings
- **Decline**: Downward trend

## File Structure

```
signal_visualization/
├── signal_renderer.py      # Main rendering engine
├── example_usage.py        # Usage examples
├── generated_signals/      # Output directory
│   ├── crcl_ipo_today.html
│   ├── btc_yolo_calls.html
│   └── signals_summary.json
└── signals/                # Original templates
    ├── IPO_today.html
    ├── Yolo_calls.html  
    └── ...
```

## Deployment

### Production Integration
1. **Connect APIs**: News feeds, market data, options flow
2. **Add Caching**: Redis for real-time data caching
3. **Scale Rendering**: Queue system for batch processing  
4. **Mobile Deploy**: CDN for fast global delivery

### Example Production Pipeline
```python
# Market scan pipeline
def production_signal_pipeline():
    # 1. Scan multiple data sources
    news_signals = scan_news_apis()
    options_signals = scan_options_flow() 
    premarket_signals = scan_premarket_data()
    
    # 2. Analyze and classify
    analyzed_signals = analysis_engine.classify(
        news_signals + options_signals + premarket_signals
    )
    
    # 3. Render to HTML
    renderer = SignalRenderer(output_dir="production_signals")
    for signal in analyzed_signals:
        renderer.render_signal(signal)
        
    # 4. Deploy to CDN
    deploy_to_cdn("production_signals/")
```

This architecture provides a complete solution for transforming market scan data into mobile-optimized trading signal pages, ready for production deployment.