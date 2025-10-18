from enum import Enum

# TODO: how to map file extensions to image type?
class ImageType(Enum):
    # The value of each member is the file extension in lowercase
    PNG = "png"
    JPEG = "jpg"
    # TODO: add support for the below
    #GIF = "gif"
    #BMP = "bmp"
    #TIFF = "tiff"
    #WEBP = "webp"
    UNKNOWN = "unknown"  # Only used to detect user errors

    # Doesn't include the '.'
    def to_extension(self) -> str:
        return self.value

    # Do not include a '.' at the start (e.g. '.png' is wrong)
    # Case insensitive
    @staticmethod
    def extension_to_img_type(extension: str) -> "ImageType":
        match extension.lower():
            case "png":
                return ImageType.PNG
            case "jpg" | "jpeg":
                return ImageType.JPEG
            case _:
                return ImageType.UNKNOWN
