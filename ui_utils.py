#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
UI utilities and components for Palia Garden Optimizer
"""

import tkinter as tk
import os
from PIL import Image, ImageTk
from crops import CROPS

class ToolTip:
    """Create a tooltip for a given widget"""
    def __init__(self, widget, text='widget info'):
        self.widget = widget
        self.text = text
        self.tipwindow = None
        self.id = None
        self.x = self.y = 0

    def showtip(self, text):
        """Display text in tooltip window"""
        self.text = text
        if self.tipwindow or not self.text:
            return
        x, y, cx, cy = self.widget.bbox("insert")
        x = x + self.widget.winfo_rootx() + 25
        y = y + cy + self.widget.winfo_rooty() + 25
        self.tipwindow = tw = tk.Toplevel(self.widget)
        tw.wm_overrideredirect(1)
        tw.wm_geometry("+%d+%d" % (x, y))
        label = tk.Label(tw, text=self.text, justify=tk.LEFT,
                        background="#ffffe0", relief=tk.SOLID, borderwidth=1,
                        font=("tahoma", "8", "normal"))
        label.pack(ipadx=1)

    def hidetip(self):
        """Hide the tooltip window"""
        tw = self.tipwindow
        self.tipwindow = None
        if tw:
            tw.destroy()

def create_tooltip(widget, text):
    """Create and bind tooltip to widget"""
    toolTip = ToolTip(widget)
    def enter(event):
        toolTip.showtip(text)
    def leave(event):
        toolTip.hidetip()
    widget.bind('<Enter>', enter)
    widget.bind('<Leave>', leave)

def load_crop_images(pics_folder="pics", thumbnail_size=(24, 24)):
    """Load crop images and create thumbnails"""
    images = {}
    if not os.path.exists(pics_folder):
        return images
    
    for crop_name in CROPS.keys():
        # Try different extensions
        for ext in ['.webp', '.png', '.jpg', '.jpeg']:
            image_path = os.path.join(pics_folder, f"{crop_name}{ext}")
            if os.path.exists(image_path):
                try:
                    # Load and resize image
                    pil_image = Image.open(image_path)
                    pil_image = pil_image.resize(thumbnail_size, Image.Resampling.LANCZOS)
                    tk_image = ImageTk.PhotoImage(pil_image)
                    images[crop_name] = tk_image
                    break
                except Exception as e:
                    print(f"Hiba a kép betöltésekor {image_path}: {e}")
                    continue
    
    return images
