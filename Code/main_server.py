from abc import ABC, abstractmethod
import ipaddress
from active_servers import ActiveServers
from virtual_server_factory import VirtualServerFactory
import random

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
        self.optional_hosts = generate_ip_addresses(self.network, number_of_hosts, [ip])
        self.virtual_server_factory = VirtualServerFactory()
        self.active_servers = ActiveServers()
        self.servers_path = [ip]

    def process_attacker_input(self, input: str):
        if not self.active_servers.get_current_server():
            server = self.virtual_server_factory.create_server(self.ip)
            self.active_servers.add_server(self.ip, server)
            self.active_servers.set_current_server(self.ip)

        if input.startswith("ssh"):
            new_ip = input.split()[1]
            if new_ip not in self.optional_hosts:
                return f"ssh: connect to host {new_ip} port 22: No route to host"
            server = self.virtual_server_factory.create_server(new_ip)
            self.active_servers.add_server(new_ip, server)
            self.active_servers.set_current_server(new_ip)
            self.servers_path.append(new_ip)
            return f"ssh: connect to host {new_ip} port 22: Connection succeed"

        if input.startswith("exit"):
            if len(self.servers_path) < 2:
                return "ERROR"
            self.servers_path.pop()
            self.active_servers.set_current_server(self.servers_path[-1])
            return f"Connected to {self.servers_path[-1]}"

        if input.startswith("nmap"):
            network = input.split()[1]

            output = f"Starting Nmap 7.94SVN\n"

            for ip in self.optional_hosts:
                output += f"Nmap scan report for {ip}\n"
                output += f"Host is up (0.000085s latency).\n"
                output += f"All 1000 scanned ports on {ip} are in ignored states.\n"
                output += "Not shown: 1000 closed tcp ports (conn-refused)\n\n"

            output += f"Nmap done: {len(self.optional_hosts)} IP address{'es' if len(self.optional_hosts) != 1 else ''} scanned\n"

            return output

        return self.active_servers.get_current_server().execute_command(input)


    def update_simulation(self):
        pass

    def log_activity(self, activity: str):
        pass


def generate_ip_addresses(network, num_addresses, existing_ips):

    network = ipaddress.ip_network(network, strict=False)
    existing_ips_set = set(ipaddress.ip_address(ip) for ip in existing_ips)

    # Generate new IP addresses
    new_ips = set()

    while len(new_ips) < num_addresses:
        # Generate a random IP within the network
        new_ip = ipaddress.ip_address(random.randint(
            int(network.network_address) + 1,
            int(network.broadcast_address) - 1
        ))

        # Check if it's not in existing IPs and not already generated
        if new_ip not in existing_ips_set and new_ip not in new_ips:
            new_ips.add(new_ip)

    # Convert IP addresses to strings
    return [str(ip) for ip in new_ips]