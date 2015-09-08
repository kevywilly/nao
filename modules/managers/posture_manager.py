__author__ = 'kevywilly'

from proxy_manager import *

class PostureManager(ProxyManager):
    def __init__(self, proxies):
        ProxyManager.__init__(self, proxies)
        self.onStart()

    def execute(self, cmd):
        self.proxies.posture.post.goToPosture(cmd, 0.8)
