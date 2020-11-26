from PIL import Image, ImageFont, ImageDraw
from io import BytesIO
from random import randint, choice

font = ImageFont.truetype("Ubuntu-B.ttf", size=70)
words = ["is alone", "is empty", "is lost", "declined", "neglected", "kidnapped", "trashed", "died", "crashed", "burned", "closed", "murdered", "hated", "left", "emptied", "is missing", "perished", "killed", "deleted", "dead", "is gone", "lagged", "freezed"]

def invert(rgb):
    return ((0, 0, 0) if (sum(rgb) / 3 > 127.5) else (255, 255, 255))

def generate():
    color = (randint(0, 255), randint(0, 255), randint(0, 255))
    main = Image.new("RGB", (500, 500), color=color)
    draw = ImageDraw.Draw(main)
    draw.text((75, 75), f"server.py\n{choice(words)}.", font=font, fill=invert(color), spacing=10)
    _bytes = BytesIO()
    main.save(_bytes, format="PNG")
    _bytes.seek(0)
    return _bytes.getvalue()