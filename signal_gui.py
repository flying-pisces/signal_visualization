#!/usr/bin/env python3
"""
Signal Generator GUI - Interactive tool for creating trading signal HTML pages
"""

import tkinter as tk
from tkinter import ttk, messagebox, filedialog, scrolledtext
import os
from signal_renderer import (
    SignalRenderer, SignalData, SignalType, SignalPriority, 
    ChartData, KeyStat, StrategyInfo, generate_chart_data
)

class SignalGeneratorGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("SignalPro - Trading Signal Generator")
        self.root.geometry("800x900")
        self.root.configure(bg='#1a1a1a')
        
        # Configure style
        style = ttk.Style()
        style.theme_use('clam')
        
        # Configure colors for dark theme
        style.configure('TLabel', foreground='white', background='#1a1a1a')
        style.configure('TFrame', background='#1a1a1a')
        style.configure('TNotebook', background='#2a2a2a')
        style.configure('TNotebook.Tab', background='#2a2a2a', foreground='white')
        style.map('TNotebook.Tab', background=[('selected', '#00ff88')])
        
        self.renderer = SignalRenderer(output_dir="gui_generated")
        self.create_widgets()
        
    def create_widgets(self):
        # Main title
        title_frame = tk.Frame(self.root, bg='#1a1a1a')
        title_frame.pack(pady=10)
        
        title_label = tk.Label(
            title_frame,
            text="🎯 SignalPro Signal Generator",
            font=('Arial', 18, 'bold'),
            bg='#1a1a1a',
            fg='#00ff88'
        )
        title_label.pack()
        
        subtitle_label = tk.Label(
            title_frame,
            text="Create mobile-optimized trading signal HTML pages",
            font=('Arial', 10),
            bg='#1a1a1a',
            fg='#aaa'
        )
        subtitle_label.pack()
        
        # Create notebook for sections
        self.notebook = ttk.Notebook(self.root)
        self.notebook.pack(expand=True, fill='both', padx=10, pady=5)
        
        # Create tabs
        self.create_basic_info_tab()
        self.create_price_data_tab()
        self.create_key_stats_tab()
        self.create_strategy_tab()
        self.create_chart_tab()
        self.create_generate_tab()
        
    def create_basic_info_tab(self):
        frame = tk.Frame(self.notebook, bg='#2a2a2a')
        self.notebook.add(frame, text="Basic Info")
        
        # Create scrollable frame
        canvas = tk.Canvas(frame, bg='#2a2a2a')
        scrollbar = ttk.Scrollbar(frame, orient="vertical", command=canvas.yview)
        scrollable_frame = tk.Frame(canvas, bg='#2a2a2a')
        
        scrollable_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )
        
        canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)
        
        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")
        
        # Basic info fields
        row = 0
        
        # Ticker
        tk.Label(scrollable_frame, text="Ticker Symbol *", font=('Arial', 11, 'bold'), 
                bg='#2a2a2a', fg='white').grid(row=row, column=0, sticky='w', padx=10, pady=5)
        self.ticker_var = tk.StringVar(value="AAPL")
        tk.Entry(scrollable_frame, textvariable=self.ticker_var, width=20, 
                font=('Arial', 11), bg='#3a3a3a', fg='white').grid(row=row, column=1, sticky='w', padx=10, pady=5)
        tk.Label(scrollable_frame, text="e.g., AAPL, BTC, TSLA", font=('Arial', 9), 
                bg='#2a2a2a', fg='#888').grid(row=row, column=2, sticky='w', padx=5, pady=5)
        
        row += 1
        
        # Company Name
        tk.Label(scrollable_frame, text="Company Name *", font=('Arial', 11, 'bold'), 
                bg='#2a2a2a', fg='white').grid(row=row, column=0, sticky='w', padx=10, pady=5)
        self.company_var = tk.StringVar(value="Apple Inc")
        tk.Entry(scrollable_frame, textvariable=self.company_var, width=40, 
                font=('Arial', 11), bg='#3a3a3a', fg='white').grid(row=row, column=1, columnspan=2, sticky='w', padx=10, pady=5)
        
        row += 1
        
        # Signal Type
        tk.Label(scrollable_frame, text="Signal Type *", font=('Arial', 11, 'bold'), 
                bg='#2a2a2a', fg='white').grid(row=row, column=0, sticky='w', padx=10, pady=5)
        self.signal_type_var = tk.StringVar(value="EARNINGS")
        signal_combo = ttk.Combobox(scrollable_frame, textvariable=self.signal_type_var, width=25,
                                   values=[st.name for st in SignalType])
        signal_combo.grid(row=row, column=1, sticky='w', padx=10, pady=5)
        
        row += 1
        
        # Signal Type descriptions
        descriptions = {
            "IPO_TODAY": "New IPO debuts and momentum plays",
            "YOLO_CALLS": "High-risk, high-reward options plays",
            "PRE_MARKET": "Pre-market movers and gap plays",
            "STOCK_SPLIT": "Stock split announcements",
            "PUT_SPREAD": "Options credit spreads",
            "CRYPTO_DEFI": "Crypto and DeFi plays",
            "FDA_EVENT": "Biotech FDA catalysts",
            "EARNINGS": "Earnings momentum plays",
            "UNUSUAL_OPTIONS": "Unusual options flow",
            "MEME_SQUEEZE": "Meme stock squeeze plays"
        }
        
        desc_text = scrolledtext.ScrolledText(scrollable_frame, width=70, height=8, 
                                            bg='#3a3a3a', fg='#aaa', font=('Arial', 9))
        desc_text.grid(row=row, column=0, columnspan=3, padx=10, pady=5)
        
        desc_content = "Signal Type Descriptions:\n\n"
        for signal_type, desc in descriptions.items():
            desc_content += f"• {signal_type}: {desc}\n"
        
        desc_text.insert('1.0', desc_content)
        desc_text.config(state='disabled')
        
        row += 1
        
        # Priority
        tk.Label(scrollable_frame, text="Priority Level", font=('Arial', 11, 'bold'), 
                bg='#2a2a2a', fg='white').grid(row=row, column=0, sticky='w', padx=10, pady=5)
        self.priority_var = tk.StringVar(value="NORMAL")
        priority_combo = ttk.Combobox(scrollable_frame, textvariable=self.priority_var, width=15,
                                     values=[p.name for p in SignalPriority])
        priority_combo.grid(row=row, column=1, sticky='w', padx=10, pady=5)
        tk.Label(scrollable_frame, text="HOT = 🔥, URGENT = ⚡, WATCH = 👀", font=('Arial', 9), 
                bg='#2a2a2a', fg='#888').grid(row=row, column=2, sticky='w', padx=5, pady=5)
        
        row += 1
        
        # Timestamp
        tk.Label(scrollable_frame, text="Timestamp", font=('Arial', 11, 'bold'), 
                bg='#2a2a2a', fg='white').grid(row=row, column=0, sticky='w', padx=10, pady=5)
        self.timestamp_var = tk.StringVar(value="Just now")
        tk.Entry(scrollable_frame, textvariable=self.timestamp_var, width=20, 
                font=('Arial', 11), bg='#3a3a3a', fg='white').grid(row=row, column=1, sticky='w', padx=10, pady=5)
        tk.Label(scrollable_frame, text="e.g., '15 min ago', 'Pre-market', 'After hours'", font=('Arial', 9), 
                bg='#2a2a2a', fg='#888').grid(row=row, column=2, sticky='w', padx=5, pady=5)
        
    def create_price_data_tab(self):
        frame = tk.Frame(self.notebook, bg='#2a2a2a')
        self.notebook.add(frame, text="Price Data")
        
        # Create main container
        container = tk.Frame(frame, bg='#2a2a2a')
        container.pack(expand=True, fill='both', padx=20, pady=20)
        
        row = 0
        
        # Current Price
        tk.Label(container, text="Current Price ($) *", font=('Arial', 12, 'bold'), 
                bg='#2a2a2a', fg='white').grid(row=row, column=0, sticky='w', pady=10)
        self.price_var = tk.DoubleVar(value=175.50)
        price_entry = tk.Entry(container, textvariable=self.price_var, width=15, 
                              font=('Arial', 12), bg='#3a3a3a', fg='white')
        price_entry.grid(row=row, column=1, sticky='w', padx=10, pady=10)
        
        row += 1
        
        # Price Change ($)
        tk.Label(container, text="Price Change ($)", font=('Arial', 12, 'bold'), 
                bg='#2a2a2a', fg='white').grid(row=row, column=0, sticky='w', pady=10)
        self.price_change_var = tk.DoubleVar(value=5.25)
        tk.Entry(container, textvariable=self.price_change_var, width=15, 
                font=('Arial', 12), bg='#3a3a3a', fg='white').grid(row=row, column=1, sticky='w', padx=10, pady=10)
        tk.Label(container, text="Positive for gains, negative for losses", font=('Arial', 9), 
                bg='#2a2a2a', fg='#888').grid(row=row, column=2, sticky='w', padx=5, pady=10)
        
        row += 1
        
        # Price Change Percentage
        tk.Label(container, text="Price Change (%) *", font=('Arial', 12, 'bold'), 
                bg='#2a2a2a', fg='white').grid(row=row, column=0, sticky='w', pady=10)
        self.price_change_pct_var = tk.DoubleVar(value=3.2)
        tk.Entry(container, textvariable=self.price_change_pct_var, width=15, 
                font=('Arial', 12), bg='#3a3a3a', fg='white').grid(row=row, column=1, sticky='w', padx=10, pady=10)
        tk.Label(container, text="e.g., 3.2 for +3.2%, -1.5 for -1.5%", font=('Arial', 9), 
                bg='#2a2a2a', fg='#888').grid(row=row, column=2, sticky='w', padx=5, pady=10)
        
        row += 1
        
        # Auto-calculate button
        calc_button = tk.Button(container, text="Auto-Calculate Change %", 
                               command=self.calculate_percentage,
                               bg='#00ff88', fg='black', font=('Arial', 10, 'bold'),
                               padx=20, pady=5)
        calc_button.grid(row=row, column=1, sticky='w', padx=10, pady=20)
        
        row += 1
        
        # Visual Options
        tk.Label(container, text="Visual Options", font=('Arial', 14, 'bold'), 
                bg='#2a2a2a', fg='#00ff88').grid(row=row, column=0, columnspan=3, sticky='w', pady=(30,10))
        
        row += 1
        
        # YOLO Style
        self.is_yolo_var = tk.BooleanVar(value=False)
        tk.Checkbutton(container, text="YOLO Style (glowing purple effect)", 
                      variable=self.is_yolo_var, bg='#2a2a2a', fg='white',
                      font=('Arial', 11), selectcolor='#3a3a3a').grid(row=row, column=0, columnspan=2, sticky='w', pady=5)
        
        row += 1
        
        # Border Style
        tk.Label(container, text="Border Style", font=('Arial', 11, 'bold'), 
                bg='#2a2a2a', fg='white').grid(row=row, column=0, sticky='w', pady=5)
        self.border_style_var = tk.StringVar(value="solid")
        border_combo = ttk.Combobox(container, textvariable=self.border_style_var, width=15,
                                   values=["solid", "dashed"])
        border_combo.grid(row=row, column=1, sticky='w', padx=10, pady=5)
        tk.Label(container, text="dashed = pre-market style", font=('Arial', 9), 
                bg='#2a2a2a', fg='#888').grid(row=row, column=2, sticky='w', padx=5, pady=5)
        
    def calculate_percentage(self):
        try:
            current_price = self.price_var.get()
            price_change = self.price_change_var.get()
            if current_price > 0:
                percentage = (price_change / current_price) * 100
                self.price_change_pct_var.set(round(percentage, 2))
                messagebox.showinfo("Calculated", f"Price change: {percentage:.2f}%")
            else:
                messagebox.showerror("Error", "Current price must be greater than 0")
        except Exception as e:
            messagebox.showerror("Error", f"Invalid price data: {e}")
    
    def create_key_stats_tab(self):
        frame = tk.Frame(self.notebook, bg='#2a2a2a')
        self.notebook.add(frame, text="Key Stats")
        
        container = tk.Frame(frame, bg='#2a2a2a')
        container.pack(expand=True, fill='both', padx=20, pady=20)
        
        tk.Label(container, text="Key Statistics (exactly 3 for mobile layout)", 
                font=('Arial', 14, 'bold'), bg='#2a2a2a', fg='#00ff88').pack(pady=10)
        
        # Create 3 stat frames
        self.stat_vars = []
        for i in range(3):
            stat_frame = tk.LabelFrame(container, text=f"Stat {i+1}", 
                                     bg='#3a3a3a', fg='white', font=('Arial', 11, 'bold'))
            stat_frame.pack(fill='x', pady=10)
            
            stat_dict = {}
            
            # Value
            tk.Label(stat_frame, text="Value:", bg='#3a3a3a', fg='white', 
                    font=('Arial', 10, 'bold')).grid(row=0, column=0, sticky='w', padx=5, pady=5)
            stat_dict['value'] = tk.StringVar(value="" if i > 0 else ["$185", "15%", "2.5M"][i])
            tk.Entry(stat_frame, textvariable=stat_dict['value'], width=15, 
                    bg='#2a2a2a', fg='white').grid(row=0, column=1, sticky='w', padx=5, pady=5)
            
            # Label
            tk.Label(stat_frame, text="Label:", bg='#3a3a3a', fg='white', 
                    font=('Arial', 10, 'bold')).grid(row=0, column=2, sticky='w', padx=5, pady=5)
            stat_dict['label'] = tk.StringVar(value="" if i > 0 else ["Target", "Beat Est", "Volume"][i])
            tk.Entry(stat_frame, textvariable=stat_dict['label'], width=15, 
                    bg='#2a2a2a', fg='white').grid(row=0, column=3, sticky='w', padx=5, pady=5)
            
            # Positive/Negative
            stat_dict['is_positive'] = tk.BooleanVar(value=True)
            tk.Checkbutton(stat_frame, text="Positive (green)", variable=stat_dict['is_positive'], 
                         bg='#3a3a3a', fg='white', selectcolor='#2a2a2a').grid(row=0, column=4, padx=5, pady=5)
            
            self.stat_vars.append(stat_dict)
        
        # Examples
        examples_frame = tk.LabelFrame(container, text="Examples", 
                                     bg='#3a3a3a', fg='white', font=('Arial', 11, 'bold'))
        examples_frame.pack(fill='x', pady=20)
        
        examples_text = """
IPO: ["223%", "Day 1 High"] | ["$6.8B", "Valuation"] | ["46M", "Volume"]
Options: ["$3.20", "Credit"] | ["72%", "PoP"] | ["21d", "DTE"]  
Crypto: ["5.2%", "APY"] | ["$4.2K", "Target"] | ["85", "RSI"]
FDA: ["+180%", "If Pass"] | ["-65%", "If Fail"] | ["220%", "IV"]
        """
        
        tk.Label(examples_frame, text=examples_text, bg='#3a3a3a', fg='#aaa', 
                font=('Arial', 9), justify='left').pack(padx=10, pady=10)
    
    def create_strategy_tab(self):
        frame = tk.Frame(self.notebook, bg='#2a2a2a')
        self.notebook.add(frame, text="Strategy")
        
        container = tk.Frame(frame, bg='#2a2a2a')
        container.pack(expand=True, fill='both', padx=20, pady=20)
        
        # Strategy Title
        tk.Label(container, text="Strategy Title *", font=('Arial', 12, 'bold'), 
                bg='#2a2a2a', fg='white').pack(anchor='w', pady=5)
        self.strategy_title_var = tk.StringVar(value="Earnings Momentum Play")
        tk.Entry(container, textvariable=self.strategy_title_var, width=60, 
                font=('Arial', 11), bg='#3a3a3a', fg='white').pack(fill='x', pady=5)
        
        # Strategy Description
        tk.Label(container, text="Strategy Description *", font=('Arial', 12, 'bold'), 
                bg='#2a2a2a', fg='white').pack(anchor='w', pady=(20,5))
        self.strategy_desc_text = scrolledtext.ScrolledText(container, width=70, height=8, 
                                                          bg='#3a3a3a', fg='white', font=('Arial', 10))
        self.strategy_desc_text.pack(fill='both', expand=True, pady=5)
        self.strategy_desc_text.insert('1.0', "Beat earnings by 15%. Strong guidance raise. Buy at open for continuation momentum. Historical 3-day avg after beats is +5%.")
        
        # Link Text and URL
        link_frame = tk.Frame(container, bg='#2a2a2a')
        link_frame.pack(fill='x', pady=20)
        
        tk.Label(link_frame, text="Link Text:", font=('Arial', 11, 'bold'), 
                bg='#2a2a2a', fg='white').grid(row=0, column=0, sticky='w', padx=5)
        self.strategy_link_text_var = tk.StringVar(value="ER playbook →")
        tk.Entry(link_frame, textvariable=self.strategy_link_text_var, width=25, 
                font=('Arial', 10), bg='#3a3a3a', fg='white').grid(row=0, column=1, sticky='w', padx=5)
        
        tk.Label(link_frame, text="Link URL:", font=('Arial', 11, 'bold'), 
                bg='#2a2a2a', fg='white').grid(row=1, column=0, sticky='w', padx=5, pady=5)
        self.strategy_link_url_var = tk.StringVar(value="https://example.com/earnings-strategy")
        tk.Entry(link_frame, textvariable=self.strategy_link_url_var, width=50, 
                font=('Arial', 10), bg='#3a3a3a', fg='white').grid(row=1, column=1, sticky='w', padx=5, pady=5)
        
        # Strategy Examples
        examples_frame = tk.LabelFrame(container, text="Strategy Examples by Signal Type", 
                                     bg='#3a3a3a', fg='white', font=('Arial', 11, 'bold'))
        examples_frame.pack(fill='x', pady=20)
        
        examples_text = """
IPO: "Stablecoin leader 3x'd on debut. ARK bought $150M. Watch for dip to $60-65 for entry."
YOLO: "Kalshi shows 75% odds of 150K by Q4. High risk, high reward - only risk what you can lose!"
Pre-Market: "TSMC production boost news. Pre-market up 6.8% on heavy volume. Buy at 9:28-9:30."
Options: "Post-earnings IV crush. Sell put spread for credit. 72% probability of profit."
Crypto: "Shanghai upgrade complete. Staking APY 5.2% + price appreciation. DeFi TVL surging."
FDA: "Alzheimer's drug PDUFA date 7/28. Binary event - ultra high risk, total loss possible."
        """
        
        tk.Label(examples_frame, text=examples_text, bg='#3a3a3a', fg='#aaa', 
                font=('Arial', 9), justify='left').pack(padx=10, pady=10)
    
    def create_chart_tab(self):
        frame = tk.Frame(self.notebook, bg='#2a2a2a')
        self.notebook.add(frame, text="Chart Data")
        
        container = tk.Frame(frame, bg='#2a2a2a')
        container.pack(expand=True, fill='both', padx=20, pady=20)
        
        # Chart Pattern
        tk.Label(container, text="Chart Pattern", font=('Arial', 12, 'bold'), 
                bg='#2a2a2a', fg='white').pack(anchor='w', pady=5)
        self.chart_pattern_var = tk.StringVar(value="momentum")
        pattern_combo = ttk.Combobox(container, textvariable=self.chart_pattern_var, width=20,
                                   values=["momentum", "volatile", "breakout", "decline"])
        pattern_combo.pack(anchor='w', pady=5)
        
        # Pattern descriptions
        pattern_desc = """
momentum: Strong upward trend
volatile: High volatility swings  
breakout: Consolidation then breakout
decline: Downward trend
        """
        tk.Label(container, text=pattern_desc, bg='#2a2a2a', fg='#888', 
                font=('Arial', 9), justify='left').pack(anchor='w', pady=10)
        
        # Event Label
        tk.Label(container, text="Event Label", font=('Arial', 12, 'bold'), 
                bg='#2a2a2a', fg='white').pack(anchor='w', pady=(20,5))
        self.event_label_var = tk.StringVar(value="Earnings beat")
        tk.Entry(container, textvariable=self.event_label_var, width=40, 
                font=('Arial', 11), bg='#3a3a3a', fg='white').pack(anchor='w', pady=5)
        
        # Event label examples
        event_examples = """
Examples:
• IPO: "IPO $31 → $103 peak"
• YOLO: "Kalshi 75% → 150K" 
• Pre-market: "Taiwan news 4AM"
• FDA: "FDA 7/28"
• Options: "IV Crush Play"
        """
        tk.Label(container, text=event_examples, bg='#2a2a2a', fg='#888', 
                font=('Arial', 9), justify='left').pack(anchor='w', pady=10)
        
        # Chart generation info
        info_frame = tk.LabelFrame(container, text="Chart Generation Info", 
                                 bg='#3a3a3a', fg='white', font=('Arial', 11, 'bold'))
        info_frame.pack(fill='x', pady=20)
        
        info_text = """
Charts are automatically generated with:
• Historical data (20 points) - solid line showing past price action
• Prediction bands - dashed lines showing bull/bear scenarios  
• Event marker - shows catalyst or signal trigger point
• Mobile optimization - 100px height for mobile screens
        """
        
        tk.Label(info_frame, text=info_text, bg='#3a3a3a', fg='#aaa', 
                font=('Arial', 9), justify='left').pack(padx=10, pady=10)
    
    def create_generate_tab(self):
        frame = tk.Frame(self.notebook, bg='#2a2a2a')
        self.notebook.add(frame, text="Generate")
        
        container = tk.Frame(frame, bg='#2a2a2a')
        container.pack(expand=True, fill='both', padx=20, pady=20)
        
        # Output options
        tk.Label(container, text="Output Options", font=('Arial', 14, 'bold'), 
                bg='#2a2a2a', fg='#00ff88').pack(pady=10)
        
        # Filename
        filename_frame = tk.Frame(container, bg='#2a2a2a')
        filename_frame.pack(fill='x', pady=10)
        
        tk.Label(filename_frame, text="Filename:", font=('Arial', 11, 'bold'), 
                bg='#2a2a2a', fg='white').pack(side='left')
        self.filename_var = tk.StringVar(value="")
        tk.Entry(filename_frame, textvariable=self.filename_var, width=40, 
                font=('Arial', 11), bg='#3a3a3a', fg='white').pack(side='left', padx=10)
        tk.Label(filename_frame, text="(leave empty for auto-generation)", font=('Arial', 9), 
                bg='#2a2a2a', fg='#888').pack(side='left', padx=5)
        
        # Generate button
        generate_button = tk.Button(container, text="🚀 Generate Signal HTML", 
                                   command=self.generate_signal,
                                   bg='#00ff88', fg='black', font=('Arial', 14, 'bold'),
                                   padx=30, pady=15)
        generate_button.pack(pady=30)
        
        # Preview button
        preview_button = tk.Button(container, text="👁️ Preview Data", 
                                  command=self.preview_data,
                                  bg='#00d4ff', fg='black', font=('Arial', 12, 'bold'),
                                  padx=20, pady=10)
        preview_button.pack(pady=10)
        
        # Output area
        output_frame = tk.LabelFrame(container, text="Generation Output", 
                                   bg='#3a3a3a', fg='white', font=('Arial', 11, 'bold'))
        output_frame.pack(fill='both', expand=True, pady=20)
        
        self.output_text = scrolledtext.ScrolledText(output_frame, width=70, height=15, 
                                                   bg='#2a2a2a', fg='#00ff88', font=('Courier', 10))
        self.output_text.pack(fill='both', expand=True, padx=10, pady=10)
        
        # Quick actions
        actions_frame = tk.Frame(container, bg='#2a2a2a')
        actions_frame.pack(fill='x', pady=10)
        
        tk.Button(actions_frame, text="Clear Output", command=self.clear_output,
                 bg='#ff4757', fg='white', font=('Arial', 10)).pack(side='left', padx=5)
        
        tk.Button(actions_frame, text="Open Output Folder", command=self.open_output_folder,
                 bg='#3498db', fg='white', font=('Arial', 10)).pack(side='left', padx=5)
    
    def preview_data(self):
        try:
            signal_data = self.collect_signal_data()
            
            preview = f"""
🎯 Signal Preview:
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

📊 Basic Info:
   Ticker: {signal_data.ticker}
   Company: {signal_data.company_name}
   Signal Type: {signal_data.signal_type.name}
   Priority: {signal_data.priority.name}
   Timestamp: {signal_data.timestamp}

💰 Price Data:
   Current Price: ${signal_data.current_price:,.2f}
   Price Change: ${signal_data.price_change:+,.2f}
   Change %: {signal_data.price_change_percent:+.2f}%

📈 Key Stats:
"""
            for i, stat in enumerate(signal_data.key_stats, 1):
                preview += f"   {i}. {stat.value} - {stat.label} {'(+)' if stat.is_positive else '(-)'}\n"
            
            preview += f"""
🧠 Strategy:
   Title: {signal_data.strategy.title}
   Description: {signal_data.strategy.description[:100]}...
   Link: {signal_data.strategy.link_text}

📊 Chart:
   Pattern: {signal_data.chart_data.event_label if signal_data.chart_data else 'Auto-generated'}
   
🎨 Visual:
   YOLO Style: {'Yes' if signal_data.is_yolo else 'No'}
   Border: {signal_data.border_style}
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
"""
            
            self.output_text.delete('1.0', tk.END)
            self.output_text.insert('1.0', preview)
            
        except Exception as e:
            messagebox.showerror("Preview Error", f"Error creating preview: {e}")
    
    def collect_signal_data(self):
        # Validate required fields
        if not self.ticker_var.get().strip():
            raise ValueError("Ticker symbol is required")
        if not self.company_var.get().strip():
            raise ValueError("Company name is required")
        
        # Collect key stats
        key_stats = []
        for stat_dict in self.stat_vars:
            value = stat_dict['value'].get().strip()
            label = stat_dict['label'].get().strip()
            if value and label:
                key_stats.append(KeyStat(value, label, stat_dict['is_positive'].get()))
        
        # Create strategy info
        strategy = StrategyInfo(
            title=self.strategy_title_var.get().strip(),
            description=self.strategy_desc_text.get('1.0', tk.END).strip(),
            link_text=self.strategy_link_text_var.get().strip(),
            link_url=self.strategy_link_url_var.get().strip()
        )
        
        # Generate chart data
        current_price = self.price_var.get()
        chart_data = generate_chart_data(
            self.ticker_var.get(), 
            current_price, 
            self.chart_pattern_var.get()
        )
        chart_data.event_label = self.event_label_var.get().strip() or f"Signal @ ${current_price:.2f}"
        
        # Create signal data
        signal_data = SignalData(
            ticker=self.ticker_var.get().strip().upper(),
            company_name=self.company_var.get().strip(),
            signal_type=SignalType[self.signal_type_var.get()],
            current_price=current_price,
            price_change=self.price_change_var.get(),
            price_change_percent=self.price_change_pct_var.get(),
            priority=SignalPriority[self.priority_var.get()],
            key_stats=key_stats,
            strategy=strategy,
            chart_data=chart_data,
            timestamp=self.timestamp_var.get().strip(),
            is_yolo=self.is_yolo_var.get(),
            border_style=self.border_style_var.get()
        )
        
        return signal_data
    
    def generate_signal(self):
        try:
            self.output_text.delete('1.0', tk.END)
            self.output_text.insert(tk.END, "🎨 Generating signal HTML...\n\n")
            self.root.update()
            
            # Collect signal data
            signal_data = self.collect_signal_data()
            
            # Generate filename if not provided
            filename = self.filename_var.get().strip()
            if not filename:
                filename = f"{signal_data.ticker}_{signal_data.signal_type.name.lower()}.html"
            elif not filename.endswith('.html'):
                filename += '.html'
            
            # Generate HTML
            output_path = self.renderer.render_signal(signal_data, filename)
            
            # Check result
            if os.path.exists(output_path):
                file_size = os.path.getsize(output_path)
                abs_path = os.path.abspath(output_path)
                
                success_msg = f"""✅ SUCCESS! Signal generated successfully!

📄 File: {filename}
📁 Path: {output_path}  
💾 Size: {file_size:,} bytes ({file_size/1024:.1f} KB)
🌐 Browser: file://{abs_path}

📊 Signal Details:
   • Ticker: {signal_data.ticker}
   • Type: {signal_data.signal_type.name}
   • Price: ${signal_data.current_price:,.2f} ({signal_data.price_change_percent:+.1f}%)
   • Stats: {len(signal_data.key_stats)} key metrics
   • Strategy: {signal_data.strategy.title}

🎨 Visual Features:
   • Mobile-optimized responsive design
   • Interactive charts with prediction bands
   • Real-time price updates (every 5s)
   • Haptic feedback for mobile devices
   • {'YOLO glow effects' if signal_data.is_yolo else 'Standard styling'}
   • {signal_data.border_style.title()} border style

🚀 Ready to view in browser!"""
                
                self.output_text.insert(tk.END, success_msg)
                
                # Show success dialog
                result = messagebox.askyesno("Success!", 
                    f"Signal '{signal_data.ticker}' generated successfully!\n\n"
                    f"File: {filename}\n"
                    f"Size: {file_size:,} bytes\n\n"
                    f"Would you like to open it in your browser?")
                
                if result:
                    import webbrowser
                    webbrowser.open(f"file://{abs_path}")
                    
            else:
                error_msg = "❌ ERROR: File was not generated!"
                self.output_text.insert(tk.END, error_msg)
                messagebox.showerror("Error", "Failed to generate HTML file")
                
        except Exception as e:
            error_msg = f"❌ GENERATION ERROR:\n\n{str(e)}\n\nPlease check your input data."
            self.output_text.insert(tk.END, error_msg)
            messagebox.showerror("Generation Error", f"Error: {e}")
    
    def clear_output(self):
        self.output_text.delete('1.0', tk.END)
    
    def open_output_folder(self):
        output_dir = os.path.abspath("gui_generated")
        if os.path.exists(output_dir):
            import subprocess
            import sys
            if sys.platform == "win32":
                os.startfile(output_dir)
            elif sys.platform == "darwin":
                subprocess.call(["open", output_dir])
            else:
                subprocess.call(["xdg-open", output_dir])
        else:
            messagebox.showinfo("Info", f"Output directory doesn't exist yet: {output_dir}")

def main():
    root = tk.Tk()
    app = SignalGeneratorGUI(root)
    
    # Add instructions
    instructions = """
Welcome to SignalPro Signal Generator!

📋 Getting Started:
1. Fill out each tab with your signal data
2. Use the Preview button to check your data
3. Click Generate to create the HTML file
4. Open the file in your browser to view

💡 Tips:
• Fields marked with * are required
• Key Stats should have exactly 3 items for mobile layout
• YOLO signals get special glowing effects
• Pre-market signals typically use dashed borders
• All generated files are mobile-optimized

🎯 Ready to create professional trading signals!
    """
    
    messagebox.showinfo("Welcome", instructions)
    
    root.mainloop()

if __name__ == "__main__":
    main()