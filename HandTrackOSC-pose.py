#Import the necessary Packages for this software to run
import mediapipe
import os
import cv2
from picamera2 import Picamera2
from libcamera import controls
import screeninfo
from pythonosc import udp_client


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
poseModule = mediapipe.solutions.pose



#Add confidence values and extra settings to MediaPipe hand tracking. As we are using a live video stream this is not a static
#image mode, confidence values in regards to overall detection and tracking and we will only let two hands be tracked at the same time
#More hands can be tracked at the same time if desired but will slow down the system
with poseModule.Pose(static_image_mode=False, min_detection_confidence=0.7, min_tracking_confidence=0.7) as pose:

#Create an infinite loop which will produce the live feed to our desktop and that will search for hands
     while True:
           im = picam2.capture_array()
           #Unedit the below line if your live feed is produced upsidedown
           im = cv2.flip(im, flipCode = 0)
           
           
           #produces the hand framework overlay ontop of the hand, you can choose the colour here too)
           results = pose.process(cv2.cvtColor(im, cv2.COLOR_BGR2RGB))
           
           #Incase the system sees multiple hands this if statment deals with that and produces another hand overlay
           if results.pose_landmarks:
              
                              ## Block to change colors of specific points
              left_drawing_spec = drawingModule.DrawingSpec(color=(0, 0, 255), thickness=5, circle_radius=5)  # Red left
              default_drawing_spec = drawingModule.DrawingSpec(color=(255, 255, 255), thickness=2, circle_radius=2)  # Green others
              connection_drawing_spec = drawingModule.DrawingSpec(color=(255, 255, 255), thickness=1)
              image_height, image_width, _ = im.shape
              right_index = results.pose_landmarks.landmark[poseModule.PoseLandmark.RIGHT_INDEX]
              left_index = results.pose_landmarks.landmark[poseModule.PoseLandmark.LEFT_INDEX]
              right_index_px = mediapipe.solutions.drawing_utils._normalized_to_pixel_coordinates(right_index.x, right_index.y, image_width, image_height)
              left_index_px = mediapipe.solutions.drawing_utils._normalized_to_pixel_coordinates(left_index.x, left_index.y, image_width, image_height)
              
              drawingModule.draw_landmarks(im, 
                                           results.pose_landmarks, 
                                           poseModule.POSE_CONNECTIONS,
                                           landmark_drawing_spec=default_drawing_spec,
                                           connection_drawing_spec=connection_drawing_spec)
  
              
              

              x_right_index = int(right_index.x * 1000)
              y_right_index = int(right_index.y * 1000)
              x_left_index = int(left_index.x * 1000)
              y_left_index = int(left_index.y * 1000)

                
              if right_index_px:
                    cv2.circle(im, right_index_px, 20, (255, 0, 0), -1)
              if left_index_px:
                    cv2.circle(im, left_index_px, 20, (0, 0, 255), -1)

              client.send_message("/control/verb", y_left_index)
              client.send_message("/control/bright", y_left_index)
              client.send_message("/control/damp", x_left_index)
              client.send_message("/control/chord", x_right_index)
              client.send_message("/control/inversion", y_right_index)
              client.send_message("/control/trigRate", y_right_index)
                            
            
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