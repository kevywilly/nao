__author__ = 'kevywilly'


from nao_module import *
from managers.proxy_manager import *
from managers.posture_manager import PostureManager
from managers.motion_manager import MotionManager
from managers.face_manager import FaceManager
from managers.tracking_manager import TrackingManager

import datetime
class NaoDate:
    def __init__(self, tts):
        self.tts = tts

    def dateRequest(self, d):
        r = d.lower()
        currentTime = datetime.datetime.now()
        dayString = currentTime.strftime('%A')
        monthString = currentTime.strftime('%B')
        yearString = "%s" % currentTime.year
        dateString = "%s %s %s %s" % (dayString, monthString, currentTime.day, yearString)
        hour = currentTime.hour
        ampm = "A M"

        if currentTime.hour == 12 and currentTime.minute == 0:
            ampm = ""
            hour = "noon"
        elif currentTime.hour == 0 and currentTime.minute == 0:
            ampm = ""
            hour = "midnight"
        elif currentTime.hour == 0:
            ampm = "A M"
            hour = 12
        elif currentTime.hour > 12:
            ampm = "P M"
            hour = hour - 12

        timeString = "%s %s %s" % (hour, currentTime.minute, ampm)

        if r == "day":
            self.tts.say("it is %s" % dayString)
        elif r == "time":
            self.tts.say("it is %s" % timeString)
            if ampm == "A M" and hour <= 3:
                self.tts.say("it is very late")
            elif ampm == "A M" and hour <= 6:
                self.tts.say("it is very early")
            elif ampm == "P M" and hour >= 10:
                self.tts.say("it is getting late")
        elif r == "date":
            self.tts.say("it is %s" % dateString)
        elif r == "year":
            self.tts.say("the year is %s" % yearString)
        elif r == "month":
            self.tts.say("it is %s" % monthString)


class NaoBrainModule(NaoModule):
    """
    Nao Brain Module
    """
    def __init__(self, name):

        NaoModule.__init__(self, name)
        self.naoMotion = ALProxy("NaoMotion")
        self.naoAwareness = ALProxy("NaoAwareness")
        self.naoDate = NaoDate(ALProxy("ALTextToSpeech"))

        self.subscriptions = ["Brain/DateRequest"]

        #self.__managers = {"Motion" : MotionManager(self.proxies),
        #                   "Posture" : PostureManager(self.proxies),
        #                   "Face" : FaceManager(self.proxies)}

        #self.__commands = ["Posture/Sit",
        #                 "Posture/Stand",
        #                 "Posture/Crouch",
        #                 "Posture/SitRelax",
        #                 "Motion/WakeUp",
        #                 "Motion/Rest"]

    def onStart(self):
        """ start brain """
        self.naoMotion.onStart()
        self.naoAwareness.onStart()

        NaoModule.onStart(self)

    def onStop(self):
        """
        stop brain
        """
        self.naoAwareness.onStop()
        self.naoMotion.onStop()

        NaoModule.onStop(self)


    #def __stopSubscriptions(self):
    #    for command in self.__commands:
    #        self.proxies.memory.unsubscribeToMicroEvent("Brain/" + command, self.getName())
    # -------------------------------------
    # Callbacks
    # -------------------------------------

    def onCommand(self, key, value, message):
        """ callback """
        print "command", key, value
        #self.proxies.memory.unsubscribeToMicroEvent(key, self.getName())
        #b,mgr,cmd = key.split("/")
        #self.__managers[mgr].execute(cmd)
        #self.proxies.memory.insertData(key, 0)
        #self.proxies.memory.subscribeToMicroEvent(key, self.getName(), "subscription", "onCommand")

    def onCallback(self, key, value, message):
        if key == "Brain/DateRequest":
            self.naoDate.dateRequest(value)
