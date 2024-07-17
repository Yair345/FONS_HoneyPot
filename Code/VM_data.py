from content_generator import DynamicContentGenerator


data = {}
commands = ["ls"]

def command_output(ip:str, command:str):
    if command not in commands:
        return f"{command} is not supported in our cmd"
    return functions[command.split()[0]](ip, command)

def ls(ip:str, command:str):
    if ip not in data.keys():
        data[ip] = DynamicContentGenerator.generate_files()

    output = ""
    keys = list(data[ip].keys())
    for i in range(0, len(keys), 5):
        line = keys[i:i + 5]
        output += "  ".join(line) + "\n"

    return output


functions = {'ls': ls}