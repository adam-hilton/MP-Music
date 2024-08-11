# Midi Hand Tracker

Midi Hand Tracker is a simple script that uses Mediapipe, OpenCV, and Mido to turn your hand movements into MIDI data.

## Dependencies & Usage

Libraries
- Picamera2
- Mediapipe
- OpenCV
- Mido

If running headless while connected to a monitor:
execute 
``export DISPLAY=:0``
in terminal prior to running. Only works after booted to desktop GUI.

Built using Picamera2 library rather OpenCV video streaming, as this was initially built using an Arducam

## Future iterations

- add support for frame buffer (true headless, no x server)
- make config.yml to support 
- make different finger/body points configurable
- add CC support
- add support for multi-hand
- add various gesture support