import sys
import time
sys.path.append("/home/volha/pynaoqi-python2.7-2.5.7.1-linux64/lib/python2.7/site-packages")
from naoqi import ALProxy

def main():

    PORT=9559
    robotIP = "192.168.0.131" #"192.168.43.7"
    motionProxy  = ALProxy("ALMotion", robotIP, PORT)
    posture_service = ALProxy("ALRobotPosture", robotIP, PORT)


    # Go to rest position
    #motionProxy.StandZero(
    # posture_service.goToPosture("StandZero", 0.5)	
    motion =  ALProxy("ALMotion", robotIP, 9559) 
    motion.setAngles("HeadPitch", 0.0, 0.15) 
    motion.setAngles("HeadYaw", 0.0, 0.1)
    # time.sleep(1)
    # motion.setAngles("HeadYaw", 0.0, 0.0)
    

    print "::::::::::::::::::::::::::::::::::::::"
    print "          NAO movement done          "
    print "::::::::::::::::::::::::::::::::::::::"

if __name__ == "__main__":
    main()
