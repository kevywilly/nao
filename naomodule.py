__author__ = 'kevywilly'

from naoqi import ALModule, ALProxy

class NaoModule(ALModule):
    def __init__(self, name):
        ALModule.__init__(self, name)

        self.memory = ALProxy("ALMemory")

    def listenTo(self, key, method):
        self.memory.subscribeToEvent(key, self.getName(), method)
        pass

    def stopListeningTo(self, key):
        self.memory.unsubscribeToEvent(key, self.getName())
        pass
