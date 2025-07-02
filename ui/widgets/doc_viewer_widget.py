from PySide6.QtWidgets import QVBoxLayout, QTextEdit
from .base_widget import BaseWidget
import os
import markdown

class DocViewerWidget(BaseWidget):
    def __init__(self, md_path=None, parent=None):
        super().__init__(parent)
        self.set_title("User Guide")
        self.text_edit = QTextEdit()
        self.text_edit.setReadOnly(True)
        self.content_layout.addWidget(self.text_edit)
        if md_path is None:
            md_path = os.path.join(os.path.dirname(__file__), '../../docs/user/USER_GUIDE.md')
        self.load_markdown(md_path)

    def load_markdown(self, md_path):
        if not os.path.exists(md_path):
            self.text_edit.setHtml("<h2>Documentation not found.</h2>")
            return
        with open(md_path, 'r', encoding='utf-8') as f:
            md_text = f.read()
        html = markdown.markdown(md_text, extensions=['extra', 'toc', 'tables'])
        # Basic styling for readability
        html = f"""
        <html><head><style>
        body {{ font-family: sans-serif; margin: 2em; }}
        h1, h2, h3 {{ color: #2a4d7a; }}
        table {{ border-collapse: collapse; }}
        th, td {{ border: 1px solid #ccc; padding: 4px 8px; }}
        </style></head><body>{html}</body></html>
        """
        self.text_edit.setHtml(html)

    def cleanup(self):
        # No-op for QTextEdit
        pass
