# Weathercam

 Simple scripts that 
 1. grab an image from one of my Reolink cameras
 2. get the weather data from my Ecowitt weather station
 3. generate a static webpage from this
 4. upload it to a S3 bucket

## Scripts 
- snap.py - get the image
- weathercam.py - get the data and create the html
- deploy.sh run all of this and upload it to S3

## Env variables 
The scripts load an .env file, there is a sample in the repo

