original_dark = """
QWidget {
    background-color: #1E1E1E;
    color: #E0E0E0;
    font-family: 'MartianMono Nerd Font', 'Segoe UI', sans-serif;
    font-size: 13pt;
}
QLabel { color: #E0E0E0; }
QLineEdit, QListWidget { background-color: #2D2D2D; border: 1px solid #3C3C3C; padding: 6px; border-radius: 8px; }
QPushButton { background-color: #007ACC; border: none; color: #FFFFFF; padding: 8px 16px; border-radius: 8px; }
QPushButton:hover { background-color: #005A9E; }
QComboBox { background-color: #2D2D2D; border: 1px solid #3C3C3C; padding: 6px; border-radius: 8px; }
QComboBox::drop-down { border: none; }
"""

light_theme = """
QWidget {
    background-color: #F5F5F5;
    color: #2E2E2E;
    font-family: 'MartianMono Nerd Font', 'Segoe UI', sans-serif;
    font-size: 13pt;
}
QLabel { color: #2E2E2E; }
QLineEdit, QListWidget { background-color: #FFFFFF; border: 1px solid #CCCCCC; padding: 6px; border-radius: 8px; }
QPushButton { background-color: #007ACC; border: none; color: #FFFFFF; padding: 8px 16px; border-radius: 8px; }
QPushButton:hover { background-color: #005A9E; }
QComboBox { background-color: #FFFFFF; border: 1px solid #CCCCCC; padding: 6px; border-radius: 8px; }
QComboBox::drop-down { border: none; }
"""

true_black = """
QWidget {
    background-color: #000000;
    color: #FFFFFF;
    font-family: 'MartianMono Nerd Font', 'Segoe UI', sans-serif;
    font-size: 13pt;
}
QLabel { color: #FFFFFF; }
QLineEdit, QListWidget { background-color: #000000; border: 1px solid #333333; padding: 6px; border-radius: 8px; }
QPushButton { background-color: #333333; border: none; color: #FFFFFF; padding: 8px 16px; border-radius: 8px; }
QPushButton:hover { background-color: #555555; }
QComboBox { background-color: #000000; border: 1px solid #333333; padding: 6px; border-radius: 8px; }
QComboBox::drop-down { border: none; }
"""

mocha_catppuccin = """
QWidget {
    background-color: #1e1e2e;
    color: #c6d0f5;
    font-family: 'MartianMono Nerd Font', 'Segoe UI', sans-serif;
    font-size: 13pt;
}
QLabel { color: #c6d0f5; }
QLineEdit, QListWidget {
    background-color: #2a273f;
    border: 1px solid #36304a;
    padding: 6px;
    border-radius: 8px;
}
QPushButton {
    background-color: #f5c2e7;
    border: none;
    color: #1e1e2e;
    padding: 8px 16px;
    border-radius: 8px;
}
QPushButton:hover { background-color: #f2a6cf; }
QComboBox {
    background-color: #2a273f;
    border: 1px solid #36304a;
    padding: 6px;
    border-radius: 8px;
}
QComboBox::drop-down { border: none; }
"""

dracula_theme = """
QWidget {
    background-color: #282a36;
    color: #f8f8f2;
    font-family: 'MartianMono Nerd Font', 'Segoe UI', sans-serif;
    font-size: 13pt;
}
QLabel { color: #f8f8f2; }
QLineEdit, QListWidget {
    background-color: #44475a;
    border: 1px solid #6272a4;
    padding: 6px;
    border-radius: 8px;
}
QPushButton {
    background-color: #bd93f9;
    border: none;
    color: #282a36;
    padding: 8px 16px;
    border-radius: 8px;
}
QPushButton:hover { background-color: #ff79c6; }
QComboBox {
    background-color: #44475a;
    border: 1px solid #6272a4;
    padding: 6px;
    border-radius: 8px;
}
QComboBox::drop-down { border: none; }
"""

modern_pro_theme = """
QWidget {
    background-color: #1a1a1a;
    color: #e6e6e6;
    font-family: 'Inter', 'SF Pro Display', 'Segoe UI Variable', 'Roboto', sans-serif;
    font-size: 12pt;
    font-weight: 400;
}

/* Tab Widget Styling */
QTabWidget::tab-bar {
    alignment: center;
}

QTabBar::tab {
    font-size: 13pt;
    font-weight: 500;
    padding: 10px 20px;
    margin-right: 4px;
    border-radius: 8px 8px 0px 0px;
    background-color: #2a2a2a;
    color: #b0b0b0;
}

QTabBar::tab:selected {
    background-color: #3a3a3a;
    color: #ffffff;
    font-weight: 600;
}

QTabBar::tab:hover:!selected {
    background-color: #333333;
    color: #d0d0d0;
}

/* Group Box Styling */
QGroupBox {
    font-size: 13pt;
    font-weight: 500;
    color: #ffffff;
    border: 2px solid #404040;
    border-radius: 10px;
    margin-top: 10px;
    padding-top: 10px;
}

QGroupBox::title {
    subcontrol-origin: margin;
    left: 15px;
    padding: 0 8px 0 8px;
    color: #ffffff;
    font-weight: 600;
}

/* Label Styling */
QLabel {
    color: #e6e6e6;
    font-size: 12pt;
    font-weight: 450;
}

/* Input Fields */
QLineEdit, QListWidget {
    background-color: #2a2a2a;
    border: 2px solid #404040;
    padding: 8px 12px;
    border-radius: 10px;
    font-size: 12pt;
    font-weight: 400;
    color: #ffffff;
    selection-background-color: #0066cc;
}

QLineEdit:focus, QListWidget:focus {
    border: 2px solid #0078d4;
    outline: none;
}

QLineEdit::placeholder {
    color: #808080;
    font-style: italic;
}

/* Button Styling */
QPushButton {
    background-color: #0078d4;
    border: none;
    color: #ffffff;
    padding: 10px 18px;
    border-radius: 10px;
    font-size: 12pt;
    font-weight: 500;
    min-height: 20px;
}

QPushButton:hover {
    background-color: #106ebe;
}

QPushButton:pressed {
    background-color: #005a9e;
}

QPushButton:disabled {
    background-color: #404040;
    color: #808080;
}

/* ComboBox Styling */
QComboBox {
    background-color: #2a2a2a;
    border: 2px solid #404040;
    padding: 8px 12px;
    border-radius: 10px;
    font-size: 12pt;
    font-weight: 400;
    color: #ffffff;
    min-width: 120px;
}

QComboBox:focus {
    border: 2px solid #0078d4;
}

QComboBox::drop-down {
    border: none;
    width: 20px;
}

QComboBox::down-arrow {
    image: none;
    border-left: 5px solid transparent;
    border-right: 5px solid transparent;
    border-top: 5px solid #e6e6e6;
    margin-right: 5px;
}

QComboBox QAbstractItemView {
    background-color: #2a2a2a;
    border: 2px solid #404040;
    border-radius: 8px;
    selection-background-color: #0078d4;
    color: #ffffff;
}

/* Tool Button Styling */
QToolButton {
    background-color: transparent;
    border: none;
    padding: 4px;
    border-radius: 6px;
}

QToolButton:hover {
    background-color: #404040;
}

QToolButton:pressed {
    background-color: #505050;
}

/* Progress Dialog */
QProgressDialog {
    font-size: 12pt;
    font-weight: 400;
}

/* Form Layout improvements */
QFormLayout QLabel {
    font-weight: 500;
    color: #ffffff;
}
"""

modern_light_theme = """
QWidget {
    background-color: #ffffff;
    color: #1a1a1a;
    font-family: 'Inter', 'SF Pro Display', 'Segoe UI Variable', 'Roboto', sans-serif;
    font-size: 12pt;
    font-weight: 400;
}

/* Tab Widget Styling */
QTabWidget::tab-bar {
    alignment: center;
}

QTabBar::tab {
    font-size: 13pt;
    font-weight: 500;
    padding: 10px 20px;
    margin-right: 4px;
    border-radius: 8px 8px 0px 0px;
    background-color: #f5f5f5;
    color: #666666;
}

QTabBar::tab:selected {
    background-color: #e6e6e6;
    color: #1a1a1a;
    font-weight: 600;
}

QTabBar::tab:hover:!selected {
    background-color: #eeeeee;
    color: #333333;
}

/* Group Box Styling */
QGroupBox {
    font-size: 13pt;
    font-weight: 500;
    color: #1a1a1a;
    border: 2px solid #d0d0d0;
    border-radius: 10px;
    margin-top: 10px;
    padding-top: 10px;
}

QGroupBox::title {
    subcontrol-origin: margin;
    left: 15px;
    padding: 0 8px 0 8px;
    color: #1a1a1a;
    font-weight: 600;
}

/* Label Styling */
QLabel {
    color: #1a1a1a;
    font-size: 12pt;
    font-weight: 450;
}

/* Input Fields */
QLineEdit, QListWidget {
    background-color: #ffffff;
    border: 2px solid #d0d0d0;
    padding: 8px 12px;
    border-radius: 10px;
    font-size: 12pt;
    font-weight: 400;
    color: #1a1a1a;
    selection-background-color: #0066cc;
}

QLineEdit:focus, QListWidget:focus {
    border: 2px solid #0078d4;
    outline: none;
}

QLineEdit::placeholder {
    color: #666666;
    font-style: italic;
}

/* Button Styling */
QPushButton {
    background-color: #0078d4;
    border: none;
    color: #ffffff;
    padding: 10px 18px;
    border-radius: 10px;
    font-size: 12pt;
    font-weight: 500;
    min-height: 20px;
}

QPushButton:hover {
    background-color: #106ebe;
}

QPushButton:pressed {
    background-color: #005a9e;
}

QPushButton:disabled {
    background-color: #cccccc;
    color: #666666;
}

/* ComboBox Styling */
QComboBox {
    background-color: #ffffff;
    border: 2px solid #d0d0d0;
    padding: 8px 12px;
    border-radius: 10px;
    font-size: 12pt;
    font-weight: 400;
    color: #1a1a1a;
    min-width: 120px;
}

QComboBox:focus {
    border: 2px solid #0078d4;
}

QComboBox::drop-down {
    border: none;
    width: 20px;
}

QComboBox::down-arrow {
    image: none;
    border-left: 5px solid transparent;
    border-right: 5px solid transparent;
    border-top: 5px solid #1a1a1a;
    margin-right: 5px;
}

QComboBox QAbstractItemView {
    background-color: #ffffff;
    border: 2px solid #d0d0d0;
    border-radius: 8px;
    selection-background-color: #0078d4;
    color: #1a1a1a;
}

/* Tool Button Styling */
QToolButton {
    background-color: transparent;
    border: none;
    padding: 4px;
    border-radius: 6px;
}

QToolButton:hover {
    background-color: #f0f0f0;
}

QToolButton:pressed {
    background-color: #e0e0e0;
}

/* Progress Dialog */
QProgressDialog {
    font-size: 12pt;
    font-weight: 400;
}

/* Form Layout improvements */
QFormLayout QLabel {
    font-weight: 500;
    color: #1a1a1a;
}
"""

THEMES = {
    "Dark": original_dark,
    "Light": light_theme,
    "True Black": true_black,
    "Mocha Catppuccin": mocha_catppuccin,
    "Dracula": dracula_theme,
    "Modern Pro": modern_pro_theme,
    "Modern Light": modern_light_theme,
}