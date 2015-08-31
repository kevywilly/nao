__author__ = 'kevywilly'

from modules.nao_module import *

class NaoPeoplePerceptionModule(NaoModule):
    def __init__(self, name):

        NaoModule.__init__(self, name)

        self.tracker = self.loadProxy('ALTracker')
        self.people = self.loadProxy('ALPeoplePerception')
        self.motion = self.loadProxy('ALMotion')

    def onStart(self):
        """ track face """
        self.people.setFastModeEnabled(False)
        self.subscribeToEvent("PeoplePerception/JustArrived", "onCallback")
        self.subscribeToEvent("PeoplePerception/JustLeft", "onCallback")
        self.people.subscribe(self.getName())
        NaoModule.onStart(self)

    def onStop(self):
        """
        stop face tracker
        """

        self.people.unsubscribe(self.getName())

        NaoModule.onStop(self)

    # -------------------------------------
    # Callbacks
    # -------------------------------------

    def onCallback(self, key, value, message):
        print key
        print value




