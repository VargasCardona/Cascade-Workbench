import cv2
import mediapipe as mp
import numpy as np
import threading
from pathlib import Path

class ViewportRendererThread(threading.Thread):
    def __init__(self, frame_callback, model_path):
        super().__init__()
        self.frame_callback = frame_callback
        self.model_path = model_path
        self.mp_drawing = mp.solutions.drawing_utils
        self.mp_hands = mp.solutions.hands
        self.stopped = False

    def run(self):
         cap = cv2.VideoCapture(0)
         while not self.stopped:
              processed_frame = self.process_cascade(cap)
              self.frame_callback(processed_frame)

    def process_cascade(self, frame):
        default_detector = cv2.CascadeClassifier(str(self.model_path))
        _, image = frame.read()
        image = cv2.flip(image, 1)

        gray_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

        detections = default_detector.detectMultiScale(gray_image,
            scaleFactor = 1.8,
            minNeighbors = 5,
            minSize = (10,10))

        for (x,y,w,h) in detections:
            x_coord = int((x+x+w) / 2)
            y_coord = int((y+y+h) / 2)

            cv2.rectangle(image, (x,y),(x+w,y+h), (0, 0, 255), 2)
            cv2.putText(image, "Detecting", (x_coord-130,y_coord+155), cv2.FONT_HERSHEY_DUPLEX, 1, (0, 0, 255), 1)

        return self.texture_convertion(image)

    def texture_convertion(self, image):
         viewport = np.flip(image, 2)
         data = viewport.ravel()
         data = np.asfarray(data, dtype='f')
         texture_data = np.true_divide(data, 255.0)

         return texture_data

    def stop(self):
         self.stopped = True
    
