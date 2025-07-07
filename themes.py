# Base theme template - all themes use this structure with different colors
def create_theme(colors):
    return f"""
QWidget {{
    background-color: {colors['bg_primary']};
    color: {colors['text_primary']};
    font-family: 'Inter', 'SF Pro Display', 'Segoe UI Variable', 'Roboto', sans-serif;
    font-size: 12pt;
    font-weight: 400;
}}

/* Group Box Styling */
QGroupBox {{
    font-size: 13pt;
    font-weight: 500;
    color: {colors['text_primary']};
    border: 1px solid {colors['border']};
    border-radius: 8px;
    margin-top: 10px;
    padding-top: 10px;
}}

QGroupBox::title {{
    subcontrol-origin: margin;
    left: 15px;
    padding: 0 8px 0 8px;
    color: {colors['text_primary']};
    font-weight: 600;
}}

/* Label Styling */
QLabel {{
    color: {colors['text_primary']};
    font-size: 12pt;
    font-weight: 450;
}}

/* Main Title (H1) */
QLabel[objectName="mainTitle"] {{
    color: {colors['text_primary']};
    font-size: 32pt;
    font-weight: 700;
    font-family: 'Inter', 'SF Pro Display', 'Segoe UI Variable', 'Roboto', sans-serif;
}}

/* Section Title (H1 Secondary) */
QLabel[objectName="sectionTitle"] {{
    color: {colors['text_primary']};
    font-size: 24pt;
    font-weight: 700;
    font-family: 'Inter', 'SF Pro Display', 'Segoe UI Variable', 'Roboto', sans-serif;
}}

/* Primary Text (H2) */
QLabel[objectName="primaryText"] {{
    color: {colors['text_primary']};
    font-size: 16pt;
    font-weight: 500;
    font-family: 'Inter', 'SF Pro Display', 'Segoe UI Variable', 'Roboto', sans-serif;
}}

/* Section Subtitle (H3) */
QLabel[objectName="sectionSubtitle"] {{
    color: {colors['text_primary']};
    font-size: 14pt;
    font-weight: 500;
    font-family: 'Inter', 'SF Pro Display', 'Segoe UI Variable', 'Roboto', sans-serif;
}}

/* Subtitle Text */
QLabel[objectName="subtitleText"] {{
    color: {colors['text_muted']};
    font-size: 14pt;
    font-weight: 400;
}}

/* Muted Text */
QLabel[objectName="mutedText"] {{
    color: {colors['text_muted']};
    font-size: 11pt;
    font-weight: 400;
}}

/* Icon Labels */
QLabel[objectName="iconLabel"] {{
    color: {colors['text_muted']};
}}

/* Input Fields */
QLineEdit, QListWidget {{
    background-color: {colors['bg_secondary']};
    border: 1px solid {colors['border']};
    padding: 8px 12px;
    border-radius: 8px;
    font-size: 12pt;
    font-weight: 400;
    color: {colors['text_primary']};
    selection-background-color: {colors['accent']};
}}

QLineEdit:focus, QListWidget:focus {{
    border: 1px solid {colors['accent']};
    outline: none;
}}

QLineEdit::placeholder {{
    color: {colors['text_muted']};
    font-style: italic;
}}

/* List Widget Items */
QListWidget::item {{
    padding: 8px 12px;
    border-radius: 6px;
    margin: 2px 0px;
    background-color: transparent;
}}

QListWidget::item:hover {{
    background-color: {colors['hover']};
}}

QListWidget::item:selected {{
    background-color: {colors['accent']};
    color: {colors['text_on_accent']};
    font-weight: 500;
}}

QListWidget::item:selected:hover {{
    background-color: {colors['accent_hover']};
}}

/* Button Styling */
QPushButton {{
    background-color: {colors['accent']};
    border: none;
    color: {colors['text_on_accent']};
    padding: 10px 18px;
    border-radius: 8px;
    font-size: 12pt;
    font-weight: 500;
    min-height: 20px;
}}

QPushButton:hover {{
    background-color: {colors['accent_hover']};
}}

QPushButton:pressed {{
    background-color: {colors['accent_pressed']};
}}

QPushButton:disabled {{
    background-color: {colors['disabled']};
    color: {colors['text_muted']};
}}

/* Primary Button Styling */
QPushButton[objectName="primaryButton"] {{
    background-color: {colors['accent']};
    border: none;
    color: {colors['text_on_accent']};
    padding: 10px 20px;
    border-radius: 8px;
    font-size: 12pt;
    font-weight: 500;
    min-height: 36px;
    min-width: 120px;
}}

QPushButton[objectName="primaryButton"]:hover {{
    background-color: {colors['accent_hover']};
}}

QPushButton[objectName="primaryButton"]:pressed {{
    background-color: {colors['accent_pressed']};
}}

QPushButton[objectName="primaryButton"]:disabled {{
    background-color: {colors['disabled']};
    color: {colors['text_muted']};
}}

/* Large Primary Button */
QPushButton[objectName="primaryButton"][buttonType="large"] {{
    padding: 14px 28px;
    font-size: 13pt;
    font-weight: 600;
    min-height: 48px;
    min-width: 160px;
}}

/* Secondary Button Styling */
QPushButton[objectName="secondaryButton"] {{
    background-color: {colors['bg_secondary']};
    border: 1px solid {colors['border']};
    color: {colors['text_primary']};
    padding: 8px 16px;
    border-radius: 8px;
    font-size: 11pt;
    font-weight: 500;
    min-height: 32px;
    min-width: 100px;
}}

QPushButton[objectName="secondaryButton"]:hover {{
    background-color: {colors['hover']};
    border-color: {colors['accent']};
}}

QPushButton[objectName="secondaryButton"]:pressed {{
    background-color: {colors['pressed']};
}}

QPushButton[objectName="secondaryButton"]:disabled {{
    background-color: {colors['disabled']};
    color: {colors['text_muted']};
}}

/* ComboBox Styling */
QComboBox {{
    background-color: {colors['bg_secondary']};
    border: 1px solid {colors['border']};
    padding: 8px 12px;
    border-radius: 8px;
    font-size: 12pt;
    font-weight: 400;
    color: {colors['text_primary']};
    min-width: 120px;
    padding-right: 30px;
}}

QComboBox:focus {{
    border: 1px solid {colors['accent']};
}}

QComboBox::drop-down {{
    border: none;
    width: 30px;
    subcontrol-origin: padding;
    subcontrol-position: top right;
    border-left: 1px solid {colors['border']};
}}

QComboBox::down-arrow {{
    image: url(data:image/svg+xml;base64,PHN2ZyB3aWR0aD0iMTYiIGhlaWdodD0iMTYiIHZpZXdCb3g9IjAgMCAxNiAxNiIgZmlsbD0ibm9uZSIgeG1sbnM9Imh0dHA6Ly93d3cudzMub3JnLzIwMDAvc3ZnIj4KPHBhdGggZD0iTTQgNkw4IDEwTDEyIDYiIHN0cm9rZT0iIzY2NjY2NiIgc3Ryb2tlLXdpZHRoPSIyIiBzdHJva2UtbGluZWNhcD0icm91bmQiIHN0cm9rZS1saW5lam9pbj0icm91bmQiLz4KPC9zdmc+);
    width: 16px;
    height: 16px;
}}

QComboBox:focus::down-arrow {{
    image: url(data:image/svg+xml;base64,PHN2ZyB3aWR0aD0iMTYiIGhlaWdodD0iMTYiIHZpZXdCb3g9IjAgMCAxNiAxNiIgZmlsbD0ibm9uZSIgeG1sbnM9Imh0dHA6Ly93d3cudzMub3JnLzIwMDAvc3ZnIj4KPHBhdGggZD0iTTQgNkw4IDEwTDEyIDYiIHN0cm9rZT0iIzJjN2FlMCIgc3Ryb2tlLXdpZHRoPSIyIiBzdHJva2UtbGluZWNhcD0icm91bmQiIHN0cm9rZS1saW5lam9pbj0icm91bmQiLz4KPC9zdmc+);
}}

QComboBox QAbstractItemView {{
    background-color: {colors['bg_secondary']};
    border: 1px solid {colors['border']};
    border-radius: 8px;
    selection-background-color: {colors['accent']};
    color: {colors['text_primary']};
    outline: none;
}}

/* Tool Button Styling */
QToolButton {{
    background-color: transparent;
    border: none;
    padding: 4px;
    border-radius: 6px;
}}

QToolButton:hover {{
    background-color: {colors['hover']};
}}

QToolButton:pressed {{
    background-color: {colors['pressed']};
}}

/* Floating Sidebar Toggle Button */
QPushButton[objectName="sidebarToggle"] {{
    background-color: {colors['accent']};
    border: none;
    border-radius: 22px;
    padding: 0px;
    font-size: 16pt;
    font-weight: 500;
    min-width: 44px;
    min-height: 44px;
    max-width: 44px;
    max-height: 44px;
    color: {colors['text_on_accent']};
}}

QPushButton[objectName="sidebarToggle"]:hover {{
    background-color: {colors['accent_hover']};
}}

QPushButton[objectName="sidebarToggle"]:pressed {{
    background-color: {colors['accent_pressed']};
}}

/* Frame Styling */
QFrame {{
    border: none;
    border-radius: 8px;
}}

/* Drop Container Styling */
QFrame[objectName="dropContainer"] {{
    background-color: rgba(0, 0, 0, 0.02);
    border: 2px dashed {colors['border']};
    border-radius: 12px;
    padding: 0px;
    margin: 8px 0px;
}}

QFrame[objectName="dropContainer"]:hover {{
    border-color: {colors['accent']};
    background-color: {colors['bg_secondary']};
    border-style: solid;
}}

/* Sidebar specific styling */
QFrame[objectName="sidebar"] {{
    border-right: 1px solid {colors['border']};
    border-radius: 0px;
}}

/* Progress Dialog */
QProgressDialog {{
    font-size: 12pt;
    font-weight: 400;
}}

QProgressBar {{
    background-color: {colors['bg_secondary']};
    border: 1px solid {colors['border']};
    border-radius: 4px;
    text-align: center;
    color: {colors['text_primary']};
}}

QProgressBar::chunk {{
    background-color: {colors['accent']};
    border-radius: 3px;
}}

/* Scrollbar */
QScrollBar:vertical {{
    background-color: {colors['bg_secondary']};
    width: 12px;
    border-radius: 6px;
}}

QScrollBar::handle:vertical {{
    background-color: {colors['border']};
    border-radius: 6px;
    min-height: 20px;
}}

QScrollBar::handle:vertical:hover {{
    background-color: {colors['hover']};
}}

QScrollBar::add-line:vertical, QScrollBar::sub-line:vertical {{
    height: 0;
    border: none;
}}

QScrollBar::add-page:vertical, QScrollBar::sub-page:vertical {{
    background: none;
}}

/* Message Boxes */
QMessageBox {{
    background-color: {colors['bg_primary']};
    color: {colors['text_primary']};
    border: 1px solid {colors['border']};
    border-radius: 8px;
}}

QMessageBox QPushButton {{
    background-color: {colors['accent']};
    border: none;
    border-radius: 6px;
    color: {colors['text_on_accent']};
    font-size: 12pt;
    font-weight: 500;
    padding: 8px 16px;
    min-width: 80px;
}}

QMessageBox QPushButton:hover {{
    background-color: {colors['accent_hover']};
}}

/* Input Dialog */
QInputDialog {{
    background-color: {colors['bg_primary']};
    color: {colors['text_primary']};
    border: 1px solid {colors['border']};
    border-radius: 8px;
}}

QInputDialog QLineEdit {{
    background-color: {colors['bg_secondary']};
    border: 1px solid {colors['border']};
    border-radius: 6px;
    color: {colors['text_primary']};
    font-size: 12pt;
    padding: 8px 12px;
}}

QInputDialog QPushButton {{
    background-color: {colors['accent']};
    border: none;
    border-radius: 6px;
    color: {colors['text_on_accent']};
    font-size: 12pt;
    font-weight: 500;
    padding: 8px 16px;
    min-width: 80px;
}}

QInputDialog QPushButton:hover {{
    background-color: {colors['accent_hover']};
}}

/* File Dialog */
QFileDialog {{
    background-color: {colors['bg_primary']};
    color: {colors['text_primary']};
    border: 1px solid {colors['border']};
    border-radius: 8px;
}}

QFileDialog QPushButton {{
    background-color: {colors['accent']};
    border: none;
    border-radius: 6px;
    color: {colors['text_on_accent']};
    font-size: 12pt;
    font-weight: 500;
    padding: 8px 16px;
    min-width: 80px;
}}

QFileDialog QPushButton:hover {{
    background-color: {colors['accent_hover']};
}}
"""

# Color schemes for each theme
DARK_MODE_COLORS = {
    'bg_primary': '#1a1a1a',
    'bg_secondary': '#2a2a2a',
    'border': '#404040',
    'text_primary': '#e6e6e6',
    'text_muted': '#808080',
    'accent': '#0078d4',
    'accent_hover': '#106ebe',
    'accent_pressed': '#005a9e',
    'text_on_accent': '#ffffff',
    'hover': '#404040',
    'pressed': '#505050',
    'disabled': '#404040'
}

CATPPUCCIN_COLORS = {
    'bg_primary': '#1e1e2e',
    'bg_secondary': '#2a273f',
    'border': '#36304a',
    'text_primary': '#c6d0f5',
    'text_muted': '#a5adce',
    'accent': '#f5c2e7',
    'accent_hover': '#f2a6cf',
    'accent_pressed': '#ef8bb7',
    'text_on_accent': '#1e1e2e',
    'hover': '#36304a',
    'pressed': '#414155',
    'disabled': '#36304a'
}

DRACULA_COLORS = {
    'bg_primary': '#282a36',
    'bg_secondary': '#44475a',
    'border': '#6272a4',
    'text_primary': '#f8f8f2',
    'text_muted': '#6272a4',
    'accent': '#bd93f9',
    'accent_hover': '#ff79c6',
    'accent_pressed': '#8be9fd',
    'text_on_accent': '#282a36',
    'hover': '#6272a4',
    'pressed': '#44475a',
    'disabled': '#44475a'
}

TRUE_BLACK_COLORS = {
    'bg_primary': '#000000',
    'bg_secondary': '#111111',
    'border': '#333333',
    'text_primary': '#ffffff',
    'text_muted': '#666666',
    'accent': '#ffffff',
    'accent_hover': '#cccccc',
    'accent_pressed': '#999999',
    'text_on_accent': '#000000',
    'hover': '#333333',
    'pressed': '#555555',
    'disabled': '#333333'
}

# Generate themes
dark_mode = create_theme(DARK_MODE_COLORS)
catppuccin_mocha = create_theme(CATPPUCCIN_COLORS)
dracula_theme = create_theme(DRACULA_COLORS)
true_black = create_theme(TRUE_BLACK_COLORS)

THEMES = {
    "Dark Mode": dark_mode,
    "Catppuccin Mocha": catppuccin_mocha,
    "Dracula": dracula_theme,
    "True Black": true_black,
}

# Default theme for imports
original_dark = dark_mode

# Export color schemes for dynamic icon updates
__all__ = ['THEMES', 'original_dark', 'DARK_MODE_COLORS', 'CATPPUCCIN_COLORS', 'DRACULA_COLORS', 'TRUE_BLACK_COLORS']