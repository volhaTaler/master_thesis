import sys
import subprocess
import datetime
sys.path.append("/home/volha/pynaoqi-python2.7-2.5.7.1-linux64/lib/python2.7/site-packages")
from naoqi import ALProxy
from PIL import Image
import pepper_image
import time

def main():

    TIME = 3
    SubID = "NAO"
    robotIP = "192.168.0.131" 
    PORT = 9559
    posture_service = ALProxy("ALRobotPosture", robotIP, PORT)
    tts = ALProxy("ALTextToSpeech", robotIP, PORT)
    tts.setLanguage("English")
    motion =  ALProxy("ALMotion", robotIP, 9559)
    posture_service.goToPosture("StandZero", 0.5) 
    #motion.setAngles("HeadPitch", 0.0, 0.15) 
    # print("pose")  
    videoDevice_nao = ALProxy('ALVideoDevice', robotIP, PORT)
    filename = '/home/volha/Desktop/MSc/master_thesis/logs/precition_logfile_' +   str(datetime.datetime.now()) + '.txt'
    for i in range(TIME):
        motion.setAngles("HeadYaw", 0.6, 0.1) # positive numbers - interaction partner is on the right
        time.sleep(2)
        result, image = pepper_image.capture_robot_camera_nao(videoDevice_nao, SubID)
        img = Image.fromarray(image)
        dt = datetime.datetime.now()
        timestamp = '%s-%s-%s_%s:%s:%s' % (dt.month, dt.day, dt.year, dt.hour, dt.minute, dt.second)
        img_name = '/home/volha/Desktop/MSc/master_thesis/trail/' + timestamp + "_" + str(i) + '.png' 
        img.save(img_name)
        
        print(str(i) + " image must be saved")
        # tts.say(str(i+1))
        # here start script for mediapipe
        prediciton = process_image(img_name)
        with open(filename, "a") as file:
            file.write(img_name + "\t" + prediciton + "\n")

        print(prediciton)
        motion.setAngles("HeadYaw", 0.0, 0.1)
        motion.setAngles("HeadPitch", 0.0, 0.15)
        time.sleep(1)

    print("DONE")
    time.sleep(3)

def process_image(pth_to_image):
    # 1. open terminal start python 3
    # 2. run shell script
    # we are ready find a solution here.
    proc= subprocess.Popen(["sh","./mediapipe_bash.sh", pth_to_image], stdout=subprocess.PIPE)
    stdout, _ = proc.communicate()
    prediction = stdout.decode()

    return"prediction: " + str(prediction);


if __name__ == "__main__":
    main()