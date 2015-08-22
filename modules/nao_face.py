__author__ = 'kevywilly'

from modules.nao_module import *

class NaoFaceTrackingModule(NaoModule):
    def __init__(self, name):

        NaoModule.__init__(self, name)

        self.tracker = self.loadProxy('ALTracker')
        self.faceDetect = self.loadProxy('ALFaceDetection')
        self.motion = self.loadProxy('ALMotion')
        self.leds = self.loadProxy("ALLeds")

        self.tracker.setMode("Head")
        self.tracking = None
        self.learnedFaces = []

        self.subscribeToEvent("ALTracker/TargetLost", "onTargetLost")
        self.subscribeToEvent("ALTracker/TargetDetected", "onTargetDetected")
        self.subscribeToEvent("FaceDetected", "onFaceDetected")

    def stopTracker(self):
        """ stop tracker """



    def onStart(self):
        """ track face """
        if False:
            self.motion.wakeUp()
            self.learnedFaces = self.faceDetect.getLearnedFacesList()
            print self.learnedFaces
            self.faceDetect.setTrackingEnabled(True)
            self.faceDetect.setRecognitionEnabled(True)
            self.faceDetect.subscribe(self.getName())

        if self.tracker:
            targetName = "Face"
            faceWidth = 0.12
            self.tracker.registerTarget(targetName, faceWidth)
            self.tracker.setMaximumDistanceDetection(5.0)
            self.tracker.track(targetName)
            self.tracking = targetName

        NaoModule.onStart(self)

    def onStop(self):
        """
        stop face tracker
        """
        if False:
            self.faceDetect.setTrackingEnabled(False)
            self.faceDetect.setRecognitionEnabled(False)
            self.faceDetect.unsubscribe(self.getName())

        if self.tracker:
            self.tracker.stopTracker()
            self.tracker.unregisterAllTargets()
            self.tracking = None

        self.stopTracker()

        NaoModule.onStop(self)

    # -------------------------------------
    # Callbacks
    # -------------------------------------

    def onFaceDetected(self, key, value, message):
        """"""
        #print key
        #print value

    def onTargetLost(self, key, value, message):
        """"""
        #print key
        #print value

    def onTargetDetected(self, key, value, message):
        """"""
        #print key
        #print value

        #print(key)
        #print(value)
        #self.logger.info(key)
        #self.logger.info(value)




