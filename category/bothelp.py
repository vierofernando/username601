import discord
from discord.ext import commands
import sys
import requests
from json import loads
from os import getcwd, name, environ
sys.path.append(environ['BOT_MODULES_DIR'])
from decorators import command, cooldown
from datetime import datetime as t
# import selfDB, Dashboard

class bothelp(commands.Cog):
    def __init__(self, client):
        self._categories = "\n".join([f"{i + 2}. `{client.cmds.categories[i]}`" for i in range(len(client.cmds.categories))])
        self._init_help = [discord.Embed(title="The bot help embed™️", description="Use the reactions to move to the next page.\n\n**PAGES:**\n1. `This page`\n"+self._categories)]
        
    @command('supportserver,support-server,botserver,bot-server')
    @cooldown(2)
    async def support(self, ctx):
        return await ctx.send(ctx.bot.util.server_invite)

    @command('subscribe,dev,development,devupdates,dev-updates,development-updates')
    @cooldown(5)
    async def sub(self, ctx, *args):
        if len(args)==0 or 'help' in ''.join(args).lower():
            embed = discord.Embed(title='Get development updates and/or events in your server!', description='Want to get up-to-date development updates? either it is bugfixes, cool events, etc.\nHow do you set up? Use `{}sub <discord webhook url>`.\nIf you still do not understand, [please watch the tutorial video here.](https://vierofernando.is-inside.me/fEhT86EE.mp4)'.format(ctx.bot.command_prefix), color=ctx.guild.me.roles[::-1][0].color)
            return await ctx.send(embed=embed)
        elif 'reset' in ''.join(args).lower():
            ctx.bot.db.Dashboard.subscribe(None, ctx.guild.id, reset=True)
            return await ctx.send('{} | Subscription has been deleted.'.format(ctx.bot.util.success_emoji))
        url = args[0].replace('<', '').replace('>', '')
        try:
            web = discord.Webhook.from_url(
                url,
                adapter=discord.RequestsWebhookAdapter()
            )
        except: return await ctx.bot.util.send_error_message(ctx, "Invalid Webhook URL. Please send the one according to the tutorial.")
        ctx.bot.db.Dashboard.subscribe(url, ctx.guild.id)
        await ctx.message.add_reaction(ctx.bot.util.success_emoji)
        web.send(
            embed=discord.Embed(title=f'Congratulations, {str(ctx.author)}!', description='Your webhook is now set! ;)\nNow every development updates or username601 events will be set here.\n\nIf you change your mind, you can do `{}sub reset` to remove the webhook from the database.\n[Join our support server if you still have any questions.]({})'.format(ctx.bot.command_prefix, ctx.bot.util.server_invite), color=discord.Color.green()),
            username='Username601 News',
            avatar_url=ctx.bot.user.avatar_url
        )

    @command('commands,yardim,yardım')
    @cooldown(2)
    async def help(self, ctx, *args):
        if len(args) == 0:
            embeds = self._init_help
            for category in ctx.bot.cmds.categories:
                embed = discord.Embed(title=category, description="**Commands:**```"+(", ".join([command['name'] for command in ctx.bot.cmds.get_commands_from_category(category.lower())]))+"```")
                embed.set_footer(text=f"Type `{ctx.bot.command_prefix}help <command>` to view command in a detailed version.")
                embeds.append(embed)
            
            paginator = ctx.bot.EmbedPaginator(ctx, embeds, show_page_count=True, auto_set_color=True)
            return await paginator.execute()
        
        data = ctx.bot.cmds.query(' '.join(args).lower())
        if data is None: return await ctx.bot.util.send_error_message(ctx, "Your command/category name does not exist, sorry!")
        
        embed = ctx.bot.ChooseEmbed(ctx, data, key=(lambda x: "[`"+x["type"]+"`] `"+x["name"]+"`"))
        result = await embed.run()
        
        if result is None: return
        is_command = (result["type"] == "COMMAND")
        data = ctx.bot.cmds.get_command_info(result["name"].lower()) if is_command else ctx.bot.cmds.get_commands_from_category(result["name"].lower())
        
        desc = '**Command name: **{}\n**Function: **{}\n**Category: **{}'.format(
            data['name'], data['function'], data['category']
        ) if is_command else '**Commands count: **{}\n**Commands:**```{}```'.format(len(data), ', '.join([i['name'] for i in data]))
        embed = ctx.bot.Embed(ctx, title="Help for "+result["type"].lower()+": "+result["name"], desc=desc)
        if is_command:
            parameters = 'No parameters required.' if len(data['parameters'])==0 else '\n'.join([i for i in data['parameters']])
            apis = 'No APIs used.' if len(data['apis'])==0 else '\n'.join(map(lambda x: f"[{x}]({x})", data['apis']))
            embed.fields = {
                'Parameters': parameters,
                'APIs used': apis
            }
        return await embed.send()

    @command()
    @cooldown(2)
    async def vote(self, ctx):
        embed = discord.Embed(title='Support by Voting us at top.gg!', description='Sure thing, mate! [Vote us at top.gg by clicking me!](https://top.gg/bot/'+str(ctx.bot.user.id)+'/vote)', colour=ctx.guild.me.roles[::-1][0].color)
        await ctx.send(embed=embed)
    
    @command('sourcecode,source-code,git,repo')
    @cooldown(2)
    async def github(self, ctx):
        embed = discord.Embed(title="Click me to visit the Bot's github page.", colour=ctx.guild.me.roles[::-1][0].color, url=ctx.bot.util.github_repo)
        await ctx.send(embed=embed)
    
    @command('inviteme,invitelink,botinvite,invitebot,addtoserver,addbot')
    @cooldown(2)
    async def invite(self, ctx):
        embed = discord.Embed(
            title='Sure thing! Invite this bot to your server by clicking me.',
            url='https://discord.com/api/oauth2/authorize?client_id='+str(ctx.bot.user.id)+'&permissions=8&scope=bot',
            colour=ctx.guild.me.roles[::-1][0].color
        )
        await ctx.send(embed=embed)
    
    @command('report,suggest,bug,reportbug,bugreport')
    @cooldown(15)
    async def feedback(self, ctx, *args):
        if ((len(args)==0) or (len(''.join(args))>1000)): return await ctx.bot.util.send_error_message(ctx, "Invalid feedback length.")
        elif (('discord.gg/' in ' '.join(args)) or ('discord.com/invite/' in ' '.join(args))): return await ctx.bot.util.send_error_message(ctx, "Please do NOT send invites. This is NOT advertising.")
        else:
            wait = await ctx.send(ctx.bot.util.loading_emoji + ' | Please wait... Transmitting data to owner...')
            banned = ctx.bot.db.selfDB.is_banned(ctx.author.id)
            if not banned:
                try:
                    fb = ' '.join(args)
                    feedbackCh = ctx.bot.get_channel(ctx.bot.util.feedback_channel)
                    await feedbackCh.send(f'<@{ctx.bot.util.owner_id}>, User with ID: {ctx.author.id} sent a feedback: **"'+str(fb)+'"**')
                    embed = discord.Embed(title='Feedback Successful', description=ctx.bot.util.success_emoji + '** | Success!**\nThanks for the feedback!\n**We will DM you as the response. **If you are unsatisfied, [Join our support server and give us more details.]('+ctx.bot.util.server_invite+')', colour=ctx.guild.me.roles[::-1][0].color)
                    await wait.edit(content='', embed=embed)
                except:
                    return await ctx.bot.util.send_error_message(ctx, 'There was an error while sending your feedback. Sorry! :(')
            else:
                return await ctx.bot.util.send_error_message(ctx, f"You have been banned from using the Feedback command.\nReason: {str(banned)}")
                
    @command()
    @cooldown(2)
    async def ping(self, ctx):
        msgping = str(round((t.now().timestamp() - ctx.message.created_at.timestamp())*1000))
        wait = await ctx.send('pinging...')
        dbping, extras = ctx.bot.db.selfDB.ping(), ''
        wsping = str(round(ctx.bot.ws.latency*1000))
        embed = discord.Embed(title=f'Pong!', description=f'**Message latency: **{msgping} ms.\n**Client Latency:** {wsping} ms.\n**Database latency:** {dbping} ms.', colour=ctx.guild.me.roles[::-1][0].color)
        embed.set_thumbnail(url='https://i.pinimg.com/originals/21/02/a1/2102a19ea556e1d1c54f40a3eda0d775.gif')
        await wait.edit(content='', embed=embed)
    
    @command('botstats,meta')
    @cooldown(10)
    async def stats(self, ctx):
        async with ctx.channel.typing():
            data = ctx.bot.util.get_stats()
            
            embed = ctx.bot.Embed(
                ctx,
                title="Bot Stats",
                fields={
                    "Uptime": f"**Bot Uptime: **{data['bot_uptime']}\n**OS Uptime: **{data['os_uptime']}",
                    "Stats": f"**Server count: **{len(ctx.bot.guilds)}\n**Served users: **{len(ctx.bot.users)}\n**Cached custom emojis: **{len(ctx.bot.emojis)}",
                    "Memory": f"**Total: **{data['memory']['total']} MB\n**Used: **{data['memory']['used']} MB\n**Free: **{data['memory']['free']} MB\n**Available: **{data['memory']['available']} MB",
                    "Platform": f"**Machine: **{data['versions']['os']}\n**Python Build: **{data['versions']['python_build']}\n**Python Compiler: **{data['versions']['python_compiler']}\n**Discord.py version: **{data['versions']['discord_py']}"
                }
            )
            
            await embed.send()

def setup(client):
    client.add_cog(bothelp(client))
