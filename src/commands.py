import tui

# Initialized later
commands = {} # Command name -> command
name_to_aliases = {}  # Command name -> aliases
alias_to_name = {}  # Alias -> command name

def init() -> None:
    register_command(quit_command, ["quit", "exit", "q"])
    register_command(help_command, ["help"])
    register_command(convert_file_command, ["convert-file"])
    register_command(convert_folder_command, ["convert-folder"])

# The first name in command_names will be the primary name and the others are aliases
# TODO: add description support
def register_command(command, command_names: list[str]) -> None:
    commands[command_names[0]] = command

    # Map aliases
    name_to_aliases[command_names[0]] = command_names[1:]

    for name in command_names:
        alias_to_name[name] = command_names[0]

# TODO: this needs to be able to parse strings in the command args
# TODO: make an error function that ensures newlines are printed after an error/in color to make it clear to the user what is happening
# TODO: perhaps color a bunch of the UI?
def parse_command(user_input: str) -> None:
    user_input = user_input.strip()
    parts = user_input.split()
    if len(parts) < 1:
        tui.error("No command provided")
        return
    
    command_name = parts[0].lower()
    if command_name not in commands.keys() and command_name not in alias_to_name.keys():
        tui.error(f"Unknown command: {command_name}")
        return

    # Map alias to command name
    if command_name in alias_to_name.keys():
        command_name = alias_to_name[command_name]

    # TODO: check if args working
    commands[command_name]([] if len(parts) == 1 else parts[1:])
    
#region Commands

def quit_command(args: list[str]) -> None:
    print("Quitting...")
    exit(0)

def help_command(args: list[str]) -> None:
    print("Available commands:")
    for cmd in commands.keys():
        # TODO: this is bad, clean this up
        print(f"- {cmd}{'/' if len(name_to_aliases[cmd]) > 0 else ''}{'/'.join(name_to_aliases[cmd]) if len(name_to_aliases[cmd]) > 0 else ''}")

# TODO: impl
def convert_file_command(args: list[str]) -> None:
    print("CONVERT FILE")
    
# TODO: impl
def convert_folder_command(args: list[str]) -> None:
    print("CONVERT FOLDER")

#endregion
