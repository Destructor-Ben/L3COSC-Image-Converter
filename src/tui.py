import commands

ESCAPE_CHAR = "\033["

USER_INPUT_COLOR = (255, 255, 0)
INPUT_PROMPT_COLOR = (80, 170, 255)
TEXT_COLOR = (255, 255, 255)
ERROR_COLOR = (255, 0, 0)
PROGRESS_COLOR = (148, 171, 247)

def run_loop() -> None:
    set_text_color(INPUT_PROMPT_COLOR)
    print("Enter a command > ", end="")

    set_text_color(USER_INPUT_COLOR)
    user_input = input()

    set_text_color(TEXT_COLOR)
    commands.parse_command(user_input)

def update_conversion_state(num_converted: int, total_to_convert: int, file: str, file_is_converted: bool) -> None:
    # Clear the current line (will be the progress bar)
    print(f"{ESCAPE_CHAR}2K", end="\r")

    if file_is_converted:
        print(f"Converted {file}")
    else:
        print(f"Converting {file}...")

    # Print the progress bar
    percent = num_converted / total_to_convert * 100
    bar_length = 15
    filled_length = int(bar_length * num_converted // total_to_convert)
    bar = '=' * filled_length + '-' * (bar_length - filled_length)
    set_text_color(PROGRESS_COLOR)
    print(f"[{bar}] {percent:.0f}% ({num_converted}/{total_to_convert})", end="", flush=True)
    set_text_color(TEXT_COLOR)

def error(message: str) -> None:
    set_text_color(ERROR_COLOR)
    print(f"Error: {message}")

def set_text_color(color: tuple[int, int, int]) -> None:
    print(f"{ESCAPE_CHAR}38;2;{color[0]};{color[1]};{color[2]}m", end="")

def reset_colors() -> None:
    print(f"{ESCAPE_CHAR}0m", end="")
