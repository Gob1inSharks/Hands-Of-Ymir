import mediapipe as mp
from mediapipe.tasks import python
from mediapipe.tasks.python import vision

from clients import ClientUDP
from clients import MQTTClient

import _config as global_vars

import math
import cv2
import threading
import time

#initialize mp mediapipe hands
mp_drawing = mp.solutions.drawing_utils
mp_drawing_styles = mp.solutions.drawing_styles
mp_hands = mp.solutions.hands

from bodyCapture import Hands

if "__main__" == __name__:

    hands = Hands()
    hands.start()