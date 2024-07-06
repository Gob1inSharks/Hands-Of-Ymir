import cv2
import math
import mediapipe as mp

def getdistance(a,b): #gets distance between two points

    return math.sqrt((a[0]-b[0])**2 + (a[1]-b[1])**2 )

def getratio(a,b): # gets ratio
    
    return a/b

L = 30
'''
def f(x):
    return 0.8* (2)**(-x/L) + 1
def rf(p):
    if p == 1:
        p = 0.0001
    elif p < 1:
        return "error"
    return -L * math.log((p - 1)/0.8 , 2)
'''

#initialize mediapip hands 
mp_drawing = mp.solutions.drawing_utils
mp_drawing_styles = mp.solutions.drawing_styles
mp_hands = mp.solutions.hands

print('starting')
#get cameras

CAM1 = cv2.VideoCapture(1)
CAM2 = cv2.VideoCapture(2)
print("Camera Found!")

#wait a while
cv2.waitKey(1000)

fout = open('text.txt','w')

if CAM1.isOpened():
    if CAM2.isOpened():
        print("Camera Open!")

        CAM1.set(cv2.CAP_PROP_FRAME_WIDTH, 720)
        CAM1.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)
        CAM2.set(cv2.CAP_PROP_FRAME_WIDTH, 720)
        CAM2.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)

        with mp_hands.Hands(
            model_complexity=0,
            min_detection_confidence=0.5,
            min_tracking_confidence=0.5) as hands:

            print("Mediapipe Running!")

            while True:

                R1 = []
                R2 = []
                P1 = []
                P2 = []
                P = []
                d = []

                #read_code0, frame0 = cap0.read() #get frame and success
                read_code1, frame1 = CAM1.read()
                read_code2, frame2 = CAM2.read()

                # To improve performance, mark frames as not writeable to pass by reference
                frame1.flags.writeable = False
                frame1 = cv2.cvtColor(frame1,cv2.COLOR_BGR2RGB)
                results1 = hands.process(frame1)

                frame2.flags.writeable = False
                frame2 = cv2.cvtColor(frame2,cv2.COLOR_BGR2RGB)
                results2 = hands.process(frame2)


                if results1.multi_hand_landmarks:
                    
                    for hand_landmarks in results1.multi_hand_landmarks:
                        R1.append([
                            
                            [hand_landmarks.landmark[mp_hands.HandLandmark.WRIST].x,
                             hand_landmarks.landmark[mp_hands.HandLandmark.WRIST].y,],
                            
                            [hand_landmarks.landmark[mp_hands.HandLandmark.MIDDLE_FINGER_TIP].x,
                             hand_landmarks.landmark[mp_hands.HandLandmark.MIDDLE_FINGER_TIP].y,]
                        ])

                if results2.multi_hand_landmarks:
                    
                    for hand_landmarks in results2.multi_hand_landmarks:
                        R2.append([
                            
                              [hand_landmarks.landmark[mp_hands.HandLandmark.WRIST].x,
                               hand_landmarks.landmark[mp_hands.HandLandmark.WRIST].y,],
                              
                              [hand_landmarks.landmark[mp_hands.HandLandmark.MIDDLE_FINGER_TIP].x,
                               hand_landmarks.landmark[mp_hands.HandLandmark.MIDDLE_FINGER_TIP].y]
                        ])

                if R1 != [] and R2 != []:
                    P1.append(getdistance(R1[0][0],R1[0][1]))
                    P2.append(getdistance(R2[0][0],R2[0][1]))
                    print("CAM1:",P1[0],R1[0])
                    print("CAM2:",P2[0],R2[0])

                    P.append(getratio(P1[0],P2[0]))
                    print("P Value:",P)

                    #print("distance: ", rf(P[0]))

                    fout.write(str(P[0]))
                
                #draw the hand annotations on the image
                frame1.flags.writeable = True
                frame1 = cv2.cvtColor(frame1,cv2.COLOR_RGB2BGR)

                frame2.flags.writeable = True
                frame2 = cv2.cvtColor(frame2,cv2.COLOR_RGB2BGR)

                if results1.multi_hand_landmarks:
                    for hand_landmarks in results1.multi_hand_landmarks:
                        mp_drawing.draw_landmarks(
                        frame1,
                        hand_landmarks,
                        mp_hands.HAND_CONNECTIONS,
                        mp_drawing_styles.get_default_hand_landmarks_style(),
                        mp_drawing_styles.get_default_hand_connections_style())

                if results2.multi_hand_landmarks:
                    for hand_landmarks in results2.multi_hand_landmarks:
                        mp_drawing.draw_landmarks(
                        frame2,
                        hand_landmarks,
                        mp_hands.HAND_CONNECTIONS,
                        mp_drawing_styles.get_default_hand_landmarks_style(),
                        mp_drawing_styles.get_default_hand_connections_style())
                
                #cv2.imshow("screen0", frame0) #show frame
                cv2.imshow("screen1", frame1)
                cv2.imshow("screen2", frame2)

                cv2.waitKey(60) #give passing time 
