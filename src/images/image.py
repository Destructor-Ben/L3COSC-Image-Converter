# Intermediate class to simplify the conversion process
# e.g. PNG -> JPEG, PNG -> GIF is replaced
# with PNG -> Image, Image -> JPEG, Image -> GIF
class Image:
    width: int
    height: int
    data: bytes  # Image data in RGBA32 format (1 byte per component)

    def __init__(self, width: int, height: int, data: bytes):
        self.width = width
        self.height = height
        self.data = data
