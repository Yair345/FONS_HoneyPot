from abc import ABC, abstractmethod
import ipaddress
from active_servers import ActiveServers
from virtual_server_factory import VirtualServerFactory
from logger import Logger
from content_generator import DynamicContentGenerator

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

    def __init__(self, ip, mask, number_of_hosts):
        self.ip = ip
        self.mask = mask
        self.network = ipaddress.ip_network(f"{self.ip}/{self.mask}", strict=False)
        self.optional_hosts = DynamicContentGenerator.generate_ip_addresses(self.network, number_of_hosts, [ip])
        self.virtual_server_factory = VirtualServerFactory()
        self.active_servers = ActiveServers()
        self.servers_path = [ip]

        self.logger = Logger()

    def process_attacker_input(self, input: str):
        self.logger.log_activity(f"Received input: {input}")

        if not self.active_servers.get_current_server():
            server = self.virtual_server_factory.create_server(self.ip)
            self.active_servers.add_server(self.ip, server)
            self.active_servers.set_current_server(self.ip)

        if input.startswith("ssh"):
            try:
                new_ip = input.split()[1]
            except:
                error_msg = "ssh: need to provide ip to connect"
                self.logger.log_activity(error_msg, "ERROR")
                return error_msg

            if new_ip not in self.optional_hosts:
                error_msg = f"ssh: connect to host {new_ip} port 22: No route to host"
                self.logger.log_activity(error_msg, "ERROR")
                return error_msg

            server = self.virtual_server_factory.create_server(new_ip)
            self.active_servers.add_server(new_ip, server)
            self.active_servers.set_current_server(new_ip)
            self.servers_path.append(new_ip)

            self.logger.log_connection(self.servers_path[-2], new_ip)
            self.logger = Logger()

            return f"ssh: connect to host {new_ip} port 22: Connection succeed"

        if input.startswith("exit"):
            if len(self.servers_path) < 2:
                error_msg = "ERROR: Cannot exit from the root server"
                self.logger.log_activity(error_msg, "ERROR")
                return error_msg

            self.servers_path.pop()
            self.active_servers.set_current_server(self.servers_path[-1])
            return f"Connected to {self.servers_path[-1]}"

        if input.startswith("nmap"):
            try:
                network = input.split()[1]
            except:
                error_msg = "nmap: need to provide network address to search"
                self.logger.log_activity(error_msg, "ERROR")
                return error_msg

            input_net = ipaddress.ip_network(network, strict=False)

            if not input_net.subnet_of(self.network):
                error_msg = "Network is not a subnet of the current network"
                self.logger.log_activity(error_msg, "ERROR")
                return error_msg

            output = f"Starting Nmap 7.94SVN\n"

            for ip in self.optional_hosts:
                output += f"Nmap scan report for {ip}\n"
                output += f"Host is up (0.000085s latency).\n"
                output += f"All 1000 scanned ports on {ip} are in ignored states.\n"
                output += "Not shown: 1000 closed tcp ports (conn-refused)\n\n"

            output += f"Nmap done: {len(self.optional_hosts)} IP address{'es' if len(self.optional_hosts) != 1 else ''} scanned\n"

            return output

        return self.active_servers.get_current_server().execute_command(input)

    def get_path(self):
        return "/".join(self.servers_path)

    def update_simulation(self):
        pass

    def log_activity(self, activity: str):
        self.logger.log_activity(activity)

