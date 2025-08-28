# 🌟 Palia Garden Optimizer 🌟

**Multi-language garden planner with crop optimization for Palia**  
*Created by: Kallós László 2025, Palia 0.194*

## 📋 Features

### 🌍 **Multi-Language Support**
- **Dynamic Language System**: Supports unlimited languages through JSON files
- **Currently Available**: English, Deutsch, Magyar, Español, Français
- **Localized Crop Names**: All plant names appear in your selected language
- **Community Contributions**: Anyone can add new languages!

### 🎯 **Smart Garden Optimization**
- **Multiple Optimization Modes**:
  - 🏆 **Balanced**: General purpose optimization
  - 🏠 **Low Maintenance**: Focus on water retention and weed protection
  - 🌾 **Max Harvest**: Maximize crop yield
  - 💎 **Max Quality**: Prioritize crop quality
- **Intelligent Plant Placement**: Considers size, effects, and synergies
- **Real-time Scoring**: See optimization scores instantly

### 🌱 **Comprehensive Plant Database**
All Palia crops with accurate sizes and boost effects:
- **3×3 Large**: Apple Tree (harvest boost)
- **2×2 Medium**: Butterfly Bean, Blueberry, Rockhopper Pumpkin, Spicy Pepper
- **1×1 Small**: All other crops with various effects

### 🎨 **Professional Interface**
- **Visual Plant Recognition**: Thumbnails for each crop (24×24px)
- **Interactive Canvas**: Click to place/remove plants, hover for effects
- **Color-coded Effects**: Each boost type has distinct colors
- **Hover Tooltips**: Real-time effect visualization
- **Configuration Persistence**: Saves your preferences

## 📁 Project Structure

The project has been refactored into a modular structure for better maintainability:

```
palia/
├── palia_garden_optimizer.py  # Main application
├── config.py                  # Configuration management
├── crops.py                   # Crop data and constants
├── garden.py                  # Garden logic and optimization algorithms
├── language.py                # Language management system
├── ui_utils.py                # UI utilities and components
├── lang/                      # Language files directory
│   ├── en.json               # English
│   ├── de.json               # German
│   ├── hu.json               # Hungarian
│   ├── es.json               # Spanish
│   └── fr.json               # French
├── pics/                      # Crop images (optional)
└── README.md                  # This file
```

## 🚀 Quick Start

### Prerequisites
```bash
pip install tkinter pillow
```

### Running the Application
```bash
python palia_garden_optimizer.py
```

## 🌍 Adding New Languages

Want to contribute a new language? It's easy!

1. **Create Language File**: Copy `lang/en.json` to `lang/[language_code].json`
2. **Translate Content**: Translate all text values (keep keys unchanged)
3. **Update Metadata**: Set `language_name` and `language_code`
4. **Translate Crops**: Update the `crops` section with localized plant names
5. **Test**: Restart the application - your language appears automatically!

### Language File Template
```json
{
    "language_name": "Your Language Name",
    "language_code": "xx",
    "creator_format": "Your Name",
    "title": "Palia Garden Optimizer (Multi-sized Plants)",
    "crops": {
        "Apple": "Localized Apple Name",
        "Corn": "Localized Corn Name",
        ...
    },
    ...
}
```

## 🎮 How to Use

### 1️⃣ **Setup Garden**
- Set desired grid size (rows × columns)
- Choose your preferred language
- Add crops to inventory using spinboxes

### 2️⃣ **Choose Strategy**
- Select preferred plant (gets priority placement)
- Pick optimization mode based on your goals
- Use "Add All Seeds" for quick testing

### 3️⃣ **Generate & Optimize**
- Click "Auto Fill" for initial placement
- Click "Optimize" to improve the layout
- Click individual cells to manually place/remove plants

### 4️⃣ **Understand Results**
- **Green overlays**: Boost effects when hovering
- **Red overlays**: Penalty areas (same species adjacent)
- **Score display**: Higher is better
- **Color coding**: Each effect type has distinct colors

## 🔧 Technical Details

### Module Overview
- **`config.py`**: JSON-based configuration persistence
- **`crops.py`**: Crop definitions, colors, and scoring weights
- **`garden.py`**: Garden grid management and optimization algorithms
- **`language.py`**: Dynamic language loading with robust fallback
- **`ui_utils.py`**: UI components like tooltips and image loading
- **`palia_garden_optimizer.py`**: Main application with modular imports

### Boost Effects System
- **Harvest** (Yellow): More crops per harvest
- **Quality** (Purple): Higher quality crops  
- **Water** (Blue): Reduced watering needs
- **Weed** (Green): Prevents weed growth
- **Growth** (Dark Blue): Faster growth time
- **Neutral** (Gray): No special effects

### Scoring Algorithm
- **Positive**: Different species adjacency bonuses
- **Negative**: Same species adjacency penalties
- **Bonus**: Preferred plant placement rewards
- **Weighted**: Different modes prioritize different effects

## 🐛 Error Handling

The application includes robust error handling:
- **Missing translations**: Falls back to English, then to key name
- **Invalid language files**: Logs errors and continues
- **Missing images**: Shows placeholder icons
- **Configuration errors**: Uses safe defaults

## 📊 Performance

### Optimization Algorithms
- **Greedy Fill**: Fast initial placement O(n²)
- **Local Search**: Iterative improvement with 3000-4000 iterations
- **Smart Prioritization**: Effect-based and size-based ordering

### Memory Usage
- **Lightweight**: Minimal memory footprint
- **Efficient**: Only loads needed images and languages
- **Scalable**: Supports gardens up to 30×30

## 🤝 Contributing

### Code Contributions
1. Fork the repository
2. Work on the modular version (`palia_garden_optimizer.py`)
3. Follow existing code structure and patterns
4. Test thoroughly with different languages and settings

### Language Contributions
1. Create new JSON file in `lang/` directory
2. Translate all keys completely
3. Test in application
4. Submit with proper language metadata

### Bug Reports
- Include language setting and OS information
- Describe steps to reproduce
- Attach configuration file if relevant

## 📈 Future Enhancements

### Planned Features
- **Garden Templates**: Save and load layouts
- **Advanced Algorithms**: Genetic algorithms for large gardens
- **Plant Growth Simulation**: Time-based optimization
- **Community Sharing**: Share optimized layouts
- **Mobile Support**: Touch-friendly interface

### Community Requests
- **More Languages**: Expanding international support
- **Custom Crops**: Support for modded content
- **Export Features**: Save layouts as images
- **Statistics**: Detailed analytics and comparisons

## 📄 License

Open source project - feel free to modify and distribute!

## 🙏 Acknowledgments

- **Palia Community**: For game data and testing
- **Contributors**: Language translators and testers  
- **Singularity 6**: For creating Palia

---

*Happy gardening in Palia! 🌱*
