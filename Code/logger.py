import logging
from datetime import datetime

class Logger:
    _instance = None

    def __new__(cls, log_file="..//Logs//system.log"):
        if cls._instance is None:
            cls._instance = super(Logger, cls).__new__(cls)
            cls._instance._initialize(log_file)
        return cls._instance

    def _initialize(self, log_file):
        self.logger = logging.getLogger("CentralManagementServer")
        self.logger.setLevel(logging.DEBUG)

        # Check if the logger already has handlers to avoid duplicates
        if not self.logger.handlers:
            file_handler = logging.FileHandler(log_file)
            file_handler.setLevel(logging.DEBUG)

            formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
            file_handler.setFormatter(formatter)

            self.logger.addHandler(file_handler)

    def log_activity(self, activity: str, level: str = "INFO"):
        log_levels = {
            "DEBUG": self.logger.debug,
            "INFO": self.logger.info,
            "WARNING": self.logger.warning,
            "ERROR": self.logger.error,
            "CRITICAL": self.logger.critical
        }
        log_function = log_levels.get(level.upper(), self.logger.info)
        log_function(activity)

    def log_command(self, ip: str, command: str):
        self.log_activity(f"Command executed on {ip}: {command}")

    def log_connection(self, source_ip: str, destination_ip: str):
        self.log_activity(f"Connection established from {source_ip} to {destination_ip}")

    def log_server_creation(self, ip: str, os_type: str):
        self.log_activity(f"New virtual server created - IP: {ip}, OS: {os_type}")