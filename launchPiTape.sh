#!/bin/bash

# Activate the Python virtual environment
source ~/environments/MediaCV/bin/activate

# Run the SuperCollider script
sclang ~/Repos/Mediapipe-Midi/SCScripts/TapeStopOSC.scd &

# Run the Python script
python ~/Repos/Mediapipe-Midi/VelocityTrackOSC-pose.py