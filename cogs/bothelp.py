import discord
from discord.ext import commands
from datetime import datetime
from json import loads
from decorators import *
from time import time

class bothelp(commands.Cog):
    def __init__(self, client):
        self._categories = "\n".join([f"{i + 2}. `{client.cmds.categories[i]}`" for i in range(len(client.cmds.categories))])
        self._init_help = [discord.Embed(title="The bot help embed™️", description="Use the reactions to move to the next page.\n\n**PAGES:**\n1. `This page`\n"+self._categories)]
        self.db = client.db
        self._cooldown_types = ("", ", **server-wide**", ", **channel-wide**")
    
    @command(['supportserver', 'support-server', 'botserver', 'bot-server'])
    @cooldown(1)
    async def support(self, ctx):
        return await ctx.send(ctx.bot.util.server_invite)

    @command(['cl', 'history', 'updates'])
    @cooldown(5)
    async def changelog(self, ctx, *args):
        data = "\n".join(self.db.get("config", {"h": True})["changelog"])
        await ctx.embed(title="Bot Changelog", description=data, footer="Sorry if it looks kinda stinky")
        del data

    @command(['commands', 'yardim', 'yardım'])
    @cooldown(2)
    @permissions(bot=['add_reactions'])
    async def help(self, ctx, *args):
        if not args:
            embeds = self._init_help
            for category in ctx.bot.cmds.categories:
                embed = discord.Embed(title=category, description="**Commands:**```"+(", ".join([command['name'] for command in ctx.bot.cmds.get_commands_from_category(category.lower())]))+"```")
                embed.set_footer(text=f"Type `{ctx.prefix}help <command>` to view command in a detailed version.")
                embeds.append(embed)
            
            paginator = ctx.bot.EmbedPaginator(ctx, embeds, show_page_count=True, auto_set_color=True)
            return await paginator.execute()
        
        await ctx.trigger_typing()
        command = ctx.bot.all_commands.get(" ".join(args).lower().lstrip("_"))
        
        try:
            assert bool(command)
            command_info = list(filter(lambda x: x["name"] == command.name.lstrip("_"), ctx.bot.cmds.commands))[0]
        except:
            raise ctx.error_message("No such command exists.")
        
        usage = [f"{ctx.prefix}{command.name}"]
        usage.extend(map(lambda x: ctx.prefix + x.split(": ")[1], command_info["parameters"]))
        cooldown = command.get_cooldown_retry_after(ctx)
        embed = ctx.bot.Embed(ctx, title=f"Command help for {command.name}", description=command_info["function"], fields={"Usage": '```'+"\n".join(usage)+'```', "Category": command_info["category"], "Cooldowns": f"{':x:' if bool(cooldown) else ':white_check_mark:'} {ctx.bot.util.strfsecond(command._buckets._cooldown.rate)}{self._cooldown_types[command._buckets._cooldown.type.value - 1]} ({ctx.bot.util.strfsecond(cooldown)} for you)" if command._buckets.valid else ":white_check_mark: No Cooldowns"})
        if command_info["apis"]:
            embed.add_field("APIs used", "\n".join(map(lambda x: f"[{x}]({x})", command_info["apis"])))
        if command.aliases:
            embed.add_field("Aliases", ", ".join(map(lambda x: f"`{x}`", command.aliases)))
        await embed.send()
        del usage, cooldown, embed, command, command_info

    @command()
    @cooldown(2)
    async def vote(self, ctx):
        return await ctx.embed(title=f'{ctx.me.display_name} seems sus. let\'s vote for him!', url=f'https://top.gg/bot/{ctx.bot.user.id}/vote')
    
    @command(['inviteme', 'invitelink', 'botinvite', 'invitebot', 'addtoserver', 'addbot'])
    @cooldown(2)
    async def invite(self, ctx):
        return await ctx.embed(title='invite this bot please the bot developer is desperate', url=f'https://discord.com/api/oauth2/authorize?client_id={ctx.bot.user.id}&permissions=8&scope=bot')
    
    @command(['report', 'suggest', 'bug', 'reportbug', 'bugreport'])
    @cooldown(15)
    @require_args()
    async def feedback(self, ctx, *args):
        if (('discord.gg/' in ' '.join(args)) or ('discord.com/invite/' in ' '.join(args))):
            raise ctx.error_message("Please do NOT send invites. This is NOT advertising.")
        
        await ctx.trigger_typing()
        banned = [i for i in self.db.get("config", {"h": True})["bans"] if i.startswith(str(ctx.author.id))]
        
        if not banned:
            try:
                feedback_channel = ctx.bot.get_channel(ctx.bot.util.feedback_channel)
                await feedback_channel.send(f'<@{ctx.bot.util.owner_id}>, User with ID: {ctx.author.id} sent a feedback: **"'+' '.join(args)[:500]+'"**')
                embed = discord.Embed(title='Feedback Successful', description='**Success!**\nThanks for the feedback!\n**We will DM you as the response. **If you are unsatisfied, [Join our support server and give us more details.]('+ctx.bot.util.server_invite+')', colour=ctx.me.color)
                return await ctx.send(embed=embed)
            except:
                raise ctx.error_message('There was an error while sending your feedback. Sorry! :(')
        reason = "|".join(banslist[0].split("|")[1:])
        raise ctx.error_message(f"You have been banned from using the Feedback command.\nReason: {reason}")
     
    @command()
    @cooldown(2)
    async def ping(self, ctx):
        msgping, wsping = round((time() - ctx.message.created_at.timestamp())*1000), round(ctx.bot.ws.latency*1000)
        await ctx.embed(title="PongChamp!", description=f"**Message latency:** `{msgping}ms`\n**Websocket latency:** `{wsping}ms`", thumbnail='https://i.pinimg.com/originals/21/02/a1/2102a19ea556e1d1c54f40a3eda0d775.gif')
        del wsping, msgping

    @command(['botstats', 'meta'])
    @cooldown(10)
    async def stats(self, ctx, *args):
        await ctx.trigger_typing()
        config = self.db.get("config", {"h": True})
        
        if args and (args[0] == "uptime"):
            last_downtime = datetime.strptime(config['down_times'][-1].split("|")[0], "%Y-%m-%dT%H:%M:%SZ")
            data = "\n".join(list(map(lambda x: f'{ctx.bot.util.timestamp(x.split("|")[0], include_time_past=False).split(", ")[1][:-1]}, with an uptime of **{x.split("|")[1]}**', config['down_times'][::-1][1:])))
            return await ctx.embed(title="Bot Uptime Data", description=f"**Downtime History:**\n{data}", fields={ "Current Uptime": ctx.bot.util.strfsecond(time() - ctx.bot.util._start), "Last Downtime": f'{ctx.bot.util.timestamp(last_downtime, include_time_past=False)[:-1]}, happens for **{ctx.bot.util.strfsecond(time() - last_downtime.timestamp())}**' })
        
        data = await ctx.bot.util.get_stats()
        return await ctx.embed(title="Bot Stats", fields={
            "Uptime": f"**OS Uptime: **{data['os_uptime']}**Bot Uptime: **`See '{ctx.prefix}stats uptime' for more info`",
            "Stats": f"**Server count: **{len(ctx.bot.guilds):,}\n**Served users: **{len(ctx.bot.users):,}\n**Cached custom emojis: **{len(ctx.bot.emojis):,}\n**Commands Ran throughout Runtime: **{ctx.bot.command_uses:,}\n**Total Commands Ran: **{config['commands_run']:,}\n**Banned users: **{len(config['bans']):,}",
            "Platform": f"**Machine: **{data['versions']['os']}\n**Python Build: **{data['versions']['python_build']}\n**Python Compiler: **{data['versions']['python_compiler']}\n**Discord.py version: **{data['versions']['discord_py']}"
        })

def setup(client):
    client.add_cog(bothelp(client))