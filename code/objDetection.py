"""
Name: objDetection
Author: Jayden Chen
Purpose: 
    Initialize object detection
    Import model
    Visualize the results for object detection
"""

import cv2
import numpy as np
import mediapipe as mp
from mediapipe.tasks import python
from mediapipe.tasks.python import vision

# initialize object detection
base_options = python.BaseOptions(model_asset_path='assets/efficientdet_lite0.tflite') #this is the model file change file name if nesscary
options = vision.ObjectDetectorOptions(base_options=base_options,
                                       score_threshold=0.5) #score threshold shows 
detector = vision.ObjectDetector.create_from_options(options)

"""


"""
def visualizeObject(image,detection_result) -> np.ndarray:
    category_name=""
    for detection in detection_result.detections:
        
        bbox = detection.bounding_box
        start_point = bbox.origin_x, bbox.origin_y
        end_point = bbox.origin_x + bbox.width, bbox.origin_y + bbox.height
        print(bbox)
        cv2.rectangle(image, start_point, end_point, (0,255,0), 3)
       
        category = detection.categories[0]
        category_name = category.category_name
        probability = round(category.score, 2)
        result_text = category_name + ' (' + str(probability) + ')'
        text_location = (0 + bbox.origin_x,0 + 0 + bbox.origin_y)
        cv2.putText(image, result_text, text_location, cv2.FONT_HERSHEY_PLAIN,1, (0,0,255), 2)

    return image,category_name

"""


"""
if __name__ == '__main__':

    cap=cv2.VideoCapture(0)#get camera

    while (True):
        ret,frame=cap.read()
        print('reading')
        cv2.imwrite("temp/frame.jpg",frame)
        #cv2.imshow("a",frame)
        image = mp.Image.create_from_file("temp/frame.jpg")

        detection_result = detector.detect(image)

        image_copy = np.copy(image.numpy_view())
        annotated_image,text = visualizeObject(image_copy, detection_result)
        rgb_annotated_image = cv2.cvtColor(annotated_image, cv2.COLOR_BGR2RGB)
        cv2.imshow("image",rgb_annotated_image)
        if cv2.waitKey(50) == 27:
            break
    cv2.destroyAllWindows()