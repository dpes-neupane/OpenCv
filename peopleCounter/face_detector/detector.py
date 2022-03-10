import cv2 as cv
from mtcnn import MTCNN
import os
import numpy as np
from pathlib import Path

class Detector():
    def __init__(self, mtcnn=False) -> None:
        self.mtcnn = mtcnn
        if not self.mtcnn:
            path_model = Path(".") / 'peopleCounter' / 'caffeModel' / "deploy.prototxt"
            path_weights = Path(".") / 'peopleCounter' / 'caffeModel' / 'res10_300x300_ssd_iter_140000.caffemodel'
            self.dnn = cv.dnn.readNet(str(path_model), str(path_weights))
            
        else:
            self.detector = MTCNN()
            
        
    def detectFace(self, imgPath):  
        if isinstance(imgPath, str):
            img = cv.imread(imgPath)
        else:
            img = imgPath
        (h,w) = img.shape[:2]
        if self.mtcnn:
            faces = self.detector.detect_faces(img)
            for face in faces:
                # print(str(face['confidence']), type(str(face['confidence'])))
                conf = str(face['confidence'])
                img = cv.putText(img, conf,(face['box'][0], face['box'][1] - 10),  cv.FONT_HERSHEY_COMPLEX, 0.5, (255, 0, 0), 2 )
                img = cv.rectangle(img, (face['box'][0],  face['box'][1]), (face['box'][0] +face['box'][2],face['box'][1]+face['box'][3]), 255, 2 )
            cv.imshow("", img)
        else:
            

            
            blob = cv.dnn.blobFromImage(cv.resize(img, (300, 300)), 1.0, (300, 300), (104, 117, 123), False, False)
            self.dnn.setInput(blob)
            
            detections = self.dnn.forward()

            for i in range(0, detections.shape[2]):
                conf = detections[0, 0, i, 2]
                if conf >=0.6:
                    box = detections[0, 0, i, 3: 7] * np.array([w, h, w, h])
                    (startX, startY, endX, endY) = box.astype("int")
                    
                    text = f"{conf:.2f}"
                    y = startY - 10 if startY - 10 > 10 else startY + 10
                    cv.rectangle(img, (startX, startY), (endX, endY), 255, 5)
                    cv.putText(img, text, (startX, y),cv.FONT_HERSHEY_SIMPLEX, 3, (0, 0, 255), 2)
            cv.imshow("", img)
        
        

        
        
    
detect = Detector(mtcnn=True)


video = "peopleCounter/highQuality.mp4"
cap = cv.VideoCapture(0)

while cap.isOpened():
    ret, frame = cap.read()
    detect.detectFace(frame)
    if cv.waitKey(10) & 0xff == ord("q"):
        break
cap.release()
cv.destroyAllWindows()