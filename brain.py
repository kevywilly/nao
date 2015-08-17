__author__ = 'kevywilly'

import sys
import time
import os

from naoqi import ALModule, ALBroker, ALProxy
from naomodule import *
from mood import Mood
from pymonad import *


class BrainModule(NaoModule):

    def __init__(self, name):
        NaoModule.__init__(self, name)

        self.tts = ALProxy("ALTextToSpeech")
        self.language = ALProxy("Language")
        self.life = ALProxy("ALAutonomousLife")
        self.moves = Nothing
        self.awareness = Nothing
        self.motion = ALProxy("ALMotion")
        self.dialog = ALProxy("ALDialog")
        self.movement = ALProxy("Movement")

        try:
            self.awareness = Just(ALProxy("ALBasicAwareness"))
            self.moves = Just(ALProxy("ALAutonomousMoves"))
        except:
            print(self.getName(), "Could not load Autonomous Moves and Basic Awareness")

        self.__mood = None

        self.__previousMood = None

        self.onStart()

    def onStart(self):
        self.setMood(0.0)
        self.language.onStart()
        self.movement.onStart()
        #self.life.setState("interactive")
        #self.movement.stand()
        # start basic awareness

        self.awareness.bind(lambda a: a.startAwareness())
        self.moves.bind(lambda x: x.setExpressiveListeningEnabled(True))

        self.tts.say("hello")

        #if self.awareness:
        #    self.awareness.startAwareness()

        # Subscribe to Memory
        self.listenTo("Brain/Set/Mood", "memoryCallback")
        self.listenTo("Brain/Commands/GotoPosture", "memoryCallback")

        pass

    def onStop(self):

        self.stopListeningTo("Brain/Set/Mood")
        self.stopListeningTo("Brain/Commands/GotoPosture")

        #self.movement.sitRelax()
        self.motion.rest()

        self.moves.bind(lambda x: x.setExpressiveListeningEnabled(False))
        self.awareness.bind(lambda a: a.stopAwareness())
        #self.life.setState("stopped")

        self.language.onStop()
        self.movement.onStop()
        pass

    def setMood(self, value):
        self.__previousMood = self.__mood
        self.__mood = Mood(value)

        self.memory.raiseEvent("Brain/Mood/Text", self.__mood.text)
        self.memory.raiseEvent("Brain/Mood/Value", self.__mood.value)
        pass

    def getMood(self):
        return self.__mood

    def getPreviousMood(self):
        return self.__previousMood


    #--------------------------------------------------------------------------------
    # Callbacks
    #--------------------------------------------------------------------------------

    def memoryCallback(self, key, value, message):
        if key == "Brain/Set/Mood":
            self.setMood(float(value))
        elif key == "Brain/Commands/GotoPosture":
            self.movement.gotoPosture(value, 1.0)












