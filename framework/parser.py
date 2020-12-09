from twemoji_parser import emoji_to_url

class Parser:
    SPLIT_CHARACTERS = [';', ', ', ',', '|',' | ']
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

    @staticmethod
    def get_numbers(args: tuple, count: int = 1):
        """ Get numbers from args """
        
        try: return [int(i) for i in args if i.isnumeric()][0:count]
        except: return None

    @staticmethod
    def require_args(ctx, args: tuple):
        """ The function name says it all. """
        if (len(args) == 0) or ("".join(args).replace("‏‏‎ ‎", "").replace("‏‏‎ ", "").replace("‏‏‎‎", "")) == "":
            raise ctx.bot.util.BasicCommandException(f"This command requires at least an argument. Try `{ctx.bot.command_prefix}help {ctx.command.name}`")
        return

    @staticmethod
    def get_input(args: tuple) -> tuple:
        """ Returns all inputs from a args """
        return tuple([i for i in args if i.startswith("--")])
    
    @staticmethod
    def get_input_values(args: tuple) -> dict:
        """ Returns all inputs with their values as a dict. """
        res = {}
        for i in range(len(args)):
            if not args[i].startswith("--"): continue
            try: res[args[i]] = args[i + 1]
            except: res[args[i]] = None
        return (res if res != {} else None)

    @staticmethod
    def get_value(args: tuple, text: str) -> tuple:
        """ Gets the value from a key. """
        
        res, has_quotation_mark = [], False
        try:
            index = args.index(text)
            for arg in args[(index + 1):]:
                if arg.startswith('"') and (not has_quotation_mark):
                    res.append(arg[1:])
                    has_quotation_mark = True
                elif has_quotation_mark and arg.endswith('"'):
                    res.append(arg[:-1])
                    break
                else:
                    return arg
        except:
            return
        

    @staticmethod
    async def __check_url(ctx, url: str, cdn_only: bool, custom_emoji: bool = False):
        try:
            if (not custom_emoji) and cdn_only:
                assert url.startswith("https://cdn.discordapp.com")
            
            data = await ctx.bot.util.default_client.get(url)
            assert data.status == 200
            if custom_emoji: return True
            
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
        if (len(ctx.message.attachments) > 0) and (not member_only):
            res = await Parser.__check_url(ctx, ctx.message.attachments[0].url, cdn_only)
            if res:
                return str(ctx.message.attachments[0].url)
        
        if len(args) < 1:
            if default_to_png: return str(ctx.author.avatar_url_as(format="png", size=size))
            return str(ctx.author.avatar_url_as(size=size))
        
        url = "".join(args).replace("<", "").replace(">", "")
        if ((url.startswith("http")) and ("://" in url)) and (not member_only):
            is_valid = await Parser.__check_url(ctx, url, cdn_only)
            if (not member_only) and is_valid:
                return url
        
        _filtered = "".join(args).replace(" ", "").lower()
        
        if (_filtered.startswith("<") and _filtered.endswith(">")) and (not member_only):
            _extension = ".gif" if _filtered.startswith("<a") else ".png"
            try:
                if default_to_png:
                    assert _extension == ".png"
                
                _id = int(_filtered.split(':')[2].split('>')[0])
                _url = f"https://cdn.discordapp.com/emojis/{_id}{_extension}"
                is_valid = await Parser.__check_url(ctx, _url, custom_emoji=True)
                assert is_valid
                return _url
            except: pass
        
        if (not member_only) and (not cdn_only):
            _emoji = await emoji_to_url(_filtered)
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
                raise Excception("Please add a mention, user ID, or a user name.")
            
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
        member = list(filter(lambda x: (x.display_name.lower().startswith(user_name)) or (user_name in x.display_name.lower()), ctx.guild.members))
        if len(member) > 0: return member[0]
        
        return ctx.author
    
    @staticmethod
    def split_content_to_two(args: tuple):
        """
        Splits a text to two text.
        Detects comma, |, semicolon, or spaces.
        """
        
        if ((args is None) or (len(args) < 2)): return None
        if len(args) == 2: return args[0], args[1]
        
        args_as_a_string = ' '.join(list(args))
        for char in Parser.SPLIT_CHARACTERS:
            if char in args_as_a_string: return args_as_a_string.split(char)[0], char.join(args_as_a_string.split(char)[1:])
        return args[0], ' '.join(args[1:])
    
    @staticmethod
    def html_to_markdown(text: str) -> str:
        """ Converts HTML string to markdown string. """
    
        result = text.lower()
        for key in Parser.HTML_DICT.keys():
            result = result.replace(key, Parser.HTML_DICT[key])
        return result
    
    @staticmethod
    def without(args: tuple, key: str) -> tuple:
        """ Returns an arg without a specific key. """
        return tuple([i for i in args if key not in i])