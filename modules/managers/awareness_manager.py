__author__ = 'kevywilly'

from proxy_manager import *

class AwarenessManager(ProxyManager):
    def __init__(self, proxies):
        ProxyManager.__init__(self, proxies)

        self.awareness = self.proxies.awareness
        self.autonomous = self.proxies.autonomous



        self.onStart()

        #ProxyManager.onStart(self)

    def onStart(self):
        self.awareness.startAwareness()
        ProxyManager.onStart(self)

    def onStop(self):
        self.awareness.stopAwareness()
        ProxyManager.onStop(self)

    def startTracker(self):
        """ Start face tracker """
        if self.trackerIsRunning is False:
            self.tracker.setEffector(self.effector)
            self.tracker.registerTarget(self.targetName, 0.1)
            self.tracker.setRelativePosition([-self.distanceX, self.distanceY, self.angleWz,
                                              self.thresholdX, self.thresholdY, self.thresholdWz])
            self.tracker.setMode(self.mode)
            self.tracker.track(self.targetName) #Start tracker
            self.trackerIsRunning = True

    def stopTracker(self):
        """ Stop face tracker """
        if self.trackerIsRunning:
            self.tracker.setEffector("None")
            self.tracker.stopTracker()
            self.tracker.unregisterTarget(self.targetName)
            self.trackerIsRunning = False

