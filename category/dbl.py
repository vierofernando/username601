from os import environ
from discord.ext import commands, tasks
from sys import path
from os import environ
path.append(environ['BOT_MODULES_DIR'])
from decorators import command, cooldown
from requests import get
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
        self.api_url = "https://top.gg/api/"
        self._dbl_type = {
            "admin": "DBL Administrator",
            "webMod": "DBL Website Moderator",
            "mod": "DBL Moderator",
            "certifiedDev": "Certified DBL Developer",
            "supporter": "DBL Supporter"
        }
        self._social_prefix = {
            "github": "/",
            "instagram": "@",
            "reddit": "u/",
            "twitter": "@",
            "youtube": "/"
        }
        self._bot_links = {"invite": "", "website": "", "support": "https://discord.gg/", "github": ""}
        self._bot_subtitution = {"invite": "Invite this Bot", "website": "Official Website", "support": "Support Server", "github": "GitHub Repository"}
    
    def resolve_user(self, ctx, args):
        if "".join(args[1:]).isnumeric():
            _input = DummyUserClass(id=int("".join(args[1])), avatar_url=None, bot=False, is_avatar_animated=(lambda: False))
        elif len(ctx.message.mentions) > 0:
            _input = ctx.message.mentions[0] if (not ctx.message.mentions[0].bot) else ctx.author
        else:
            _input = self.client.utils.getUser(ctx, args[1:])
        
        if _input.bot: raise self.client.utils.send_error_message(str(_input) + " is a bot.")
        data = get(self.api_url + "/users/" + str(_input.id), headers={"Authorization": "Bearer "+environ["DBL_TOKEN"]}).json()
        
        if data.get("error") is not None:
            raise self.client.utils.send_error_message(str(_input) + " does not exist in the [top.gg](https://top.gg/) database.")
        _ext = ".gif" if _input.is_avatar_animated() else ".png"
        _social = "\n".join([
            (key + ": " +self._social_prefix[key] + data["social"][key] if data["social"].get(key) else "<?>") for key in self._social_prefix.keys()
        ])
        _social = _social.replace("\n<?>", "").replace("<?>", "")
        if not _social: _social = "`<not provided>`" # lmao this statement
        _bio = "***\""+data["bio"].replace("*", "\*")+"\"***" if data.get("bio") else "This user has no bio."
        
        return self.client.Embed(
            ctx,
            title=data["username"] + "#" + data["discriminator"],
            image=data.get("banner"),
            desc="***\""+_bio+"\"***\n\nColor: `" + data['color'] + "`",
            fields={
                "User Type": "\n".join([
                    (":white_check_mark:" if data[key] else ":x:") + " " + self._dbl_type[key] for key in self._dbl_type.keys()
                ]),
                "Social Links": _social
            },
            thumbnail=(_input.avatar_url if _input.avatar_url is not None else "https://cdn.discordapp.com/avatars/"+data["id"]+"/"+data["avatar"]+".png"),
            url="https://top.gg/user/"+data["id"]
        )
    
    def get_owner_name(self, id):
        data = get("https://top.gg/api/users/"+str(id), headers={"Authorization": "Bearer "+environ["DBL_TOKEN"]}).json()
        if data.get("error") is not None: return "<not available>"
        return data["username"] + "#" + data["discriminator"]
    
    async def search_bots(self, ctx, query):
        data = get("https://top.gg/api/search?q="+str(query)+"&type=bot").json()["results"]
        _length = len(data)
        
        if _length == 0: raise self.client.utils.send_error_message("That bot does not exist on the [top.gg](https://top.gg/) database.")
        elif _length == 1:
            return data[0]["id"]
        
        embed = await self.client.Embed(
            ctx,
            title=f"Found {_length} matches.",
            desc="**Send the number:**\n" + ("\n".join(["`"+str(i + 1)+"` ["+data[i]["name"]+"](https://top.gg/bot/"+data[i]["id"]+")" for i in range(_length)]))
        ).send()
        _check = (lambda x: x.channel == ctx.channel and x.author == ctx.author and x.content.isnumeric())
        message = await self.client.utils.wait_for_message(ctx, message=None, func=_check, timeout=30.0)
        if message is None: return
        elif int(message.content) not in range(1, _length + 1): return
        await embed.delete()
        return data[int(message.content) - 1]["id"]
    
    async def resolve_bot(self, ctx, args):
        if len(args[1:]) == 0:
            _id = str(self.client.user.id)
        elif len(ctx.message.mentions) > 0:
            _id = str(ctx.message.mentions[0].id) if ctx.message.mentions[0].bot else str(self.client.user.id)
        elif "".join(args[1:]).isnumeric():
            _id = "".join(args[1:])
        else:
            _id = await self.search_bots(ctx, self.client.utils.encode_uri(" ".join(args[1:])))
            if _id is None: return
        
        data = get(self.api_url + "/bots/" + _id, headers={"Authorization": "Bearer "+environ["DBL_TOKEN"]}).json()
        
        if data.get("error") is not None:
            raise self.client.utils.send_error_message("That bot does not exist in the [top.gg](https://top.gg/) database.")
        _links = "\n".join([("["+self._bot_subtitution[key]+"]("+self._bot_links[key]+data[key]+")" if data.get(key) else "??") for key in self._bot_links.keys()])
        _links = _links.replace("\n??", "")
        
        return self.client.Embed(
            ctx,
            title=data["username"] + "#" + data["discriminator"],
            url="https://top.gg/bot/" + data["id"],
            desc="***\"" + data["shortdesc"] + "\"***",
            fields={
                "General Information": "**Published at: **"+data["date"][:-5].replace("T", " ")+"\n**Bot Prefix: **`"+data["prefix"]+"`\n**Discord Library: **`"+data["lib"]+"`\n**Tags: **"+(
                    " - ".join(["["+key+"](https://top.gg/tag/"+key.lower().replace(" ", "-")+")" for key in data["tags"]])
                ),
                "Bot Stats": "**Server Count: **`"+(str(data["server_count"]) if data.get("server_count") else "<not shown>")+"`\n**Shard Count: **`"+str(len(data["shards"]))+"`\n"+(":white_check_mark:" if data["certifiedBot"] else ":x:")+" Certified DBL Bot\n**"+str(data["points"])+"** Upvotes\n**"+str(data["monthlyPoints"])+"** Upvotes in this month",
                "Bot Developers": ", ".join(["["+self.get_owner_name(_id)+"](https://top.gg/user/"+str(_id)+")" for _id in data["owners"]]),
                "Links": _links
            },
            thumbnail="https://cdn.discordapp.com/avatars/{}/{}.png".format(data["id"], data["avatar"])
        )
    
    @command("dbl,top-gg,botlist,discordbotlist") 
    @cooldown(7)
    async def topgg(self, ctx, *args):
        if (len(args) == 0) or (args[0].lower() not in self.types):
            embed = self.client.Embed(ctx, title="top.gg command usage", desc=f"Usage:\n`{self.client.command_prefix[0]}topgg bot <bot_name>`\n`{self.client.command_prefix[0]}topgg user <user_name/mention/user_id>`", url="https://top.gg/")
            return await embed.send()
        _type = args[0].lower() if (args[0].lower().endswith("s")) else args[0].lower() + "s"
        if _type == "users":
            embed = self.resolve_user(ctx, args)
            return await embed.send()    
        else:
            embed = await self.resolve_bot(ctx, args)
            if embed is None: return
            return await embed.send()

def setup(bot):
    bot.add_cog(dbl(bot))