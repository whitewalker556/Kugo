#!/bin/bash
# Desktop entry installer for Kugo

DESKTOP_FILE="kugo.desktop"
INSTALL_DIR="$HOME/.local/share/applications"
CURRENT_DIR="$(pwd)"

echo "📱 Installing Kugo desktop entry..."

# Create applications directory if it doesn't exist
mkdir -p "$INSTALL_DIR"

# Update desktop file with correct paths
sed "s|/home/tim/Projects/Main/Kugo|$CURRENT_DIR|g" "$DESKTOP_FILE" > "$INSTALL_DIR/kugo.desktop"

# Make desktop file executable
chmod +x "$INSTALL_DIR/kugo.desktop"

echo "✅ Desktop entry installed to $INSTALL_DIR/kugo.desktop"
echo "You can now launch Kugo from your application menu!"

# Update desktop database if available
if command -v update-desktop-database &> /dev/null; then
    update-desktop-database "$INSTALL_DIR"
    echo "✓ Desktop database updated"
fi
