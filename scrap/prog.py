

NAOIP="127.0.0.1"
NAOPORT=53281

import sys
import time

from naoqi import ALProxy, motion
import almath

def getProxy(name):
    try:
        return ALProxy(name, NAOIP, NAOPORT)
    except Exception, e:
        print "Could not create proxy to ALRobotPosture"
        print "Error was: ", e

class Proxies:
    TextToSpeech = "ALTextToSpeech"
    SpeechRecognition = "ALSpeechRecognition"
    RobotPosture = "ALRobotPosture"
    Motion = "ALMotion"

class Postures:
    StandInit = "StandInit"
    Sit = "Sit"
    Crouch = "Crouch"
    LyingBack = "LyingBack"
    LyingBelly = "LyingBelly"
    SitRelax = "SitRelax"

class Chains:
    Head = "Head"
    LArm = "LArm"
    RArm = "RArm"
    LLeg = "LLeg"
    RLeg = "RLeg"
    Torso = "Torso"

class Space:
    Torso = 0
    World = 1
    Robot = 2

class Axis:
    Position = 7
    Rotation = 56
    Both = 63


class TtsHelper:
    def __init__(self):
        self.tts = getProxy(Proxies.TextToSpeech)

    def say(self, text):
        self.tts.say(text)

    def say_async(self, text):
        self.tts.post.say(text)



class MotionHelper:


    def __init__(self):
        self.motionProxy = getProxy(Proxies.Motion)
        self.postureProxy = getProxy(Proxies.RobotPosture)

    # -------------- Motion Methods ------------------

    def wakeUp(self):
        self.motionProxy.wakeUp()

    def stiffnessOn(self):
        self.motionProxy.stiffnessInterpolation("Body", 1.0, 0.5)

    def stiffnessOff(self):
        self.motionProxy.stiffnessInterpolation("Body", 0.0, 0.5)

    def getPosition(self, chainName, space, sensors = False):

        return self.motionProxy.getPosition(chainName, space, sensors)

    def setPosition(self, chainName, space, target, speed = 0.5, axisMask = 7):
        self.motionProxy.setPosition(chainName, space, target, speed, axisMask)
        return target

    def changePosition(self, chainName, space, target, speed = 0.5, axisMask = 7):
        self.motionProxy.setPosition(chainName, space, target, speed, axisMask)
        return target

    # ------------- Posture Methods -----------------

    def getPosture(self):
        return self.postureProxy.getPosture()

    def getPostureFamily(self):
        return self.postureProxy.getPostureFamily()

    def goToPosture(self, posture, speed = 1.0):
        return self.postureProxy.goToPosture(posture, speed)

import math
def radians(angle):
    if float(angle) == 0.0:
        return 0.0
    else:
        return math.pi/(180.0/float(angle))

def main():


    motionProxy = getProxy(Proxies.Motion)
    postureProxy = getProxy(Proxies.RobotPosture)

    # --- Defaults ----
    speed = 0.5
    useSensorValues = False

    # Stand Init
    postureProxy.goToPosture("StandInit", speed)

    # Get position in the world
    result = motionProxy.getRobotPosition(False)
    print "Robot Postition", result

    # Get robot displacement
    initRobotPosition = almath.Pose2D(motionProxy.getRobotPosition(False))
    print "Init Robot Position", initRobotPosition

    motionProxy.moveTo(0.5, 0.0, radians(280))

    endRobotPosition = almath.Pose2D(motionProxy.getRobotPosition(False))
    print "End Position", endRobotPosition

    robotMove = almath.pose2DInverse(initRobotPosition)*endRobotPosition
    print "Robot move", robotMove












if __name__ == "__main__":
    main()