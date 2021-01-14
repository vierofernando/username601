from os import environ
from discord.ext import commands, tasks
from decorators import *
from aiohttp import ClientSession
from PIL import ImageColor
import dbl as topgg
import discord

class DummyUserClass:
    def __init__(self, **kwargs):
        for kwarg in kwargs.keys():
            setattr(self, kwarg, kwargs[kwarg])

class dbl(commands.Cog):
    def __init__(self, client):
        self.client = client
        self.token = environ['DBL_TOKEN']
        self.dblpy = topgg.DBLClient(client, self.token, autopost=True)
        self.types = ["bots", "users", "bot", "user"]
        self._bot_links = {"invite": "", "website": "", "support": "https://discord.gg/", "github": ""}
        self._bot_subtitution = {"invite": "Invite this Bot", "website": "Official Website", "support": "Support Server", "github": "GitHub Repository"}
        self._none = ["", None, "#"]
        self._connection = ClientSession(headers={"Authorization": "Bearer "+environ["DBL_TOKEN"]})
    
    async def get(self, path):
        res = await self._connection.get("https://top.gg/api" + path)
        return await res.json()
    
    async def resolve_user(self, ctx, args):
        if "".join(args[1:]).isnumeric():
            _input = DummyUserClass(id=int("".join(args[1])), avatar_url=None, bot=False, is_avatar_animated=(lambda: False))
        elif ctx.message.mentions:
            _input = ctx.message.mentions[0] if (not ctx.message.mentions[0].bot) else ctx.author
        else:
            _input = self.client.Parser.parse_user(ctx, args[1:])
        
        if _input.bot:
            raise ctx.error_message(str(_input) + " is a bot.")
        data = await self.get(f"/users/{_input.id}")
        
        if data.get("error"):
            raise ctx.error_message(str(_input) + " does not exist in the [top.gg](https://top.gg/) database.", description=True)
        _ext = ".gif" if _input.is_avatar_animated() else ".png"
        _bio = discord.utils.escape_markdown(data["bio"]) if data.get("bio") else "This user has no bio."
        _color = "`"+data['color'].upper()+"`" if (data.get('color') not in self._none) else "`<not set>`"
        _avatar = "https://cdn.discordapp.com/avatars/"+data["id"]+"/"+data["avatar"]+".png" if data.get("avatar") else None
        if not _avatar:
            raise ctx.error_message("That user does not exist in the [top.gg](https://top.gg/) database.", description=True)
        
        return self.client.Embed(
            ctx,
            title=data["username"] + "#" + data["discriminator"],
            image=data.get("banner"),
            fields={
                "Bio": _bio,
                "Color": _color
            },
            thumbnail=_avatar,
            url="https://top.gg/user/"+data["id"],
            color=discord.Color.from_rgb(*ImageColor.getrgb(data["color"])) if data.get("color") else ctx.me.color
        )
    
    async def get_owner_name(self, id):
        _cached_user = self.client.get_user(int(id))
        if _cached_user:
            return str(_cached_user)
        
        data = await self.get(f"/users/{id}")
        if data.get("error"): return "<not available>"
        return data["username"] + "#" + data["discriminator"]
    
    async def search_bots(self, ctx, query):
        data = await self.get(f"/search?q={query}&type=bot")
        data = data["results"] # why
        
        if not data:
            raise ctx.error_message("That bot does not exist on the [top.gg](https://top.gg/) database.", description=True)
        embed = self.client.ChooseEmbed(ctx, data, key=(lambda x: "["+x["name"]+"](https://top.gg/bot/"+x["id"]+")"))
        res = await embed.run()
        del embed, data

        if not res: return
        return res["id"]
    
    async def resolve_bot(self, ctx, args):
        if not args[1:]:
            _id = str(self.client.user.id)
        elif ctx.message.mentions:
            _id = str(ctx.message.mentions[0].id) if ctx.message.mentions[0].bot else str(self.client.user.id)
        elif "".join(args[1:]).isnumeric():
            _id = "".join(args[1:])
        else:
            _id = await self.search_bots(ctx, self.client.util.encode_uri(" ".join(args[1:])))
            if not _id: return
        
        data = await self.get(f"/bots/{_id}")
        
        if data.get("error"):
            raise ctx.error_message("That bot does not exist in the [top.gg](https://top.gg/) database.", description=True)
        _links = "\n".join([("["+self._bot_subtitution[key]+"]("+self._bot_links[key]+data[key]+")" if data.get(key) else "??") for key in self._bot_links.keys()])
        _links = _links.replace("\n??", "").replace("??", "")
        bot_devs = ""
        for _id in data['owners']:
            name = await self.get_owner_name(str(_id))
            bot_devs += f"[{name}](https://top.gg/user/{_id})\n"
        
        return self.client.Embed(
            ctx,
            title=data["username"] + "#" + data["discriminator"],
            url="https://top.gg/bot/" + data["id"],
            desc="***\"" + data["shortdesc"] + "\"***",
            fields={
                "General Information": "**Published at: **"+ctx.bot.util.timestamp(data["date"])+"\n**Bot Prefix: **`"+data["prefix"]+"`\n**Tags: **"+(
                    " - ".join(["["+key+"](https://top.gg/tag/"+key.lower().replace(" ", "-")+")" for key in data["tags"]])
                ),
                "Bot Stats": "**Server Count: **`"+(str(data["server_count"]) if data.get("server_count") else "<not shown>")+"`\n**Shard Count: **`"+str(len(data["shards"]))+"`\n"+(":white_check_mark:" if data["certifiedBot"] else ":x:")+" Certified DBL Bot\n**"+str(data["points"])+"** Upvotes\n**"+str(data["monthlyPoints"])+"** Upvotes in this month",
                "Bot Developers": bot_devs[:-1],
                "Links": _links
            },
            thumbnail="https://cdn.discordapp.com/avatars/{}/{}.png".format(data["id"], data["avatar"])
        )
    
    @command(['dbl', 'top-gg', 'botlist', 'discordbotlist']) 
    @cooldown(7)
    async def topgg(self, ctx, *args):
        if (not args) or (args[0].lower() not in self.types):
            embed = self.client.Embed(ctx, title="top.gg command usage", desc=f"Usage:\n`{self.client.command_prefix[0]}topgg bot <bot_name>`\n`{self.client.command_prefix[0]}topgg user <user_name/mention/user_id>`", url="https://top.gg/")
            return await embed.send()
        _type = args[0].lower() if (args[0].lower().endswith("s")) else args[0].lower() + "s"
        if _type == "users":
            embed = await self.resolve_user(ctx, args)
            return await embed.send() 
        else:
            embed = await self.resolve_bot(ctx, args)
            if not embed: return
            return await embed.send()

def setup(bot):
    bot.add_cog(dbl(bot))