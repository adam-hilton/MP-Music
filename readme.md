# Mediapipe Midi

Mediapipe Midi is a series of simple scripts that use Mediapipe, OpenCV, Mido, and OSC to turn your movements into usable data that can be used for 

## Dependencies & Usage

### Key Libraries
- Picamera2
- Mediapipe
- OpenCV
- Mido
- Python OSC
- PyYAML
- PyAutoGUI


### If running headless via ssh:
- connect pi to external monitor
- start x server
- execute ``export DISPLAY=:0``

<!-- Built using Picamera2 library rather OpenCV video streaming, as this was initially built using an Arducam -->

## Backlog

- add support for non-X frame buffer (true headless, no x server)
- modularize MIDI and OSC commands to be called separately based on config.yaml
- abstract the image stream so multiple MP meshes can run concurrently
- create python launcher script to install & run dependency environment
