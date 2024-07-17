from main_server import CentralManagementServer
from logger import Logger

cms = CentralManagementServer("10.7.3.86", "21", 5)
logger = Logger()

def main():
    logger.log_activity("Access point started")
    print(f"┌──((yair㉿shlomi)-[/{cms.get_path()} ~]")
    print("└─$ ", end='')
    user_input = input()
    while user_input != "EXIT":
        print(cms.process_attacker_input(user_input))
        print(f"┌──((yair㉿shlomi)-[/{cms.get_path()} ~]")
        print("└─$ ", end='')
        user_input = input()


if __name__ == "__main__":
    main()