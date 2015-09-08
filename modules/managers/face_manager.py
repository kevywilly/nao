__author__ = 'kevywilly'

from proxy_manager import *

class FaceManager(ProxyManager):
    def __init__(self, proxies):
        ProxyManager.__init__(self, proxies)
        self.face = self.proxies.face

        self.onStart()


