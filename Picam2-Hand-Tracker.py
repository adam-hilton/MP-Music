#Import the necessary Packages for this software to run
# from sklearn import preprocessing
import mediapipe
import cv2
from picamera2 import Picamera2
import mido

#Configuring picam2 stream

picam2 = Picamera2()
picam2.preview_configuration.main.size = (720,480)
picam2.preview_configuration.main.format = "RGB888"
picam2.preview_configuration.align()
picam2.configure("preview")

#startpicam2 stream
picam2.start()

# set port to pisound DIN5
port = mido.open_output('pisound MIDI PS-1MJPEPE')

#Use MediaPipe to draw the hand framework over the top of hands it identifies in Real-Time
drawingModule = mediapipe.solutions.drawing_utils
handsModule = mediapipe.solutions.hands

# function to scale ouput to readable midi values

def mapToNote(value, min_value, max_value, min_result, max_result):
 
 midiValue = min_result + (value - min_value)/(max_value - min_value)*(max_result - min_result)
 return midiValue

min_value = 0
max_value = 720
min_result = 50
max_result = 80

def mapToVel(value2, min_value2, max_value2, min_resul2, max_result2):
    velValue = min_result2 + (value2 - min_value2)/(max_value2 - min_value2)*(max_result2 - min_result2)
    return velValue

min_value2 = 0
max_value2 = 480
min_result2 = 127
max_result2 = 0

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
                    pixelCoordinatesLandmark= drawingModule._normalized_to_pixel_coordinates(normalizedLandmark.x, normalizedLandmark.y, 720, 480)
                    if point == 8:
                        if pixelCoordinatesLandmark != None:
                            IndexTipX = pixelCoordinatesLandmark[0]
                            noteVar = int(mapToNote(IndexTipX, min_value, max_value, min_result, max_result))
                            # print(noteVar)
                            IndexTipY = pixelCoordinatesLandmark[1]
                            velVar = int(mapToVel(IndexTipY, min_value2, max_value2, min_result2, max_result2))
                            # print(velVar)
                            noteOnMsg = mido.Message('note_on', channel=midiChannel, note=noteVar, velocity=velVar)
                            noteOffMsg = mido.Message('note_off', channel=midiChannel, note=noteVar)
                            port.send(noteOnMsg)
                            port.send(noteOffMsg)
            

            
           #Below shows the current frame to the desktop 
        #    cv2.namedWindow("foo", cv2.WINDOW_NORMAL)
        #    cv2.setWindowProperty("foo", cv2.WND_PROP_FULLSCREEN, cv2.WINDOW_FULLSCREEN)
           cv2.imshow("Frame", im);
           key = cv2.waitKey(1) & 0xFF
        
           #Below states that if the |q| is press on the keyboard it will stop the system
           if key == ord("q"):
              break