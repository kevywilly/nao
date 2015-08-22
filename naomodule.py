__author__ = 'kevywilly'

from naoqi import ALModule, ALProxy

class NaoModule(ALModule):

    mySubscriptions = []

    def __init__(self, name):
        ALModule.__init__(self, name)
        self.memory = ALProxy("ALMemory")

    def getProxy(self, name):
        """ get proxy """
        try:
            return ALProxy(name)
        except:
            print("could not subscribe to proxy: " + name)

    def getTTS(self):
        return  ALProxy("ALTextToSpeech")

    def getBasicAwareness(self):
        return ALProxy("ALBasicAwareness")

    def getAutonomousMoves(self):
        return ALProxy("ALAutonomousMoves")

    def exit(self):
        """ exit module """
        for key in self.mySubscriptions:
            self.stopListeningTo(key)

        ALModule.exit(self)

    def listenTo(self, key, method):
        """ listen to memory event """
        self.memory.subscribeToEvent(key, self.getName(), method)
        self.mySubscriptions.append(key)
        pass

    def stopListeningTo(self, key):
        """ stop listening to memory event """
        try:
            self.memory.unsubscribeToEvent(key, self.getName())
        except:
            print("not subscribed to " + key)
        pass
