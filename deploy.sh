#!/bin/bash

echo "* getting snapshot"
./snap.py

echo "* getting weather"
./weathercam.py

echo "* copy static files"
cp -avu static output/

echo "* uploading files"
aws s3 sync output/. s3://webcam.calpenedes.com/ --cache-control "max-age=600"

exit 0
