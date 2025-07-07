from typing import Optional
from PyQt6.QtWidgets import QListWidget
from PyQt6.QtCore import pyqtSignal
from PyQt6.QtGui import QDragEnterEvent, QDragMoveEvent, QDropEvent

class DragDropListWidget(QListWidget):
    filesAdded = pyqtSignal()  # Signal emitted when files are added
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setAcceptDrops(True)
        self.setDragEnabled(True)

    def dragEnterEvent(self, e: Optional[QDragEnterEvent]):
        if e is not None:
            mime_data = e.mimeData()
            if mime_data is not None and mime_data.hasUrls():
                e.acceptProposedAction()
                return
        super().dragEnterEvent(e)

    def dragMoveEvent(self, e: Optional[QDragMoveEvent]):
        if e is not None:
            mime_data = e.mimeData()
            if mime_data is not None and mime_data.hasUrls():
                e.acceptProposedAction()
                return
        super().dragMoveEvent(e)

    def dropEvent(self, event: Optional[QDropEvent]):
        if event is not None:
            mime_data = event.mimeData()
            if mime_data is not None and mime_data.hasUrls():
                for url in mime_data.urls():
                    file_path = url.toLocalFile()
                    if file_path:
                        self.addItem(file_path)
                event.acceptProposedAction()
                self.filesAdded.emit()  # Emit signal after adding files
                return
        super().dropEvent(event)