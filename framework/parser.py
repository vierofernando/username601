from requests import get
from .emote import emoji_to_url, valid_src
from discord import Embed, Color

class Parser:
    ALPHABET = list("abcdefghijklmnopqrstuvwxyz0123456789~!@#$%^&*()_+`-=[];',./{}|:")

    def __init__(self, text, arguments: list = None) -> None:
        """
        An object of a parser.
        
        Example:
        
        parser = Parser(ctx)
        parser.add_argument("--argument")
        parser.add_argument("--required", is_required=True)
        parser.add_argument("--value", is_required=True, get_value=True, value_placeholder="value_name")
        
        result = await parser.parse()
        
        if not parser.success:
            return
        
        print(result)
        
        """
        content = ctx.message.content.lower().split()
        
        self.ctx = ctx
        self.args = tuple(content[1:])
        self.arguments = [] if arguments is None else arguments
        self.usage = content[0] + " "
        self.__is_valid_value = (lambda x: x in range(len(self.args)))
        self._argument_names = []
        self.success = False
        
        if self.arguments != []:
            for arg in arguments:
                self.__update_usage(arg)
    
    def add_argument(self, argument_name: str, is_required: bool = False, get_value: bool = False, value_placeholder: str = "argument") -> None:
        """
        Adds an argument manually.
        argument_name = the argument name. example `--arg`
        is_required = if the argument is required.
        get_value = gets the value after the argument. e.g: `--arg parameter` and returns a `parameter`
        value_placeholder = the name to show in the usage (in case an error.)
        
        """
        __arg = {
            "name": argument_name.lower(),
            "required": is_required,
            "get": get_value,
            "value": value_placeholder
        }
        
        self.arguments.append(__arg)
        self.__update_usage(__arg)
    
    def __update_usage(self, element: dict):
        _end = ">" if element["required"] else "]"
        __extra = _end if not element["get"] else " " + element["value"] + _end
        if element["required"]:
            self.usage += "<" + element["name"] + __extra
        else:
            self.usage += "[" + element["name"] + __extra
        
        self._argument_names.append(element["name"])
    
    def __parse_value(self, index):
        _res = ""
    
        if self.args[index].startswith('"'):
            for arg in self.args[index:]:
                _res += arg + " "
                if arg.endswith('"') or (arg in self._argument_names):
                    break
        else:
            return self.args[index]
        
        if _res:
            return _res[:-1].replace('"', "")
        return None
    
    async def parse(self) -> dict:
        """ Parses the whole thing. """
        
        if self.arguments == []: return
        
        _res_dict = {}
        for argument in self.arguments:

            if (argument["name"] not in self.args):
                _res_dict[argument["name"]] = {"exists": False, "value": None}
                if argument["required"]:
                    await self.ctx.send(embed=Embed(title="Missing required argument", description="This command is missing a `{}`.\nUsage: ```{}```".format(argument["name"], self.usage)).set_footer(text="P.S: <arg> is required and [arg] is optional. Do NOT literally type the [] or <>."))
                    return _res_dict
                continue
                
            try:
                assert argument["get"]
                _index = self.args.index(argument["name"]) + 1
                assert self.__is_valid_value(_index)
                _value = self.__parse_value(_index)
                assert _value is not None
            except:
                _value = None
            
            _res_dict[argument["name"]] = {"exists": True, "value": _value}
        
        self.success = True
        return _res_dict

    @staticmethod
    def __check_url(url: str, cdn_only: bool):
        try:
            if cdn_only:
                assert url.startswith("https://cdn.discordapp.com")
            
            data = get(url, timeout=5)
            assert data.headers['Content-Type'].startswith('image/')
            assert (int(data.headers['Content-Length'])/1024/1024) < 2
            return True
        except:
            return False

    @staticmethod
    def is_mentionable(name: str):
        """
        Checks if a name is mentionable.
        """
        name = name.replace(" ", "").lower()
        
        for char in name:
            if char in Parser.ALPHABET: return True
        return False

    @staticmethod
    def parse_image(ctx, args, default_to_png=True, size=1024, member_only=False, cdn_only=False):
        """
        Gets the image from message.
        Either it's attachment, a URL, or just a mention to get someone's avatar.
        Disabling member_only will also detect URL or attachment.
        Enabling cdn_only will only detect cdn.discordapp.com urls.
        """
        if len(args) < 1:
            if default_to_png: return str(ctx.author.avatar_url_as(format="png", size=size))
            return str(ctx.author.avatar_url_as(size=size))
        
        if (len(ctx.message.attachments) > 0) and (not member_only):
            res = Parser.__check_url(ctx.message.attachments[0].url, cdn_only)
            if res:
                return str(ctx.message.attachments[0].url)
        
        url = "".join(args).replace("<", "").replace(">", "")
        if ((url.startswith("http")) and ("://" in url)) and (not member_only):
            if (not member_only) and Parser.__check_url(url, cdn_only):
                return url
        
        _filtered = "".join(args).replace(" ", "").lower()
        
        if (_filtered.startswith("<") and _filtered.endswith(">")) and (not member_only):
            _extension = ".gif" if _filtered.startswith("<a") else ".png"
            try:
                if default_to_png:
                    assert _extension == ".png"
                
                _id = int(_filtered.split(':')[2].split('>')[0])
                _url = f"https://cdn.discordapp.com/emojis/{_id}{_extension}"
                assert valid_src(_url)
                return _url
            except: pass
        
        if (not member_only) and (not cdn_only):
            _emoji = emoji_to_url(_filtered)
            if _emoji != _filtered:
                return _emoji
        
        user = Parser.parse_user(ctx, args)
        if not default_to_png: return str(user.avatar_url_as(size=size))
        return str(user.avatar_url_as(format="png", size=size))

    @staticmethod
    def parse_user(ctx, args, allownoargs=True):
        """
        Gets the user from message.
        Parameters can be either User ID, username, mention, or just nothing.
        Disabling allownoargs will raise an Error if there is no arguments.

        user = Parser.parse_user(ctx, *args)
        """
        args = tuple(args)
        if len(args) < 1:
            if not allownoargs:
                
                if hasattr(ctx.bot, "utils"):
                    raise ctx.bot.utils.send_error_message("Please add a mention, user ID, or a user name.")
                raise Exception("Please add a mention, user ID, or a user name.")
            
            return ctx.author
        elif len(ctx.message.mentions) > 0: return ctx.message.mentions[0]
        
        guild_members = list(map(lambda x: x.id, ctx.guild.members))

        try:
            if args[0].isnumeric():
                _temp = guild_members.index(int(args[0]))
                return ctx.guild.get_member(int(args[0]))
        except:
            return ctx.author
        
        user_name = " ".join(args).lower()
        member = filter(lambda x: (x.name.lower().startswith(user_name)) or (user_name in x.name.lower()), ctx.guild.members)
        if len(member) > 0: return member[0]
        
        return ctx.author