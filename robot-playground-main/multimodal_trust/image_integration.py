import sys
import subprocess
import datetime
sys.path.append("/home/path/pynaoqi-python2.7-2.5.7.1-linux64/lib/python2.7/site-packages")
from naoqi import ALProxy
from PIL import Image
import numpy as np
import Tkinter
import os
import random
import constants
import time

TRUST_IMG_FOLDER = "/home/path/images_condition1"
UNTRUST_IMG_FOLDER = "/home/path/images_condition2"

def predict_intention(condition=0, offline_mode=True):

    SubID = "NAO"
    robotIP = "" 
    PORT = 9559
    posture_service = ALProxy("ALRobotPosture", robotIP, PORT)
    tts = ALProxy("ALTextToSpeech", robotIP, PORT)
    tts.setLanguage("English")
    motion =  ALProxy("ALMotion", robotIP, 9559)

    videoDevice_nao = ALProxy('ALVideoDevice', robotIP, PORT)
    filename = '/home/path/logs/record_test.txt'
   
     # positive numbers - interaction partner is on the right
    
    if(offline_mode):
    
        if(condition==1 or condition==3):
            image_path = choose_image(condition=1)
            display_img_screen(image_path) 
        elif(condition==2):
            image_path = choose_image(condition=2)
            display_img_screen(image_path) 

    time.sleep(0.7)
    result, image = capture_robot_camera_nao(videoDevice_nao, SubID)
    time.sleep(0.5)
    img = Image.fromarray(image)
    if(offline_mode):
        # To adjust
        img = img.crop((constants.p_left, constants.p_top, constants.p_right, constants.p_bottom))
    dt = datetime.datetime.now()
    timestamp = '%s-%s-%s_%s:%s:%s' % (dt.month, dt.day, dt.year, dt.hour, dt.minute, dt.second)

    ### MUST BE CHANGED FOR EVERY strategy##
    img_name = '/home/path/record_test/' + timestamp + '_condition1.png' 
    img.save(img_name)
    if(offline_mode):
        time.sleep(0.3)
        finish_display_image()
    
    # here start script for mediapipe
    prediciton = process_image(img_name)

    # log the location of the captured image and prediction that wasmade
    with open(filename, "a") as file:
        file.write(img_name + "\t" + prediciton + "\n")

    print(prediciton)
    
    return prediciton

def process_image(pth_to_image):
    # 1. open terminal start python 3
    # 2. run shell script
    # we are ready find a solution here.
    proc= subprocess.Popen(["sh","./mediapipe_bash.sh", pth_to_image], stdout=subprocess.PIPE)
    stdout, _ = proc.communicate()
    prediction = stdout.decode()

    return str(prediction)

def choose_image(condition):
    if (condition == 1 or condition == 3):
        return TRUST_IMG_FOLDER + "/" + random.choice(os.listdir(TRUST_IMG_FOLDER))
    elif (condition == 2):
        return UNTRUST_IMG_FOLDER + "/" + random.choice(os.listdir(UNTRUST_IMG_FOLDER))
    else: 
        return "IMAGE OR FOLDER NOT FOUND"

def display_img_screen(img):
   """ Show the image in fullscreen on the experiment monitor"""
   show_img = 'eog --fullscreen ' + img + ' &'
    # time.sleep(0.1)
   os.system(show_img)

def finish_display_image():
    """Closes the window that displays the chosen image in full screen
    """
    done = "pkill eog"
    os.system(done)

def capture_robot_camera_nao(videoDevice_nao, SubID):
    """ Capture images from Nao's TOP camera. Note that the Nao's
        camera resolution is lower than the Pepper robot.
        Remember you need to subscribe and unsubscribe respectively
        see, https://ai-coordinator.jp/pepper-ssd#i-3
    """
   # SubID = "NAO"
   # videoDevice_nao = ALProxy('ALVideoDevice', NAO_IP, PORT)

    # subscribe top camera, Image of 320*240px
    AL_kTopCamera, AL_kVGA, Frame_Rates = 0, 2, 5  # 2.5  #10
    AL_kBGRColorSpace = 11  # Buffer contains triplet on the format 0xRRGGBB, equivalent to three unsigned char
    captureDevice_nao = videoDevice_nao.subscribeCamera(SubID, AL_kTopCamera, AL_kVGA, AL_kBGRColorSpace, Frame_Rates)

    width, height =  640, 480
    image = np.zeros((height, width, 3), np.uint8)
    result = videoDevice_nao.getImageRemote(captureDevice_nao)

    if result == None:
        print("Camera problem.")
    elif result[6] == None:
        print("No image. ")
    else:
        # translate value to mat
        values = map(ord, list(result[6]))
        i = 0
        for y in range(0, height):
            for x in range(0, width):
                image.itemset((y, x, 0), values[i + 0])
                image.itemset((y, x, 1), values[i + 1])
                image.itemset((y, x, 2), values[i + 2])
                i += 3

    # unsubscribe from the camera
    videoDevice_nao.unsubscribe(captureDevice_nao)
    return result[6], image
