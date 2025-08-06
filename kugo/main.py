#!/usr/bin/env python3
"""
Main entry point for Kugo application
"""

import sys
import os
from PySide6.QtWidgets import QApplication
from PySide6.QtCore import Qt
from kugo.main_window import MainWindow


def main():
    """Main application entry point"""
    # Enable high DPI support
    QApplication.setAttribute(Qt.AA_EnableHighDpiScaling, True)
    QApplication.setAttribute(Qt.AA_UseHighDpiPixmaps, True)
    
    app = QApplication(sys.argv)
    app.setApplicationName("Kugo")
    app.setApplicationVersion("1.0.0")
    app.setOrganizationName("Kugo")
    
    # Set application icon (if available)
    # app.setWindowIcon(QIcon(":/icons/kugo.png"))
    
    window = MainWindow()
    window.show()
    
    return app.exec()


if __name__ == "__main__":
    sys.exit(main())
