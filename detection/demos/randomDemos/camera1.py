import cv2
import mediapipe as mp

#initialize mediapip hands 
mp_drawing = mp.solutions.drawing_utils
mp_drawing_styles = mp.solutions.drawing_styles
mp_hands = mp.solutions.hands

camnum = 0
#get camera
cap = cv2.VideoCapture(camnum) 

cv2.waitKey(1000) #some passing time


if cap.isOpened():

    with mp_hands.Hands(
    model_complexity=0,
    min_detection_confidence=0.5,
    min_tracking_confidence=0.5) as hands:

        #set frame settings. settings are 480p 3:2 
        cap.set(cv2.CAP_PROP_FRAME_WIDTH, 720)
        cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)

        print('screen1 running')
                
        while True: #show image on repeat to get video
                    
            read_code1, frame1 = cap.read()

            # To improve performance, mark frames as not writeable to pass by reference
            frame1.flags.writeable = False
            frame1 = cv2.cvtColor(frame1,cv2.COLOR_BGR2RGB)
            results1 = hands.process(frame1)

            allhands = []
            
            if results1.multi_hand_landmarks:
                for hand_landmarks in results1.multi_hand_landmarks:
                    
                    allhands.append(
                        #apend to allhands the two points
                   [hand_landmarks.landmark[mp_hands.HandLandmark.WRIST].y],
                    #make sure formatting is correct
                    hand_landmarks.landmark[mp_hands.HandLandmark.MIDDLE_FINGER_TIP].y])

            HL1 = []

            for p in allhands:
                
                HL1.append(

            #send HL1 to calculator program

                    
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

            cv2.waitKey(33) #give passing time for memory (33 milisecs means 30fps, 1000/30 = 33.33333333333336)        



