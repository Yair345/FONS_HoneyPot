from abc import ABC, abstractmethod
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
    def generate_command_output(cls, command: str, os: str) -> str:
        if os not in cls.command_outputs.keys():
            return f"Unsupported OS type {os}"
        if command not in cls.command_outputs[os]:
            return f"Command {command} not found"

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
