"""
Main window for Kugo application
"""

import os
import json
from pathlib import Path
from PySide6.QtWidgets import (
    QMainWindow, QWidget, QHBoxLayout, QVBoxLayout, QSplitter,
    QTabWidget, QListWidget, QListWidgetItem, QTextEdit, QPushButton,
    QMenuBar, QMenu, QFileDialog, QMessageBox, QDialog, QLabel,
    QLineEdit, QDialogButtonBox, QFormLayout, QCheckBox, QToolBar,
    QStatusBar, QComboBox, QInputDialog
)
from PySide6.QtCore import Qt, QSettings, Signal, QThread
from PySide6.QtGui import QAction, QIcon, QFont

from kugo.markdown_editor import MarkdownEditor
from kugo.file_browser import FileBrowser
from kugo.hugo_manager import HugoManager
from kugo.blog_manager import BlogManager
from kugo.resources import get_app_icon


class MainWindow(QMainWindow):
    """Main application window"""
    
    def __init__(self):
        super().__init__()
        self.settings = QSettings()
        self.blog_manager = BlogManager()
        self.hugo_manager = HugoManager()
        self.current_blog_path = None
        
        self.init_ui()
        self.connect_signals()
        self.load_settings()
        
    def init_ui(self):
        """Initialize the user interface"""
        self.setWindowTitle("Kugo - Hugo Front-end")
        self.setGeometry(100, 100, 1200, 800)
        
        # Set window icon
        self.setWindowIcon(get_app_icon())
        
        # Set WM_CLASS for proper GNOME dock integration
        self.setProperty("applicationName", "Kugo")
        
        # Create central widget
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        
        # Create main layout
        main_layout = QHBoxLayout(central_widget)
        
        # Create splitter for resizable panels
        splitter = QSplitter(Qt.Orientation.Horizontal)
        main_layout.addWidget(splitter)
        
        # Left panel - file browser
        self.create_left_panel(splitter)
        
        # Right panel - markdown editor
        self.create_right_panel(splitter)
        
        # Set splitter proportions
        splitter.setStretchFactor(0, 1)
        splitter.setStretchFactor(1, 2)
        
        # Create menu bar
        self.create_menu_bar()
        
        # Create toolbar
        self.create_toolbar()
        
        # Create status bar
        self.create_status_bar()
        
    def create_left_panel(self, parent):
        """Create the left panel with posts and pages tabs"""
        left_widget = QWidget()
        left_layout = QVBoxLayout(left_widget)
        
        # Blog selector
        blog_layout = QHBoxLayout()
        self.blog_combo = QComboBox()
        self.blog_combo.currentTextChanged.connect(self.on_blog_changed)
        blog_layout.addWidget(QLabel("Blog:"))
        blog_layout.addWidget(self.blog_combo)
        
        add_blog_btn = QPushButton("Add Blog")
        add_blog_btn.clicked.connect(self.add_blog)
        blog_layout.addWidget(add_blog_btn)
        
        left_layout.addLayout(blog_layout)
        
        # File browser with tabs
        self.file_browser = FileBrowser()
        left_layout.addWidget(self.file_browser)
        
        # Hugo commands section
        hugo_group = QVBoxLayout()
        
        # Only keep essential buttons
        build_btn = QPushButton("Build Site")
        build_btn.clicked.connect(self.hugo_build)
        hugo_group.addWidget(build_btn)
        
        serve_btn = QPushButton("Serve Site")
        serve_btn.clicked.connect(self.hugo_serve)
        hugo_group.addWidget(serve_btn)
        
        self.stop_serve_btn = QPushButton("Stop Server")
        self.stop_serve_btn.clicked.connect(self.hugo_stop_serve)
        self.stop_serve_btn.setEnabled(False)  # Initially disabled
        hugo_group.addWidget(self.stop_serve_btn)
        
        left_layout.addLayout(hugo_group)
        
        parent.addWidget(left_widget)
        
    def create_right_panel(self, parent):
        """Create the right panel with markdown editor"""
        self.markdown_editor = MarkdownEditor()
        parent.addWidget(self.markdown_editor)
        
    def create_menu_bar(self):
        """Create the menu bar"""
        menubar = self.menuBar()
        
        # File menu
        file_menu = menubar.addMenu("&File")
        
        open_blog_action = QAction("&Open Blog...", self)
        open_blog_action.setShortcut("Ctrl+O")
        open_blog_action.triggered.connect(self.open_blog)
        file_menu.addAction(open_blog_action)
        
        file_menu.addSeparator()
        
        open_file_action = QAction("Open &File...", self)
        open_file_action.setShortcut("Ctrl+Shift+O")
        open_file_action.triggered.connect(self.open_file)
        file_menu.addAction(open_file_action)
        
        save_action = QAction("&Save", self)
        save_action.setShortcut("Ctrl+S")
        save_action.triggered.connect(self.save_file)
        file_menu.addAction(save_action)
        
        file_menu.addSeparator()
        
        exit_action = QAction("E&xit", self)
        exit_action.setShortcut("Ctrl+Q")
        exit_action.triggered.connect(self.close)
        file_menu.addAction(exit_action)
        
        # Content menu
        content_menu = menubar.addMenu("&Content")
        
        new_draft_action = QAction("New &Draft", self)
        new_draft_action.setShortcut("Ctrl+N")
        new_draft_action.triggered.connect(self.file_browser.create_new_draft)
        content_menu.addAction(new_draft_action)
        
        new_page_action = QAction("New Pa&ge", self)
        new_page_action.setShortcut("Ctrl+Alt+N")
        new_page_action.triggered.connect(self.file_browser.create_new_page)
        content_menu.addAction(new_page_action)
        
        content_menu.addSeparator()
        
        insert_image_action = QAction("Insert &Image...", self)
        insert_image_action.setShortcut("Ctrl+I")
        insert_image_action.triggered.connect(self.insert_image)
        content_menu.addAction(insert_image_action)
        
        content_menu.addSeparator()
        
        delete_action = QAction("&Delete Current File", self)
        delete_action.setShortcut("Delete")
        delete_action.triggered.connect(self.delete_current_file)
        content_menu.addAction(delete_action)
        
        # Hugo menu
        hugo_menu = menubar.addMenu("&Hugo")
        
        build_action = QAction("&Build Site", self)
        build_action.setShortcut("F5")
        build_action.triggered.connect(self.hugo_build)
        hugo_menu.addAction(build_action)
        
        serve_action = QAction("&Serve Site", self)
        serve_action.setShortcut("F6")
        serve_action.triggered.connect(self.hugo_serve)
        hugo_menu.addAction(serve_action)
        
        stop_serve_action = QAction("S&top Server", self)
        stop_serve_action.setShortcut("F7")
        stop_serve_action.triggered.connect(self.hugo_stop_serve)
        hugo_menu.addAction(stop_serve_action)
        
        hugo_menu.addSeparator()
        
        # Draft inclusion toggle
        self.include_drafts_action = QAction("Include &Drafts in Preview", self)
        self.include_drafts_action.setCheckable(True)
        self.include_drafts_action.setChecked(False)  # Default to not showing drafts
        self.include_drafts_action.triggered.connect(self.toggle_draft_inclusion)
        hugo_menu.addAction(self.include_drafts_action)
        
        hugo_menu.addSeparator()
        
        config_action = QAction("Edit &Config", self)
        config_action.triggered.connect(self.edit_config)
        hugo_menu.addAction(config_action)
        
        hugo_menu.addSeparator()
        
        publish_action = QAction("&Publish Command", self)
        publish_action.triggered.connect(self.show_publish_command)
        hugo_menu.addAction(publish_action)
        
        hugo_menu.addSeparator()
        
        manage_blogs_action = QAction("&Manage Blogs", self)
        manage_blogs_action.triggered.connect(self.manage_blogs)
        hugo_menu.addAction(manage_blogs_action)
        
        # View menu
        view_menu = menubar.addMenu("&View")
        
        switch_to_edit_action = QAction("Switch to &Edit", self)
        switch_to_edit_action.setShortcut("Ctrl+1")
        switch_to_edit_action.triggered.connect(lambda: self.markdown_editor.tab_widget.setCurrentIndex(0))
        view_menu.addAction(switch_to_edit_action)
        
        switch_to_preview_action = QAction("Switch to &Preview", self)
        switch_to_preview_action.setShortcut("Ctrl+2")
        switch_to_preview_action.triggered.connect(lambda: self.markdown_editor.tab_widget.setCurrentIndex(1))
        view_menu.addAction(switch_to_preview_action)
        
        # Help menu
        help_menu = menubar.addMenu("&Help")
        
        about_action = QAction("&About", self)
        about_action.triggered.connect(self.about)
        help_menu.addAction(about_action)
        
    def create_toolbar(self):
        """Create the toolbar"""
        toolbar = QToolBar()
        self.addToolBar(toolbar)
        
        # Add common actions to toolbar
        toolbar.addAction("New Draft", self.new_draft)
        toolbar.addAction("New Page", self.new_page)
        toolbar.addSeparator()
        toolbar.addAction("Save", self.save_file)
        toolbar.addSeparator()
        toolbar.addAction("Build", self.hugo_build)
        toolbar.addAction("Serve", self.hugo_serve)
        
    def create_status_bar(self):
        """Create the status bar"""
        self.status_bar = QStatusBar()
        self.setStatusBar(self.status_bar)
        self.status_bar.showMessage("Ready")
        
    def connect_signals(self):
        """Connect signals between components"""
        self.file_browser.file_selected.connect(self.markdown_editor.load_file)
        self.file_browser.file_selected.connect(self.on_file_selected)
        
        # Connect image dropped signal
        self.markdown_editor.image_dropped.connect(self.handle_dropped_image)
        
        # Connect delete requested signal
        self.markdown_editor.delete_requested.connect(self.delete_current_file)
        
        # Connect Hugo manager signals
        self.hugo_manager.command_finished.connect(self.on_hugo_command_finished)
        self.hugo_manager.command_output.connect(self.on_hugo_output)
        
    def on_file_selected(self, file_path):
        """Handle file selection"""
        self.current_file_path = file_path  # Track current file
        self.status_bar.showMessage(f"Editing: {file_path}")
        
    def on_hugo_command_finished(self, command, exit_code):
        """Handle Hugo command completion"""
        if command == "serve":
            self.stop_serve_btn.setEnabled(False)  # Disable stop button when serve ends
            if exit_code == 0:
                self.status_bar.showMessage("✓ Hugo server stopped")
            else:
                self.status_bar.showMessage("✗ Hugo server stopped with error")
        else:
            if exit_code == 0:
                self.status_bar.showMessage(f"✓ {command} completed successfully")
            else:
                self.status_bar.showMessage(f"✗ {command} failed (exit code: {exit_code})")
            
    def on_hugo_output(self, output):
        """Handle Hugo command output"""
        print(f"Hugo: {output}")
        
    def handle_dropped_image(self, image_path):
        """Handle image dropped onto the editor"""
        if not self.current_blog_path:
            QMessageBox.warning(self, "Warning", "Please select a blog first.")
            return
            
        try:
            # Get the blog's static directory
            blog_static_dir = Path(self.current_blog_path) / "static" / "images"
            blog_static_dir.mkdir(parents=True, exist_ok=True)
            
            # Copy image to static/images directory
            image_file = Path(image_path)
            dest_path = blog_static_dir / image_file.name
            
            # Handle duplicate names
            counter = 1
            original_name = image_file.stem
            extension = image_file.suffix
            while dest_path.exists():
                new_name = f"{original_name}_{counter}{extension}"
                dest_path = blog_static_dir / new_name
                counter += 1
            
            # Copy the file
            import shutil
            shutil.copy2(image_path, dest_path)
            
            # Generate markdown image syntax
            image_url = f"/images/{dest_path.name}"
            alt_text = dest_path.stem.replace('_', ' ').replace('-', ' ').title()
            markdown_syntax = f"![{alt_text}]({image_url})"
            
            # Insert the markdown syntax into the editor
            self.markdown_editor.insert_at_cursor(markdown_syntax)
            
            self.status_bar.showMessage(f"✓ Image added: {dest_path.name}")
            
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Failed to handle dropped image: {str(e)}")
        # You could show this in a dedicated output window if needed
        
    def on_blog_changed(self, blog_name):
        """Handle blog selection change"""
        if blog_name:
            blog_info = self.blog_manager.get_blog(blog_name)
            if blog_info:
                self.current_blog_path = blog_info['root_path']
                self.file_browser.set_root_path(self.current_blog_path)
                self.hugo_manager.set_blog_path(self.current_blog_path)
                self.status_bar.showMessage(f"Blog: {blog_name}")
                
    def new_draft(self):
        """Create a new draft"""
        if not self.current_blog_path:
            QMessageBox.warning(self, "Warning", "Please select a blog first.")
            return
            
        self.file_browser.create_new_draft()
        
    def new_page(self):
        """Create a new page"""
        if not self.current_blog_path:
            QMessageBox.warning(self, "Warning", "Please select a blog first.")
            return
            
        self.file_browser.create_new_page()
        
    def delete_current_file(self):
        """Delete the currently opened file"""
        current_file = self.markdown_editor.current_file
        if not current_file:
            QMessageBox.warning(self, "Warning", "No file is currently open.")
            return
            
        file_path = Path(current_file)
        reply = QMessageBox.question(
            self, "Delete File",
            f"Are you sure you want to delete '{file_path.name}'?\nThis action cannot be undone.",
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No,
            QMessageBox.StandardButton.No
        )
        
        if reply == QMessageBox.StandardButton.Yes:
            try:
                os.remove(current_file)
                
                # Clear the editor
                self.markdown_editor.clear()
                
                # Refresh file browser
                self.file_browser.refresh_all()
                
                QMessageBox.information(self, "Success", "File deleted successfully.")
                
            except Exception as e:
                QMessageBox.critical(self, "Error", f"Failed to delete file: {str(e)}")
        
    def insert_image(self):
        """Insert an image into the current post/page"""
        current_file = self.markdown_editor.current_file
        if not current_file:
            QMessageBox.warning(self, "Warning", "Please open a post or page first.")
            return
            
        if not self.current_blog_path:
            QMessageBox.warning(self, "Warning", "Please select a blog first.")
            return
            
        # Open file dialog to select image
        image_path, _ = QFileDialog.getOpenFileName(
            self, "Select Image",
            os.path.expanduser("~"),
            "Image Files (*.png *.jpg *.jpeg *.gif *.bmp *.webp *.svg);;All Files (*)"
        )
        
        if not image_path:
            return
            
        try:
            # Get the blog's static directory
            blog_static_dir = Path(self.current_blog_path) / "static" / "images"
            blog_static_dir.mkdir(parents=True, exist_ok=True)
            
            # Copy image to static/images directory
            image_file = Path(image_path)
            dest_path = blog_static_dir / image_file.name
            
            # Handle duplicate names
            counter = 1
            original_name = image_file.stem
            extension = image_file.suffix
            while dest_path.exists():
                new_name = f"{original_name}_{counter}{extension}"
                dest_path = blog_static_dir / new_name
                counter += 1
            
            # Copy the file
            import shutil
            shutil.copy2(image_path, dest_path)
            
            # Generate markdown image syntax
            image_url = f"/images/{dest_path.name}"
            alt_text, ok = QInputDialog.getText(
                self, "Image Alt Text", 
                "Enter alt text for accessibility (optional):",
                text=dest_path.stem.replace('_', ' ').replace('-', ' ').title()
            )
            
            if ok:
                if alt_text.strip():
                    markdown_syntax = f"![{alt_text}]({image_url})"
                else:
                    markdown_syntax = f"![]({image_url})"
                
                # Insert the markdown syntax into the editor
                self.markdown_editor.insert_at_cursor(markdown_syntax)
                
                QMessageBox.information(
                    self, "Success", 
                    f"Image copied to static/images/ and markdown syntax inserted."
                )
            
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Failed to insert image: {str(e)}")
        
    def open_file(self):
        """Open a file"""
        file_path, _ = QFileDialog.getOpenFileName(
            self, "Open File", "", "Markdown Files (*.md);;All Files (*)"
        )
        if file_path:
            self.markdown_editor.load_file(file_path)
            
    def save_file(self):
        """Save the current file"""
        self.markdown_editor.save_file()
        
    def hugo_build(self):
        """Run Hugo build command"""
        if not self.current_blog_path:
            QMessageBox.warning(self, "Warning", "Please select a blog first.")
            return
            
        self.hugo_manager.build()
        self.status_bar.showMessage("Hugo build started...")
        
    def hugo_serve(self):
        """Run Hugo serve command"""
        if not self.current_blog_path:
            QMessageBox.warning(self, "Warning", "Please select a blog first.")
            return
            
        self.hugo_manager.serve()
        self.status_bar.showMessage("Hugo server started...")
        self.stop_serve_btn.setEnabled(True)  # Enable stop button
        
    def hugo_stop_serve(self):
        """Stop Hugo serve command"""
        self.hugo_manager.stop_serve()
        self.status_bar.showMessage("Hugo server stopped")
        self.stop_serve_btn.setEnabled(False)  # Disable stop button
        
    def toggle_draft_inclusion(self):
        """Toggle whether drafts are included in Hugo serve"""
        include_drafts = self.include_drafts_action.isChecked()
        self.hugo_manager.set_include_drafts(include_drafts)
        
        if include_drafts:
            self.status_bar.showMessage("Drafts will be included in next serve")
        else:
            self.status_bar.showMessage("Drafts will be excluded from next serve")
        
    def edit_config(self):
        """Edit Hugo configuration"""
        if not self.current_blog_path:
            QMessageBox.warning(self, "Warning", "Please select a blog first.")
            return
            
        config_path = self.hugo_manager.get_config_path()
        if config_path and os.path.exists(config_path):
            self.markdown_editor.load_file(config_path)
        else:
            QMessageBox.warning(self, "Warning", "Configuration file not found.")
            
    def show_publish_command(self):
        """Show the publish command for the current blog"""
        if not self.current_blog_path:
            QMessageBox.warning(self, "Warning", "Please select a blog first.")
            return
            
        blog_name = self.blog_combo.currentText()
        if blog_name:
            self.blog_manager.show_publish_command(blog_name, self)
            
    def add_blog(self):
        """Add a new Hugo blog"""
        self.blog_manager.add_blog_dialog(self)
        self.refresh_blog_list()
        
    def open_blog(self):
        """Open a blog directory directly"""
        directory = QFileDialog.getExistingDirectory(
            self, "Select Hugo Blog Directory"
        )
        if directory:
            # Check if it's a valid Hugo site
            config_files = ['config.toml', 'config.yaml', 'config.yml', 'hugo.toml', 'hugo.yaml', 'hugo.yml']
            has_config = any((Path(directory) / config).exists() for config in config_files)
            
            if has_config:
                # Add to blog manager if not already there
                blog_name = Path(directory).name
                blogs = self.blog_manager.get_all_blogs()
                if blog_name not in blogs:
                    self.blog_manager.add_blog(blog_name, directory)
                    self.refresh_blog_list()
                
                # Select the blog
                index = self.blog_combo.findText(blog_name)
                if index >= 0:
                    self.blog_combo.setCurrentIndex(index)
            else:
                QMessageBox.warning(
                    self, "Invalid Hugo Site",
                    "The selected directory does not appear to be a valid Hugo site.\n"
                    "Please select a directory containing a Hugo configuration file."
                )
        
    def manage_blogs(self):
        """Open blog management dialog"""
        self.blog_manager.manage_blogs_dialog(self)
        self.refresh_blog_list()
        
    def refresh_blog_list(self):
        """Refresh the blog list in the combo box"""
        self.blog_combo.clear()
        blogs = self.blog_manager.get_all_blogs()
        for blog_name in blogs.keys():
            self.blog_combo.addItem(blog_name)
            
    def about(self):
        """Show about dialog"""
        QMessageBox.about(
            self, "About Kugo",
            "Kugo - A Hugo front-end for KDE/Plasma\n\n"
            "Version 1.0.0\n"
            "Built with PySide6"
        )
        
    def load_settings(self):
        """Load application settings"""
        geometry = self.settings.value("geometry")
        if geometry:
            self.restoreGeometry(geometry)
            
        self.refresh_blog_list()
        
        # Select last used blog
        last_blog = self.settings.value("last_blog")
        if last_blog:
            index = self.blog_combo.findText(last_blog)
            if index >= 0:
                self.blog_combo.setCurrentIndex(index)
                
    def save_settings(self):
        """Save application settings"""
        self.settings.setValue("geometry", self.saveGeometry())
        self.settings.setValue("last_blog", self.blog_combo.currentText())
        
    def closeEvent(self, event):
        """Handle application close event"""
        self.save_settings()
        super().closeEvent(event)
