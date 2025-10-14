import tui
import images.converter as converter

# Initialized later
commands = {} # Command name -> command
command_descriptions = {}  # Command name -> description
name_to_aliases = {}  # Command name -> aliases
alias_to_name = {}  # Alias -> command name

def init() -> None:
    register_command(quit_command, ["quit", "exit", "q"], "Quit the program")
    register_command(help_command, ["help"], "View a list of all commands and their descriptions")
    register_command(convert_file_command, ["convert-file"], "Convert a single image file")
    register_command(convert_folder_command, ["convert-folder"], "Convert an entire folder of images")

# The first name in command_names will be the primary name and the others are aliases
def register_command(command, command_names: list[str], description: str) -> None:
    commands[command_names[0]] = command
    command_descriptions[command_names[0]] = description

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

    # Call the function with the correct args
    commands[command_name]([] if len(parts) == 1 else parts[1:])
    
#region Commands

def quit_command(args: list[str]) -> None:
    print("Quitting...")
    tui.reset_colors()
    exit(0)

def help_command(args: list[str]) -> None:
    print("Available commands:")
    for cmd in commands.keys():
        # TODO: this is bad, clean this up
        print(f"- {cmd}{'/' if len(name_to_aliases[cmd]) > 0 else ''}{'/'.join(name_to_aliases[cmd]) if len(name_to_aliases[cmd]) > 0 else ''} - {command_descriptions[cmd]}")

# TODO: impl
def convert_file_command(args: list[str]) -> None:
    if len(args) != 1:
        tui.error("convert-file requires exactly one argument, the file path")
        return

    converter.convert_file(args[0])
    
# TODO: impl
def convert_folder_command(args: list[str]) -> None:
    if len(args) != 1:
        tui.error("convert-folder requires exactly one argument, the folder path")
        return

    converter.convert_folder(args[0])

#endregion
