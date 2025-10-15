import commands
import tui

def init() -> None:
    commands.init()

def main() -> None:
    # Execute commands continuously until the user wants to exit
    while True:
        tui.run_loop()

if __name__ == "__main__":
    init()
    main()
