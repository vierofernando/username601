# IMPORT EVERY SINGLE MODULE FROM PYTHON FIRST
from discord import Embed, Color, File, __version__, Forbidden, AllowedMentions, gateway
from platform import python_build, python_compiler, uname
from aiohttp import ClientSession, ClientTimeout
from .xmltodict import parse as xmltodict
from discord.ext.commands import Context
from configparser import ConfigParser
from os import getenv, name, listdir
from urllib.parse import quote_plus
from googletrans import LANGUAGES
from discord.ext import commands
from subprocess import run, PIPE
from traceback import format_exc
from datetime import datetime
from base64 import b64encode
from random import choice
from json import loads
from io import BytesIO
from time import time
from enum import Enum
from PIL import Image
import re
import gc

class LengthFormats(Enum):
    KILOMETERS  = (("km", "kilometer", "kilometre", "kilometers", "kilometres"), (
        None, "*1000", "*100000", "*1000000", "/1.609", "*1094", "*3281", "*39370"
    ))
    METERS      = (("m", "meter", "metre", "meters", "metres"), (
        "/1000", None, "*100", "*1000", "/1609", "*1.094", "*3.281", "*39.37"
    ))
    CENTIMETERS = (("cm", "centimeter", "centimetre", "centimeters", "centimetres"), (
        "/100000", "/100", None, "*10", "/160934", "/91.44", "/30.48", "/2.54"
    ))
    MILLIMETERS = (("mm", "millimeter", "millimetre", "millimeters", "millimetres"), (
        "/1000000", "/1000", "/10", None, "/1609000", "/914", "/305", "/25.4"
    ))
    MILES       = (("mile", "mi.", "miles", "mi"), (
        "*1.609", "*1609", "*160934", "*1609000", None, "*1760", "*5280", "*63360"
    ))
    YARDS       = (("yard", "yards", "yd"), (
        "/1094", "/1.094", "*91.44", "*914", "/1760", None, "*3", "*36"
    ))
    FOOT        = (("feet", "foot", "ft", "ft."), (
        "/3281", "/3.281", "*30.48", "*305", "/5280", "/3", None, "*12"
    ))
    INCHES      = (("inch", "inches"), (
        "/39370", "/39.37", "*2.54", "*25.4", "/63360", "/36", "/12", None
    ))
    
    _ALL = ("KILOMETERS", "METERS", "CENTIMETERS", "MILLIMETERS", "MILES", "YARDS", "FOOT", "INCHES")

class error_message(Exception):
    def __init__(self, message: str, description: bool = False):
        self.use_description = description or (len(message) > 256)
        self.embed = Embed(title=None if self.use_description else message, description=message if self.use_description else None, color=Color.red())
        super().__init__(message)

class Util:
    def __init__(
        self,
        client,
        attribute_name: str = "util",
        config_file: str = "config.ini"
    ):
        """
        Bot Utilities. That's all.
        
        Upon initiation, this class will make a copy of itself to the discord.Client object.
        """
        self.bot = client
        self.prefix_length = len(client.command_prefix)
        self._alphabet = list('abcdefghijklmnopqrstuvwxyz')
        self._start = time()
        self.no_mentions = AllowedMentions(everyone=False, users=False, roles=False)
        self.xmltodict = xmltodict
        self.alex_client = ClientSession(headers={'Authorization': getenv("ALEXFLIPNOTE_TOKEN")}, timeout=ClientTimeout(total=10.0))
        self.github_client = ClientSession(headers={'Authorization': 'token ' + getenv('GITHUB_TOKEN')}, timeout=ClientTimeout(total=10.0))
        
        self._time = {
            31536000: "year",
            2592000: "month",
            86400: "day",
            3600: "hour",
            60: "minute"
        }
        
        def _embed_add_useless_stuff(self, ctx, disable_color: bool = False):
            self._footer = {
                "text": "Command executed by "+str(ctx.author),
                "icon_url": str(ctx.author.avatar_url)
            }
            self.timestamp = datetime.now()
            
            if not disable_color:
                self.colour = ctx.me.colour
            return self
        
        async def send_image(self, url, alexflipnote: bool = False, message_options: dict = {}):
            try:
                session = self.bot.util.alex_client if alexflipnote else self.bot.http._HTTPClient__session
                
                async with session.get(url) as data:
                    _bytes = await data.read()
                    assert data.status < 400, "API returns a bad status code"
                    assert data.headers['Content-Type'].startswith("image/"), "Content does not have an image."
                    extension = "." + data.headers['Content-Type'][6:].lower()
                    buffer = self.bot.util._crop_out_memegen(self, _bytes) if url.startswith("https://api.memegen.link/") else BytesIO(_bytes)
                    await self.send(file=File(buffer, f"file{extension}"), **message_options)
                    del extension, _bytes, data, buffer
                    gc.collect()
            except Exception as e:
                raise self.error_message("Image not found.\n`"+str(e)+"`")
        
        async def success_embed(self, message=None, description=None, delete_after=None):
            return await self.send(embed=Embed(title=message, description=description, color=Color.green()), delete_after=delete_after)
        
        setattr(Context, "error_message", error_message)
        setattr(Context, "send_image", send_image)
        setattr(Context, "success_embed", success_embed)
        setattr(Embed, "add_useless_stuff", _embed_add_useless_stuff)
        self._on_command_error = None
        self._config = ConfigParser()
        self._config.read(config_file)
        
        for key in dict(self._config["bot"]).keys():
            setattr(self, key, int(self._config["bot"][key]) if self._config["bot"][key].isnumeric() else self._config["bot"][key])
        
        self._8ball_template = [
            "As I see it, {}",
            "My reply is {}",
            "My sources say {}",
            "{}",
            "Of course {}",
            "Well, {}. Of course",
            "{}, definitely",
            "Signs point to {}",
            "{}. Without a doubt",
            "Hell {}",
            "Well... {}",
            "Why did you ask me for this. The answer is always {}",
            "The answer is always {}",
            "Shut up. The answer is {}",
            "Stop asking me that question. The answer is definitely {}",
            "Heck {}",
            "That question's answer is always {}",
            "{}. {}!!!",
            "Someone told me the answer is {}",
            "Sorry, but the answer is {}"
        ]
        
        del self._config, _embed_add_useless_stuff, send_image, success_embed
        self.status_codes = loads(open(self.json_dir + "/status.json", "r", encoding="utf-8").read())

        setattr(client, attribute_name, self)

    def mobile_indicator(self) -> None:
        """ Turns your bot to a bot with mobile status. Source from this gist: https://gist.github.com/norinorin/0ef021163d042b3be76b892726d76e52 """
        
        s = __import__("inspect").getsource(gateway.DiscordWebSocket.identify).split('\n')
        indent = len(s[0]) - len(s[0].lstrip())
        source_ = '\n'.join(i[indent:] for i in s)

        source_ = __import__("re").sub(r'([\'"]\$browser[\'"]:\s?[\'"]).+([\'"])', r'\1Discord Android\2', source_)  # hh this regex
        m = __import__("ast").parse(source_)
        
        loc = {}
        exec(compile(m, '<string>', 'exec'), gateway.__dict__, loc)
        
        gateway.DiscordWebSocket.identify = loc['identify']
        del m, loc, source_, s, indent
        __import__("gc").collect()

    def timestamp(self, input, time_data: str = None, include_time_past: bool = True) -> str:
        """ Formats a timestamp. """
        if isinstance(input, str):
            input = datetime.strptime(input.split(".")[0].strip("Z"), "%Y-%m-%dT%H:%M:%S" if input.count("T") else time_data)
        
        _past = f"({self.strfsecond(time() - input.timestamp())} ago)" if include_time_past else ""
        return f'{input.strftime("%A, %d %B %Y" if input.minute == input.hour else "%A, %d %B %Y at %H:%M:%S")} {_past}'

    def convert_length(self, string):
        """ Does a math like `10 meters to kilometers` """
        try:
            string = string.lower().replace(" ", "")
            formats = re.sub(r"\d+", "", string)
            number = int(string.replace(formats, "").strip(",."))
            first_format, second_format = formats.split("to")
            assert first_format != second_format
            assert (-999999 < number < 999999999)
            
            for format in LengthFormats._ALL.value:
                if first_format in getattr(LengthFormats, format).value[0]:
                    first_format = getattr(LengthFormats, format).value[1]
                elif second_format in getattr(LengthFormats, format).value[0]:
                    second_format = format
            
            return f'{eval(f"{number}{first_format[LengthFormats._ALL.value.index(second_format)]}")} {second_format.lower()}'
        except:
            raise error_message("Unsupported or invalid calculation.")

    def toggle_debug_mode(self) -> bool:
        """ Toggles debug mode. Returns a bool whether debug mode is currently ON or not. """
    
        if self._on_command_error:
            setattr(self.bot, "on_command_error", self._on_command_error)
            self._on_command_error = None
            return True
        self._on_command_error = self.bot.on_command_error
        delattr(self.bot, "on_command_error")
        return False
    
    def has_nitro(self, guild, member) -> bool:
        
        if member.bot:
            return False
        elif member.is_avatar_animated():
            return True
        elif member in guild.premium_subscribers:
            return True
        elif hasattr(member.activity, "emoji") and hasattr(member.activity.emoji, "url") and member.activity.emoji.url:
            return True
        return False
    
    def join_position(self, guild, member) -> int:
        sorted_array = sorted([i.joined_at.timestamp() for i in guild.members])
        res = sorted_array.index(member.joined_at.timestamp())
        del sorted_array, guild, member
        return res + 1
   
    def eight_ball(self, ctx) -> str:
        """ Gets the eight ball answer. """
        code = hash(ctx.message.content.lower().replace(" ", "").replace("?", ""))
        if code < 0: code *= -1
        
        response = ((code + ctx.author.id) % 2 == 0)
        del code, ctx
        return choice(self._8ball_template).format("yes" if response else "no")

    def resolve_starboard_message(self, message):
        """ Gets the embed from a message as a form of starboard post. """
        embed = Embed(title=f"{message.author.display_name}#{message.author.discriminator} | #{str(message.channel)}", description=message.content, url=message.jump_url, color=discord.Color.from_rgb(255, 255, 0))
        if message.embeds:
            embed.description = message.embeds[0].description
        if message.attachments:
            if message.attachments[0].url.split(".")[::-1] in ["png", "jpeg", "jpg", "gif", "webp"]:
                embed.set_image(url=message.attachments[0].url)
        return embed
    
    async def handle_error(self, ctx, error):
        """ Handles errors like a boss. """
        error = getattr(error, "original", error)
        if isinstance(error, commands.CommandNotFound) or isinstance(error, commands.CheckFailure): return
        elif isinstance(error, commands.CommandOnCooldown): return await ctx.send("Calm down. Try again in {}.".format(self.strfsecond(round(error.retry_after))), delete_after=2)
        elif isinstance(error, error_message):
            await ctx.send(embed=error.embed)
            del error
            return
        elif isinstance(error, Forbidden): 
            try: return await ctx.send("I don't have the permission required to use that command!")
            except: return
        await self.bot.get_channel(self.feedback_channel).send(content='<@{}> there was an error!'.format(self.owner_id), embed=Embed(
            title='Error', color=Color.red(), description=f'Content:\n```{ctx.message.content}```\n\nError:\n```{str(error)}```'
        ).set_footer(text='Bug made by user: {} (ID of {})'.format(str(ctx.author), ctx.author.id)))
        return await ctx.send('Sorry, there was an error while executing this command.\nThis message has been reported to the developer of the bot.', delete_after=3)
    
    def load_cog(self, cog_folder: str = None, exclude: list = []):
        """ Loads the cogs from a directory. """

        try:
            _cog_folder = self.bot.cogs_dirname
        except:
            _cog_folder = cog_folder
        
        for i in listdir(_cog_folder):
            if not i.endswith(".py") or i in exclude: continue
            try:
                print("Loading cog", i)
                self.bot.load_extension('{}.{}'.format(_cog_folder, i[:-3]))
            except Exception as e:
                print("Error while loading cog:", str(e))

    def _crop_out_memegen(self, ctx, _bytes: bytes) -> BytesIO:
        """ idk if this is illegal but anyway """
        image = Image.open(BytesIO(_bytes))
        return ctx.bot.Image.save(image.crop((0, 12, image.width, image.height - 12)))
    
    def get_command_name(self, ctx) -> str:
        """ Gets the command name from a discord context object. This includes the alias used. """
        first_line = ctx.message.content.split()[0]
        return first_line[self.prefix_length:].lower()
    
    async def request(self, url, json=False, xml=False, alexflipnote=False, github=False, **kwargs):
        """ Does a GET request to a specific URL with a query parameters."""

        query_param = "?" + "&".join([i + "=" + quote_plus(str(kwargs[i])).replace("+", "%20") for i in kwargs.keys()]) if kwargs else ""
        
        try:
            session = self.alex_client if alexflipnote else (
                self.github_client if github else self.bot.http._HTTPClient__session
            )
            result = await session.get(url + query_param)
            assert result.status < 400, f"API returns a non-OK status code: {result.status}"
            if json:
                try:
                    return await result.json()
                except:
                    _bytes = await result.read()
                    return loads(_bytes)
            elif xml:
                text = await result.text()
                return xmltodict(text)
            return await result.text()
        except Exception as e:
            raise error_message("Request Failed. Exception: " + str(e))
    
    def encode_uri(self, text: str) -> str:
        """ Encodes a string to URI text. """
        return quote_plus(text).replace("+", "%20")
    
    def binary(self, text: str) -> str:
        """ Encodes a text to binary. """
        return ''.join(map(lambda x: f"{ord(x):08b}", text))

    def base64(self, text: str) -> str:
        """ Encodes a text to base64 string. """
        return b64encode(text.encode('ascii')).decode('ascii')
    
    def strfsecond(self, seconds: int):
        """ Converts a second to a string """
        seconds = int(seconds)
        
        if seconds < 60:
            return f"{seconds} second" + ("" if (seconds == 1) else "s")
        
        for key in self._time.keys():
            if seconds >= key:
                seconds //= key
                return f"{seconds} {self._time[key]}" + ("" if seconds == 1 else "s")
        
        seconds //= 31536000
        return f"{seconds} year" + ("" if seconds == 1 else "s")
    
    async def get_stats(self, evaluate: bool = True) -> dict:
        """
        Gets the bot stats.
        disabling `evaluate` will not get the RAM/memory data and OS uptime. this makes the process a bit faster.
        
        NOTE: evaluate will only enable on Linux-based operating systems.
        """
        
        if name != 'nt' and evaluate:
            free = await self.execute("free -m")
            free = free.split("\n")[1].split()[1:]
            _ram_eval = list(map(lambda x: int(x), free))
            _os_uptime = await self.execute("uptime -p")
            _os_uptime = _os_uptime[3:]
        else:
            _ram_eval = [None] * 6
            _os_uptime = None
        
        _uname = uname()
        _build = " ".join(python_build())
        
        return {
            "start_time": self._start,
            "bot_uptime": time() - self._start,
            "os_uptime": _os_uptime,
            "memory": {
                "total": _ram_eval[0],
                "used": _ram_eval[1],
                "free": _ram_eval[2],
                "shared": _ram_eval[3],
                "cache": _ram_eval[4],
                "available": _ram_eval[5]
            },
            "versions": {
                "os": _uname.system + " ver. " + _uname.version + ", machine " + _uname.machine,
                "python_build": _build,
                "python_compiler": python_compiler(),
                "discord_py": __version__
            }
        }
    
    async def execute(self, command: str) -> str:
        """ Evaluates a terminal command and returns an output. """
        
        return run(command.split(), stdout=PIPE).stdout.decode('utf-8')
    
    def atbash(self, text: str):
        """ Encodes a text to atbash cipher. """
        
        result = ""
        for char in text:
            if char.isalpha():
                result += self._alphabet[::-1][self._alphabet.index(char.lower())]
            else:
                result += char
        return result
    
    def caesar(self, text: str, offset: int):
        """Encodes a text as caesar cipher."""
        
        if offset > 26:
            while offset > 26:
                offset -= 26
        elif offset < 0:
            while offset < 0:
                offset += 26
        
        result = ""
        for char in text:
            if char.isalpha():
                index = self._alphabet.index(char.lower()) + offset
                
                if index > 25:
                    result += self._alphabet[index - 26]
                elif index < 0:
                    result += self._alphabet[index + 26]
                else:
                    result += self._alphabet[index]
            else:
                result += char
        return result
