from abc import ABC, abstractmethod
from VM_data import command_output
from logger import Logger

class IVirtualServer(ABC):
    @abstractmethod
    def execute_command(self, command: str):
        pass

class VirtualServer(IVirtualServer):

    def __init__(self, ip: str, os: str):
        self.ip_address = ip
        self.os_type = os
        self.services = []
        self.logger = Logger()

    def execute_command(self, command: str):
        output = command_output(self.ip_address, command)
        if output.startswith("ERROR") or output.endswith("is not supported in our cmd"):
            self.logger.log_activity(f"Command execution error on {self.ip_address}: {command}", "ERROR")
        return output
