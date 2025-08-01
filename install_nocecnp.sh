#!/bin/bash
set -e

if [ "$EUID" -ne 0 ]; then
  echo "This installer must be run as root. Please use sudo."
  exit 1
fi

INSTALL_DIR="/opt/nocecnp"
VENV_DIR="$INSTALL_DIR/venv"
CONFIG_DIR="/etc/opt/nocecnp"
CONFIG_FILE="$CONFIG_DIR/config.ini"
SERVICE_FILE="/etc/systemd/system/nocecnp.service"

echo "Creating $INSTALL_DIR..."
mkdir -p "$INSTALL_DIR"
# Copy only relevant files (excluding .git, venv, etc.)
rsync -rv \
  --include='nocecnp.py' \
  --include='nocecnp/***' \
  --include='requirements.txt' \
  --include='config.ini.example' \
  --exclude='*' \
  ./ "$INSTALL_DIR/"

# Ensure the main script is executable
chmod +x "$INSTALL_DIR/nocecnp.py"

echo "Creating config directory and example config if needed..."
mkdir -p "$CONFIG_DIR"
if [ ! -f "$CONFIG_FILE" ]; then
    cp "$INSTALL_DIR/config.ini.example" "$CONFIG_FILE"
    echo "Example config created at $CONFIG_FILE"
else
    echo "Config already exists at $CONFIG_FILE"
fi

echo "Setting up Python virtual environment..."
python3 -m venv "$VENV_DIR"
source "$VENV_DIR/bin/activate"

echo "Installing dependencies from requirements.txt..."
pip install --upgrade pip
pip install -r "$INSTALL_DIR/requirements.txt"

echo "Setting up systemd service..."
cat > "$SERVICE_FILE" <<EOF
[Unit]
Description=Nocecnp - CEC Alternative
After=network.target dbus.service

[Service]
Type=simple
ExecStart=$VENV_DIR/bin/python $INSTALL_DIR/nocecnp.py
Restart=on-failure
User=root
Environment=PYTHONUNBUFFERED=1

[Install]
WantedBy=multi-user.target
EOF

echo "Reloading systemd and enabling service..."
systemctl daemon-reload
systemctl enable --now nocecnp.service

echo "Done!"