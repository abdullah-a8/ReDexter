import sys
from PyQt6.QtWidgets import QApplication
from ui import MainWindow
from themes import original_dark

def main():
    app = QApplication(sys.argv)
    # Set default theme
    app.setStyleSheet(original_dark)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())

if __name__ == '__main__':
    main()