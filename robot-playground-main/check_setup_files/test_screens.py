import cv2
import numpy as np
from PIL import Image, ImageTk
import Tkinter

import time
# import matplotlib.pyplot as plt




# def show_monitor_img(img):
#     """ Show the image in fullscreen on the experiment monitor"""
#     show_img = 'eog --fullscreen '+ img + ' &'
#     # time.sleep(0.1)
#     os.system(show_img)


import os, random


FOLDER_PATH="/home/volha/Desktop/MSc/master_thesis/peppercam13"

def main():
   for i in range(5):
      random_file=random.choice(os.listdir(FOLDER_PATH))
      print(FOLDER_PATH + "/" + random_file)
      img = FOLDER_PATH + "/" + random_file
      show_monitor_img(img)


def show_monitor_img(img):
   """ Show the image in fullscreen on the experiment monitor"""
   show_img = 'eog --fullscreen ' + img + ' &'
    # time.sleep(0.1)
   os.system(show_img)
   time.sleep(2)
   done = "pkill eog"
   os.system(done)

if __name__=="__main__":
   
   main()

    #show_monitor_img('/home/anna/MultimodalTrust//Visual/Images/5.png')
