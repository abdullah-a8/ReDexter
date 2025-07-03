import os
import subprocess
import configparser

from PyQt6.QtWidgets import (
    QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, QLabel, QLineEdit,
    QPushButton, QFileDialog, QMessageBox, QComboBox, QFormLayout, QInputDialog,
    QTabWidget, QProgressDialog, QStyle, QGraphicsOpacityEffect, QToolButton, QGroupBox
)
from PyQt6.QtCore import Qt, QThread, pyqtSignal, QPropertyAnimation
from PyQt6.QtGui import QIcon

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

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("ReDexter")
        self.resize(950, 700)
        self.rclone_config = None
        self.crypt_remotes = {}  # Mapping: remote name -> (password, salt)
        self.dest_dir = None
        self.worker = None  # To hold the decryption thread
        self.current_animation = None  # Keep a reference to the current animation
        self.setup_ui()
        self.load_last_config()

    def setup_ui(self):
        # Create a QTabWidget to hold our three tabs.
        self.tab_widget = QTabWidget()
        self.setCentralWidget(self.tab_widget)
        self.tab_widget.currentChanged.connect(self.animate_tab_change)

        # ----- Tab 1: Decryption -----
        decryption_tab = QWidget()
        decryption_layout = QVBoxLayout(decryption_tab)
        decryption_layout.setContentsMargins(30, 30, 30, 30)
        decryption_layout.setSpacing(20)

        # Input Files area
        files_label = QLabel("Input Files (drag and drop supported):")
        decryption_layout.addWidget(files_label)
        self.files_listwidget = DragDropListWidget()
        decryption_layout.addWidget(self.files_listwidget)
        browse_button = QPushButton("Browse Files")
        browse_button.setIcon(self.style().standardIcon(QStyle.StandardPixmap.SP_FileIcon))
        browse_button.clicked.connect(self.select_input_files)
        decryption_layout.addWidget(browse_button)

        # Destination Directory Selection
        dest_layout = QHBoxLayout()
        dest_button = QPushButton("Select Destination Directory")
        dest_button.setIcon(self.style().standardIcon(QStyle.StandardPixmap.SP_DirOpenIcon))
        dest_button.clicked.connect(self.select_destination)
        dest_layout.addWidget(dest_button)
        self.dest_dir_lineedit = QLineEdit()
        self.dest_dir_lineedit.setPlaceholderText("No destination selected. (Defaults to input file folder)")
        dest_layout.addWidget(self.dest_dir_lineedit)
        decryption_layout.addLayout(dest_layout)

        # Decrypt Button
        decrypt_button = QPushButton("Decrypt Files")
        decrypt_button.setIcon(self.style().standardIcon(QStyle.StandardPixmap.SP_DialogApplyButton))
        decrypt_button.clicked.connect(self.decrypt_action)
        decryption_layout.addWidget(decrypt_button)

        self.tab_widget.addTab(decryption_tab, "Decryption")

        # ----- Tab 2: Configuration -----
        config_tab = QWidget()
        config_layout = QVBoxLayout(config_tab)
        config_layout.setContentsMargins(30, 30, 30, 30)
        config_layout.setSpacing(20)

        # Rclone Configuration Group Box
        rclone_group = QGroupBox("Rclone Configuration")
        rclone_layout = QVBoxLayout(rclone_group)
        # Top row: Load and Remove Config buttons
        config_buttons_layout = QHBoxLayout()
        config_button = QPushButton("Load rclone Config")
        config_button.setIcon(self.style().standardIcon(QStyle.StandardPixmap.SP_DialogOpenButton))
        config_button.clicked.connect(self.load_config_action)
        config_buttons_layout.addWidget(config_button)
        remove_config_button = QPushButton("Remove Config")
        remove_config_button.setIcon(self.style().standardIcon(QStyle.StandardPixmap.SP_DialogCancelButton))
        remove_config_button.clicked.connect(self.remove_config_action)
        config_buttons_layout.addWidget(remove_config_button)
        rclone_layout.addLayout(config_buttons_layout)
        # Display loaded config file name
        self.config_path_label = QLabel("No config loaded.")
        rclone_layout.addWidget(self.config_path_label)
        # Crypt Remote Selection
        crypt_layout = QHBoxLayout()
        crypt_layout.addWidget(QLabel("Select Crypt Remote:"))
        self.crypt_combobox = QComboBox()
        self.crypt_combobox.currentTextChanged.connect(self.populate_credentials_from_config)
        crypt_layout.addWidget(self.crypt_combobox)
        rclone_layout.addLayout(crypt_layout)

        config_layout.addWidget(rclone_group)

        # Manual Credentials Group Box
        credentials_group = QGroupBox("Manual Credentials")
        cred_layout = QFormLayout(credentials_group)

        # Crypt Password field with eye toggle using qtawesome
        self.password_lineedit = QLineEdit()
        self.password_lineedit.setEchoMode(QLineEdit.EchoMode.Password)
        self.password_toggle_button = QToolButton()
        self.password_toggle_button.setCheckable(True)
        # Use qtawesome icons – eye-slash means hidden by default.
        self.password_toggle_button.setIcon(qta.icon('fa5s.eye-slash'))
        self.password_toggle_button.clicked.connect(self.toggle_password_visibility)
        password_widget = QWidget()
        password_layout = QHBoxLayout(password_widget)
        password_layout.setContentsMargins(0, 0, 0, 0)
        password_layout.addWidget(self.password_lineedit)
        password_layout.addWidget(self.password_toggle_button)
        cred_layout.addRow("Crypt Password:", password_widget)

        # Crypt Salt field with eye toggle using qtawesome
        self.salt_lineedit = QLineEdit()
        self.salt_lineedit.setEchoMode(QLineEdit.EchoMode.Password)
        self.salt_toggle_button = QToolButton()
        self.salt_toggle_button.setCheckable(True)
        self.salt_toggle_button.setIcon(qta.icon('fa5s.eye-slash'))
        self.salt_toggle_button.clicked.connect(self.toggle_salt_visibility)
        salt_widget = QWidget()
        salt_layout = QHBoxLayout(salt_widget)
        salt_layout.setContentsMargins(0, 0, 0, 0)
        salt_layout.addWidget(self.salt_lineedit)
        salt_layout.addWidget(self.salt_toggle_button)
        cred_layout.addRow("Crypt Salt:", salt_widget)

        config_layout.addWidget(credentials_group)
        self.tab_widget.addTab(config_tab, "Configuration")

        # ----- Tab 3: Theme -----
        theme_tab = QWidget()
        theme_layout = QVBoxLayout(theme_tab)
        theme_layout.setContentsMargins(30, 30, 30, 30)
        theme_layout.setSpacing(20)
        theme_layout.addStretch(1)
        theme_h_layout = QHBoxLayout()
        theme_h_layout.addStretch(1)
        theme_label = QLabel("Theme:")
        theme_h_layout.addWidget(theme_label)
        self.theme_combobox = QComboBox()
        self.theme_combobox.addItems(list(THEMES.keys()))
        self.theme_combobox.currentTextChanged.connect(self.change_theme)
        theme_h_layout.addWidget(self.theme_combobox)
        theme_h_layout.addStretch(1)
        theme_layout.addLayout(theme_h_layout)
        theme_layout.addStretch(1)
        self.tab_widget.addTab(theme_tab, "Theme")

    def animate_tab_change(self, index):
        # Fade in animation for the current tab for smooth transitions.
        current_widget = self.tab_widget.widget(index)
        effect = QGraphicsOpacityEffect(current_widget)
        current_widget.setGraphicsEffect(effect)
        self.current_animation = QPropertyAnimation(effect, b"opacity")
        self.current_animation.setDuration(300)
        self.current_animation.setStartValue(0)
        self.current_animation.setEndValue(1)
        self.current_animation.start()

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
        self.config_path_label.setText(os.path.basename(file_path))
        self.crypt_remotes = get_crypt_remotes(config)
        self.crypt_combobox.clear()
        if not self.crypt_remotes:
            QMessageBox.warning(self, "Warning", "No crypt remotes found in config.")
        else:
            self.crypt_combobox.addItems(sorted(self.crypt_remotes.keys()))
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
        self.config_path_label.setText("No config loaded.")
        self.crypt_remotes = {}
        self.crypt_combobox.clear()
        # Allow manual entry by making the fields editable and clearing any auto-populated values.
        self.password_lineedit.setReadOnly(False)
        self.password_lineedit.clear()
        self.salt_lineedit.setReadOnly(False)
        self.salt_lineedit.clear()
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
                self.config_path_label.setText(os.path.basename(last_config))
                self.crypt_remotes = get_crypt_remotes(config)
                self.crypt_combobox.clear()
                if not self.crypt_remotes:
                    QMessageBox.warning(self, "Warning", "No crypt remotes found in config from last loaded config.")
                else:
                    self.crypt_combobox.addItems(sorted(self.crypt_remotes.keys()))
        except Exception as e:
            print("Error during auto-loading config:", e)

    def populate_credentials_from_config(self, remote_name):
        if remote_name in self.crypt_remotes:
            pw, salt = self.crypt_remotes[remote_name]
            self.password_lineedit.setText(pw)
            self.salt_lineedit.setText(salt if salt else "")
            self.password_lineedit.setReadOnly(True)
            self.salt_lineedit.setReadOnly(True)

    def select_destination(self):
        directory = QFileDialog.getExistingDirectory(self, "Select Destination Directory")
        if directory:
            self.dest_dir = directory
            self.dest_dir_lineedit.setText(directory)

    def select_input_files(self):
        files, _ = QFileDialog.getOpenFileNames(self, "Select Input Files")
        if files:
            self.files_listwidget.clear()
            for file in files:
                self.files_listwidget.addItem(file)

    def decrypt_action(self):
        files = [self.files_listwidget.item(i).text() for i in range(self.files_listwidget.count())]
        password = self.password_lineedit.text().strip()
        salt_text = self.salt_lineedit.text().strip()
        salt = salt_text if salt_text else None

        if not files or not password:
            QMessageBox.critical(self, "Error", "Please select files and ensure crypt credentials are provided.")
            return

        try:
            data_key = make_key(password, salt)
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Key derivation failed:\n{e}")
            return

        dest = self.dest_dir_lineedit.text().strip() if self.dest_dir_lineedit.text().strip() else None

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
        if self.password_toggle_button.isChecked():
            self.password_lineedit.setEchoMode(QLineEdit.EchoMode.Normal)
            self.password_toggle_button.setIcon(qta.icon('fa5s.eye'))
        else:
            self.password_lineedit.setEchoMode(QLineEdit.EchoMode.Password)
            self.password_toggle_button.setIcon(qta.icon('fa5s.eye-slash'))

    def toggle_salt_visibility(self):
        if self.salt_toggle_button.isChecked():
            self.salt_lineedit.setEchoMode(QLineEdit.EchoMode.Normal)
            self.salt_toggle_button.setIcon(qta.icon('fa5s.eye'))
        else:
            self.salt_lineedit.setEchoMode(QLineEdit.EchoMode.Password)
            self.salt_toggle_button.setIcon(qta.icon('fa5s.eye-slash'))