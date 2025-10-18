import tui
import images.decoders as decoders
import images.encoders as encoders
import os

from images.image import Image
from images.image_type import ImageType
from pathlib import Path

class FileToConvert:
    # Both of these include the file extension
    src_path: str
    dst_path: str
    src_image_type: ImageType

    def __init__(self, src_path: str, dst_path: str, src_image_type: ImageType):
        self.src_path = src_path
        self.dst_path = dst_path
        self.src_image_type = src_image_type

files_to_convert: list[FileToConvert] = []
target_image_type: ImageType = ImageType.UNKNOWN

# The 2 functions below queue files to be converted on files_to_convert

# Path can be relative or absolute
def convert_file(target_type: ImageType, src_path: str, dst_path: str | None) -> None:
    global files_to_convert
    global target_image_type

    if not os.path.isfile(src_path):
        tui.error(f"The file '{src_path}' does not exist")
        return
    
    # Default destination path
    if dst_path is None:
        dst_path = change_extension(src_path, target_type.to_extension())

    if get_image_type(dst_path) != target_type:
        tui.error(f"Desination file extension doesn't match target image type")
        return

    src_extension = get_image_type(src_path)
    files_to_convert.append(FileToConvert(src_path, dst_path, src_extension))

    target_image_type = target_type
    process_files()

def convert_folder(target_type: ImageType, src_folder: str, dst_folder: str | None) -> None:
    global files_to_convert
    global target_image_type

    if not os.path.isdir(src_folder):
        tui.error(f"The folder '{src_folder}' does not exist")
        return
    
    # Default destination folder
    if dst_folder is None:
        dst_folder = "converted/"
    
    if not os.path.exists(dst_folder):
        os.makedirs(dst_folder, exist_ok=True)

    # Recurse through src_folder, change extension and path, and add images to the queue
    src_path = Path(src_folder)
    dst_path_root = Path(dst_folder)
    for src_file in src_path.rglob("*"):
        if not src_file.is_file():
            continue

        # Calculate the destination file name
        rel_path = src_file.relative_to(src_path)
        new_name = change_extension(rel_path.stem, target_type.to_extension())
        dst_file = dst_path_root / rel_path.parent / new_name
        
        print(f"{src_file.as_posix()} -> {dst_file.as_posix()}")

        src_extension = get_image_type(src_file)
        files_to_convert.append(FileToConvert(src_file.as_posix(), dst_file.as_posix(), src_extension))

    target_image_type = target_type
    process_files()

# Converts each file in the queue
def process_files() -> None:
    num_converted = 0
    number_of_files = len(files_to_convert)

    if number_of_files <= 0:
        print("Warning: No files to convert")
        return

    for file in files_to_convert:
        tui.update_conversion_state(num_converted, number_of_files, file.src_path, False)
    
        error = process_file(file.src_path, file.dst_path, file.src_image_type, target_image_type)
        if not error is None:
            print()
            tui.error(error)
            files_to_convert.clear()
            return

        num_converted += 1
        tui.update_conversion_state(num_converted, number_of_files, file.dst_path, True)

    files_to_convert.clear()

    # New line required, since the progress bar doesn't end with a newline
    print()

# Returns an error string if it fails
def process_file(src_path: str, dst_path: str, src_type: ImageType, dst_type: ImageType) -> None | str:
    try:
        with open(src_path, "rb") as file:
            src_bytes = file.read()
        
        # Convert to intermediate Image class then to target type
        image: Image = decoders.decode_image(src_type, src_bytes)
        dst_bytes = encoders.encode_image(dst_type, image)

        # Directory needs to be created before writing to file
        dst_dir = os.path.dirname(dst_path)
        if dst_dir and not os.path.exists(dst_dir):
            os.makedirs(dst_dir, exist_ok=True)

        with open(dst_path, "wb") as file:
            file.write(dst_bytes)
    except PermissionError:
        return f"Insufficient permissions to read/write to source or destination file"
    except Exception:
        return "An unknown error occurred"

def change_extension(path: str, new_extension: str) -> str:
    return Path(path).with_suffix(new_extension).as_posix()

def get_image_type(path: str) -> ImageType:
    return ImageType.from_extension(Path(path).suffix)
