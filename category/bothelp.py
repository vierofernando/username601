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
        self.client = client

    @command('supportserver,support-server,botserver,bot-server')
    @cooldown(1)
    async def support(self, ctx):
        return await ctx.send(self.client.utils.cfg('SERVER_INVITE'))

    @command('subscribe,dev,development,devupdates,dev-updates,development-updates')
    @cooldown(5)
    async def sub(self, ctx, *args):
        if len(args)==0 or 'help' in ''.join(args).lower():
            embed = discord.Embed(title='Get development updates and/or events in your server!', description='Want to get up-to-date development updates? either it is bugfixes, cool events, etc.\nHow do you set up? Use `{}sub <discord webhook url>`.\nIf you still do not understand, [please watch the tutorial video here.](https://vierofernando.is-inside.me/fEhT86EE.mp4)'.format(self.client.command_prefix), color=self.client.utils.get_embed_color())
            return await ctx.send(embed=embed)
        elif 'reset' in ''.join(args).lower():
            self.client.db.Dashboard.subscribe(None, ctx.guild.id, reset=True)
            return await ctx.send('{} | Subscription has been deleted.'.format(self.client.success_emoji))
        url = list(args)[0].replace('<', '').replace('>', '')
        try:
            web = discord.Webhook.from_url(
                url,
                adapter=discord.RequestsWebhookAdapter()
            )
        except: raise self.client.utils.SendErrorMessage("Invalid Webhook URL. Please send the one according to the tutorial.")
        self.client.db.Dashboard.subscribe(url, ctx.guild.id)
        await ctx.message.add_reaction(self.client.success_emoji)
        web.send(
            embed=discord.Embed(title=f'Congratulations, {str(ctx.author)}!', description='Your webhook is now set! ;)\nNow every development updates or username601 events will be set here.\n\nIf you change your mind, you can do `{}sub reset` to remove the webhook from the database.\n[Join our support server if you still have any questions.]({})'.format(self.client.command_prefix, self.client.utils.cfg('SERVER_INVITE')), color=discord.Color.green()),
            username='Username601 News',
            avatar_url=self.client.user.avatar_url
        )

    @command('commands,yardim,yardım')
    @cooldown(1)
    async def help(self, ctx, *args):
        args = list(args)
        if len(args) == 0:
            cate = '\n'.join(['[{}. {}help {}]({}?category={})'.format(i+1, self.client.command_prefix, self.client.cmds.categories[i], self.client.utils.cfg('WEBSITE_COMMANDS'), i) for i in range(len(self.client.cmds.categories))])
            embed = discord.Embed(
                title='Username601\'s commands',
                description='[Invite the bot]('+self.client.utils.cfg('BOT_INVITE')+') | [Vote us on top.gg](https://top.gg/bot/'+str(self.client.user.id)+'/vote)\n\n**[More information on our website here.]('+self.client.utils.cfg('WEBSITE_COMMANDS')+')**\n**Command Categories:** \n'+str(cate),
                colour=self.client.utils.get_embed_color()
            )
            embed.set_footer(text=f'Type {self.client.command_prefix}help <command/category> for more details.')
            await ctx.send(embed=embed)
        else:
            data = self.client.cmds.get_commands_auto(' '.join(args).lower())
            if data==None: raise self.client.utils.SendErrorMessage("Your command/category name does not exist, sorry!")
            datatype = 'Category' if isinstance(data, list) else 'Command'
            desc = '**Command name: **{}\n**Function: **{}\n**Category: **{}'.format(
                data['name'], data['function'], data['category']
            ) if datatype=='Command' else '**Commands count: **{}\n**Commands:**```{}```'.format(len(data), ', '.join([i['name'] for i in data]))
            embed = discord.Embed(title='{} help for query: "{}"'.format(datatype, ' '.join(args)), description=desc, color=self.client.utils.get_embed_color())
            if datatype=='Command':
                parameters = 'No parameters required.' if len(data['parameters'])==0 else '\n'.join([i for i in data['parameters']])
                apis = 'No APIs used.' if len(data['apis'])==0 else '\n'.join([f'[{i}]({i})' for i in data['apis']])
                embed.add_field(name='Parameters', value=parameters)
                embed.add_field(name='APIs used', value=apis)
            await ctx.send(embed=embed)

    @command()
    @cooldown(1)
    async def vote(self, ctx):
        embed = discord.Embed(title='Support by Voting us at top.gg!', description='Sure thing, mate! [Vote us at top.gg by clicking me!](https://top.gg/bot/'+str(self.client.user.id)+'/vote)', colour=self.client.utils.get_embed_color())
        await ctx.send(embed=embed)
    
    @command('sourcecode,source-code,git,repo')
    @cooldown(1)
    async def github(self, ctx):
        embed = discord.Embed(title="Click me to visit the Bot's github page.", colour=self.client.utils.get_embed_color(), url=self.client.utils.cfg('GITHUB_REPO'))
        await ctx.send(embed=embed)
    
    @command('inviteme,invitelink,botinvite,invitebot,addtoserver,addbot')
    @cooldown(1)
    async def invite(self, ctx):
        embed = discord.Embed(
            title='Sure thing! Invite this bot to your server by clicking me.',
            url='https://discord.com/api/oauth2/authorize?client_id='+str(self.client.user.id)+'&permissions=8&scope=bot',
            colour=self.client.utils.get_embed_color()
        )
        await ctx.send(embed=embed)
    
    @command('report,suggest,bug,reportbug,bugreport')
    @cooldown(15)
    async def feedback(self, ctx, *args):
        if ((len(args)==0) or (len(''.join(args))>1000)): raise self.client.utils.SendErrorMessage("Invalid feedback length.")
        elif (('discord.gg/' in ' '.join(args)) or ('discord.com/invite/' in ' '.join(args))): raise self.client.utils.SendErrorMessage("Please do NOT send invites. This is NOT advertising.")
        else:
            wait = await ctx.send(self.client.loading_emoji + ' | Please wait... Transmitting data to owner...')
            banned = self.client.db.selfDB.is_banned(ctx.author.id)
            if not banned:
                try:
                    fb = ' '.join(args)
                    feedbackCh = self.client.get_channel(self.client.utils.cfg('FEEDBACK_CHANNEL', integer=True))
                    await feedbackCh.send('<@'+self.client.utils.cfg('OWNER_ID')+'>, User with ID: '+str(ctx.author.id)+' sent a feedback: **"'+str(fb)+'"**')
                    embed = discord.Embed(title='Feedback Successful', description=self.client.success_emoji + '** | Success!**\nThanks for the feedback!\n**We will DM you as the response. **If you are unsatisfied, [Join our support server and give us more details.]('+self.client.utils.cfg('SERVER_INVITE')+')',colour=self.client.utils.get_embed_color())
                    await wait.edit(content='', embed=embed)
                except:
                    raise self.client.utils.SendErrorMessage('There was an error while sending your feedback. Sorry! :(')
            else:
                raise self.client.utils.SendErrorMessage("You have been banned from using the Feedback command.\nReason: {str(banned)}")
                
    @command()
    @cooldown(2)
    async def ping(self, ctx):
        msgping = str(round((t.now().timestamp() - ctx.message.created_at.timestamp())*1000))
        wait = await ctx.send('pinging...')
        dbping, extras = self.client.db.selfDB.ping(), ''
        if self.client.utils.cfg('HOST_URL').lower()!='none':
            webping = self.client.utils.ping()
            extras = f'\n**Hosting latency: **{webping} ms.'
        wsping = str(round(self.client.ws.latency*1000))
        embed = discord.Embed(title=f'Pong!', description=f'**Message latency: **{msgping} ms.\n**Client Latency:** {wsping} ms.\n**Database latency:** {dbping} ms.{extras}', colour=self.client.utils.get_embed_color())
        embed.set_thumbnail(url='https://i.pinimg.com/originals/21/02/a1/2102a19ea556e1d1c54f40a3eda0d775.gif')
        await wait.edit(content='', embed=embed)
    
    @command('botstats,meta')
    @cooldown(10)
    async def stats(self, ctx):
        bot_uptime = self.client.utils.time_encode(round(t.now().timestamp() - self.client.last_downtime))
        embed = discord.Embed(description='This bot is serving **{} servers** each with **{} users.**\nBot uptime: {}\nOS uptime: {}\nLast downtime: {} UTC\nCommands run in the past {}: {}\nTotal commands: {}'.format(
            len(self.client.guilds),
            len(self.client.users),
            bot_uptime,
            self.client.utils.terminal('uptime -p')[3:],
            t.fromtimestamp(self.client.last_downtime),
            bot_uptime,
            self.client.command_uses,
            self.client.cmds.length
        ), color=self.client.utils.get_embed_color())
        await ctx.send(embed=embed)

    @command('botinfo,aboutbot,bot,info,information')
    @cooldown(2)
    async def about(self, ctx):
        if str(self.client.get_guild(self.client.utils.cfg('SERVER_ID', integer=True)).get_member(self.client.utils.cfg('OWNER_ID', integer=True)).status)=='offline': devstatus = 'Offline'
        else: devstatus = 'Online'
        embed = discord.Embed(title = 'About '+str(ctx.guild.me.display_name), colour = self.client.utils.get_embed_color())
        embed.add_field(name='Bot general Info', value='**Bot name: ** Username601\n**Library: **Discord.py\n**Default self.client.command_prefix: **'+self.client.command_prefix)
        embed.add_field(name='Programmer info', value='**Programmed by: **'+str(self.client.get_user(self.client.utils.cfg('OWNER_ID', integer=True)))+'\n(Indie developed)\n**Current Discord Status:** '+devstatus)
        embed.add_field(name='Version Info', value='**Bot version: ** '+self.client.utils.cfg('VERSION')+'\n**Changelog: **'+self.client.utils.cfg('CHANGELOG'))#+'\n'+str(osinfo))
        embed.add_field(name='Links', value='[Invite this bot to your server!]('+self.client.utils.cfg('BOT_INVITE')+')\n[The support server!]('+self.client.utils.cfg('SERVER_INVITE')+')\n[Vote us on top.gg](https://top.gg/bot/'+str(self.client.user.id)+'/vote)\n[Official Website]('+self.client.utils.cfg('WEBSITE_MAIN')+')')
        embed.set_thumbnail(url=self.client.utils.cfg('WEBSITE_MAIN')+'/assets/pics/pfp.png')
        embed.set_footer(text='© '+str(self.client.get_user(self.client.utils.cfg('OWNER_ID', integer=True)))+' Programming, 2020. All rights reserved.')
        await ctx.send(embed=embed)

def setup(client):
    client.add_cog(bothelp(client))