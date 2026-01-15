# PathOfCount

Overlay counter for Path of Exile and other games.

## Features
- ✅ Multiple counters per game
- ✅ Persistent data between sessions
- ✅ Hotkeys support
- ✅ Click-through mode
- ✅ Movable overlay

## Download

Download the latest release: [Releases](https://github.com/YOUR_USERNAME/PathOfCount/releases)

## Installation

1. Download `PathOfCount.exe` from releases
2. Run the executable
3. (Optional) Add to Windows startup

## Usage

### Hotkeys
- `Ctrl+Alt+M` - Toggle move mode
- `Ctrl+Alt+L` - Toggle click-through
- `Ctrl+Alt+K` - Quit application

### Controls
- Click `☰` to switch between counters
- Click `⚙` for settings menu
- Click counter name for rename/delete options

## Building from source

### Requirements
- Python 3.10+
- PyQt6
- pynput
- psutil

### Steps
```bash
# Clone repository
git clone https://github.com/YOUR_USERNAME/PathOfCount.git
cd PathOfCount

# Install dependencies
pip install -r requirements.txt

# Run from source
python src/main.py

# Build executable
python build_exe.py
```

## License
MIT License 
