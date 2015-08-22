__author__ = 'kevywilly'

import time
import argparse
from naoqi import ALProxy, ALModule
import math

class SPEED:
    Fast = 1.0
    Medium = 0.75
    Slow = 0.5

class DIR:
    Forward = [1.0, 0.0, 0.0]
    Backward = [-0.5, 0.0, 0.0]
    SlideRight = [0.0, 0.3, 0.0]
    SlideLeft = [0.0, 0.3, 0.0]
    AvoidRight = [0.5, 0.1, -45*math.pi/180]
    AvoidLeft = [0.5, 0.1, 45*math.pi/180]
    AvoidBackRight = [-0.5, 0.1, -45*math.pi/180]
    AvoidBackLeft = [-0.5, 0.1, 45*math.pi/180]

class NaoWalkModule(ALModule):

    def __init__(self, name):
        ALModule.__init__(self, name)

        print "initializing ", self.getName()

        self.motionProxy  = ALProxy("ALMotion")
        self.postureProxy = ALProxy("ALRobotPosture")
        self.tts = ALProxy("ALTextToSpeech")
        self.memory = ALProxy("ALMemory")
        self.isWalking = False

    def onStart(self):
        """ start  """
        print "starting"
        self.stopWalk()
        self.motionProxy.wakeUp()
        self.postureProxy.goToPosture("StandInit", 0.5)
        self.lookStraight()

    def onStop(self):
        """ stop """
        self.stopWalk()
        self.lookStraight()
        self.motionProxy.rest()

    def runDemo(self):
        """ run demo """
        self.onStart()

        self.tts.post.say("My mom always says look left and right before walking")

        self.lookLeft()
        self.lookRight()

        self.walk(DIR.Forward)
        self.tts.say("Walking forward")

        time.sleep(2)

        self.lookLeft()

        time.sleep(2)

        self.lookRight()

        time.sleep(1)

        self.lookStraight()

        time.sleep(1)

        self.walk(DIR.Backward)

        self.tts.say("Walking backward")

        time.sleep(5)

        self.walk(DIR.AvoidLeft)
        self.tts.say("Turning left")

        time.sleep(3)

        self.walk(DIR.AvoidRight)
        self.tts.say("Turning right")
        time.sleep(3)

        self.walk(DIR.AvoidBackRight)
        self.tts.say("Moving backwards right")

        time.sleep(5)

        self.walk(DIR.AvoidBackLeft)
        self.tts.say("Moving backwards left")

        time.sleep(5)

        self.onStop()

    def walk(self, dir):
        """ walk in specific dir [x, y, angle] """
        x, y, theta = dir
        self.motionProxy.moveToward(x, y, theta, [["Frequency", 1]])
        self.isWalking = True

    def walkTo(self, x, y, angle):
        """ walk meters x, y, angle """
        self.motionProxy.moveTo(x, y, math.pi*float(angle)/180.0)

    def stopWalk(self):
        """ stop walking """
        self.motionProxy.stopMove()
        self.isWalking = False

    def lookStraight(self):
        """ look straight ahead"""
        names  = ["HeadYaw", "HeadPitch"]
        angles = [0.0, 0.0]
        times  = [1.0, 1.0]
        isAbsolute = True
        self.motionProxy.angleInterpolation(names, angles, times, isAbsolute)

    def lookLeftRight(self):
        """Look left then right"""
        self.lookLeft()
        time.sleep(0.5)
        self.lookRight()

    def lookLeft(self):
        """ look left """
        names  = "HeadYaw"
        angles = 90*math.pi/180
        times  = 2.0
        isAbsolute = True
        self.motionProxy.angleInterpolation(names, angles, times, isAbsolute)

    def lookRight(self):
        """ look right """
        names  = "HeadYaw"
        angles = -90*math.pi/180
        times  = 2.0
        isAbsolute = True
        self.motionProxy.angleInterpolation(names, angles, times, isAbsolute)
