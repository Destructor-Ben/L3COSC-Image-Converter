from PIL import Image as PILImage
from image import Image
from image_type import ImageType

decoders = {}

def register_decoder(file_type: ImageType, decoder):
    decoders[file_type] = decoder

# TODO: call this
def init_decoders():
    register_decoder(ImageType.PNG, decode_with_pil)
    register_decoder(ImageType.JPEG, decode_with_pil)
    # TODO: finish setting up

# Generic PIL decoder
def decode_with_pil(file) -> Image:
    pil_image = PILImage.open(file)
    width, height = pil_image.size
    data = pil_image.tobytes()
    return Image(width, height, data)
