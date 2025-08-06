# Kugo - Hugo Front-end for KDE/Plasma

<div align="center">

![Kugo Icon](kugo/resources/kugo.jpeg)

**A modern, user-friendly desktop application for managing Hugo static sites**

[![Python](https://img.shields.io/badge/Python-3.8+-blue.svg)](https://www.python.org)
[![PySide6](https://img.shields.io/badge/PySide6-6.7+-green.svg)](https://doc.qt.io/qtforpython/)
[![Hugo](https://img.shields.io/badge/Hugo-Compatible-orange.svg)](https://gohugo.io)
[![Linux](https://img.shields.io/badge/Linux-KDE%2FPlasma-lightblue.svg)](https://kde.org)

</div>

## ✨ Features

### 🎯 **Content Management**
- **Draft-First Workflow**: All content starts as drafts, publish when ready
- **Smart Organization**: Chronological listing, separate drafts and posts
- **Cross-Reference Links**: Right-click to copy Hugo URLs for easy linking
- **Rich Editing**: Markdown editor with live preview and syntax highlighting

### 🔧 **Hugo Integration** 
- **Multi-Site Support**: Manage multiple Hugo blogs from one interface
- **Build & Serve**: Integrated Hugo commands with server management
- **Configuration Editing**: Direct access to Hugo config files
- **Draft Control**: Toggle draft inclusion for preview testing

### 🎨 **User Experience**
- **Dual-Panel Interface**: File browser + editor with live preview
- **KDE/Plasma Native**: Designed for Linux desktop environments
- **Professional Preview**: Modern styling with responsive design
- **Efficient Workflow**: Keyboard shortcuts and context menus

## 🚀 Quick Start

### Installation

```bash
# Clone the repository
git clone https://github.com/yourusername/Kugo.git
cd Kugo

# Run the automatic installer
./install.sh

# Launch Kugo
./run_kugo.sh
```

### First Setup

1. **Add Your Hugo Site**
   - Click "Add Blog" or use Hugo → Manage Blogs
   - Enter a name and select your Hugo site directory
   - Set publish command if needed

2. **Start Creating**
   - Use "New Draft" to create content
   - Edit in the markdown editor with live preview
   - Publish by changing `draft: true` to `draft: false`

## 📋 Requirements

- **Python**: 3.8 or higher
- **Hugo**: Latest version recommended
- **Operating System**: Linux (optimized for KDE/Plasma)
- **Dependencies**: Automatically installed via requirements.txt

## 📚 Documentation

- **[User Guide](USER_GUIDE.md)**: Complete usage instructions
- **[Changelog](CHANGELOG.md)**: Version history and updates
- **[Contributing](#contributing)**: How to contribute to the project

## 🗂️ Project Structure

```
Kugo/
├── kugo/                    # Main application package
│   ├── main_window.py      # Main application interface
│   ├── markdown_editor.py  # Editor with live preview
│   ├── file_browser.py     # Content browser and management
│   ├── hugo_manager.py     # Hugo command integration
│   ├── blog_manager.py     # Multi-blog management
│   └── resources/          # Application resources
├── templates/              # Content templates
├── install.sh             # Installation script
├── run_kugo.sh            # Launch script
└── main.py                # Application entry point
```

## 🎮 Usage Highlights

### Creating Content
```bash
Ctrl+D    # New Draft
Ctrl+G    # New Page
Ctrl+S    # Save
```

### Hugo Commands
```bash
F5        # Build Site
F6        # Serve Site  
F7        # Stop Server
```

### Navigation
```bash
Ctrl+1    # Switch to Editor
Ctrl+2    # Switch to Preview
```

## 🤝 Contributing

We welcome contributions! Here's how to get started:

1. **Fork** the repository
2. **Create** a feature branch (`git checkout -b feature/amazing-feature`)
3. **Commit** your changes (`git commit -m 'Add amazing feature'`)
4. **Push** to the branch (`git push origin feature/amazing-feature`)
5. **Open** a Pull Request

### Development Setup

```bash
# Clone your fork
git clone https://github.com/yourusername/Kugo.git
cd Kugo

# Create virtual environment
python -m venv .venv
source .venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Run in development mode
python main.py
```

## 📄 License

This project is open source - see the [LICENSE](LICENSE) file for details.

## 🐛 Support

- **Issues**: Report bugs and request features on [GitHub Issues](https://github.com/yourusername/Kugo/issues)
- **Documentation**: Check the [User Guide](USER_GUIDE.md) for detailed help
- **Community**: Join discussions in the project repository

## 🏆 Acknowledgments

- Built with [PySide6](https://doc.qt.io/qtforpython/) for the GUI framework
- Powered by [Hugo](https://gohugo.io) for static site generation
- Designed for the [KDE/Plasma](https://kde.org) desktop environment

---

<div align="center">
<strong>Made with ❤️ for the Hugo and KDE communities</strong>
</div>
