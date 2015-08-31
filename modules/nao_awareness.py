__author__ = 'kevywilly'

from modules.nao_module import *

class NaoAwarenessModule(NaoModule):
    def __init__(self, name):

        NaoModule.__init__(self, name)

        self.awareness = self.loadProxy('ALBasicAwareness')

    def onStart(self):
        self.awareness.resetAllParameters()
        self.awareness.setStimulusDetectionEnabled("People", True)
        self.awareness.setStimulusDetectionEnabled("Sound", False)
        self.awareness.setStimulusDetectionEnabled("Movement", False)
        self.awareness.setStimulusDetectionEnabled("Touch", True)
        self.awareness.setEngagementMode("FullyEngaged")

        self.subscribeToEvent("ALBasicAwareness/HumanTracked")
        self.subscribeToEvent("ALBasicAwareness/HumanLost")
        self.subscribeToEvent("PeoplePerception/PeopleDetected")
        self.subscribeToEvent("FaceDetected")

        self.awareness.startAwareness()
        NaoModule.onStart(self)

    def onStop(self):
        self.awareness.stopAwareness()
        NaoModule.onStop(self)

    def onCallback(self, key, value, message):
        print(key)
        print(value)




