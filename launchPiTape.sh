#!/bin/bash

# Activate the Python virtual environment
source ~/environments/MediaCV/bin/activate

# Run the SuperCollider script
sclang ~/Repos/Mediapipe-Midi/SCScripts/TapeStop.scd &

# Run the Python script
python ~/Repos/Mediapipe-Midi/VelocityOSC-pose.py