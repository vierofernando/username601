# this is a custom color thief made by me,
# since the PyPI version of ColorThief seems to a bit inaccurate.
# NOTE: this only generates a SINGLE color.

from io import BytesIO
from PIL import Image

class Smart_ColorThief:
    async def __get_image(self):
        res = await self.ctx.bot.util.default_client.get(self.url)
        res = await res.read()
        self.image = Image.open(BytesIO(res)).resize((self.quality, self.quality))
        del res

    def __init__(self, ctx, url: str, quality: int = 50) -> None:
        """
        Initiation.
        The higher the quality, the more accurate, but the longer the time to process.
        """
        self.ctx = ctx
        self.url = url
        self.quality = quality
    
    async def get_color(self, right=False) -> tuple:
        """Gets the color accent."""
        await self.__get_image()

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
            del arr_L, arr_R, arr_T, arr_B
        total = max(set(res), key=res.count)
        del res
        if not total:
            return (0, 0, 0)
        
        return total
