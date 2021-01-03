"""
The following code is from the Legofy github repo.
Modified a bit to make it some "sort of a PIL module" instead of just a CLI.
Original repo: https://github.com/JuanPotato/Legofy/
"""

import gc
from PIL import Image, ImageSequence
from io import BytesIO
from os.path import abspath
static_brick_image = Image.open(abspath("./framework/1x1.png"))

def apply_color_overlay(image, color):
    overlay_red, overlay_green, overlay_blue = color
    channels = image.split()
    r = channels[0].point(lambda color: overlay_effect(color, overlay_red))
    g = channels[1].point(lambda color: overlay_effect(color, overlay_green))
    b = channels[2].point(lambda color: overlay_effect(color, overlay_blue))
    channels[0].paste(r)
    channels[1].paste(g)
    channels[2].paste(b)
    return Image.merge(image.mode, channels)

def overlay_effect(color, overlay):
    if color < 33: return overlay - 100
    elif color > 233: return overlay + 100
    else: return overlay - 133 + color

def make_lego_image(thumbnail_image, brick_image):
    base_width, base_height = thumbnail_image.size
    brick_width, brick_height = brick_image.size
    if thumbnail_image.mode not in ["RGB", "RGBA"]:
        thumbnail_image = thumbnail_image.convert("RGB")
    lego_image = Image.new(thumbnail_image.mode, (base_width * brick_width, base_height * brick_height), "white" if thumbnail_image.mode != "RGBA" else (0, 0, 0, 0))
    for brick_x in range(base_width):
        for brick_y in range(base_height):
            color = thumbnail_image.getpixel((brick_x, brick_y))
            if color == (0, 0, 0, 0):
                continue
            
            lego_image.paste(apply_color_overlay(brick_image, color[:3]), (brick_x * brick_width, brick_y * brick_height))
    return lego_image

def get_new_size(base_image, brick_image, size=None):
    new_size = base_image.size
    if size:
        scale_x, scale_y = size, size
    else:
        scale_x, scale_y = brick_image.size

    if new_size[0] > scale_x or new_size[1] > scale_y:
        scale = (new_size[1] / scale_y) if (new_size[0] < new_size[1]) else (new_size[0] / scale_x)

        new_size = (int(round(new_size[0] / scale)) or 1, int(round(new_size[1] / scale)) or 1)

    return new_size

def legofy_image(base_image, brick_image, output_path, size, palette_mode, dither):
    new_size = get_new_size(base_image, brick_image, size)
    base_image.thumbnail(new_size, Image.ANTIALIAS)
    return make_lego_image(base_image, brick_image)

def main(base_image):
    brick_image = static_brick_image.copy()

    if hasattr(base_image, "is_animated") and base_image.is_animated:
        base_image.seek(0)
    img = legofy_image(base_image, brick_image, "result.png", None, None, False)
    base_image.close()
    brick_image.close()
    del base_image, brick_image
    
    _bytes = BytesIO()
    img.save(_bytes, format="PNG")
    _bytes.seek(0)
    del img
    gc.collect()
    return _bytes

async def legofy(url: str, session):
    resp = await session.get(url)
    byte = await resp.read()
    image = Image.open(BytesIO(byte))
    if url.startswith("https://twemoji.maxcdn.com"):
        image = image.convert("RGBA")
    
    res = main(image)
    del image, byte, resp, session
    gc.collect()
    return res