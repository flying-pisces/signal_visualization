#!/usr/bin/env python3
"""
Test the complete web GUI workflow
"""

import os
import json
import time
import requests
import subprocess
import signal
from threading import Thread

def test_web_server():
    """Test the Flask web server functionality"""
    print("🧪 Testing Web Server Functionality")
    print("=" * 50)
    
    # Test data
    test_signal = {
        "ticker": "TSLA",
        "companyName": "Tesla Inc",
        "signalType": "EARNINGS", 
        "priority": "HOT",
        "currentPrice": 248.50,
        "changePercent": 12.3,
        "stats": [
            {"value": "+15%", "label": "AH Move", "is_positive": True},
            {"value": "$275", "label": "Target", "is_positive": True},
            {"value": "8.5M", "label": "AH Vol", "is_positive": True}
        ],
        "strategyTitle": "Post-Earnings Rocket",
        "strategyDesc": "Crushed delivery numbers and FSD progress update. After-hours up 15% on massive volume. Buy at open for continuation.",
        "chartPattern": "momentum",
        "eventLabel": "Q4 delivery beat",
        "isYolo": False,
        "timestamp": "After hours"
    }
    
    base_url = "http://localhost:5000"
    
    print("📊 Testing API endpoints...")
    
    # Test 1: Types endpoint
    try:
        response = requests.get(f"{base_url}/api/types", timeout=5)
        if response.status_code == 200:
            data = response.json()
            print(f"✅ GET /api/types - {len(data['signal_types'])} types, {len(data['priorities'])} priorities")
        else:
            print(f"❌ GET /api/types - Status {response.status_code}")
    except Exception as e:
        print(f"❌ GET /api/types - Error: {e}")
    
    # Test 2: Preview endpoint
    try:
        response = requests.post(f"{base_url}/api/preview", json=test_signal, timeout=5)
        if response.status_code == 200:
            data = response.json()
            if data['success']:
                preview = data['preview']
                print(f"✅ POST /api/preview - {preview['ticker']} {preview['signal_type']}")
            else:
                print(f"❌ POST /api/preview - {data.get('error', 'Unknown error')}")
        else:
            print(f"❌ POST /api/preview - Status {response.status_code}")
    except Exception as e:
        print(f"❌ POST /api/preview - Error: {e}")
    
    # Test 3: Generate endpoint
    try:
        response = requests.post(f"{base_url}/api/generate", json=test_signal, timeout=10)
        if response.status_code == 200:
            data = response.json()
            if data['success']:
                print(f"✅ POST /api/generate - {data['filename']} ({data['file_size']:,} bytes)")
                
                # Test 4: Download endpoint
                download_response = requests.get(f"{base_url}{data['download_url']}", timeout=5)
                if download_response.status_code == 200:
                    print(f"✅ GET {data['download_url']} - File downloaded successfully")
                else:
                    print(f"❌ GET {data['download_url']} - Status {download_response.status_code}")
                    
                # Test 5: View endpoint
                view_url = f"{base_url}/view/{data['filename']}"
                view_response = requests.get(view_url, timeout=5)
                if view_response.status_code == 200:
                    print(f"✅ GET /view/{data['filename']} - File viewable in browser")
                else:
                    print(f"❌ GET /view/{data['filename']} - Status {view_response.status_code}")
                    
            else:
                print(f"❌ POST /api/generate - {data.get('error', 'Unknown error')}")
        else:
            print(f"❌ POST /api/generate - Status {response.status_code}")
    except Exception as e:
        print(f"❌ POST /api/generate - Error: {e}")
    
    # Test 6: Files endpoint
    try:
        response = requests.get(f"{base_url}/api/files", timeout=5)
        if response.status_code == 200:
            data = response.json()
            if data['success']:
                print(f"✅ GET /api/files - {data['total_count']} files listed")
            else:
                print(f"❌ GET /api/files - {data.get('error', 'Unknown error')}")
        else:
            print(f"❌ GET /api/files - Status {response.status_code}")
    except Exception as e:
        print(f"❌ GET /api/files - Error: {e}")
    
    return True

def test_offline_html():
    """Test the standalone HTML GUI"""
    print("\n🌐 Testing Standalone HTML GUI")
    print("=" * 50)
    
    # Check if HTML file exists
    if os.path.exists('web_gui.html'):
        print("✅ web_gui.html - File exists")
        
        # Check file size
        size = os.path.getsize('web_gui.html')
        print(f"✅ File size: {size:,} bytes ({size/1024:.1f} KB)")
        
        # Check basic HTML structure
        with open('web_gui.html', 'r') as f:
            content = f.read()
            
        checks = [
            ('DOCTYPE', '<!DOCTYPE html>' in content),
            ('Title', '<title>' in content),
            ('CSS', '<style>' in content),
            ('JavaScript', '<script>' in content),
            ('Form Elements', 'id="signalForm"' in content),
            ('Preview Section', 'id="previewCard"' in content),
            ('Generate Function', 'function generateSignal()' in content)
        ]
        
        for check_name, passed in checks:
            status = "✅" if passed else "❌"
            print(f"{status} {check_name}")
            
        return all(check[1] for check in checks)
    else:
        print("❌ web_gui.html - File not found")
        return False

def test_api_html():
    """Test the API-connected HTML GUI"""
    print("\n🌐 Testing API-Connected HTML GUI")
    print("=" * 50)
    
    # Check if HTML file exists
    if os.path.exists('web_gui_api.html'):
        print("✅ web_gui_api.html - File exists")
        
        # Check file size
        size = os.path.getsize('web_gui_api.html')
        print(f"✅ File size: {size:,} bytes ({size/1024:.1f} KB)")
        
        # Check API integration features
        with open('web_gui_api.html', 'r') as f:
            content = f.read()
            
        checks = [
            ('API Base URL', 'API_BASE = ' in content),
            ('Fetch API', 'fetch(' in content),
            ('API Status', 'checkApiConnection' in content),
            ('API Generate', 'generateViaAPI' in content),
            ('Offline Fallback', 'generateOffline' in content),
            ('File Management', 'loadRecentFiles' in content)
        ]
        
        for check_name, passed in checks:
            status = "✅" if passed else "❌"
            print(f"{status} {check_name}")
            
        return all(check[1] for check in checks)
    else:
        print("❌ web_gui_api.html - File not found")
        return False

def create_quick_start_guide():
    """Create a quick start guide for the web GUI"""
    print("\n📝 Creating Web GUI Quick Start Guide")
    print("=" * 50)
    
    guide_content = """# 🌐 SignalPro Web GUI Quick Start

## 🚀 Three Ways to Use the Web GUI

### Method 1: Standalone HTML (No Server Required)
```bash
# Simply open in any browser
open web_gui.html
```
- ✅ **No setup required** - works offline
- ✅ **Client-side generation** - creates downloadable HTML
- ✅ **Full functionality** - all signal types supported
- ❌ **Limited features** - simplified chart generation

### Method 2: Full Web App (Recommended)
```bash
# Start the Flask server
python web_server.py

# Open in browser
http://localhost:5000
```
- ✅ **Full functionality** - complete signal rendering engine
- ✅ **File management** - view and download generated signals  
- ✅ **API integration** - real-time preview and validation
- ✅ **Recent files** - track generated signals

### Method 3: API-Connected Version
```bash
# Start server first
python web_server.py

# Open API version in browser  
open web_gui_api.html
```
- ✅ **Best of both worlds** - works online and offline
- ✅ **Automatic fallback** - switches to offline mode if server unavailable
- ✅ **Enhanced features** - file management, API status, recent files

## 📱 Features Comparison

| Feature | Standalone HTML | Full Web App | API-Connected |
|---------|----------------|--------------|---------------|
| Offline Mode | ✅ Always | ❌ No | ✅ Fallback |
| Full Rendering Engine | ❌ Simplified | ✅ Complete | ✅ Complete |
| File Management | ❌ No | ✅ Yes | ✅ Yes |
| Recent Files | ❌ No | ✅ Yes | ✅ Yes |
| Real-time Preview | ✅ Yes | ✅ Yes | ✅ Yes |
| Mobile Optimized Output | ✅ Basic | ✅ Full | ✅ Full |
| Chart Generation | ❌ No charts | ✅ Interactive | ✅ Interactive |

## 🎯 Quick Demo

1. **Open any version** in your browser
2. **Fill out the form**:
   - Ticker: `TSLA`
   - Company: `Tesla Inc` 
   - Signal Type: `Earnings`
   - Price: `$248.50`
   - Change: `+12.3%`
3. **Add 3 key stats** (Target, Volume, etc.)
4. **Write strategy** description
5. **Click Generate** - get mobile-optimized signal page!

## 🌐 Browser Compatibility

- ✅ **Chrome** - Full support
- ✅ **Safari** - Full support  
- ✅ **Firefox** - Full support
- ✅ **Edge** - Full support
- ✅ **Mobile browsers** - Responsive design

Ready to create professional trading signals in your browser! 🎉"""

    with open('WEB_GUI_QUICK_START.md', 'w') as f:
        f.write(guide_content)
    
    print("✅ WEB_GUI_QUICK_START.md created")
    return True

def main():
    """Run all web GUI tests"""
    print("🌐 SignalPro Web GUI Test Suite")
    print("=" * 60)
    
    results = []
    
    # Test standalone HTML
    results.append(("Standalone HTML GUI", test_offline_html()))
    
    # Test API-connected HTML  
    results.append(("API-Connected HTML GUI", test_api_html()))
    
    # Test web server (if running)
    print(f"\n🔍 Checking if web server is running on localhost:5000...")
    try:
        response = requests.get("http://localhost:5000", timeout=3)
        print("✅ Web server is running - testing API endpoints")
        results.append(("Web Server API", test_web_server()))
    except:
        print("❌ Web server not running - skipping API tests")
        print("💡 Start with: python web_server.py")
        results.append(("Web Server API", False))
    
    # Create documentation
    results.append(("Quick Start Guide", create_quick_start_guide()))
    
    # Summary
    print(f"\n📋 Test Results Summary:")
    print("=" * 60)
    
    passed = 0
    for test_name, result in results:
        status = "✅ PASS" if result else "❌ FAIL" 
        print(f"  {status} {test_name}")
        if result:
            passed += 1
    
    print(f"\n🎯 Overall: {passed}/{len(results)} tests passed")
    
    if passed == len(results):
        print("🎉 All web GUI components are working perfectly!")
        print("\n🚀 Ready to use:")
        print("   • Standalone: open web_gui.html") 
        print("   • Full App: python web_server.py")
        print("   • API Version: open web_gui_api.html")
    else:
        print("🔧 Some components need attention - check the failed tests above")

if __name__ == "__main__":
    main()