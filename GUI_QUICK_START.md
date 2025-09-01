# 🎯 SignalPro GUI Quick Start Guide

## Launch the GUI

```bash
python signal_gui.py
```

## Complete Step-by-Step Walkthrough

### Tab 1: Basic Info ✅
**Required fields (marked with *):**
- **Ticker Symbol**: Stock/crypto symbol (e.g., AAPL, TSLA, BTC)
- **Company Name**: Full company name (e.g., Apple Inc, Tesla Inc)
- **Signal Type**: Choose from 10 types:
  - `IPO_TODAY` - New IPO debuts 
  - `YOLO_CALLS` - High-risk options plays
  - `PRE_MARKET` - Pre-market movers
  - `STOCK_SPLIT` - Split announcements
  - `PUT_SPREAD` - Credit spreads
  - `CRYPTO_DEFI` - Crypto/DeFi plays
  - `FDA_EVENT` - Biotech catalysts
  - `EARNINGS` - Earnings momentum
  - `UNUSUAL_OPTIONS` - Options flow
  - `MEME_SQUEEZE` - Squeeze plays

**Optional fields:**
- **Priority**: NORMAL, HOT (🔥), URGENT (⚡), WATCH (👀)
- **Timestamp**: e.g., "15 min ago", "Pre-market", "After hours"

### Tab 2: Price Data 💰
**Required fields:**
- **Current Price**: Current stock price in dollars
- **Price Change %**: Percentage change (positive/negative)

**Optional:**
- **Price Change $**: Dollar amount change
- **Auto-Calculate**: Button to calculate % from price and change
- **YOLO Style**: Enable purple glow effects
- **Border Style**: solid or dashed (dashed for pre-market)

### Tab 3: Key Stats 📊
**Create exactly 3 statistics for mobile layout:**

Each stat needs:
- **Value**: The number/percentage (e.g., "$185", "15%", "2.5M")
- **Label**: What it represents (e.g., "Target", "Volume", "IV")
- **Positive**: Checkbox for green/red coloring

**Examples by signal type:**
- **IPO**: `["223%", "Day 1 High"]` | `["$6.8B", "Valuation"]` | `["46M", "Volume"]`
- **Options**: `["$3.20", "Credit"]` | `["72%", "PoP"]` | `["21d", "DTE"]`
- **Crypto**: `["5.2%", "APY"]` | `["$4.2K", "Target"]` | `["85", "RSI"]`
- **FDA**: `["+180%", "If Pass"]` | `["-65%", "If Fail"]` | `["220%", "IV"]`

### Tab 4: Strategy 🧠
**Required fields:**
- **Strategy Title**: Brief strategy name (e.g., "Hot IPO Momentum Play")
- **Strategy Description**: Detailed analysis and trading plan

**Optional:**
- **Link Text**: Text for the strategy link (e.g., "IPO playbook →")
- **Link URL**: URL for more information

**Example descriptions by type:**
- **IPO**: "Stablecoin leader 3x'd on debut. ARK bought $150M. Watch for dip to $60-65 for entry."
- **YOLO**: "Kalshi shows 75% odds of 150K by Q4. High risk, high reward - only risk what you can lose!"
- **Pre-Market**: "TSMC production boost news. Pre-market up 6.8% on heavy volume. Buy at 9:28-9:30."
- **FDA**: "Alzheimer's drug PDUFA date 7/28. Binary event - ultra high risk, total loss possible."

### Tab 5: Chart Data 📈
**Chart Pattern** (auto-generates realistic data):
- `momentum` - Strong upward trend
- `volatile` - High volatility swings  
- `breakout` - Consolidation then breakout
- `decline` - Downward trend

**Event Label**: Description of the catalyst
- Examples: "IPO $31 → $103 peak", "Kalshi 75% → 150K", "FDA 7/28"

### Tab 6: Generate 🚀
1. **Preview Data**: Check all your inputs before generating
2. **Generate Signal HTML**: Creates the mobile-optimized page
3. **View Output**: See generation results and file path
4. **Open in Browser**: Direct link to view your signal

## 📱 Generated Features

Every signal gets:
- ✅ **Mobile-responsive design** (phones, tablets, watches)
- ✅ **Interactive charts** with prediction bands
- ✅ **Real-time price updates** (every 5 seconds)
- ✅ **Haptic feedback** on mobile devices
- ✅ **PWA support** for app-like experience
- ✅ **Professional styling** based on signal type

## 🎨 Visual Styles by Signal Type

- **IPO_TODAY**: Red gradient with hot pulse animation
- **YOLO_CALLS**: Purple gradient with glow (if YOLO enabled)
- **PRE_MARKET**: Yellow badge with dashed border
- **STOCK_SPLIT**: Blue professional styling
- **PUT_SPREAD**: Red professional styling
- **CRYPTO_DEFI**: Orange crypto-themed
- **FDA_EVENT**: Teal biotech styling
- **EARNINGS**: Gray professional
- **UNUSUAL_OPTIONS**: Dark orange flow theme
- **MEME_SQUEEZE**: Purple with diamond hands

## 🚀 Complete Example Walkthrough

**Let's create a Tesla earnings signal:**

1. **Basic Info**:
   - Ticker: `TSLA`
   - Company: `Tesla Inc`
   - Signal Type: `EARNINGS`
   - Priority: `HOT`
   - Timestamp: `After hours`

2. **Price Data**:
   - Current Price: `248.50`
   - Price Change %: `12.3`
   - YOLO Style: ❌ (unchecked)
   - Border: `solid`

3. **Key Stats**:
   - Stat 1: `+15%` | `AH Move` | ✅ Positive
   - Stat 2: `$275` | `Target` | ✅ Positive  
   - Stat 3: `8.5M` | `AH Vol` | ✅ Positive

4. **Strategy**:
   - Title: `Post-Earnings Rocket`
   - Description: `Crushed delivery numbers and FSD progress update. After-hours up 15% on massive volume. Buy at open for continuation. Historical momentum avg is +8% over 3 days.`
   - Link: `Earnings playbook →`

5. **Chart Data**:
   - Pattern: `momentum`
   - Event Label: `Q4 delivery beat`

6. **Generate**: Click "🚀 Generate Signal HTML"

**Result**: Professional mobile-optimized Tesla earnings signal page!

## 💡 Pro Tips

1. **Use realistic data** - The GUI validates inputs and provides helpful examples
2. **Preview first** - Always use "Preview Data" before generating
3. **Mobile-first** - Remember these are designed for mobile trading
4. **Signal-specific styling** - Each signal type has unique visual treatments
5. **Save variations** - Generate multiple versions with different data
6. **Test on mobile** - Open generated files on your phone to see mobile features

## 📁 Output Location

Generated files are saved to:
```
gui_generated/
├── TSLA_earnings.html
├── AAPL_ipo_today.html
└── ... (your generated signals)
```

## 🌐 Browser Testing

Open generated HTML files in any modern browser:
- ✅ Chrome/Safari/Firefox (desktop)
- ✅ Mobile Safari (iPhone)
- ✅ Chrome Mobile (Android)
- ✅ All responsive breakpoints

The GUI makes creating professional trading signals as easy as filling out a form! 🎯