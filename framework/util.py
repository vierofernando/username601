from discord import Embed, Color
from io import BytesIO
from requests import get
from os import getenv
from subprocess import run, PIPE
from base64 import b64encode
from configparser import ConfigParser
from urllib.parse import quote_plus
from time import time

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
    
    async def send_image_attachment(self, ctx, url, alexflipnote=False) -> None:
        """
        Sends an image attachment from a URL.
        Enabling alexflipnote will also add a Authorization header of "ALEXFLIPNOTE_TOKEN" to the GET request method.
        """
        try:
            data = get(url, timeout=5.0) if (not alexflipnote) else get(url, timeout=10.0, headers={'Authorization': getenv("ALEXFLIPNOTE_TOKEN")})        
            assert data.status_code < 400, "API returns a bad status code"
            assert data.headers['Content-Type'].startswith("image/"), "Content does not have an image."
            extension = "." + data.headers['Content-Type'][6:]
            return await ctx.send(file=File(BytesIO(data.content), "file"+extension.lower()))
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

        return_json = False

        if len(kwargs.keys()) > 0:
            if kwargs.get("json") is not None:
                return_json = True
                kwargs.pop("json")
        
            query_param = "?" + "&".join([i + "=" + quote_plus(str(kwargs[i])).replace("+", "%20") for i in kwargs.keys()])
        else:
            query_param = ""
        
        try:
            data = get(url + query_param, timeout=10.0)
            assert data.status_code < 400
            return (data.json() if return_json else data.text)
        except:
            return None
    
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
    
    def get_stats(self, gather_os_data: bool = True) -> dict:
        """
        Gets the bot stats.
        disabling `gather_os_data` will not get the RAM/memory data and OS uptime. this makes the process a bit faster.
        
        NOTE: Only works in hosts with Linux
        """
        
        if gather_os_data:
            _ram_eval = list(map(lambda x: int(x), self.execute("free -m").split("\n")[1].split()[1:]))
            _os_uptime = self.execute("uptime -p")[3:]
        else:
            _ram_eval = [None] * 6
            _os_uptime = None
        
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
            }
        }
    
    def execute(self, command: str) -> str:
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