__author__ = 'kevywilly'

import sys
import time
from optparse import OptionParser

from naoqi import ALBroker

from modules.nao_motion import *
from modules.nao_walk import *
from modules.nao_talk import *
from modules.nao_people import *
from modules.nao_awareness import *
from modules.nao_brain import *

NAO_IP = "nao.local"

def main():
    """Main entry point"""

    print "broker running"
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
    pip = opts.pip
    pport = opts.pport

    # We need this broker to be able to construct
    # NAOqi modules and subscribe to other modules
    # The broker must stay alive until the program exists
    myBroker = ALBroker("myBroker",
                        "0.0.0.0",   # listen to anyone
                        0,           # find a free port and use it
                        pip,         # parent broker IP
                        pport)       # parent broker port

    # Load Face tracking module

    global NaoMotion
    NaoMotion = NaoMotionModule("NaoMotion")

    global NaoPeople
    NaoPeople = NaoPeoplePerceptionModule("NaoPeople")

    global NaoWalk
    NaoWalk = NaoWalkingModule("NaoWalk")

    global NaoTalk
    NaoTalk = NaoTalkingModule("NaoTalk")

    global NaoAwareness
    NaoAwareness = NaoAwarenessModule("NaoAwareness")

    global NaoBrain
    NaoBrain = NaoBrainModule("NaoBrain")


    #NaoBrain.onStart()
    #NaoPeople.onStart()
    #NaoAwareness.onStart()











    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        print "Interrupted by user, shutting down"
        NaoBrain.onStop()
        myBroker.shutdown()
        sys.exit(0)

if __name__ == "__main__":
    main()