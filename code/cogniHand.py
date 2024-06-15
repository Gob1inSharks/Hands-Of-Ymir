"""
Name: Cognition
Author: Jayden Chen
Purpose: Determines if Hand Gesture is valid

input: 
    hand_landmarks from mediapipe hands

output: 
    Boolean
    WristToMiddle

remarks:

"""

import math
import mediapipe as mp
import cv2
import numpy as np

#initialize mediapip hands 
mp_drawing = mp.solutions.drawing_utils
mp_drawing_styles = mp.solutions.drawing_styles
mp_hands = mp.solutions.hands

"""
Func: disformula
Author: Jayden Chen
Purpose: gets the distance between two points

input: 
    (x,y) * 2
    
output:
    integer

remarks:
    note 
"""
def disformula(a,b): 

    return math.sqrt((a[0]-b[0])**2 + (a[1]-b[1])**2 )

"""
Func: angleformula
Author: Jayden Chen
Purpose: gets a point's angles from three coordinates

input: 
    (x,y) * 3
    
output:
    int

remarks:
    note that this equation returns in radians, so convert to angle
"""
def angleformula(A,B,C): #gets the angle of a point 
    a = disformula(B,C)
    b = disformula(A,C)
    c = disformula(A,B)
    return 180*math.acos((b**2+c**2-a**2)/(2*b*c))/(math.pi)

"""
Func: radianformula
Author: Jayden Chen
Purpose: gets a point's radian from three coordinates

input: 
    (x,y) * 3
    
output:
    int

remarks:

"""

def angleformulaRadian(A,B,C): 

    a = disformula(B,C)
    b = disformula(A,C) 
    c = disformula(A,B)
    return math.acos((b**2+c**2-a**2)/(2*b*c))

"""
Func: isHand
Author: Jayden Chen
Purpose: determines if the hand gesture is valid or not

input: 
    [WristToThumb,WrsitToIndex,WristToMiddle,WristToRing,WristToPinky,ThumbToIndex,ThumbToRing,ThumbToMiddle,ThumbToPinky][ThumbMcp,ThumbIp,IndexPip,IndexDip,MiddlePip,MiddleDip,RingPip,RingDip,PinkyPip,PinkyDip]

output:
    Boolean

remarks:

"""
def isHand(data):      

    if float(data['ThumbToIndex']) / float(data['ThumbToMiddle']) < 0.2:
        return True
    else:
        return False

"""
Func: CleanDisData
Author: Jayden Chen
Purpose: Translate handmarks into angle and distance data for cognition

input: 
    hand_landmarks
    
output:
    WristToThumb,WrsitToIndex,WristToMiddle,WristToRing,WristToPinky,ThumbToIndex,ThumbToRing,ThumbToMiddle,ThumbToPink,ThumbMcp,ThumbIp,IndexPip,IndexDip,MiddlePip,MiddleDip,RingPip,RingDip,PinkyPip,PinkyDip in a list

remarks:
    note that mediapipe returns a percentage, so you'd have to multiply the percentage by the width and heigh to get accurate measurements
"""
def cleanDisData(hand_landmarks,width,height):

    #format is [WristToThumb,WrsitToIndex,WristToMiddle,WristToRing,WristToPinky,ThumbToIndex,ThumbToRing,ThumbToMiddle,ThumbToPinky][ThumbMcp,ThumbIp,IndexPip,IndexDip,MiddlePip,MiddleDip,RingPip,RingDip,PinkyPip,PinkyDip]
    return [

        #Distance - This gets distance from tips to wrist - for general direction of hand and P1, P2 for twocamdis
         #WristToThumb
        [round(disformula((hand_landmarks.landmark[mp_hands.HandLandmark.WRIST].x*width,             hand_landmarks.landmark[mp_hands.HandLandmark.WRIST].y*height),
                          (hand_landmarks.landmark[mp_hands.HandLandmark.THUMB_TIP].x*width,         hand_landmarks.landmark[mp_hands.HandLandmark.THUMB_TIP].y*height)),2),
         #WristToIndex
         round(disformula((hand_landmarks.landmark[mp_hands.HandLandmark.WRIST].x*width,             hand_landmarks.landmark[mp_hands.HandLandmark.WRIST].y*height),
                          (hand_landmarks.landmark[mp_hands.HandLandmark.INDEX_FINGER_TIP].x*width,  hand_landmarks.landmark[mp_hands.HandLandmark.INDEX_FINGER_TIP].y*height)),2),
         #WristToMiddle
         round(disformula((hand_landmarks.landmark[mp_hands.HandLandmark.WRIST].x*width,             hand_landmarks.landmark[mp_hands.HandLandmark.WRIST].y*height),
                          (hand_landmarks.landmark[mp_hands.HandLandmark.MIDDLE_FINGER_TIP].x*width, hand_landmarks.landmark[mp_hands.HandLandmark.MIDDLE_FINGER_TIP].y)*height),2),
         #WristToRing
         round(disformula((hand_landmarks.landmark[mp_hands.HandLandmark.WRIST].x*width,             hand_landmarks.landmark[mp_hands.HandLandmark.WRIST].y*height),
                          (hand_landmarks.landmark[mp_hands.HandLandmark.RING_FINGER_TIP].x*width,   hand_landmarks.landmark[mp_hands.HandLandmark.RING_FINGER_TIP].y*height)),2),
         #WristToPinky
         round(disformula((hand_landmarks.landmark[mp_hands.HandLandmark.WRIST].x*width,             hand_landmarks.landmark[mp_hands.HandLandmark.WRIST].y*height),
                          (hand_landmarks.landmark[mp_hands.HandLandmark.PINKY_TIP].x*width,         hand_landmarks.landmark[mp_hands.HandLandmark.PINKY_TIP].y*height)),2),
         #ThumbToIndex                 
         round(disformula((hand_landmarks.landmark[mp_hands.HandLandmark.THUMB_TIP].x*width,         hand_landmarks.landmark[mp_hands.HandLandmark.THUMB_TIP].y*height),
                          (hand_landmarks.landmark[mp_hands.HandLandmark.INDEX_FINGER_TIP].x*width,  hand_landmarks.landmark[mp_hands.HandLandmark.INDEX_FINGER_TIP].y*height)),2),           
         #ThumbToMiddle                  
         round(disformula((hand_landmarks.landmark[mp_hands.HandLandmark.THUMB_TIP].x*width,         hand_landmarks.landmark[mp_hands.HandLandmark.THUMB_TIP].y*height),
                          (hand_landmarks.landmark[mp_hands.HandLandmark.MIDDLE_FINGER_TIP].x*width, hand_landmarks.landmark[mp_hands.HandLandmark.MIDDLE_FINGER_TIP].y*height)),2),
         #ThumbToRing                 
         round(disformula((hand_landmarks.landmark[mp_hands.HandLandmark.THUMB_TIP].x*width,         hand_landmarks.landmark[mp_hands.HandLandmark.THUMB_TIP].y*height),
                          (hand_landmarks.landmark[mp_hands.HandLandmark.RING_FINGER_TIP].x*width,   hand_landmarks.landmark[mp_hands.HandLandmark.RING_FINGER_TIP].y*height)),2),
         #ThumbToPinky                 
         round(disformula((hand_landmarks.landmark[mp_hands.HandLandmark.THUMB_TIP].x*width,         hand_landmarks.landmark[mp_hands.HandLandmark.THUMB_TIP].y*height),
                          (hand_landmarks.landmark[mp_hands.HandLandmark.PINKY_TIP].x*width,         hand_landmarks.landmark[mp_hands.HandLandmark.PINKY_TIP].y*height)),2)],

        #Angle - This will give the angles of each finger segment - for hand gestures
         #ThumbMcp
        [round(angleformula((hand_landmarks.landmark[mp_hands.HandLandmark.THUMB_MCP].x*width,         hand_landmarks.landmark[mp_hands.HandLandmark.THUMB_MCP].y*height),
                            (hand_landmarks.landmark[mp_hands.HandLandmark.THUMB_IP].x*width,          hand_landmarks.landmark[mp_hands.HandLandmark.THUMB_IP].y*height),
                            (hand_landmarks.landmark[mp_hands.HandLandmark.THUMB_CMC].x*width,         hand_landmarks.landmark[mp_hands.HandLandmark.THUMB_CMC].y*height)),2),
         #ThumbIp
         round(angleformula((hand_landmarks.landmark[mp_hands.HandLandmark.THUMB_IP].x*width,          hand_landmarks.landmark[mp_hands.HandLandmark.THUMB_IP].y*height),
                            (hand_landmarks.landmark[mp_hands.HandLandmark.THUMB_TIP].x*width,         hand_landmarks.landmark[mp_hands.HandLandmark.THUMB_TIP].y*height),
                            (hand_landmarks.landmark[mp_hands.HandLandmark.THUMB_MCP].x*width,         hand_landmarks.landmark[mp_hands.HandLandmark.THUMB_MCP].y*height)),2),
         #IndexPip
         round(angleformula((hand_landmarks.landmark[mp_hands.HandLandmark.INDEX_FINGER_PIP].x*width,  hand_landmarks.landmark[mp_hands.HandLandmark.INDEX_FINGER_PIP].y*height),
                            (hand_landmarks.landmark[mp_hands.HandLandmark.INDEX_FINGER_DIP].x*width,  hand_landmarks.landmark[mp_hands.HandLandmark.INDEX_FINGER_DIP].y*height),
                            (hand_landmarks.landmark[mp_hands.HandLandmark.INDEX_FINGER_MCP].x*width,  hand_landmarks.landmark[mp_hands.HandLandmark.INDEX_FINGER_MCP].y*height)),2),
         #IndexDip
         round(angleformula((hand_landmarks.landmark[mp_hands.HandLandmark.INDEX_FINGER_DIP].x*width,  hand_landmarks.landmark[mp_hands.HandLandmark.INDEX_FINGER_DIP].y*height),
                            (hand_landmarks.landmark[mp_hands.HandLandmark.INDEX_FINGER_TIP].x*width,  hand_landmarks.landmark[mp_hands.HandLandmark.INDEX_FINGER_TIP].y*height),
                            (hand_landmarks.landmark[mp_hands.HandLandmark.INDEX_FINGER_PIP].x*width,  hand_landmarks.landmark[mp_hands.HandLandmark.INDEX_FINGER_PIP].y*height)),2),
         #MiddlePip
         round(angleformula((hand_landmarks.landmark[mp_hands.HandLandmark.MIDDLE_FINGER_PIP].x*width, hand_landmarks.landmark[mp_hands.HandLandmark.MIDDLE_FINGER_PIP].y*height),
                            (hand_landmarks.landmark[mp_hands.HandLandmark.MIDDLE_FINGER_DIP].x*width, hand_landmarks.landmark[mp_hands.HandLandmark.MIDDLE_FINGER_DIP].y*height),
                            (hand_landmarks.landmark[mp_hands.HandLandmark.MIDDLE_FINGER_MCP].x*width, hand_landmarks.landmark[mp_hands.HandLandmark.MIDDLE_FINGER_MCP].y*height)),2),
         #MiddleDip
         round(angleformula((hand_landmarks.landmark[mp_hands.HandLandmark.MIDDLE_FINGER_DIP].x*width, hand_landmarks.landmark[mp_hands.HandLandmark.MIDDLE_FINGER_DIP].y*height),
                            (hand_landmarks.landmark[mp_hands.HandLandmark.MIDDLE_FINGER_TIP].x*width, hand_landmarks.landmark[mp_hands.HandLandmark.MIDDLE_FINGER_TIP].y*height),
                            (hand_landmarks.landmark[mp_hands.HandLandmark.MIDDLE_FINGER_PIP].x*width, hand_landmarks.landmark[mp_hands.HandLandmark.MIDDLE_FINGER_PIP].y*height)),2),
         #RingPip
         round(angleformula((hand_landmarks.landmark[mp_hands.HandLandmark.RING_FINGER_PIP].x*width,   hand_landmarks.landmark[mp_hands.HandLandmark.RING_FINGER_PIP].y*height),
                            (hand_landmarks.landmark[mp_hands.HandLandmark.RING_FINGER_DIP].x*width,   hand_landmarks.landmark[mp_hands.HandLandmark.RING_FINGER_DIP].y*height),
                            (hand_landmarks.landmark[mp_hands.HandLandmark.RING_FINGER_MCP].x*width,   hand_landmarks.landmark[mp_hands.HandLandmark.RING_FINGER_MCP].y*height)),2),
         #RingDip
         round(angleformula((hand_landmarks.landmark[mp_hands.HandLandmark.RING_FINGER_DIP].x*width,   hand_landmarks.landmark[mp_hands.HandLandmark.RING_FINGER_DIP].y*height),
                            (hand_landmarks.landmark[mp_hands.HandLandmark.RING_FINGER_TIP].x*width,   hand_landmarks.landmark[mp_hands.HandLandmark.RING_FINGER_TIP].y*height),
                            (hand_landmarks.landmark[mp_hands.HandLandmark.RING_FINGER_PIP].x*width,   hand_landmarks.landmark[mp_hands.HandLandmark.RING_FINGER_PIP].y*height)),2),
         #PinkyPip
         round(angleformula((hand_landmarks.landmark[mp_hands.HandLandmark.PINKY_PIP].x*width,         hand_landmarks.landmark[mp_hands.HandLandmark.PINKY_PIP].y*height),
                            (hand_landmarks.landmark[mp_hands.HandLandmark.PINKY_DIP].x*width,         hand_landmarks.landmark[mp_hands.HandLandmark.PINKY_DIP].y*height),
                            (hand_landmarks.landmark[mp_hands.HandLandmark.PINKY_MCP].x*width,         hand_landmarks.landmark[mp_hands.HandLandmark.PINKY_MCP].y*height)),2),
         #PinkyPip
         round(angleformula((hand_landmarks.landmark[mp_hands.HandLandmark.PINKY_DIP].x*width,         hand_landmarks.landmark[mp_hands.HandLandmark.PINKY_DIP].y*height),
                            (hand_landmarks.landmark[mp_hands.HandLandmark.PINKY_TIP].x*width,         hand_landmarks.landmark[mp_hands.HandLandmark.PINKY_TIP].y*height),
                            (hand_landmarks.landmark[mp_hands.HandLandmark.PINKY_PIP].x*width,         hand_landmarks.landmark[mp_hands.HandLandmark.PINKY_PIP].y*height)),2)
        ]]

"""
Func: CleanDisDataDict
Author: Jayden Chen
Purpose: Translate handmarks into angle and distance data for cognition

input: 
    hand_landmarks
    
output:
    WristToThumb,WrsitToIndex,WristToMiddle,WristToRing,WristToPinky,ThumbToIndex,ThumbToRing,ThumbToMiddle,ThumbToPink,ThumbMcp,ThumbIp,IndexPip,IndexDip,MiddlePip,MiddleDip,RingPip,RingDip,PinkyPip,PinkyDip in a dict

remarks:
    dict 
"""
def cleanDisDataDict(hand_landmarks,width,height):

    #format is [WristToThumb,WrsitToIndex,WristToMiddle,WristToRing,WristToPinky,ThumbToIndex,ThumbToRing,ThumbToMiddle,ThumbToPinky][ThumbMcp,ThumbIp,IndexPip,IndexDip,MiddlePip,MiddleDip,RingPip,RingDip,PinkyPip,PinkyDip]
    return {

        #Distance - This gets distance from tips to wrist - for general direction of hand and P1, P2 for twocamdis
         #WristToThumb
         'WristToThumb'  : round(disformula((hand_landmarks.landmark[mp_hands.HandLandmark.WRIST].x*width,             hand_landmarks.landmark[mp_hands.HandLandmark.WRIST].y*height),
                                            (hand_landmarks.landmark[mp_hands.HandLandmark.THUMB_TIP].x*width,         hand_landmarks.landmark[mp_hands.HandLandmark.THUMB_TIP].y*height)),2),
         #WristToIndex
         'WristToIndex'  : round(disformula((hand_landmarks.landmark[mp_hands.HandLandmark.WRIST].x*width,             hand_landmarks.landmark[mp_hands.HandLandmark.WRIST].y*height),
                                            (hand_landmarks.landmark[mp_hands.HandLandmark.INDEX_FINGER_TIP].x*width,  hand_landmarks.landmark[mp_hands.HandLandmark.INDEX_FINGER_TIP].y*height)),2),
         #WristToMiddle
         'WristToMiddle' : round(disformula((hand_landmarks.landmark[mp_hands.HandLandmark.WRIST].x*width,             hand_landmarks.landmark[mp_hands.HandLandmark.WRIST].y*height),
                                            (hand_landmarks.landmark[mp_hands.HandLandmark.MIDDLE_FINGER_TIP].x*width, hand_landmarks.landmark[mp_hands.HandLandmark.MIDDLE_FINGER_TIP].y)*height),2),
         #WristToRing
         'WristToRing'   : round(disformula((hand_landmarks.landmark[mp_hands.HandLandmark.WRIST].x*width,             hand_landmarks.landmark[mp_hands.HandLandmark.WRIST].y*height),
                                            (hand_landmarks.landmark[mp_hands.HandLandmark.RING_FINGER_TIP].x*width,   hand_landmarks.landmark[mp_hands.HandLandmark.RING_FINGER_TIP].y*height)),2),
         #WristToPinky
         'WristToPinky'  : round(disformula((hand_landmarks.landmark[mp_hands.HandLandmark.WRIST].x*width,             hand_landmarks.landmark[mp_hands.HandLandmark.WRIST].y*height),
                                            (hand_landmarks.landmark[mp_hands.HandLandmark.PINKY_TIP].x*width,         hand_landmarks.landmark[mp_hands.HandLandmark.PINKY_TIP].y*height)),2),
         #ThumbToIndex                 
         'ThumbToIndex'  : round(disformula((hand_landmarks.landmark[mp_hands.HandLandmark.THUMB_TIP].x*width,         hand_landmarks.landmark[mp_hands.HandLandmark.THUMB_TIP].y*height),
                                            (hand_landmarks.landmark[mp_hands.HandLandmark.INDEX_FINGER_TIP].x*width,  hand_landmarks.landmark[mp_hands.HandLandmark.INDEX_FINGER_TIP].y*height)),2),           
         #ThumbToMiddle                  
         'ThumbToMiddle' : round(disformula((hand_landmarks.landmark[mp_hands.HandLandmark.THUMB_TIP].x*width,         hand_landmarks.landmark[mp_hands.HandLandmark.THUMB_TIP].y*height),
                                            (hand_landmarks.landmark[mp_hands.HandLandmark.MIDDLE_FINGER_TIP].x*width, hand_landmarks.landmark[mp_hands.HandLandmark.MIDDLE_FINGER_TIP].y*height)),2),
         #ThumbToRing                 
         'ThumbToRing'   : round(disformula((hand_landmarks.landmark[mp_hands.HandLandmark.THUMB_TIP].x*width,         hand_landmarks.landmark[mp_hands.HandLandmark.THUMB_TIP].y*height),
                                            (hand_landmarks.landmark[mp_hands.HandLandmark.RING_FINGER_TIP].x*width,   hand_landmarks.landmark[mp_hands.HandLandmark.RING_FINGER_TIP].y*height)),2),
         #ThumbToPinky                 
         'ThumbToPinky'  : round(disformula((hand_landmarks.landmark[mp_hands.HandLandmark.THUMB_TIP].x*width,         hand_landmarks.landmark[mp_hands.HandLandmark.THUMB_TIP].y*height),
                                            (hand_landmarks.landmark[mp_hands.HandLandmark.PINKY_TIP].x*width,         hand_landmarks.landmark[mp_hands.HandLandmark.PINKY_TIP].y*height)),2),

        #Angle - This will give the angles of each finger segment - for hand gestures
         #ThumbMcp
         'ThumbMcp' : round(angleformula((hand_landmarks.landmark[mp_hands.HandLandmark.THUMB_MCP].x*width,         hand_landmarks.landmark[mp_hands.HandLandmark.THUMB_MCP].y*height),
                                         (hand_landmarks.landmark[mp_hands.HandLandmark.THUMB_IP].x*width,          hand_landmarks.landmark[mp_hands.HandLandmark.THUMB_IP].y*height),
                                         (hand_landmarks.landmark[mp_hands.HandLandmark.THUMB_CMC].x*width,         hand_landmarks.landmark[mp_hands.HandLandmark.THUMB_CMC].y*height)),2),
         #ThumbIp
         'ThumbIp'  : round(angleformula((hand_landmarks.landmark[mp_hands.HandLandmark.THUMB_IP].x*width,          hand_landmarks.landmark[mp_hands.HandLandmark.THUMB_IP].y*height),
                                         (hand_landmarks.landmark[mp_hands.HandLandmark.THUMB_TIP].x*width,         hand_landmarks.landmark[mp_hands.HandLandmark.THUMB_TIP].y*height),
                                         (hand_landmarks.landmark[mp_hands.HandLandmark.THUMB_MCP].x*width,         hand_landmarks.landmark[mp_hands.HandLandmark.THUMB_MCP].y*height)),2),
         #IndexPip
         'IndexPip' : round(angleformula((hand_landmarks.landmark[mp_hands.HandLandmark.INDEX_FINGER_PIP].x*width,  hand_landmarks.landmark[mp_hands.HandLandmark.INDEX_FINGER_PIP].y*height),
                                         (hand_landmarks.landmark[mp_hands.HandLandmark.INDEX_FINGER_DIP].x*width,  hand_landmarks.landmark[mp_hands.HandLandmark.INDEX_FINGER_DIP].y*height),
                                         (hand_landmarks.landmark[mp_hands.HandLandmark.INDEX_FINGER_MCP].x*width,  hand_landmarks.landmark[mp_hands.HandLandmark.INDEX_FINGER_MCP].y*height)),2),
         #IndexDip
         'IndexDip' : round(angleformula((hand_landmarks.landmark[mp_hands.HandLandmark.INDEX_FINGER_DIP].x*width,  hand_landmarks.landmark[mp_hands.HandLandmark.INDEX_FINGER_DIP].y*height),
                                         (hand_landmarks.landmark[mp_hands.HandLandmark.INDEX_FINGER_TIP].x*width,  hand_landmarks.landmark[mp_hands.HandLandmark.INDEX_FINGER_TIP].y*height),
                                         (hand_landmarks.landmark[mp_hands.HandLandmark.INDEX_FINGER_PIP].x*width,  hand_landmarks.landmark[mp_hands.HandLandmark.INDEX_FINGER_PIP].y*height)),2),
         #MiddlePip
         'MiddlePip': round(angleformula((hand_landmarks.landmark[mp_hands.HandLandmark.MIDDLE_FINGER_PIP].x*width, hand_landmarks.landmark[mp_hands.HandLandmark.MIDDLE_FINGER_PIP].y*height),
                                         (hand_landmarks.landmark[mp_hands.HandLandmark.MIDDLE_FINGER_DIP].x*width, hand_landmarks.landmark[mp_hands.HandLandmark.MIDDLE_FINGER_DIP].y*height),
                                         (hand_landmarks.landmark[mp_hands.HandLandmark.MIDDLE_FINGER_MCP].x*width, hand_landmarks.landmark[mp_hands.HandLandmark.MIDDLE_FINGER_MCP].y*height)),2),
         #MiddleDip
         'MiddleDip': round(angleformula((hand_landmarks.landmark[mp_hands.HandLandmark.MIDDLE_FINGER_DIP].x*width, hand_landmarks.landmark[mp_hands.HandLandmark.MIDDLE_FINGER_DIP].y*height),
                                         (hand_landmarks.landmark[mp_hands.HandLandmark.MIDDLE_FINGER_TIP].x*width, hand_landmarks.landmark[mp_hands.HandLandmark.MIDDLE_FINGER_TIP].y*height),
                                         (hand_landmarks.landmark[mp_hands.HandLandmark.MIDDLE_FINGER_PIP].x*width, hand_landmarks.landmark[mp_hands.HandLandmark.MIDDLE_FINGER_PIP].y*height)),2),
         #RingPip
         'RingPip'  : round(angleformula((hand_landmarks.landmark[mp_hands.HandLandmark.RING_FINGER_PIP].x*width,   hand_landmarks.landmark[mp_hands.HandLandmark.RING_FINGER_PIP].y*height),
                                         (hand_landmarks.landmark[mp_hands.HandLandmark.RING_FINGER_DIP].x*width,   hand_landmarks.landmark[mp_hands.HandLandmark.RING_FINGER_DIP].y*height),
                                         (hand_landmarks.landmark[mp_hands.HandLandmark.RING_FINGER_MCP].x*width,   hand_landmarks.landmark[mp_hands.HandLandmark.RING_FINGER_MCP].y*height)),2),
         #RingDip
         'RingDip'  : round(angleformula((hand_landmarks.landmark[mp_hands.HandLandmark.RING_FINGER_DIP].x*width,   hand_landmarks.landmark[mp_hands.HandLandmark.RING_FINGER_DIP].y*height),
                                         (hand_landmarks.landmark[mp_hands.HandLandmark.RING_FINGER_TIP].x*width,   hand_landmarks.landmark[mp_hands.HandLandmark.RING_FINGER_TIP].y*height),
                                         (hand_landmarks.landmark[mp_hands.HandLandmark.RING_FINGER_PIP].x*width,   hand_landmarks.landmark[mp_hands.HandLandmark.RING_FINGER_PIP].y*height)),2),
         #PinkyPip
         'PinkyPip' : round(angleformula((hand_landmarks.landmark[mp_hands.HandLandmark.PINKY_PIP].x*width,         hand_landmarks.landmark[mp_hands.HandLandmark.PINKY_PIP].y*height),
                                         (hand_landmarks.landmark[mp_hands.HandLandmark.PINKY_DIP].x*width,         hand_landmarks.landmark[mp_hands.HandLandmark.PINKY_DIP].y*height),
                                         (hand_landmarks.landmark[mp_hands.HandLandmark.PINKY_MCP].x*width,         hand_landmarks.landmark[mp_hands.HandLandmark.PINKY_MCP].y*height)),2),
         #PinkyDip
         'PinkyDip' : round(angleformula((hand_landmarks.landmark[mp_hands.HandLandmark.PINKY_DIP].x*width,         hand_landmarks.landmark[mp_hands.HandLandmark.PINKY_DIP].y*height),
                                         (hand_landmarks.landmark[mp_hands.HandLandmark.PINKY_TIP].x*width,         hand_landmarks.landmark[mp_hands.HandLandmark.PINKY_TIP].y*height),
                                         (hand_landmarks.landmark[mp_hands.HandLandmark.PINKY_PIP].x*width,         hand_landmarks.landmark[mp_hands.HandLandmark.PINKY_PIP].y*height)),2)}

def handCoordinates2D(hand_landmarks,width,height):
    return {
         'Wrist'  : (round(hand_landmarks.landmark[mp_hands.HandLandmark.WRIST].x*width,2),                  round(hand_landmarks.landmark[mp_hands.HandLandmark.WRIST].y*height),2),
         'Thumb'  : (round(hand_landmarks.landmark[mp_hands.HandLandmark.THUMB_TIP].x*width,2),              round(hand_landmarks.landmark[mp_hands.HandLandmark.THUMB_TIP].y*height,2)),
         'Index'  : (round(hand_landmarks.landmark[mp_hands.HandLandmark.INDEX_FINGER_TIP].x*width,2),       round(hand_landmarks.landmark[mp_hands.HandLandmark.INDEX_FINGER_TIP].y*height),2),
         'Middle' : (round(hand_landmarks.landmark[mp_hands.HandLandmark.MIDDLE_FINGER_TIP].x*width,2),      round(hand_landmarks.landmark[mp_hands.HandLandmark.MIDDLE_FINGER_TIP].y*height),2),
         'Ring'   : (round(hand_landmarks.landmark[mp_hands.HandLandmark.RING_FINGER_TIP].x*width,2),        round(hand_landmarks.landmark[mp_hands.HandLandmark.RING_FINGER_TIP].y*height),2),
         'Pinky'  : (round(hand_landmarks.landmark[mp_hands.HandLandmark.PINKY_TIP].x*width,2),              round(hand_landmarks.landmark[mp_hands.HandLandmark.PINKY_TIP].y*height),2)}


def cleanSideData(hand_landmarks,width):

    return {
        'X-Axis' : round((hand_landmarks.landmark[mp_hands.HandLandmark.WRIST].x*width),2)
    }

"""
Func: cogni
Author: Jayden Chen
Purpose: Returns if hand gesture is recognized
         Formatted for TwoCamDis

input: 
    hand_landmarks, width, height
    
output:
    float, boolean, float

remarks:
    
"""
def cogni(hand_landmarks,width,height):
    return (cleanDisDataDict(hand_landmarks,width,height)['WristToMiddle'],isHand(cleanDisDataDict(hand_landmarks,width,height)),cleanSideData(hand_landmarks,width)['X-Axis'])

def main():

    #test camera number before start
    CAM1 = cv2.VideoCapture(0)
    #change video format for better performance in raspberry pi
    CAM1.set(cv2.CAP_PROP_FOURCC,cv2.VideoWriter_fourcc('M','J','P','G'))
    print("Camera Found!")  

    #get Width and Height for 
    frameWidth = int(CAM1.get(cv2.CAP_PROP_FRAME_WIDTH))
    frameHeight = int(CAM1.get(cv2.CAP_PROP_FRAME_HEIGHT))

    #wait a while
    cv2.waitKey(1000)
 
    if CAM1.isOpened():
        print("Camera Open!")

        with mp_hands.Hands(
            model_complexity=0,
            min_detection_confidence=0.5,
            min_tracking_confidence=0.5) as hands:
                
            print("Mediapipe Running!")

            #wait a while
            cv2.waitKey(1000)

            while True:

                #get frame and success
                read_code1, frame1 = CAM1.read()

                #if Frame is successful
                if read_code1:

                    # To improve performance, mark frames as not writeable to pass by reference
                    frame1.flags.writeable = False
                    frame1 = cv2.cvtColor(frame1,cv2.COLOR_BGR2RGB)
                    results1 = hands.process(frame1)

                    #if mediapipe is successful
                    if results1.multi_hand_landmarks:

                        print('hand is found')

                        handnum = 0
                        #for all hands detected
                        for hand_landmarks1 in results1.multi_hand_landmarks:
                            #print('wa ho')
                            handnum += 1
                            print(cleanDisDataDict(hand_landmarks1,frameWidth,frameHeight))
                            print(cleanSideData(hand_landmarks1,frameWidth))
                            print(cogni(hand_landmarks1,frameWidth,frameHeight))                

                    else:
                        print('hand not found')

                    #mark frames as writeable for visual
                    frame1.flags.writeable = True
                    frame1 = cv2.cvtColor(frame1,cv2.COLOR_RGB2BGR)

                    #if mediapipe is successful
                    if results1.multi_hand_landmarks:
                        #for hands detected
                        for hand_landmarks in results1.multi_hand_landmarks:
                            #draw hand landmarks on image
                            mp_drawing.draw_landmarks(
                            frame1,
                            hand_landmarks,
                            mp_hands.HAND_CONNECTIONS,
                            mp_drawing_styles.get_default_hand_landmarks_style(),
                            mp_drawing_styles.get_default_hand_connections_style())
                
                    #cv2.imshow("screen0", frame0) 
                    #show visual
                    cv2.imshow("screen1", frame1)
                else:
                    print('frame not found')

                #if esc key is pressed, break
                if cv2.waitKey(33) == 27:
                        break
                
    #close camera and window for 'eleganto' ending
    CAM1.release()
    cv2.destroyAllWindows

if __name__ == '__main__':
    main()
