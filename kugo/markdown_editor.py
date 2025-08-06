"""
Markdown editor with preview functionality
"""

import os
import markdown
from pathlib import Path
from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QTextEdit,
    QPushButton, QSplitter, QFileDialog, QMessageBox, QTabWidget,
    QPlainTextEdit, QCheckBox
)
from PySide6.QtCore import Qt, QTimer, QUrl, Signal
from PySide6.QtGui import QFont, QTextDocument


class MarkdownEditor(QWidget):
    """Markdown editor with live preview"""
    
    image_dropped = Signal(str)  # Signal emitted when an image is dropped
    delete_requested = Signal()  # Signal emitted when delete button is clicked
    
    def __init__(self):
        super().__init__()
        self.current_file = None
        
        # Initialize markdown processor with comprehensive extensions
        try:
            self.markdown_processor = markdown.Markdown(
                extensions=[
                    'markdown.extensions.codehilite',
                    'markdown.extensions.fenced_code', 
                    'markdown.extensions.tables',
                    'markdown.extensions.toc',
                    'markdown.extensions.nl2br',
                    'markdown.extensions.sane_lists'
                ],
                extension_configs={
                    'codehilite': {
                        'css_class': 'highlight',
                        'use_pygments': True
                    }
                }
            )
            print("✓ Markdown processor initialized with extensions")
        except Exception as e:
            print(f"⚠ Markdown processor error: {e}")
            # Fallback to basic processor
            self.markdown_processor = markdown.Markdown()
        
        self.init_ui()
        self.setup_timer()
        
    def init_ui(self):
        """Initialize the user interface"""
        layout = QVBoxLayout(self)
        
        # Control buttons
        button_layout = QHBoxLayout()
        
        # View mode tabs
        self.tab_widget = QTabWidget()
        
        # Editor tab
        editor_widget = QWidget()
        editor_layout = QVBoxLayout(editor_widget)
        
        self.text_editor = QPlainTextEdit()
        self.text_editor.setFont(QFont("Courier", 12))
        self.text_editor.textChanged.connect(self.on_text_changed)
        
        # Enable drag and drop for images
        self.text_editor.setAcceptDrops(True)
        self.text_editor.dragEnterEvent = self.drag_enter_event
        self.text_editor.dropEvent = self.drop_event
        
        editor_layout.addWidget(self.text_editor)
        
        self.tab_widget.addTab(editor_widget, "Edit")
        
        # Preview tab
        preview_widget = QWidget()
        preview_layout = QVBoxLayout(preview_widget)
        
        # Preview area
        self.use_webengine = False
        try:
            from PySide6.QtWebEngineWidgets import QWebEngineView
            self.preview = QWebEngineView()
            self.use_webengine = True
            print("✓ Using QWebEngineView for preview")
        except ImportError as e:
            print(f"⚠ WebEngine not available ({e}), falling back to QTextEdit")
            # Fallback to QTextEdit if WebEngine is not available
            self.preview = QTextEdit()
            self.preview.setReadOnly(True)
            self.use_webengine = False
            
        preview_layout.addWidget(self.preview)
        self.tab_widget.addTab(preview_widget, "Preview")
        
        # Auto-update preview when switching to preview tab
        self.tab_widget.currentChanged.connect(self.on_tab_changed)
        
        layout.addWidget(self.tab_widget)
        
        # Simplified control bar
        control_layout = QHBoxLayout()
        
        save_btn = QPushButton("Save")
        save_btn.clicked.connect(self.save_file)
        control_layout.addWidget(save_btn)
        
        self.delete_btn = QPushButton("Delete File")
        self.delete_btn.clicked.connect(self.delete_requested.emit)
        self.delete_btn.setEnabled(False)  # Initially disabled
        control_layout.addWidget(self.delete_btn)
        
        control_layout.addStretch()
        
        # Auto-update checkbox (smaller, in corner)
        self.auto_update_checkbox = QCheckBox("Auto-update preview")
        self.auto_update_checkbox.setChecked(True)
        control_layout.addWidget(self.auto_update_checkbox)
        
        layout.addLayout(control_layout)
        
    def setup_timer(self):
        """Setup timer for live preview updates"""
        self.update_timer = QTimer()
        self.update_timer.setSingleShot(True)
        self.update_timer.timeout.connect(self.update_preview)
        
    def on_text_changed(self):
        """Handle text changes for live preview"""
        if self.auto_update_checkbox.isChecked():
            self.update_timer.start(500)  # 500ms delay for performance
            
    def on_tab_changed(self, index):
        """Handle tab change - update preview when switching to preview tab"""
        if index == 1:  # Preview tab
            self.update_preview()
            
    def toggle_preview(self, enabled):
        """Toggle preview visibility - now just updates when on preview tab"""
        if enabled and self.tab_widget.currentIndex() == 1:
            self.update_preview()
            
    def update_preview(self):
        """Update the markdown preview"""
        # Only update if auto-update is enabled or we're on the preview tab
        if not self.auto_update_checkbox.isChecked() and self.tab_widget.currentIndex() != 1:
            return
            
        markdown_text = self.text_editor.toPlainText()
        if not markdown_text.strip():
            # Clear preview if no content
            if self.use_webengine:
                self.preview.setHtml("<html><body><p><em>No content to preview</em></p></body></html>")
            else:
                self.preview.setHtml("<p><em>No content to preview</em></p>")
            return
            
        try:
            html = self.markdown_to_html(markdown_text)
            
            if self.use_webengine:
                # QWebEngineView - load full HTML
                self.preview.setHtml(html)
                print("✓ Preview updated with WebEngine")
            else:
                # QTextEdit fallback - set rich text
                self.preview.setHtml(html)
                print("✓ Preview updated with QTextEdit fallback")
        except Exception as e:
            print(f"✗ Error updating preview: {e}")
            error_html = f"<html><body><p style='color: red;'>Error rendering preview: {e}</p></body></html>"
            if self.use_webengine:
                self.preview.setHtml(error_html)
            else:
                self.preview.setHtml(error_html)
        
    def markdown_to_html(self, markdown_text):
        """Convert markdown to HTML"""
        # Reset the markdown processor
        self.markdown_processor.reset()
        
        # Add custom CSS for better styling
        html = self.markdown_processor.convert(markdown_text)
        
        styled_html = f"""
        <!DOCTYPE html>
        <html>
        <head>
            <meta charset="utf-8">
            <meta name="viewport" content="width=device-width, initial-scale=1">
            <style>
                body {{
                    font-family: 'Segoe UI', 'Noto Sans', Tahoma, Geneva, Verdana, sans-serif;
                    line-height: 1.6;
                    margin: 20px;
                    background-color: #ffffff;
                    color: #333333;
                    max-width: 800px;
                    margin: 0 auto;
                    padding: 20px;
                }}
                
                h1, h2, h3, h4, h5, h6 {{
                    color: #2c3e50;
                    margin-top: 30px;
                    margin-bottom: 15px;
                    font-weight: 600;
                }}
                
                h1 {{ 
                    border-bottom: 3px solid #3498db; 
                    padding-bottom: 10px; 
                    font-size: 2.2em;
                }}
                
                h2 {{ 
                    border-bottom: 2px solid #ecf0f1; 
                    padding-bottom: 5px; 
                    font-size: 1.8em;
                }}
                
                h3 {{ font-size: 1.4em; }}
                h4 {{ font-size: 1.2em; }}
                h5 {{ font-size: 1.1em; }}
                h6 {{ font-size: 1em; }}
                
                p {{
                    margin-bottom: 16px;
                    text-align: justify;
                }}
                
                a {{
                    color: #3498db;
                    text-decoration: none;
                }}
                
                a:hover {{
                    text-decoration: underline;
                }}
                
                code {{
                    background-color: #f8f9fa;
                    border: 1px solid #e9ecef;
                    border-radius: 4px;
                    padding: 3px 6px;
                    font-family: 'Cascadia Code', 'Fira Code', 'Consolas', 'Monaco', 'Courier New', monospace;
                    font-size: 0.9em;
                    color: #e74c3c;
                }}
                
                pre {{
                    background-color: #f8f9fa;
                    border: 1px solid #e9ecef;
                    border-radius: 6px;
                    padding: 20px;
                    overflow-x: auto;
                    margin: 20px 0;
                    line-height: 1.4;
                }}
                
                pre code {{
                    background: none;
                    border: none;
                    padding: 0;
                    color: inherit;
                    font-size: 0.95em;
                }}
                
                blockquote {{
                    border-left: 4px solid #3498db;
                    margin: 20px 0;
                    padding: 10px 20px;
                    color: #7f8c8d;
                    background-color: #f8f9fa;
                    border-radius: 0 4px 4px 0;
                }}
                
                ul, ol {{
                    margin-bottom: 16px;
                    padding-left: 30px;
                }}
                
                li {{
                    margin-bottom: 8px;
                }}
                
                table {{
                    border-collapse: collapse;
                    width: 100%;
                    margin: 20px 0;
                    box-shadow: 0 2px 4px rgba(0,0,0,0.1);
                }}
                
                th, td {{
                    border: 1px solid #dee2e6;
                    padding: 12px 16px;
                    text-align: left;
                }}
                
                th {{
                    background-color: #3498db;
                    color: white;
                    font-weight: 600;
                }}
                
                tr:nth-child(even) {{
                    background-color: #f8f9fa;
                }}
                
                tr:hover {{
                    background-color: #e3f2fd;
                }}
                
                img {{
                    max-width: 100%;
                    height: auto;
                    border-radius: 4px;
                    box-shadow: 0 2px 8px rgba(0,0,0,0.1);
                    margin: 10px 0;
                }}
                
                hr {{
                    border: none;
                    height: 2px;
                    background: linear-gradient(to right, #3498db, #ecf0f1, #3498db);
                    margin: 30px 0;
                }}
                
                /* Code highlighting styles */
                .codehilite {{
                    background: #f8f9fa;
                    border-radius: 6px;
                    padding: 20px;
                    margin: 20px 0;
                    overflow-x: auto;
                }}
                
                .codehilite pre {{
                    background: none;
                    border: none;
                    padding: 0;
                    margin: 0;
                }}
                
                /* Table of contents */
                .toc {{
                    background-color: #f8f9fa;
                    border: 1px solid #e9ecef;
                    border-radius: 6px;
                    padding: 20px;
                    margin: 20px 0;
                }}
                
                .toc ul {{
                    list-style-type: none;
                    padding-left: 20px;
                }}
                
                .toc a {{
                    color: #2c3e50;
                    text-decoration: none;
                }}
                
                .toc a:hover {{
                    color: #3498db;
                }}
                
                /* Responsive design */
                @media (max-width: 768px) {{
                    body {{
                        padding: 15px;
                        font-size: 16px;
                    }}
                    
                    h1 {{ font-size: 1.8em; }}
                    h2 {{ font-size: 1.5em; }}
                    h3 {{ font-size: 1.3em; }}
                    
                    table, th, td {{
                        font-size: 14px;
                        padding: 8px;
                    }}
                }}
            </style>
        </head>
        <body>
            {html}
        </body>
        </html>
        """
        
        return styled_html
        
    def load_file(self, file_path):
        """Load a file into the editor"""
        try:
            with open(file_path, 'r', encoding='utf-8') as file:
                content = file.read()
                self.text_editor.setPlainText(content)
                self.current_file = file_path
                self.delete_btn.setEnabled(True)  # Enable delete button
                self.update_preview()
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Failed to load file: {str(e)}")
            
    def save_file(self):
        """Save the current file"""
        if not self.current_file:
            self.save_file_as()
            return
            
        try:
            with open(self.current_file, 'w', encoding='utf-8') as file:
                file.write(self.text_editor.toPlainText())
            QMessageBox.information(self, "Success", "File saved successfully!")
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Failed to save file: {str(e)}")
            
    def save_file_as(self):
        """Save the file with a new name"""
        file_path, _ = QFileDialog.getSaveFileName(
            self, "Save File", "", "Markdown Files (*.md);;All Files (*)"
        )
        
        if file_path:
            self.current_file = file_path
            self.save_file()
            
    def get_current_text(self):
        """Get the current text in the editor"""
        return self.text_editor.toPlainText()
        
    def set_text(self, text):
        """Set text in the editor"""
        self.text_editor.setPlainText(text)
        self.update_preview()
        
    def clear(self):
        """Clear the editor"""
        self.text_editor.clear()
        self.current_file = None
        self.delete_btn.setEnabled(False)  # Disable delete button
        if self.use_webengine:
            self.preview.setHtml("<html><body></body></html>")
        else:
            self.preview.setHtml("")
    
    def insert_at_cursor(self, text):
        """Insert text at the current cursor position"""
        cursor = self.text_editor.textCursor()
        cursor.insertText(text)
        self.text_editor.setTextCursor(cursor)
        self.update_preview()
        
    def drag_enter_event(self, event):
        """Handle drag enter events for image files"""
        if event.mimeData().hasUrls():
            # Check if any URL is an image file
            for url in event.mimeData().urls():
                file_path = url.toLocalFile()
                if file_path.lower().endswith(('.png', '.jpg', '.jpeg', '.gif', '.bmp', '.webp', '.svg')):
                    event.acceptProposedAction()
                    return
        event.ignore()
        
    def drop_event(self, event):
        """Handle drop events for image files"""
        if event.mimeData().hasUrls():
            for url in event.mimeData().urls():
                file_path = url.toLocalFile()
                if file_path.lower().endswith(('.png', '.jpg', '.jpeg', '.gif', '.bmp', '.webp', '.svg')):
                    # Signal to main window to handle image insertion
                    self.image_dropped.emit(file_path)
                    event.acceptProposedAction()
                    return
        event.ignore()
