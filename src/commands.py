# Initialized later
commands = {}

def init():
    register_command(quit_command, "quit")
    register_command(help_command, "help")
    register_command(convert_file_command, "convert-file")
    register_command(convert_folder_command, "convert-folder")

# TODO: add support for aliases
def register_command(command, command_name: str):
    commands[command_name] = command

# TODO: this needs to be able to parse strings in the command args
# TODO: make an error function that ensures newlines are printed after an error/in color to make it clear to the user what is happening
# TODO: perhaps color a bunch of the UI?
def parse_command(user_input: str) -> None:
    user_input = user_input.strip()
    parts = user_input.split()
    if len(parts) < 1:
        print("No command provided.")
        return
    
    command_name = parts[0].lower()
    if command_name not in commands.keys():
        print(f"Unknown command: {command_name}")
        return
    
    # TODO: check if args working
    commands[command_name]([] if len(parts) == 1 else parts[1:])
    
#region Commands

def quit_command(args: list[str]) -> None:
    print("Quitting...")
    exit(0)

def help_command(args: list[str]) -> None:
    print("Available commands:")
    for cmd in commands.keys():
        print(f"- {cmd}")

def convert_file_command(args: list[str]) -> None:
    print("CONVERT FILE")
    
def convert_folder_command(args: list[str]) -> None:
    print("CONVERT FOLDER")

#endregion
