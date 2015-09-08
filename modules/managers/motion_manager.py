__author__ = 'kevywilly'

from proxy_manager import *

class MotionManager(ProxyManager):
    def __init__(self, proxies):
        ProxyManager.__init__(self, proxies)
        ProxyManager.onStart(self)

    def execute(self, cmd):
        cmd = cmd.lower()
        if cmd == "wakeup":
            self.proxies.motion.wakeUp
        elif cmd == "rest":
            self.proxies.motion.rest()