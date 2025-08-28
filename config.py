#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Configuration management for Palia Garden Optimizer
"""

import os
import json

# Configuration file path
CONFIG_FILE = "palia_config.json"

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
