import random
from abc import ABC, abstractmethod
from logger import Logger
from virtual_server import IVirtualServer, VirtualServer

class IVirtualServerFactory(ABC):
    @abstractmethod
    def create_server(self, ip: str) -> IVirtualServer:
        pass


class VirtualServerFactory(IVirtualServerFactory):
    def __init__(self):
        self.os_types = ["Windows", "Linux"]
        self.logger = Logger()

    def create_server(self, ip: str) -> IVirtualServer:
        os_type = random.choice(self.os_types)
        self.logger.log_server_creation(ip, os_type)
        return VirtualServer(ip, os_type)
