#!/usr/bin/env python3
"""
Test markdown rendering
"""

import sys
from pathlib import Path

# Add the kugo directory to Python path
sys.path.insert(0, str(Path(__file__).parent))

def test_markdown_rendering():
    """Test markdown rendering functionality"""
    try:
        import markdown
        
        # Test basic markdown
        md = markdown.Markdown(extensions=['codehilite', 'fenced_code', 'tables', 'toc'])
        
        test_markdown = """
# Test Header

This is a **bold** test with *italic* text.

## Code Block

```python
def hello():
    print("Hello, World!")
```

## Table

| Name | Age |
|------|-----|
| John | 25  |
| Jane | 30  |

## List

- Item 1
- Item 2
- Item 3
"""
        
        html = md.convert(test_markdown)
        print("✓ Markdown conversion successful")
        print(f"Generated HTML length: {len(html)} characters")
        
        # Test WebEngine availability
        try:
            from PySide6.QtWebEngineWidgets import QWebEngineView
            print("✓ QWebEngineView available")
        except ImportError as e:
            print(f"⚠ QWebEngineView not available: {e}")
            
        return True
        
    except Exception as e:
        print(f"✗ Markdown test failed: {e}")
        return False

if __name__ == "__main__":
    test_markdown_rendering()
