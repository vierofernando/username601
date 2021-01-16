from discord import Embed, Colour, File
from datetime import datetime, timezone
from io import BytesIO
from time import time
from os import getenv
import gc

class Paginator:
    def __init__(
        self,
        ctx,
        embeds: list,
        ratelimit: int = 1.5,
        max_time: int = 20,
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
                embed.color = ctx.me.color
        
        if show_page_count:
            _embed_index = 1
            for embed in self.embeds:
                embed.set_author(name=f"Page {_embed_index}/{len(embeds)}")
                self.embeds[_embed_index - 1] = embed
                _embed_index += 1
        
        self.ctx, self.max_time, self.ratelimit, self.index, self.last_reaction, self.max = ctx, max_time, ratelimit, 0, time(), len(embeds)
        self.valid_emojis = [start_emoji, previous_emoji, close_emoji, next_emoji, end_emoji]
        self.check = (lambda reaction, user: (str(reaction.emoji) in self.valid_emojis) and (user == self.ctx.author))
        self.http = ctx._state.http
    
    def __del__(self):
        """ Let the object kill itself first before getting deleted. """
        del self.ctx, self.max_time, self.ratelimit, self.index, self.last_reaction, self.max
        del self.valid_emojis, self.check
        del self.embeds, self.http
    
    async def _edit(self):
        await self.http.edit_message(self.message.channel.id, self.message.id, embed=self.embeds[self.index].to_dict())
    
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
        await self._edit()

    async def execute(self):
        self.message = await self.ctx.send(embed=self.embeds[0])
        for i in self.valid_emojis:
            await self.message.add_reaction(i)
        
        while True:
            try:
                reaction, user = await self.ctx.bot.wait_for("reaction_add", timeout=self.max_time, check=self.check)
                resolve = await self.resolve_reaction(reaction)
                assert resolve != -1
                del reaction, user, resolve
            except:
                break
    
    async def delete(self):
        if not hasattr(self, "message"):
            raise TypeError("Message has not been sent.")
        return await self.http.delete_message(self.message.channel.id, self.message.id)

    @staticmethod
    def from_long_array(ctx, array: list, data: dict = {}, char: str = "\n", max_pages: int = 20, max_char_length: int = 2000, *args, **kwargs):
        if len(char.join(array)) <= max_char_length:
            return
        
        size = len(char)
        total = []
        current = char
        for i in array:
            if len(total) >= max_pages:
                break
        
            _current = current + char + i
            if len(_current[size:]) >= max_char_length:
                total.append(current[size:])
                current = char + i
                continue
            current = _current
            del _current
        
        if current:
            total.append(current[size:])
        
        embeds = []
        
        for section in total:
            temp = data.copy()
            temp["description"] = section
            embeds.append(Embed.from_dict(temp).add_useless_stuff(ctx))
            del section, temp
        
        del total, current, size
        show_page_count = kwargs.pop("show_page_count", True)
        return Paginator(ctx, embeds, show_page_count=show_page_count, *args, **kwargs)

    @staticmethod
    def from_long_string(ctx, string, max_char_length: int = 2000, max_pages: int = 20, data: dict = {}, *args, **kwargs):
        if len(string) <= max_char_length:
            return
        chunks = [string[i:i + max_char_length] for i in range(0, len(string), max_char_length)]
        embeds = []
        
        for i, chunk in enumerate(chunks):
            if len(embeds) >= max_pages:
                break
            temp = data.copy()
            temp["description"] = chunk + ("" if (i == (len(chunks) - 1)) else "...")
            embeds.append(Embed.from_dict(temp).add_useless_stuff(ctx))
            del chunk, temp
        del chunks, string
        show_page_count = kwargs.pop("show_page_count", True)
        return Paginator(ctx, embeds, show_page_count=show_page_count, *args, **kwargs)

class embed:
    COL = {
        Colour: lambda x: x.value,
        tuple: lambda x: (x[0] << 16 | x[1] << 8 | x[2]),
        str: lambda x: int(x.lstrip("#"), 16)
    }
    TIME = {
        datetime: lambda x: x.astimezone(tz=timezone.utc).isoformat(),
        float: lambda x: datetime.fromtimestamp(x).astimezone(tz=timezone.utc).isoformat(),
        int: lambda x: datetime.fromtimestamp(x).astimezone(tz=timezone.utc).isoformat()
    }
    """
    Embed 'wrapper' i guess (lower level than discord.py's so it's faster maybe?)
    Example:

    embed = framework.embed(ctx, title="Hello, world!", description="this is the description", color=(255, 0, 0), fields={
        "field 1": "this is a field",
        "field 2": "this is also another field!"
    })
    await embed.send()
    
    """
    
    def __dict__(self):
        return self.dict
    
    def __getitem__(self, item):
        return self.dict[item]

    def __init__(self, ctx, **param) -> None:
        self.channel = ctx.channel
        self.state = ctx._state
        
        self.dict = { "type": "rich" }
        self.param = param
        
        self.dict["color"] = embed.COL[param["color"].__class__](param["color"]) if param.get("color") else ctx.me.color.value
        self._add_to_dict("title",       "title",       str)
        self._add_to_dict("description", "description", str)
        self._add_to_dict("url",         "url",         str)
        self._add_to_dict("time",        "timestamp",   lambda x: embed.TIME[x.__class__](x))
        self._add_to_dict("image",       "image",       lambda x: { "url": str(x) })
        self._add_to_dict("thumbnail",   "thumbnail",   lambda x: { "url": str(x) })
        self._add_to_dict("footer",      "footer",      lambda x: { "text": str(x) })
        self._add_to_dict("image",       "image",       lambda x: { "url": str(x) })
        
        self.dict["footer"] = {
            "text": self.param.get("footer", f"Command executed by {ctx.author}"),
            "icon_url": self.param.get("footer_icon", str(ctx.author.avatar_url))
        }
        
        _author = {}
        if param.get("author_name"):
            _author["name"] = param["author_name"]
        
        if param.get("author_url"):
            _author["url"] = param["author_url"]
        
        if param.get("author_icon"):
            _author["icon_url"] = param["author_icon"]
        
        if _author:
            self.dict["author"] = _author
        del _author
        
        if self.param.get("fields"):
            self.dict["fields"] = []
            for key in self.param["fields"].keys():
                self.dict["fields"].append({ "name": key, "value": self.param["fields"][key], "inline": False })
        
        del self.param, param
        
    def _add_to_dict(self, name, key_name, func):
        if not self.param.get(name): return
        self.dict[key_name] = func(self.param[name])

    def color(self, color):
        self.dict["color"] = embed.COL[color.__class__](color)

    def add_field(self, name, value, inline: bool = False):
        self.dict["fields"].append({
            "name": name,
            "value": value,
            "inline": inline
        })
        return self # just like discord.py hehe

    async def send(self, return_message_object: bool = False):
        """ Sends the embed to the current channel. """
        try:
            return await self.state.http.send_message(self.channel.id, content="", embed=self.dict)
        except Exception as e:
            raise self.ctx.error_message(f"Something wrong happened while sending the message embed.\n`{str(e)}`")
    
    async def edit_to(self, message):
        """ Appends the embed to a discord.Message object """
        await self.state.http.edit_message(message.channel.id, message.id, content="", embed=self.dict)

class WaitForMessage:
    def __init__(self, ctx, timeout=20.0, check=None):
        """ A wrapper class that waits for message. """
        self.bot = ctx.bot
        self._check = check if check else (lambda x: x.channel == ctx.channel and x.author == ctx.author)
        self._timeout = float(timeout)
        del ctx
    
    async def get_message(self):
        """ Runs the whole thing. """
        try:
            text = await self.bot.wait_for("message", check=self._check, timeout=self._timeout)
            return text
        except:
            return
    
    def __del__(self):
        del self.bot, self._check, self._timeout
        gc.collect()

class ChooseEmbed:
    def __init__(self, ctx, reference: list, key = None):
        """
        The choose embed, waits for the user to input the number.
        The key is a method that temporarily shows a reference. Example: (lambda x: x["name"])
        """
        
        reference = reference[:20]
        self._pre_res = None if (len(reference) != 1) else reference[0]
        
        if not self._pre_res:
            self._size = len(reference)
            self._range = range(1, self._size + 1)
            self._ctx = ctx
            self.embed = embed(ctx, title=f"Found {self._size} matches.", description=f"**Send a number between `{self._range[0]}` and `{self._range[::-1][0]}` corresponding to your choice.**\n")
            self._reference = []
    
            _i = 0
            for choice in reference:
                self._reference.append(choice)
                self.embed.dict["description"] += f"\n`{_i + 1}.` {key(choice)}" if key else f"\n`{_i + 1}.` {choice}"
                _i += 1
    
    async def run(self):
        """ Runs the whole thing. Returns an index of the choice, or None. """
    
        if self._pre_res is not None:
            return self._pre_res
        
        message = await self.embed.send()
        message_id, channel_id, http = message["id"], message["channel_id"], self.embed.state.http
        del message
        
        _wait = WaitForMessage(self._ctx, check=lambda x: x.channel == self._ctx.channel and x.author == self._ctx.author, timeout=20.0)
        _res = await _wait.get_message()
        if (not _res) or (not _res.content.isnumeric()):
            await http.edit_message(channel_id, message_id, embed={
                "title": "Canceled.",
                "color": 15158332
            })
            return
        _user_choice = int(_res.content)
        if _user_choice not in self._range:
            await http.edit_message(channel_id, message_id, embed={
                "title": "Invalid range. Please try again.",
                "color": 15158332
            })
            return
        await http.delete_message(channel_id, message_id)
        return self._reference[_user_choice - 1]
    
    def __del__(self):
        del self.embed
        del self._pre_res
        
        try:
            del self._size
            del self._range
            del self._ctx
            del self._reference
        except:
            return