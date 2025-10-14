import commands

ESCAPE_CHAR = "\033["

BG_COLOR = (36, 41, 46)
USER_INPUT_COLOR = (255, 255, 0)
TEXT_COLOR = (255, 255, 255)
ERROR_COLOR = (255, 0, 0)

def init() -> None:
    set_bg_color(BG_COLOR)

def run_loop() -> None:
    set_text_color(TEXT_COLOR)
    print("Enter a command > ", end="")

    set_text_color(USER_INPUT_COLOR)
    user_input = input()

    set_text_color(TEXT_COLOR)
    commands.parse_command(user_input)

def update_conversion_state(num_converted: int, total_to_convert: int, recently_converted_file: str | None) -> None:
    percent = num_converted / total_to_convert * 100

    # Clear the current line (will be the progress bar)
    print(f"{ESCAPE_CHAR}2K", end="\r")

    if recently_converted_file is not None:
        print(f"Converted {recently_converted_file}")

    # Print the progress bar
    bar_length = 30
    filled_length = int(bar_length * num_converted // total_to_convert)
    bar = '█' * filled_length + '-' * (bar_length - filled_length)
    print(f"Progress: |{bar}| {percent:.0f}% ({num_converted}/{total_to_convert})", end="")

def error(message: str) -> None:
    set_text_color(ERROR_COLOR)
    print(f"Error: {message}")

def set_text_color(color: tuple[int, int, int]) -> None:
    print(f"{ESCAPE_CHAR}38;2;{color[0]};{color[1]};{color[2]}m", end="")

# TODO: test this
def set_bg_color(color: tuple[int, int, int]) -> None:
    print(f"{ESCAPE_CHAR}48;2;{color[0]};{color[1]};{color[2]}m", end="")
