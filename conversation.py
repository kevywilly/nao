__author__ = 'kevywilly'

__author__ = 'kevywilly'

import sys
import time
from naoqi import ALModule, ALBroker, ALProxy
from optparse import OptionParser

from mood import Mood

class ConversationModule(ALModule):
    def __init__(self, name):
        ALModule.__init__(self, name)

        self.tts = ALProxy("ALTextToSpeech")
        self.ears = ALProxy("ALSpeechRecognition")
        self.memory = ALProxy("ALMemory")
        self.log = ALProxy("ALLogger")

        self.ears.subscribe("Conversation")
        self.memory.subscribeToEvent("WordRecognized", "Conversation", "onWordRecognized")

    def onWordRecognized(self, key, value, message):
        """
        Subscribe to change in mood
        :param key: memory key
        :param value: memory value
        :param message: message of the event
        :return:
        """

        self.ears.unsubscribe("Conversation")

        self.tts.say("I recognized %s" % value)

        self.ears.subscribe("Conversation")

        pass

    def setMood(self, value):
        """
        Sets the current mood felt by the robot
        :param value: Mood value 1=good, 0=neutral, -1=bad
        :return:
        """
        self.__previousMood = self.__mood
        self.__mood = Mood(value)

        self.memory.raiseEvent("Brain/Mood/Text", self.__mood.text)
        self.memory.raiseEvent("Brain/Mood/Value", self.__mood.value)
        pass

    def getMood(self):
        """
        Gets the current mood
        :return:
        """
        return self.__mood

    def getPreviousMood(self):
        """
        Gets the previous mood
        :return:
        """
        return self.__previousMood









