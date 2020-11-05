from requests import get

class Parser:
    @staticmethod
    def __check_url(url):
        try:
            data = get(url, timeout=5)
            assert data.headers['Content-Type'].startswith('image/')
            assert (int(data.headers['Content-Length'])/1024/1024) < 2
            return True
        except:
            return False

    @staticmethod
    def parse_image(ctx, *args):
        """
        Gets the image from message.
        Either it's attachment, a URL, or just a mention to get someone's avatar.
        """
        if len(ctx.message.attachments) > 0:
            res = Parser.__check_url(ctx.message.attachments[0].url)
            if res:
                return str(ctx.message.attachments[0].url)
        
        url = "".join(args).replace("<", "").replace(">", "")
        if ((url.startswith("http")) and ("://" in url)):
            if Parser.__check_url(url):
                return url
        
        user = Parser.parse_user(ctx, *args)
        return str(user.avatar_url_as(format="png"))

    @staticmethod
    def parse_user(ctx, *args):
        """
        Gets the user from message.
        Parameters can be either User ID, username, mention, or just nothing.

        user = Parser.parse_user(ctx, *args)
        """
        args = tuple(args)
        guild_members = list(map(lambda x: x.id, ctx.guild.members))

        if len(args) < 1: return ctx.author
        elif len(ctx.message.mentions) > 0: return ctx.message.mentions[0]

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
    def parameter_exists(args, parameter):
        try:
            statement = list(map(lambda x: x.lower(), args)).index(parameter.lower())
            return tuple(filter(lambda x: x != args[statement], args))
        except:
            return None