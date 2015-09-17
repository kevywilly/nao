__author__ = 'kevywilly'


import sys
from modules.nao_module import *

class Face:
    def __init__(self, p):

        self.timestampSeconds, self.timestampMicroseconds = p[0]
        self.unused1, self.alpha, self.beta, self.sizeX, self.sizeY = p[1][0][0]
        self.faceId, self.scoreReco, self.label, self.leftEyePoints, self.rightEyePoints, self.unused2, self.unused3, self.nosePoints, self.mouthPoints = p[1][0][1]
        self.tfr = p[1][len(p[1]) -1]
        self.unrecognized = False
        self.label = None
        self.labels = []

        if len(self.tfr) > 0:
            if self.tfr[0] == 4:
                self.unrecognized = True
            elif self.tfr[0] in [2,3]:
                self.label = self.tfr[1][0]
                self.labels = self.tfr[1]

    def __repr__(self):
        return "<%s faceId=%s label=%s labels=%s>" % (self.__class__.__name__, self.faceId, self.label, self.labels)

    def noChange(self):
        if len(self.tfr) == 0:
            return True
        else:
            return False

class NaoAwarenessModule(NaoModule):
    def __init__(self, name):

        NaoModule.__init__(self, name)

        self.faceTracker = self.loadProxy('ALTracker')
        self.awareness = self.loadProxy('ALBasicAwareness')
        self.currentHuman = None
        self.faceDetect = ALProxy('ALFaceDetection')
        self.tts = ALProxy("ALTextToSpeech")
        self.lastFace = None

        # set default subscriptions
        self.subscriptions = ["ALBasicAwareness/HumanTracked",
                              "ALBasicAwareness/HumanLost",
                              "PeoplePerception/PeopleDetected",
                              "FaceDetected",
                              "Brain/Awareness/LearnFace",
                              "ALTracker/ActiveTargetChanged"]

        self.unrecognizedFace = False
        self.unrecognizedName = None
        self.isTracking = False

    # Startup
    def onStart(self):

        # Memory Settings
        self.memory.insertData("Brain/Awareness/CurrentHuman", None)
        self.memory.insertData("Brain/Awareness/RecognizedFace", None)
        self.memory.declareEvent("Brain/Awareness/RecognizedFace", self.getName())
        self.memory.declareEvent("Brain/Awareness/UnrecognizedFace", self.getName())
        self.memory.declareEvent("Brain/Awareness/LearnFace", self.getName())


        # Awareness
        self.startAwareness()

        # Face Tracker
        self.startFaceTracker()

        self.faceDetect.setRecognitionEnabled(True)
        self.faceDetect.setTrackingEnabled(True)

        # call super start method
        NaoModule.onStart(self)

    # Shutdown
    def onStop(self):
        self.stopFaceTracker()
        self.stopAwareness()

        NaoModule.onStop(self)

    # Start Awareness
    def startAwareness(self):
        """ Start Basic Awareness """
        if self.awareness:
            self.awareness.resetAllParameters()
            self.awareness.setStimulusDetectionEnabled("People", True)
            self.awareness.setStimulusDetectionEnabled("Sound", False)
            self.awareness.setStimulusDetectionEnabled("Movement", True)
            self.awareness.setStimulusDetectionEnabled("Touch", True)
            self.awareness.setEngagementMode("FullyEngaged")
            self.awareness.startAwareness()

    def stopAwareness(self):
        """ Stop Basic Awareness"""
        if self.awareness:
            self.awareness.stopAwareness()

    # Start Face Tracker
    def startFaceTracker(self):
        """ Start Face Tracker """
        if self.faceTracker:
            targetName = "Face"
            faceWidth = 0.12
            self.faceTracker.setMode("Head")
            self.faceTracker.registerTarget(targetName, faceWidth)
            self.faceTracker.setMaximumDistanceDetection(5.0)
            self.faceTracker.track(targetName)
            self.isTracking = True

    def stopFaceTracker(self):
        if self.faceTracker:
            self.faceTracker.stopTracker()
            self.faceTracker.unregisterAllTargets()
            self.isTracking = False

    def onDetectWithoutReco(self, face):
        self.currentHuman = None
        self.memory.raiseEvent("Brain/Awareness/UnrecognizedFace", face.faceId)
        self.memory.insertData("Brain/Awareness/CurrentHuman", None)
        self.memory.insertData("Brain/Awareness/RecognizedFace", None)
        self.unrecognizedFace == True

    def onRecognizedFaces(self, face):
        print face.scoreReco
        self.currentHuman = face.label
        self.memory.insertData("Brain/Awareness/CurrentHuman", face.label)
        self.memory.raiseEvent("Brain/Awareness/RecognizedFace", face.label)
        self.memory.insertData("Brain/Awareness/UnrecognizedFace", None)
        self.unrecognizedFace = False
        self.unsubscribeToEvent("FaceDetected")

        print "got face", face

    def learnFace(self, name):
        self.unrecognizedName = name
        print "got unrecognized face - learning"
        if self.faceDetect.learnFace(name):
            self.tts.say("Got it!")
            self.lastFace.label = name
            self.lastFace.labels = [name]

    def recognizeFace(self, p):
        """ try to recognize face """

        if(len(p) > 0):
            face = Face(p)
            if face.noChange():
                return

            if face.label != None and face.scoreReco < 0.20:
                return

            if face.label != None:
                print "got possible label", face.label
                if self.lastFace != None and (face.scoreReco < self.lastFace.scoreReco):
                    return


            self.lastFace = face
            if self.lastFace.label == None:
                self.onDetectWithoutReco(self.lastFace)
            else:

                self.onRecognizedFaces(self.lastFace)



            #if(len(p[1]) > 0): # just in case of the ALValue is in the wrong format
                # get the ALValue returned by the time filtered recognition:
                #    - [] when nothing new.
                #    - [4] when a face has been detected but not recognized during the first 8s.
                #    - [2, [faceName]] when one face has been recognized.
                #    - [3, [faceName1, faceName2, ...]] when several faces have been recognized.
                #print p
                #self.timeFilteredResult = p[1][len(p[1]) -1]

                #if( len(self.timeFilteredResult) == 1 ):
                    # If a face has been detected for more than 8s but not recognized
                #    if(self.timeFilteredResult[0] == 4):
                #        self.onDetectWithoutReco()
                #elif( len(self.timeFilteredResult) == 2 ):
                    # If one or several faces have been recognized
                #    if(self.timeFilteredResult[0] in [2, 3]):
                        #self.onRecognizedFaces(self.timeFilteredResult[1])
                #        return
                        #for s in self.timeFilteredResult[1]:
                        #    self.onRecognizedFace( s )



    def onCallback(self, key, value, message):
        if key == "FaceDetected":
            self.recognizeFace(value)
        elif key == "Brain/Awareness/LearnFace":
            self.learnFace(value)


        #else:
            #print(key) #NaoModule.onCallback(self, key, value, message)





