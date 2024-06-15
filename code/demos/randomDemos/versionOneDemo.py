"""
Name: TwoCamDis 
Author: Jayden Chen
Purpose: Get the distance of a person from Two Cameras

input: 
    hand_landmarks from mediapipe hands * 2

output: 
    distance in meters

"""
import math
import mediapipe as mp
import cv2
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
from mediapipe.tasks import python
from mediapipe.tasks.python import vision

from obj import visualizeObject
from obj import ObjProperties
from obj import cleanSuitcaseData

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

"""
def disformula(a,b): #gets distance between two points

    return math.sqrt((a[0]-b[0])**2 + (a[1]-b[1])**2 )

"""
Func: pythagorean
Author: Jayden Chen
Purpose: finds the hypo using the pythagorean theorem

input: 
    width, height (int)
    
output:
    integer

remarks:
"""
def pythagorean(a,b):

    return round(math.sqrt(int(a)**2 + int(b)**2),2)

"""
Func: visualize distance
Author: Jayden Chen
Purpose: 
input: 
    
output:

remarks:
"""
img=cv2.imread('canvas.jpg')
imgorg=img.copy()



"""
Func: disrtance formula values
Author: Jayden Chen
Purpose: 

remarks:
"""
#test data 
#1m: 2.04 1.93 1.92 avg1.95
#1.25m: 1.82 1.86 avg1.85
#1.5m: 1.65 1.65, 1.68, 1.5 avg1.65
#1.75m: 1.5 1.51 1.41 avg1.5
#2m: 1.35 1.39 avg1.35

#P = b + a/(x + c)

#values for distance formula
a = 1 
b = 1 #this value does not change unless camera issues
c = 0.05
L = 1 #horizontal distance between cmameras in meters

"""
Func: calcRegression
Author: Jayden Chen
Purpose: based on the data given, change the values of a,b,c in L*(a/(P-b) - c)

input: data.csv
    
output: 

remarks: don't know if it works or not. bad at math(s)

"""


#distance = L * (a / (P-b) -c)


"""
Func: calcDis 
Author: Jayden Chen
Purpose: calculates the distance based on the equation: 

input: P (the ratio of P1 and P2)
    
output: distance in meters


remarks:

"""
def calcDis(P):
    #P = b + a/(x*d + c)
    #x*d = a / (P-b) -c

    #return round(((a/(P-b) + c))*L,2) #can't do this well without calculus :(
    slopeMap = {1.95:(1,0.8),1.75:(1.25,0.6),1.6:(1.5,0.2),1.55:(1.75,0.4)}
    
    position = 1.95
    return (P-position)*(-slopeMap[position][1]) + slopeMap[position][0]
 
"""
Func: cleanSingleData
Author: Jayden Chen
Purpose: formats the hand landmark points into distance

input: hand_landmarks, width, height
    
output: P1 or P2

remarks: need to rewrite
    
"""
def cleanSingleData(hand_landmarks,width,height):
            
    return 0

"""
Func: cleanCoupledData
Author: Jayden Chen
Purpose: gets the P value

input: P1, P2
    
output: P

remarks:
    
"""
def cleanCoupledData(P1,P2):

    return P1/P2

"""
Func: twocamdis
Author: Jayden Chen
Purpose: returns the distance as fast as possible

input: P1, P2
    
output: distance in meters

remarks: need to rewrite
    
"""
def twocamdis(P1,P2):
    return 0

"""
Func: CompleteTwocamdis
Author: Jayden Chen
Purpose: returns the distance from the less-processed value given

input: hand_landmarks * 2, width, height
    
output: distance in meters

remarks: need to rewrite
    
"""
def CompleteTwocamdis(hand_landmarks1,hand_landmarks2,width,height):

    

    return 0

def main():
    #initialize mediapipe vision
    base_options = python.BaseOptions(model_asset_path='efficientdet_lite0.tflite') #this is the model file, change file name if nesscary
    options = vision.ObjectDetectorOptions(base_options=base_options,
                                       score_threshold=0.5) #score threshold shows 
    detector = vision.ObjectDetector.create_from_options(options)

    CAM1 = cv2.VideoCapture(0)
    CAM1.set(cv2.CAP_PROP_FOURCC,cv2.VideoWriter_fourcc('M','J','P','G'))
    CAM2 = cv2.VideoCapture(2)
    CAM2.set(cv2.CAP_PROP_FOURCC,cv2.VideoWriter_fourcc('M','J','P','G'))
    #wait a while
    cv2.waitKey(1000)

    print('starting')
 
    if CAM1.isOpened():
        print('One Camera Open')
        if CAM2.isOpened():
            print("Cameras Open!")

            while True:

                #get frame and success
                read_code1, frame1 = CAM1.read()
                read_code2, frame2 = CAM2.read()

                if read_code1 and read_code2:

                    print('Frame is found, proceding')

                    #save image for formatting
                    cv2.imwrite("frame1.jpg",frame1)
                    frame1 = mp.Image.create_from_file("frame1.jpg")
                    cv2.imwrite("frame2.jpg",frame2)
                    frame2 = mp.Image.create_from_file("frame2.jpg")

                    #get results
                    results1 = detector.detect(frame1)
                    results2 = detector.detect(frame2)

                    raw1 = ObjProperties(results1)
                    raw2 = ObjProperties(results2)

                    print(raw1,len(raw1))
                    print(raw2,len(raw2))

                    P1,X1 = cleanSuitcaseData(raw1)
                    P2,X2 = cleanSuitcaseData(raw2)
                    print(P1)
                    print(P2)

                    if P1 != 'NA' or P2 != 'NA':
                        print('object detected')
                        #if raw2['item'] == 'suitcase':
                        P = cleanCoupledData(P1,P2)

                        print(calcDis(P),'meters away')
                        distance1 = calcDis(P)
                        distance2 = X1
                    else:
                        distance1 = 0
                        distance2 = 0

                    
                    img = imgorg.copy()

                    x = int(140 + 120 * float(distance1))
                    y = int(425 + 120 * float(distance2))
                    cv2.circle(img,(y,x),20,(255,0,255))
                    print('showing distance')
                    cv2.imshow('canvas',img)
                    cv2.waitKey(10)
                        
                    #show frames
                    image1 = np.copy(frame1.numpy_view())
                    annotated_image1,text1 = visualizeObject(image1, results1)
                    rgb_annotated_image = cv2.cvtColor(annotated_image1, cv2.COLOR_BGR2RGB)
                    cv2.imshow("image1",rgb_annotated_image)
                    image2 = np.copy(frame2.numpy_view())
                    annotated_image2,text2 = visualizeObject(image2, results2)
                    rgb_annotated_image = cv2.cvtColor(annotated_image2, cv2.COLOR_BGR2RGB)
                    cv2.imshow("image2",rgb_annotated_image)

                else:
                    print('Frames are not found')

                #if esc is pressed, break
                if cv2.waitKey(90) == 27:
                    break
    CAM1.release()
    CAM2.release()
    cv2.destroyAllWindows

main()