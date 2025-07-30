#!/bin/bash

echo "* getting snapshot"
./snap.py

echo "* getting weather"
./weathercam.py

echo "* uploading files"
aws --profile webcam-script s3 cp --recursive output/. s3://webcam.calpenedes.com/

