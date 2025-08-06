# 📖 Kugo User Guide

Welcome to Kugo - your modern Hugo front-end for KDE/Plasma!

## 🚀 Quick Start

1. **Install**: Run `./install.sh`
2. **Launch**: Run `./run_kugo.sh` or use your applications menu
3. **Add Blog**: Click "Add Blog" and select your Hugo site directory
4. **Start Creating**: Use "New Draft" to create content

## � Interface Overview

### Left Panel
- **Blog Selector**: Switch between multiple Hugo sites
- **Posts**: Published content (`draft: false`)
- **Drafts**: Unpublished content (`draft: true`)
- **Pages**: Static pages (About, Contact, etc.)
- **Hugo Commands**: Build, Serve, Stop Server buttons

### Right Panel
- **Editor Tab**: Markdown editor with syntax highlighting
- **Preview Tab**: Live HTML preview with professional styling
- **Controls**: Save (`Ctrl+S`) and Delete buttons

## ✍️ Creating Content

### Draft-First Workflow
1. **New Draft** → Write content → **Publish** (change `draft: true` to `draft: false`)

### Methods to Create Content
- **New Draft**: Click button, `Ctrl+D`, or right-click → "New Draft"
- **New Page**: Click button, `Ctrl+G`, or right-click → "New Page"

### File Management
- **Edit**: Double-click any content to open
- **Delete**: Right-click → "Delete" or use Delete button
- **Copy Link**: Right-click → "Copy Link" for cross-referencing

### Automatic Features
- **Clean Filenames**: "My Post" → `my-post.md`
- **Duplicate Handling**: `my-post.md`, `my-post-1.md`, etc.
- **Front Matter**: Automatically generated with proper dates and settings

## 🛠️ Hugo Integration

### Commands
- **Build** (`F5`): Generate static files
- **Serve** (`F6`): Start development server + open browser
- **Stop** (`F7`): Stop development server
- **Edit Config**: Open Hugo configuration file

### Draft Control
- **Default**: Drafts excluded from preview (matches production)
- **Toggle**: Hugo → "Include Drafts in Preview" to show/hide drafts

## 🔧 Multi-Blog Management

### Adding Blogs
**Hugo** → **Manage Blogs** → **Add**
- **Name**: Display name
- **Root Path**: Hugo site directory
- **Public Path**: Build output (usually `public/`)
- **Publish Command**: Deployment command (optional)

### Blog Operations
- **Switch**: Use dropdown in left panel
- **Edit**: Select blog → modify settings → "Save Changes"
- **Remove**: Select blog → "Remove" (files stay untouched)

## ⌨️ Keyboard Shortcuts

| Action | Shortcut |
|--------|----------|
| New Draft | `Ctrl+D` |
| New Page | `Ctrl+G` |
| Save | `Ctrl+S` |
| Build Site | `F5` |
| Serve Site | `F6` |
| Stop Server | `F7` |
| Switch to Editor | `Ctrl+1` |
| Switch to Preview | `Ctrl+2` |

## 🚀 Publishing

### Deployment Commands
Set up in **Manage Blogs** → **Publish Command**:

```bash
# Git workflow
git add . && git commit -m "Update" && git push

# Server upload
rsync -av public/ user@server:/var/www/html/

# Netlify
netlify deploy --prod
```

Access via **Hugo** → **Publish Command** to copy and run.

## 🔗 Content Features

### Copy Link
Right-click any content → "Copy Link" generates Hugo URLs:
- Posts: `/posts/my-post/`
- Pages: `/about/`
- Use for internal linking: `[See this post](/posts/other-post/)`

### Add to Menu
Right-click pages → "Add to Menu" → Enter weight → Automatically added to Hugo navigation

### Front Matter Examples

**Draft:**
```yaml
---
title: "My Draft"
date: 2025-08-05T10:30:00Z
draft: true
---
```

**Published Post:**
```yaml
---
title: "My Post"
date: 2025-08-05T10:30:00Z
draft: false
---
```

## 🐛 Troubleshooting

| Problem | Solution |
|---------|----------|
| Hugo not found | `sudo apt install hugo` |
| Blog won't load | Check for `config.toml/yaml` in root path |
| Server won't start | Check port 1313 usage: `pkill hugo` |
| Preview not updating | Save file first (`Ctrl+S`) |

### Configuration
- **App Settings**: `~/.local/share/Kugo/blogs.json`
- **Templates**: `templates/` directory in Kugo folder

## 📞 Support

- **Issues**: https://github.com/timappledotcom/Kugo/issues
- **Documentation**: README.md and CHANGELOG.md
- **Community**: Fork, contribute, share feedback!

---

**Happy blogging with Kugo! 🎉**
