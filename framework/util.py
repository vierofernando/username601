from discord import Embed, Color, File, __version__, Forbidden, AllowedMentions, gateway
from platform import python_build, python_compiler, uname
from aiohttp import ClientSession, ClientTimeout
from configparser import ConfigParser
from os import getenv, name, listdir
from urllib.parse import quote_plus
from googletrans import LANGUAGES
from discord.ext import commands
from subprocess import run, PIPE
from base64 import b64encode
from random import choice
from json import loads
from io import BytesIO
from time import time
from PIL import Image
import gc

class GetRequestFailedException(Exception): pass
class error_message(Exception): pass

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
        self.error_message = error_message

        self.alex_client = ClientSession(headers={'Authorization': getenv("ALEXFLIPNOTE_TOKEN")}, timeout=ClientTimeout(total=10.0))
        self.github_client = ClientSession(headers={'Authorization': 'token ' + getenv('GITHUB_TOKEN')}, timeout=ClientTimeout(total=10.0))
        
        self._time = {
            31536000: "year",
            2592000: "month",
            86400: "day",
            3600: "hour",
            60: "minute"
        }
        
        self._on_command_error = None
        self._config = ConfigParser()
        self._config.read(config_file)
        
        for key in dict(self._config["bot"]).keys():
            if self._config["bot"][key].isnumeric():
                setattr(self, key, int(self._config["bot"][key]))
            else:
                setattr(self, key, self._config["bot"][key])
        
        self._8ball_template = [
            "As I see it, ??",
            "My reply is ??",
            "My sources say ??",
            "??",
            "Of course ??",
            "Well, ??. Of course",
            "??, definitely",
            "Signs point to ??",
            "??. Without a doubt",
            "Hell ??",
            "Well... ??",
            "Why did you ask me for this. The answer is always ??",
            "The answer is always ??",
            "Shut up. The answer is ??",
            "Stop asking me that question. The answer is definitely ??",
            "Heck ??",
            "That question's answer is always ??",
            "??. ??!!!",
            "Someone told me the answer is ??",
            "Sorry, but the answer is ??"
        ]
        
        del self._config
        self.status_codes = loads(open(self.json_dir + "/status.json", "r", encoding="utf-8").read())

        setattr(client, attribute_name, self)

    def mobile_indicator(self) -> None:
        """ Turns your bot to a bot with mobile status. Source from this gist: https://gist.github.com/norinorin/0ef021163d042b3be76b892726d76e52 """
        
        def source(o):
            s = __import__("inspect").getsource(o).split('\n')
            indent = len(s[0]) - len(s[0].lstrip())
            return '\n'.join(i[indent:] for i in s)

        source_ = source(gateway.DiscordWebSocket.identify)
        source_ = __import__("re").sub(r'([\'"]\$browser[\'"]:\s?[\'"]).+([\'"])', r'\1Discord Android\2', source_)  # hh this regex
        m = __import__("ast").parse(source_)
        
        loc = {}
        exec(compile(m, '<string>', 'exec'), gateway.__dict__, loc)
        
        gateway.DiscordWebSocket.identify = loc['identify']
        del m, loc, source, source_
        __import__("gc").collect()

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
        return choice(self._8ball_template).replace("??", ("yes" if response else "no"))

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
        if isinstance(error, commands.CommandNotFound) or isinstance(error, commands.CheckFailure): return
        elif isinstance(error, commands.CommandOnCooldown): return await ctx.send("Calm down. Try again in {}.".format(self.strfsecond(round(error.retry_after))), delete_after=2)
        # put both of this on first because it's the most common exception
        
        if hasattr(error, "original"): # discord.py is weird
            error = error.original
        
        if isinstance(error, Forbidden): 
            try: return await ctx.send("I don't have the permission required to use that command!")
            except: return
        elif isinstance(error, self.error_message):
            return await ctx.send(embed=Embed(title=str(error) if len(str(error)) <= 256 else None, description=None if len(str(error)) <= 256 else str(error), color=Color.red()))
        elif isinstance(error, GetRequestFailedException):
            return await ctx.send(embed=Embed(description="A request failed to the API. Please try again later!\nError: " + str(error), color=Color.red()))
        else:
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

    async def send_image_attachment(self, ctx, url, alexflipnote: bool = False, message_options: dict = {}) -> None:
        """
        Sends an image attachment from a URL.
        Enabling alexflipnote will also add a Authorization header of "ALEXFLIPNOTE_TOKEN" to the GET request method.
        """
        try:
            session = self.alex_client if alexflipnote else self.bot.http._HTTPClient__session
            
            async with session.get(url) as data:
                _bytes = await data.read()
                assert data.status < 400, "API returns a bad status code"
                assert data.headers['Content-Type'].startswith("image/"), "Content does not have an image."
                extension = "." + data.headers['Content-Type'][6:].lower()
                buffer = self._crop_out_memegen(ctx, _bytes) if url.startswith("https://api.memegen.link/") else BytesIO(_bytes)
                await ctx.send(file=File(buffer, f"file{extension}"), **message_options)
                del extension, _bytes, data, buffer, ctx
                gc.collect()
        except Exception as e:
            raise self.error_message("Image not found.\n`"+str(e)+"`")
    
    def get_command_name(self, ctx) -> str:
        """ Gets the command name from a discord context object. This includes the alias used. """
        first_line = ctx.message.content.split()[0]
        return first_line[self.prefix_length:].lower()
    
    async def get_request(self, url, **kwargs):
        """ Does a GET request to a specific URL with a query parameters."""

        return_json, raise_errors, using_alexflipnote_token, force_json, github_token = False, False, False, False, False

        if list(kwargs.keys()):
            if kwargs.get("json"):
                return_json = True
                kwargs.pop("json")
            if kwargs.get("raise_errors"):
                raise_errors = True
                kwargs.pop("raise_errors")
            if kwargs.get("alexflipnote"):
                using_alexflipnote_token = True
                kwargs.pop("alexflipnote")
            if kwargs.get("force_json"):
                force_json = True
                kwargs.pop("force_json")
            if kwargs.get("github"):
                github_token = True
                kwargs.pop("github")

            query_param = "?" + "&".join([i + "=" + quote_plus(str(kwargs[i])).replace("+", "%20") for i in kwargs.keys()])
        else:
            query_param = ""
        
        try:
            session = self.alex_client if using_alexflipnote_token else (
                self.github_client if github_token else self.bot.http._HTTPClient__session
            )
            result = await session.get(url + query_param)
            assert result.status < 400
            if return_json:
                if force_json:
                    result = await result.read()
                    return loads(result)

                return await result.json()
            return await result.text()
        except Exception as e:
            if raise_errors:
                raise GetRequestFailedException("Request Failed. Exception: " + str(e))
            return
    
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
