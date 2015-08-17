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
        self.currentPosture = self.postureProxy.getPosture()
        self.currentPostureFamily = self.postureProxy.getPostureFamily()
        self.valid_postures = self.postureProxy.getPostureList()
        self.onStart()

    # ------------------------------------------
    # determines whether Nao can go to posture
    # ------------------------------------------
    def canGotoPosture(self, posture):
        valid = posture in self.valid_postures
        notInPosture = self.currentPosture != posture

        if (posture in self.valid_postures) and (self.currentPosture != posture):
            self.memory.raiseEvent("Brain/Movement/WillGoToPosture", posture)
            return True
        else:
            self.memory.raiseEvent("Brain/Movement/AlreadyInPosture", self.currentPostureFamily)
            return False

    # ------------------------------------
    # Tell NAO to got to a posture
    # ------------------------------------
    def gotoPosture(self, posture, speed):
        """Go to requested posture"""
        print("goto posture received", posture, speed)
        if self.canGotoPosture(posture) is True:
            self.postureProxy.post.goToPosture(posture, speed)

            self.currentPostureFamily = self.postureProxy.getPostureFamily()
            self.currentPosture = self.postureProxy.getPosture()
        pass

    # -- posture changed callback
    def memoryCallback(self, key, value, message):
        if key == "PostureChanged":
            self.currentPosture = value
        elif key == "PostureFamilyChanged":
            self.currentPostureFamily = value

        pass

    # -- posture fammily changed callback
    def postureFamilyChanged(self, key, value, message):
        self.currentPostureFamily = value

    def onStart(self):
        """ on Start"""
        self.motion.wakeUp()
        self.listenTo("PostureChanged", "memoryCallback")
        self.listenTo("PostureFamilyChanged", "memoryCallback")
        pass

    def onStop(self):
        """ on Start"""
        self.stopListeningTo("PostureChanged")
        self.stopListeningTo("PostureFamilyChanged")
        pass

