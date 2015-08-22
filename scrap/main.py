__author__ = 'kevywilly'

NAO_IP = "192.168.1.150"
PORT = 9559

import sys
import time
from optparse import OptionParser

from modules.nao_brain import *

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

    brain = NaoBrain(pip, pport)

    brain.start()
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        print "Interrupted by user, shutting down"
        brain.stop()
        sys.exit(0)

if __name__ == "__main__":
    main()