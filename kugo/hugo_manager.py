"""
Hugo command manager
"""

import os
import subprocess
import threading
from pathlib import Path
from PySide6.QtCore import QObject, Signal, QProcess
from PySide6.QtWidgets import QMessageBox


class HugoManager(QObject):
    """Manager for Hugo commands"""
    
    command_finished = Signal(str, int)  # command, exit_code
    command_output = Signal(str)  # output text
    
    def __init__(self):
        super().__init__()
        self.blog_path = None
        self.serve_process = None
        self.include_drafts = False  # Default to not showing drafts
        
    def set_blog_path(self, path):
        """Set the current blog path"""
        self.blog_path = Path(path)
        
    def build(self):
        """Run Hugo build command"""
        if not self.blog_path:
            return False
            
        print("🔨 Starting Hugo build...")
        return self.run_hugo_command(["hugo"])
        
    def serve(self, include_drafts=None):
        """Run Hugo serve command"""
        if not self.blog_path:
            return False
            
        # Use parameter value or instance setting
        if include_drafts is None:
            include_drafts = self.include_drafts
            
        # Stop existing serve process
        self.stop_serve()
        
        # Start new serve process
        self.serve_process = QProcess()
        self.serve_process.finished.connect(self.on_serve_finished)
        self.serve_process.readyReadStandardOutput.connect(self.on_serve_output)
        self.serve_process.started.connect(self.on_serve_started)
        
        self.serve_process.setWorkingDirectory(str(self.blog_path))
        
        # Build command with optional draft inclusion
        args = ["serve"]
        if include_drafts:
            args.append("--buildDrafts")
            
        self.serve_process.start("hugo", args)
        
        return True
        
    def set_include_drafts(self, include_drafts):
        """Set whether to include drafts in serve"""
        self.include_drafts = include_drafts
        
    def on_serve_started(self):
        """Handle when Hugo serve process starts"""
        print("✓ Hugo serve started")
        # Open browser after a short delay to allow server to start
        from PySide6.QtCore import QTimer
        QTimer.singleShot(2000, self.open_browser)  # 2 second delay
        
    def open_browser(self):
        """Open browser to Hugo development server"""
        import webbrowser
        url = "http://localhost:1313"
        try:
            webbrowser.open(url)
            print(f"✓ Opened browser to {url}")
            self.command_output.emit(f"Opened browser to {url}")
        except Exception as e:
            print(f"✗ Failed to open browser: {e}")
            self.command_output.emit(f"Failed to open browser: {e}")
        
    def stop_serve(self):
        """Stop the Hugo serve process"""
        if self.serve_process and self.serve_process.state() != QProcess.ProcessState.NotRunning:
            self.serve_process.kill()
            self.serve_process.waitForFinished(3000)
            
    def on_serve_finished(self, exit_code):
        """Handle serve process completion"""
        self.command_finished.emit("serve", exit_code)
        
    def on_serve_output(self):
        """Handle serve process output"""
        if self.serve_process:
            data = self.serve_process.readAllStandardOutput()
            try:
                output = bytes(data.data()).decode('utf-8')
            except:
                output = str(data)
            self.command_output.emit(output)
            
    def run_hugo_command(self, args):
        """Run a Hugo command"""
        if not self.blog_path:
            return False
            
        try:
            # Run Hugo command in a separate thread to avoid blocking UI
            def run_command():
                try:
                    process = subprocess.run(
                        args,
                        cwd=str(self.blog_path),
                        capture_output=True,
                        text=True,
                        timeout=30
                    )
                    
                    # Emit signals from main thread
                    self.command_finished.emit(" ".join(args), process.returncode)
                    if process.stdout:
                        self.command_output.emit(process.stdout)
                    if process.stderr:
                        self.command_output.emit(process.stderr)
                        
                except subprocess.TimeoutExpired:
                    self.command_finished.emit(" ".join(args), -1)
                    self.command_output.emit("Command timed out")
                except Exception as e:
                    self.command_finished.emit(" ".join(args), -1)
                    self.command_output.emit(f"Error: {str(e)}")
                    
            thread = threading.Thread(target=run_command)
            thread.daemon = True
            thread.start()
            
            return True
            
        except Exception as e:
            self.command_output.emit(f"Failed to run Hugo command: {str(e)}")
            return False
            
    def get_config_path(self):
        """Get the path to Hugo configuration file"""
        if not self.blog_path:
            return None
            
        # Check for different config file formats
        config_files = [
            "hugo.toml", "hugo.yaml", "hugo.yml", "hugo.json",
            "config.toml", "config.yaml", "config.yml", "config.json"
        ]
        
        for config_file in config_files:
            config_path = self.blog_path / config_file
            if config_path.exists():
                return str(config_path)
                
        return None
        
    def is_hugo_site(self, path):
        """Check if a directory is a Hugo site"""
        hugo_path = Path(path)
        
        # Check for Hugo config file
        config_files = [
            "hugo.toml", "hugo.yaml", "hugo.yml", "hugo.json",
            "config.toml", "config.yaml", "config.yml", "config.json"
        ]
        
        for config_file in config_files:
            if (hugo_path / config_file).exists():
                return True
                
        # Check for content directory
        if (hugo_path / "content").exists():
            return True
            
        return False
        
    def get_hugo_version(self):
        """Get Hugo version"""
        try:
            result = subprocess.run(
                ["hugo", "version"],
                capture_output=True,
                text=True,
                timeout=5
            )
            if result.returncode == 0:
                return result.stdout.strip()
        except:
            pass
            
        return "Hugo not found"
        
    def create_new_site(self, path, site_name):
        """Create a new Hugo site"""
        try:
            result = subprocess.run(
                ["hugo", "new", "site", site_name],
                cwd=str(path),
                capture_output=True,
                text=True,
                timeout=30
            )
            
            if result.returncode == 0:
                return True, result.stdout
            else:
                return False, result.stderr
                
        except Exception as e:
            return False, str(e)
