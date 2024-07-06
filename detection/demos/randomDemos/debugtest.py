"""
ID: Jayden Chen
LANG: python
TASK: get distance percent through two cameras
"""

import cv2
import mediapipe as mp
import math

#initialize mediapip hands 
mp_drawing = mp.solutions.drawing_utils
mp_drawing_styles = mp.solutions.drawing_styles
mp_hands = mp.solutions.hands

cap1 = cv2.VideoCapture(2) 
cv2.waitKey(1000) #some passing time

#defining some variables
h = 22
alpha = 1135
d = 60

def getdistance(a):

    output = float(int(100000* math.sqrt((a[0][0]-a[1][0])**2 + (a[0][1]-a[1][1])**2)))/100
    return output

def getcamdistance(P):

    #P1 = alpha*H/L1
    #L1 = alpha*H/P1

    output = float(int(100*alpha*h / P))/100
    
    return output

def getdistanceratio(P1,P2):

    L1 = getcamdistance(P1) + d
    L2 = getcamdistance(P2)

    print(L1,L2) 

#print(L1,L2)

    output = float(int(10000* L1/L2))/100
    return output

def getlowestlength(LP1,LP2):
    if len(LP1) < len(LP2):
        return len(LP1)
    else:
        return len(LP2)
    
fout = open('testdata.txt', 'w')

if cap1.isOpened():

    with mp_hands.Hands(
        model_complexity=0,
        min_detection_confidence=0.5,
        min_tracking_confidence = 0.5) as hands:

        cap1.set(cv2.CAP_PROP_FRAME_WIDTH, 720)
        cap1.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)

        print('screen running')

        framenum = 0

        while True:

            framenum += 1

            read_code1, frame1 = cap1.read()

            #to improve performance, make frames as not writeable to pass by reference 
            frame1.flags.writeable = False
            frame1 = cv2.cvtColor(frame1,cv2.COLOR_BGR2RGB)
            results1 = hands.process(frame1)

            allhands = []
            #get lowest and highest pos to get height of hand
            if results1.multi_hand_landmarks:
                for hand_landmarks in results1.multi_hand_landmarks:

                    allhands.append(
                        #apend to allhands the two points
                   [[hand_landmarks.landmark[mp_hands.HandLandmark.WRIST].x,hand_landmarks.landmark[mp_hands.HandLandmark.WRIST].y],
                    #make sure formatting is correct
                    [hand_landmarks.landmark[mp_hands.HandLandmark.MIDDLE_FINGER_TIP].x,hand_landmarks.landmark[mp_hands.HandLandmark.MIDDLE_FINGER_TIP].y]])

            P1 = []
            #get HL1s
            for hand in allhands:
                P1.append(getdistance(hand))

            distances = []
            handnum = 0
            for p1 in P1:
                handnum += 1
                temp = getcamdistance(p1)
                distances.append(temp)
                print(temp,framenum)
                fout.write(str(temp)+" "+str(handnum)+" "+str(framenum))

            #show camera
            #draw the hand annotations on the image
            frame1.flags.writeable = True
            frame1 = cv2.cvtColor(frame1,cv2.COLOR_RGB2BGR)
            
            if results1.multi_hand_landmarks:
                for hand_landmarks in results1.multi_hand_landmarks:
                    mp_drawing.draw_landmarks(
                    frame1,
                    hand_landmarks,
                    mp_hands.HAND_CONNECTIONS,
                    mp_drawing_styles.get_default_hand_landmarks_style(),
                    mp_drawing_styles.get_default_hand_connections_style())

            #cv2.imshow("screen0", frame0) #show frame
            cv2.imshow("screen1", frame1)

            cv2.waitKey(20) #give passing time for no memory overflow
            
print("camera fail to open")
