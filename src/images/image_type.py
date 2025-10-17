from enum import Enum

# TODO: how to map file extensions to image type?
class ImageType(Enum):
    PNG = "png"
    JPEG = "jpeg"
    # TODO: add support for the below
    GIF = "gif"
    BMP = "bmp"
    TIFF = "tiff"
    WEBP = "webp"
