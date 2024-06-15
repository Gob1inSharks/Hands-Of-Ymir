import cv2
import numpy as np
import mediapipe as mp
from mediapipe.tasks import python
from mediapipe.tasks.python import vision

x=0

def visualize(image,detection_result) -> np.ndarray:
    category_name=""
    for detection in detection_result.detections:
        
        bbox = detection.bounding_box
        start_point = bbox.origin_x, bbox.origin_y
        end_point = bbox.origin_x + bbox.width, bbox.origin_y + bbox.height
        cv2.rectangle(image, start_point, end_point, (0,255,0), 3)
       
        category = detection.categories[0]
        category_name = category.category_name
        probability = round(category.score, 2)
        result_text = category_name + ' (' + str(probability) + ')'
        text_location = (0 + bbox.origin_x,0 + 0 + bbox.origin_y)
        cv2.putText(image, result_text, text_location, cv2.FONT_HERSHEY_PLAIN,1, (0,0,255), 2)

    return image,category_name

base_options = python.BaseOptions(model_asset_path='efficientdet_lite0.tflite')
options = vision.ObjectDetectorOptions(base_options=base_options,
                                       score_threshold=0.5)
detector = vision.ObjectDetector.create_from_options(options)

cap=cv2.VideoCapture(0)
while(True):
    ret,frame=cap.read()
    cv2.imwrite("frame.jpg",frame)
    #cv2.imshow("a",frame)
    image = mp.Image.create_from_file("frame.jpg")

    detection_result = detector.detect(image)

    image_copy = np.copy(image.numpy_view())
    annotated_image,text = visualize(image_copy, detection_result)
    rgb_annotated_image = cv2.cvtColor(annotated_image, cv2.COLOR_BGR2RGB)
    cv2.imshow("image",rgb_annotated_image)
    if cv2.waitKey(50) == 27:
        break
cv2.destroyAllWindows()

