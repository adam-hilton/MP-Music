#!/bin/bash

# Activate the Python virtual environment
source ~/environments/MediaCV/bin/activate

# Run the SuperCollider script
sclang ~/Repos/Mediapipe-Midi/SCScripts/RingsCloudsChords-OSC.scd &

# Run the Python script
python ~/Repos/Mediapipe-Midi/HandTrackOSC.py