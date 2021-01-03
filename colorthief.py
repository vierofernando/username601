# this is a custom color thief made by me,
# since the PyPI version of ColorThief seems to a bit inaccurate.
# NOTE: this only generates a SINGLE color.

from io import BytesIO
from PIL import Image

class Smart_ColorThief:
    async def __get_image(self):
        res = await self.ctx.bot.http._HTTPClient__session.get(self.url)
        res = await res.read()
        self.image = Image.open(BytesIO(res)).resize((self.quality, self.quality))
        del res

    def __init__(self, ctx, url: str, quality: int = 50) -> None:
        """
        Initiation.
        The higher the quality, the more accurate, but the longer the time to process.
        """
        if isinstance(url, Image.Image):
            self.image = url
        elif isinstance(url, BytesIO):
            self.image = Image.open(BytesIO)
        else:
            self.ctx = ctx
            self.url = url
            self.quality = quality
    
    async def get_color(self, right=False) -> tuple:
        """Gets the color accent."""
        
        if not hasattr(self, "image"):
            await self.__get_image()

        load = self.image.load()
        if right:
            res = []
            for i in range(self.image.height):
                for j in range(self.image.width):
                    res.append(load[self.image.width-1, i])
        else:
            arr_L, arr_R, arr_T, arr_B = [], [], [], []
            for i in range(self.image.height):
                for j in range(self.image.width):
                    arr_L.append(load[0, i])
                    arr_R.append(load[self.image.width-1, i])
                    arr_T.append(load[j, 0])
                    arr_B.append(load[j, self.image.height-1])
            res = arr_L + arr_R + arr_T + arr_B
            del arr_L, arr_R, arr_T, arr_B
        total = max(set(res), key=res.count)
        del res, load
        if not total:
            return (0, 0, 0)
        
        return total
