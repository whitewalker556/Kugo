#!/usr/bin/env python3
"""
Test script for Kugo application
"""

import sys
import os
from pathlib import Path

# Add the kugo directory to Python path
sys.path.insert(0, str(Path(__file__).parent))

def test_imports():
    """Test that all modules can be imported"""
    try:
        from kugo import main_window, markdown_editor, file_browser
        from kugo import hugo_manager, blog_manager, config, utils
        print("✓ All modules imported successfully")
        return True
    except ImportError as e:
        print(f"✗ Import error: {e}")
        return False

def test_dependencies():
    """Test that all dependencies are available"""
    try:
        import PySide6
        import markdown
        import pygments
        import watchdog
        import toml
        import yaml
        print("✓ All dependencies available")
        return True
    except ImportError as e:
        print(f"✗ Dependency error: {e}")
        return False

def test_application():
    """Test basic application functionality"""
    try:
        from PySide6.QtWidgets import QApplication
        from kugo.main_window import MainWindow
        
        # Create application instance
        app = QApplication.instance()
        if app is None:
            app = QApplication([])
        
        # Create main window
        window = MainWindow()
        print("✓ Application window created successfully")
        
        # Test blog manager
        blogs = window.blog_manager.get_all_blogs()
        print(f"✓ Blog manager working (found {len(blogs)} blogs)")
        
        return True
    except Exception as e:
        print(f"✗ Application error: {e}")
        return False

def main():
    """Run all tests"""
    print("Testing Kugo application...")
    print("-" * 40)
    
    tests = [
        ("Import test", test_imports),
        ("Dependencies test", test_dependencies),
        ("Application test", test_application),
    ]
    
    passed = 0
    total = len(tests)
    
    for test_name, test_func in tests:
        print(f"\n{test_name}:")
        if test_func():
            passed += 1
    
    print("\n" + "=" * 40)
    print(f"Tests passed: {passed}/{total}")
    
    if passed == total:
        print("🎉 All tests passed! Kugo is ready to use.")
        return 0
    else:
        print("❌ Some tests failed. Please check the errors above.")
        return 1

if __name__ == "__main__":
    sys.exit(main())
