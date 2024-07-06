"""
Name: run
Author: Jayden Chen
Purpose: to run the mediapipe hand detection script
    
"""

from detection.cogniHand import handCoordinates2D

import os
import cv2
import numpy as np
import math
import random

import mediapipe as mp
from mediapipe.tasks import python
from mediapipe.tasks.python import vision

from paho.mqtt import client as mqtt_client

#initialize mediapip hands 
mp_drawing = mp.solutions.drawing_utils
mp_drawing_styles = mp.solutions.drawing_styles
mp_hands = mp.solutions.hands

#global constants for mediapipe hands
MODEL_COMPLEXITY=0
MINIMUM_DETECTION_CONFIDENCE=0.5
MINIMUM_TRACKING_CONFIDENCE=0.5

CAMERA_PORT = 0

#global constants for mqtt
BROKER = 'broker.emqx.io'
PORT = 1883
SUBSCRIBE_TOPIC = "goblinsharks_hands/test"
PUBLISH_TOPIC = "goblinsharks_hands/test"
CLIENT_ID = f'python-mqtt-{random.randint(0, 1000)}'

def on_connect(client, userdata, flags, rc):
    if rc == 0:
        print("Connected to MQTT Broker!")
    else:
        print("Failed to connect, return code %d\n", rc)

client = mqtt_client.Client(CLIENT_ID)
client.on_connect = on_connect
client.connect(BROKER, PORT)
client.loop_start()

#wait a while to make sure mqtt is open
cv2.waitKey(2000)

def sendMessage(finger,msg):

    #clean message
    msg = msg[finger]
    msg = str(msg[0])+','+str(msg[1])

    #publish message to topic
    result = client.publish(PUBLISH_TOPIC, msg)

    return result

def main():

    #test camera number before start
    CAM = cv2.VideoCapture(CAMERA_PORT)
    #change video format for better performance if needed
    #CAM.set(cv2.CAP_PROP_FOURCC,cv2.VideoWriter_fourcc('M','J','P','G'))

    #get Width and Height for 
    CAMERA_WIDTH = int(CAM.get(cv2.CAP_PROP_FRAME_WIDTH))
    CAMERA_HEIGHT= int(CAM.get(cv2.CAP_PROP_FRAME_HEIGHT))
    #wait a while to make sure camera is open
    cv2.waitKey(1000)
    print("Camera Present!")

    if CAM.isOpened():

        with mp_hands.Hands(
            model_complexity=MODEL_COMPLEXITY,
            min_detection_confidence=MINIMUM_DETECTION_CONFIDENCE,
            min_tracking_confidence=MINIMUM_TRACKING_CONFIDENCE) as hands:
        
            while True:

                #get frame and success
                read_code, frame = CAM.read()
                #if frame is not dropped

                if read_code:

                    # To improve performance, mark frames as not writeable to pass by reference
                    frame.flags.writeable = False
                    frame = cv2.cvtColor(frame,cv2.COLOR_BGR2RGB)
                    results = hands.process(frame)

                    #if mediapipe is successful
                    if results.multi_hand_landmarks:

                        #print('hand is found') #here for debugging

                        handNum = 0
                        for hand_landmarks in results.multi_hand_landmarks:

                            handNum += 1
                            
                            #input 1 as width,height for percentages
                            cleanedData = handCoordinates2D(hand_landmarks,1,1)

                            sendMessage('Index',cleanedData)                        

                #if esc key is pressed, break
                if cv2.waitKey(100) == 27:
                    CAM.release()
                    cv2.destroyAllWindows
                    break

if __name__ == '__main__':
    main()