__author__ = 'kevywilly'

class Proxies:
    def __init__(self):
        self.memory = None
        self.posture = None
        self.tts = None
        self.face = None
        self.motion = None
        self.tracker = None
        self.leds = None
        self.people = None
        self.awareness = None
        self.autonomous = None

class ProxyManager:
    def __init__(self, proxies):
        self.proxies = proxies

    def getName(self):
        return self.__class__.__name__

    def onStart(self):
        print("started" + self.getName() + "...")

    def onStop(self):
        print "stopped " + self.getName() + "..."


    def execute(self, cmd):
        print self.getName(), cmd