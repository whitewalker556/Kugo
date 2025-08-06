"""
Configuration and settings management
"""

import os
import json
from pathlib import Path
from PySide6.QtCore import QSettings, QStandardPaths


class AppConfig:
    """Application configuration manager"""
    
    def __init__(self):
        self.settings = QSettings()
        self.app_data_dir = self.get_app_data_dir()
        
    def get_app_data_dir(self):
        """Get application data directory"""
        app_data_dir = QStandardPaths.writableLocation(
            QStandardPaths.StandardLocation.AppDataLocation
        )
        os.makedirs(app_data_dir, exist_ok=True)
        return Path(app_data_dir)
        
    def get_themes_dir(self):
        """Get themes directory"""
        themes_dir = self.app_data_dir / "themes"
        themes_dir.mkdir(exist_ok=True)
        return themes_dir
        
    def get_templates_dir(self):
        """Get templates directory"""
        templates_dir = self.app_data_dir / "templates"
        templates_dir.mkdir(exist_ok=True)
        return templates_dir
        
    def save_window_geometry(self, geometry):
        """Save window geometry"""
        self.settings.setValue("window/geometry", geometry)
        
    def load_window_geometry(self):
        """Load window geometry"""
        return self.settings.value("window/geometry")
        
    def save_splitter_state(self, state):
        """Save splitter state"""
        self.settings.setValue("ui/splitter_state", state)
        
    def load_splitter_state(self):
        """Load splitter state"""
        return self.settings.value("ui/splitter_state")
        
    def save_last_blog(self, blog_name):
        """Save last used blog"""
        self.settings.setValue("last_blog", blog_name)
        
    def load_last_blog(self):
        """Load last used blog"""
        return self.settings.value("last_blog", "")
        
    def save_editor_settings(self, font_family, font_size, theme):
        """Save editor settings"""
        self.settings.setValue("editor/font_family", font_family)
        self.settings.setValue("editor/font_size", font_size)
        self.settings.setValue("editor/theme", theme)
        
    def load_editor_settings(self):
        """Load editor settings"""
        font_size_value = self.settings.value("editor/font_size", 12)
        if isinstance(font_size_value, int):
            font_size = font_size_value
        elif isinstance(font_size_value, str):
            try:
                font_size = int(font_size_value)
            except ValueError:
                font_size = 12
        else:
            font_size = 12
            
        return {
            'font_family': self.settings.value("editor/font_family", "Courier") or "Courier",
            'font_size': font_size,
            'theme': self.settings.value("editor/theme", "default") or "default"
        }
