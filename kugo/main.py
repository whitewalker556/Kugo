#!/usr/bin/env python3
"""
Main entry point for Kugo application
"""

import sys
import os
from PySide6.QtWidgets import QApplication
from PySide6.QtCore import Qt
from kugo.main_window import MainWindow
from kugo.resources import get_app_icon


def main():
    """Main application entry point"""
    # Enable high DPI support
    QApplication.setAttribute(Qt.AA_EnableHighDpiScaling, True)
    QApplication.setAttribute(Qt.AA_UseHighDpiPixmaps, True)
    
    app = QApplication(sys.argv)
    app.setApplicationName("Kugo")
    app.setApplicationDisplayName("Kugo")
    app.setApplicationVersion("1.0.0")
    app.setOrganizationName("Kugo")
    app.setDesktopFileName("kugo")
    
    # Set application icon
    app.setWindowIcon(get_app_icon())
    
    window = MainWindow()
    window.show()
    
    return app.exec()


if __name__ == "__main__":
    sys.exit(main())
