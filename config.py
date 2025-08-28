#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Configuration management for Palia Garden Optimizer
"""

import os
import json
from pathlib import Path

def get_config_dir():
    """Get the appropriate configuration directory for the current OS"""
    if os.name == 'nt':  # Windows
        # Use AppData/Local for application data
        app_data = os.environ.get('LOCALAPPDATA')
        if app_data:
            config_dir = Path(app_data) / "PaliaGardenOptimizer"
        else:
            # Fallback to user profile
            config_dir = Path.home() / "AppData" / "Local" / "PaliaGardenOptimizer"
    else:  # Linux/Mac
        # Use XDG Base Directory specification or fallback
        xdg_config = os.environ.get('XDG_CONFIG_HOME')
        if xdg_config:
            config_dir = Path(xdg_config) / "palia-garden-optimizer"
        else:
            config_dir = Path.home() / ".config" / "palia-garden-optimizer"
    
    # Create directory if it doesn't exist
    config_dir.mkdir(parents=True, exist_ok=True)
    return config_dir

# Configuration file path
CONFIG_FILE = get_config_dir() / "palia_config.json"

def save_config(config_data):
    """Save configuration to JSON file"""
    try:
        with open(CONFIG_FILE, 'w') as f:
            json.dump(config_data, f, indent=2)
    except Exception as e:
        print(f"Error saving config: {e}")

def load_config():
    """Load configuration from JSON file"""
    try:
        if os.path.exists(CONFIG_FILE):
            with open(CONFIG_FILE, 'r') as f:
                return json.load(f)
    except Exception as e:
        print(f"Error loading config: {e}")
    return {}
