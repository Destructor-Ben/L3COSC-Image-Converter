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
target_image_type: str = ''

# The 2 functions below queue files to be converted on files_to_convert

# Path can be relative or absolute
def convert_file(target_type: ImageType, src_path: str, dst_path: str | None) -> None:
    global files_to_convert
    global target_image_type

    src_extension = Path(src_path).suffix
    src_extension = ImageType.from_extension(src_extension)
    # TODO: check that src_path exists and that dst_path isn't the same as src_path
    # TODO: function to change extension?
    # TODO: function to check if the src file exists, target file doesn't (unless exact path specified), and that both aren't the same
    target_path = Path(src_path).with_suffix(f".{target_type.to_extension()}")

    files_to_convert.append(FileToConvert(src_path, target_path.as_posix()))

    target_image_type = target_type
    process_files()

# TODO: queue each file in the folder
def convert_folder(target_type: ImageType, src_folder: str, dst_folder: str | None) -> None:
    global files_to_convert
    global target_image_type

    files_to_convert.append(src_folder)
    files_to_convert.append(src_folder)
    files_to_convert.append(src_folder)
    files_to_convert.append(src_folder)
    files_to_convert.append(src_folder)
    files_to_convert.append(src_folder)
    files_to_convert.append(src_folder)
    target_image_type = 'png'
    process_files()

# Converts each file in the queue
def process_files() -> None:
    num_converted = 0
    number_of_files = len(files_to_convert)

    for file in files_to_convert:
        tui.update_conversion_state(num_converted, number_of_files, file.src_path, False)
    
        process_file(file.src_path, file.dst_path, file.src_image_type, target_image_type)

        num_converted += 1
        tui.update_conversion_state(num_converted, number_of_files, file.dst_path, True)

    files_to_convert.clear()

    # New line required, since the progress bar doesn't end with a newline
    print()

def process_file(src_path: str, dst_path: str, src_type: ImageType, dst_type: ImageType) -> None:
    with open(src_path, "rb") as file:
        src_bytes = file.read()
    
    # Convert to intermediate Image class then to target type
    image: Image = decoders.decode_image(src_type, src_bytes)
    dst_bytes = encoders.encode_image(dst_type, image)

    with open(dst_path, "wb") as file:
        file.write(dst_bytes)
