import commands
import tui
import images.encoders as encoders
import images.decoders as decoders

def init() -> None:
    commands.init()
    encoders.init()
    decoders.init()
    tui.init()

def main() -> None:
    # Execute commands continuously until the user wants to exit
    while True:
        tui.run_loop()

if __name__ == "__main__":
    init()
    main()
