from abc import ABC, abstractmethod
import ipaddress
from active_servers import ActiveServers
from virtual_server_factory import VirtualServerFactory

class ICentralManager(ABC):
    @abstractmethod
    def process_attacker_input(self, input: str):
        pass

    @abstractmethod
    def update_simulation(self):
        pass

    @abstractmethod
    def log_activity(self, activity: str):
        pass

class CentralManagementServer(ICentralManager):

    def __init__(self, ip, mask):
        self.ip = ip
        self.mask = mask
        self.network = ipaddress.ip_network(f"{self.ip}/{self.mask}", strict=False)
        self.virtual_server_factory = VirtualServerFactory()
        self.active_servers = ActiveServers()

    def process_attacker_input(self, input: str):
        if input.startswith("ssh"):
            new_ip = input.split()[1]
            server = self.virtual_server_factory.create_server(new_ip)
            self.active_servers.add_server(new_ip, server)
            self.active_servers.set_current_server(new_ip)
            return f"Moved to {new_ip}"

        if not self.active_servers.get_current_server():
            server = self.virtual_server_factory.create_server(self.ip)
            self.active_servers.add_server(self.ip, server)
            self.active_servers.set_current_server(self.ip)

        return self.active_servers.get_current_server().execute_command(input)


    def update_simulation(self):
        pass

    def log_activity(self, activity: str):
        pass