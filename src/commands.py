import tui
import images.converter as converter

from images.image_type import ImageType
from pathlib import Path

commands = {} # Command name -> command
command_descriptions = {}  # Command name -> description
name_to_aliases = {}  # Command name -> aliases
alias_to_name = {}  # Alias -> command name

# Output type settings (e.g. jpeg quality)
# - set these in dedicated commands

def init() -> None:
    register_command(quit_command, ["quit", "exit", "q"], "Quit the program")
    register_command(help_command, ["help"], "View a list of all commands and their descriptions")
    register_command(supported_formats_command, ["supported-formats"], "View a list of the supported image formats")
    register_command(convert_file_command, ["convert-file", "cfi"],
                     "Convert a single image file to a different image type\n" \
                     "Usage: convert-file [Target file extension] [Source file path] [Target file path (Optional)]")
    register_command(convert_folder_command, ["convert-folder", "cfo"],
                     "Convert an entire folder of images to a different image type\n" \
                     "Usage: convert-folder [Target file extension] [Source folder path] [Target folder path (Optional)]")

# The first name in command_names will be the primary name and the others are aliases
def register_command(command, command_names: list[str], description: str) -> None:
    commands[command_names[0]] = command
    command_descriptions[command_names[0]] = description

    # Map aliases
    name_to_aliases[command_names[0]] = command_names[1:]

    for name in command_names:
        alias_to_name[name] = command_names[0]

def parse_command(user_input: str) -> None:
    user_input = user_input.strip()
    tokens = tokenize(user_input)

    # Error, already handled in tokenize
    if tokens is None:
        return

    if len(tokens) < 1:
        tui.error("No command provided")
        return
    
    command_name = tokens[0].lower()
    if command_name not in commands.keys() and command_name not in alias_to_name.keys():
        tui.error(f"Unknown command: {command_name}")
        return

    # Map alias to command name
    if command_name in alias_to_name.keys():
        command_name = alias_to_name[command_name]

    # Call the function with the correct args
    commands[command_name]([] if len(tokens) == 1 else tokens[1:])

# Perform lexical analysis on the string to convert it to tokens (accounting for quotation marks)
def tokenize(user_input: str) -> list[str] | None:
    tokens = []
    current = ''
    in_quotes = False  # This basically just controls whether spaces will be added and is toggled when a quote is hit
    quote_char = ''
    next_character_must_be_space = False

    for i in range(len(user_input)):
        c = user_input[i]

        # This character is after a quote, so it must be a space
        if next_character_must_be_space:
            next_character_must_be_space = False
            if c != ' ':
                tui.error(f"Missing space between token and quote at index {i}")
                return None

        # Add a finished token if it isn't empty
        if c == ' ' and not in_quotes:
            if current != '':
                tokens.append(current)
                current = ''
                continue
            else:
                continue

        # Toggle in_quotes if we hit a quote character
        if c in ['"', "'"]:
            # End quote
            if quote_char == c:
                in_quotes = False
                quote_char = ''
                next_character_must_be_space = True
                continue

            # Start quote
            if quote_char == '':
                # Case like this: asd'asd'
                if current != '':
                    tui.error(f"Missing space between token and quote at index {i}")
                    return None

                in_quotes = True
                quote_char = c
                continue
        
        # Add the next char to the current token
        current += c

    # Detect unfinished quotes
    if in_quotes:
        tui.error(f"Unfinished quoted string: {quote_char}{current}")
        return None

    # Add any leftover tokens
    if current != '':
        tokens.append(current)

    return tokens

#region Commands

def quit_command(args: list[str]) -> None:
    print("Quitting...")
    tui.reset_colors()
    exit(0)

def help_command(args: list[str]) -> None:
    print("Available commands:")
    for cmd in commands.keys():
        has_aliases = len(name_to_aliases[cmd]) > 0
        if has_aliases:
            command_names = '/'.join([cmd] + name_to_aliases[cmd])
        else:
            command_names = cmd

        # Ensure that multiple lines have the same indentation of the first line
        first_line_prefix = f"- {command_names} - "
        indentation = " " * len(first_line_prefix)
        description_lines = command_descriptions[cmd].split("\n")

        print(f"{first_line_prefix}{description_lines[0]}")
        for line in description_lines[1:]:
            print(f"{indentation}{line}")

def supported_formats_command(args: list[str]) -> None:
    print("Supported formats:")
    
    for format in ImageType:
        if format == ImageType.UNKNOWN:
            continue

        extension_list = "/".join(format.get_possible_extensions())
        print(f"- {extension_list}")

def convert_file_command(args: list[str]) -> None:
    arg_count = len(args)
    if arg_count != 2 and arg_count != 3:
        tui.error(f"Incorrect number of arguments supplied ({arg_count} instead of 2 or 3)")
        return
    
    image_type = ImageType.from_extension(args[0])
    if image_type == ImageType.UNKNOWN:
        tui.error(f"Unknown image type: {args[0]}")
        return

    input_file = args[1]
    output_file = args[2] if arg_count == 3 else None

    converter.convert_file(image_type, input_file, output_file)

def convert_folder_command(args: list[str]) -> None:
    arg_count = len(args)
    if arg_count != 2 and arg_count != 3:
        tui.error(f"Incorrect number of arguments supplied ({arg_count} instead of 2 or 3)")
        return
    
    image_type = ImageType.from_extension(args[0])
    if image_type == ImageType.UNKNOWN:
        tui.error(f"Unknown image type: {args[0]}")
        return

    input_folder = args[1]
    output_folder = args[2] if arg_count == 3 else None

    converter.convert_folder(image_type, input_folder, output_folder)

#endregion
