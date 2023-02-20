import pickle
import cv2
import matplotlib.pyplot as plt
import mediapipe as mp
from sklearn import svm
import time
import os
import sys

with open(sys.argv[2], "rb") as model:
    loaded_model = pickle.load(model)
    path = sys.argv[1]
    img_path = cv2.imread(path)
    temp = []
    mpPose = mp.solutions.pose
    pose = mpPose.Pose(static_image_mode=True,
    model_complexity=2,
    enable_segmentation=True,
    min_detection_confidence=0.5)
    mpDraw = mp.solutions.drawing_utils
    #img = cv2.imread(img_path)
    imgRGB = cv2.cvtColor(img_path, cv2.COLOR_BGR2RGB)
    results = pose.process(imgRGB)
    if results.pose_landmarks:
        landmarks = results.pose_landmarks.landmark
        for j in landmarks:
            temp = temp + [j.x, j.y, j.z, j.visibility]
        y = loaded_model.predict([temp])
        if y == 0:
            print(-1)
        else:
            print(1)
    else:
        print(0)
