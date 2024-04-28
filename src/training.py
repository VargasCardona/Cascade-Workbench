import cv2
import numpy as np
import os

pos_path = '../datasets/pos/'
neg_path = '../datasets/neg/'

pos_imgs = os.listdir(pos_path)
neg_imgs = os.listdir(neg_path)

samples = []
labels = []

for img in pos_imgs:
    img_path = os.path.join(pos_path, img)
    sample = cv2.imread(img_path, cv2.IMREAD_GRAYSCALE)
    sample = np.float32(sample) / 255.0
    samples.append(sample)
    labels.append(1)

for img in neg_imgs:
    img_path = os.path.join(neg_path, img)
    sample = cv2.imread(img_path, cv2.IMREAD_GRAYSCALE)
    sample = np.float32(sample) / 255.0
    samples.append(sample)
    labels.append(0)

samples = np.array(samples).squeeze()
labels = np.array(labels)
print(samples[0].shape)
len(samples)
dataset = cv2.ml.TrainData_create(samples, cv2.ml.ROW_SAMPLE, labels)

parameters = cv2.CascadeClassifier()

params = cv2.CascadeClassifierParams()
params.maxDepth = 1
params.maxNumSplits = 0
params.minSampleCount = 100
params.minNodesPerTree = 10

# Training
num_stages = 10
num_pos = len(pos_imgs)
num_neg = len(neg_imgs)
print("Training with {num_pos} positive samples and {num_neg} negative samples.")
haar_classifier.train(dataset, params, num_stages)

# Save the trained classifier
haar_classifier.save('trained_classifier.xml')
