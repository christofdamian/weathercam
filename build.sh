#!/bin/bash

set -e

echo "Building Docker image..."
docker build -t weathercam:latest .

echo "Saving Docker image to weathercam.img..."
docker save weathercam:latest -o weathercam.img

echo "Done! Docker image saved to weathercam.img"
echo "Image size: $(du -h weathercam.img | cut -f1)"
