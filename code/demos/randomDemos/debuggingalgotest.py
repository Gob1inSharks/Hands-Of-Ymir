"""
ID: Jayden Chen
LANG: python
TASK: determine if distance is reliable
"""

import cv2
import math
import numpy as np

#define a few necessary variables
h = 22
alpha = 1135

def getdistance(a):
    output = float(int(100000* math.sqrt((a[0][0]-a[1][0])**2 + (a[0][1]-a[1][1])**2)))/100
    return output

def getcamdistance(P):
    output = float(int(100*alpha*h / getdistance(P)))/100
    return output

fout = open('testdata.txt','w')

cap = cv2.VideoCapture(0)

if cap.isOpened():

    cap.set(cv2.CAP_PROP_FRAME_WIDTH)
    cap.set(cv2.CAP_PROP_FRAME_HEIGHT)
    print('screen running')

    while(1):
        readcode,frame = cap.read()

    
