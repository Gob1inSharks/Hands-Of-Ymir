"""
Name: TwoCamDis 
Author: Jayden Chen
Purpose: 
    Get the distance of an object from Two Cameras

"""
#import os
#import cv2
import numpy as np
"""
import mediapipe as mp
from mediapipe.tasks import python
from mediapipe.tasks.python import vision

print('initialize object detection')
# initialize object detection
base_options = python.BaseOptions(model_asset_path='assets//efficientdet_lite0.tflite') #this is the model file
options = vision.ObjectDetectorOptions(base_options=base_options,
                                       score_threshold=0.5) #score threshold shows 
detector = vision.ObjectDetector.create_from_options(options)
"""

"""
Func: calcDis 
Author: Jayden Chen
Purpose: calculates the distance based on the equation: 

input: results from object detection
    
output:  width, orgin x of suitcase

remarks:

"""
def objProperties(detection_result) -> np.ndarray:
    properties = []

    for detection in detection_result.detections:

        #get object box dimensions and origin
        bbox = detection.bounding_box
        width = bbox.width
        height = bbox.height
        origin = (bbox.origin_x, bbox.origin_y)

        #get object category name and accuracy probability
        category = detection.categories[0]
        item = category.category_name
        score = category.score

        properties.append({'item':item,'score':score ,'width':int(width),'height':int(height),'origin':origin})

    return properties

"""
Func: calcDis 
Author: Jayden Chen
Purpose: calculates the distance based on the equation: 

input: results from object detection
    
output:  width, orgin x of suitcase

remarks:

"""
def plantProperties(detection_result) -> np.ndarray:
        
    for detection in detection_result.detections:

        #get object box dimensions and origin
        bbox = detection.bounding_box
        width = bbox.width
        originX = bbox.origin_x

        #get object category name and accuracy probability
        category = detection.categories[0]
        item = category.category_name
        if 'suitcase' in str(item) or 'backpack' in str(item) or 'plant' in str(item) or 'refrigerator' in str(item):
            return width, originX
    
    return None, None

#P = b + a/(x + c)
#distance = L * (a / (P-b) -c)

#values for distance formula
with open('code/twoCamDisVariables.varfx','r') as fin:
    L = float(fin.readline().split()[1])

"""
Func: calcDis 
Author: Jayden Chen
Purpose: calculates the distance based on the equation: 

input: P (the ratio of P1 and P2)
    
output: distance in meters, Ls

remarks:

"""
def calcDis(P):

    slopeMap = {1.95:(1,0.8),1.75:(1.25,0.6),1.6:(1.5,0.2),1.55:(1.75,0.4)}

    return round(((1/(P-1))),4),round(((1/(P-1))/L),4)
    
    #position = 1.95 #don't need to draw secant liness
    #return (P-position)*(-slopeMap[position][1]) + slopeMap[position][0]

"""
Func: twocamdis
Author: Jayden Chen
Purpose: returns the distance as fast as possible

input: results1, results2 from object detection
    
output: distance in meters, distance in Ls, distance in 

remarks: this version is different because it only considers one target instead of multiple
    
"""
def twoCamDis(results1,results2):
    #print('something') #here for debug
    P1,X1 = plantProperties(results1)
    P2,X2 = plantProperties(results2)

    if P1 != None:
        if P2 != None:
            #if raw2['item'] == 'suitcase':
            P = P1/P2
            distanceZMeters, distanceLMeters = calcDis(P)
            distanceX = X1

            return distanceLMeters, distanceZMeters, distanceX
        
    return None, None, None
        
if __name__ == '__main__':

    print(L)
    print(calcDis(1.5))
    """
    #initialize camera
    CAM1 = cv2.VideoCapture(0)
    CAM1.set(cv2.CAP_PROP_FOURCC,cv2.VideoWriter_fourcc('M','J','P','G'))
    CAM2 = cv2.VideoCapture(1)
    CAM2.set(cv2.CAP_PROP_FOURCC,cv2.VideoWriter_fourcc('M','J','P','G'))
    #wait a while
    cv2.waitKey(100)

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
                    cv2.imwrite("temp//frame1.jpg",frame1)
                    frame1 = mp.Image.create_from_file("temp//frame1.jpg")
                    cv2.imwrite("temp//frame2.jpg",frame2)
                    frame2 = mp.Image.create_from_file("temp//frame2.jpg")

                    #get results
                    results1 = detector.detect(frame1)
                    results2 = detector.detect(frame2)

                    print(results1,results2)

                    print('getting results')

                    distanceInLs, distanceInMeters, distanceHorizontal = twoCamDis(results1,results2)
                    
                    print(distanceInLs, distanceInMeters, distanceHorizontal)

                else:
                    print('Frames are not found')

                #userInterfaceShow(distanceInLs, distanceInMeters, distanceHorizontal)
                #if esc is pressed, break
                if cv2.waitKey(80) == 27:
                    break

    CAM1.release()
    CAM2.release()
    cv2.destroyAllWindows #this thing is here for debugging
    """