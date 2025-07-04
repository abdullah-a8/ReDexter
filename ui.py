import os
import subprocess
import configparser

from PyQt6.QtWidgets import (
    QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, QLabel, QLineEdit,
    QPushButton, QFileDialog, QMessageBox, QComboBox, QFormLayout, QInputDialog,
    QProgressDialog, QStyle, QGraphicsOpacityEffect, QToolButton, QGroupBox,
    QFrame, QSizePolicy, QSpacerItem, QScrollArea
)
from PyQt6.QtCore import Qt, QThread, pyqtSignal, QPropertyAnimation, QSize, QEasingCurve, QParallelAnimationGroup, QPoint
from PyQt6.QtGui import QIcon, QFont, QPixmap, QPainter, QColor

import qtawesome as qta

from themes import THEMES, original_dark
from drag_drop_listwidget import DragDropListWidget
from crypto import make_key, decrypt_file
from config_utils import load_rclone_config, get_crypt_remotes

class DecryptionWorker(QThread):
    progress_update = pyqtSignal(int)   # Emits progress percentage
    finished_signal = pyqtSignal(bool)    # Emits True on success
    error_signal = pyqtSignal(str)        # Emits error message

    def __init__(self, files, data_key, dest):
        super().__init__()
        self.files = files
        self.data_key = data_key
        self.dest = dest
        self._is_interrupted = False

    def run(self):
        total = len(self.files)
        for index, file in enumerate(self.files):
            if self._is_interrupted:
                self.error_signal.emit("Operation cancelled.")
                return
            result = decrypt_file(file, self.data_key, self.dest)
            if result != 0:
                self.error_signal.emit(f"Decryption failed for {file}")
                return
            percent = int(((index + 1) / total) * 100)
            self.progress_update.emit(percent)
        self.finished_signal.emit(True)

    def cancel(self):
        self._is_interrupted = True

class ModernSidebar(QFrame):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setFixedWidth(280)
        self.setObjectName("sidebar")
        self.setup_ui()

    def setup_ui(self):
        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)

        # Header with just the settings label (no close button)
        header = QFrame()
        header.setFixedHeight(60)
        header_layout = QHBoxLayout(header)
        header_layout.setContentsMargins(60, 10, 15, 10)  # Extra left margin for toggle button space
        
        # Settings label
        settings_label = QLabel("Settings")
        font = settings_label.font()
        font.setPointSize(16)
        font.setBold(True)
        settings_label.setFont(font)
        
        header_layout.addWidget(settings_label)
        header_layout.addStretch()

        layout.addWidget(header)

        # Scrollable content area
        scroll_area = QScrollArea()
        scroll_area.setWidgetResizable(True)
        scroll_area.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        scroll_area.setVerticalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAsNeeded)
        
        content_widget = QWidget()
        content_layout = QVBoxLayout(content_widget)
        content_layout.setContentsMargins(15, 15, 15, 15)
        content_layout.setSpacing(20)

        # Configuration section  
        config_section = self.create_config_section()
        content_layout.addWidget(config_section)

        # Theme section
        theme_section = self.create_theme_section()
        content_layout.addWidget(theme_section)

        content_layout.addStretch()
        
        scroll_area.setWidget(content_widget)
        layout.addWidget(scroll_area)



    def create_config_section(self):
        section = QGroupBox("RCLONE Configuration")
        
        layout = QVBoxLayout(section)
        layout.setContentsMargins(10, 15, 10, 10)
        layout.setSpacing(12)

        # Config controls
        config_controls = QVBoxLayout()
        config_controls.setSpacing(8)
        
        # Load config button
        self.load_config_btn = QPushButton("Load rclone Config")
        self.load_config_btn.setIcon(self.style().standardIcon(QStyle.StandardPixmap.SP_DialogOpenButton))
        self.load_config_btn.clicked.connect(self.parent().load_config_action)
        config_controls.addWidget(self.load_config_btn)
        
        # Remove config button
        self.remove_config_btn = QPushButton("Remove Config")
        self.remove_config_btn.setIcon(self.style().standardIcon(QStyle.StandardPixmap.SP_DialogCancelButton))
        self.remove_config_btn.clicked.connect(self.parent().remove_config_action)
        config_controls.addWidget(self.remove_config_btn)
        
        # Config status
        self.config_status = QLabel("No config loaded")
        font = self.config_status.font()
        font.setPointSize(font.pointSize() - 1)
        font.setItalic(True)
        self.config_status.setFont(font)
        config_controls.addWidget(self.config_status)
        
        # Crypt remote selection
        remote_layout = QVBoxLayout()
        remote_layout.setSpacing(6)
        
        remote_label = QLabel("Select Crypt Remote:")
        remote_layout.addWidget(remote_label)
        
        self.crypt_combobox = QComboBox()
        self.crypt_combobox.currentTextChanged.connect(self.parent().populate_credentials_from_config)
        remote_layout.addWidget(self.crypt_combobox)
        
        config_controls.addLayout(remote_layout)
        
        layout.addLayout(config_controls)

        # Manual credentials section
        creds_group = QGroupBox("Manual Credentials")
        creds_layout = QVBoxLayout(creds_group)
        creds_layout.setContentsMargins(10, 15, 10, 10)
        creds_layout.setSpacing(10)
        
        # Password field
        pwd_layout = QVBoxLayout()
        pwd_layout.setSpacing(6)
        
        pwd_label = QLabel("Crypt Password:")
        pwd_layout.addWidget(pwd_label)
        
        pwd_container = QHBoxLayout()
        pwd_container.setSpacing(4)
        
        self.password_lineedit = QLineEdit()
        self.password_lineedit.setEchoMode(QLineEdit.EchoMode.Password)
        self.password_lineedit.setPlaceholderText("Enter password...")
        
        self.password_toggle_button = QToolButton()
        self.password_toggle_button.setCheckable(True)
        self.password_toggle_button.setIcon(qta.icon('fa5s.eye-slash'))
        self.password_toggle_button.clicked.connect(self.parent().toggle_password_visibility)
        
        pwd_container.addWidget(self.password_lineedit)
        pwd_container.addWidget(self.password_toggle_button)
        
        pwd_layout.addLayout(pwd_container)
        creds_layout.addLayout(pwd_layout)
        
        # Salt field
        salt_layout = QVBoxLayout()
        salt_layout.setSpacing(6)
        
        salt_label = QLabel("Crypt Salt:")
        salt_layout.addWidget(salt_label)
        
        salt_container = QHBoxLayout()
        salt_container.setSpacing(4)
        
        self.salt_lineedit = QLineEdit()
        self.salt_lineedit.setEchoMode(QLineEdit.EchoMode.Password)
        self.salt_lineedit.setPlaceholderText("Enter salt...")
        
        self.salt_toggle_button = QToolButton()
        self.salt_toggle_button.setCheckable(True)
        self.salt_toggle_button.setIcon(qta.icon('fa5s.eye-slash'))
        self.salt_toggle_button.clicked.connect(self.parent().toggle_salt_visibility)
        
        salt_container.addWidget(self.salt_lineedit)
        salt_container.addWidget(self.salt_toggle_button)
        
        salt_layout.addLayout(salt_container)
        creds_layout.addLayout(salt_layout)
        
        layout.addWidget(creds_group)
        
        return section

    def create_theme_section(self):
        section = QGroupBox("Theme")
        
        layout = QVBoxLayout(section)
        layout.setContentsMargins(10, 15, 10, 10)
        layout.setSpacing(10)
        
        # Theme selector
        theme_layout = QVBoxLayout()
        theme_layout.setSpacing(6)
        
        theme_label = QLabel("Select Theme:")
        theme_layout.addWidget(theme_label)
        
        self.theme_combobox = QComboBox()
        self.theme_combobox.addItems(list(THEMES.keys()))
        self.theme_combobox.setCurrentText("Dark Mode")  # Set default to match main.py
        self.theme_combobox.currentTextChanged.connect(self.parent().change_theme)
        theme_layout.addWidget(self.theme_combobox)
        
        layout.addLayout(theme_layout)
        
        return section

class ModernMainContent(QFrame):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setup_ui()

    def setup_ui(self):
        layout = QVBoxLayout(self)
        layout.setContentsMargins(24, 20, 24, 20)
        layout.setSpacing(20)

        # Header with title and subtitle
        self.create_header(layout)

        # Modern file drop area
        self.create_modern_file_drop_area(layout)

        # Bottom actions section
        self.create_bottom_actions(layout)

    def create_header(self, parent_layout):
        header_container = QWidget()
        header_layout = QVBoxLayout(header_container)
        header_layout.setContentsMargins(0, 0, 0, 0)
        header_layout.setSpacing(4)
        
        # Main title
        title_label = QLabel("ReDexter")
        title_font = title_label.font()
        title_font.setFamily("Inter")
        title_font.setPointSize(20)
        title_font.setWeight(QFont.Weight.Medium)
        title_label.setFont(title_font)
        title_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        header_layout.addWidget(title_label)
        
        # Subtitle
        subtitle_label = QLabel("Decrypt your rclone files with ease")
        subtitle_font = subtitle_label.font()
        subtitle_font.setFamily("Inter")
        subtitle_font.setPointSize(12)
        subtitle_font.setWeight(QFont.Weight.Normal)
        subtitle_label.setFont(subtitle_font)
        subtitle_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        subtitle_label.setStyleSheet("color: rgba(136, 136, 136, 1);")
        header_layout.addWidget(subtitle_label)
        
        parent_layout.addWidget(header_container)

    def create_modern_file_drop_area(self, parent_layout):
        # Main container for the drop area
        drop_container = QFrame()
        drop_container.setStyleSheet("""
            QFrame {
                background-color: transparent;
                border: 1px dashed rgba(203, 213, 224, 0.8);
                border-radius: 8px;
                padding: 0px;
            }
            QFrame:hover {
                border-color: rgba(59, 130, 246, 0.6);
            }
        """)
        drop_container.setMinimumHeight(200)
        drop_container.setMaximumHeight(200)
        
        # Main layout for drop area
        drop_layout = QVBoxLayout(drop_container)
        drop_layout.setContentsMargins(24, 24, 24, 24)
        drop_layout.setSpacing(12)
        drop_layout.setAlignment(Qt.AlignmentFlag.AlignCenter)
        
        # Upload icon
        upload_icon = QLabel()
        upload_icon.setPixmap(qta.icon('fa5s.cloud-upload-alt', color='#9CA3AF').pixmap(32, 32))
        upload_icon.setAlignment(Qt.AlignmentFlag.AlignCenter)
        drop_layout.addWidget(upload_icon)
        
        # Primary text
        primary_text = QLabel("Drag & drop your files here")
        primary_font = primary_text.font()
        primary_font.setFamily("Inter")
        primary_font.setPointSize(14)
        primary_font.setWeight(QFont.Weight.Medium)
        primary_text.setFont(primary_font)
        primary_text.setAlignment(Qt.AlignmentFlag.AlignCenter)
        drop_layout.addWidget(primary_text)
        
        # Secondary text
        secondary_text = QLabel("or click to browse")
        secondary_font = secondary_text.font()
        secondary_font.setFamily("Inter")
        secondary_font.setPointSize(11)
        secondary_font.setWeight(QFont.Weight.Normal)
        secondary_text.setFont(secondary_font)
        secondary_text.setAlignment(Qt.AlignmentFlag.AlignCenter)
        secondary_text.setStyleSheet("color: rgba(107, 114, 128, 1);")
        drop_layout.addWidget(secondary_text)
        
        # Browse button
        browse_btn = QPushButton("Browse Files")
        browse_btn.setIcon(qta.icon('fa5s.folder-open', color='white'))
        browse_btn.clicked.connect(self.parent().select_input_files)
        browse_btn.setStyleSheet("""
            QPushButton {
                background-color: rgba(59, 130, 246, 1);
                border: none;
                color: white;
                padding: 8px 16px;
                border-radius: 6px;
                font-size: 12pt;
                font-weight: 500;
                min-width: 100px;
                min-height: 32px;
                max-height: 32px;
            }
            QPushButton:hover {
                background-color: rgba(37, 99, 235, 1);
            }
            QPushButton:pressed {
                background-color: rgba(29, 78, 216, 1);
            }
        """)
        drop_layout.addWidget(browse_btn, alignment=Qt.AlignmentFlag.AlignCenter)
        
        parent_layout.addWidget(drop_container)
        
        # File list section (separate from drop area)
        files_section = QWidget()
        files_layout = QVBoxLayout(files_section)
        files_layout.setContentsMargins(0, 16, 0, 0)
        files_layout.setSpacing(8)
        
        # Files header
        files_header = QWidget()
        files_header_layout = QHBoxLayout(files_header)
        files_header_layout.setContentsMargins(0, 0, 0, 0)
        files_header_layout.setSpacing(6)
        
        files_icon = QLabel()
        files_icon.setPixmap(qta.icon('fa5s.file-alt', color='#6B7280').pixmap(16, 16))
        files_header_layout.addWidget(files_icon)
        
        files_title = QLabel("Selected Files")
        files_title_font = files_title.font()
        files_title_font.setFamily("Inter")
        files_title_font.setPointSize(12)
        files_title_font.setWeight(QFont.Weight.Medium)
        files_title.setFont(files_title_font)
        files_header_layout.addWidget(files_title)
        
        files_header_layout.addStretch()
        
        # Files count
        self.files_count_label = QLabel("0 files")
        count_font = self.files_count_label.font()
        count_font.setFamily("Inter")
        count_font.setPointSize(11)
        count_font.setWeight(QFont.Weight.Normal)
        self.files_count_label.setFont(count_font)
        self.files_count_label.setStyleSheet("color: rgba(107, 114, 128, 1);")
        files_header_layout.addWidget(self.files_count_label)
        
        files_layout.addWidget(files_header)
        
        # File list widget
        self.files_listwidget = DragDropListWidget()
        self.files_listwidget.setMaximumHeight(100)
        self.files_listwidget.setStyleSheet("""
            QListWidget {
                background-color: transparent;
                border: 1px solid rgba(229, 231, 235, 0.8);
                border-radius: 6px;
                padding: 4px;
                font-size: 11pt;
            }
            QListWidget::item {
                padding: 6px 8px;
                border-radius: 4px;
                margin: 1px 0px;
            }
            QListWidget::item:hover {
                background-color: rgba(243, 244, 246, 0.8);
            }
            QListWidget::item:selected {
                background-color: rgba(59, 130, 246, 0.1);
                color: rgba(59, 130, 246, 1);
            }
        """)
        files_layout.addWidget(self.files_listwidget)
        
        parent_layout.addWidget(files_section)

    def create_bottom_actions(self, parent_layout):
        # Bottom actions container
        actions_container = QWidget()
        actions_layout = QVBoxLayout(actions_container)
        actions_layout.setContentsMargins(0, 0, 0, 0)
        actions_layout.setSpacing(16)
        
        # Output folder section
        output_section = QGroupBox("Output Folder")
        output_section.setStyleSheet("""
            QGroupBox {
                font-size: 12pt;
                font-weight: 500;
                border: 1px solid rgba(229, 231, 235, 0.8);
                border-radius: 6px;
                margin-top: 8px;
                padding-top: 12px;
                background-color: transparent;
            }
            QGroupBox::title {
                subcontrol-origin: margin;
                left: 12px;
                padding: 0 6px 0 6px;
                font-weight: 500;
            }
        """)
        output_layout = QVBoxLayout(output_section)
        output_layout.setContentsMargins(12, 12, 12, 12)
        output_layout.setSpacing(8)
        
        # Output folder input
        output_container = QHBoxLayout()
        output_container.setSpacing(8)
        
        self.dest_dir_lineedit = QLineEdit()
        self.dest_dir_lineedit.setPlaceholderText("Leave empty to use same folder as input files")
        self.dest_dir_lineedit.setStyleSheet("""
            QLineEdit {
                background-color: transparent;
                border: 1px solid rgba(209, 213, 219, 0.8);
                border-radius: 4px;
                padding: 6px 8px;
                font-size: 11pt;
                min-height: 24px;
                max-height: 24px;
            }
            QLineEdit:focus {
                border-color: rgba(59, 130, 246, 1);
                outline: none;
            }
            QLineEdit::placeholder {
                color: rgba(156, 163, 175, 1);
            }
        """)
        
        select_folder_btn = QPushButton("Choose Folder")
        select_folder_btn.setIcon(qta.icon('fa5s.folder', color='#6B7280'))
        select_folder_btn.clicked.connect(self.parent().select_destination)
        select_folder_btn.setStyleSheet("""
            QPushButton {
                background-color: transparent;
                border: 1px solid rgba(209, 213, 219, 0.8);
                color: rgba(55, 65, 81, 1);
                padding: 6px 12px;
                border-radius: 4px;
                font-size: 11pt;
                font-weight: 500;
                min-width: 100px;
                min-height: 24px;
                max-height: 24px;
            }
            QPushButton:hover {
                background-color: rgba(243, 244, 246, 0.8);
                border-color: rgba(156, 163, 175, 1);
            }
            QPushButton:pressed {
                background-color: rgba(229, 231, 235, 0.8);
            }
        """)
        
        output_container.addWidget(self.dest_dir_lineedit)
        output_container.addWidget(select_folder_btn)
        
        output_layout.addLayout(output_container)
        actions_layout.addWidget(output_section)
        
        # Decrypt button
        self.decrypt_btn = QPushButton("Start Decryption")
        self.decrypt_btn.setIcon(qta.icon('fa5s.unlock', color='white'))
        self.decrypt_btn.clicked.connect(self.parent().decrypt_action)
        self.decrypt_btn.setStyleSheet("""
            QPushButton {
                background-color: rgba(59, 130, 246, 1);
                border: none;
                color: white;
                padding: 12px 24px;
                border-radius: 6px;
                font-size: 13pt;
                font-weight: 500;
                min-height: 40px;
                max-height: 40px;
            }
            QPushButton:hover {
                background-color: rgba(37, 99, 235, 1);
            }
            QPushButton:pressed {
                background-color: rgba(29, 78, 216, 1);
            }
            QPushButton:disabled {
                background-color: rgba(156, 163, 175, 1);
                color: rgba(255, 255, 255, 0.8);
            }
        """)
        actions_layout.addWidget(self.decrypt_btn)
        
        parent_layout.addWidget(actions_container)

class ModernSidebarToggle(QPushButton):
    """Modern floating sidebar toggle button that animates position and icon"""
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.main_window = None
        self.is_sidebar_open = False
        
        self.setFixedSize(44, 44)
        self.setObjectName("sidebarToggle")
        
        # Set initial position (top-left when closed)
        self.move(16, 16)
        
        # Initialize with hamburger icon
        self.update_icon()
        
        # Animation setup
        self.position_animation = QPropertyAnimation(self, b"pos")
        self.position_animation.setDuration(300)
        self.position_animation.setEasingCurve(QEasingCurve.Type.OutCubic)
        
        # Connect click event
        self.clicked.connect(self.toggle_sidebar)
        
        # Bring to front
        self.raise_()
        self.show()
    
    def set_main_window(self, main_window):
        """Set reference to main window for sidebar control"""
        self.main_window = main_window
    
    def update_icon(self):
        """Update icon based on sidebar state"""
        if self.is_sidebar_open:
            # X icon when open
            self.setIcon(qta.icon('fa5s.times'))
        else:
            # Hamburger icon when closed  
            self.setIcon(qta.icon('fa5s.bars'))
    
    def toggle_sidebar(self):
        """Toggle sidebar and animate button position"""
        if not self.main_window:
            return
            
        if self.is_sidebar_open:
            # Close sidebar - button moves first, then sidebar closes
            self.animate_to_closed_position()
            self.main_window.hide_sidebar()
        else:
            # Open sidebar - sidebar opens first, then button moves
            self.main_window.show_sidebar()
            # Small delay for more natural feel
            from PyQt6.QtCore import QTimer
            QTimer.singleShot(50, self.animate_to_open_position)
    
    def animate_to_open_position(self):
        """Animate button to position inside opened sidebar"""
        self.is_sidebar_open = True
        self.update_icon()
        
        # Position at right edge of sidebar (280px width - 44px button width - 16px margin)
        target_pos = QPoint(220, 16)  # Inside sidebar at top-right
        
        self.position_animation.setStartValue(self.pos())
        self.position_animation.setEndValue(target_pos)
        self.position_animation.start()
    
    def animate_to_closed_position(self):
        """Animate button to position at left edge when sidebar is closed"""
        self.is_sidebar_open = False
        self.update_icon()
        
        # Position at left edge of main window
        target_pos = QPoint(16, 16)
        
        self.position_animation.setStartValue(self.pos())
        self.position_animation.setEndValue(target_pos)
        self.position_animation.start()
    
    def resizeEvent(self, event):
        """Ensure button stays on top when parent resizes"""
        super().resizeEvent(event)
        self.raise_()
    
    def update_position_for_sidebar_state(self):
        """Update button position based on current sidebar state without animation"""
        if self.is_sidebar_open:
            self.move(220, 16)  # Inside sidebar at top-right
        else:
            self.move(16, 16)   # At left edge of main window

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("ReDexter")
        self.resize(1000, 700)
        self.setMinimumSize(800, 500)
        
        self.rclone_config = None
        self.crypt_remotes = {}  # Mapping: remote name -> (password, salt)
        self.dest_dir = None
        self.worker = None  # To hold the decryption thread
        self.current_animation = None  # Keep a reference to the current animation
        
        self.setup_ui()
        self.load_last_config()
        self.update_files_count()

    def setup_ui(self):
        # Main container
        main_container = QWidget()
        self.setCentralWidget(main_container)
        
        # Main layout
        main_layout = QHBoxLayout(main_container)
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.setSpacing(0)
        
        # Create sidebar (initially hidden)
        self.sidebar = ModernSidebar(self)
        self.sidebar.hide()
        main_layout.addWidget(self.sidebar)
        
        # Create main content area
        self.main_content = ModernMainContent(self)
        main_layout.addWidget(self.main_content)
        
        # Create floating sidebar toggle button
        self.sidebar_toggle = ModernSidebarToggle(main_container)
        self.sidebar_toggle.set_main_window(self)
        
        # Connect file list changes to update counter
        self.main_content.files_listwidget.itemChanged.connect(self.update_files_count)
        self.main_content.files_listwidget.filesAdded.connect(self.update_files_count)
    
    def resizeEvent(self, event):
        """Handle window resize events to maintain toggle button positioning"""
        super().resizeEvent(event)
        # Ensure toggle button stays on top and in correct position
        if hasattr(self, 'sidebar_toggle'):
            self.sidebar_toggle.raise_()
            self.sidebar_toggle.update_position_for_sidebar_state()
        
    def show_sidebar(self):
        self.sidebar.show()
        self.animate_sidebar_show()
        
    def hide_sidebar(self):
        self.animate_sidebar_hide()
        
    def animate_sidebar_show(self):
        self.sidebar.setFixedWidth(0)
        self.sidebar.show()
        
        self.sidebar_animation = QPropertyAnimation(self.sidebar, b"minimumWidth")
        self.sidebar_animation.setDuration(300)
        self.sidebar_animation.setStartValue(0)
        self.sidebar_animation.setEndValue(280)
        self.sidebar_animation.start()
        
    def animate_sidebar_hide(self):
        self.sidebar_animation = QPropertyAnimation(self.sidebar, b"minimumWidth")
        self.sidebar_animation.setDuration(300)
        self.sidebar_animation.setStartValue(280)
        self.sidebar_animation.setEndValue(0)
        self.sidebar_animation.finished.connect(self.sidebar.hide)
        self.sidebar_animation.start()
        
    def update_files_count(self):
        count = self.main_content.files_listwidget.count()
        if count == 0:
            self.main_content.files_count_label.setText("0 files")
        elif count == 1:
            self.main_content.files_count_label.setText("1 file")
        else:
            self.main_content.files_count_label.setText(f"{count} files")

    def load_config_action(self):
        file_path, _ = QFileDialog.getOpenFileName(self, "Select rclone Config File")
        if not file_path:
            return
        pwd, ok = QInputDialog.getText(self, "Config Password",
                                       "Enter rclone config password (leave blank if none):",
                                       QLineEdit.EchoMode.Password)
        if not ok:
            return
        config_password = pwd.strip()
        try:
            config = load_rclone_config(file_path, config_password)
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Failed to load config:\n{e}")
            return
        self.rclone_config = config
        self.sidebar.config_status.setText(f"Loaded: {os.path.basename(file_path)}")
        self.crypt_remotes = get_crypt_remotes(config)
        self.sidebar.crypt_combobox.clear()
        if not self.crypt_remotes:
            QMessageBox.warning(self, "Warning", "No crypt remotes found in config.")
        else:
            self.sidebar.crypt_combobox.addItems(sorted(self.crypt_remotes.keys()))
        try:
            import config_storage
            config_storage.set_last_config_path(file_path)
            if config_password:
                config_storage.set_config_password(file_path, config_password)
        except Exception as e:
            print("Error saving config info:", e)

    def remove_config_action(self):
        """
        Clears the loaded config and allows the user to manually enter credentials.
        """
        self.rclone_config = None
        self.sidebar.config_status.setText("No config loaded")
        self.crypt_remotes = {}
        self.sidebar.crypt_combobox.clear()
        # Allow manual entry by making the fields editable and clearing any auto-populated values.
        self.sidebar.password_lineedit.setReadOnly(False)
        self.sidebar.password_lineedit.clear()
        self.sidebar.salt_lineedit.setReadOnly(False)
        self.sidebar.salt_lineedit.clear()
        try:
            import config_storage
            config_storage.clear_config_full()
        except Exception as e:
            print("Error clearing stored config info:", e)
        QMessageBox.information(self, "Info", "Configuration has been removed. Please enter credentials manually.")

    def load_last_config(self):
        try:
            import config_storage
            last_config = config_storage.get_last_config_path()
            if last_config:
                stored_password = config_storage.get_config_password(last_config)
                if stored_password is None:
                    stored_password = ""
                try:
                    config = load_rclone_config(last_config, stored_password)
                except Exception as e:
                    print("Auto-loading last config failed:", e)
                    return
                self.rclone_config = config
                self.sidebar.config_status.setText(f"Loaded: {os.path.basename(last_config)}")
                self.crypt_remotes = get_crypt_remotes(config)
                self.sidebar.crypt_combobox.clear()
                if not self.crypt_remotes:
                    QMessageBox.warning(self, "Warning", "No crypt remotes found in config from last loaded config.")
                else:
                    self.sidebar.crypt_combobox.addItems(sorted(self.crypt_remotes.keys()))
        except Exception as e:
            print("Error during auto-loading config:", e)

    def populate_credentials_from_config(self, remote_name):
        if remote_name in self.crypt_remotes:
            pw, salt = self.crypt_remotes[remote_name]
            self.sidebar.password_lineedit.setText(pw)
            self.sidebar.salt_lineedit.setText(salt if salt else "")
            self.sidebar.password_lineedit.setReadOnly(True)
            self.sidebar.salt_lineedit.setReadOnly(True)

    def select_destination(self):
        directory = QFileDialog.getExistingDirectory(self, "Select Destination Directory")
        if directory:
            self.dest_dir = directory
            self.main_content.dest_dir_lineedit.setText(directory)

    def select_input_files(self):
        files, _ = QFileDialog.getOpenFileNames(self, "Select Input Files")
        if files:
            self.main_content.files_listwidget.clear()
            for file in files:
                self.main_content.files_listwidget.addItem(file)
            self.update_files_count()

    def decrypt_action(self):
        files = [self.main_content.files_listwidget.item(i).text() for i in range(self.main_content.files_listwidget.count())]
        password = self.sidebar.password_lineedit.text().strip()
        salt_text = self.sidebar.salt_lineedit.text().strip()
        salt = salt_text if salt_text else None

        if not files or not password:
            QMessageBox.critical(self, "Error", "Please select files and ensure crypt credentials are provided.")
            return

        try:
            data_key = make_key(password, salt)
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Key derivation failed:\n{e}")
            return

        dest = self.main_content.dest_dir_lineedit.text().strip() if self.main_content.dest_dir_lineedit.text().strip() else None

        self.progress_dialog = QProgressDialog("Decrypting files...", "Cancel", 0, 100, self)
        self.progress_dialog.setWindowTitle("Decrypting")
        self.progress_dialog.setWindowModality(Qt.WindowModality.WindowModal)
        self.progress_dialog.setValue(0)
        self.progress_dialog.canceled.connect(self.cancel_decryption)

        self.worker = DecryptionWorker(files, data_key, dest)
        self.worker.progress_update.connect(self.progress_dialog.setValue)
        self.worker.error_signal.connect(self.handle_worker_error)
        self.worker.finished_signal.connect(self.handle_worker_finished)
        self.worker.start()

    def cancel_decryption(self):
        if self.worker is not None:
            self.worker.cancel()

    def handle_worker_error(self, message):
        self.progress_dialog.cancel()
        QMessageBox.critical(self, "Error", message)

    def handle_worker_finished(self, success):
        self.progress_dialog.cancel()
        if success:
            QMessageBox.information(self, "Success", "Decryption completed successfully.")
        self.worker = None

    def change_theme(self, theme):
        stylesheet = THEMES.get(theme, original_dark)
        self.setStyleSheet(stylesheet)

    def toggle_password_visibility(self):
        if self.sidebar.password_toggle_button.isChecked():
            self.sidebar.password_lineedit.setEchoMode(QLineEdit.EchoMode.Normal)
            self.sidebar.password_toggle_button.setIcon(qta.icon('fa5s.eye'))
        else:
            self.sidebar.password_lineedit.setEchoMode(QLineEdit.EchoMode.Password)
            self.sidebar.password_toggle_button.setIcon(qta.icon('fa5s.eye-slash'))

    def toggle_salt_visibility(self):
        if self.sidebar.salt_toggle_button.isChecked():
            self.sidebar.salt_lineedit.setEchoMode(QLineEdit.EchoMode.Normal)
            self.sidebar.salt_toggle_button.setIcon(qta.icon('fa5s.eye'))
        else:
            self.sidebar.salt_lineedit.setEchoMode(QLineEdit.EchoMode.Password)
            self.sidebar.salt_toggle_button.setIcon(qta.icon('fa5s.eye-slash'))