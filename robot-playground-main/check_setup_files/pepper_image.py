import sys
import os
import random
sys.path.append("/home/volha/pynaoqi-python2.7-2.5.7.1-linux64/lib/python2.7/site-packages")
from naoqi import ALProxy
from PIL import Image
import numpy as np
import time



TRUST_IMG_FOLDER = "/home/volha/Desktop/MSc/MSC_data/trail/images.05.01.23_cond1"
UNTRUST_IMG_FOLDER = "/home/volha/Desktop/MSc/MSC_data/trail/images.05.01.23_cond2"
# width 640, 480
left =  20 #70  # x left
top =  40 #55  # y top
right = 570 #265 #255  # x right
bottom = 440 

def show_monitor_img(img):
    """ Show the image in fullscreen on the experiment monitor"""
    show_img = 'eog --fullscreen ' + img + ' &'
    # time.sleep(0.1)
    os.system(show_img)

def choose_image(condition):
    if (condition == 1 or condition == 3):
        return TRUST_IMG_FOLDER + "/" + random.choice(os.listdir(TRUST_IMG_FOLDER))
    elif (condition == 2):
        return UNTRUST_IMG_FOLDER + "/" + random.choice(os.listdir(UNTRUST_IMG_FOLDER))
    else: 
        return "NOT FOUND"

def display_img_screen(img):
   """ Show the image in fullscreen on the experiment monitor"""
   show_img = 'eog --fullscreen ' + img + ' &'
    # time.sleep(0.1)
   os.system(show_img)

    

    #show_monitor_img('/home/anna/MultimodalTrust//Visual/Images/5.png')


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


def main():

    SubID = "NAO"
    robotIP = "192.168.0.131" 
    PORT = 9559
    posture_service = ALProxy("ALRobotPosture", robotIP, PORT)
    tts = ALProxy("ALTextToSpeech", robotIP, PORT)
    tts.setLanguage("English")
    motion =  ALProxy("ALMotion", robotIP, 9559)
    # motion.setAngles("HeadPitch", 0.0, 0.15)
    time.sleep(1)
    # motion.setAngles("HeadYaw", 0.0, 0.15)
    # time.sleep(1.5) 
    image_path = choose_image(condition=1)
    display_img_screen(image_path) 
    time.sleep(0.5)
    videoDevice_nao = ALProxy('ALVideoDevice', robotIP, PORT)
    result, image = capture_robot_camera_nao(videoDevice_nao, SubID)
    time.sleep(0.5)
    img = Image.fromarray(image)

    img = img.crop((left, top, right, bottom))
    img_name = '/home/volha/Desktop/MSc/MSC_data/peppercam999/' +'test_' + str(18.02) + '.png' 
    img.save(img_name)

    print("pose")  
    
    # motion.setAngles("HeadPitch", 0.0, 0.15)
    
    # motion.setAngles("HeadYaw", 0.6, 0.1)
    # time.sleep(1.5)
    image_path = choose_image(condition=2)
    display_img_screen(image_path) 
    
    result, image = capture_robot_camera_nao(videoDevice_nao, SubID)
    img = Image.fromarray(image)
    img = img.crop((left, top, right, bottom))
    img_name = '/home/volha/Desktop/MSc/MSC_data/peppercam999/' +'test_' + str(18.202) + '.png' 
    img.save(img_name)
    # time.sleep(3)
    # #motion.setAngles("HeadYaw", 0.0, 0.1)
    # motion.setAngles("HeadPitch", 0.0, 0.15)
    # time.sleep(1.5)
    # motion.setAngles("HeadYaw", -0.6, 0.1)
    # time.sleep(1.5)
    # motion.setAngles("HeadYaw", 0.0, 0.1)
    # time.sleep(1.5)
    # #time.sleep(3)
    # result, image = capture_robot_camera_nao(videoDevice_nao, SubID)
    # img = Image.fromarray(image)
    
    # img_name = '/home/volha/Desktop/MSc/master_thesis/peppercam999/' +'_' + str(3) + '.png' 
    # img.save(img_name)
    #posture_service.goToPosture("StandZero", 0.5) 

    print("DONE")
    


if __name__ == "__main__":
    main()
