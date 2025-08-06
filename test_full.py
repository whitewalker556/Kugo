#!/usr/bin/env python3
"""
Comprehensive test of Kugo functionality
"""

import sys
import tempfile
import shutil
from pathlib import Path

# Add the kugo directory to Python path
sys.path.insert(0, str(Path(__file__).parent))

from PySide6.QtWidgets import QApplication, QMessageBox
from kugo.main_window import MainWindow

def setup_test_blog():
    """Set up a test Hugo blog"""
    test_blog_path = Path("/tmp/kugo-test-blog")
    
    # Remove existing test blog if it exists
    if test_blog_path.exists():
        shutil.rmtree(test_blog_path)
    
    # Copy the test blog we created
    if Path("/tmp/test-blog").exists():
        shutil.copytree("/tmp/test-blog", test_blog_path)
        print(f"✓ Test blog copied to {test_blog_path}")
        return str(test_blog_path)
    else:
        print("✗ No test blog found. Please create one first.")
        return None

def test_kugo_full():
    """Test the full Kugo application"""
    app = QApplication.instance()
    if app is None:
        app = QApplication([])
    
    # Create main window
    window = MainWindow()
    window.show()
    
    # Set up test blog
    test_blog_path = setup_test_blog()
    if test_blog_path:
        # Add the test blog
        window.blog_manager.add_blog(
            "Test Blog", 
            test_blog_path, 
            str(Path(test_blog_path) / "public"),
            "echo 'This is a test publish command'"
        )
        
        # Refresh blog list and select the test blog
        window.refresh_blog_list()
        window.blog_combo.setCurrentText("Test Blog")
        
        print("✓ Test blog added and selected")
        print(f"✓ Blog path: {test_blog_path}")
        print("✓ Kugo application is ready for testing")
        print()
        print("Test the following features:")
        print("1. Click 'New Draft' to create a draft post")
        print("2. Check that drafts appear in the Drafts tab")
        print("3. Click 'New Post' to create a published post")
        print("4. Check that posts appear in the Posts tab")
        print("5. Test the markdown preview functionality")
        print("6. Click 'Hugo Build' to test building")
        print("7. Click 'Hugo Serve' to test serving (should open browser)")
        
    else:
        print("✗ Could not set up test blog")
    
    return app.exec()

if __name__ == "__main__":
    sys.exit(test_kugo_full())
