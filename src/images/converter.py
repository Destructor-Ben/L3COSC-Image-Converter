import tui
import time
import random

files_to_convert: list[str] = []

# The functions below queue files to be converted on a conversion list

def convert_file(file_path: str) -> None:
    files_to_convert.append(file_path)
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