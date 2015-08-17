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