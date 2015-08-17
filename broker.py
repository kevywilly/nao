__author__ = 'kevywilly'


import sys
import time
from naoqi import ALModule, ALBroker, ALProxy
from optparse import OptionParser
from brain import *
from language import *
from movement import *



NAO_IP = "nao.local"

Brain = None
Language = None
Movement = None

def main():
    """Main entry point"""

    parser = OptionParser()
    parser.add_option("--pip",
                      help="Parent broker port. The IP address or your robot",
                      dest="pip")
    parser.add_option("--pport",
                      help="Parent broker port. The port NAOqi is listening to",
                      dest="pport",
                      type="int")
    parser.set_defaults(
        pip=NAO_IP,
        pport=9559)

    (opts, args_) = parser.parse_args()
    pip   = opts.pip
    pport = opts.pport

    # We need this broker to be able to construct
    # NAOqi modules and subscribe to other modules
    # The broker must stay alive until the program exists
    myBroker = ALBroker("myBroker",
                        "0.0.0.0",   # listen to anyone
                        0,           # find a free port and use it
                        pip,         # parent broker IP
                        pport)       # parent broker port

    global Language
    Language = LanguageModule("Language")

    global Movement
    Movement = MovementModule("Movement")

    global Brain
    Brain = BrainModule("Brain")
    #Brain.onStart()



    try:
        while True:
            time.sleep(1)
            #Brain.setMood(-1.0)
    except KeyboardInterrupt:
        print
        print "Interrupted by user, shutting down"
        Brain.onStop()
        myBroker.shutdown()
        sys.exit(0)

if __name__ == "__main__":
    main()