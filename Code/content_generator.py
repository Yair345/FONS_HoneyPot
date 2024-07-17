from abc import ABC, abstractmethod
from logger import Logger
import ipaddress
import random
import string


class IContentGenerator(ABC):
    @abstractmethod
    def generate_file_content(self, file_type: str):
        pass

    @abstractmethod
    def generate_command_output(self, command: str, os: str) -> str:
        pass

    @abstractmethod
    def create_dynamic_scenario(self):
        pass


class DynamicContentGenerator(IContentGenerator):
    file_templates = {}
    command_outputs = {}

    @classmethod
    def generate_file_content(cls, file_type: str):
        pass

    @classmethod
    @classmethod
    def generate_command_output(cls, command: str, os: str) -> str:
        if os not in cls.command_outputs.keys():
            error_msg = f"Unsupported OS type {os}"
            Logger().log_activity(error_msg, "ERROR")
            return error_msg
        if command not in cls.command_outputs[os]:
            error_msg = f"Command {command} not found"
            Logger().log_activity(error_msg, "ERROR")
            return error_msg

        return cls.command_outputs[os][command]

    @classmethod
    def create_dynamic_scenario(cls):
        pass

    @classmethod
    def generate_files(cls, num_files=10):
        files = {}
        extensions = ['.txt', '.log', '.cfg', '.dat', '.tmp']

        for _ in range(num_files):
            name = ''.join(random.choices(string.ascii_lowercase, k=random.randint(3, 10)))
            ext = random.choice(extensions)
            filename = f"{name}{ext}"
            files[filename] = ""

        return files

    @classmethod
    def generate_ip_addresses(cls, network, num_addresses, existing_ips):
        network = ipaddress.ip_network(network, strict=False)
        existing_ips_set = set(ipaddress.ip_address(ip) for ip in existing_ips)

        new_ips = set()
        while len(new_ips) < num_addresses:
            new_ip = ipaddress.ip_address(random.randint(
                int(network.network_address) + 1,
                int(network.broadcast_address) - 1
            ))

            if new_ip not in existing_ips_set and new_ip not in new_ips:
                new_ips.add(new_ip)

        return [str(ip) for ip in new_ips]
