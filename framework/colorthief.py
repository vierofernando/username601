# this is a custom color thief made by me,
# since the PyPI version of ColorThief seems to a bit inaccurate.
# NOTE: this only generates a SINGLE color.

from io import BytesIO
from requests import get
from PIL import Image

class Smart_ColorThief:
    def __image_from_url(self, url):
        return Image.open(BytesIO(get(url).content))

    def __init__(self, url, quality=50) -> None:
        """
        Initiation.
        The higher the quality, the more accurate, but the longer the time to process.
        """
        self.image = self.__image_from_url(url).resize((quality, quality))
    
    def get_color(self, right=False) -> tuple:
        """Gets the color accent."""

        if right:
            res = []
            for i in range(self.image.height):
                for j in range(self.image.width):
                    res.append(self.image.getpixel((self.image.width-1, i)))
        else:
            arr_L, arr_R, arr_T, arr_B = [], [], [], []
            for i in range(self.image.height):
                for j in range(self.image.width):
                    arr_L.append(self.image.getpixel((0, i)))
                    arr_R.append(self.image.getpixel((self.image.width-1, i)))
                    arr_T.append(self.image.getpixel((j, 0)))
                    arr_B.append(self.image.getpixel((j, self.image.height-1)))
            res = arr_L + arr_R + arr_T + arr_B
        return max(set(res), key=res.count)