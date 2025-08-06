"""
Blog management functionality
"""

import json
import os
from pathlib import Path
from PySide6.QtCore import QSettings, QStandardPaths
from PySide6.QtWidgets import (
    QDialog, QVBoxLayout, QHBoxLayout, QListWidget, QPushButton,
    QMessageBox, QFileDialog, QInputDialog, QFormLayout, QLineEdit,
    QLabel, QDialogButtonBox, QTextEdit, QGroupBox
)


class BlogManager:
    """Manager for multiple Hugo blogs"""
    
    def __init__(self):
        self.settings = QSettings()
        self.config_file = self.get_config_file_path()
        self.load_blogs()
        
    def get_config_file_path(self):
        """Get the path to the blogs configuration file"""
        app_data_dir = QStandardPaths.writableLocation(
            QStandardPaths.StandardLocation.AppDataLocation
        )
        os.makedirs(app_data_dir, exist_ok=True)
        return os.path.join(app_data_dir, "blogs.json")
        
    def load_blogs(self):
        """Load blogs configuration from file"""
        try:
            if os.path.exists(self.config_file):
                with open(self.config_file, 'r', encoding='utf-8') as f:
                    self.blogs = json.load(f)
            else:
                self.blogs = {}
        except Exception:
            self.blogs = {}
            
    def save_blogs(self):
        """Save blogs configuration to file"""
        try:
            with open(self.config_file, 'w', encoding='utf-8') as f:
                json.dump(self.blogs, f, indent=2)
        except Exception as e:
            print(f"Failed to save blogs config: {e}")
            
    def add_blog(self, name, root_path, public_path=None, publish_command=""):
        """Add a new blog"""
        self.blogs[name] = {
            'root_path': root_path,
            'public_path': public_path or os.path.join(root_path, 'public'),
            'publish_command': publish_command
        }
        self.save_blogs()
        
    def remove_blog(self, name):
        """Remove a blog"""
        if name in self.blogs:
            del self.blogs[name]
            self.save_blogs()
            
    def get_blog(self, name):
        """Get blog information"""
        return self.blogs.get(name)
        
    def get_all_blogs(self):
        """Get all blogs"""
        return self.blogs
        
    def update_blog(self, name, **kwargs):
        """Update blog information"""
        if name in self.blogs:
            self.blogs[name].update(kwargs)
            self.save_blogs()
            
    def add_blog_dialog(self, parent):
        """Show dialog to add a new blog"""
        dialog = AddBlogDialog(parent)
        if dialog.exec() == QDialog.DialogCode.Accepted:
            blog_data = dialog.get_blog_data()
            self.add_blog(**blog_data)
            return True
        return False
        
    def manage_blogs_dialog(self, parent):
        """Show dialog to manage blogs"""
        dialog = ManageBlogsDialog(self, parent)
        dialog.exec()
        
    def show_publish_command(self, blog_name, parent):
        """Show publish command for a blog"""
        blog = self.get_blog(blog_name)
        if not blog:
            return
            
        dialog = PublishCommandDialog(blog, parent)
        if dialog.exec() == QDialog.DialogCode.Accepted:
            new_command = dialog.get_command()
            self.update_blog(blog_name, publish_command=new_command)


class AddBlogDialog(QDialog):
    """Dialog for adding a new blog"""
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Add Hugo Blog")
        self.setModal(True)
        self.resize(500, 300)
        
        self.init_ui()
        
    def init_ui(self):
        """Initialize the user interface"""
        layout = QVBoxLayout(self)
        
        # Form layout
        form_layout = QFormLayout()
        
        self.name_edit = QLineEdit()
        form_layout.addRow("Blog Name:", self.name_edit)
        
        # Root path selection
        root_layout = QHBoxLayout()
        self.root_path_edit = QLineEdit()
        browse_root_btn = QPushButton("Browse...")
        browse_root_btn.clicked.connect(self.browse_root_path)
        root_layout.addWidget(self.root_path_edit)
        root_layout.addWidget(browse_root_btn)
        form_layout.addRow("Root Path:", root_layout)
        
        # Public path selection
        public_layout = QHBoxLayout()
        self.public_path_edit = QLineEdit()
        browse_public_btn = QPushButton("Browse...")
        browse_public_btn.clicked.connect(self.browse_public_path)
        public_layout.addWidget(self.public_path_edit)
        public_layout.addWidget(browse_public_btn)
        form_layout.addRow("Public Path:", public_layout)
        
        # Publish command
        self.publish_command_edit = QTextEdit()
        self.publish_command_edit.setMaximumHeight(80)
        form_layout.addRow("Publish Command:", self.publish_command_edit)
        
        layout.addLayout(form_layout)
        
        # Buttons
        button_box = QDialogButtonBox(
            QDialogButtonBox.StandardButton.Ok | QDialogButtonBox.StandardButton.Cancel
        )
        button_box.accepted.connect(self.accept)
        button_box.rejected.connect(self.reject)
        layout.addWidget(button_box)
        
    def browse_root_path(self):
        """Browse for root path"""
        path = QFileDialog.getExistingDirectory(self, "Select Hugo Site Root")
        if path:
            self.root_path_edit.setText(path)
            # Auto-fill public path
            public_path = os.path.join(path, "public")
            self.public_path_edit.setText(public_path)
            
    def browse_public_path(self):
        """Browse for public path"""
        path = QFileDialog.getExistingDirectory(self, "Select Public Directory")
        if path:
            self.public_path_edit.setText(path)
            
    def get_blog_data(self):
        """Get the blog data from the form"""
        return {
            'name': self.name_edit.text(),
            'root_path': self.root_path_edit.text(),
            'public_path': self.public_path_edit.text(),
            'publish_command': self.publish_command_edit.toPlainText()
        }


class ManageBlogsDialog(QDialog):
    """Dialog for managing existing blogs"""
    
    def __init__(self, blog_manager, parent=None):
        super().__init__(parent)
        self.blog_manager = blog_manager
        self.setWindowTitle("Manage Blogs")
        self.setModal(True)
        self.resize(600, 400)
        
        self.init_ui()
        self.refresh_list()
        
    def init_ui(self):
        """Initialize the user interface"""
        layout = QHBoxLayout(self)
        
        # Left side - blog list
        left_layout = QVBoxLayout()
        
        self.blog_list = QListWidget()
        self.blog_list.currentItemChanged.connect(self.on_blog_selected)
        left_layout.addWidget(QLabel("Blogs:"))
        left_layout.addWidget(self.blog_list)
        
        # Blog list buttons
        list_buttons = QHBoxLayout()
        
        add_btn = QPushButton("Add")
        add_btn.clicked.connect(self.add_blog)
        list_buttons.addWidget(add_btn)
        
        remove_btn = QPushButton("Remove")
        remove_btn.clicked.connect(self.remove_blog)
        list_buttons.addWidget(remove_btn)
        
        left_layout.addLayout(list_buttons)
        layout.addLayout(left_layout)
        
        # Right side - blog details
        right_layout = QVBoxLayout()
        
        details_group = QGroupBox("Blog Details")
        details_layout = QFormLayout(details_group)
        
        self.details_name = QLineEdit()
        details_layout.addRow("Name:", self.details_name)
        
        self.details_root = QLineEdit()
        details_layout.addRow("Root Path:", self.details_root)
        
        self.details_public = QLineEdit()
        details_layout.addRow("Public Path:", self.details_public)
        
        self.details_command = QTextEdit()
        self.details_command.setMaximumHeight(100)
        details_layout.addRow("Publish Command:", self.details_command)
        
        save_btn = QPushButton("Save Changes")
        save_btn.clicked.connect(self.save_changes)
        details_layout.addRow(save_btn)
        
        right_layout.addWidget(details_group)
        layout.addLayout(right_layout)
        
        # Dialog buttons
        button_box = QDialogButtonBox(QDialogButtonBox.StandardButton.Close)
        button_box.rejected.connect(self.accept)
        layout.addWidget(button_box)
        
    def refresh_list(self):
        """Refresh the blog list"""
        self.blog_list.clear()
        for blog_name in self.blog_manager.get_all_blogs().keys():
            self.blog_list.addItem(blog_name)
            
    def on_blog_selected(self, current, previous):
        """Handle blog selection"""
        if not current:
            return
            
        blog_name = current.text()
        blog = self.blog_manager.get_blog(blog_name)
        
        if blog:
            self.details_name.setText(blog_name)
            self.details_root.setText(blog.get('root_path', ''))
            self.details_public.setText(blog.get('public_path', ''))
            self.details_command.setPlainText(blog.get('publish_command', ''))
            
    def add_blog(self):
        """Add a new blog"""
        if self.blog_manager.add_blog_dialog(self):
            self.refresh_list()
            
    def remove_blog(self):
        """Remove selected blog"""
        current = self.blog_list.currentItem()
        if not current:
            return
            
        blog_name = current.text()
        reply = QMessageBox.question(
            self, "Remove Blog",
            f"Are you sure you want to remove '{blog_name}'?",
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No,
            QMessageBox.StandardButton.No
        )
        
        if reply == QMessageBox.StandardButton.Yes:
            self.blog_manager.remove_blog(blog_name)
            self.refresh_list()
            
    def save_changes(self):
        """Save changes to selected blog"""
        current = self.blog_list.currentItem()
        if not current:
            return
            
        old_name = current.text()
        new_name = self.details_name.text()
        
        if not new_name:
            QMessageBox.warning(self, "Warning", "Blog name cannot be empty.")
            return
            
        # If name changed, remove old and add new
        if old_name != new_name:
            self.blog_manager.remove_blog(old_name)
            
        self.blog_manager.add_blog(
            new_name,
            self.details_root.text(),
            self.details_public.text(),
            self.details_command.toPlainText()
        )
        
        self.refresh_list()
        QMessageBox.information(self, "Success", "Blog updated successfully.")


class PublishCommandDialog(QDialog):
    """Dialog for showing and editing publish command"""
    
    def __init__(self, blog, parent=None):
        super().__init__(parent)
        self.blog = blog
        self.setWindowTitle("Publish Command")
        self.setModal(True)
        self.resize(500, 300)
        
        self.init_ui()
        
    def init_ui(self):
        """Initialize the user interface"""
        layout = QVBoxLayout(self)
        
        layout.addWidget(QLabel("Publish command for this blog:"))
        
        self.command_edit = QTextEdit()
        self.command_edit.setPlainText(self.blog.get('publish_command', ''))
        layout.addWidget(self.command_edit)
        
        # Info label
        info_label = QLabel(
            "This command will be shown when you click 'Publish Command' "
            "so you can copy and paste it into a terminal."
        )
        info_label.setWordWrap(True)
        info_label.setStyleSheet("color: gray; font-size: 10px;")
        layout.addWidget(info_label)
        
        # Buttons
        button_layout = QHBoxLayout()
        
        copy_btn = QPushButton("Copy to Clipboard")
        copy_btn.clicked.connect(self.copy_to_clipboard)
        button_layout.addWidget(copy_btn)
        
        button_layout.addStretch()
        
        button_box = QDialogButtonBox(
            QDialogButtonBox.StandardButton.Ok | QDialogButtonBox.StandardButton.Cancel
        )
        button_box.accepted.connect(self.accept)
        button_box.rejected.connect(self.reject)
        button_layout.addWidget(button_box)
        
        layout.addLayout(button_layout)
        
    def copy_to_clipboard(self):
        """Copy command to clipboard"""
        from PySide6.QtGui import QGuiApplication
        clipboard = QGuiApplication.clipboard()
        clipboard.setText(self.command_edit.toPlainText())
        
    def get_command(self):
        """Get the command text"""
        return self.command_edit.toPlainText()
