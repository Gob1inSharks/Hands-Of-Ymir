"""
ID: Jayden Chen
LANG: python
TASK: get distance percent through one camera
"""
#405 = alpha * H/L1 H = 18, L1 = 50. alpha = 1125
#830 . alpha = 1135
#680 
import cv2
import mediapipe as mp
import math

#initialize mediapip hands 
mp_drawing = mp.solutions.drawing_utils
mp_drawing_styles = mp.solutions.drawing_styles
mp_hands = mp.solutions.hands

cap = cv2.VideoCapture(0) #change number if wrong camera
cv2.waitKey(1000) #some passing time

def getdistance(a):

    output = float(int(100000*math.sqrt((a[0][0]-a[1][0])**2 + (a[0][1]-a[1][1])**2)))/100
    return output

alpha = 1

def getdistanceratio(a):

    output = a / alpha
    return output
    
fout = open('testdata.txt', 'w')

if cap.isOpened():

    with mp_hands.Hands(
        model_complexity=0,
        min_detection_confidence=0.5,
        min_tracking_confidence = 0.5) as hands:

        cap.set(cv2.CAP_PROP_FRAME_WIDTH, 720)
        cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)

        print('screen1 running')

        framenum = 0

        while True:

            framenum += 1

            read_code, frame = cap.read()

            #to improve performance, make frames as not writeable to pass by reference 
            frame.flags.writeable = False
            frame = cv2.cvtColor(frame,cv2.COLOR_BGR2RGB)
            results = hands.process(frame)


            allhands = []
            #get lowest and highest pos to get height of hand
            if results.multi_hand_landmarks:
                for hand_landmarks in results.multi_hand_landmarks:

                    allhands.append(
                        #apend to allhands the two points
                   [[hand_landmarks.landmark[mp_hands.HandLandmark.WRIST].x,hand_landmarks.landmark[mp_hands.HandLandmark.WRIST].y],
                    #make sure formatting is correct
                    [hand_landmarks.landmark[mp_hands.HandLandmark.MIDDLE_FINGER_TIP].x,hand_landmarks.landmark[mp_hands.HandLandmark.MIDDLE_FINGER_TIP].y]])

            HL1 = []
            #get HL1s
            for hand in allhands:
                #print(hand)
                HL1.append(getdistance(hand))

            #get ratios
            distanceratios = []
            handnum = 0
            for hl1 in HL1:
                handnum += 1
                distanceratios.append(getdistanceratio(hl1))
                print("hand no.",handnum," D-percentage is ",distanceratios[handnum-1]," at frame: ",framenum)

                fout.write(str(handnum)+" "+str(distanceratios[handnum-1])+" "+str(framenum)+'\n')
            
            #draw the hand annotations on the image
            frame.flags.writeable = True
            frame = cv2.cvtColor(frame,cv2.COLOR_RGB2BGR)
            
            if results.multi_hand_landmarks:
                for hand_landmarks in results.multi_hand_landmarks:
                    mp_drawing.draw_landmarks(
                    frame,
                    hand_landmarks,
                    mp_hands.HAND_CONNECTIONS,
                    mp_drawing_styles.get_default_hand_landmarks_style(),
                    mp_drawing_styles.get_default_hand_connections_style())

            #cv2.imshow("screen0", frame0) #show frame
            cv2.imshow("screen", frame)

            cv2.waitKey(33) #give passing time for memory (33 milisecs means 30fps, 1000/30 = 33.33333333333336)
