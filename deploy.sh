#!/bin/bash

./snap.py
./weathercam.py

aws s3 cp --dryrun --recursive output/. s3://webcam.calpenedes.com/

