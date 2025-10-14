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
# TODO: temp, test string: asd asd "asd" 'asd' asd"asd" asd'asd' "asd"asd 'asd'asd 'asd "asd"' "asd 'asd'"
# TODO: test lots of spaces, indivudual quotes, in each of the above examples, and unfinished quotes, and fiffereing quotes e.g. 'asd"
# TODO: handle escaped quotes
# TODO: handle asd'asd' and asd"asd"
def tokenize(user_input: str) -> list[str] | None:
    tokens = []
    current = ''
    in_quotes = False  # This basically just controls whether spaces will be added and is toggled when a quote is hit
    quote_char = ''

    for c in user_input:
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
                # TODO: ensure that the next char is a space
                in_quotes = False
                quote_char = ''
                continue

            # Start quote
            if quote_char == '':
                # Case like this: asd'asd'
                if current != '':
                    tui.error(f"Missing space between token and quote: {current}{c}")
                    return None

                in_quotes = True
                quote_char = c
                continue
        
        # Add the next char to the current token
        current += c

    # Add any leftover tokens if we aren't in a quote
    # TODO: test - this doesn't work with a trailing quote
    # TODO: test trailing quotes: "'" and "asd asd '"
    if current != '':
        if in_quotes:
            tui.error(f"Unfinished quoted string in input: {quote_char}{current}")
            return None
        else:
            tokens.append(current)

    # TODO: temporary
    for token in tokens:
        print("- " + token)

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

        print(f"- {command_names} - {command_descriptions[cmd]}")

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
