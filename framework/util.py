from discord import Embed, Color, File, __version__
from io import BytesIO
from requests import get
from aiohttp import ClientSession
from os import getenv, name, listdir
from subprocess import run, PIPE
from base64 import b64encode
from configparser import ConfigParser
from urllib.parse import quote_plus
from time import time
from platform import python_build, python_compiler, uname

class GetRequestFailedException(Exception): pass

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

        self.useless_client = ClientSession(headers={"superdupersecretkey": getenv("USELESSAPI")})
        self.alex_client = ClientSession(headers={'Authorization': getenv("ALEXFLIPNOTE_TOKEN")})
        self.default_client = ClientSession()
        
        self._time = {
            31536000: "year",
            2592000: "month",
            86400: "day",
            3600: "hour",
            60: "minute"
        }
        
        self._config = ConfigParser()
        self._config.read(config_file)
        
        for key in dict(self._config["bot"]).keys():
            if self._config["bot"][key].isnumeric():
                setattr(self, key, int(self._config["bot"][key]))
            else:
                setattr(self, key, self._config["bot"][key])
        
        delattr(self, "_config")
        setattr(client, attribute_name, self)
    
    def load_cog(self, cog_folder: str = None, exclude: list = []):
        """ Loads the cogs from a directory. """

        try:
            _cog_folder = self.bot.cogs_dirname
        except:
            _cog_folder = cog_folder
        
        for i in listdir(cog_folder):
            if not i.endswith(".py") or i in exclude: continue
            try:
                print("Loading cog", i)
                self.bot.load_extension('{}.{}'.format(_cog_folder, i[:-3]))
            except Exception as e:
                print("Error while loading cog:", str(e))

    def post_ready(self):
        """ A method to be executed after the client is ready on on_ready event."""
        try:
            setattr(self, "loading_emoji", str(self.bot.get_emoji(self.emoji_loading)))
            setattr(self, "error_emoji", str(self.bot.get_emoji(self.emoji_error)))
            setattr(self, "success_emoji", str(self.bot.get_emoji(self.emoji_success)))
            delattr(self, "emoji_loading")
            delattr(self, "emoji_error")
            delattr(self, "emoji_success")
        except:
            return

    async def send_image_attachment(self, ctx, url, alexflipnote=False, uselessapi=False) -> None:
        """
        Sends an image attachment from a URL.
        Enabling alexflipnote will also add a Authorization header of "ALEXFLIPNOTE_TOKEN" to the GET request method.
        """
        try:
            if alexflipnote: session = self.alex_client
            elif uselessapi: session = self.useless_client
            else: session = self.default_client
            
            async with session.get(url) as data:
                _bytes = await data.read()
                assert data.status < 400, "API returns a bad status code"
                assert data.headers['Content-Type'].startswith("image/"), "Content does not have an image."
                extension = "." + data.headers['Content-Type'][6:]
                return await ctx.send(file=File(BytesIO(_bytes), "file"+extension.lower()))
        except Exception as e:
            return await self.send_error_message(ctx, "Image not found.\n`"+str(e)+"`")
    
    async def send_error_message(self, ctx, message):
        """ Sends an error message embed. """
        await ctx.send(embed=Embed(title="Error", description=message, color=Color.red()))
    
    def get_command_name(self, ctx) -> str:
        """ Gets the command name from a discord context object """
        first_line = ctx.message.content.split()[0]
        return first_line[self.prefix_length:].lower()
    
    def get_request(self, url, **kwargs):
        """ Does a GET request to a specific URL with a query parameters."""

        return_json, raise_errors, using_alexflipnote_token = False, False, False

        if len(kwargs.keys()) > 0:
            if kwargs.get("json") is not None:
                return_json = True
                kwargs.pop("json")
            if kwargs.get("raise_errors") is not None:
                raise_errors = True
                kwargs.pop("raise_errors")
            if kwargs.get("alexflipnote") is not None:
                using_alexflipnote_token = True
                kwargs.pop("alexflipnote")
        
            query_param = "?" + "&".join([i + "=" + quote_plus(str(kwargs[i])).replace("+", "%20") for i in kwargs.keys()])
        else:
            query_param = ""
        
        try:
            data = get(url + query_param, timeout=10.0, headers={'Authorization': getenv("ALEXFLIPNOTE_TOKEN")}) if using_alexflipnote_token else get(url + query_param, timeout=10.0)
            assert data.status_code < 400
            return (data.json() if return_json else data.text)
        except:
            if raise_errors:
                raise GetRequestFailedException("Request Failed")
            return None
    
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
        result = None
        
        if seconds < 60:
            return f"{seconds} second" + ("" if (seconds == 1) else "s")
        
        for key in self._time.keys():
            if seconds >= key:
                seconds = round(seconds / key)
                return f"{seconds} {self._time[key]}" + ("" if seconds == 1 else "s")
        
        seconds = round(seconds / 31536000)
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
