__author__ = 'kevywilly'


from nao_module import *
from managers.proxy_manager import *
from managers.posture_manager import PostureManager
from managers.motion_manager import MotionManager
from managers.face_manager import FaceManager
from managers.tracking_manager import TrackingManager


class NaoBrainModule(NaoModule):
    """
    Nao Brain Module
    """
    def __init__(self, name):

        NaoModule.__init__(self, name)

        self.proxies = Proxies()
        self.proxies.memory = self.memory
        self.proxies.tracker = self.loadProxy('ALTracker')
        self.proxies.face = self.loadProxy('ALFaceDetection')
        self.proxies.motion = self.loadProxy('ALMotion')
        self.proxies.leds = self.loadProxy("ALLeds")
        self.proxies.posture = self.loadProxy("ALRobotPosture")
        self.proxies.tts = self.loadProxy("ALTextToSpeech")
        self.proxies.people = self.loadProxy('ALPeoplePerception')

        self.__managers = {"Motion" : MotionManager(self.proxies),
                           "Posture" : PostureManager(self.proxies),
                           "Face" : FaceManager(self.proxies)}

        self.__commands = ["Posture/Sit",
                         "Posture/Stand",
                         "Posture/Crouch",
                         "Posture/SitRelax",
                         "Motion/WakeUp",
                         "Motion/Rest"]

    def onStart(self):
        """ start brain """
        self.__prepNao()
        self.__startSubscriptions()
        NaoModule.onStart(self)

    def onStop(self):
        """
        stop brain
        """
        self.__stopSubscriptions()
        NaoModule.onStop(self)

    def __prepNao(self):
        self.proxies.motion.wakeUp()
        self.proxies.tts.say("Time to wake up!")

    def __startSubscriptions(self):
        for command in self.__commands:
            key = "Brain/" + command
            print "subscribe to " + key + "..."
            self.proxies.memory.subscribeToMicroEvent("Brain/" + command, self.getName(), "subscription", "onCommand")

    def __stopSubscriptions(self):
        for command in self.__commands:
            self.proxies.memory.unsubscribeToMicroEvent("Brain/" + command, self.getName())
    # -------------------------------------
    # Callbacks
    # -------------------------------------

    def onCommand(self, key, value, message):
        """ callback """
        print "command", key, value
        self.proxies.memory.unsubscribeToMicroEvent(key, self.getName())
        b,mgr,cmd = key.split("/")
        self.__managers[mgr].execute(cmd)
        self.proxies.memory.insertData(key, 0)
        self.proxies.memory.subscribeToMicroEvent(key, self.getName(), "subscription", "onCommand")
