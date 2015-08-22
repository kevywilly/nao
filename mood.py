__author__ = 'kevywilly'

class Mood:

    def __init__(self,value):
        self.value = value
        self.text = self.getText(value)

    def getText(self,value):
        """
        Gets text representaion of the current mood
        :param value:
        :return:
        """
        v = float(value)
        if v < (-.25):
            return "sad"
        elif v > 0.25:
            return "happy"
        else:
            return "ok"

    def setValue(self,value):
        """ Sets value of the current mood
        :param value:
        :return:
        """
        v = float(value)
        self.value = float(v)
        self.text = self.getText(float(v))


from naomodule import *

class MoodModule(NaoModule):

    def __init__(self, name):
        NaoModule.__init__(self, name)

        self.previous_mood = None
        self.mood = None

        self.listenTo("Brain/SetMood", "memoryCallback")

    def setMood(self, value):
        self.previous_mood = self.mood
        self.mood = Mood(value)

        self.memory.raiseEvent("Brain/MoodText", self.__mood.text)
        self.memory.raiseEvent("Brain/MoodValue", self.__mood.value)

        pass


    #--------------------------------------------------------------------------------
    # Callbacks
    #--------------------------------------------------------------------------------

    def memoryCallback(self, key, value, message):
        if key == "Brain/SetMood":
            self.setMood(float(value))