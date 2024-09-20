#Import the necessary Packages for this software to run
# from sklearn import preprocessing
import mediapipe
import os
import cv2
from picamera2 import Picamera2
import mido
from libcamera import controls
import screeninfo
from pythonosc import udp_client

# # Set the environment for framebuffer -- not yet used
# os.putenv('SDL_FBDEV', '/dev/fb0')  # Framebuffer device
# os.putenv('SDL_VIDEODRIVER', 'fbcon')  # Use framebuffer console
# os.putenv('SDL_NOMOUSE', '1')  # Disable mouse cursor


# get size of screen
screen = screeninfo.get_monitors()[0]

# setup the OSC client
client = udp_client.SimpleUDPClient("127.0.0.1", 57120)

#Configuring picam2 stream

picam2 = Picamera2()
picam2.preview_configuration.main.size = (720,576)

picam2.preview_configuration.main.format = "RGB888"
picam2.preview_configuration.align()
picam2.configure("preview")

#startpicam2 stream
picam2.start()
picam2.set_controls({"AfMode": controls.AfModeEnum.Continuous})

#Use MediaPipe to draw the hand framework over the top of hands it identifies in Real-Time
drawingModule = mediapipe.solutions.drawing_utils
handsModule = mediapipe.solutions.hands

# function to scale ouput to readable midi values

# def mapToChordFloat(value, min_value, max_value, min_result, max_result):
 
#  midiValue = float(min_result) + (float(value) - float(min_value)) / (float(max_value) - float(min_value)) * (float(max_result) - float(min_result))
#  return midiValue

# min_value = 0
# max_value = 720
# min_result = 0.0
# max_result = 8.0

# def mapToVelFloat(value2, min_value2, max_value2, min_resul2, max_result2):
#     velValue = float(min_result2) + (float(value2) - float(min_value2)) / (float(max_value2) - float(min_value2)) * (float(max_result2) - float(min_result2))
#     return velValue

# min_value2 = 0
# max_value2 = 576
# min_result2 = 1.0
# max_result2 = 0.0



#Add confidence values and extra settings to MediaPipe hand tracking. As we are using a live video stream this is not a static
#image mode, confidence values in regards to overall detection and tracking and we will only let two hands be tracked at the same time
#More hands can be tracked at the same time if desired but will slow down the system
with handsModule.Hands(static_image_mode=False, min_detection_confidence=0.7, min_tracking_confidence=0.7, max_num_hands=2) as hands:

#Create an infinite loop which will produce the live feed to our desktop and that will search for hands
     while True:
           im = picam2.capture_array()
           #Unedit the below line if your live feed is produced upsidedown
           im = cv2.flip(im, flipCode = 0)
           
           
           #produces the hand framework overlay ontop of the hand, you can choose the colour here too)
           results = hands.process(cv2.cvtColor(im, cv2.COLOR_BGR2RGB))
           
           #Incase the system sees multiple hands this if statment deals with that and produces another hand overlay
           if results.multi_hand_landmarks !=None:
              for handLandmarks in results.multi_hand_landmarks:
                wrist_drawing_spec = drawingModule.DrawingSpec(color=(0, 0, 255), thickness=5, circle_radius=5)  # Red wrist
                default_drawing_spec = drawingModule.DrawingSpec(color=(255, 255, 255), thickness=2, circle_radius=2)  # Green others
                connection_drawing_spec = drawingModule.DrawingSpec(color=(255, 255, 255), thickness=1)
                wrist = handLandmarks.landmark[handsModule.HandLandmark.THUMB_TIP]
                index_finger_tip = handLandmarks.landmark[handsModule.HandLandmark.INDEX_FINGER_TIP]
                image_height, image_width, _ = im.shape
                wrist_px = mediapipe.solutions.drawing_utils._normalized_to_pixel_coordinates(wrist.x, wrist.y, image_width, image_height)
                index_finger_tip_px = mediapipe.solutions.drawing_utils._normalized_to_pixel_coordinates(index_finger_tip.x, index_finger_tip.y, image_width, image_height)
                
                drawingModule.draw_landmarks(im
                                             , handLandmarks
                                             , handsModule.HAND_CONNECTIONS
                                             , landmark_drawing_spec=default_drawing_spec
                                             , connection_drawing_spec=connection_drawing_spec)
                if wrist_px:
                    cv2.circle(im, wrist_px, 5, (255, 0, 0), -1)
                if index_finger_tip_px:
                    cv2.circle(im, index_finger_tip_px, 5, (0, 0, 255), -1)
              for point in handsModule.HandLandmark:
                    normalizedLandmark = handLandmarks.landmark[point]
                    pixelCoordinatesLandmark = drawingModule._normalized_to_pixel_coordinates(normalizedLandmark.x, normalizedLandmark.y, 1000, 1000)
                    if point == 8:
                        if pixelCoordinatesLandmark != None:
                            # assign Index axes to variables
                            IndexTipX = pixelCoordinatesLandmark[0]
                            # print('Index X is: ' + str(IndexTipX))
                            IndexTipY = pixelCoordinatesLandmark[1]
                            # print('Index Z is: ' + str())
                            # send Index variables to various OSC messages
                            client.send_message("/control/verb", IndexTipY)
                            client.send_message("/control/bright", IndexTipY)
                            client.send_message("/control/trigRate", IndexTipY)
                            client.send_message("/control/damp", IndexTipX)
                            
                    if point == 4:
                        if pixelCoordinatesLandmark != None:
                            # assign Thumb axes to variables
                            ThumbTipX = pixelCoordinatesLandmark[0]
                            ThumbTipY = pixelCoordinatesLandmark[1]
                            # send Thumb variables to OSC
                            client.send_message("/control/chord", ThumbTipX)
                            client.send_message("/control/inversion", ThumbTipY)


            
           #Below shows the current frame to the desktop 
           window_name = "Frame"
           cv2.namedWindow(window_name, cv2.WINDOW_NORMAL)
           cv2.moveWindow(window_name, screen.x - 1, screen.y - 1)
           cv2.setWindowProperty(window_name, cv2.WND_PROP_FULLSCREEN,
                          cv2.WINDOW_FULLSCREEN)
           cv2.imshow(window_name, im);
           key = cv2.waitKey(1) & 0xFF
        
           #Below states that if the |q| is press on the keyboard it will stop the system
           if key == ord("q"):
              break