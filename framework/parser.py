from twemoji_parser import emoji_to_url
from .util import BasicCommandException
from PIL import ImageColor
import re

class Parser:
    SPLIT_CHARACTERS = [';', ', ', ',', '|',' | ', ' ']
    HTML_DICT = {
        "<p>": "",
        "</p>": "",
        "<b>": "**",
        "</b>": "**",
        "<i>": "*",
        "</i>": "*",
        "<br />": "\n",
        "<br>": "\n"
    }
    EMOJI_REGEX = re.compile("<:(.*?)>")
    CHANNEL_REGEX = re.compile("<#(.*?)>")
    ROLES_REGEX = re.compile("<@&(.*?)>")

    def __bool__(self) -> bool:
        return bool(self.flags)

    def __getitem__(self, value: str) -> str:
        if not self.flags:
            return
        return self.flags.get(value)

    def __dict__(self) -> dict:
        if not self.flags:
            return
        return self.flags

    def __init__(
        self,
        args: tuple,
        *trash,
        **other_trash
    ) -> None:
        """ The main options parser object. Only a tuple is required. """
        self.raw = args
        self.flags = {}
        self.other = list(self.raw)
    
    def parse(self) -> dict:
        """ Parses the arguments and gets the options. """
        
        for i, arg in enumerate(self.raw):
            if (not arg.startswith("--")) and (not arg.startswith("—")):
                continue
            
            name, with_quotes, content = arg[2:] if arg.startswith("--") else arg[1:], None, ""
            if (not name) or (name in self.flags.keys()):
                continue
            self.other.remove(arg)
            
            for value in self.raw[i + 1:]:
                if value.startswith("--") or value.startswith("—"):
                    break
                
                self.other.remove(value)
                
                if (value.startswith("'") or value.startswith('"')) and (not with_quotes):
                    with_quotes = value[0]
                    content += value[1:]
                    continue
                elif (value.endswith('"') or value.endswith("'")) and with_quotes:
                    del with_quotes
                    content += " " + value[:-1]
                    break
                elif with_quotes:
                    content += " " + value
                    continue
                content = value
                break
            self.flags[name] = content if content else None
        return self.flags
    
    def has(self, query: str) -> bool:
        """ Checks ONLY if a flag exists, even returns True despite the value is None. """
        return (query in self.flags.keys())
    
    def has_multiple(self, *args) -> bool:
        """ Checks multiple flags, unlike the has() method which only accepts one argument. Returns True if at least ONE value is True. """
        
        for key in self.flags.keys():
            if key in args:
                return True
        return False
    
    def shift(self, argument_name: str, _check: bool = True) -> None:
        """ Shifts a flag value and dumps it to self.other. """
        if not self.has(argument_name):
            return
        
        value = self.flags[argument_name]
        self.flags.pop(argument_name)
        
        if value:
            self.other.extend(value.split(" "))
    
    def shift_multiple(self, *args) -> None:
        """ Shifts multiple flags. disabling shift_all will quit if at least one flag is shifted. """
        
        for i, arg in enumerate(args):
            self.shift(arg)
    
    def __del__(self):
        del (self.flags, self.other, self.raw)
    
    @staticmethod
    def has_flag(args: tuple, flag_name: str) -> bool:
        """ Runs a quick check to see if flag is in args tuple. """
        
        lowered_text = [i.lower() for i in args]
        return ((lowered_text.count("--" + flag_name.lower()) > 0) or (lowered_text.count("—" + flag_name.lower()) > 0))

    @staticmethod
    def parse_color(args) -> tuple:
        """ Gets RGB color from a string. """
    
        if isinstance(args, str):
            args = tuple(args.split())
    
        string = "".join(args).lower()
        
        if string.startswith("rgb(") and string.endswith(")"):
            string = string[4:-1]
        if string.count(",") >= 2:
            try:
                return tuple([int(i) for i in string.split(",")])[:3]
            except:
                return
        
        try:
            return ImageColor.getrgb(" ".join(args))
        except:
            return
    
    @staticmethod
    def parse_role(ctx, text: str, return_array: bool = False):
        parse = list(Parser.ROLES_REGEX.finditer(text))
        if parse != []:
            try:
                role = ctx.guild.get_role(int(parse[0].group()[:3][:-1]))
                assert role
                return role
            except:
                return
        
        try:
            if text.isnumeric():
                role = ctx.guild.get_role(int(text))
                if role:
                    return role
            res = [i for i in ctx.guild.roles if text.lower() in i.name.lower()]
            assert res
            if return_array:
                return res
            return res[0]
        except:
            return

    @staticmethod
    def parse_channel(ctx, text: str, return_array: bool = False):
        parse = list(Parser.CHANNEL_REGEX.finditer(text))
        if parse != []:
            try:
                channel = ctx.guild.get_channel(int(parse[0].group()[:2][:-1]))
                assert channel
                return channel
            except:
                return
        
        try:
            if text.isnumeric():
                channel = ctx.guild.get_channel(int(text))
                if channel:
                    return channel
            res = [i for i in ctx.guild.channels if text.lower() in i.name.lower()]
            assert res
            if return_array:
                return res
            return res[0]
        except:
            return

    @staticmethod
    async def parse_emoji(ctx, text: str) -> str:
        """ Gets emoji URL from a text. """

        is_animated = "<a:" in text
        if is_animated:
            text = text.replace("<a:", "<:")

        _iter = list(Parser.EMOJI_REGEX.finditer(text))
        if not _iter:
            twemoji = await emoji_to_url(text, session=ctx.bot.http._HTTPClient__session)
            if twemoji == text:
                return
            return twemoji
        try:
            emoji_id = int(_iter[0].group().split(":")[2].split(">")[0])
            supposed_url = f"https://cdn.discordapp.com/emojis/{emoji_id}{'.gif' if is_animated else '.png'}"
            is_valid = await Parser.__check_url(ctx, url=supposed_url, cdn_only=True, custom_emoji=True)
            assert is_valid
            return supposed_url
        except:
            return

    @staticmethod
    def get_numbers(args: tuple, count: int = 1):
        """ Get numbers from args """
        
        try: return [int(i) for i in args if i.isnumeric()][0:count]
        except: return

    @staticmethod
    async def __check_url(ctx, url: str, cdn_only: bool, custom_emoji: bool = False):
        try:
            if (not custom_emoji) and cdn_only:
                assert url.startswith("https://cdn.discordapp.com")
            
            data = await ctx.bot.http._HTTPClient__session.get(url)
            assert data.status == 200
            if custom_emoji:
                return True
            
            assert data.headers['Content-Type'].startswith('image/')
            assert (int(data.headers['Content-Length'])/1024/1024) < 2
            return True
        except:
            return False

    @staticmethod
    async def parse_image(ctx, args, default_to_png=True, size=1024, member_only=False, cdn_only=False):
        """
        Gets the image from message.
        Either it's attachment, a URL, or just a mention to get someone's avatar.
        Disabling member_only will also detect URL or attachment.
        Enabling cdn_only will only detect cdn.discordapp.com urls.
        """
        if ctx.message.attachments and (not member_only):
            res = await Parser.__check_url(ctx, ctx.message.attachments[0].url, cdn_only)
            if res:
                return str(ctx.message.attachments[0].url)
        
        if not args:
            return str(ctx.author.avatar_url_as(format=("png" if (default_to_png or (not ctx.author.is_avatar_animated())) else "gif"), size=size))
        
        url = "".join(args).replace("<", "").replace(">", "")
        if ((url.startswith("http")) and ("://" in url)) and (not member_only):
            is_valid = await Parser.__check_url(ctx, url, cdn_only)
            if (not member_only) and is_valid:
                return url
        
        _filtered = "".join(args).replace(" ", "").lower()
        
        if (_filtered.startswith("<") and _filtered.endswith(">")) and (not member_only) and (_filtered.count(":") > 1):
            _extension = ".gif" if _filtered.startswith("<a") else ".png"
            try:
                if default_to_png:
                    assert _extension == ".png"
                
                _id = int(_filtered.split(':')[2].split('>')[0])
                _url = f"https://cdn.discordapp.com/emojis/{_id}{_extension}"
                is_valid = await Parser.__check_url(ctx, _url, cdn_only=True, custom_emoji=True)
                assert is_valid
                return _url
            except:
                pass
        
        if (not member_only) and (not cdn_only):
            _emoji = await emoji_to_url(_filtered, session=ctx.bot.http._HTTPClient__session)
            if _emoji != _filtered:
                return _emoji
        
        user = Parser.parse_user(ctx, args)
        return str(user.avatar_url_as(format=("gif" if ((not default_to_png) or user.is_avatar_animated()) else "png"), size=size))

    @staticmethod
    def parse_user(ctx, args, allownoargs=True):
        """
        Gets the user from message.
        Parameters can be either User ID, username, mention, or just nothing.
        Disabling allownoargs will raise an Error if there is no arguments.

        user = Parser.parse_user(ctx, *args)
        """
        args = tuple(args)
        if not args:
            if not allownoargs:
                raise Excception("Please add a mention, user ID, or a user name.")
            
            return ctx.author
        elif ctx.message.mentions: return ctx.message.mentions[0]
        
        guild_members = list(map(lambda x: x.id, ctx.guild.members))

        try:
            if args[0].isnumeric():
                _temp = guild_members.index(int(args[0]))
                return ctx.guild.get_member(int(args[0]))
        except:
            return ctx.author
        
        user_name = " ".join(args).lower()
        member = list(filter(lambda x: (x.display_name.lower().startswith(user_name)) or (user_name in x.display_name.lower()), ctx.guild.members))
        if member:
            return member[0]
        
        return ctx.author
    
    @staticmethod
    def split_args(args: tuple, amount: int = 2):
        """
        Splits a text to multiple text text.
        Detects comma, |, semicolon, or spaces.
        """
        
        _str = " ".join(args)
        for i in Parser.SPLIT_CHARACTERS:
            _split = _str.split(i)
            if (len(_split) >= amount) and (not _split.count("")):
                return _split[:amount]
        
        raise BasicCommandException(f"This command requires at least {amount} arguments.")
    
    @staticmethod
    def html_to_markdown(text: str) -> str:
        """ Converts HTML string to markdown string. """
    
        result = text.lower()
        for key in Parser.HTML_DICT.keys():
            result = result.replace(key, Parser.HTML_DICT[key])
        return result