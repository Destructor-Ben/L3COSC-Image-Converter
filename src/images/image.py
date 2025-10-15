# TODO: the image class that is used by the encoders + decoders

class Image:
    width: int
    height: int
    data: bytes

    def __init__(self, width: int, height: int, data: bytes):
        self.width = width
        self.height = height
        self.data = data
