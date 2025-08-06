# 📝 Changelog

All notable changes to Kugo are documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [1.2.0] - 2025-08-05

### ✨ Added
- **Copy Link Feature**: Right-click posts/pages to copy Hugo URLs for cross-referencing
- **Application Icon**: Custom Kugo icon for better desktop integration
- **Blog Information Editing**: Complete blog settings management via Hugo → Manage Blogs

### 🔧 Fixed
- **URL Generation**: Fixed copy link URLs to properly include `/posts/` prefix for posts
- **Draft Visibility**: Removed default `--buildDrafts` flag from serve command
- **Desktop Integration**: Proper icon paths for KDE/Plasma desktop entries

### 📚 Improved
- **Documentation**: Consolidated and cleaned up all documentation files
- **User Experience**: Better context menus and workflow integration

## [1.1.0] - 2025-08-05

### ✨ Added
- **Drafts Management**: Separate drafts tab with dedicated workflow
- **Enhanced Preview**: Professional HTML rendering with modern CSS styling
- **Draft Control Toggle**: Optional draft inclusion in preview server
- **Smart File Naming**: Clean filenames without date prefixes
- **Server Management**: Dedicated stop server functionality
- **Menu Integration**: Add pages to Hugo navigation with automatic weight calculation

### 🔄 Changed
- **Draft-First Workflow**: All content starts as drafts, publish when ready
- **Content Organization**: Chronological sorting by front matter date (newest first)
- **UI Simplification**: Consolidated menus and removed redundant buttons
- **File Management**: Improved delete button placement and functionality

### 🛠️ Technical
- **Front Matter Parsing**: Enhanced date detection and draft status handling
- **URL Routing**: Proper Hugo URL generation for internal linking
- **State Management**: Better server start/stop state tracking
- **Duplicate Handling**: Automatic numbering for duplicate filenames

## [1.0.0] - 2025-08-05

### 🎉 Initial Release

#### ✨ Core Features
- **Multi-Blog Support**: Manage multiple Hugo sites from one application
- **Dual-Panel Interface**: File browser and markdown editor with live preview
- **Hugo Integration**: Build, serve, and configuration editing
- **Content Management**: Create, edit, and delete posts, drafts, and pages
- **KDE/Plasma Integration**: Native desktop application with proper theming

#### 🖥️ User Interface
- **Markdown Editor**: Syntax highlighting and live preview
- **File Browser**: Organized posts, drafts, and pages with context menus
- **Menu System**: Comprehensive menu bar with keyboard shortcuts
- **Status Management**: Clear feedback for all operations

#### 🔧 Technical Foundation
- **PySide6 Framework**: Modern Qt-based GUI
- **Hugo CLI Integration**: Direct command execution and process management
- **Configuration Management**: JSON-based blog settings storage
- **Template System**: Customizable content templates
- **Cross-Platform**: Designed for Linux with KDE/Plasma optimization

#### 📦 Distribution
- **Installation Scripts**: Automated setup and desktop integration
- **Virtual Environment**: Isolated Python dependencies
- **Documentation**: Comprehensive user guide and technical docs
- **Test Suite**: Application validation and reliability testing

---

### Legend
- ✨ **Added**: New features
- 🔧 **Fixed**: Bug fixes
- 🔄 **Changed**: Modified existing functionality
- 🛠️ **Technical**: Internal improvements
- 📚 **Documentation**: Documentation updates
- 🎉 **Major**: Significant milestones
- **Template System**: Customizable templates for new content
- **File Watching**: Automatic refresh when files change externally

### Technical
- Built with PySide6 for native Qt/KDE integration
- Markdown processing with Python-Markdown
- Syntax highlighting with Pygments
- File system monitoring with Watchdog
- Configuration management with QSettings
- YAML front matter support
- Cross-platform Python codebase (Linux focus)
