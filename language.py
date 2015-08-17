__author__ = 'kevywilly'

import sys
import time
import os

from naoqi import ALModule, ALProxy

OS_PATH = os.path.dirname(os.path.abspath(__file__))

TOPICS_PATH = OS_PATH + "/topics"

TOPICS = {'greetings' : TOPICS_PATH + '/greetings_enu.top'}
          #'lexicon' : TOPICS_PATH + '/lexicon_enu.top'}

#TOPICS_PATH = "/home/nao/topics"
#TOPICS = {'greetings' : '/home/nao/topics/greetings_enu.top',
#          'lexicon' : '/home/nao/.local/share/PackageManager/apps/dialog_lexicon/lexicon_enu.top'}

from database import *
from naomodule import *

class LanguageModule(NaoModule):

    def __init__(self, name):
        NaoModule.__init__(self, name)

        self.db = GraphDB()
        self.tts = ALProxy("ALTextToSpeech")
        self.dialog = ALProxy("ALDialog")
        self.logger = ALProxy("ALLogger")
        #self.moves = ALProxy("ALAutonomousMoves")
        #self.voiceAnalysis = ALProxy("ALVoiceEmotionAnalysis")

        self.current_topic = None
        self.topics = {}

    def setCurrentTopic(self, key):
        self.current_topic = self.topics[key]

    def unloadTopics(self):
        for topic in self.dialog.getLoadedTopics("enu"):
            self.dialog.unloadTopic(topic)

    def deactivateTopics(self):
        for topic in self.dialog.getActivatedTopics():
            self.dialog.deactivateTopic(topic)

    def startTopics(self):

        self.dialog.setLanguage("English")

        self.deactivateTopics()
        self.unloadTopics()

        for key in TOPICS:
            self.topics[key] = self.dialog.loadTopic(TOPICS[key])

        self.setCurrentTopic("greetings")

        self.dialog.subscribe(self.getName())
        self.dialog.activateTopic(self.current_topic)

    def onStart(self):
        self.startTopics()
        #self.listenTo("WordRecognized", "memoryCallback")
        self.listenTo("Language/NotUnderstood", "memoryCallback")
        self.listenTo("Language/Define/Parent", "memoryCallback")
        self.listenTo("Language/IsItA/Parent", "memoryCallback")
        self.listenTo("Language/CanIt/Action", "memoryCallback")
        self.listenTo("Language/ItCan/Action", "memoryCallback")
        self.listenTo("Language/WhatIs", "memoryCallback")

    def onStop(self):

        self.stopListeningTo("Language/NotUnderstood")
        self.stopListeningTo("Language/Define/Parent")
        self.stopListeningTo("Language/IsItA/Parent")
        self.stopListeningTo("Language/CanIt/Action")
        self.stopListeningTo("Language/ItCan/Action")
        self.stopListeningTo("Language/WhatIs")

        try:
            self.deactivateTopics()
            self.unloadTopics()
            self.dialog.unsubscribe(self.getName())

        finally:
            print("language stopped")

    # -- Callbacks --

    def memoryCallback(self, key, value, identifier):
        print(key)
        #if key == "WordRecognized":
        #    print(value)
        #el
        if key == "Language/NotUnderstood":
            self.did_not_understand(value)
        elif key == "Language/Define/Parent":
            self.define(self.memory.getData("Language/Define/Name", 0), value)
        elif key == "Language/IsItA/Parent":
            self.is_it_a(self.memory.getData("Language/IsItA/Name", 0), value)
        elif key == "Language/CanIt/Action":
            self.can_it(self.memory.getData("Language/CanIt/Name", 0), value)
        elif key == "Language/ItCan/Action":
            self.it_can(self.memory.getData("Language/ItCan/Name", 0), value)
        elif key == "Language/WhatIs":
            self.what_is(value)

    def did_not_understand(self, value):
        self.say(value)

    def define(self, name, parent):
        self.db.assign_parent("Thing", name, parent)
        self.say("Ok, thank you, I will try to remember that %s is %s" % (name, parent))

    def what_is(self, value):
        result = self.db.definition_of(value)
        if len(result) > 0:
            self.say("a %s is a type of %s" % (value, result[0]))
        else:
            self.say("I don't know /PAU=200/ what is %s" % value)

    def is_it_a(self, name, parent):
        if self.db.is_it_a(name, parent) is True:
            self.say("Yes it is!")
        else:
            self.say("Not that I am aware of!")

    def can_it(self, name, action):
        result, example = self.db.can_it(name, action)
        print(result, example)
        if result is True:
            if example is None:
                self.say("Yes %s can %s" %(name, action))
            else:
                self.say("%s probably can because a %s can %s" % (name, example, action))
        else:
            self.say("No %s cannot %s as far as I know" % (name, action))

    def it_can(self, name, action):
        self.db.assign_ability(name, action)
        self.say("Ok, thank you, I will try to remember that %s can %s" % (name, action))

    def say(self, text):
        self.memory.raiseEvent("Language/Say", text)



