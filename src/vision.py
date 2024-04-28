from exceptions import exceptions
import cv2
import numpy as np
import threading
import time

class ViewportRendererThread(threading.Thread):
    def __init__(self, frame_callback, frame_dimentions, input_type, media_path, model_path):
        super().__init__()
        self.frame_callback = frame_callback
        self.frame_dimentions = frame_dimentions
        self.input_type = input_type
        self.media_path = media_path
        self.model_path = model_path
        self.width = 0
        self.height = 0
        self.stopped = False

        self.MEDIA_INPUT = "Media"
        self.WEBCAM_INPUT = "Webcam"

    def run(self):
        cap = None
        if self.input_type == self.MEDIA_INPUT:
            cap = cv2.VideoCapture(self.media_path)
            print(self.media_path)
        elif self.input_type == self.WEBCAM_INPUT:
            cap = cv2.VideoCapture(0)
        else:
            raise exceptions.EmptyInputException()

        processed_frame, width, height = self.process_cascade(cap)
        self.frame_dimentions(width, height)

        while not self.stopped:
              processed_frame, width, height = self.process_cascade(cap)
              self.frame_callback(processed_frame)

    def process_cascade(self, frame):
        default_detector = cv2.CascadeClassifier(str(self.model_path))
        _, image = frame.read()
        image = cv2.flip(image, 1)
        if self.input_type == self.MEDIA_INPUT: 
            ratio = 0.5
            height, width, _ = image.shape
            image = cv2.resize(image, (int(width * ratio), int(height * ratio)), interpolation=cv2.INTER_AREA)

        #fps = frame.get(cv2.CAP_PROP_FPS)
        gray_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

        #cv2.putText(image, str(fps), (20,20), cv2.FONT_HERSHEY_DUPLEX, 1, (0, 0, 255), 1)
        #cv2.putText(image, str(fps), (20,20), cv2.FONT_HERSHEY_DUPLEX, 1, (0, 0, 255), 1)
        detections = default_detector.detectMultiScale(gray_image,
            scaleFactor = 5.1,
            minNeighbors = 300,
            minSize = (50,50))

        for (x,y,w,h) in detections:
            x_coord = int((x+x+w) / 2)
            y_coord = int((y+y+h) / 2)

            cv2.rectangle(image, (x,y),(x+w,y+h), (0, 0, 255), 2)
            #cv2.putText(image, "Detecting", (x_coord-130,y_coord+155), cv2.FONT_HERSHEY_DUPLEX, 1, (0, 0, 255), 1)

        time.sleep(0.05)
        return self.texture_convertion(image)

    def texture_convertion(self, image):
         viewport = np.flip(image, 2)
         height, width,  _ = image.shape
         data = viewport.ravel()
         data = np.asfarray(data, dtype='f')
         texture_data = np.true_divide(data, 255.0)
         return texture_data, height, width

    def stop(self):
         self.stopped = True
    
