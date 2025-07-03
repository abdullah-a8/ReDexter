# ReDexter - Rclone Decrypter

A modern PyQt6-based GUI application for decrypting files encrypted with rclone's crypt remote.

## Features

- **Modern Typography**: Professional font hierarchy with recommended modern fonts
- **Multiple Themes**: Choose from 7 different themes including new Modern Pro and Modern Light
- **Drag & Drop Support**: Easy file selection through drag and drop
- **Rclone Config Integration**: Load credentials directly from rclone configuration files
- **Batch Processing**: Decrypt multiple files at once
- **Progress Tracking**: Real-time progress updates during decryption

## New Typography Features

### Recommended Fonts
- **Inter** (Primary) - Modern UI font designed for digital interfaces
- **SF Pro Display** - Apple's system font (macOS)
- **Segoe UI Variable** - Microsoft's modern system font (Windows 11)
- **Roboto** - Google's universal font (fallback)

### Enhanced Themes
- **Modern Pro**: Professional dark theme with improved typography
- **Modern Light**: Clean light theme with modern font stack
- Plus 5 additional themes: Dark, Light, True Black, Mocha Catppuccin, Dracula

## Installation

1. **Install Dependencies**
   ```bash
   pip install -r requirements.txt
   ```

2. **Install Recommended Fonts** (Optional but recommended)
   ```bash
   # Run the automated installer
   ./install_fonts.sh
   
   # Or install manually:
   # - Inter: https://github.com/rsms/inter
   # - Roboto: https://fonts.google.com/specimen/Roboto
   ```

3. **Run the Application**
   ```bash
   python main.py
   ```

## Usage

1. **Select Theme**: Go to the Theme tab and choose your preferred theme
2. **Load Configuration**: Import your rclone config file or enter credentials manually
3. **Add Files**: Drag and drop files or use the Browse button
4. **Decrypt**: Click "Decrypt Files" to start the process

## Typography Improvements

### Before
- Monospace font for all UI elements
- No visual hierarchy
- Single font weight
- Basic styling

### After
- Professional font stack with fallbacks
- Clear typography hierarchy
- Multiple font weights for visual distinction
- Enhanced spacing and modern styling

## Requirements

- Python 3.6+
- PyQt6
- Additional packages listed in `requirements.txt`

## Font Installation

For the best typography experience, install the recommended fonts:

**Fedora/RHEL:**
```bash
sudo dnf install google-roboto-fonts
# Inter font will be installed automatically by the script
```

**Ubuntu/Debian:**
```bash
sudo apt install fonts-roboto fonts-inter
```

**Arch Linux:**
```bash
sudo pacman -S ttf-roboto
# For Inter: yay -S ttf-inter (if using AUR)
```

## License

This project is released under the MIT License.

---

*Enjoy the improved typography and modern interface!* 