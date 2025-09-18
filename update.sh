#!/bin/bash

# Configuration
REMOTE_HOST="tp2"  # Change this to your server's hostname/IP
REMOTE_USER="tuma"  # Change this to your username on the server
REMOTE_PATH="~/civ6notifier"  # Change this to the target path on the server

# Rsync options:
# -a: archive mode (preserves permissions, timestamps, etc.)
# -v: verbose
# -z: compress during transfer
# --delete: delete files on remote that don't exist locally
# --exclude: exclude certain files/directories
rsync -avz --delete \
  --exclude='.git/' \
  --exclude='__pycache__/' \
  --exclude='*.pyc' \
  --exclude='.venv/' \
  --exclude='*.log' \
  --exclude='.DS_Store' \
  --exclude='civ6notifier.secrets' \
  ./ "${REMOTE_USER}@${REMOTE_HOST}:${REMOTE_PATH}"

echo "Sync complete!"
echo "To rebuild and restart the service on the server, run:"
echo "ssh ${REMOTE_USER}@${REMOTE_HOST} 'cd ${REMOTE_PATH} && ./run_docker.sh'"