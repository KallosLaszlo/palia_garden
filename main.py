#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Palia Garden Optimizer - Main Entry Point
Created by: Kallós László 2025, Palia 0.194
"""

import sys
import argparse
from palia_garden_optimizer import App

def main():
    """Main entry point"""
    parser = argparse.ArgumentParser(
        description='Palia Garden Optimizer - Multi-language garden planner',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python main.py                 # Start the GUI application
  python main.py --help          # Show this help message
  
For more information, visit: https://github.com/KallosLaszlo/palia_garden
        """
    )
    
    parser.add_argument(
        '--version', '-v',
        action='version',
        version='Palia Garden Optimizer v1.0 (Palia 0.194)'
    )
    
    parser.add_argument(
        '--debug',
        action='store_true',
        help='Enable debug mode'
    )
    
    args = parser.parse_args()
    
    try:
        # Create and run the application
        app = App()
        
        if args.debug:
            print("Debug mode enabled")
            app.title(app.title() + " (DEBUG)")
        
        # Start the main loop
        app.mainloop()
        
    except KeyboardInterrupt:
        print("\nApplication interrupted by user")
        sys.exit(0)
    except Exception as e:
        print(f"Error starting application: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
