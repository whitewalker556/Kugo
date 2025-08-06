# 📖 Kugo User Guide

Welcome to Kugo - your modern Hugo front-end for KDE/Plasma! This guide will help you get started and master all features.

## 🚀 Getting Started

### First Launch

1. **Install Kugo** using `./install.sh`
2. **Launch** with `./run_kugo.sh` or from your applications menu
3. **Add your first blog** via the "Add Blog" button

### Adding a Hugo Site

**Option 1: Quick Add**
- Click the "Add Blog" button in the main interface
- Fill in the blog details and click OK

**Option 2: Menu Access**
- Go to `Hugo` → `Manage Blogs`
- Click "Add" to create a new blog entry

**Required Information:**
- **Blog Name**: Display name in Kugo (e.g., "My Personal Blog")
- **Root Path**: Your Hugo site directory (contains `config.toml/yaml`)
- **Public Path**: Build output directory (usually `public/`)
- **Publish Command**: Optional deployment command

## 🖥️ Interface Overview

### Left Panel: Content Browser

**📁 Blog Selector**
- Switch between multiple Hugo sites
- Shows currently active blog at the top

**📝 Content Tabs**
- **Posts**: Published blog posts (chronological order)
- **Drafts**: Unpublished content (`draft: true`)
- **Pages**: Static pages (About, Contact, etc.)

**⚡ Hugo Commands**
- **Build Site**: Generate static files
- **Serve Site**: Start development server
- **Stop Server**: Stop the development server

### Right Panel: Editor & Preview

**✏️ Editor Tab**
- Full markdown editor with syntax highlighting
- Auto-completion for markdown syntax
- Live word count and cursor position

**👁️ Preview Tab**
- Real-time HTML preview
- Professional styling that matches modern web standards
- Responsive design preview

**🔧 Editor Controls**
- **Save**: Save current file (Ctrl+S)
- **Delete**: Remove current file (with confirmation)

## ✍️ Creating Content

### The Draft-First Workflow

Kugo uses a draft-first approach for content creation:

1. **Create Draft**: All new content starts as a draft
2. **Edit & Preview**: Write and refine your content
3. **Publish**: Change `draft: true` to `draft: false` when ready

### Creating a New Draft

**Method 1: Toolbar Button**
- Click "New Draft" in the left panel
- Enter a title when prompted

**Method 2: Keyboard Shortcut**
- Press `Ctrl+D` anywhere in the application

**Method 3: Context Menu**
- Right-click in the Posts or Drafts tab
- Select "New Draft"

### Creating a New Page

**Method 1: Toolbar Button**
- Click "New Page" in the left panel
- Enter a title when prompted

**Method 2: Keyboard Shortcut**
- Press `Ctrl+G` anywhere in the application

**Method 3: Context Menu**
- Right-click in the Pages tab
- Select "New Page"

### File Naming

Kugo automatically creates clean filenames:
- **Input**: "My First Blog Post"
- **Filename**: `my-first-blog-post.md`
- **Duplicates**: Automatically numbered (`my-post.md`, `my-post-1.md`)

## 🔗 Content Management Features

### Copy Link Feature

Easily get Hugo URLs for cross-referencing:

1. **Right-click** any post or page
2. **Select "Copy Link"** from the context menu
3. **Paste** the URL into other content

**Generated URLs:**
- Posts: `/posts/my-post/`
- Pages: `/about/` (no `/pages/` prefix)
- Root content: `/my-content/`

### Front Matter Management

Kugo automatically handles Hugo front matter:

**For Posts:**
```yaml
---
title: "My Post Title"
date: 2025-08-05T10:30:00Z
draft: true
tags: []
categories: []
---
```

**For Pages:**
```yaml
---
title: "About"
date: 2025-08-05T10:30:00Z
draft: false
menu:
  main:
    weight: 1
---
```

### Adding Pages to Menu

1. **Right-click** any page in the Pages tab
2. **Select "Add to Menu"**
3. **Enter weight** (or accept auto-calculated suggestion)
4. Page automatically added to Hugo navigation

## 🛠️ Hugo Integration

### Building Your Site

**Quick Build**: Press `F5` or click "Build Site"
- Generates static files in the public directory
- Shows build status and any errors

### Development Server

**Start Server**: Press `F6` or click "Serve Site"
- Starts Hugo development server
- Automatically opens your default browser
- Shows server URL and status

**Stop Server**: Press `F7` or click "Stop Server"
- Cleanly stops the development server
- Frees up the port for other uses

### Draft Preview Control

**Include Drafts Toggle**:
- Go to `Hugo` → `Include Drafts in Preview`
- Toggle on/off to show/hide drafts in development server
- Default: OFF (matches production behavior)

### Configuration Editing

**Access Hugo Config**:
- Go to `Hugo` → `Edit Config`
- Opens your `config.toml`, `config.yaml`, or `config.json`
- Make changes and save directly in Kugo

## ⌨️ Keyboard Shortcuts

### Content Creation
- `Ctrl+D` - New Draft
- `Ctrl+G` - New Page
- `Ctrl+S` - Save current file

### Hugo Commands
- `F5` - Build Site
- `F6` - Serve Site
- `F7` - Stop Server

### Navigation
- `Ctrl+1` - Switch to Editor tab
- `Ctrl+2` - Switch to Preview tab

### File Management
- `Ctrl+O` - Open Blog
- `Ctrl+Shift+O` - Open File
- `Delete` - Delete selected content (with confirmation)

## 📊 Content Organization

### Chronological Sorting

Content is automatically sorted by date from the front matter:
- **Newest first** in all tabs
- **Based on publication date**, not file creation time
- **Consistent sorting** across posts, drafts, and pages

### Draft vs Published

**Drafts Tab**: Shows content with `draft: true`
**Posts Tab**: Shows content with `draft: false` or no draft field

To publish a draft:
1. Open the draft in the editor
2. Change `draft: true` to `draft: false` in the front matter
3. Save the file
4. Content moves from Drafts to Posts automatically

## 🔧 Managing Multiple Blogs

### Switching Blogs

1. **Open Blog Selector** (dropdown at top of left panel)
2. **Choose** from your configured blogs
3. **Interface updates** to show the selected blog's content

### Blog Settings

**Access**: `Hugo` → `Manage Blogs`

**Edit Blog Information**:
- Select blog from the list
- Modify name, paths, or publish command
- Click "Save Changes"

**Add New Blog**:
- Click "Add" in the Manage Blogs dialog
- Fill in the blog details
- Blog appears in your blog selector

**Remove Blog**:
- Select blog from the list
- Click "Remove" (confirmation required)
- Blog removed from Kugo (files remain untouched)

## 🚀 Publishing & Deployment

### Publish Commands

Store your deployment commands for easy access:

1. **Set Command**: In Blog settings, add your publish command
2. **Access Command**: `Hugo` → `Publish Command`
3. **Copy & Use**: Command is displayed with copy button

**Example Commands**:
```bash
# GitHub Pages
git add . && git commit -m "Update" && git push

# Netlify CLI
netlify deploy --prod

# FTP Upload
rsync -av public/ user@server:/var/www/html/

# Custom Script
./deploy.sh
```

## 🎨 Customization

### Editor Preferences

The markdown editor includes:
- **Syntax highlighting** for markdown and code blocks
- **Auto-indentation** for lists and code
- **Line numbers** and current line highlighting
- **Word wrap** for comfortable editing

### Preview Styling

The preview uses modern, professional CSS with:
- **Typography**: Clean, readable fonts
- **Layout**: Responsive design that looks great on any screen
- **Code Syntax**: Highlighted code blocks
- **Tables**: Properly styled data tables

## 🐛 Troubleshooting

### Common Issues

**Hugo Not Found**:
- Install Hugo: `sudo apt install hugo` (Ubuntu/Debian)
- Or download from: https://gohugo.io/installation/

**Blog Not Loading**:
- Verify the root path contains a valid Hugo site
- Check for `config.toml`, `config.yaml`, or `config.json`

**Server Won't Start**:
- Check if port 1313 is already in use
- Stop any existing Hugo servers: `pkill hugo`

**Preview Not Updating**:
- Save the file first (Ctrl+S)
- Switch tabs to refresh preview

### Configuration Files

**Application Data Location**:
- Linux: `~/.local/share/Kugo/blogs.json`
- Contains your blog configurations and settings

**Template Location**:
- Kugo directory: `templates/`
- Contains post and page templates

## 📞 Getting Help

### Resources
- **GitHub Issues**: Report bugs and request features
- **User Guide**: This comprehensive guide
- **Changelog**: See what's new in each version

### Community
- **Contribute**: Fork the repository and submit pull requests
- **Share**: Tell others about Kugo if you find it useful
- **Feedback**: Let us know how we can improve!

---

**Happy blogging with Kugo! 🎉**

1. **Method 1**: Click "New Draft" button or use `Ctrl+N`
2. **Method 2**: Right-click in the Posts or Drafts tab and select "New Draft"

This will:
- Prompt for a title
- Generate a clean filename (e.g., `my-draft.md`)
- Create the file with proper front matter (`draft: true`)
- Open it in the editor
- Show in the Drafts tab

### Publishing Drafts

To publish a draft as a post:
1. Open the draft file
2. In the front matter, change `draft: true` to `draft: false`
3. Save the file
4. The content will move from Drafts tab to Posts tab

### Creating New Pages

1. **Method 1**: Click "New Page" button or use `Ctrl+G`
2. **Method 2**: Right-click in the Pages tab and select "New Page"

Pages are created without date prefixes and typically go in the root content directory or a pages subdirectory.

### Editing Content

- **Double-click** any post or page in the browser to open it
- Use the **markdown editor** with syntax highlighting
- **Live preview** shows formatted output in real-time
- **Save** with `Ctrl+S` or the Save button

### Deleting Content

- **Right-click** on any post or page and select "Delete"
- Confirm the deletion when prompted

### Copying Links for Cross-References

- **Right-click** on any post or page and select "Copy Link"
- The Hugo URL is copied to your clipboard
- Perfect for creating internal links like `[see this post](/posts/my-other-post/)`
- Works for both posts and pages

## Hugo Integration

### Building Your Site

Click the "Hugo Build" button to generate your static site. This runs `hugo` in your site directory and always excludes drafts.

### Testing Your Site

Click "Hugo Serve" to start a local development server. 

**Draft Handling**:
- **Default**: Excludes drafts (matches production behavior)
- **Include Drafts**: Use Hugo → "Include Drafts in Preview" to show drafts during development
- **Toggle**: Change setting any time - applies to next serve command

### Editing Configuration

Click "Edit Config" to open your Hugo configuration file (`hugo.toml`, `config.toml`, etc.) in the editor.

## Managing Multiple Blogs

### Adding Blogs

1. Click "Add Blog" 
2. Provide:
   - **Name**: Friendly name for your blog
   - **Root Path**: Path to your Hugo site directory
   - **Public Path**: Where generated files go (usually `root/public`)
   - **Publish Command**: Command to deploy your site

### Switching Between Blogs

Use the dropdown at the top of the left panel to switch between configured blogs.

### Managing Blog Settings

Use **Hugo** → **Manage Blogs** to:
- Edit blog settings
- Update paths
- Modify publish commands
- Remove blogs

## Publishing Your Site

### Setting Up Publish Commands

When adding or editing a blog, you can specify a publish command. Common examples:

```bash
# Git-based publishing
cd /path/to/blog && git add . && git commit -m "Update" && git push

# rsync to server
rsync -avz --delete public/ user@server:/var/www/html/

# AWS S3
aws s3 sync public/ s3://my-bucket/ --delete

# Netlify CLI
netlify deploy --prod --dir=public
```

### Using Publish Commands

1. Click "Publish Command" button
2. Copy the command to your clipboard
3. Paste and run in your terminal

## Tips and Tricks

### Keyboard Shortcuts

- `Ctrl+N`: New draft
- `Ctrl+Alt+N`: New page  
- `Ctrl+O`: Open file
- `Ctrl+S`: Save file
- `Ctrl+Q`: Quit application

### Content Creation Workflow

Kugo uses a **draft-first workflow** for better content management:

1. **Create Draft**: All new content starts as drafts (`draft: true`)
2. **Write & Edit**: Develop your content in the draft
3. **Publish**: When ready, change `draft: true` to `draft: false` in the front matter
4. **Organize**: Published content appears in the Posts tab, drafts stay in Drafts tab

### Front Matter

Kugo automatically creates proper front matter for posts and pages:

**Posts**:
```yaml
---
title: "My Post Title"
date: 2025-08-05T10:30:00+00:00
draft: false
---
```

**Drafts**:
```yaml
---
title: "My Draft Title"
date: 2025-08-05T10:30:00+00:00
draft: true
---
```

**Pages**:
```yaml
---
title: "My Page Title"
---
```

### File Organization

Kugo follows Hugo conventions and intelligently separates content:
- **Published Posts**: Content with `draft: false` or no draft field, shown in Posts tab
- **Draft Posts**: Content with `draft: true`, shown in Drafts tab  
- **Pages**: Static content without dates, shown in Pages tab
- Posts and drafts go in `content/posts/` (or root `content/` for simple sites)
- Pages go in `content/pages/` (or root `content/`)
- Static files go in `static/`
- Layouts/templates go in `layouts/`

### Preview Features

The live preview supports:
- **Professional HTML rendering** with modern styling
- Headers and formatting with visual hierarchy
- Code blocks with syntax highlighting
- Tables with hover effects and alternating row colors
- Links and images with styling
- Blockquotes with accent borders
- Lists with proper spacing
- Responsive design for different screen sizes
- Table of contents generation
- **Real-time updates** as you type

### Performance

- Live preview updates with a 500ms delay to avoid lag while typing
- File watching automatically refreshes the file browser when content changes
- Large sites are handled efficiently with lazy loading

## Troubleshooting

### Hugo Not Found

If you get "Hugo not found" errors:

```bash
# Ubuntu/Debian
sudo apt install hugo

# Or download from https://gohugo.io/installation/
```

### Permission Issues

If you can't write to directories:
```bash
# Check permissions
ls -la /path/to/your/blog

# Fix if needed
chmod -R u+w /path/to/your/blog
```

### Dependencies Issues

If the application won't start:
```bash
# Reinstall dependencies
cd /path/to/kugo
./install.sh
```

### Configuration Reset

To reset all settings:
```bash
# Remove config directory
rm -rf ~/.local/share/Kugo/
```

## Advanced Usage

### Custom Templates

You can modify the templates in the `templates/` directory to customize the default content for new posts and pages.

### Multiple Hugo Versions

If you have multiple Hugo versions, you can specify the path in your publish commands:
```bash
/usr/local/bin/hugo-v0.123.0 build
```

### Theme Development

Kugo works great for theme development - use the live preview to see changes as you edit your theme files.

## Support

For issues, suggestions, or contributions, please visit the project repository or open an issue.

Happy blogging with Kugo! 🚀
