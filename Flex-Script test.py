#Import the necessary Packages for this software to run
import os, yaml, mediapipe, cv2, screeninfo
# import pyautogui
from picamera2 import Picamera2
from libcamera import controls
from pythonosc import udp_client
from utils.config_loader import load_config
from utils.min_max_scaler import scale_value


def send_midi():
    print("Midi data sent")

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
    client = udp_client.SimpleUDPClient(config['osc']['ip'], 
                                        config['osc']['port'])
    print("Main function ran")
    scaled = scale_value(500, 
                         config['midi']['min_in_1'], 
                         config['midi']['max_in_1'], 
                         config['midi']['min_out_1'], 
                         config['midi']['max_out_1'])
    print(scaled)
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