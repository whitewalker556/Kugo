<!-- Use this file to provide workspace-specific custom instructions to Copilot. For more details, visit https://code.visualstudio.com/docs/copilot/copilot-customization#_use-a-githubcopilotinstructionsmd-file -->

This is a PySide6 desktop application for managing Hugo static sites. The application is designed for KDE/Plasma desktop environment and includes:

- Hugo site management (multiple sites support)
- Markdown editor with live preview
- Posts and pages management
- Hugo command integration (build, serve, config editing)
- Publish command management

Key technologies:
- PySide6 for the GUI framework
- Markdown library for rendering
- Pygments for syntax highlighting
- TOML for configuration parsing
- Watchdog for file system monitoring

The application follows a modular structure with separate modules for the main window, markdown editor, file browser, and Hugo integration.
