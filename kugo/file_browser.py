"""
File browser for posts and pages
"""

import os
import re
import toml
import yaml
from datetime import datetime
from pathlib import Path
from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QTabWidget, QListWidget, QListWidgetItem,
    QMenu, QInputDialog, QMessageBox, QHeaderView, QTreeWidget, 
    QTreeWidgetItem, QPushButton, QHBoxLayout, QDialog, QLabel,
    QLineEdit, QDialogButtonBox, QFormLayout
)
from PySide6.QtCore import Qt, Signal, QFileSystemWatcher
from PySide6.QtGui import QIcon


class FileBrowser(QWidget):
    """File browser with posts and pages tabs"""
    
    file_selected = Signal(str)
    
    def __init__(self):
        super().__init__()
        self.root_path = None
        self.file_watcher = QFileSystemWatcher()
        self.file_watcher.directoryChanged.connect(self.refresh_all)
        
        self.init_ui()
        
    def init_ui(self):
        """Initialize the user interface"""
        layout = QVBoxLayout(self)
        
        # Create tab widget
        self.tab_widget = QTabWidget()
        layout.addWidget(self.tab_widget)
        
        # Posts tab
        self.posts_widget = self.create_file_list("posts")
        self.tab_widget.addTab(self.posts_widget, "Posts")
        
        # Drafts tab
        self.drafts_widget = self.create_file_list("drafts")
        self.tab_widget.addTab(self.drafts_widget, "Drafts")
        
        # Pages tab
        self.pages_widget = self.create_file_list("pages")
        self.tab_widget.addTab(self.pages_widget, "Pages")
        
        # Refresh button
        refresh_btn = QPushButton("Refresh")
        refresh_btn.clicked.connect(self.refresh_all)
        layout.addWidget(refresh_btn)
        
    def create_file_list(self, content_type):
        """Create a file list widget for posts or pages"""
        widget = QWidget()
        layout = QVBoxLayout(widget)
        
        # Create tree widget for hierarchical display
        tree = QTreeWidget()
        tree.setHeaderLabel(f"{content_type.title()}")
        tree.itemDoubleClicked.connect(self.on_item_double_clicked)
        tree.setContextMenuPolicy(Qt.ContextMenuPolicy.CustomContextMenu)
        tree.customContextMenuRequested.connect(
            lambda pos: self.show_context_menu(pos, tree, content_type)
        )
        
        layout.addWidget(tree)
        
        # Store reference to tree widget
        setattr(self, f"{content_type}_tree", tree)
        
        return widget
        
    def set_root_path(self, path):
        """Set the root path for the Hugo site"""
        self.root_path = Path(path)
        
        # Stop watching old directories
        watched_dirs = self.file_watcher.directories()
        if watched_dirs:
            self.file_watcher.removePaths(watched_dirs)
            
        # Watch new directories
        content_path = self.root_path / "content"
        if content_path.exists():
            self.file_watcher.addPath(str(content_path))
            
        self.refresh_all()
        
    def refresh_all(self):
        """Refresh both posts and pages lists"""
        self.refresh_posts()
        self.refresh_drafts()
        self.refresh_pages()
        
    def refresh_posts(self):
        """Refresh the posts list"""
        self.refresh_content_type("posts")
        
    def refresh_drafts(self):
        """Refresh the drafts list"""
        self.refresh_content_type("drafts")
        
    def refresh_pages(self):
        """Refresh the pages list"""
        self.refresh_content_type("pages")
        
    def refresh_content_type(self, content_type):
        """Refresh content list for a specific type"""
        if not self.root_path:
            return
            
        tree = getattr(self, f"{content_type}_tree")
        tree.clear()
        
        content_path = self.root_path / "content"
        if not content_path.exists():
            return
            
        # Get all markdown files
        files = []
        
        if content_type == "posts":
            # Look for published posts (draft: false or no draft field)
            posts_path = content_path / "posts"
            if posts_path.exists():
                files.extend(self.get_published_posts(posts_path))
            else:
                # Look for dated content in root that are published
                files.extend(self.get_published_dated_content(content_path))
        elif content_type == "drafts":
            # Look for draft posts (draft: true)
            posts_path = content_path / "posts"
            if posts_path.exists():
                files.extend(self.get_draft_posts(posts_path))
            else:
                # Look for dated content in root that are drafts
                files.extend(self.get_draft_dated_content(content_path))
        else:
            # Pages are usually in root content or pages directory
            pages_path = content_path / "pages"
            if pages_path.exists():
                files.extend(self.get_markdown_files(pages_path))
            else:
                # Get non-dated content from root
                files.extend(self.get_non_dated_content(content_path))
                
        # Sort files by date in front matter (newest first)
        files.sort(key=lambda f: self.get_file_date(f), reverse=True)
        
        # Populate tree
        for file_path in files:
            self.add_file_to_tree(tree, file_path)
            
    def get_markdown_files(self, directory):
        """Get all markdown files from a directory recursively"""
        files = []
        for file_path in directory.rglob("*.md"):
            if file_path.is_file():
                files.append(file_path)
        return files
        
    def get_published_posts(self, directory):
        """Get published posts from a directory"""
        files = []
        for file_path in directory.rglob("*.md"):
            if file_path.is_file() and not self.is_draft(file_path):
                files.append(file_path)
        return files
        
    def get_draft_posts(self, directory):
        """Get draft posts from a directory"""
        files = []
        for file_path in directory.rglob("*.md"):
            if file_path.is_file() and self.is_draft(file_path):
                files.append(file_path)
        return files
        
    def get_published_dated_content(self, directory):
        """Get published dated content from directory"""
        files = []
        for file_path in directory.glob("*.md"):
            if file_path.is_file() and self.looks_like_post(file_path) and not self.is_draft(file_path):
                files.append(file_path)
        return files
        
    def get_draft_dated_content(self, directory):
        """Get draft dated content from directory"""
        files = []
        for file_path in directory.glob("*.md"):
            if file_path.is_file() and self.looks_like_post(file_path) and self.is_draft(file_path):
                files.append(file_path)
        return files
        
    def get_dated_content(self, directory):
        """Get content that looks like blog posts (dated)"""
        files = []
        for file_path in directory.glob("*.md"):
            if file_path.is_file() and self.looks_like_post(file_path):
                files.append(file_path)
        return files
        
    def get_non_dated_content(self, directory):
        """Get content that looks like pages (non-dated)"""
        files = []
        for file_path in directory.glob("*.md"):
            if file_path.is_file() and not self.looks_like_post(file_path):
                files.append(file_path)
        return files
        
    def looks_like_post(self, file_path):
        """Check if a file looks like a blog post"""
        filename = file_path.name
        # Check for date pattern in filename
        date_pattern = r'\d{4}-\d{2}-\d{2}'
        if re.search(date_pattern, filename):
            return True
            
        # Check front matter for date
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read(1000)  # Read first 1000 chars
                if 'date:' in content.lower() and '---' in content:
                    return True
        except:
            pass
            
        return False
        
    def is_draft(self, file_path):
        """Check if a file is marked as draft in front matter"""
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read(2000)  # Read first 2000 chars to get front matter
                
                # Check for YAML front matter
                if content.startswith('---'):
                    parts = content.split('---', 2)
                    if len(parts) >= 2:
                        front_matter = parts[1].strip()
                        # Look for draft: true
                        for line in front_matter.split('\n'):
                            line = line.strip().lower()
                            if line.startswith('draft:'):
                                value = line.split(':', 1)[1].strip()
                                return value.lower() in ['true', 'yes', '1']
        except:
            pass
            
        return False
        
    def get_file_date(self, file_path):
        """Extract date from file's front matter, fallback to modification time"""
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
                
            # Parse front matter
            if content.startswith('---'):
                parts = content.split('---', 2)
                if len(parts) >= 2:
                    front_matter = parts[1]
                    for line in front_matter.split('\n'):
                        line = line.strip()
                        if line.startswith('date:'):
                            date_str = line.split(':', 1)[1].strip().strip('"\'')
                            try:
                                # Try to parse ISO format
                                if 'T' in date_str:
                                    return datetime.fromisoformat(date_str.replace('Z', '+00:00')).timestamp()
                                else:
                                    return datetime.fromisoformat(date_str).timestamp()
                            except:
                                # Try other common formats
                                for fmt in ['%Y-%m-%d', '%Y-%m-%d %H:%M:%S', '%Y/%m/%d']:
                                    try:
                                        return datetime.strptime(date_str, fmt).timestamp()
                                    except:
                                        continue
        except:
            pass
            
        # Fallback to modification time
        return file_path.stat().st_mtime
        
    def add_file_to_tree(self, tree, file_path):
        """Add a file to the tree widget"""
        if self.root_path:
            try:
                rel_path = file_path.relative_to(self.root_path / "content")
            except ValueError:
                # File might not be under content directory
                rel_path = file_path.relative_to(self.root_path)
        else:
            rel_path = file_path
        
        # Create item
        item = QTreeWidgetItem()
        item.setText(0, file_path.name)
        item.setData(0, Qt.ItemDataRole.UserRole, str(file_path))
        
        # Add metadata as tooltip
        try:
            stat = file_path.stat()
            modified = datetime.fromtimestamp(stat.st_mtime)
            draft_status = " (Draft)" if self.is_draft(file_path) else ""
            item.setToolTip(0, f"Modified: {modified.strftime('%Y-%m-%d %H:%M')}{draft_status}")
        except:
            pass
            
        tree.addTopLevelItem(item)
        
    def on_item_double_clicked(self, item, column):
        """Handle item double click"""
        file_path = item.data(0, Qt.ItemDataRole.UserRole)
        if file_path:
            self.file_selected.emit(file_path)
            
    def show_context_menu(self, position, tree, content_type):
        """Show context menu for file operations"""
        item = tree.itemAt(position)
        
        menu = QMenu()
        
        # New file action - customize based on content type
        if content_type == "posts":
            new_action = menu.addAction("New Draft")
        elif content_type == "drafts":
            new_action = menu.addAction("New Draft")
        else:
            new_action = menu.addAction("New Page")
            
        new_action.triggered.connect(
            lambda: self.create_new_content(content_type)
        )
        
        if item:
            menu.addSeparator()
            
            # Edit action
            edit_action = menu.addAction("Edit")
            edit_action.triggered.connect(
                lambda: self.file_selected.emit(
                    item.data(0, Qt.ItemDataRole.UserRole)
                )
            )
            
            # Copy link action (for posts and pages)
            if content_type in ["posts", "pages"]:
                copy_link_action = menu.addAction("Copy Link")
                copy_link_action.triggered.connect(
                    lambda: self.copy_content_link(item)
                )
            
            # Add to menu action (only for pages)
            if content_type == "pages":
                add_to_menu_action = menu.addAction("Add to Menu")
                add_to_menu_action.triggered.connect(
                    lambda: self.add_page_to_menu(item)
                )
            
            # Delete action
            delete_action = menu.addAction("Delete")
            delete_action.triggered.connect(
                lambda: self.delete_file(item)
            )
            
        menu.exec(tree.mapToGlobal(position))
        
    def create_new_content(self, content_type):
        """Create new content file"""
        if content_type == "posts":
            self.create_new_draft()  # Posts tab now creates drafts
        elif content_type == "drafts":
            self.create_new_draft()
        else:
            self.create_new_page()
            
    def create_new_post(self):
        """Create a new blog post (published)"""
        if not self.root_path:
            return
            
        title, ok = QInputDialog.getText(self, "New Post", "Enter post title:")
        if not ok or not title:
            return
            
        # Create filename (no date prefix)
        slug = re.sub(r'[^\w\s-]', '', title.lower())
        slug = re.sub(r'[-\s]+', '-', slug)
        filename = f"{slug}.md"
        
        # Determine directory
        content_path = self.root_path / "content"
        posts_path = content_path / "posts"
        
        if posts_path.exists():
            file_path = posts_path / filename
        else:
            file_path = content_path / filename
            
        # Handle duplicate filenames
        counter = 1
        original_stem = file_path.stem
        while file_path.exists():
            new_filename = f"{original_stem}-{counter}.md"
            file_path = file_path.parent / new_filename
            counter += 1
            
        # Create directory if needed
        file_path.parent.mkdir(parents=True, exist_ok=True)
        
        # Create file with front matter (published)
        front_matter = f"""---
title: "{title}"
date: {datetime.now().isoformat()}
draft: false
---

# {title}

Your post content here...
"""
        
        try:
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(front_matter)
                
            self.refresh_posts()
            self.file_selected.emit(str(file_path))
            
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Failed to create post: {str(e)}")
            
    def create_new_draft(self):
        """Create a new draft post"""
        if not self.root_path:
            return
            
        title, ok = QInputDialog.getText(self, "New Draft", "Enter draft title:")
        if not ok or not title:
            return
            
        # Create filename (no date prefix)
        slug = re.sub(r'[^\w\s-]', '', title.lower())
        slug = re.sub(r'[-\s]+', '-', slug)
        filename = f"{slug}.md"
        
        # Determine directory
        content_path = self.root_path / "content"
        posts_path = content_path / "posts"
        
        if posts_path.exists():
            file_path = posts_path / filename
        else:
            file_path = content_path / filename
            
        # Handle duplicate filenames
        counter = 1
        original_stem = file_path.stem
        while file_path.exists():
            new_filename = f"{original_stem}-{counter}.md"
            file_path = file_path.parent / new_filename
            counter += 1
            
        # Create directory if needed
        file_path.parent.mkdir(parents=True, exist_ok=True)
        
        # Create file with front matter (draft)
        front_matter = f"""---
title: "{title}"
date: {datetime.now().isoformat()}
draft: true
---

# {title}

Your draft content here...
"""
        
        try:
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(front_matter)
                
            self.refresh_drafts()
            self.file_selected.emit(str(file_path))
            
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Failed to create draft: {str(e)}")
            
    def create_new_page(self):
        """Create a new page"""
        if not self.root_path:
            return
            
        title, ok = QInputDialog.getText(self, "New Page", "Enter page title:")
        if not ok or not title:
            return
            
        # Create filename
        slug = re.sub(r'[^\w\s-]', '', title.lower())
        slug = re.sub(r'[-\s]+', '-', slug)
        filename = f"{slug}.md"
        
        # Determine directory
        content_path = self.root_path / "content"
        pages_path = content_path / "pages"
        
        if pages_path.exists():
            file_path = pages_path / filename
        else:
            file_path = content_path / filename
            
        # Create directory if needed
        file_path.parent.mkdir(parents=True, exist_ok=True)
        
        # Create file with front matter
        front_matter = f"""---
title: "{title}"
---

# {title}

Your page content here...
"""
        
        try:
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(front_matter)
                
            self.refresh_pages()
            self.file_selected.emit(str(file_path))
            
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Failed to create page: {str(e)}")
            
    def delete_file(self, item):
        """Delete a file"""
        file_path = item.data(0, Qt.ItemDataRole.UserRole)
        if not file_path:
            return
            
        reply = QMessageBox.question(
            self, "Delete File",
            f"Are you sure you want to delete {Path(file_path).name}?",
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No,
            QMessageBox.StandardButton.No
        )
        
        if reply == QMessageBox.StandardButton.Yes:
            try:
                os.remove(file_path)
                self.refresh_all()
            except Exception as e:
                QMessageBox.critical(self, "Error", f"Failed to delete file: {str(e)}")
                
    def get_next_menu_weight(self):
        """Get the next available menu weight (current max + 1)"""
        if not self.root_path:
            return 10
            
        config_files = ['config.toml', 'config.yaml', 'config.yml', 'hugo.toml', 'hugo.yaml', 'hugo.yml']
        max_weight = 0
        
        for config_file in config_files:
            config_path = self.root_path / config_file
            if config_path.exists():
                try:
                    if config_file.endswith('.toml'):
                        with open(config_path, 'r', encoding='utf-8') as f:
                            config = toml.load(f)
                    elif config_file.endswith(('.yaml', '.yml')):
                        with open(config_path, 'r', encoding='utf-8') as f:
                            config = yaml.safe_load(f) or {}
                    else:
                        continue
                        
                    # Find existing menu weights
                    if 'menu' in config and 'main' in config['menu']:
                        for menu_item in config['menu']['main']:
                            if isinstance(menu_item, dict) and 'weight' in menu_item:
                                weight = menu_item['weight']
                                if isinstance(weight, int) and weight > max_weight:
                                    max_weight = weight
                    
                    break  # Found config file, stop searching
                except Exception as e:
                    print(f"Error reading {config_file}: {e}")
                    continue
        
        return max_weight + 1 if max_weight > 0 else 10
        
    def copy_content_link(self, item):
        """Copy the Hugo URL for a post or page to clipboard"""
        file_path = item.data(0, Qt.ItemDataRole.UserRole)
        if not file_path:
            return
            
        try:
            # Convert file path to Hugo URL
            hugo_url = self.get_hugo_url(file_path)
            
            # Copy to clipboard
            from PySide6.QtWidgets import QApplication
            clipboard = QApplication.clipboard()
            clipboard.setText(hugo_url)
            
            # Show feedback
            from PySide6.QtWidgets import QMessageBox
            file_name = Path(file_path).name
            QMessageBox.information(
                self, "Link Copied", 
                f"Hugo URL copied to clipboard:\n{hugo_url}"
            )
            
        except Exception as e:
            from PySide6.QtWidgets import QMessageBox
            QMessageBox.warning(
                self, "Error", 
                f"Failed to copy link: {str(e)}"
            )
    
    def get_hugo_url(self, file_path):
        """Generate Hugo URL from file path"""
        if not self.root_path:
            raise Exception("No blog root path set")
            
        file_path = Path(file_path)
        
        # Get relative path from content directory
        content_path = self.root_path / "content"
        try:
            rel_path = file_path.relative_to(content_path)
        except ValueError:
            # File might not be under content directory
            rel_path = file_path.relative_to(self.root_path)
        
        # Convert path to Hugo URL
        url_parts = list(rel_path.parts)
        
        # Remove file extension
        if url_parts:
            filename = url_parts[-1]
            if filename.endswith('.md'):
                url_parts[-1] = filename[:-3]  # Remove .md extension
        
        # Handle special Hugo directory structures
        if url_parts and url_parts[0] == 'pages':
            # For pages in 'pages' directory, remove 'pages' prefix
            # e.g., pages/about.md -> /about/
            url_parts = url_parts[1:]
        # For posts, keep the full path including 'posts'
        # e.g., posts/my-post.md -> /posts/my-post/
        
        # Build URL
        if url_parts:
            hugo_url = '/' + '/'.join(url_parts) + '/'
        else:
            hugo_url = '/'
            
        return hugo_url
        
    def add_page_to_menu(self, item):
        """Add a page to the Hugo site menu"""
        if not self.root_path:
            return
            
        file_path = item.data(0, Qt.ItemDataRole.UserRole)
        if not file_path:
            return
            
        page_path = Path(file_path)
        page_name = page_path.stem
        
        # Calculate next available weight
        suggested_weight = self.get_next_menu_weight()
        
        # Get menu details from user
        dialog = AddToMenuDialog(page_name, suggested_weight, self)
        if dialog.exec() == QDialog.DialogCode.Accepted:
            menu_name = dialog.menu_name
            menu_weight = dialog.menu_weight
            page_url = f"/{page_name}/"
            
            # Find and update config file
            config_updated = self.update_hugo_config(menu_name, page_url, menu_weight)
            
            if config_updated:
                QMessageBox.information(
                    self, "Success", 
                    f"Page '{page_name}' added to menu as '{menu_name}'"
                )
            else:
                QMessageBox.warning(
                    self, "Warning", 
                    "Could not automatically update config. Please add menu entry manually."
                )
                
    def update_hugo_config(self, menu_name, page_url, weight):
        """Update Hugo configuration to add menu item"""
        if not self.root_path:
            return False
            
        config_files = ['config.toml', 'config.yaml', 'config.yml', 'hugo.toml', 'hugo.yaml', 'hugo.yml']
        
        for config_file in config_files:
            config_path = self.root_path / config_file
            if config_path.exists():
                try:
                    if config_file.endswith('.toml'):
                        return self.update_toml_config(config_path, menu_name, page_url, weight)
                    elif config_file.endswith(('.yaml', '.yml')):
                        return self.update_yaml_config(config_path, menu_name, page_url, weight)
                except Exception as e:
                    print(f"Error updating {config_file}: {e}")
                    continue
        return False
        
    def update_toml_config(self, config_path, menu_name, page_url, weight):
        """Update TOML config file"""
        try:
            with open(config_path, 'r', encoding='utf-8') as f:
                config = toml.load(f)
            
            # Ensure menu structure exists
            if 'menu' not in config:
                config['menu'] = {}
            if 'main' not in config['menu']:
                config['menu']['main'] = []
            
            # Add new menu item
            new_item = {
                'name': menu_name,
                'url': page_url,
                'weight': weight
            }
            config['menu']['main'].append(new_item)
            
            # Write back to file
            with open(config_path, 'w', encoding='utf-8') as f:
                toml.dump(config, f)
            
            return True
        except Exception as e:
            print(f"Error updating TOML config: {e}")
            return False
            
    def update_yaml_config(self, config_path, menu_name, page_url, weight):
        """Update YAML config file"""
        try:
            with open(config_path, 'r', encoding='utf-8') as f:
                config = yaml.safe_load(f) or {}
            
            # Ensure menu structure exists
            if 'menu' not in config:
                config['menu'] = {}
            if 'main' not in config['menu']:
                config['menu']['main'] = []
            
            # Add new menu item
            new_item = {
                'name': menu_name,
                'url': page_url,
                'weight': weight
            }
            config['menu']['main'].append(new_item)
            
            # Write back to file
            with open(config_path, 'w', encoding='utf-8') as f:
                yaml.dump(config, f, default_flow_style=False)
            
            return True
        except Exception as e:
            print(f"Error updating YAML config: {e}")
            return False


class AddToMenuDialog(QDialog):
    """Dialog for adding a page to the menu"""
    
    def __init__(self, page_name, suggested_weight=10, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Add Page to Menu")
        self.setModal(True)
        self.resize(400, 200)
        
        layout = QVBoxLayout(self)
        
        # Form layout
        form_layout = QFormLayout()
        
        # Menu name field
        self.menu_name_edit = QLineEdit(page_name.title())
        form_layout.addRow("Menu Name:", self.menu_name_edit)
        
        # Menu weight field
        self.menu_weight_edit = QLineEdit(str(suggested_weight))
        self.menu_weight_edit.setToolTip("Lower numbers appear first in menu")
        form_layout.addRow("Menu Weight:", self.menu_weight_edit)
        
        layout.addLayout(form_layout)
        
        # Info label
        info_label = QLabel("This will add the page to the main navigation menu in your Hugo configuration.")
        info_label.setWordWrap(True)
        layout.addWidget(info_label)
        
        # Buttons
        button_box = QDialogButtonBox(
            QDialogButtonBox.StandardButton.Ok | QDialogButtonBox.StandardButton.Cancel
        )
        button_box.accepted.connect(self.accept)
        button_box.rejected.connect(self.reject)
        layout.addWidget(button_box)
        
    @property
    def menu_name(self):
        return self.menu_name_edit.text().strip()
        
    @property
    def menu_weight(self):
        try:
            return int(self.menu_weight_edit.text())
        except ValueError:
            return 10
