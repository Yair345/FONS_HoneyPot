from main_server import CentralManagementServer

cms = CentralManagementServer("10.7.3.86", "21", 5)

def main():
    user_input = input()
    while user_input != "EXIT":
        print(cms.process_attacker_input(user_input))
        user_input = input()


if __name__ == "__main__":
    main()