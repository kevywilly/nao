

from naoqi import ALProxy

tts = ALProxy("ALTextToSpeech", "127.0.0.1", 56323)

tts.say("hello")

