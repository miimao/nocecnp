#!/bin/bash
set -e

SERVICE_FILE="/etc/systemd/system/nocecnp.service"
INSTALL_DIR="/opt/nocecnp"
CONFIG_DIR="/etc/opt/nocecnp"

if [ "$EUID" -ne 0 ]; then
  echo "This uninstaller must be run as root. Please use sudo."
  exit 1
fi

echo "Stopping and disabling systemd service..."
systemctl stop nocecnp.service || true
systemctl disable nocecnp.service || true

echo "Removing systemd service file..."
rm -f "$SERVICE_FILE"

echo "Reloading systemd daemon..."
systemctl daemon-reload

echo "Removing installed files..."
rm -rf "$INSTALL_DIR"

echo "Removing config directory..."
rm -rf "$CONFIG_DIR"

echo "Uninstall complete."