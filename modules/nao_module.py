__author__ = 'kevywilly'

from naoqi import ALModule, ALProxy

class NaoModule(ALModule):
    def __init__(self, name):
        ALModule.__init__(self, name)

        self.memory = ALProxy("ALMemory")
        self.subscriptions = []

        print "... initialized " + self.getName()

    def loadProxy(self, name):
        try:
            return ALProxy(name)
        except Exception, e:
            print self.getName(), "Could not load proxy ", name
            return None

    def subscribeToEvent(self, key, callback = "onCallback"):
        self.memory.subscribeToEvent(key, self.getName(), callback)
        if key not in self.subscriptions:
            self.subscriptions.append(key)

        print self.getName() + "subscribed to " + key

    def unsubscribeToEvent(self, key):
        try:
            self.memory.unsubscribeToEvent(key, self.getName())
            while key in self.subscriptions:
                self.subscriptions.remove(key)

        except Exception, e:
            print "Not subscribed to " + key

    def unsubscribeAllEvents(self):
        for key in self.subscriptions:
            try:
                self.memory.unsubscribeToEvent(key, self.getName())
            except Exception, e:
                print "Not subscribed to " + key
            finally:
                self.subscriptions = []

    def subscribeAllEvents(self):
        for key in self.subscriptions:
            try:
                self.memory.subscribeToEvent(key, self.getName(), "onCallback")
            except Exception, e:
                print "Cound not subscribe to " + key
                print e
            finally:
                self.subscriptions = []

    def onStart(self):
        self.subscribeAllEvents()
        print self.getName() + "... started"

    def onStop(self):
        self.unsubscribeAllEvents()
        print self.getName() + "... stopped"

    def onCallback(self, key, value, message):
        """"""
        print self.getName() + "got default callback for: %s " % key
        print "... value is: %s " % value

