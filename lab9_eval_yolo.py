from darkflow.net.build import TFNet
import cv2
import numpy as np
import matplotlib.pyplot as plt
import os 

threshold = 0.5
options = {"pbLoad": "built_graph/tiny-yolo-lab9.pb",
            "threshold": threshold,
           "metaLoad": "built_graph/tiny-yolo-lab9.meta" 
           }
eval_path = 'test_img/'         

tfnet = TFNet(options)



def boxing(original_img, predictions, thre):
    newImage = np.copy(original_img)

    for result in predictions:
        top_x = result['topleft']['x']
        top_y = result['topleft']['y']

        btm_x = result['bottomright']['x']
        btm_y = result['bottomright']['y']

        confidence = result['confidence']
        label = result['label'] + " " + str(round(confidence, 2))

        if confidence > thre:
            newImage = cv2.putText(newImage, label, (top_x, top_y-5), cv2.FONT_HERSHEY_SIMPLEX ,1, (0, 255, 0), 1, cv2.LINE_AA)
            newImage = cv2.rectangle(newImage, (top_x, top_y), (btm_x, btm_y), (255,0,0), 3)
            
            
    return newImage

images_ls = [f for f in os.listdir(eval_path) if f.endswith('.jpg')]

video = cv2.VideoCapture('demo_video/demo.wmv')

try:
    while video.isOpened():
        ret, frame = video.read()
        if not ret:
            print("Can't receive frame (stream end?). Exiting ...")
            break
        result = tfnet.return_predict(frame)
        if len(result)!=0:
            frame = boxing(frame, result, threshold)
        else:
            print("Nothing detected")
            
        cv2.imshow("result", frame)
        cv2.waitKey(33)
except KeyboardInterrupt:
    print("KeyboardInterrupt")
video.release()
cv2.destroyAllWindows()



