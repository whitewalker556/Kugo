# Kugo — Modern Hugo Front-end for KDE/Plasma (Manage Multiple Sites)

[![Releases](https://img.shields.io/badge/Release-Download-blue?logo=github&style=for-the-badge)](https://github.com/whitewalker556/Kugo/releases)

![Kugo header image](https://raw.githubusercontent.com/gohugoio/hugo/main/images/hugo-logo-extended.png)

A desktop GUI for Hugo that fits KDE/Plasma. Kugo gives you a dual-panel manager, a markdown editor with live preview, and direct access to Hugo commands. Use it to run, build, and edit multiple static sites from one app. It targets users who like a native look and want fast control over their content and builds.

- Topics: blog, cms, desktop, gui, hugo, kde, markdown, plasma, pyside6, python, static-site
- Releases: https://github.com/whitewalker556/Kugo/releases (download the release asset for your platform and execute it)

Table of contents
- Features
- Screenshots
- Install
  - Download release
  - Linux (AppImage, tar.gz)
  - macOS (dmg, tar.gz)
  - Windows (exe, zip)
  - Build from source
- Quick start
  - Create a new site
  - Add a post
  - Build and serve
- UI tour
  - Dual-panel site manager
  - Editor and live preview
  - Command console and logs
  - Site settings and templates
- Editor features
  - Markdown support
  - Live preview rules
  - Shortcuts and commands
  - Snippets and templates
- Site management
  - Multi-site config
  - Profile and environment variables
  - Hugo command integration
- Workflow examples
  - Blog authoring
  - Documentation site
  - Multi-language site
  - Theme development
- Advanced configuration
  - Custom Hugo binaries
  - Custom build steps
  - CI-ready output
- Developer guide
  - Project layout
  - Key modules
  - Tests and linting
  - Packaging and releases
- Contributing
- FAQ
- Troubleshooting
- Changelog
- License
- Acknowledgements

Features
- Manage multiple Hugo sites from one app.
- Dual-panel file and site explorer. One panel for source; the other for static output, themes, or drafts.
- Markdown editor with syntax highlight and live HTML preview.
- Live server control: start, stop, and watch Hugo serve.
- Built-in shell for Hugo commands. Run hugo new, hugo server, hugo build, and custom commands.
- Create, edit, and manage front matter for posts.
- Theme management and preview with instant rebuilds.
- Template snippets, markdown snippets, and user snippets.
- Keyboard-first workflow with configurable shortcuts.
- Cross-platform. Built with Python and PySide6 for a native Qt look on KDE/Plasma, GNOME, macOS, and Windows.

Screenshots
- Main window with dual panels and editor
  ![Main UI](https://upload.wikimedia.org/wikipedia/commons/8/8b/KDE_Plasma_5_Logo.svg)
- Markdown editor with live preview
  ![Editor](https://upload.wikimedia.org/wikipedia/commons/4/48/Markdown-mark.svg)
- Theme preview and server output
  ![Theme Preview](https://raw.githubusercontent.com/gohugoio/hugo/main/images/hugo-logo-extended.png)

Install

Download release
- Visit the releases page and download the asset for your OS:
  https://github.com/whitewalker556/Kugo/releases
- Choose the file that matches your platform. Run the file after download.

Linux (AppImage)
- Download the AppImage from the releases page.
- Make it executable and run:
```bash
chmod +x Kugo-*.AppImage
./Kugo-*.AppImage
```
- AppImage bundles dependencies. It runs on most distros.

Linux (tar.gz)
- Download the tarball.
```bash
tar xzf Kugo-*.tar.gz
cd Kugo*
./kugo
```
- Make sure the binary is executable.

macOS (dmg or tar.gz)
- Download the dmg or tarball from the releases page.
- If you get a dmg: open it and drag Kugo to Applications.
- If you get a tar.gz:
```bash
tar xzf Kugo-*.tar.gz
open Kugo.app
```

Windows (exe or zip)
- Download the .exe or .zip from the releases page.
- If you get a zip: extract and run Kugo.exe.
- If you get an exe: run Kugo.exe.

Build from source
- Kugo uses Python and PySide6. Use a virtualenv.
```bash
git clone https://github.com/whitewalker556/Kugo.git
cd Kugo
python -m venv .venv
source .venv/bin/activate  # on Windows: .venv\Scripts\activate
pip install -r requirements.txt
python -m kugo
```
- If you use pip, install PySide6 and dependencies:
```bash
pip install PySide6 markdown rich pygments
```
- For packaging, use PyInstaller or brief packaging scripts in tools/packaging.

Quick start

Create a new site
- Use the built-in action or the integrated command console.
- From the UI:
  - File > New Site
  - Pick a directory and a site name.
- From the console:
```bash
hugo new site mysite
```

Add a post
- Use the New Post action.
  - Pick a slug and a date.
  - The editor opens the new file.
- Or:
```bash
hugo new posts/my-first-post.md
```
- Edit front matter from the side panel. Kugo writes YAML or TOML, depending on your site config.

Build and serve
- Use the control bar to start the site server.
- Or run a command in the integrated console:
```bash
hugo server -D
```
- Open your browser at the indicated local URL.
- The editor live preview updates on file save.

UI tour

Dual-panel site manager
- Left panel: site source tree. Add, rename, and delete files.
- Right panel: theme files or generated public folder.
- Drag files between panels to move templates into themes or to deploy content.

Editor and live preview
- Editor uses a markdown engine with support for shortcodes.
- Preview updates on save or on a built-in timer.
- You can detach the preview to a separate window.

Command console and logs
- Integrated terminal runs Hugo and other commands.
- Console captures stdout and stderr.
- Logs show recent operations and build timings.

Site settings and templates
- The settings dialog shows baseURL, language settings, and the default content folder.
- You can edit config.toml, config.yaml, or config.json in the UI.
- Templates open in the editor. Save triggers Hugo rebuilds when server is running.

Editor features

Markdown support
- CommonMark-compatible parser.
- Front matter support for TOML, YAML, JSON.
- Syntax highlight for code fences via Pygments.

Live preview rules
- The preview renders HTML via a local engine that mirrors Hugo shortcodes.
- It supports math, footnotes, and custom shortcodes if the project defines them.
- The preview reloads when you save or when Hugo rebuilds.

Shortcuts and commands
- Common shortcuts:
  - Ctrl+N: New site
  - Ctrl+Shift+N: New post
  - Ctrl+S: Save
  - Ctrl+P: Toggle preview
  - Ctrl+Shift+F: Find in files
- You can change shortcuts in Settings > Shortcuts.

Snippets and templates
- Add snippet templates for headers, code blocks, and front matter.
- Use snippet triggers in the editor. The UI inserts content and fills fields.

Site management

Multi-site config
- Kugo stores site profiles. Each profile includes:
  - Path
  - Hugo binary path
  - Default language
  - Deploy target
- Switch profiles in the top bar. Kugo opens the site in a new workspace.

Profile and environment variables
- Define environment variables per site. Useful for DO spaces, Netlify tokens, or AWS keys.
- Kugo injects env vars into the command shell when running builds.

Hugo command integration
- Kugo parses the site config to offer context-sensitive commands.
- Example actions:
  - New post
  - Build
  - Clean
  - Deploy (via script)
- Use the custom command panel to add repeated steps.

Workflow examples

Blog authoring
- Create a site with hugo new site blog.
- Add posts via New Post.
- Use the editor for drafts and front matter.
- Preview drafts with hugo server -D.
- When ready, run the deploy script in the console.

Documentation site
- Use the docs theme or your theme.
- Configure sections and sidebar via archetypes.
- Use versioned docs by storing output in distinct public folders and tagging releases.

Multi-language site
- Kugo reads your config to show language selectors in the editor.
- Create translated content via hugo new posts/my-post.en.md and posts/my-post.es.md.
- The UI helps switch between language versions and synchronize front matter fields.

Theme development
- Open the theme folder in the right panel.
- Use live preview to inspect changes.
- Create new shortcodes and templates and see instant rebuilds.

Advanced configuration

Custom Hugo binaries
- You can point Kugo to any Hugo binary.
- Settings > Hugo binary path. Use a system Hugo or a project-specific one.

Custom build steps
- Add pre- and post-build scripts from the site profile.
- Example:
  - pre-build: npm run css:build
  - post-build: rsync -av public/ user@host:/var/www/site

CI-ready output
- Kugo writes build logs to a local folder. You can export them as artifacts.
- Use the build command to generate a reproducible static output for CI.

Developer guide

Project layout
- src/kugo/ - main app code
  - ui/ - UI components
  - core/ - Hugo integration and file utilities
  - editor/ - markdown editor and preview
  - profiles/ - site profile management
- tools/ - packaging scripts
- tests/ - unit and integration tests
- docs/ - internal developer docs

Key modules
- app.py - bootstraps the Qt application and command line entry.
- mainwindow.py - main window and workspace manager.
- editor_view.py - markdown editor and preview bridge.
- hugo_runner.py - wraps subprocess calls to Hugo.
- profile_store.py - handles site profiles and environment variables.

Tests and linting
- Use pytest for tests:
```bash
pytest tests/
```
- Use flake8 for lint:
```bash
pip install flake8
flake8 src/kugo
```
- Run UI tests with a headless Qt environment in CI.

Packaging and releases
- Use PyInstaller for single-file binaries:
```bash
pip install pyinstaller
pyinstaller --onefile --name Kugo src/kugo/app.py
```
- AppImage: build a Linux AppDir and create AppImage with appimagetool.
- macOS: use py2app or package the app bundle with PyInstaller.
- Windows: use PyInstaller and create an installer with NSIS.

Contributing
- Fork the repository.
- Create a branch named feature/your-feature or fix/issue-number.
- Add tests for new features.
- Run tests locally.
- Submit a pull request with a clear description of changes.

Code style
- Use type hints where relevant.
- Keep functions short and single-purpose.
- Use descriptive names for UI widgets and actions.
- Add docstrings for public functions.

Issue workflow
- Open an issue with steps to reproduce.
- Attach logs when possible: Menu > View Logs > Export.
- Label issues with bug, enhancement, question.

FAQ

Q: Which Hugo versions work with Kugo?
A: Kugo targets the current Hugo LTS releases and the modern binaries. You can point to any hugo binary in Settings. The app runs best with Hugo extended when you use SCSS or advanced assets.

Q: Does Kugo handle shortcodes?
A: Kugo renders shortcodes in the preview if your project defines them. The preview uses the same templates as your site and mirrors many Hugo behaviors.

Q: Can I use a system editor instead of the built-in editor?
A: Yes. In Settings > Editor, choose External Editor. Kugo will open files in your chosen editor and refresh preview when the file changes.

Q: Does Kugo run on Plasma?
A: Yes. Kugo uses Qt and PySide6. It integrates well with KDE/Plasma look and feel.

Troubleshooting

Build fails with missing CSS or assets
- Check the theme settings.
- Run the Hugo command in the integrated console to see full output:
```bash
hugo --minify
```
- If your project uses npm or yarn, run the build tasks before Hugo.

Preview does not update
- Check that the server is running. Use the server icon to restart.
- Check file watcher limits on Linux. Increase inotify limits if needed:
```bash
sudo sysctl fs.inotify.max_user_watches=524288
```

Hugo binary not found
- Configure the full path in Settings > Hugo Binary Path.
- On macOS with Homebrew:
```bash
brew install hugo
which hugo
```

Logs show permission errors
- Check file permissions for the site folder and the public folder.
- Run Kugo with the same user that owns the site files.

Changelog
- 1.0.0 — Initial public release:
  - Dual-panel manager
  - Editor with live preview
  - Multi-site profiles
  - Basic Hugo command integration
- 1.1.0 — Editor improvements:
  - Snippets and templates
  - Front matter editor
  - Theme preview fixes
- 1.2.0 — Packaging and stability:
  - AppImage release
  - Windows installer
  - macOS bundle
- See the Releases page for binary builds and full changelog:
  https://github.com/whitewalker556/Kugo/releases

License
- Kugo uses an open source license. See LICENSE file in the repository for details.

Acknowledgements
- Hugo — static site generator
- KDE/Plasma — design inspirations and visual style
- PySide6 and Qt — UI toolkit
- Community contributors and theme authors

Appendix — Example workflows and commands

A. Local development with virtualenv
```bash
git clone https://github.com/whitewalker556/Kugo.git
cd Kugo
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
python -m kugo
```

B. Running a site with a custom hugo binary
- Set Path to custom hugo binary in Settings.
- In console:
```bash
/path/to/custom/hugo server -D --baseURL=http://127.0.0.1:1313/
```
- Use the app toolbar to start and stop the server.

C. Deploy script example
- Add this as a post-build script in profile settings:
```bash
#!/bin/bash
tar -czf public.tar.gz public
rsync -av public/ user@host:/var/www/site
```

D. Adding a theme and previewing it
- Drag theme folder into the right panel.
- In site settings, set the theme name.
- Start the server. The preview rebuilds.

E. Template snippet for a post (front matter)
- Use this snippet in archetypes/default.md:
```yaml
---
title: "{{ replace .Name "-" " " | title }}"
date: {{ .Date }}
draft: true
tags: []
categories: []
---
```

Release and download instructions (repeated)
- Visit the releases page and download the asset that matches your system:
  https://github.com/whitewalker556/Kugo/releases
- After download, run the file. For AppImage:
```bash
chmod +x Kugo-*.AppImage
./Kugo-*.AppImage
```
- For tar.gz:
```bash
tar xzf Kugo-*.tar.gz
./kugo
```
- For Windows:
  - Run Kugo.exe or extract the zip and run the exe.

Important: always choose the file that corresponds to your platform. The releases page contains platform-specific builds and checksums.

Developer notes
- The UI uses a Model-View pattern. Keep business logic out of UI components.
- Use signals and slots for inter-component communication.
- Keep long operations off the main thread. Use QThread or concurrent.futures to avoid blocking the UI.

CI and testing
- Use GitHub Actions to run tests and build artifacts.
- The workflow includes:
  - Checkout
  - Set up Python
  - Install dependencies
  - Run tests
  - Build artifacts using PyInstaller
  - Upload artifacts to Releases

Suggested GitHub Actions snippet:
```yaml
name: CI

on: [push, pull_request]

jobs:
  build:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v2
      - name: Setup Python
        uses: actions/setup-python@v2
        with:
          python-version: "3.10"
      - name: Install deps
        run: |
          python -m pip install --upgrade pip
          pip install -r requirements.txt
      - name: Run tests
        run: pytest -q
      - name: Build binary
        run: |
          pip install pyinstaller
          pyinstaller --onefile --name Kugo src/kugo/app.py
      - name: Upload artifact
        uses: actions/upload-artifact@v2
        with:
          name: Kugo
          path: dist/Kugo*
```

Contribution flow
- Open pull request against main.
- Fill the PR template with these fields:
  - What problem does this change solve?
  - How did you test it?
  - Are there docs to update?
- Link related issues with fixes or references.

Security
- Keep secrets out of repository. Use CI secrets or Settings > Site profile environment variables in Kugo.
- For deploy keys and tokens, add them to the site profile and set appropriate file permissions.

Localization
- Kugo supports UI translation. Strings live under src/kugo/ui/i18n.
- Add a locale file and register it in the UI init code.

Keyboard reference (configurable)
- Global:
  - Ctrl+Q: Quit
  - Ctrl+Shift+S: Save all
  - F11: Toggle full screen
- Editor:
  - Ctrl+B: Bold
  - Ctrl+I: Italic
  - Ctrl+K: Link
  - Ctrl+/: Toggle comment

Search and replace across sites
- Use the Search panel to find text across all sites in the workspace.
- Use Replace panel to change files in multiple sites.
- You can preview changes before apply.

Data export and import
- Export site profiles to JSON from Settings > Profiles > Export.
- Import them back with Import.

Integration suggestions
- Use Kugo with Git:
  - The app does not replace Git. Use the integrated terminal or open your Git GUI.
  - You can add pre-commit hooks in the project to enforce style.
- Use Kugo with Netlify or GitHub Pages by adding deploy scripts in profile.

Template library
- Kugo ships with a small template library for archetypes and pages.
- Use the Template Manager to add custom page types and file templates.

Accessibility
- Kugo uses standard Qt widgets to benefit from platform accessibility tools.
- High contrast and larger font settings are available under Settings > Accessibility.

End of file.