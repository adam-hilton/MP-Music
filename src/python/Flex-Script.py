#Import the necessary Packages for this software to run
import os
import yaml
import importlib
import mediapipe
import cv2
from picamera2 import Picamera2
from libcamera import controls
import screeninfo
from pythonosc import udp_client
# import pyautogui

# load the config dictionary
def load_config(file_path="config/config.yaml"):
    with open(file_path, "r") as file:
        config = yaml.safe_load(file)
    return config

# # get size of screen from environment resolution
# screen = screeninfo.get_monitors()[0]

def send_midi():
    print("Midi data sent")

def midi_note_scale(value):

    min_value = 0
    max_value = 720
    min_result = 50
    max_result = 80

    midiValue = min_result + (value - min_value)/(max_value - min_value)*(max_result - min_result)
    return midiValue

def midi_cc_scale(value2):
    min_value2 = 0
    max_value2 = 576
    min_result2 = 127
    max_result2 = 0

    ccVal = min_result2 + (value2 - min_value2)/(max_value2 - min_value2)*(max_result2 - min_result2)
    return ccVal


def send_osc(client):
    print("OSC data sent")
    client.send_message("/control/XLeftIndex", 100)
    client.send_message("/control/YLeftIndex", 11)
              
    client.send_message("/control/XRightIndex", 13)
    client.send_message("/control/YRightIndex", 12)

def main():
    config = load_config()
    # setup the OSC client
    client = udp_client.SimpleUDPClient(config['osc']['ip'], config['osc']['port'])
    print("Main function ran")
    if config['mediapipe_module'].get('pose', False):
        print("Pose module present")
        if config["midi"].get("out"):
            send_midi()
        if config["osc"].get("out"):
            send_osc(client)
    else:
        print("Pose module not present")

    if config['mediapipe_module'].get('hands', False):
        print("Hands module present")
        if config["midi"].get("out"):
            send_midi()
        if config["osc"].get("out"):
            send_osc(client)
    else:
        print("Hands module not present")
    

if __name__ == "__main__":
    main()