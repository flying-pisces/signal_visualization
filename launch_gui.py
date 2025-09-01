#!/usr/bin/env python3
"""
Simple GUI launcher with error handling
"""

import sys
import os

def check_dependencies():
    """Check if all required modules are available"""
    missing = []
    
    try:
        import tkinter
    except ImportError:
        missing.append("tkinter (GUI framework)")
    
    try:
        from signal_renderer import SignalRenderer
    except ImportError:
        missing.append("signal_renderer.py (not found)")
    
    return missing

def main():
    print("🎯 SignalPro GUI Launcher")
    print("=" * 40)
    
    # Check dependencies
    missing = check_dependencies()
    if missing:
        print("❌ Missing dependencies:")
        for item in missing:
            print(f"   • {item}")
        print("\n💡 Please install missing components and try again.")
        return False
    
    print("✅ All dependencies found")
    print("🚀 Launching GUI...")
    
    try:
        # Import and launch GUI
        from signal_gui import SignalGeneratorGUI
        import tkinter as tk
        
        root = tk.Tk()
        app = SignalGeneratorGUI(root)
        
        print("✅ GUI launched successfully!")
        print("📱 Use the tabs to create your trading signal")
        print("🔄 Close this terminal to exit the GUI")
        
        root.mainloop()
        return True
        
    except Exception as e:
        print(f"❌ GUI launch failed: {e}")
        print("\n🔧 Try running directly: python signal_gui.py")
        return False

if __name__ == "__main__":
    success = main()
    if not success:
        sys.exit(1)