# Mediapipe Midi

Mediapipe Midi is a series of simple script that use Mediapipe, OpenCV, and Mido to turn your movements into usable MIDI.

## Dependencies & Usage

Libraries
- Picamera2
- Mediapipe
- OpenCV
- Mido

If running headless:
connect pi to external monitor
start x server
execute 
``export DISPLAY=:0``

<!-- Built using Picamera2 library rather OpenCV video streaming, as this was initially built using an Arducam -->

## Backlog

- add support for frame buffer (true headless, no x server)
- make config.yml to support reusable elements
- more gestures & pose detections
- refactor for improved performance
- outline for full pi setup in readme