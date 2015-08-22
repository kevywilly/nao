__author__ = 'kevywilly'

ip = "nao.local"
port = 9559

from naoqi import ALProxy

def getProxy(name):
    return ALProxy(name, ip, port)

class NaoTrackModule:

    def __init__(self):
        self.tracker = getProxy('ALTracker')
        self.memory = getProxy('ALMemory')
        self.motion = getProxy('ALMotion')
        self.leds = getProxy("ALLeds")
        self.targetName = "Face"

    def onStart(self):
        self.motion.wakeUp()

        targetName = "Face"
        faceWidth = 0.1
        self.tracker.registerTarget(targetName, faceWidth)
        self.tracker.setMaximumDistanceDetection(3.0)
        self.tracker.track(targetName)
        self.leds.setIntensity("LeftFaceLedsGreen", 0.5)
        self.leds.setIntensity("RightFaceLedsGreen", 0.5)

    def onStop(self):
        self.tracker.stopTracker()
        self.tracker.unregisterAllTargets()
        self.motion.rest()
        self.leds.reset()


m = NaoTrackModule()
m.onStart()

import time
try:
    while True:
        time.sleep(1)
except KeyboardInterrupt:
    print
    print "Interrupted by user"
    print "Stopping..."
    m.onStop()
    # Stop tracker.

