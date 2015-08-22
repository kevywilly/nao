__author__ = 'kevywilly'

from naoqi import ALModule, ALProxy

from naomodule import *

class MovementModule(NaoModule):

    # ---------------------------------------------------------------------------------------
    # This module manages movement and changes in posture for NAO
    # ---------------------------------------------------------------------------------------

    def __init__(self, name):
        NaoModule.__init__(self, name)

        self.motion = ALProxy("ALMotion")
        self.postureProxy = ALProxy("ALRobotPosture")
        self.valid_postures = self.postureProxy.getPostureList()
        self.currentPosture = None
        self.currentPostureFamily = None
        self.listenTo("Movement/GotoPosture", "memoryCallback")
        self.listenTo("PostureChanged", "memoryCallback")

    def getPosture(self):
        self.currentPosture = self.postureProxy.getPosture()
        self.currentPostureFamily = self.postureProxy.getPostureFamily()
    # ------------------------------------------
    # determines whether Nao can go to posture
    # ------------------------------------------
    def canGotoPosture(self, posture):
        if (posture in self.valid_postures) and (self.postureProxy.getPosture() != posture):
            self.memory.raiseEvent("Movement/WillGoToPosture", posture)
            return True
        else:
            self.memory.raiseEvent("Movement/AlreadyInPosture", self.currentPostureFamily)
            return False

    # ------------------------------------
    # Tell NAO to got to a posture
    # ------------------------------------

    def gotoPosture(self, posture, speed = 1.0):
        """Go to requested posture"""
        print("goto posture received", posture, speed)
        if self.canGotoPosture(posture) is True:
            self.postureProxy.post.goToPosture(posture, speed)

        pass

    def wakeUp(self):
        """Wake up"""
        self.motion.wakeUp()

    # -- posture changed callback
    def memoryCallback(self, key, value, message):
        if key == "PostureChanged":
            self.getPosture()
        elif key == "Movement/GotoPosture":
            self.gotoPosture(value, 1.0)

        pass



