import cv2
import mediapipe as mp
import numpy as np
import threading

class ViewportRendererThread(threading.Thread):
    def __init__(self, frame_callback, processing_type):
        super().__init__()
        self.frame_callback = frame_callback
        self.processing_type = processing_type
        self.mp_drawing = mp.solutions.drawing_utils
        self.mp_hands = mp.solutions.hands
        self.stopped = False

        self.MEDIAPIPE_PROCESSING = "mediapipe"
        self.CASCADE_PROCESSING = "cascade"

    def run(self):
         cap = cv2.VideoCapture(0, cv2.CAP_DSHOW)
         while not self.stopped:
             processed_frame = None
             if self.processing_type == self.MEDIAPIPE_PROCESSING:
              processed_frame = self.process_mediapipe(cap)
             elif self.processing_type == self.CASCADE_PROCESSING:
              processed_frame = self.process_cascade(cap)

             self.frame_callback(processed_frame)
    def process_cascade(self, frame):
        default_detector = cv2.CascadeClassifier('trash.xml')
        _, image = frame.read()
        image = cv2.flip(image, 1)

        gray_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

        detections = default_detector.detectMultiScale(image,
            scaleFactor = 5,
            minNeighbors = 91)

        for (x,y,w,h) in detections:
            cv2.rectangle(frame, (x,y),(x+w,y+h), (0, 255, 0), 2)

        return self.texture_convertion(image)

    def process_mediapipe(self, frame):
        with self.mp_hands.Hands(
                static_image_mode = False,
                max_num_hands = 1,
                min_detection_confidence=0.5) as hands:

         _, image = frame.read()
         image = cv2.flip(image, 1)
         image_rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
 
         results = hands.process(image_rgb)
  
         if results.multi_hand_landmarks is not None:
             for hand_landmarks in results.multi_hand_landmarks:
                 self.mp_drawing.draw_landmarks(image, hand_landmarks, self.mp_hands.HAND_CONNECTIONS,
                 self.mp_drawing.DrawingSpec(color=(0,0,255),thickness=-1, circle_radius=5),
                 self.mp_drawing.DrawingSpec(color=(0,40,255),thickness=2,))

         return self.texture_convertion(image)

    def texture_convertion(self, image):
         viewport = np.flip(image, 2)
         data = viewport.ravel()
         data = np.asfarray(data, dtype='f')
         texture_data = np.true_divide(data, 255.0)

         return texture_data

    def stop(self):
         self.stopped = True
    
