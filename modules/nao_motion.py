__author__ = 'kevywilly'

import time
import argparse
from modules.nao_module import *

class NaoMotionModule(NaoModule):

    def __init__(self, name):
        NaoModule.__init__(self, name)
        self.motionProxy  = ALProxy("ALMotion")
        self.postureProxy = ALProxy("ALRobotPosture")
        self.tts = ALProxy("ALTextToSpeech")

        self.defaultSpeed = 0.5

        self.subscriptions = ["NaoBrain/Motion/GotoPosture"]
        self.subscriptions = ["NaoBrain/Motion/WakeUp"]
        self.subscriptions = ["NaoBrain/Motion/Rest"]

        self.movingToPosture = False

    def onStart(self):
        """on stop"""
        self.motionProxy.wakeUp()

        NaoModule.onStart(self)

    def onStop(self):
        """on stop"""
        self.motionProxy.rest()
        NaoModule.onStop(self)

    def goToPosture(self, posture, speed = 0.5):
        """ go to requested posture if not already there """

        currentPosture = self.postureProxy.getPosture()

        if currentPosture == posture:
            self.tts.say("Nice try, i don't think so.")
            return
        elif self.movingToPosture:
            self.tts.say("Sorry, i can't do that right now.")
            return

        self.movingToPosture = True
        self.gotoPosture(posture, speed)
        self.movingToPosture = False

    def moveInit(self):
        """ prepare for move """
        self.motionProxy.moveInit()

    def wakeUp(self):
        """ wake up """
        self.motionProxy.wakeUp()

    def rest(self):
        """ stop """
        self.motionProxy.rest()

    def onCallback(self, key, value, message):
        if key == "NaoBrain/Motion/GotoPosture":
            self.goToPosture(value)
        elif key == "NaoBrain/Motion/WakeUp":
            self.wakeUp()
        elif key == "NaoBrain/Motion/Rest":
            self.rest()
        else:
            NaoModule.onCallback(self, key, value, message)

