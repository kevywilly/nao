__author__ = 'kevywilly'

from proxy_manager import *

class TrackingManager(ProxyManager):
    def __init__(self, proxies):
        ProxyManager.__init__(self, proxies)

        self.tracker = self.proxies.tracker
        self.people = self.proxies.people

        self.people.setFastModeEnabled(False)
        self.people.subscribe(self.getName())
        self.mode = "Head"
        self.width = 0.1
        self.targetName = "Face"
        self.distanceX = 0.3
        self.distanceY = 0.0
        self.angleWz = 0.0
        self.thresholdX = 0.1
        self.thresholdY = 0.1
        self.thresholdWz = 0.3
        self.subscribeDone = False
        self.effector = "None"
        self.trackerIsRunning = False

        self.onStart()

        #ProxyManager.onStart(self)

    def onStart(self):
        self.startTracker()
        ProxyManager.onStart(self)

    def onStop(self):
        self.stopTracker()
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

