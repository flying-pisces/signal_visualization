"""
Signal HTML Rendering Engine
Generates mobile-friendly trading signal HTML pages from market scan data
"""

from dataclasses import dataclass, field
from typing import List, Optional, Dict, Tuple, Literal
from enum import Enum
import json
from datetime import datetime
import os

class SignalType(Enum):
    """Signal types with their associated visual styles"""
    IPO_TODAY = ("ipo-debut", "linear-gradient(135deg, #ff4757, #ff6348)", "#ff4757")
    YOLO_CALLS = ("yolo-play", "linear-gradient(135deg, #ff00ff, #ff4757)", "#ff00ff")
    PRE_MARKET = ("pre-market", "#ffd93d", "#ffd93d")
    STOCK_SPLIT = ("stock-split", "#3498db", "#3498db")
    PUT_SPREAD = ("option-spread", "#e74c3c", "#e74c3c")
    CRYPTO_DEFI = ("crypto-play", "#f7931a", "#f7931a")
    FDA_EVENT = ("fda-event", "#16a085", "#16a085")
    EARNINGS = ("post-market", "#95a5a6", "#95a5a6")
    UNUSUAL_OPTIONS = ("indicator-signal", "#d35400", "#d35400")
    MEME_SQUEEZE = ("yolo-play", "linear-gradient(135deg, #ff00ff, #ff4757)", "#ff00ff")

class SignalPriority(Enum):
    """Signal priority levels"""
    HOT = "🔥 HOT"
    URGENT = "⚡ URGENT"
    NORMAL = ""
    WATCH = "👀 WATCH"

@dataclass
class ChartData:
    """Chart configuration and data"""
    historical_data: List[float]
    prediction_upper: List[float]
    prediction_base: List[float] 
    prediction_lower: List[float]
    event_label: str
    chart_color: str = "#00ff88"
    
@dataclass
class KeyStat:
    """Key statistic display"""
    value: str
    label: str
    is_positive: bool = True
    
@dataclass
class StrategyInfo:
    """Trading strategy information"""
    title: str
    description: str
    link_text: str = "Learn more →"
    link_url: str = "https://example.com/strategy"

@dataclass
class SignalData:
    """Complete signal data from market scan engine"""
    # Basic Info
    ticker: str
    company_name: str
    signal_type: SignalType
    current_price: float
    price_change: float
    price_change_percent: float
    
    # Optional fields with defaults
    priority: SignalPriority = SignalPriority.NORMAL
    key_stats: List[KeyStat] = field(default_factory=list)
    strategy: StrategyInfo = None
    chart_data: ChartData = None
    timestamp: str = "Just now"
    notifications_enabled: bool = True
    is_yolo: bool = False
    has_animation: bool = False
    border_style: Literal["solid", "dashed"] = "solid"
    
class SignalRenderer:
    """Universal rendering engine for trading signals"""
    
    def __init__(self, output_dir: str = "signals"):
        self.output_dir = output_dir
        os.makedirs(output_dir, exist_ok=True)
        
    def render_signal(self, signal: SignalData, filename: str = None) -> str:
        """
        Render a signal to HTML
        
        Args:
            signal: SignalData object with all required information
            filename: Optional output filename (defaults to ticker_signal.html)
            
        Returns:
            Path to generated HTML file
        """
        if not filename:
            filename = f"{signal.ticker.lower()}_{signal.signal_type.name.lower()}.html"
            
        html = self._generate_html(signal)
        
        output_path = os.path.join(self.output_dir, filename)
        with open(output_path, 'w') as f:
            f.write(html)
            
        return output_path
    
    def _generate_html(self, signal: SignalData) -> str:
        """Generate complete HTML for a signal"""
        
        # Get style configuration
        badge_class, card_bg, chart_color = signal.signal_type.value
        
        # Determine card classes
        card_classes = ["signal-card"]
        if signal.is_yolo:
            card_classes.append("yolo")
        if signal.border_style == "dashed":
            card_classes.append("pre-market")
            
        # Generate chart JavaScript
        chart_js = self._generate_chart_js(signal, chart_color)
        
        # Build HTML
        html = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{signal.ticker} - {signal.strategy.title if signal.strategy else signal.signal_type.name}</title>
    <script src="https://cdnjs.cloudflare.com/ajax/libs/Chart.js/4.4.0/chart.umd.js"></script>
    <style>
{self._get_css(signal)}
    </style>
</head>
<body>
    <div class="header">
        <div class="logo">SignalPro</div>
        <a href="../summary.html" class="back-button haptic">
            <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                <path d="M19 12H5M12 19l-7-7 7-7"/>
            </svg>
            Back
        </a>
    </div>
    
    <div class="{' '.join(card_classes)}">
        {self._get_priority_label(signal)}
        <div class="signal-header">
            <div class="ticker-main">
                <span class="ticker">{signal.ticker}</span>
                <span class="strategy-badge {badge_class}">{signal.signal_type.name.replace('_', ' ')}</span>
            </div>
            <div class="company-name">{signal.company_name}</div>
            <div class="price-row">
                <span class="price">${signal.current_price:,.2f}</span>
                <span class="change {'positive' if signal.price_change_percent > 0 else 'negative'}">
                    {'+' if signal.price_change_percent > 0 else ''}{signal.price_change_percent:.1f}%
                </span>
            </div>
        </div>
        
        {self._get_chart_section(signal)}
        
        {self._get_key_stats(signal)}
        
        {self._get_strategy_section(signal)}
        
        <div class="signal-footer">
            <div class="notify-toggle">
                <span>Exit alert</span>
                <div class="toggle {'on' if signal.notifications_enabled else ''} haptic" onclick="toggleNotify(this)">
                    <div class="toggle-knob"></div>
                </div>
            </div>
            <span>{signal.timestamp}</span>
        </div>
    </div>

    <script>
{chart_js}
{self._get_javascript()}
    </script>
</body>
</html>"""
        
        return html
    
    def _get_css(self, signal: SignalData) -> str:
        """Generate CSS styles based on signal type"""
        
        _, card_bg, primary_color = signal.signal_type.value
        
        # Determine if gradient or solid background
        if "gradient" in str(card_bg):
            card_bg_style = f"background: {card_bg};"
        else:
            card_bg_style = f"background: linear-gradient(135deg, #1a1a1a 0%, #2a2a2a 100%);"
            
        yolo_styles = """
        .signal-card.yolo {
            background: linear-gradient(135deg, #1a1a1a 0%, #2d0d2d 100%);
            border-color: #ff00ff;
            animation: yolo-glow 3s ease-in-out infinite;
        }
        
        @keyframes yolo-glow {
            0%, 100% { box-shadow: 0 0 10px rgba(255, 0, 255, 0.3); }
            50% { box-shadow: 0 0 20px rgba(255, 0, 255, 0.5); }
        }""" if signal.is_yolo else ""
        
        pre_market_styles = """
        .signal-card.pre-market {
            border-style: dashed;
            border-color: #ffd93d;
        }""" if signal.border_style == "dashed" else ""
        
        return f"""        * {{
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }}
        
        body {{
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
            background: #000000;
            color: #ffffff;
            padding: 10px;
            max-width: 420px;
            margin: 0 auto;
            min-height: 100vh;
            -webkit-font-smoothing: antialiased;
        }}
        
        /* Header */
        .header {{
            display: flex;
            justify-content: space-between;
            align-items: center;
            padding: 15px 5px;
            margin-bottom: 15px;
        }}
        
        .logo {{
            font-size: 22px;
            font-weight: bold;
            background: linear-gradient(45deg, #00ff88, #00d4ff, #ff00ff);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            display: flex;
            align-items: center;
            gap: 5px;
        }}
        
        .back-button {{
            display: flex;
            align-items: center;
            gap: 5px;
            color: #00ff88;
            text-decoration: none;
            font-size: 14px;
            font-weight: 500;
            transition: opacity 0.3s;
        }}
        
        .back-button:hover {{
            opacity: 0.8;
        }}
        
        /* Signal Card */
        .signal-card {{
            {card_bg_style}
            border-radius: 16px;
            padding: 16px;
            border: 1px solid {primary_color};
            position: relative;
            overflow: hidden;
            animation: fadeIn 0.5s ease;
        }}
        
        {yolo_styles}
        {pre_market_styles}
        
        @keyframes fadeIn {{
            from {{
                opacity: 0;
                transform: translateY(10px);
            }}
            to {{
                opacity: 1;
                transform: translateY(0);
            }}
        }}
        
        .hot-label {{
            position: absolute;
            top: 10px;
            right: 10px;
            background: linear-gradient(135deg, #ff4757, #ff6348);
            color: white;
            font-size: 9px;
            font-weight: bold;
            padding: 3px 8px;
            border-radius: 10px;
            text-transform: uppercase;
            animation: hot-pulse 2s infinite;
        }}
        
        @keyframes hot-pulse {{
            0%, 100% {{ transform: scale(1); }}
            50% {{ transform: scale(1.1); }}
        }}
        
        .signal-header {{
            margin-bottom: 12px;
        }}
        
        .ticker-main {{
            display: flex;
            align-items: center;
            gap: 8px;
            margin-bottom: 4px;
        }}
        
        .ticker {{
            font-size: 20px;
            font-weight: bold;
        }}
        
        .strategy-badge {{
            padding: 4px 10px;
            border-radius: 12px;
            font-size: 10px;
            font-weight: 600;
            text-transform: uppercase;
            letter-spacing: 0.5px;
        }}
        
        /* Strategy Badge Colors */
        .ipo-debut {{ background: linear-gradient(135deg, #ff4757, #ff6348); }}
        .yolo-play {{ 
            background: linear-gradient(135deg, #ff00ff, #ff4757); 
            animation: color-shift 3s infinite;
        }}
        .pre-market {{ background: #ffd93d; color: #000; }}
        .stock-split {{ background: #3498db; }}
        .option-spread {{ background: #e74c3c; }}
        .crypto-play {{ background: #f7931a; color: #000; }}
        .fda-event {{ background: #16a085; }}
        .post-market {{ background: #95a5a6; }}
        .indicator-signal {{ background: #d35400; }}
        
        @keyframes color-shift {{
            0%, 100% {{ filter: hue-rotate(0deg); }}
            50% {{ filter: hue-rotate(30deg); }}
        }}
        
        .company-name {{
            font-size: 12px;
            color: #666;
            margin-bottom: 6px;
        }}
        
        .price-row {{
            display: flex;
            align-items: baseline;
            gap: 8px;
        }}
        
        .price {{
            font-size: 24px;
            font-weight: bold;
        }}
        
        .change {{
            font-size: 14px;
            font-weight: 600;
        }}
        
        .positive {{ color: #00ff88; }}
        .negative {{ color: #ff4757; }}
        
        /* Chart Section */
        .chart-section {{
            height: 100px;
            margin-bottom: 12px;
            position: relative;
            background: rgba(255, 255, 255, 0.02);
            border-radius: 10px;
            padding: 8px;
        }}
        
        .chart-section::after {{
            content: '';
            position: absolute;
            top: 10%;
            left: 50%;
            width: 1px;
            height: 80%;
            background: rgba(255, 255, 255, 0.2);
            border-left: 1px dashed rgba(255, 255, 255, 0.3);
        }}
        
        .event-label {{
            position: absolute;
            top: 8px;
            right: 8px;
            background: rgba(0, 0, 0, 0.8);
            padding: 3px 8px;
            border-radius: 6px;
            font-size: 10px;
            backdrop-filter: blur(10px);
            border: 1px solid rgba(255, 255, 255, 0.1);
            z-index: 10;
        }}
        
        .prediction-indicator {{
            position: absolute;
            bottom: 4px;
            left: 50%;
            transform: translateX(-50%);
            font-size: 9px;
            color: #666;
            letter-spacing: 0.5px;
            text-transform: uppercase;
        }}
        
        /* Key Stats */
        .key-stats {{
            display: grid;
            grid-template-columns: repeat(3, 1fr);
            gap: 8px;
            margin-bottom: 12px;
        }}
        
        .stat {{
            text-align: center;
            padding: 8px 4px;
            background: rgba(255, 255, 255, 0.05);
            border-radius: 8px;
        }}
        
        .stat-value {{
            font-size: 16px;
            font-weight: bold;
            margin-bottom: 2px;
        }}
        
        .stat-label {{
            font-size: 10px;
            color: #666;
            text-transform: uppercase;
        }}
        
        /* Strategy Info */
        .strategy-info {{
            background: rgba(255, 255, 255, 0.03);
            border-radius: 10px;
            padding: 12px;
            margin-bottom: 12px;
            border: 1px solid rgba(255, 255, 255, 0.08);
        }}
        
        .strategy-title {{
            font-size: 13px;
            font-weight: 600;
            margin-bottom: 6px;
            color: #00d4ff;
        }}
        
        .strategy-desc {{
            font-size: 12px;
            line-height: 1.4;
            color: #aaa;
            margin-bottom: 6px;
        }}
        
        .strategy-link {{
            display: inline-flex;
            align-items: center;
            gap: 4px;
            color: #00ff88;
            text-decoration: none;
            font-size: 11px;
            font-weight: 500;
        }}
        
        /* Signal Footer */
        .signal-footer {{
            display: flex;
            justify-content: space-between;
            align-items: center;
            font-size: 11px;
            color: #666;
        }}
        
        .notify-toggle {{
            display: flex;
            align-items: center;
            gap: 6px;
        }}
        
        .toggle {{
            width: 36px;
            height: 20px;
            background: #333;
            border-radius: 10px;
            position: relative;
            cursor: pointer;
            transition: background 0.3s;
        }}
        
        .toggle.on {{
            background: #00ff88;
        }}
        
        .toggle-knob {{
            width: 16px;
            height: 16px;
            background: white;
            border-radius: 50%;
            position: absolute;
            top: 2px;
            left: 2px;
            transition: transform 0.3s;
        }}
        
        .toggle.on .toggle-knob {{
            transform: translateX(16px);
        }}
        
        /* Haptic Feedback */
        .haptic {{
            cursor: pointer;
            -webkit-tap-highlight-color: transparent;
        }}
        
        /* Mobile Optimizations */
        @media (max-width: 375px) {{
            .signal-card {{
                padding: 12px;
            }}
            
            .ticker {{
                font-size: 18px;
            }}
            
            .price {{
                font-size: 22px;
            }}
            
            .key-stats {{
                gap: 6px;
            }}
            
            .stat {{
                padding: 6px 4px;
            }}
            
            .stat-value {{
                font-size: 14px;
            }}
        }}
        
        /* Watch Mode */
        @media (max-width: 200px) {{
            body {{
                padding: 8px;
            }}
            
            .signal-card {{
                padding: 10px;
            }}
            
            .ticker {{
                font-size: 16px;
            }}
            
            .price {{
                font-size: 18px;
            }}
            
            .chart-section {{
                height: 50px;
            }}
            
            .key-stats {{
                display: none;
            }}
            
            .strategy-info {{
                font-size: 10px;
                padding: 8px;
            }}
            
            .strategy-desc {{
                display: none;
            }}
        }}"""
    
    def _get_priority_label(self, signal: SignalData) -> str:
        """Generate priority label HTML if needed"""
        if signal.priority != SignalPriority.NORMAL and signal.priority.value:
            return f'<div class="hot-label">{signal.priority.value}</div>'
        return ""
    
    def _get_chart_section(self, signal: SignalData) -> str:
        """Generate chart section HTML"""
        if not signal.chart_data:
            return ""
            
        return f"""        <div class="chart-section">
            <canvas id="chart-{signal.ticker.lower()}"></canvas>
            <div class="event-label">{signal.chart_data.event_label}</div>
            <div class="prediction-indicator">← now | prediction →</div>
        </div>"""
    
    def _get_key_stats(self, signal: SignalData) -> str:
        """Generate key statistics HTML"""
        if not signal.key_stats:
            return ""
            
        stats_html = ""
        for stat in signal.key_stats[:3]:  # Limit to 3 for mobile layout
            color_class = "positive" if stat.is_positive else "negative" if not stat.is_positive and stat.value.startswith('-') else ""
            stats_html += f"""            <div class="stat">
                <div class="stat-value {color_class}">{stat.value}</div>
                <div class="stat-label">{stat.label}</div>
            </div>
"""
        
        return f"""        <div class="key-stats">
{stats_html}        </div>"""
    
    def _get_strategy_section(self, signal: SignalData) -> str:
        """Generate strategy information HTML"""
        if not signal.strategy:
            return ""
            
        return f"""        <div class="strategy-info">
            <div class="strategy-title">{signal.strategy.title}</div>
            <div class="strategy-desc">
                {signal.strategy.description}
            </div>
            <a href="{signal.strategy.link_url}" class="strategy-link">
                {signal.strategy.link_text}
            </a>
        </div>"""
    
    def _generate_chart_js(self, signal: SignalData, chart_color: str) -> str:
        """Generate Chart.js initialization code"""
        if not signal.chart_data:
            return ""
            
        ticker_lower = signal.ticker.lower()
        
        # Convert data to JavaScript arrays
        historical = json.dumps(signal.chart_data.historical_data)
        upper = json.dumps(signal.chart_data.prediction_upper)
        base = json.dumps(signal.chart_data.prediction_base)
        lower = json.dumps(signal.chart_data.prediction_lower)
        
        return f"""        // Mini chart configuration
        const miniChartOptions = {{
            responsive: true,
            maintainAspectRatio: false,
            plugins: {{
                legend: {{ display: false }},
                tooltip: {{ enabled: false }}
            }},
            scales: {{
                x: {{ 
                    display: false,
                    grid: {{ display: false }}
                }},
                y: {{ 
                    display: false,
                    grid: {{ display: false }}
                }}
            }},
            elements: {{
                point: {{ radius: 0 }},
                line: {{ borderWidth: 2 }}
            }},
            interaction: {{
                intersect: false
            }}
        }};
        
        // Initialize chart with prediction bands
        const chartCtx = document.getElementById('chart-{ticker_lower}')?.getContext('2d');
        if (chartCtx) {{
            const currentPrice = {signal.current_price};
            new Chart(chartCtx, {{
                type: 'line',
                data: {{
                    labels: Array.from({{length: 40}}, (_, i) => i - 20),
                    datasets: [
                        {{
                            label: 'Historical',
                            data: {historical}.concat(Array(20).fill(null)),
                            borderColor: '{chart_color}',
                            backgroundColor: 'transparent',
                            borderWidth: 2,
                            pointRadius: 0,
                            tension: 0.3
                        }},
                        {{
                            label: 'Upper Band',
                            data: Array(20).fill(null).concat({upper}),
                            borderColor: 'rgba(255, 71, 87, 0.3)',
                            borderDash: [5, 5],
                            borderWidth: 1,
                            pointRadius: 0,
                            fill: '+1',
                            backgroundColor: 'rgba(255, 71, 87, 0.1)'
                        }},
                        {{
                            label: 'Base Case',
                            data: Array(20).fill(null).concat({base}),
                            borderColor: '{chart_color}',
                            borderDash: [5, 5],
                            borderWidth: 2,
                            pointRadius: 0
                        }},
                        {{
                            label: 'Lower Band',
                            data: Array(20).fill(null).concat({lower}),
                            borderColor: 'rgba(255, 71, 87, 0.3)',
                            borderDash: [5, 5],
                            borderWidth: 1,
                            pointRadius: 0,
                            fill: false
                        }}
                    ]
                }},
                options: miniChartOptions
            }});
        }}"""
    
    def _get_javascript(self) -> str:
        """Generate common JavaScript functions"""
        return """        
        // Toggle notification
        function toggleNotify(element) {
            element.classList.toggle('on');
            vibrate();
        }
        
        // Haptic feedback
        function vibrate(duration = 10) {
            if ('vibrate' in navigator) {
                navigator.vibrate(duration);
            }
        }
        
        // Real-time price updates
        function updatePrice() {
            const priceEl = document.querySelector('.price');
            const changeEl = document.querySelector('.change');
            if (priceEl) {
                const current = parseFloat(priceEl.textContent.replace('$', '').replace(',', ''));
                const change = (Math.random() - 0.5) * 0.02 * current;
                const newPrice = current + change;
                
                if (current > 1000) {
                    priceEl.textContent = '$' + newPrice.toLocaleString('en-US', { minimumFractionDigits: 2, maximumFractionDigits: 2 });
                } else {
                    priceEl.textContent = '$' + newPrice.toFixed(2);
                }
                
                if (changeEl) {
                    const percent = ((Math.random() - 0.4) * 5).toFixed(1);
                    changeEl.textContent = (percent > 0 ? '+' : '') + percent + '%';
                    changeEl.className = 'change ' + (percent > 0 ? 'positive' : 'negative');
                }
            }
        }
        
        // Initialize
        document.addEventListener('DOMContentLoaded', () => {
            // Start price updates
            setInterval(updatePrice, 5000);
            
            // Add haptic to all interactive elements
            document.querySelectorAll('.haptic').forEach(el => {
                el.addEventListener('click', () => vibrate());
            });
        });
        
        // PWA Support
        if ('serviceWorker' in navigator) {
            navigator.serviceWorker.register('/sw.js').catch(() => {});
        }"""

def generate_chart_data(ticker: str, current_price: float, pattern: str = "momentum") -> ChartData:
    """
    Helper function to generate realistic chart data based on pattern
    
    Patterns:
    - momentum: Strong upward trend
    - volatile: High volatility swings
    - breakout: Consolidation then breakout
    - decline: Downward trend
    """
    import math
    import random
    
    # Generate historical data based on pattern
    historical = []
    
    if pattern == "momentum":
        # Strong upward trend
        base = current_price * 0.8
        for i in range(20):
            if i < 15:
                historical.append(base + (current_price - base) * (i / 15) + random.uniform(-2, 2))
            else:
                historical.append(current_price + random.uniform(-3, 3))
                
    elif pattern == "volatile":
        # High volatility
        for i in range(20):
            historical.append(current_price + math.sin(i * 0.5) * current_price * 0.1 + random.uniform(-5, 5))
            
    elif pattern == "breakout":
        # Consolidation then breakout
        for i in range(20):
            if i < 15:
                historical.append(current_price * 0.9 + random.uniform(-2, 2))
            else:
                historical.append(current_price * 0.9 + (current_price - current_price * 0.9) * ((i - 15) / 5))
                
    else:  # decline
        # Downward trend
        base = current_price * 1.2
        for i in range(20):
            historical.append(base - (base - current_price) * (i / 20) + random.uniform(-2, 2))
    
    # Generate prediction bands
    prediction_upper = []
    prediction_base = []
    prediction_lower = []
    
    for i in range(20):
        progress = i / 20
        
        # Upper band (bullish scenario)
        prediction_upper.append(current_price + current_price * 0.3 * progress + math.pow(i, 1.1))
        
        # Base case (moderate growth)
        prediction_base.append(current_price + current_price * 0.1 * progress)
        
        # Lower band (bearish scenario)
        prediction_lower.append(current_price - current_price * 0.2 * progress - math.pow(i, 1.05))
    
    return ChartData(
        historical_data=historical,
        prediction_upper=prediction_upper,
        prediction_base=prediction_base,
        prediction_lower=prediction_lower,
        event_label=f"Signal @ ${current_price:.2f}",
        chart_color="#00ff88"
    )

def demo_signal_renderer():
    """Demo function to show signal renderer in action"""
    print("🎯 Signal Renderer Demo")
    print("=" * 40)
    
    # Create demo signal
    demo_signal = SignalData(
        ticker="DEMO",
        company_name="Demo Company Inc",
        signal_type=SignalType.IPO_TODAY,
        current_price=50.00,
        price_change=15.00,
        price_change_percent=42.9,
        priority=SignalPriority.HOT,
        key_stats=[
            KeyStat("150%", "Day High", True),
            KeyStat("$2.5B", "Market Cap"),
            KeyStat("25M", "Volume")
        ],
        strategy=StrategyInfo(
            title="Demo IPO Play",
            description="This is a demonstration of the signal rendering engine. In production, this data would come from your market scan engine.",
            link_text="Demo →",
            link_url="https://example.com/demo"
        ),
        chart_data=generate_chart_data("DEMO", 50.00, "momentum"),
        timestamp="Demo",
        is_yolo=False
    )
    
    # Render signal
    renderer = SignalRenderer(output_dir="demo_output")
    output_path = renderer.render_signal(demo_signal, "demo_signal.html")
    
    print(f"✅ Demo signal rendered!")
    print(f"📄 Output: {output_path}")
    print(f"📊 Signal: {demo_signal.ticker} - {demo_signal.company_name}")
    print(f"💰 Price: ${demo_signal.current_price} (+{demo_signal.price_change_percent}%)")
    
    # Check file
    if os.path.exists(output_path):
        size = os.path.getsize(output_path)
        print(f"📁 File size: {size:,} bytes")
        print(f"🌐 Open in browser: file://{os.path.abspath(output_path)}")
    else:
        print("❌ Error: File not generated")
    
    print("\n💡 To use with real data, see example_usage.py")

if __name__ == "__main__":
    # Run demo when script is executed directly
    demo_signal_renderer()