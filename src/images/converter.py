import tui
import time
import random

# TODO: think a lot about the different types of inputs:
# File
# - input file (relative/absolute)
# - output file type
# - output file specified (relative/absolute, only works for single file)

# Folder
# - input folder
# - output file type
# - output folder (change input file/folder path to output folder)
# - output folder not specified (put in a new "converted images" folder in cwd)

# Output type settings
# - set these in dedicated commands

files_to_convert: list[str] = []
conversion_type: str = ''

# The functions below queue files to be converted on a conversion list

# Path can be relative or absolute
def convert_file(file_path: str, file_type: str) -> None:
    files_to_convert.append(file_path)
    conversion_type = file_type
    process_files()

# TODO: queue each file in the folder
def convert_folder(folder_path: str) -> None:
    files_to_convert.append(folder_path)
    files_to_convert.append(folder_path)
    files_to_convert.append(folder_path)
    files_to_convert.append(folder_path)
    files_to_convert.append(folder_path)
    files_to_convert.append(folder_path)
    files_to_convert.append(folder_path)
    conversion_type = 'png'
    process_files()

# Converts each file
def process_files() -> None:
    num_converted = 0
    number_of_files = len(files_to_convert)

    for file in files_to_convert:
        tui.update_conversion_state(num_converted, number_of_files, file, False)

        # TODO: actually convert, this is just dummy code
        time.sleep(random.randint(1, 3) / 2)

        num_converted += 1
        tui.update_conversion_state(num_converted, number_of_files, file, True)

    files_to_convert.clear()

    # New line required, since the progress bar doesn't end with a newline
    print()