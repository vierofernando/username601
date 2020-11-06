from requests import get

class Parser:
    ALPHABET = list("abcdefghijklmnopqrstuvwxyz0123456789~!@#$%^&*()_+`-=[];',./{}|:")

    @staticmethod
    def __check_url(url: str):
        try:
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
        
        for char in Parser.ALPHABET:
            if char in name: return False
        return True

    @staticmethod
    def parse_image(ctx, default_to_png=True, size=1024, *args):
        """
        Gets the image from message.
        Either it's attachment, a URL, or just a mention to get someone's avatar.
        """
        if len(args) < 1:
            if default_to_png: return ctx.author.avatar_url_as(format="png", size=size)
            return ctx.author.avatar_url_as(size=size)
        
        if len(ctx.message.attachments) > 0:
            res = Parser.__check_url(ctx.message.attachments[0].url)
            if res:
                return str(ctx.message.attachments[0].url)
        
        url = "".join(args).replace("<", "").replace(">", "")
        if ((url.startswith("http")) and ("://" in url)):
            if Parser.__check_url(url):
                return url
        
        user = Parser.parse_user(ctx, *args)
        if not default_to_png: return str(user.avatar_url_as(size=size))
        return str(user.avatar_url_as(format="png", size=size))

    @staticmethod
    def parse_user(ctx, *args):
        """
        Gets the user from message.
        Parameters can be either User ID, username, mention, or just nothing.

        user = Parser.parse_user(ctx, *args)
        """
        args = tuple(args)
        if len(args) < 1: return ctx.author
        elif len(ctx.message.mentions) > 0: return ctx.message.mentions[0]
        
        guild_members = list(map(lambda x: x.id, ctx.guild.members))

        try:
            if args[0].isnumeric():
                try:
                    _temp = guild_members.index(int(args[0]))
                    return ctx.guild.get_member(int(args[0]))
                except ValueError:
                    return ctx.author
        except:
            return ctx.author
        
        user_name = " ".join(args).lower()
        for member in ctx.guild.members:
            if str(member).lower().startswith(user_name): return member
            elif user_name in str(member).lower(): return member

        return ctx.author
    
    @staticmethod
    def parameter_exists(args: tuple, flag: str, return_as_bool=False, return_index=False):
        """
        Check if a specific flag exists on a argument.
        Returns None if it doesn't exist,
        otherwise returns a tuple without the flag.
        Example:

        args = ("!say", "hello", "--hidden")
        res = Parser.parameter_exists(args, "--hidden")
        if res:
            await ctx.message.delete()
        else:
            res = args
        return await ctx.send(res)

        """
        try:
            statement = list(map(lambda x: x.lower(), args)).index(flag.lower())
            if return_index: return statement
            return tuple(filter(lambda x: x != args[statement], args))
        except:
            return None