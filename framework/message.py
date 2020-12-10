from discord import Embed, Color, File
from datetime import datetime
from io import BytesIO
from time import time
from os import getenv

class Paginator:
    def __init__(
        self,
        ctx,
        embeds: list,
        ratelimit: int = 1,
        max_time: int = 30,
        next_emoji: str = "▶️",
        previous_emoji: str = "◀️",
        start_emoji: str = "⏮",
        end_emoji: str = "⏭",
        close_emoji: str = "❌",
        show_page_count: bool = False,
        auto_set_color: bool = False
    ):
        """
        Simple Discord Paginator.
        Example:

        paginator = framework.Paginator(ctx, embeds=[
            discord.Embed(title="embed #1", description="This is the first embed"),
            discord.Embed(title="embed #2", description="This is the second embed"),
            discord.Embed(title="embed #3", description="This is the third embed")
        ])

        await paginator.execute()
        """
        self.embeds = embeds
        if auto_set_color:
            for embed in self.embeds:
                embed.color = ctx.guild.me.roles[::-1][0].color
        if show_page_count:
            _embed_index = 1
            for embed in self.embeds:
                embed.set_author(name=f"Page {_embed_index}/{len(embeds)}")
                self.embeds[_embed_index - 1] = embed
                _embed_index += 1
        self.max = len(embeds)
        self.last_reaction = time()
        self.ctx, self.max_time, self.ratelimit = ctx, max_time, ratelimit
        self.index = 0
        self.valid_emojis = [start_emoji, previous_emoji, close_emoji, next_emoji, end_emoji]
        self.check = (lambda reaction, user: (str(reaction.emoji) in self.valid_emojis) and (user == self.ctx.author))
    
    async def resolve_reaction(self, reaction):
        current_time = time()
        if (current_time - self.last_reaction) <= self.ratelimit:
            return
        self.last_reaction = current_time
        if (str(reaction.emoji) == self.valid_emojis[0]) and (self.index > 0): self.index = 0
        elif (str(reaction.emoji) == self.valid_emojis[1]) and (self.index > 0): self.index -= 1
        elif (str(reaction.emoji) == self.valid_emojis[2]):
            await self.delete()
            return -1
        elif (str(reaction.emoji) == self.valid_emojis[3]) and (self.index < (self.max - 1)): self.index += 1
        elif (str(reaction.emoji) == self.valid_emojis[4]) and (self.index < (self.max - 1)): self.index = (self.max - 1)
        else: return
        await self.message.edit(content='', embed=self.embeds[self.index])

    async def execute(self):
        self.message = await self.ctx.send(embed=self.embeds[0])
        for i in self.valid_emojis:
            await self.message.add_reaction(i)
        
        while True:
            try:
                reaction, user = await self.ctx.bot.wait_for("reaction_add", timeout=self.max_time, check=self.check)
                resolve = await self.resolve_reaction(reaction)
                assert resolve != -1
            except:
                break
    
    async def delete(self):
        if not hasattr(self, "message"):
            raise TypeError("Message has not been sent.")
        return await self.message.delete()

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

    async def get_embed(self) -> tuple:
        """ Gets the embed and the attachment in it, returns a tuple(discord.Embed, Union[discord.File, None]) """
        _embed = Embed(title=self.title, description=self.description, color=self.color, url=self.url)
        if self.fields is not None:
            for i in self.fields.keys():
                _embed.add_field(name=i, value=self.fields[i])
        _embed.timestamp = self.current_time
        _embed.set_footer(text=self.footer, icon_url=self.footer_icon)
        if self.image_url:
            _embed.set_image(url=str(self.image_url))
        if self.thumbnail_url:
            _embed.set_thumbnail(url=str(self.thumbnail_url))
        _file = None

        if self.attachment_url:
            if isinstance(self.attachment_url, str):
                _bytes = await self.ctx.bot.util.default_client.get(self.attachment_url)
                _bytes = await _bytes.read()
                self.attachment_url = BytesIO(_bytes)
            _file = File(self.attachment_url, "image.png")
            _embed.set_image(url="attachment://image.png")

        return _embed, _file

    async def send(self):
        """ Sends the embed to the current channel. """
        _embed, _attachment = await self.get_embed()
        if _attachment is None:
            return await self.ctx.send(embed=_embed)
        return await self.ctx.send(embed=_embed, file=_attachment)
    
    async def edit_to(self, message):
        """ Appends the embed to a discord.Message object """
        _embed, _attachment = await self.get_embed()
        if _attachment is None:
            return await message.edit(content='', embed=_embed)
        await message.edit(content='', embed=_embed, file=_attachment)

class WaitForMessage:
    def __init__(self, ctx, timeout=20.0, check=None):
        """ A wrapper class that waits for message. """
        self.ctx = ctx
        self._check = (lambda x: x.channel == self.ctx.channel and x.author == self.ctx.author) if check is None else check
        self._timeout = float(timeout)
    
    async def get_message(self):
        """ Runs the whole thing. """
        try:
            text = await self.ctx.bot.wait_for("message", check=self._check, timeout=self._timeout)
            return text
        except:
            return None

class ChooseEmbed(embed):
    def __init__(self, ctx, reference: list, key = None):
        """
        The choose embed, waits for the user to input the number.
        The key is a method that temporarily shows a reference. Example: (lambda x: x["name"])
        """
        
        reference = reference[0:20]
        self._pre_res = None if (len(reference) != 1) else reference[0]
        self.message = None
        
        if self._pre_res is None:
            self._size = len(reference)
            self._range = range(1, self._size + 1)
            self._ctx = ctx
            self.embed = embed(ctx, title=f"Found {self._size} matches.", desc=f"**Send a number between `{self._range[0]}` and `{self._range[::-1][0]}` corresponding to your choice.**\n")
            self._reference = []
    
            _i = 0
            for choice in reference:
                self._reference.append(choice)
                self.embed.description += f"\n`{_i + 1}.` {choice}" if key is None else f"\n`{_i + 1}.` {key(choice)}"
                _i += 1
    
    async def run(self):
        """ Runs the whole thing. Returns an index of the choice, or None. """
    
        if self.message is not None: return
        elif self._pre_res is not None:
            return self._pre_res
        
        self.message = await self.embed.send()
        _check = (lambda x: x.channel == self.message.channel and x.author == self._ctx.author)
        _res = await self._ctx.bot.utils.wait_for_message(self._ctx, message=None, func=_check, timeout=20.0)
        if (_res is None) or (not _res.content.isnumeric()):
            await self.message.edit(embed=Embed(title="Canceled.", color=Color.red()))
            return
        _user_choice = int(_res.content)
        if _user_choice not in self._range:
            await self.message.edit(embed=Embed(title="Invalid range. Please try again.", color=Color.red()))
            return
        else:
            await self.message.delete()
            return self._reference[_user_choice - 1]