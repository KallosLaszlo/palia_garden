#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Palia Garden Optimizer / Palia Garten-Optimierer / Palia ültetvény-optimalizáló
Multi-language garden planner with crop optimization
Created by: Kallós László 2025, Palia 0.194
"""

import tkinter as tk
from tkinter import ttk, messagebox
import sys
import os

# Resource path handling for PyInstaller
def get_resource_path(relative_path):
    """Get absolute path to resource, works for dev and for PyInstaller"""
    try:
        # PyInstaller creates a temp folder and stores path in _MEIPASS
        base_path = sys._MEIPASS
    except AttributeError:
        base_path = os.path.abspath(".")
    return os.path.join(base_path, relative_path)

# Import our modules
from config import save_config, load_config
from crops import CROPS, COLOR
from language import LANGUAGES, LanguageManager
from garden import Garden, score_garden_optimized, greedy_fill_optimized, local_search_optimized
from ui_utils import create_tooltip, load_crop_images


class App(tk.Tk):
    """Main application class"""
    
    def __init__(self):
        super().__init__()
        
        # Set window icon
        try:
            icon_path = get_resource_path("icon.ico")
            if os.path.exists(icon_path):
                self.iconbitmap(icon_path)
        except Exception as e:
            print(f"Could not load icon: {e}")
        
        # Load saved configuration
        self.config = load_config()
        
        # Initialize language manager
        self.lang_manager = LanguageManager(self.config.get("language", "en"))
        
        # Initialize UI variables
        self.rows_var = tk.IntVar(value=self.config.get("rows", 9))
        self.cols_var = tk.IntVar(value=self.config.get("cols", 9))
        self.inventory_vars = {name: tk.IntVar(value=self.config.get("inventory", {}).get(name, 0)) for name in CROPS.keys()}
        
        # Add trace callbacks for inventory changes
        for var in self.inventory_vars.values():
            var.trace_add("write", lambda *args: self.after_idle(self.save_current_config))
        self.preferred_var = tk.StringVar(value=self.config.get("preferred_plant", "Apple"))
        self.optimization_mode = tk.StringVar(value=self.config.get("optimization_mode", "balanced"))
        
        # Load crop images
        self.crop_images = load_crop_images()

        self.garden = Garden(self.rows_var.get(), self.cols_var.get())
        self._build_ui()
        self.update_language()
        self.redraw()
        
        # Bind save config on window close
        self.protocol("WM_DELETE_WINDOW", self.on_closing)

    def get_text(self, key):
        """Get localized text using language manager"""
        return self.lang_manager.get_text(key)
    
    def get_crop_name(self, crop_key):
        """Get localized crop name using language manager"""
        return self.lang_manager.get_crop_name(crop_key)

    def update_language(self):
        """Update all UI text when language changes"""
        self.title(self.get_text("title"))
        self.rebuild_ui()

    def on_language_change(self):
        """Called when language selection changes"""
        selected_display = self.lang_combo.get()
        lang_code = next((code for code, name in self.lang_options if name == selected_display), "en")
        self.lang_manager.set_language(lang_code)
        self.update_language()
        self.save_current_config()
    
    def on_closing(self):
        """Save config when closing the application"""
        self.save_current_config()
        self.destroy()
    
    def save_current_config(self):
        """Save current configuration to file"""
        config = {
            "language": self.lang_manager.current_language_code,
            "rows": self.rows_var.get(),
            "cols": self.cols_var.get(),
            "inventory": {name: var.get() for name, var in self.inventory_vars.items()},
            "preferred_plant": self.preferred_var.get(),
            "optimization_mode": self.optimization_mode.get()
        }
        save_config(config)

    def update_language_display(self):
        """Update the language combobox to show the correct display name"""
        if hasattr(self, 'lang_combo'):
            current_display = next((name for code, name in self.lang_options if code == self.lang_manager.current_language_code), "English")
            self.lang_combo.set(current_display)

    def _build_ui(self):
        """Build the main UI structure"""
        self.geometry("1200x800")
        
        # Create main frames
        self.ctrl = ttk.Frame(self)
        self.ctrl.pack(side=tk.LEFT, fill=tk.Y, padx=8, pady=8)
        
        self.right = ttk.Frame(self)
        self.right.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)
        
        # Status bar
        self.status = ttk.Label(self.right, text=f"{self.get_text('ready')} | {self.get_text('created_by')}")
        self.status.pack(side=tk.BOTTOM, fill=tk.X)
        
        # Canvas
        self.canvas = tk.Canvas(self.right, bg="#1b2430")
        self.canvas.pack(fill=tk.BOTH, expand=True)
        self.canvas.bind("<Button-1>", self.on_canvas_click)
        self.canvas.bind("<Motion>", self.on_canvas_hover)
        self.canvas.bind("<Leave>", self.on_canvas_leave)
        
        # Track hover state
        self.hover_cell = None
        self.hover_overlays = []
        
        # Build the control panel
        self.build_controls()

    def build_controls(self):
        """Build the control panel UI"""
        # Clear existing controls
        for widget in self.ctrl.winfo_children():
            widget.destroy()
            
        # Settings box
        settings_box = ttk.LabelFrame(self.ctrl, text=self.get_text("settings"))
        settings_box.pack(fill=tk.X, pady=6)
        
        # Language selection
        ttk.Label(settings_box, text=self.get_text("language")).grid(row=0, column=0, sticky="w")
        
        # Build language options dynamically from loaded languages
        self.lang_options = []
        for code, lang_data in LANGUAGES.items():
            name = lang_data.get('language_name', code.upper())
            self.lang_options.append((code, name))
        
        # Sort by language name for better UX
        self.lang_options.sort(key=lambda x: x[1])
        
        # Create combobox with display names
        self.lang_combo = ttk.Combobox(settings_box, state="readonly", width=12)
        self.lang_combo['values'] = [name for _, name in self.lang_options]
        
        # Set current display value
        current_display = next((name for code, name in self.lang_options if code == self.lang_manager.current_language_code), "English")
        self.lang_combo.set(current_display)
        
        self.lang_combo.bind("<<ComboboxSelected>>", lambda e: self.on_language_change())
        self.lang_combo.grid(row=0, column=1, sticky="ew", padx=(5,0))
        
        # Grid size controls
        ttk.Label(settings_box, text=self.get_text("rows")).grid(row=1, column=0, sticky="w")
        ttk.Spinbox(settings_box, from_=1, to=30, textvariable=self.rows_var, 
                   width=6, command=self.on_grid_change).grid(row=1, column=1, sticky="ew", padx=(5,0))
        ttk.Label(settings_box, text=self.get_text("cols")).grid(row=2, column=0, sticky="w")
        ttk.Spinbox(settings_box, from_=1, to=30, textvariable=self.cols_var, 
                   width=6, command=self.on_grid_change).grid(row=2, column=1, sticky="ew", padx=(5,0))
        
        settings_box.columnconfigure(1, weight=1)

        # Inventory box
        self._build_inventory_section()
        
        # Preferred plant box
        self._build_preferred_plant_section()

        # Optimization mode selection
        self._build_optimization_section()

        # Buttons
        self._build_buttons_section()

        # Description box
        self._build_description_section()

    def _build_inventory_section(self):
        """Build the inventory section of the control panel"""
        inv_box = ttk.LabelFrame(self.ctrl, text=self.get_text("available_seeds"))
        inv_box.pack(fill=tk.BOTH, expand=False, pady=6)
        
        # Create a scrollable frame for the inventory
        canvas = tk.Canvas(inv_box, height=200)
        scrollbar = ttk.Scrollbar(inv_box, orient="vertical", command=canvas.yview)
        scrollable_frame = ttk.Frame(canvas)
        
        scrollable_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )
        
        canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)
        
        # Mouse wheel scrolling
        def _on_mousewheel(event):
            canvas.yview_scroll(int(-1*(event.delta/120)), "units")
        
        canvas.bind("<MouseWheel>", _on_mousewheel)
        scrollable_frame.bind("<MouseWheel>", _on_mousewheel)
        
        # Add crops with images and spinboxes
        for i, name in enumerate(sorted(CROPS.keys())):
            row_frame = ttk.Frame(scrollable_frame)
            row_frame.pack(fill=tk.X, pady=1)
            
            # Add image if available
            if name in self.crop_images:
                img_label = tk.Label(row_frame, image=self.crop_images[name])
                img_label.pack(side=tk.LEFT, padx=(2, 5))
            else:
                # Placeholder if no image
                placeholder = tk.Label(row_frame, text="🌱", font=("Arial", 12))
                placeholder.pack(side=tk.LEFT, padx=(2, 5))
            
            # Crop name - use localized name
            localized_name = self.get_crop_name(name)
            name_label = ttk.Label(row_frame, text=localized_name, width=16)
            name_label.pack(side=tk.LEFT)
            
            # Spinbox
            spinbox = ttk.Spinbox(row_frame, from_=0, to=999, textvariable=self.inventory_vars[name], width=6)
            spinbox.pack(side=tk.RIGHT, padx=(5, 2))
        
        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")

    def _build_preferred_plant_section(self):
        """Build the preferred plant selection section"""
        pref_box = ttk.LabelFrame(self.ctrl, text=self.get_text("preferred_plant"))
        pref_box.pack(fill=tk.X, pady=6)
        
        # Create list of localized crop names for combobox
        localized_crop_names = [(name, self.get_crop_name(name)) for name in sorted(CROPS.keys())]
        crop_display_values = [display_name for _, display_name in localized_crop_names]
        
        self.pref_combo = ttk.Combobox(pref_box, values=crop_display_values, state="readonly")
        
        # Set current selection based on preferred_var
        current_pref = self.preferred_var.get()
        current_display = self.get_crop_name(current_pref)
        if current_display in crop_display_values:
            self.pref_combo.set(current_display)
        else:
            self.pref_combo.set(crop_display_values[0] if crop_display_values else "")
        
        def on_pref_change(event):
            selected_display = self.pref_combo.get()
            # Find the original crop name for the selected display name
            for orig_name, display_name in localized_crop_names:
                if display_name == selected_display:
                    self.preferred_var.set(orig_name)
                    break
            self.save_current_config()
        
        self.pref_combo.bind("<<ComboboxSelected>>", on_pref_change)
        self.pref_combo.pack(fill=tk.X)

    def _build_optimization_section(self):
        """Build the optimization mode selection section"""
        opt_box = ttk.LabelFrame(self.ctrl, text=self.get_text("optimization_mode"))
        opt_box.pack(fill=tk.X, pady=6)
        modes = [
            ("balanced", self.get_text("balanced")),
            ("low_maintenance", self.get_text("low_maintenance")),
            ("max_harvest", self.get_text("max_harvest")),
            ("max_quality", self.get_text("max_quality"))
        ]
        for value, text in modes:
            ttk.Radiobutton(opt_box, text=text, variable=self.optimization_mode, value=value).pack(anchor="w")

    def _build_buttons_section(self):
        """Build the buttons section"""
        btn_box = ttk.Frame(self.ctrl)
        btn_box.pack(fill=tk.X, pady=6)
        
        # Create buttons with tooltips
        auto_fill_btn = ttk.Button(btn_box, text=self.get_text("auto_fill"), command=self.on_generate)
        auto_fill_btn.pack(fill=tk.X)
        create_tooltip(auto_fill_btn, self.get_text("tooltip_auto_fill"))
        
        optimize_btn = ttk.Button(btn_box, text=self.get_text("optimize"), command=self.on_optimize)
        optimize_btn.pack(fill=tk.X, pady=4)
        create_tooltip(optimize_btn, self.get_text("tooltip_optimize"))
        
        add_all_btn = ttk.Button(btn_box, text=self.get_text("add_all_seeds"), command=self.on_add_all_seeds)
        add_all_btn.pack(fill=tk.X, pady=2)
        create_tooltip(add_all_btn, self.get_text("tooltip_add_all"))
        
        clear_btn = ttk.Button(btn_box, text=self.get_text("clear"), command=self.on_clear)
        clear_btn.pack(fill=tk.X)
        create_tooltip(clear_btn, self.get_text("tooltip_clear"))

    def _build_description_section(self):
        """Build the description section"""
        info_box = ttk.LabelFrame(self.ctrl, text=self.get_text("description"))
        info_box.pack(fill=tk.BOTH, pady=6, expand=True)
        
        # Create scrollable text widget for description
        info_canvas = tk.Canvas(info_box, height=150)
        info_scrollbar = ttk.Scrollbar(info_box, orient="vertical", command=info_canvas.yview)
        info_scrollable_frame = ttk.Frame(info_canvas)
        
        info_scrollable_frame.bind(
            "<Configure>",
            lambda e: info_canvas.configure(scrollregion=info_canvas.bbox("all"))
        )
        
        info_canvas.create_window((0, 0), window=info_scrollable_frame, anchor="nw")
        info_canvas.configure(yscrollcommand=info_scrollbar.set)
        
        # Mouse wheel scrolling for info
        def _on_info_mousewheel(event):
            info_canvas.yview_scroll(int(-1*(event.delta/120)), "units")
        
        info_canvas.bind("<MouseWheel>", _on_info_mousewheel)
        info_scrollable_frame.bind("<MouseWheel>", _on_info_mousewheel)
        
        info_label = tk.Label(info_scrollable_frame, text=self.get_text("description_text"), 
                             justify=tk.LEFT, anchor="nw", wraplength=260, font=("Arial", 8))
        info_label.pack(fill=tk.BOTH, expand=True, anchor="nw")
        
        info_canvas.pack(side="left", fill="both", expand=True)
        info_scrollbar.pack(side="right", fill="y")

    def rebuild_ui(self):
        """Rebuild UI with current language"""
        self.build_controls()
        self.status.config(text=f"{self.get_text('ready')} | {self.get_text('created_by')}")
        # Update language combobox display
        self.update_language_display()
        
        # Track hover state
        self.hover_cell = None
        self.hover_overlays = []

    def on_grid_change(self):
        """Handle grid size changes"""
        r = self.rows_var.get(); c = self.cols_var.get()
        self.garden = Garden(r, c); self.redraw()
        self.save_current_config()

    def on_add_all_seeds(self):
        """Add all available crops to inventory with a reasonable amount"""
        for name in CROPS.keys():
            # Set different amounts based on plant size and type
            if CROPS[name]["size"] == (3, 3):  # Large plants like Apple
                self.inventory_vars[name].set(2)
            elif CROPS[name]["size"] == (2, 2):  # Medium plants
                self.inventory_vars[name].set(4)
            else:  # Small plants
                self.inventory_vars[name].set(8)
        self.status.config(text=f"{self.get_text('all_seeds_added')} | {self.get_text('created_by')}")

    def on_generate(self):
        """Generate garden layout"""
        inv = {k: max(0, v.get()) for k, v in self.inventory_vars.items()}
        pref = self.preferred_var.get()
        opt_mode = self.optimization_mode.get()
        self.garden.clear(); 
        greedy_fill_optimized(self.garden, inv, pref, opt_mode)
        total, metrics = score_garden_optimized(self.garden, pref, opt_mode)
        self.status.config(text=f"{self.get_text('generated')} ({opt_mode}) - {self.get_text('score')}: {metrics['total_score']} | {self.get_text('created_by')}")
        self.redraw()

    def on_optimize(self):
        """Optimize garden layout"""
        pref = self.preferred_var.get()
        opt_mode = self.optimization_mode.get()
        self.garden, best_score = local_search_optimized(self.garden, pref, opt_mode, iterations=4000)
        self.status.config(text=f"{self.get_text('optimized')} ({opt_mode}) - {self.get_text('score')}: {round(best_score,3)} | {self.get_text('created_by')}")
        self.redraw()
        self.save_current_config()

    def on_clear(self):
        """Clear garden"""
        self.garden.clear(); self.redraw()

    def cell_at_pixel(self, x, y):
        """Convert pixel coordinates to grid cell"""
        W = self.canvas.winfo_width(); H = self.canvas.winfo_height()
        pad = 10
        
        # Calculate same cell size as in redraw
        available_w = W - 2*pad
        available_h = H - 2*pad
        max_cell_by_width = available_w // max(1, self.garden.cols)
        max_cell_by_height = available_h // max(1, self.garden.rows)
        cell_size = min(max_cell_by_width, max_cell_by_height, 120)
        cell_size = max(cell_size, 30)
        
        # Apply same size adjustments as in redraw
        total_cells = self.garden.rows * self.garden.cols
        if total_cells <= 25:
            cell_size = min(max_cell_by_width, max_cell_by_height, 150)
        elif total_cells <= 64:
            cell_size = min(max_cell_by_width, max_cell_by_height, 100)
        
        # Center the grid
        total_w = cell_size * self.garden.cols
        total_h = cell_size * self.garden.rows
        start_x = (W - total_w) // 2
        start_y = (H - total_h) // 2
        
        if x < start_x or y < start_y:
            return None
        c = (x - start_x) // cell_size
        r = (y - start_y) // cell_size
        if r < 0 or r >= self.garden.rows or c < 0 or c >= self.garden.cols:
            return None
        return int(r), int(c)

    def on_canvas_click(self, event):
        """Handle canvas click events"""
        cell = self.cell_at_pixel(event.x, event.y)
        if cell is None: return
        r, c = cell
        pid = self.garden.grid[r][c]
        if pid is not None:
            self.garden.remove(pid); self.redraw(); return
        name = self.preferred_var.get()
        if not self.garden.can_place(name, r, c):
            localized_name = self.get_crop_name(name)
            messagebox.showwarning(self.get_text("cannot_place"), 
                                 f"{localized_name} {self.get_text('collision_error')}")
            return
        self.garden.place(name, r, c); self.redraw()

    def on_canvas_hover(self, event):
        """Handle canvas hover events"""
        cell = self.cell_at_pixel(event.x, event.y)
        if cell != self.hover_cell:
            self.hover_cell = cell
            self.clear_hover_overlays()
            if cell is not None:
                self.show_hover_effects(cell)

    def on_canvas_leave(self, event):
        """Handle canvas leave events"""
        self.hover_cell = None
        self.clear_hover_overlays()

    def clear_hover_overlays(self):
        """Clear hover effect overlays"""
        for overlay_id in self.hover_overlays:
            self.canvas.delete(overlay_id)
        self.hover_overlays.clear()

    def show_hover_effects(self, cell):
        """Show hover effects for a cell"""
        r, c = cell
        pid = self.garden.grid[r][c]
        if pid is None:
            return
            
        plant_meta = self.garden.placements[pid]
        plant_name = plant_meta["name"]
        effect = CROPS[plant_name]["effect"]
        
        if effect is None:
            return
            
        # Calculate grid parameters (same as redraw)
        W = self.canvas.winfo_width(); H = self.canvas.winfo_height()
        pad = 10
        available_w = W - 2*pad
        available_h = H - 2*pad
        max_cell_by_width = available_w // max(1, self.garden.cols)
        max_cell_by_height = available_h // max(1, self.garden.rows)
        cell_size = min(max_cell_by_width, max_cell_by_height, 120)
        cell_size = max(cell_size, 30)
        
        total_cells = self.garden.rows * self.garden.cols
        if total_cells <= 25:
            cell_size = min(max_cell_by_width, max_cell_by_height, 150)
        elif total_cells <= 64:
            cell_size = min(max_cell_by_width, max_cell_by_height, 100)
        
        total_w = cell_size * self.garden.cols
        total_h = cell_size * self.garden.rows
        start_x = (W - total_w) // 2
        start_y = (H - total_h) // 2
        
        # Highlight the plant itself with a thick border
        x0 = start_x + plant_meta["c"] * cell_size
        y0 = start_y + plant_meta["r"] * cell_size
        x1 = start_x + (plant_meta["c"] + plant_meta["w"]) * cell_size - 2
        y1 = start_y + (plant_meta["r"] + plant_meta["h"]) * cell_size - 2
        
        highlight_id = self.canvas.create_rectangle(x0, y0, x1, y1, outline="#FFD700", width=4, fill="")
        self.hover_overlays.append(highlight_id)
        
        # Show affected neighboring cells
        from garden import ortho_neighbors
        affected_cells = set()
        for pr in range(plant_meta["r"], plant_meta["r"] + plant_meta["h"]):
            for pc in range(plant_meta["c"], plant_meta["c"] + plant_meta["w"]):
                for nr, nc in ortho_neighbors(pr, pc, self.garden.rows, self.garden.cols):
                    n_pid = self.garden.grid[nr][nc]
                    if n_pid != pid:  # Don't highlight the plant itself
                        affected_cells.add((nr, nc))
        
        # Draw overlay on affected cells
        for ar, ac in affected_cells:
            ax0 = start_x + ac * cell_size
            ay0 = start_y + ar * cell_size
            ax1 = ax0 + cell_size - 1
            ay1 = ay0 + cell_size - 1
            
            # Different colors for boost vs debuff
            n_pid = self.garden.grid[ar][ac]
            if n_pid is not None:
                n_name = self.garden.placements[n_pid]["name"]
                if n_name == plant_name:
                    # Same species = debuff (red overlay)
                    overlay_id = self.canvas.create_rectangle(ax0, ay0, ax1, ay1, 
                                                            outline="#FF4444", width=2, 
                                                            fill="#FF4444", stipple="gray25")
                else:
                    # Different species = boost (green overlay)  
                    overlay_id = self.canvas.create_rectangle(ax0, ay0, ax1, ay1,
                                                            outline="#44FF44", width=2,
                                                            fill="#44FF44", stipple="gray25")
            else:
                # Empty cell that would get boost
                overlay_id = self.canvas.create_rectangle(ax0, ay0, ax1, ay1,
                                                        outline="#44FF44", width=2,
                                                        fill="#44FF44", stipple="gray50")
            self.hover_overlays.append(overlay_id)
        
        # Show effect description
        effect_names = {
            "harvest": f"🟡 {self.get_text('harvest_boost_name')}",
            "quality": f"🟣 {self.get_text('quality_boost_name')}", 
            "growth": f"🟦 {self.get_text('growth_boost_name')}",
            "water": f"💧 {self.get_text('water_boost_name')}",
            "weed": f"🌿 {self.get_text('weed_boost_name')}"
        }
        
        localized_plant_name = self.get_crop_name(plant_name)
        boost_text = self.get_text('boost_tooltip')
        description = f"{localized_plant_name}\n{effect_names.get(effect, effect)}\n{boost_text}"
        
        # Position tooltip in top-left corner
        tooltip_x = 10
        tooltip_y = 10
        
        # Create tooltip background
        bg_id = self.canvas.create_rectangle(tooltip_x, tooltip_y, tooltip_x + 140, tooltip_y + 50,
                                           fill="#2C3E50", outline="#34495E", width=2)
        self.hover_overlays.append(bg_id)
        
        # Create tooltip text
        text_id = self.canvas.create_text(tooltip_x + 5, tooltip_y + 5, text=description, 
                                        anchor="nw", fill="#ECF0F1", font=("Arial", 8, "bold"))
        self.hover_overlays.append(text_id)

    def redraw(self):
        """Redraw the garden canvas"""
        self.canvas.delete("all")
        W = self.canvas.winfo_width(); H = self.canvas.winfo_height()
        pad = 10
        if self.garden.cols == 0 or self.garden.rows == 0: return
        
        # Calculate square cell size (1:1 aspect ratio) - optimized for better space usage
        available_w = W - 2*pad
        available_h = H - 2*pad
        
        # Try to use more space by increasing maximum cell size
        max_cell_by_width = available_w // max(1, self.garden.cols)
        max_cell_by_height = available_h // max(1, self.garden.rows)
        cell_size = min(max_cell_by_width, max_cell_by_height, 120)
        cell_size = max(cell_size, 30)
        
        # If grid is very small, allow larger cells
        total_cells = self.garden.rows * self.garden.cols
        if total_cells <= 25:  # 5x5 or smaller
            cell_size = min(max_cell_by_width, max_cell_by_height, 150)
        elif total_cells <= 64:  # 8x8 or smaller  
            cell_size = min(max_cell_by_width, max_cell_by_height, 100)
        
        # Center the grid
        total_w = cell_size * self.garden.cols
        total_h = cell_size * self.garden.rows
        start_x = (W - total_w) // 2
        start_y = (H - total_h) // 2
        
        # Draw grid
        for r in range(self.garden.rows):
            for c in range(self.garden.cols):
                x0 = start_x + c * cell_size; y0 = start_y + r * cell_size
                x1 = x0 + cell_size - 1; y1 = y0 + cell_size - 1
                self.canvas.create_rectangle(x0, y0, x1, y1, outline="#444", width=1)
        
        # Draw plants
        for pid, meta in self.garden.placements.items():
            x0 = start_x + meta["c"] * cell_size; y0 = start_y + meta["r"] * cell_size
            x1 = start_x + (meta["c"] + meta["w"]) * cell_size - 2; y1 = start_y + (meta["r"] + meta["h"]) * cell_size - 2
            name = meta["name"]; color = COLOR.get(name, "#95a5a6")
            localized_name = self.get_crop_name(name)
            self.canvas.create_rectangle(x0, y0, x1, y1, fill=color, outline="#111", width=2)
            
            # Add image if available and cell is large enough
            center_x, center_y = (x0+x1)//2, (y0+y1)//2
            if name in self.crop_images and cell_size >= 40:
                # Show image in the center-top
                img_y = y0 + cell_size//3
                self.canvas.create_image(center_x, img_y, image=self.crop_images[name])
                # Text below image
                text_y = y0 + cell_size - 10
                font_size = max(8, min(16, cell_size//7))
                self.canvas.create_text(center_x, text_y, text=localized_name[:10], fill="#fff", font=("Arial", font_size, "bold"))
            else:
                # Just text, adjust font size based on cell size
                font_size = max(7, min(18, cell_size//4))
                # Split long names into two lines for better readability
                if len(localized_name) > 8 and cell_size >= 50:
                    words = localized_name.split()
                    if len(words) > 1:
                        line1 = words[0]
                        line2 = " ".join(words[1:])[:10]
                        self.canvas.create_text(center_x, center_y - font_size//2, text=line1, fill="#fff", font=("Arial", font_size))
                        self.canvas.create_text(center_x, center_y + font_size//2, text=line2, fill="#fff", font=("Arial", font_size))
                    else:
                        self.canvas.create_text(center_x, center_y, text=localized_name[:12], fill="#fff", font=("Arial", font_size))
                else:
                    self.canvas.create_text(center_x, center_y, text=localized_name[:10], fill="#fff", font=("Arial", font_size))
        
        # Update status
        pref = self.preferred_var.get()
        opt_mode = self.optimization_mode.get()
        total, metrics = score_garden_optimized(self.garden, pref, opt_mode)
        stat_text = f"{self.get_text('score')}: {metrics['total_score']} | {opt_mode} | {self.get_text('created_by')}"
        self.status.config(text=stat_text)


def main():
    """Main entry point"""
    app = App()
    app.mainloop()


if __name__ == '__main__':
    main()
