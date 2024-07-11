from virtual_server import IVirtualServer
from VM_data import command_output

class ActiveServers:

    def __init__(self):
        self.servers = dict()
        self.current_server_ip = ""

    def add_server(self, ip:str, server:IVirtualServer):
        self.servers[ip] = server
        if not self.current_server_ip:
            self.current_server_ip = ip

    def get_server(self, ip:str) -> IVirtualServer:
        if ip in self.servers.keys():
            return self.servers[ip]
        return None

    def set_current_server(self, ip:str):
        if ip in self.servers.keys():
            self.current_server_ip = ip
        else:
            raise ValueError(f"There is no server with ip {ip} in our net")

    def get_current_server(self) -> IVirtualServer:
        if self.is_server_exist(self.current_server_ip):
            return self.servers[self.current_server_ip]
        return None

    def is_server_exist(self, ip:str) -> bool:
        return ip in self.servers.keys()