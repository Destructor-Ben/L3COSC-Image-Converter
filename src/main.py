import commands

def init():
    commands.init()

def main():
    # Execute commands continuously until the user wants to exit
    while True:
        user_input = input("Enter a command >")
        commands.parse_command(user_input)

if __name__ == "__main__":
    init()
    main()
