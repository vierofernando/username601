from discord import Embed, Color, File
from datetime import datetime
from io import BytesIO
from requests import get

class embed:
    """
    Embed 'wrapper' i guess
    Example:

    embed = framework.embed(ctx, title="Hello, world!", desc="this is the description", color=(255, 0, 0), fields={
        "field 1": "this is a field",
        "field 2": "this is also another field!"
    })
    await embed.send()
    
    """

    def _convert_hex_to_rgb(self) -> None:
        self.color = Color(*tuple(int(self.color[i:i+2], 16) for i in (0, 2, 4)))

    def __init__(self, ctx, author_name=None, attachment=None, author_url=None, url=None, desc=None, footer_icon=None, thumbnail=None, image=None, title=None, color=None, fields={}, footer=None) -> None:
        self.ctx = ctx
        self.color = self.ctx.guild.me.roles[::-1][0].color if color is None else color
        self.title = "" if title is None else str(title)
        self.description = "" if desc is None else str(desc)
        self.current_time = datetime.now()
        self.fields = None if (fields == {}) else fields
        self.footer = "Command executed by "+str(self.ctx.author) if footer is None else str(footer)
        self.url = url
        self.image_url = image
        self.thumbnail_url = thumbnail
        self.footer_icon = str(self.ctx.author.avatar_url) if footer_icon is None else str(footer_icon)
        self.attachment_url = attachment

        if isinstance(self.color, tuple):
            self.color = Color.from_rgb(*self.color)
        elif ((isinstance(self.color, str)) and (self.color.startswith("#"))):
            self._convert_hex_to_rgb()
        return None

    def get_embed(self) -> Embed:
        _embed = Embed(title=self.title, description=self.description, color=self.color, url=self.url)
        if self.fields is not None:
            for i in self.fields.keys():
                _embed.add_field(name=i, value=self.fields[i])
        _embed.timestamp = self.current_time
        _embed.set_footer(text=self.footer, icon_url=self.footer_icon)
        if self.image_url is not None: _embed.set_image(url=str(self.image_url))
        if self.thumbnail_url is not None: _embed.set_thumbnail(url=str(self.thumbnail_url))
        _file = None

        if self.attachment_url is not None:
            if isinstance(self.attachment_url, str):
                self.attachment_url = BytesIO(get(self.attachment_url).content)
            _file = File(self.attachment_url, "image.png")
            _embed.set_image(url="attachment://image.png")

        return _embed, _file

    async def send(self):
        _embed, attachment = self.get_embed()

        if attachment is None:
            return await self.ctx.send(embed=_embed)
        return await self.ctx.send(embed=_embed, file=attachment)