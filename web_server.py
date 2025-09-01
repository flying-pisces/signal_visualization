#!/usr/bin/env python3
"""
Flask Web Server for SignalPro Web GUI
Provides API endpoints for generating signal HTML files
"""

import os
import json
from datetime import datetime
from flask import Flask, request, jsonify, send_file, render_template_string
from flask_cors import CORS
from signal_renderer import (
    SignalRenderer, SignalData, SignalType, SignalPriority, 
    ChartData, KeyStat, StrategyInfo, generate_chart_data
)

app = Flask(__name__)
CORS(app)  # Enable CORS for web GUI

# Initialize renderer
renderer = SignalRenderer(output_dir="web_generated")

@app.route('/')
def index():
    """Serve the web GUI"""
    try:
        with open('web_gui.html', 'r', encoding='utf-8') as f:
            return f.read()
    except FileNotFoundError:
        return """
        <h1>SignalPro Web GUI</h1>
        <p>web_gui.html not found. Please ensure the file is in the same directory.</p>
        <p>Available endpoints:</p>
        <ul>
            <li><a href="/api/generate">/api/generate</a> - POST: Generate signal HTML</li>
            <li><a href="/api/preview">/api/preview</a> - POST: Preview signal data</li>
            <li><a href="/api/types">/api/types</a> - GET: Get signal types and priorities</li>
        </ul>
        """

@app.route('/api/types', methods=['GET'])
def get_types():
    """Get available signal types and priorities"""
    return jsonify({
        'signal_types': [
            {'value': st.name, 'label': st.name.replace('_', ' ').title()} 
            for st in SignalType
        ],
        'priorities': [
            {'value': sp.name, 'label': sp.value if sp.value else sp.name} 
            for sp in SignalPriority
        ]
    })

@app.route('/api/preview', methods=['POST'])
def preview_signal():
    """Preview signal data without generating HTML"""
    try:
        data = request.json
        signal_data = create_signal_from_request(data)
        
        # Return preview data
        preview = {
            'ticker': signal_data.ticker,
            'company_name': signal_data.company_name,
            'signal_type': signal_data.signal_type.name,
            'priority': signal_data.priority.name,
            'current_price': signal_data.current_price,
            'price_change_percent': signal_data.price_change_percent,
            'key_stats': [
                {
                    'value': stat.value,
                    'label': stat.label,
                    'is_positive': stat.is_positive
                }
                for stat in signal_data.key_stats
            ],
            'strategy': {
                'title': signal_data.strategy.title,
                'description': signal_data.strategy.description[:200] + '...' if len(signal_data.strategy.description) > 200 else signal_data.strategy.description
            } if signal_data.strategy else None,
            'timestamp': signal_data.timestamp,
            'is_yolo': signal_data.is_yolo
        }
        
        return jsonify({
            'success': True,
            'preview': preview
        })
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 400

@app.route('/api/generate', methods=['POST'])
def generate_signal():
    """Generate signal HTML file"""
    try:
        data = request.json
        print(f"📊 Received request: {data.get('ticker', 'Unknown')} - {data.get('signalType', 'Unknown')}")
        
        # Create signal data
        signal_data = create_signal_from_request(data)
        
        # Generate filename
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"{signal_data.ticker}_{signal_data.signal_type.name.lower()}_{timestamp}.html"
        
        # Generate HTML
        output_path = renderer.render_signal(signal_data, filename)
        
        # Verify file was created
        if not os.path.exists(output_path):
            raise Exception("HTML file was not generated")
        
        file_size = os.path.getsize(output_path)
        abs_path = os.path.abspath(output_path)
        
        print(f"✅ Generated: {filename} ({file_size:,} bytes)")
        
        return jsonify({
            'success': True,
            'filename': filename,
            'file_path': output_path,
            'file_size': file_size,
            'absolute_path': abs_path,
            'download_url': f"/download/{filename}",
            'view_url': f"file://{abs_path}",
            'signal_data': {
                'ticker': signal_data.ticker,
                'signal_type': signal_data.signal_type.name,
                'price': signal_data.current_price,
                'change_percent': signal_data.price_change_percent,
                'priority': signal_data.priority.name
            }
        })
        
    except Exception as e:
        print(f"❌ Generation error: {e}")
        return jsonify({
            'success': False,
            'error': str(e)
        }), 400

@app.route('/download/<filename>')
def download_file(filename):
    """Download generated HTML file"""
    try:
        file_path = os.path.join(renderer.output_dir, filename)
        if not os.path.exists(file_path):
            return jsonify({'error': 'File not found'}), 404
        
        return send_file(
            file_path,
            as_attachment=True,
            download_name=filename,
            mimetype='text/html'
        )
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/view/<filename>')
def view_file(filename):
    """View generated HTML file in browser"""
    try:
        file_path = os.path.join(renderer.output_dir, filename)
        if not os.path.exists(file_path):
            return "File not found", 404
        
        with open(file_path, 'r', encoding='utf-8') as f:
            return f.read()
    except Exception as e:
        return f"Error loading file: {e}", 500

@app.route('/api/files', methods=['GET'])
def list_files():
    """List generated files"""
    try:
        files = []
        if os.path.exists(renderer.output_dir):
            for filename in os.listdir(renderer.output_dir):
                if filename.endswith('.html'):
                    file_path = os.path.join(renderer.output_dir, filename)
                    file_size = os.path.getsize(file_path)
                    file_time = os.path.getmtime(file_path)
                    
                    files.append({
                        'filename': filename,
                        'size': file_size,
                        'created': datetime.fromtimestamp(file_time).isoformat(),
                        'download_url': f"/download/{filename}",
                        'view_url': f"/view/{filename}"
                    })
        
        files.sort(key=lambda x: x['created'], reverse=True)
        
        return jsonify({
            'success': True,
            'files': files,
            'total_count': len(files)
        })
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 400

def create_signal_from_request(data):
    """Convert request data to SignalData object"""
    
    # Parse key stats
    key_stats = []
    stats_data = data.get('stats', [])
    for stat in stats_data:
        if stat.get('value') and stat.get('label'):
            key_stats.append(KeyStat(
                value=stat['value'],
                label=stat['label'],
                is_positive=stat.get('is_positive', True)
            ))
    
    # Create strategy info
    strategy = None
    if data.get('strategyTitle') and data.get('strategyDesc'):
        strategy = StrategyInfo(
            title=data['strategyTitle'],
            description=data['strategyDesc'],
            link_text=data.get('strategyLinkText', 'Learn more →'),
            link_url=data.get('strategyLinkUrl', 'https://example.com/strategy')
        )
    
    # Generate chart data
    current_price = float(data.get('currentPrice', 100.0))
    chart_pattern = data.get('chartPattern', 'momentum')
    chart_data = generate_chart_data(data.get('ticker', 'STOCK'), current_price, chart_pattern)
    
    # Set event label
    event_label = data.get('eventLabel', '')
    if event_label:
        chart_data.event_label = event_label
    
    # Calculate price change
    change_percent = float(data.get('changePercent', 0))
    price_change = current_price * (change_percent / 100)
    
    # Create signal data
    signal_data = SignalData(
        ticker=data.get('ticker', 'STOCK').upper(),
        company_name=data.get('companyName', 'Unknown Company'),
        signal_type=SignalType[data.get('signalType', 'EARNINGS')],
        current_price=current_price,
        price_change=price_change,
        price_change_percent=change_percent,
        priority=SignalPriority[data.get('priority', 'NORMAL')],
        key_stats=key_stats,
        strategy=strategy,
        chart_data=chart_data,
        timestamp=data.get('timestamp', 'Just now'),
        is_yolo=data.get('isYolo', False),
        border_style=data.get('borderStyle', 'solid')
    )
    
    return signal_data

@app.errorhandler(404)
def not_found(error):
    return jsonify({'error': 'Endpoint not found'}), 404

@app.errorhandler(500)
def internal_error(error):
    return jsonify({'error': 'Internal server error'}), 500

def main():
    """Run the web server"""
    print("🌐 SignalPro Web Server")
    print("=" * 40)
    print("📱 Web GUI: http://localhost:5000")
    print("🔗 API Endpoints:")
    print("   • GET  /api/types - Signal types and priorities")
    print("   • POST /api/preview - Preview signal data")
    print("   • POST /api/generate - Generate signal HTML")
    print("   • GET  /api/files - List generated files")
    print("   • GET  /download/<file> - Download HTML file")
    print("   • GET  /view/<file> - View HTML file")
    print("=" * 40)
    print("🚀 Starting server...")
    
    # Create output directory
    os.makedirs(renderer.output_dir, exist_ok=True)
    
    app.run(
        host='0.0.0.0',
        port=5000,
        debug=True,
        use_reloader=False
    )

if __name__ == '__main__':
    main()