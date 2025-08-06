"""
Utility functions for Kugo
"""

import os
import re
import json
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Optional


def slugify(text: str) -> str:
    """Convert text to URL-friendly slug"""
    # Convert to lowercase
    text = text.lower()
    # Remove non-alphanumeric characters except spaces and hyphens
    text = re.sub(r'[^\w\s-]', '', text)
    # Replace spaces and multiple hyphens with single hyphen
    text = re.sub(r'[-\s]+', '-', text)
    # Remove leading/trailing hyphens
    text = text.strip('-')
    return text


def parse_front_matter(content: str) -> tuple[Dict, str]:
    """Parse YAML front matter from markdown content"""
    import yaml
    
    if not content.startswith('---'):
        return {}, content
        
    try:
        # Find the end of front matter
        parts = content.split('---', 2)
        if len(parts) >= 3:
            front_matter = yaml.safe_load(parts[1])
            body = parts[2].lstrip('\n')
            return front_matter or {}, body
    except:
        pass
        
    return {}, content


def create_front_matter(data: Dict) -> str:
    """Create YAML front matter from dictionary"""
    import yaml
    
    # Custom representer for dates
    def date_representer(dumper, data):
        return dumper.represent_scalar('tag:yaml.org,2002:timestamp', data.isoformat())
    
    yaml.add_representer(datetime, date_representer)
    
    return f"---\n{yaml.dump(data, default_flow_style=False)}---\n\n"


def get_hugo_content_types(hugo_root: Path) -> List[str]:
    """Get content types from Hugo site"""
    content_dir = hugo_root / "content"
    if not content_dir.exists():
        return []
        
    content_types = []
    for item in content_dir.iterdir():
        if item.is_dir() and not item.name.startswith('.'):
            content_types.append(item.name)
            
    return sorted(content_types)


def find_hugo_config(hugo_root: Path) -> Optional[Path]:
    """Find Hugo configuration file"""
    config_files = [
        "hugo.toml", "hugo.yaml", "hugo.yml", "hugo.json",
        "config.toml", "config.yaml", "config.yml", "config.json"
    ]
    
    for config_file in config_files:
        config_path = hugo_root / config_file
        if config_path.exists():
            return config_path
            
    return None


def is_hugo_site(path: Path) -> bool:
    """Check if directory is a Hugo site"""
    # Check for config file
    if find_hugo_config(path):
        return True
        
    # Check for content directory
    if (path / "content").exists():
        return True
        
    return False


def get_file_metadata(file_path: Path) -> Dict:
    """Get metadata for a file"""
    try:
        stat = file_path.stat()
        return {
            'size': stat.st_size,
            'modified': datetime.fromtimestamp(stat.st_mtime),
            'created': datetime.fromtimestamp(stat.st_ctime),
        }
    except:
        return {}


def load_template(template_name: str) -> str:
    """Load a template file"""
    template_dir = Path(__file__).parent.parent / "templates"
    template_path = template_dir / f"{template_name}.md"
    
    if template_path.exists():
        try:
            with open(template_path, 'r', encoding='utf-8') as f:
                return f.read()
        except:
            pass
            
    return ""


def format_template(template: str, **kwargs) -> str:
    """Format template with variables"""
    try:
        return template.format(**kwargs)
    except:
        # Fallback for templates with double braces
        for key, value in kwargs.items():
            template = template.replace(f"{{{{ {key} }}}}", str(value))
        return template


def ensure_directory(path: Path) -> bool:
    """Ensure directory exists, create if needed"""
    try:
        path.mkdir(parents=True, exist_ok=True)
        return True
    except:
        return False


def backup_file(file_path: Path) -> Optional[Path]:
    """Create a backup of a file"""
    try:
        backup_path = file_path.with_suffix(file_path.suffix + '.bak')
        import shutil
        shutil.copy2(file_path, backup_path)
        return backup_path
    except:
        return None


def get_word_count(text: str) -> int:
    """Get word count for text"""
    # Remove markdown syntax for more accurate count
    text = re.sub(r'#+ ', '', text)  # Headers
    text = re.sub(r'\*\*(.*?)\*\*', r'\1', text)  # Bold
    text = re.sub(r'\*(.*?)\*', r'\1', text)  # Italic
    text = re.sub(r'`(.*?)`', r'\1', text)  # Code
    text = re.sub(r'\[(.*?)\]\(.*?\)', r'\1', text)  # Links
    
    # Count words
    words = text.split()
    return len([word for word in words if word.strip()])


def get_reading_time(text: str, words_per_minute: int = 200) -> int:
    """Estimate reading time in minutes"""
    word_count = get_word_count(text)
    return max(1, round(word_count / words_per_minute))


def validate_hugo_site(path: Path) -> Dict[str, bool]:
    """Validate Hugo site structure"""
    checks = {
        'is_directory': path.is_dir(),
        'has_config': find_hugo_config(path) is not None,
        'has_content': (path / "content").exists(),
        'has_themes': (path / "themes").exists() or (path / "theme.toml").exists(),
    }
    
    checks['is_valid'] = checks['is_directory'] and checks['has_config']
    
    return checks
