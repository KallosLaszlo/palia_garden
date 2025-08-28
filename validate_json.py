#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
JSON validation script for Palia Garden Optimizer
"""

import os
import json
import sys
import glob

def validate_json_files():
    """Validate all JSON files in the lang directory"""
    print("🔍 Validating JSON files...")
    
    lang_dir = "lang"
    if not os.path.exists(lang_dir):
        print(f"❌ Error: {lang_dir} directory not found!")
        return False
    
    # Find all JSON files
    json_files = glob.glob(os.path.join(lang_dir, "*.json"))
    
    if not json_files:
        print(f"❌ Error: No JSON files found in {lang_dir} directory!")
        return False
    
    print(f"📁 Found {len(json_files)} JSON files:")
    for file in json_files:
        print(f"  - {file}")
    print()
    
    # Required fields for language files
    required_fields = [
        'language_name', 'title', 'select_garden_size', 'rows', 'cols',
        'create_garden', 'garden_size', 'mode_label', 'auto_fill', 
        'optimize', 'add_all', 'clear', 'crops'
    ]
    
    all_valid = True
    
    for file_path in json_files:
        print(f"🔎 Validating {file_path}...")
        
        try:
            # Try different encodings
            data = None
            for encoding in ['utf-8-sig', 'utf-8']:
                try:
                    with open(file_path, 'r', encoding=encoding) as f:
                        data = json.load(f)
                    break
                except (UnicodeDecodeError, json.JSONDecodeError):
                    continue
            
            if data is None:
                print(f"❌ Error: Could not decode {file_path}")
                all_valid = False
                continue
            
            # Check required fields
            missing_fields = []
            for field in required_fields:
                if field not in data:
                    missing_fields.append(field)
            
            if missing_fields:
                print(f"❌ Error: Missing required fields in {file_path}: {', '.join(missing_fields)}")
                all_valid = False
                continue
            
            # Check crops section
            if not isinstance(data['crops'], dict) or len(data['crops']) == 0:
                print(f"❌ Error: 'crops' section invalid or empty in {file_path}")
                all_valid = False
                continue
            
            print(f"✅ {file_path} is valid ({len(data['crops'])} crops)")
            
        except json.JSONDecodeError as e:
            print(f"❌ Error: Invalid JSON in {file_path}: {e}")
            all_valid = False
        except Exception as e:
            print(f"❌ Error: Failed to validate {file_path}: {e}")
            all_valid = False
    
    print()
    if all_valid:
        print("✅ All JSON files are valid!")
        return True
    else:
        print("❌ Some JSON files have errors!")
        return False

def main():
    """Main function"""
    print("Palia Garden Optimizer - JSON Validator")
    print("=" * 40)
    
    if validate_json_files():
        print("\n🎉 Validation completed successfully!")
        sys.exit(0)
    else:
        print("\n💥 Validation failed!")
        sys.exit(1)

if __name__ == "__main__":
    main()
