import discord
from discord.ext import commands
from json import loads
from decorators import *
from time import time

class bothelp(commands.Cog):
    def __init__(self, client):
        self._categories = "\n".join([f"{i + 2}. `{client.cmds.categories[i]}`" for i in range(len(client.cmds.categories))])
        self._init_help = [discord.Embed(title="The bot help embed™️", description="Use the reactions to move to the next page.\n\n**PAGES:**\n1. `This page`\n"+self._categories)]
        self.db = client.db
    
    @command(['supportserver', 'support-server', 'botserver', 'bot-server'])
    @cooldown(1)
    async def support(self, ctx):
        return await ctx.send(ctx.bot.util.server_invite)

    @command(['cl', 'history', 'updates'])
    @cooldown(5)
    async def changelog(self, ctx, *args):
        data = "\n".join(self.db.get("config", {"h": True})["changelog"])
        embed = ctx.bot.Embed(
            ctx,
            title="Bot Changelog",
            desc=data,
            footer="Sorry if it looks kinda stinky"
        )
        await embed.send()
        del embed, data

    @command(['commands', 'yardim', 'yardım'])
    @cooldown(2)
    async def help(self, ctx, *args):
        if not args:
            embeds = self._init_help
            for category in ctx.bot.cmds.categories:
                embed = discord.Embed(title=category, description="**Commands:**```"+(", ".join([command['name'] for command in ctx.bot.cmds.get_commands_from_category(category.lower())]))+"```")
                embed.set_footer(text=f"Type `{ctx.bot.command_prefix}help <command>` to view command in a detailed version.")
                embeds.append(embed)
            
            paginator = ctx.bot.EmbedPaginator(ctx, embeds, show_page_count=True, auto_set_color=True)
            return await paginator.execute()
        
        data = ctx.bot.cmds.query(' '.join(args).lower())
        if not data: raise ctx.error_message("Your command/category name does not exist, sorry!")
        
        embed = ctx.bot.ChooseEmbed(ctx, data, key=(lambda x: "[`"+x["type"]+"`] `"+x["name"]+"`"))
        result = await embed.run()
        
        if not result: return
        is_command = (result["type"] == "COMMAND")
        data = ctx.bot.cmds.get_command_info(result["name"].lower()) if is_command else ctx.bot.cmds.get_commands_from_category(result["name"].lower())
        
        desc = '**Command name: **{}\n**Function: **{}\n**Category: **{}'.format(
            data['name'], data['function'], data['category']
        ) if is_command else '**Commands count: **{}\n**Commands:**```{}```'.format(len(data), ', '.join([i['name'] for i in data]))
        embed = ctx.bot.Embed(ctx, title="Help for "+result["type"].lower()+": "+result["name"], desc=desc)
        if is_command:
            parameters = "```"+'\n'.join([i.split(": ")[1] for i in data['parameters']])+"```" if data['parameters'] else "No parameters required."
            apis = '\n'.join(map(lambda x: f"[{x}]({x})", data['apis'])) if data['apis'] else 'No APIs used.'
            embed.fields = {
                'Parameters': parameters,
                'APIs used': apis
            }
        return await embed.send()

    @command()
    @cooldown(2)
    async def vote(self, ctx):
        embed = ctx.bot.Embed(
            ctx,
            title=f'{ctx.me.display_name} seems sus. let\'s vote for him!',
            url=f'https://top.gg/bot/{ctx.bot.user.id}/vote'
        )
        await embed.send()
        del embed
    
    @command(['inviteme', 'invitelink', 'botinvite', 'invitebot', 'addtoserver', 'addbot'])
    @cooldown(2)
    async def invite(self, ctx):
        embed = ctx.bot.Embed(
            ctx,
            title='invite this bot please the bot developer is desperate',
            url=f'https://discord.com/api/oauth2/authorize?client_id={ctx.bot.user.id}&permissions=8&scope=bot'
        )
        await embed.send()
        del embed
    
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
        msgping = round((time() - ctx.message.created_at.timestamp())*1000)
        await ctx.trigger_typing()
        wsping = round(ctx.bot.ws.latency*1000)
        embed = ctx.bot.Embed(
            ctx,
            title="PongChamp!",
            desc=f"**Message latency:** `{msgping}ms`\n**Websocket latency:** `{wsping}ms`",
            thumbnail='https://i.pinimg.com/originals/21/02/a1/2102a19ea556e1d1c54f40a3eda0d775.gif'
        )
        await embed.send()
        del embed, wsping, msgping

    @command(['botstats', 'meta'])
    @cooldown(10)
    async def stats(self, ctx):
        await ctx.trigger_typing()
        data = await ctx.bot.util.get_stats()
        
        embed = ctx.bot.Embed(
            ctx,
            title="Bot Stats",
            fields={
                "Uptime": f"**Bot Uptime: **{ctx.bot.util.strfsecond(data['bot_uptime'])}\n**OS Uptime: **{data['os_uptime']}",
                "Stats": f"**Server count: **{len(ctx.bot.guilds)}\n**Served users: **{len(ctx.bot.users)}\n**Cached custom emojis: **{len(ctx.bot.emojis)}",
                "Platform": f"**Machine: **{data['versions']['os']}\n**Python Build: **{data['versions']['python_build']}\n**Python Compiler: **{data['versions']['python_compiler']}\n**Discord.py version: **{data['versions']['discord_py']}"
            }
        )
        
        await embed.send()

def setup(client):
    client.add_cog(bothelp(client))