__author__ = 'kevywilly'

import time
import argparse
from modules.nao_module import *

class NaoMotionModule(NaoModule):

    def __init__(self, name):
        NaoModule.__init__(self, name)
        self.motionProxy  = ALProxy("ALMotion")
        self.postureProxy = ALProxy("ALRobotPosture")
        self.defaultSpeed = 0.5

    def sit(self, speed = 0.5):
        """ stop """
        self.postureProxy.goToPosture("Sit", speed)

    def standInit(self, speed = 0.5):
        """ stand init """
        self.postureProxy.goToPosture("StandInit", speed)

    def crouch(self, speed = 0.5):
        """ crouch """
        self.postureProxy.goToPosture("Crouch", speed)

    def sitRelax(self, speed = 0.5):
        """ sit relaxed """
        self.postureProxy.goToPosture("SitRelax", speed)

    def lyingBack(self, speed = 0.5):
        """ lie back """
        self.postureProxy.goToPosture("LyingBack", speed)

    def moveInit(self):
        """ prepare for move """
        self.motionProxy.moveInit()

    def wakeUp(self):
        """ wake up """
        self.motionProxy.wakeUp()

    def rest(self):
        """ stop """
        self.motionProxy.rest()

