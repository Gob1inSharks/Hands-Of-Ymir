import mediapipe as mp
from mediapipe.tasks import python
from mediapipe.tasks.python import vision

from clients import ClientUDP
from clients import MQTTClient

import _config as global_vars

import math
import cv2
import threading
import time

#initialize mp mediapipe hands
mp_drawing = mp.solutions.drawing_utils
mp_drawing_styles = mp.solutions.drawing_styles
mp_hands = mp.solutions.hands


# the capture thread captures images from the WebCam on a separate thread (for performance)
class Capture(threading.Thread):

    def run(self):
        self.capture()

    def __init__(self) -> None:

        threading.Thread.__init__(self)

        self.CAMERA_INDEX = global_vars.INDEX
        self.CAMERA_HEIGHT = global_vars.HEIGHT
        self.CAMERA_WIDTH = global_vars.WIDTH
        self.CAMERA_FPS = global_vars.FPS

        self.isRunning = False
        self.CAM = None
        self.frame = None
        self.read_code = None

        pass

    def capture(self):
 
        self.CAM = cv2.VideoCapture(self.CAMERA_INDEX)
        cv2.waitKey(500)

        self.isRunning = True
        while True:

            #get frame and success
            read_code, frame = self.CAM.read()

            self.read_code = read_code

            #if frame is not dropped
            if read_code:

                # To improve performance, mark frames as not writeable to pass by reference
                frame.flags.writeable = False
                frame = cv2.cvtColor(frame,cv2.COLOR_BGR2RGB)
                frame = cv2.flip(frame, 1)

                self.frame = frame

            if self.isRunning == False:
                self.CAM.release()
                break

class Hands(threading.Thread):

    def run(self):

        self.capture.start()
        self.client.start()

        self.process()

    def __init__(self,save = False) -> None:
        
        threading.Thread.__init__(self)

        self.waitTime = 1000//(2*global_vars.FPS)
 
        self.results = None
        self.handNumber = 0
        self.coordinates = None

        self.mqttClient = MQTTClient(global_vars.BROKER,global_vars.PORT,global_vars.PUBLISH_TOPIC)
        self.socketClient = ClientUDP(global_vars.IP,global_vars.PORT)
        self.capture = Capture()

        self.save = save

    def process(self):

        cv2.waitKey(5000)

        with mp_hands.Hands(
            model_complexity         = global_vars.MODEL_COMPLEXITY,
            min_detection_confidence = global_vars.MINIMUM_DETECTION_CONFIDENCE,
            min_tracking_confidence  = global_vars.MINIMUM_TRACKING_CONFIDENCE ) as hands:

            while (not self.capture.isRunning):
                print('waiting for capture to start')
                cv2.waitKey(1000)
            print("beginning capture")

            while self.capture.CAM.isOpened():

                read_code = self.capture.read_code
                frame = self.capture.frame

                if read_code:

                    try: #do a try because frame may be an array of None values #todo: fix this

                        self.results = hands.process(frame)

                        if self.results.multi_hand_landmarks:

                            self.handNumber = 0
                            for hand_landmarks in self.results.multi_hand_landmarks:

                                self.handNumber += 1
                            
                                #input 1 as width,height for percentages
                                self.coordinates = IndexToThumbCoordinates3D(hand_landmarks,1,1)

                                print(self.coordinates)
                                self.sendMessage(self.coordinates)
                    
                        self.show(frame,save = self.save) #put show in new thread #todo

                    except:
                        pass

                if cv2.waitKey(self.waitTime) == 27:
                    self.quit()
                    break

    def quit(self):

        self.capture.isRunning = False
        self.client.disconnect()
        cv2.destroyAllWindows

        print("quitting")

        #give some time for mqtt to disconnect
        cv2.waitKey(2000)

    def show(self,frame,save = False,filename = None):

        #mark frames as writeable for annotations
        frame.flags.writeable = True
        frame = cv2.cvtColor(frame,cv2.COLOR_RGB2BGR)

        if self.results.multi_hand_landmarks:

            for hand_landmarks in self.results.multi_hand_landmarks:
                #draw hand landmarks on image
                mp_drawing.draw_landmarks(
                frame,
                hand_landmarks,
                mp_hands.HAND_CONNECTIONS,
                mp_drawing_styles.get_default_hand_landmarks_style(),
                mp_drawing_styles.get_default_hand_connections_style())

        cv2.imshow("screen", frame) 

        if save:
            if filename is None:
                filename = "temp/capture_" + str(time.time()) + ".png"
            cv2.imwrite(filename,frame)

    def sendMessage(self,message):

        message = str(message[0]) + "," + str(message[1]) + "," + str(message[2])

        self.client.sendMessage(message)

def IndexToThumbCoordinates3D(hand_landmarks,width,height):
    """
    Calculates the 2D coordinates of the index finger, and the z axis coordinate of the index tip relative to the thumb tip.
    
    Args:
        hand_landmarks: The detected hand landmarks.
        width: The width of the image or frame.
        height: The height of the image or frame.
    
    Returns:
        A 3d list containing the X-axis, Y-axis, and Z-axis
    """

    def distanceBetween(a,b): 
        return math.sqrt((a[0]-b[0])**2 + (a[1]-b[1])**2 )

    return [round(hand_landmarks.landmark[mp_hands.HandLandmark.INDEX_FINGER_TIP].x*width,4),
            round(hand_landmarks.landmark[mp_hands.HandLandmark.INDEX_FINGER_TIP].y*height,4),
            round(distanceBetween([hand_landmarks.landmark[mp_hands.HandLandmark.INDEX_FINGER_TIP].x*width,
                                      hand_landmarks.landmark[mp_hands.HandLandmark.INDEX_FINGER_TIP].y*height],
                                     [hand_landmarks.landmark[mp_hands.HandLandmark.THUMB_TIP].x*width,             
                                      hand_landmarks.landmark[mp_hands.HandLandmark.THUMB_TIP].y*height]),4)]

