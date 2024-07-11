from abc import ABC, abstractmethod
from VM_data import command_output

class IVirtualServer(ABC):
    @abstractmethod
    def execute_command(self, command: str):
        pass

    @abstractmethod
    def get_system_info(self):
        pass

    @abstractmethod
    def simulate_service(self, service: str):
        pass

class VirtualServer(IVirtualServer):

    def __init__(self, ip: str, os: str):
        self.ip_address = ip
        self.os_type = os
        self.services = []

    def execute_command(self, command: str):
        return command_output(self.ip_address, command)

    def get_system_info(self):
        pass

    def simulate_service(self, service: str):
        if service in self.services:
            return "run"
