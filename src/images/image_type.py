from enum import Enum

class ImageType(Enum):
    # The value of each member is the file extension in lowercase
    PNG = "png"
    JPEG = "jpg"
    GIF = "gif"
    BMP = "bmp"
    TIFF = "tiff"
    UNKNOWN = "unknown"  # Only used to detect user errors

    # Includes the '.'
    def to_extension(self) -> str:
        return f".{self.value}"
    
    def get_possible_extensions(self) -> str:
        if self == ImageType.JPEG:
            return ["jpg", "jpeg"]
        
        return [self.value]

    # Will remove a '.' at the start
    # Case insensitive
    @staticmethod
    def from_extension(extension: str) -> "ImageType":
        if extension.startswith('.'):
            extension = extension[1:]

        match extension.lower():
            case "png":
                return ImageType.PNG
            case "jpg" | "jpeg":
                return ImageType.JPEG
            case "gif":
                return ImageType.GIF
            case "bmp":
                return ImageType.BMP
            case "tiff":
                return ImageType.TIFF
            case _:
                return ImageType.UNKNOWN
