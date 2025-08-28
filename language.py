#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Language management for Palia Garden Optimizer
"""

import os
import json
import glob
import sys

def get_resource_path(relative_path):
    """Get absolute path to resource, works for dev and for PyInstaller"""
    try:
        # PyInstaller creates a temp folder and stores path in _MEIPASS
        base_path = sys._MEIPASS
    except AttributeError:
        base_path = os.path.abspath(".")
    return os.path.join(base_path, relative_path)

def load_languages():
    """Load all language files from the lang directory"""
    languages = {}
    lang_dir = get_resource_path('lang')
    
    if not os.path.exists(lang_dir):
        print(f"Warning: Language directory {lang_dir} not found!")
        return {}
    
    # Find all JSON files in lang directory
    lang_files = glob.glob(os.path.join(lang_dir, '*.json'))
    
    for lang_file in lang_files:
        try:
            # Try UTF-8-sig first (handles BOM), then UTF-8
            lang_data = None
            for encoding in ['utf-8-sig', 'utf-8']:
                try:
                    with open(lang_file, 'r', encoding=encoding) as f:
                        lang_data = json.load(f)
                    break
                except (UnicodeDecodeError, json.JSONDecodeError):
                    continue
            
            if lang_data is None:
                raise ValueError("Could not decode file or invalid JSON")
                
            # Use language_code from the file, or filename as fallback
            lang_code = lang_data.get('language_code', os.path.splitext(os.path.basename(lang_file))[0])
            languages[lang_code] = lang_data
            print(f"Loaded language: {lang_data.get('language_name', lang_code)} ({lang_code})")
            
        except Exception as e:
            print(f"Error loading language file {lang_file}: {e}")
    
    return languages

# Load all available languages on module import
LANGUAGES = load_languages()

class LanguageManager:
    """Manages language switching and text retrieval"""
    
    def __init__(self, default_language="en"):
        self.current_language_code = default_language
    
    def set_language(self, language_code):
        """Set the current language"""
        self.current_language_code = language_code
    
    def get_text(self, key):
        """Get localized text for current language with robust error handling"""
        # Handle special hardcoded case for created_by
        if key == "created_by":
            return "Created by: Kallós László 2025, Palia 0.194"
        
        # Fallback to English if current language not available
        lang_data = LANGUAGES.get(self.current_language_code, LANGUAGES.get("en", {}))
        
        # Get the text with fallback handling
        result = lang_data.get(key, key)
        
        # If we didn't find the key in current language, try English as fallback
        if result == key and self.current_language_code != "en":
            en_lang_data = LANGUAGES.get("en", {})
            result = en_lang_data.get(key, key)
            
            # Log missing translation for debugging
            if result == key:
                print(f"Warning: Missing translation for key '{key}' in languages {self.current_language_code} and en")
        
        return result
    
    def get_crop_name(self, crop_key):
        """Get localized crop name with fallback to original name"""
        # Get current language data
        lang_data = LANGUAGES.get(self.current_language_code, LANGUAGES.get("en", {}))
        
        # Try to get crop name from crops section
        crops_data = lang_data.get("crops", {})
        localized_name = crops_data.get(crop_key)
        
        if localized_name:
            return localized_name
        
        # Fallback to English if current language doesn't have the crop
        if self.current_language_code != "en":
            en_lang_data = LANGUAGES.get("en", {})
            en_crops_data = en_lang_data.get("crops", {})
            en_name = en_crops_data.get(crop_key)
            if en_name:
                return en_name
        
        # Final fallback to original crop key
        return crop_key
