from PIL import Image as PILImage
from io import BytesIO
from images.image import Image
from images.image_type import ImageType

encoders = {}

def init() -> None:
    register_encoder(ImageType.PNG, get_encode_with_pil("PNG"))
    register_encoder(ImageType.JPEG, get_encode_with_pil("JPEG"))
    register_encoder(ImageType.GIF, get_encode_with_pil("GIF"))

def register_encoder(file_type: ImageType, encoder) -> None:
    encoders[file_type] = encoder

def encode_image(img_type: ImageType, img: Image) -> bytes:
    return encoders[img_type](img)

#region Encoder Functions

# Generic PIL encoder
def get_encode_with_pil(format: str):
    def encode_with_pil(img: Image) -> bytes:
        pil_image = PILImage.frombytes("RGBA", (img.width, img.height), img.data)

        # JPEG doesn't have alpha channel
        if format == "JPEG":
            pil_image = pil_image.convert("RGB")

        buffer = BytesIO()
        pil_image.save(buffer, format=format)
        return buffer.getvalue()
    
    return encode_with_pil


#endregion
