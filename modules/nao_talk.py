__author__ = 'kevywilly'

import time
import argparse
from modules.nao_module import *

class NaoTalkingModule(NaoModule):

    initVocab = ['hello','hi','walk','stop']

    def __init__(self, name):
        NaoModule.__init__(self, name)

        print "initializing ", self.getName()
        self.naoWalk = self.loadProxy("NaoWalk")
        self.tts = self.loadProxy("ALTextToSpeech")
        self.speech = self.loadProxy("ALSpeechRecognition")
        self.autonomous = self.loadProxy("ALAutonomousMoves")

        if self.autonomous:
            self.autonomous.setExpressiveListeningEnabled(False)

    def onStart(self):
        """ start  """
        self.initSpeech()
        self.say("hello")

        self.subscribeToEvent("WordRecognized", "onWordRecognized")

        NaoModule.onStart(self)

    def onStop(self):
        """ stop """
        self.say("goodbye")
        self.stopSpeech()

        NaoModule.onStop(self)

    def initSpeech(self):
        """ init speech """
        if self.speech:
            #self.animatedSpeech.setBodyLanguageMode(0)
            self.speech.pause(True)
            self.speech.setAudioExpression(False)

            self.speech.setVocabulary(self.initVocab, True)
            self.speech.pause(False)
            self.speech.subscribe(self.getName())

    def stopSpeech(self):
        if self.speech:
            try:
                self.speech.unsubscribe(self.getName())
            except:
                print "done"

    def pauseSpeech(self, bool):
        if self.speech:
            self.speech.pause(bool)


    def say(self, text, async=False):
        self.pauseSpeech(True)
        """ say text """
        if async is True:
            self.tts.post.say(text)
        else:
            self.tts.say(text)
        self.pauseSpeech(False)


    # ---------------------------------
    # Callbacks
    # ---------------------------------

    def onWordRecognized(self, key, value, message):
        word = value[0]
        print word
        self.unsubscribeToEvent(key)

        if "walk" in word:
            self.naoWalk.runDemo()

        elif "stop" in word:
            self.naoWalk.onStop()

        self.subscribeToEvent(key, "onWordRecognized")


