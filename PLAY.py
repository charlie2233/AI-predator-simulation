#!/usr/bin/env python3
"""
🧬 EVOLUTION SANDBOX - Launch Script
Commercial Edition with Enhanced UI/UX

Quick start script to launch the AI Evolution Sandbox game.
"""

import os
import sys

def print_banner():
    """Print a cool ASCII banner."""
    banner = """
╔══════════════════════════════════════════════════════════════════╗
║                                                                  ║
║     🧬  E V O L U T I O N   S A N D B O X  🧬                   ║
║                                                                  ║
║           AI Ecosystem Simulator - Commercial Edition            ║
║                                                                  ║
╚══════════════════════════════════════════════════════════════════╝

🎮 Features:
  • 7 Unique Species with Genetic Evolution
  • Real-time Population & Trait Visualization
  • Achievement System with 15+ Unlockables
  • Interactive Tutorial & Help System
  • Manual Disaster Events (Earthquakes, Tsunamis, Meteors)
  • Agent Inspector with DNA Visualization
  • Minimap for Quick Navigation
  • Particle Effects & Screen Shake
  • Professional Settings Menu
  • Save/Load System

🚀 Starting game...
"""
    print(banner)

def check_dependencies():
    """Check if required packages are installed."""
    try:
        import pygame
        import numpy
        print("✅ All dependencies installed")
        return True
    except ImportError as e:
        print(f"❌ Missing dependency: {e}")
        print("\n📦 Install dependencies:")
        print("   pip install -r requirements.txt")
        return False

def main():
    """Launch the game."""
    print_banner()
    
    if not check_dependencies():
        input("\nPress Enter to exit...")
        return
    
    # Add current directory to path
    sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
    
    try:
        from simulation.main import main as game_main
        game_main()
    except Exception as e:
        print(f"\n❌ Error launching game: {e}")
        import traceback
        traceback.print_exc()
        input("\nPress Enter to exit...")

if __name__ == "__main__":
    main()

