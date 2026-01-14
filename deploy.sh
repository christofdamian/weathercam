#!/bin/bash

set -e

# Load .env file if it exists
if [ -f .env ]; then
    set -a
    source <(grep -v '^#' .env | grep -v '^$' | grep -v 'SERVER_SSH_KEY')
    set +a
    # Handle SERVER_SSH_KEY separately (base64 encoded)
    SERVER_SSH_KEY=$(grep '^SERVER_SSH_KEY=' .env | cut -d'=' -f2- | tr -d '"')
fi

echo "* getting snapshot"
./snap.py

echo "* getting weather"
./weathercam.py

echo "* copy static files"
cp -avu static output/

echo "* uploading files"

DEPLOY_TARGET="${DEPLOY_TARGET:-aws}"

if [ "$DEPLOY_TARGET" = "server" ]; then
    echo "  target: server"

    if [ -z "$SERVER_HOST" ] || [ -z "$SERVER_USER" ] || [ -z "$SERVER_SSH_KEY" ]; then
        echo "Error: SERVER_HOST, SERVER_USER, and SERVER_SSH_KEY must be set"
        exit 1
    fi

    SERVER_PATH="${SERVER_PATH:-/var/www/html}"

    # Write SSH key to temp file (decode from base64)
    SSH_KEY_FILE=$(mktemp)
    echo "$SERVER_SSH_KEY" | base64 -d > "$SSH_KEY_FILE"
    chmod 600 "$SSH_KEY_FILE"

    # Cleanup on exit
    trap "rm -f $SSH_KEY_FILE" EXIT

    rsync -avz --delete \
        -e "ssh -i $SSH_KEY_FILE -o StrictHostKeyChecking=accept-new" \
        output/. \
        "${SERVER_USER}@${SERVER_HOST}:${SERVER_PATH}/"
else
    echo "  target: aws"
    aws s3 sync output/. s3://webcam.calpenedes.com/ --cache-control "max-age=600"
fi

exit 0
