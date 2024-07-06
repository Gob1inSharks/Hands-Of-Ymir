import cv2
import math
import mediapipe as mp

#initialize mediapip hands 
mp_drawing = mp.solutions.drawing_utils
mp_drawing_styles = mp.solutions.drawing_styles
mp_hands = mp.solutions.hands

def getdirection(a,b): # gets the angle between two points for image recognition #needs editing
    direction = 0

    for x in a: #check if points are valid
        for y in b:
            if x == 0 or y == 0:
                return direction

    points = [[int(1000*a[0]),int(1000*a[1])],[int(1000*b[0]),int(1000*b[1])]] #create int points

    #get slope
    if points[0][1]-points[1][1] != 0:
        slope = float((points[0][0]-points[1][0])/(points[0][1]-points[1][1]))
    else:
        slope = 0

    #get tan-1 & angle
    pAngle = math.degrees(math.atan(slope))      
    #print(pAngle)
    
    return direction

def getdistance(a,b): #gets distance between two points

    for x in a: #check if points are valid
        for y in b:
            if x == 0 or y == 0:
                return int(0)

    p = [[int(10000*a[0]),int(10000*a[1])],[int(10000*b[0]),int(10000*b[1])]] #create int points

    distance = p[0][1] - p[1][1]

    return distance
    
def getratio(a,b,c): # gets the ratio of two camera's height
    
    if a == 0 or b == 0:
        return int(0)

    
    ratio = int(c*100*(a/b))
    
    return ratio

def getdistancepercentage(a,b):

    if a == 0 or b == 0:
        return int(0)

    if a < (100 - b):
        a = 100-b
    elif a > (100+b):
        a = 100+b

    percentage = 100*(a-100+b) / (2*b)
    return percentage

#get two cameras
cap0 = cv2.VideoCapture(0) #find laptop camera and exclude it
cap1 = cv2.VideoCapture(1)
cap2 = cv2.VideoCapture(2)

cv2.waitKey(1000) #some passing time


if cap0.isOpened():
    if cap1.isOpened():
        if cap2.isOpened():

            with mp_hands.Hands(
                model_complexity=0,
                min_detection_confidence=0.5,
                min_tracking_confidence=0.5) as hands:

                #set frame settings. settings are 480p 3:2 
                cap0.set(cv2.CAP_PROP_FRAME_WIDTH, 720)
                cap0.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)
                cap1.set(cv2.CAP_PROP_FRAME_WIDTH, 720)
                cap1.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)
                cap2.set(cv2.CAP_PROP_FRAME_WIDTH, 720)
                cap2.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)

                print('screenrunning')

                framenum = 0
                
                while True: #show image on repeat to get video
                    
                    #read_code0, frame0 = cap0.read() #get frame and success
                    read_code1, frame1 = cap0.read()
                    read_code2, frame2 = cap2.read()

                    # To improve performance, mark frames as not writeable to pass by reference
                    frame1.flags.writeable = False
                    frame1 = cv2.cvtColor(frame1,cv2.COLOR_BGR2RGB)
                    results1 = hands.process(frame1)

                    frame2.flags.writeable = False
                    frame2 = cv2.cvtColor(frame2,cv2.COLOR_BGR2RGB)
                    results2 = hands.process(frame2)

                    framenum += 1
                    #get needed points and find ratio
                    if results1.multi_hand_landmarks:
                        ap = []
                        bp = []
                        for hand_landmarks in results1.multi_hand_landmarks:
                            ap.append(
                               [[hand_landmarks.landmark[mp_hands.HandLandmark.WRIST].x,
                                 hand_landmarks.landmark[mp_hands.HandLandmark.WRIST].y,
                                 hand_landmarks.landmark[mp_hands.HandLandmark.WRIST].z],
                                [hand_landmarks.landmark[mp_hands.HandLandmark.MIDDLE_FINGER_TIP].x,
                                 hand_landmarks.landmark[mp_hands.HandLandmark.MIDDLE_FINGER_TIP].y,
                                 hand_landmarks.landmark[mp_hands.HandLandmark.MIDDLE_FINGER_TIP].z]])

                        distance1 = []
                        for i in range(0,len(ap)):
                            distance1.append(getratio(getdistance(ap[i][0],ap[i][1]),720,10000))

                        if results2.multi_hand_landmarks:
                            for hand_landmarks in results2.multi_hand_landmarks:
                                bp.append(
                                     [[hand_landmarks.landmark[mp_hands.HandLandmark.WRIST].x,
                                       hand_landmarks.landmark[mp_hands.HandLandmark.WRIST].y,
                                       hand_landmarks.landmark[mp_hands.HandLandmark.WRIST].z],
                                      [hand_landmarks.landmark[mp_hands.HandLandmark.MIDDLE_FINGER_TIP].x,
                                       hand_landmarks.landmark[mp_hands.HandLandmark.MIDDLE_FINGER_TIP].y,
                                       hand_landmarks.landmark[mp_hands.HandLandmark.MIDDLE_FINGER_TIP].z]])

                            distance2 = []
                            for i in range(0,len(bp)):
                                distance2.append(getratio(getdistance(bp[i][0],bp[i][1]),720,10000))

                            if len(distance1) > len(distance2):
                                z = len(distance2)
                            else:
                                z = len(distance1)
                            for i in range(0,z):
                                twocamratio = float( getratio(distance1[i],distance2[i],10000) /10000)
                                print(distance1,distance2,twocamratio,framenum)

                            percentage = getdistancepercentage(twocamratio,20)
                            print(percentage)
                            
                            
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

                    cv2.waitKey(33) #give passing time for memory (33 milisecs means 30fps, 1000/30 = 33.33333333333336)        



