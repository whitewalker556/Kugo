#!/usr/bin/env python3
"""
Test the markdown editor preview functionality
"""

import sys
from pathlib import Path

# Add the kugo directory to Python path
sys.path.insert(0, str(Path(__file__).parent))

from PySide6.QtWidgets import QApplication
from kugo.markdown_editor import MarkdownEditor

def test_preview():
    """Test the markdown preview"""
    app = QApplication.instance()
    if app is None:
        app = QApplication([])
    
    # Create markdown editor
    editor = MarkdownEditor()
    editor.resize(800, 600)
    editor.show()
    
    # Set some test content
    test_content = """# Test Document

This is a **test** of the markdown preview functionality.

## Features to Test

- **Bold text**
- *Italic text*
- `Inline code`
- Links: [Example](https://example.com)

### Code Block

```python
def hello_world():
    print("Hello, World!")
    return True
```

### Table

| Feature | Status |
|---------|--------|
| Headers | ✓      |
| Tables  | ✓      |
| Code    | ✓      |

> This is a blockquote to test styling.

---

The preview should render this properly with professional styling.
"""
    
    editor.set_text(test_content)
    
    print("✓ Markdown editor test window opened")
    print("- Check if the preview pane shows rendered HTML")
    print("- Verify that styling looks professional")
    print("- Test toggling the preview on/off")
    
    return app.exec()

if __name__ == "__main__":
    sys.exit(test_preview())
