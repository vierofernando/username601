from PIL import Image, ImageDraw, ImageFont
from discord import Spotify, File
from io import BytesIO
from requests import get
from time import strftime, gmtime
from datetime import datetime as t
from .colorthief import Smart_ColorThief

class CustomPanel(Smart_ColorThief):
    def __buffer_from_url(self, url, *args, **kwargs):
        return Image.open(BytesIO(get(url).content), *args, **kwargs)

    def __invert(self, color):
        if sum(color) >= 126: return (0, 0, 0)
        return (255, 255, 255)

    def __get_color_accent(self, url, right=False):
        return Smart_ColorThief(url).get_color(right=right)

    def __init__(self, title="Title text", subtitle="Subtitle text", description="Description text here", icon="https://cdn.discordapp.com/embed/avatars/0.png", font="NotoSansDisplay-Bold.otf", min_width=500, margin=20, spotify=None, auto_draw=False):
        """
        Creates a custom panel.
        Can be used for Spotify commands.
        Example:

        spotify = CustomPanel(spotify=ctx.author.activity)
        spotify.draw()
        await spotify.send_as_attachment(ctx, content=f"This is your spotify activity, {ctx.author.name}!")
        """
        
        self.FONT = font
        self.__get_font = (lambda s: ImageFont.truetype(self.FONT, s))

        if (spotify is not None) and (not isinstance(spotify, Spotify)):
            raise TypeError("Spotify argument is not an instance of Spotify")
        
        self.SPOTIFY = spotify
        self.TITLE_TEXT = title if not self.SPOTIFY else self.SPOTIFY.title
        self.TITLE_FONT = self.__get_font(30)
        self.SUBTITLE_TEXT = subtitle if not self.SPOTIFY else "By "+(', '.join(self.SPOTIFY.artists))
        self.SUBTITLE_FONT = self.__get_font(20)
        self.DESC_TEXT = description if not self.SPOTIFY else "On "+self.SPOTIFY.album
        self.DESC_FONT = self.__get_font(15)
        self.COVER_URL = icon if not self.SPOTIFY else self.SPOTIFY.album_cover_url
        self.COVER = self.__buffer_from_url(self.COVER_URL).resize((200, 200))
        self.BACKGROUND_COLOR = self.__get_color_accent(self.COVER_URL, right=True)
        self.FOREGROUND_COLOR = self.__invert(self.BACKGROUND_COLOR)

        if len(self.TITLE_TEXT) > 25: self.TITLE_TEXT = self.TITLE_TEXT[0:25] + "..."
        if len(self.SUBTITLE_TEXT) > 35: self.SUBTITLE_TEXT = self.SUBTITLE_TEXT[0:35] + "..."
        if len(self.DESC_TEXT) > 45: self.DESC_TEXT = self.DESC_TEXT[0:45] + "..."

        self.TITLE_SIZE = self.TITLE_FONT.getsize(self.TITLE_TEXT)
        self.SUBTITLE_SIZE = self.SUBTITLE_FONT.getsize(self.SUBTITLE_TEXT)
        self.DESC_SIZE = self.DESC_FONT.getsize(self.DESC_TEXT)
        self.WIDTH = max([self.TITLE_SIZE[0], self.SUBTITLE_SIZE[0], self.DESC_SIZE[0]]) + 270

        if ((min_width is not None) and (self.WIDTH < min_width)):
            self.WIDTH = min_width
        
        self.MARGIN_LEFT = 200 + margin
        self.MARGIN_RIGHT = self.WIDTH - margin
        self.MARGIN_TOP = margin

        if auto_draw:
            self.draw()
    
    def draw(self):
        self.MAIN = Image.new(mode="RGB", color=self.BACKGROUND_COLOR, size=(self.WIDTH, 200))
        self.DRAW = ImageDraw.Draw(self.MAIN)

        if self.SPOTIFY:
            SEEK = round(round((t.now() - self.SPOTIFY.created_at).total_seconds())/round(self.SPOTIFY.duration.total_seconds())*100)
            STR_CURRENT = strftime('%H:%M:%S', gmtime(round((t.now() - self.SPOTIFY.created_at).total_seconds())))
            STR_END = strftime('%H:%M:%S', gmtime(round(self.SPOTIFY.duration.total_seconds())))
            DURATION_LEFT_SIZE = self.DRAW.textsize(STR_END, font=self.SUBTITLE_FONT)[0]

            self.DRAW.rectangle([(self.MARGIN_LEFT, self.MARGIN_TOP + 100), (self.MARGIN_RIGHT, self.MARGIN_TOP + 120)], fill=tuple(map(lambda x: x - 25, self.BACKGROUND_COLOR)))
            self.DRAW.rectangle([(self.MARGIN_LEFT, self.MARGIN_TOP + 100), ((SEEK / 100 * (self.MARGIN_RIGHT - self.MARGIN_LEFT)) + self.MARGIN_LEFT, self.MARGIN_TOP + 120)], fill=self.FOREGROUND_COLOR)
            self.DRAW.text((self.MARGIN_LEFT, self.MARGIN_TOP + 130), STR_CURRENT, font=self.SUBTITLE_FONT, fill=self.FOREGROUND_COLOR)
            self.DRAW.text((self.MARGIN_RIGHT - DURATION_LEFT_SIZE, self.MARGIN_TOP + 130), STR_END, font=self.SUBTITLE_FONT, fill=self.FOREGROUND_COLOR)

        self.DRAW.text((self.MARGIN_LEFT, self.MARGIN_TOP), self.TITLE_TEXT, font=self.TITLE_FONT, fill=self.FOREGROUND_COLOR)
        self.DRAW.text((self.MARGIN_LEFT, self.MARGIN_TOP + 38), self.SUBTITLE_TEXT, font=self.SUBTITLE_FONT, fill=self.FOREGROUND_COLOR)
        self.DRAW.text((self.MARGIN_LEFT, self.MARGIN_TOP + 65), self.DESC_TEXT, font=self.DESC_FONT, fill=self.FOREGROUND_COLOR)

        self.MAIN.paste(self.COVER, (0, 0))
    
    def get_buffer(self):
        if not hasattr(self, "MAIN"):
            raise OSError("Canvas has not been drawn yet.")
        
        BytesIO_array = BytesIO()
        self.MAIN.save(BytesIO_array, format="PNG")
        BytesIO_array.seek(0)
        return BytesIO_array
    
    async def send_as_attachment(self, ctx, content=""):
        return await ctx.send(content=content, file=File(self.get_buffer(), "image.png"))