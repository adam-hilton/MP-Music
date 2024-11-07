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

# Dynamically import the specified mediapipe module
def load_mediapipe_class(module_name):
    try:
        # Import the entire module dynamically
        mediapipe_module = importlib.import_module(f"mediapipe.python.solutions.{module_name}")
        # Get the class with the same name as the module
        mediapipe_class = getattr(mediapipe_module, module_name.capitalize())
        return mediapipe_class
    except (ModuleNotFoundError, AttributeError) as e:
        print(f"Error loading module '{module_name}': {e}")
        return None

config = load_config()

mediapipe_module_name = config.get("mediapipe_module")
if mediapipe_module_name:
    mediapipe_class = load_mediapipe_class(mediapipe_module_name)
    if mediapipe_class:
        print(f"Successfully loaded mediapipe class: {mediapipe_class}")
        # Instantiate the class (e.g., Hands or Pose)
        instance = mediapipe_class()
        # Now `instance` refers to either Hands(), Pose(), etc., based on the config
    else:
        print("Failed to load specified mediapipe class.")
else:
    print("No mediapipe module specified in config.")



# # get size of screen from environment resolution
# screen = screeninfo.get_monitors()[0]

# setup the OSC client
client = udp_client.SimpleUDPClient(config['osc']['ip'], config['osc']['port'])
