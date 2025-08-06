"""
Resources module for Kugo application
"""

from pathlib import Path
from PySide6.QtGui import QIcon

def get_icon(name: str) -> QIcon:
    """
    Get an icon from the resources directory
    
    Args:
        name: Icon filename (e.g., 'kugo.jpeg')
    
    Returns:
        QIcon object, or empty QIcon if file not found
    """
    icon_path = Path(__file__).parent / name
    if icon_path.exists():
        return QIcon(str(icon_path))
    return QIcon()

def get_app_icon() -> QIcon:
    """Get the main application icon"""
    return get_icon("kugo.jpeg")
