from PIL import Image as PILImage
from io import BytesIO
from images.image import Image
from images.image_type import ImageType

decoders = {}

def init() -> None:
    register_decoder(ImageType.PNG, decode_with_pil)
    register_decoder(ImageType.JPEG, decode_with_pil)
    register_decoder(ImageType.GIF, decode_with_pil)
    register_decoder(ImageType.BMP, decode_with_pil)
    register_decoder(ImageType.TIFF, decode_with_pil)

def register_decoder(file_type: ImageType, decoder) -> None:
    decoders[file_type] = decoder

def decode_image(img_type: ImageType, file: bytes) -> Image:
    return decoders[img_type](file)

#region Decoder Functions

# Generic PIL decoder
def decode_with_pil(file: bytes) -> Image:
    pil_image = PILImage.open(BytesIO(file)).convert("RGBA")  # Force RGBA32
    width, height = pil_image.size
    data = pil_image.tobytes()
    return Image(width, height, data)

#endregion
