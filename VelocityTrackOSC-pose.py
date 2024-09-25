#Import the necessary Packages for this software to run
# from sklearn import preprocessing
import mediapipe
import os
import cv2
from picamera2 import Picamera2
# import mido
from libcamera import controls
import screeninfo
from pythonosc import udp_client
import time

# # Set the environment for framebuffer -- to access later for headless mode
# os.putenv('SDL_FBDEV', '/dev/fb0')  # Framebuffer device
# os.putenv('SDL_VIDEODRIVER', 'fbcon')  # Use framebuffer console
# os.putenv('SDL_NOMOUSE', '1')  # Disable mouse cursor


# get size of screen
screen = screeninfo.get_monitors()[0]

# setup OSC client
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

# set port to pisound DIN5
# port = mido.open_output('pisound MIDI PS-1MJPEPE')

#Use MediaPipe to draw the hand framework over the top of hands it identifies in Real-Time
drawingModule = mediapipe.solutions.drawing_utils
poseModule = mediapipe.solutions.pose

# define initial 'Previous' position
PosPrev = 0

# define loop interval
time_interval = .05

OSCVal = 1

# function to scale ouput to readable midi values

def mapToVel(value, min_value, max_value, min_result, max_result):
    clamped_vel = max(min_value, min(value, 1000))
    velValue = min_result + (clamped_vel - min_value)/(max_value - min_value)*(max_result - min_result)
    return velValue

min_value = -1000
max_value = 1000
min_result = -2
max_result = 2


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
           
            if results.pose_landmarks:

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
                                           connection_drawing_spec=connection_drawing_spec
                                           )
  
              right_index = results.pose_landmarks.landmark[poseModule.PoseLandmark.RIGHT_INDEX]
              left_index = results.pose_landmarks.landmark[poseModule.PoseLandmark.LEFT_INDEX]

              x_right_index = int(right_index.x * 720)
              x_left_index = int(left_index.x * 720)

              if right_index_px:
                    cv2.circle(im, right_index_px, 5, (255, 255, 255), -1)
              if left_index_px:
                    cv2.circle(im, left_index_px, 20, (0, 0, 255), -1)
              
              # print(f"Left index x-coordinate: {x_left_index}")

              # for poseLandmarks in results.pose_landmarks.landmark:
                # for point in poseModule.PoseLandmark:
                    # normalizedLandmark = poseLandmarks[0][0]
                    # pixelCoordinatesLandmark= drawingModule._normalized_to_pixel_coordinates(normalizedLandmark.x, normalizedLandmark.y, 720, 576)
                    # if point == 8 and pixelCoordinatesLandmark != None:
              if 0 <= left_index.x <=1 and 0<= left_index.y <= 1:
                PosNew = x_left_index
                
                vel = (PosNew - PosPrev)/time_interval

                OSCVal = mapToVel(vel, min_value, max_value, min_result, max_result)

                print(OSCVal)
                print(f"Right index x-coordinate: {x_left_index}")
                client.send_message("/control/freq", OSCVal)

                PosPrev = PosNew
                # if results.multi_hand_landmarks is None:
                #         # print('No hand in frame')
              else: client.send_message("/control/freq", 1)
                            

            
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
            #   port.close()
            #   if port.closed:
            #       print("port closed.")
              break