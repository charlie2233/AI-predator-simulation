#!/usr/bin/env python3
"""
Launch script for the AI Predator-Prey Simulation.
"""
import sys
import os

# Add the current directory to the path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from simulation.main import main

if __name__ == "__main__":
    main()
