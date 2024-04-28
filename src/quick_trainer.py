import cv2
import numpy as nnp
import imutils
import os

data = 'p'
if not os.path.exists(data):
    print("New directory created")
    os.makedirs(data)

cap = cv2.VideoCapture(0)
count = 0

x1, y1 = 190, 80
x2, y2 = 450, 380

while True:
    ret, frame = cap.read()
    if ret == False : break
    aux = frame.copy()
    cv2.rectangle(frame, (x1, y1), (x2, y2),(255, 0, 0), 2)

    object = aux[y1:y2, x1:x2]
    object = imutils.resize(object, width = 38)

    key = cv2.waitKey(1)
    if key == 27:
        break
    if key == ord('s'):
        cv2.imwrite(data+'/object_{}.jpg'.format(count), object)
        print('Picture stured: ', 'object_{}'.format(count))
        count += 1
    cv2.imshow('frame', frame)
    cv2.imshow('object', object)



