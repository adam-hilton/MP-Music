#Import the necessary Packages for this software to run
# from sklearn import preprocessing
import mediapipe
import os
import cv2
from picamera2 import Picamera2
import mido
from libcamera import controls
import screeninfo
import time

# # Set the environment for framebuffer -- to access later for headless mode
# os.putenv('SDL_FBDEV', '/dev/fb0')  # Framebuffer device
# os.putenv('SDL_VIDEODRIVER', 'fbcon')  # Use framebuffer console
# os.putenv('SDL_NOMOUSE', '1')  # Disable mouse cursor


# get size of screen
screen = screeninfo.get_monitors()[0]

#Configuring picam2 stream

picam2 = Picamera2()
picam2.preview_configuration.main.size = (720,576)

picam2.preview_configuration.main.format = "RGB888"
picam2.preview_configuration.align()
picam2.configure("preview")

#startpicam2 stream
picam2.start()
picam2.set_controls({"AfMode": controls.AfModeEnum.Continuous})

# set port to pisound DIN5
port = mido.open_output('pisound MIDI PS-1MJPEPE')

#Use MediaPipe to draw the hand framework over the top of hands it identifies in Real-Time
drawingModule = mediapipe.solutions.drawing_utils
handsModule = mediapipe.solutions.hands

# define initial 'Previous' position
PosPrev = None

# define loop interval
time_interval = .1

ccVal = 96

# function to scale ouput to readable midi values

def mapToCC(value, min_value, max_value, min_result, max_result):
    clamped_vel = max(min_value, min(value, 1000))
    velValue = min_result + (clamped_vel - min_value)/(max_value - min_value)*(max_result - min_result)
    return velValue

min_value = -1000
max_value = 1000
min_result = 0
max_result = 127

# Midi variables
midiChannel = 1


#Add confidence values and extra settings to MediaPipe hand tracking. As we are using a live video stream this is not a static
#image mode, confidence values in regards to overall detection and tracking and we will only let two hands be tracked at the same time
#More hands can be tracked at the same time if desired but will slow down the system
with handsModule.Hands(static_image_mode=False, min_detection_confidence=0.7, min_tracking_confidence=0.7, max_num_hands=1) as hands:

#Create an infinite loop which will produce the live feed to our desktop and that will search for hands
     while True:
           im = picam2.capture_array()
           #Unedit the below line if your live feed is produced upsidedown
           im = cv2.flip(im, flipCode = 0)
           
           
           #produces the hand framework overlay ontop of the hand, you can choose the colour here too)
           results = hands.process(cv2.cvtColor(im, cv2.COLOR_BGR2RGB))
           
           #Incase the system sees multiple hands this if statment deals with that and produces another hand overlay
           if results.multi_hand_landmarks != None:
              for handLandmarks in results.multi_hand_landmarks:
                drawingModule.draw_landmarks(im, handLandmarks, handsModule.HAND_CONNECTIONS)
                for point in handsModule.HandLandmark:
                    normalizedLandmark = handLandmarks.landmark[point]
                    pixelCoordinatesLandmark= drawingModule._normalized_to_pixel_coordinates(normalizedLandmark.x, normalizedLandmark.y, 720, 576)
                    if point == 8:
                        if pixelCoordinatesLandmark != None:
                            PosNew = pixelCoordinatesLandmark[0]
                            if PosPrev is not None:
                                vel = (PosNew - PosPrev)/time_interval

                                if vel >= -1000 and vel <= 1000:

                                    ccVal = int(mapToCC(vel, min_value, max_value, min_result, max_result))

                                    message = mido.Message('control_change', channel=4, control=1, value=ccVal, time=1)

                                    port.send(message)
                            

                                

                                print(ccVal)

                            PosPrev = PosNew

                            time.sleep(time_interval)
                        # else:
                        #     port.send(mido.Message('control_change', channel=4, control=1, value=96, time=1))
                        #     print(96)
                            

            
           #Below shows the current frame to the desktop 
        #    cv2.namedWindow("foo", cv2.WINDOW_NORMAL)
        #    cv2.setWindowProperty("foo", cv2.WND_PROP_FULLSCREEN, cv2.WINDOW_FULLSCREEN)
           window_name = "Frame"
           cv2.namedWindow(window_name, cv2.WINDOW_NORMAL)
           cv2.moveWindow(window_name, screen.x - 1, screen.y - 1)
           cv2.setWindowProperty(window_name, cv2.WND_PROP_FULLSCREEN,
                          cv2.WINDOW_FULLSCREEN)
           cv2.imshow(window_name, im);
           key = cv2.waitKey(1) & 0xFF
        
           #Below states that if the |q| is press on the keyboard it will stop the system
           if key == ord("q"):
              port.close()
              if port.closed:
                  print("port closed.")
              break