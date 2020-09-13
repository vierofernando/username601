import discord
from discord.ext import commands
import sys
import requests
from json import loads
from os import getcwd, name
dirname = getcwd()+'\\..' if name=='nt' else getcwd()+'/..'
sys.path.append(dirname)
del dirname
from username601 import *
sys.path.append(cfg('MODULES_DIR'))
from decorators import command, cooldown
from datetime import datetime as t
from database import selfDB, username601Stats, Dashboard

class bothelp(commands.Cog):
    def __init__(self, client):
        self.client = client
        self.db = Dashboard

    @command('supportserver,support-server,botserver,bot-server')
    @cooldown(1)
    async def support(self, ctx):
        return await ctx.send(cfg('SERVER_INVITE'))

    @command('subscribe,dev,development,devupdates,dev-updates,development-updates')
    @cooldown(5)
    async def sub(self, ctx, *args):
        if len(list(args))==0 or 'help' in ''.join(list(args)).lower():
            embed = discord.Embed(title='Get development updates and/or events in your server!', description='Want to get up-to-date development updates? either it is bugfixes, cool events, etc.\nHow do you set up? Use `{}sub <discord webhook url>`.\nIf you still do not understand, please watch the tutorial video below.'.format(prefix), color=get_embed_color(discord))
            embed.video(url='https://vierofernando.is-inside.me/fEhT86EE.mp4')
            return await ctx.send(embed=embed)
        elif 'reset' in ''.join(list(args)).lower():
            self.db.subscribe(None, ctx.guild.id, reset=True)
            return await ctx.send('{} | Subscription has been deleted.'.format(emote(self.client, 'success')))
        url = list(args)[0].replace('<', '').replace('>', '')
        try:
            web = discord.Webhook.from_url(
                url,
                adapter=discord.RequestsWebhookAdapter()
            )
        except: return await ctx.send("{} | Invalid url! Please follow the tutorial.".format(emote(self.client, 'error')))
        self.db.subscribe(url, ctx.guild.id)
        await ctx.message.add_reaction(emote(self.client, 'success'))
        web.send(
            embed=discord.Embed(title=f'Congratulations, {str(ctx.author)}!', description='Your webhook is now set! ;)\nNow every development updates will be set here.\n\nIf you change your mind, you can do `{}sub reset` to remove the webhook from the database.\n[Join our support server if you still have any questions.]({})'.format(prefix, cfg('SERVER_INVITE')), color=discord.Color.green()),
            username='Username601 Updates',
            avatar_url=self.client.user.avatar_url
        )

    @command('commands,yardim,yardım')
    @cooldown(1)
    async def help(self, ctx, *args):
        data = requests.get(cfg("WEBSITE_MAIN")+"/assets/json/commands.json").json()
        types, args = loads(open(cfg("JSON_DIR")+'/categories.json').read()), list(args)
        if len(args)<1:
            cate, web_commands_list = '', cfg('WEBSITE_COMMANDS')
            for i in range(0, len(types)):
                cate += f'**{str(i+1)}. **[{prefix}help {str(types[i])}]({web_commands_list}?category={i})\n'
            embed = discord.Embed(
                title='Username601\'s commands',
                description='[Join the support server]('+cfg('SERVER_INVITE')+') | [Vote us on top.gg](https://top.gg/bot/'+str(self.client.user.id)+'/vote)\n\n**[More information on our website here.]('+cfg('WEBSITE_COMMANDS')+')**\n**Command Categories:** \n'+str(cate),
                colour=get_embed_color(discord)
            )
            embed.set_footer(text=f'Type {prefix}help <command/category> for more details.')
            await ctx.send(embed=embed)
        else:
            source = None
            typ = ''
            category_name = None
            query = ' '.join(list(args))
            for i in range(0, len(types)):
                if query.lower()==types[i].lower():
                    source = data[i][types[i]]
                    typ = 'Category'
                    category_name = types[i]
                    break
            if source==None:
                for i in range(0, len(data)):
                    for j in range(0, len(data[i][types[i]])):
                        if query.lower()==data[i][types[i]][j]['n'].lower():
                            source = data[i][types[i]][j]
                            typ = 'Command'
                            break
                    if not typ=='':
                        break
            if source==None:
                await ctx.send('Oops... Your command doesn\'t seem to exist.')
            else:
                if typ=='Category':
                    cmds = []
                    for i in range(0, len(source)):
                        cmds.append(source[i]['n'])
                    cmds = ', '.join(cmds)
                    embed = discord.Embed(title='Category help for '+str(category_name)+':', description='**Commands:** \n```'+str(cmds)+'```', colour=get_embed_color(discord))
                if typ=='Command':
                    parameters = 'No parameters required.'
                    if len(source['p'])>0:
                        parameters = ''
                        for i in range(0, len(source['p'])):
                            parameters += '**'+source['p'][i]+'**\n'
                    embed = discord.Embed(title='Command help for '+str(source['n'])+':', description='**Function: **'+str(source['f'])+'\n**Parameters:** \n'+str(parameters), colour=get_embed_color(discord))
                await ctx.send(embed=embed)

    @command()
    @cooldown(1)
    async def vote(self, ctx):
        embed = discord.Embed(title='Support by Voting us at top.gg!', description='Sure thing, mate! [Vote us at top.gg by clicking me!](https://top.gg/bot/'+str(self.client.user.id)+'/vote)', colour=get_embed_color(discord))
        await ctx.send(embed=embed)
    
    @command()
    @cooldown(1)
    async def github(self, ctx):
        embed = discord.Embed(title="Click me to visit the Bot's github page.", colour=get_embed_color(discord), url=cfg('GITHUB_REPO'))
        await ctx.send(embed=embed)
    
    @command('inviteme,invitelink,botinvite,invitebot,addtoserver,addbot')
    @cooldown(1)
    async def invite(self, ctx):
        embed = discord.Embed(
            title='Sure thing! Invite this bot to your server by clicking me.',
            url='https://discord.com/api/oauth2/authorize?client_id='+str(self.client.user.id)+'&permissions=8&scope=bot',
            colour=get_embed_color(discord)
        )
        await ctx.send(embed=embed)
    
    @command('report,suggest,bug,reportbug,bugreport')
    @cooldown(15)
    async def feedback(self, ctx, *args):
        if len(list(args))==0:
            await ctx.send(emote(self.client, 'error')+' | Where\'s the feedback? :(')
        elif len(list(args))>1000:
            await ctx.send(emote(self.client, 'error')+' | That\'s too long! Please provide a simpler description.')
        elif 'discord.gg/' in ' '.join(list(args)):
            await ctx.send(emote(self.client, 'error')+' | Do NOT send discord invites through feedback! Use the advertising channel in our support server instead!')
        else:
            wait = await ctx.send(emote(self.client, 'loading') + ' | Please wait... Transmitting data to owner...')
            banned = selfDB.is_banned(ctx.author.id)
            if not banned:
                try:
                    fb = ' '.join(list(args))
                    feedbackCh = self.client.get_channel(cfg('FEEDBACK_CHANNEL', integer=True))
                    await feedbackCh.send('<@'+cfg('OWNER_ID')+'>, User with ID: '+str(ctx.author.id)+' sent a feedback: **"'+str(fb)+'"**')
                    embed = discord.Embed(title='Feedback Successful', description=emote(self.client, 'success') + '** | Success!**\nThanks for the feedback!\n**We will DM you as the response. **If you are unsatisfied, [Join our support server and give us more details.]('+cfg('SERVER_INVITE')+')',colour=get_embed_color(discord))
                    await wait.edit(content='', embed=embed)
                except:
                    await wait.edit(content=emote(self.client, 'error') + ' | Error: There was an error while sending your feedback. Sorry! :(')
            else:
                await wait.edit(content='', embed=discord.Embed(
                    title="You have been banned from using the Feedback command.",
                    description="**Reason: **```"+str(banned)+"```",
                    color=discord.Colour.red()
                ))
    @command()
    @cooldown(2)
    async def ping(self, ctx):
        msgping = str(round((t.now().timestamp() - ctx.message.created_at.timestamp())*1000))
        wait = await ctx.send('pinging...')
        dbping, extras = selfDB.ping(), ''
        if cfg('HOST_URL').lower()!='none':
            webping = ping()
            extras = f'\n**Hosting latency: **{webping} ms.'
        wsping = str(round(self.client.ws.latency*1000))
        embed = discord.Embed(title=f'Pong!', description=f'**Message latency: **{msgping} ms.\n**Client Latency:** {wsping} ms.\n**Database latency:** {dbping} ms.{extras}', colour=get_embed_color(discord))
        embed.set_thumbnail(url='https://i.pinimg.com/originals/21/02/a1/2102a19ea556e1d1c54f40a3eda0d775.gif')
        await wait.edit(content='', embed=embed)
    
    @command('botstats,meta')
    @cooldown(10)
    async def stats(self, ctx):
        up, cmds, commandLength = selfDB.get_uptime(), username601Stats.retrieveData(), getCommandLength()
        #imageurl = urlify(uptimerobot())
        bot_uptime = up.split('|')[0].split(':')[0]+' Hours, '+up.split('|')[0].split(':')[1]+' minutes, '+up.split('|')[0].split(':')[2]+' seconds.'
        embed = discord.Embed(description='This bot is in {} servers.\nWith {} users\nBot uptime: {}\nOS uptime: {}\nLast downtime: {} UTC\nCommands run in the past {}: {}\nTotal commands: {}'.format(len(self.client.guilds), len(self.client.users), bot_uptime, str(terminal('uptime -p'))[3:], up.split('|')[1], time_encode(round(t.now().timestamp()) - round(cmds['lastreset'])), str(cmds['count']), str(commandLength)), color=get_embed_color(discord))
        #embed.set_image(url='https://quickchart.io/chart?c='+imageurl)
        await ctx.send(embed=embed)

    @command('botinfo,aboutbot,bot')
    @cooldown(2)
    async def about(self, ctx):
        if str(self.client.get_guild(cfg('SERVER_ID', integer=True)).get_member(cfg('OWNER_ID', integer=True)).status)=='offline': devstatus = 'Offline'
        else: devstatus = 'Online'
        embed = discord.Embed(title = 'About '+str(ctx.guild.me.display_name), colour = get_embed_color(discord))
        embed.add_field(name='Bot general Info', value='**Bot name: ** Username601\n**Library: **Discord.py\n**Default prefix: **'+prefix)
        embed.add_field(name='Programmer info', value='**Programmed by: **'+str(self.client.get_user(cfg('OWNER_ID', integer=True)))+'\n(Indie developed)\n**Current Discord Status:** '+devstatus)
        embed.add_field(name='Version Info', value='**Bot version: ** '+cfg('VERSION')+'\n**Changelog: **'+cfg('CHANGELOG'))#+'\n'+str(osinfo))
        embed.add_field(name='Links', value='[Invite this bot to your server!]('+cfg('BOT_INVITE')+')\n[The support server!]('+cfg('SERVER_INVITE')+')\n[Vote us on top.gg](https://top.gg/bot/'+str(self.client.user.id)+'/vote)\n[Official Website]('+cfg('WEBSITE_MAIN')+')')
        embed.set_thumbnail(url=cfg('WEBSITE_MAIN')+'/assets/pics/pfp.png')
        embed.set_footer(text='© '+str(self.client.get_user(cfg('OWNER_ID', integer=True)))+' Programming, 2020. All rights reserved.')
        await ctx.send(embed=embed)

def setup(client):
    client.add_cog(bothelp(client))
