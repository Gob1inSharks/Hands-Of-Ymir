import random
import time
from paho.mqtt import client as mqtt_client

import cv2
import numpy as np
import mediapipe as mp
from mediapipe.tasks import python
from mediapipe.tasks.python import vision

# initialize object detection
base_options = python.BaseOptions(model_asset_path='efficientdet_lite0.tflite') #this is the model file change file name if nesscary
options = vision.ObjectDetectorOptions(base_options=base_options,
                                       score_threshold=0.5) #score threshold shows 
detector = vision.ObjectDetector.create_from_options(options)

broker = 'broker.emqx.io'
port = 1883
topic = "/falk0or/distancedetection"
client_id = f'python-mqtt-{random.randint(0, 1000)}'


def on_connect(client, userdata, flags, rc):
    if rc == 0:
        print("Connected to MQTT Broker!")
    else:
        print("Failed to connect, return code %d\n", rc)

client = mqtt_client.Client(client_id)
client.on_connect = on_connect
client.connect(broker, port)
client.loop_start()

msg_count=0

def visualizeObject(image,detection_result) -> np.ndarray:
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

def ObjProperties(detection_result) -> np.ndarray:
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

time.sleep(2)
if __name__ == '__main__':

    cap=cv2.VideoCapture(0)#get camera

    while (True):
        ret,frame=cap.read()
        cv2.imwrite("frame.jpg",frame)
        #cv2.imshow("a",frame)
        image = mp.Image.create_from_file("frame.jpg")

        detection_result = detector.detect(image)

        image_copy = np.copy(image.numpy_view())
        annotated_image,text = visualizeObject(image_copy, detection_result)
        rgb_annotated_image = cv2.cvtColor(annotated_image, cv2.COLOR_BGR2RGB)
        cv2.imshow("image",rgb_annotated_image)


        print('======================================')
        output = ObjProperties(detection_result)
        print('publishing results:',output)
        msg = str(output)
        result = client.publish(topic, msg)
        if cv2.waitKey(50) == 27:
            break

    cv2.destroyAllWindows()