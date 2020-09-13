import discord
from discord.ext import commands
import sys
from username601 import *
sys.path.append(cfg('MODULES_DIR'))
from database import *
from decorators import command, cooldown
# MAKE SURE OWNER HAS ACCESS TO "EVERYTHING"
import discordgames as Games
import requests
from canvas import *
import algorithm
from datetime import datetime as t
from subprocess import run, PIPE
from inspect import isawaitable
from asyncio import sleep
import os

totallyrealtoken = 'Ng5NDU4MjY5NTI2Mjk0MTc1.AkxrpC.MyB2BEHJLXuZ8h0wY0Qro6Pwi8'

class owner(commands.Cog):
    def __init__(self, client):
        self.client = client
        self.protected_files = [ # CONFIDENTIAL FILES
            os.environ['DISCORD_TOKEN'],
            os.environ['DBL_TOKEN'],
            os.environ['DB_LINK'],
            os.environ['USELESSAPI']
        ]
    
    @command('ann,announcement')
    @cooldown(2)
    async def announce(self, ctx, *args):
        if ctx.author.id != cfg('OWNER_ID', integer=True): return
        data, wr, sc = Dashboard.get_subscribers(), 0, 0
        for i in data:
            try:
                web = discord.Webhook.from_url(
                    i['url'], adapter=discord.RequestsWebhookAdapter()
                )
                web.send(
                    embed=discord.Embed(title=f'Username601 News: {str(t.now())[:-7]}', description=' '.join(list(args)).replace('\\n', '\n'), color=discord.Color.green()),
                    username='Username601 News',
                    avatar_url=self.client.user.avatar_url
                )
                sc += 1
            except:
                wr += 1
                Dashboard.subscribe(None, i['serverid'], reset=True)
            await sleep(1)
        await ctx.send(f'Done with {sc} success and {wr} fails')
    
    @command('pm')
    async def postmeme(self, ctx, *args):
        if ctx.author.id!=cfg('OWNER_ID', integer=True):
            return await ctx.message.add_reaction(emote(self.client, 'error'))
        url = ''.join(list(args))
        if url.startswith('<'): url = url[1:]
        if url.endswith('>'): url = url[:-1]
        data = requests.post('https://useless-api--vierofernando.repl.co/postprogrammermeme', headers={
            'superdupersecretkey': os.getenv('USELESSAPI'),
            'url': url
        })
        data = data.json()
        try:
            if data['success']: return await ctx.message.add_reaction(emote(self.client, 'success'))
        except Exception as e:
            await ctx.author.send(str(e))


    @command()
    async def cont(self, ctx):
        if ctx.author.id==cfg('OWNER_ID', integer=True):
            owners, c = [i.owner.id for i in self.client.guilds], 0
            for i in self.client.get_guild(cfg('SERVER_ID', integer=True)).members:
                if i.id in owners:
                    await self.client.get_guild(cfg('SERVER_ID', integer=True)).get_member(i.id).add_roles(self.client.get_guild(cfg('SERVER_ID', integer=True)).get_role(727667048645394492))
                    await sleep(1)
                    c += 1
            await ctx.send(f"found {str(c)} new conts!")

    @command()
    async def rp(self, ctx, *args):
        if ctx.author.id==cfg('OWNER_ID', integer=True):
            try:
                user_to_send = self.client.get_user(int(args[0]))
                em = discord.Embed(title="Hi, "+user_to_send.name+"! the bot owner sent a response for your feedback.", description=' '.join(list(args)[1:len(list(args))]), colour=get_embed_color(discord))
                await user_to_send.send(embed=em)
                await ctx.message.add_reaction('✅')
            except Exception as e:
                await ctx.send(emote(self.client, 'error') + f' | Error: `{e}`')
        else:
            await ctx.send('You are not the bot owner. Go get a life.')

    @command()
    async def fban(self, ctx, *args):
        if int(ctx.author.id)==cfg('OWNER_ID', integer=True):
            selfDB.feedback_ban(int(list(args)[0]), str(' '.join(list(args)[1:len(list(args))])))
            await ctx.message.add_reaction(emote(self.client, 'success'))
        else:
            await ctx.send(emote(self.client, 'error') +' | You are not the owner, nerd.')
    @command()
    async def funban(self, ctx, *args):
        if int(ctx.author.id)==cfg('OWNER_ID', integer=True):
            data = selfDB.feedback_unban(int(list(args)[0]))
            if data=='200': await ctx.message.add_reaction(emote(self.client, 'success'))
            else: await ctx.message.add_reaction(emote(self.client, 'error'))
        else:
            await ctx.send(emote(self.client, 'error') +' | Invalid person.')
    @command('ex,eval')
    async def evaluate(self, ctx, *args):
        unprefixed = ' '.join(list(args)).replace("`", "").replace('"', "'") if len(list(args))!=0 else 'undefined'
        if int(ctx.author.id)==cfg('OWNER_ID', integer=True):
            try:
                res = eval(unprefixed)
                for i in self.protected_files:
                    if str(i).lower() in str(res).lower(): res = totallyrealtoken
                    elif str(i).lower() in str(' '.join(list(args))).lower():
                        res = totallyrealtoken
                if isawaitable(res): await ctx.send(embed=discord.Embed(title='Evaluation Success', description='Input:```py\n'+unprefixed+'```**Output:**```py\n'+str(await res)+'```Return type:```py\n'+str(type(await res))+'```', color=discord.Colour.green()))
                else: await ctx.send(embed=discord.Embed(title='Evaluation Success', description='Input:```py\n'+unprefixed+'```**Output:**```py\n'+str(res)+'```Return type:```py\n'+str(type(res))+'```', color=discord.Color.green()))
            except Exception as e:
                if 'cannot reuse already awaited coroutine' in str(e): return
                await ctx.send(embed=discord.Embed(title='Evaluation Caught an Exception', description='Input:```py\n'+unprefixed+'```\nException:```py\n'+str(e)+'```', color=discord.Colour.red()), delete_after=5)
        else:
            fake_err = f"name '{unprefixed}' is not defined"
            return await ctx.send(embed=discord.Embed(title='Evaluation Caught an Exception', description='Input:```py\n'+unprefixed+'```\nException:```py\n'+str(fake_err)+'```', color=discord.Colour.red()))

    @command()
    async def token(self, ctx):
        await ctx.send(totallyrealtoken)

    @command('sh')
    async def bash(self, ctx, *args):
        unprefixed = ' '.join(list(args))
        if unprefixed == ' ': unprefixed = 'undefined'
        if int(ctx.author.id)==cfg('OWNER_ID', integer=True):
            try:
                if len(list(args))==0: raise OSError('you are gay')
                if len(unprefixed.split())==1: data = run([unprefixed], stdout=PIPE).stdout.decode('utf-8')
                else: data = run([unprefixed.split()[0], ' '.join(unprefixed.split()[1:len(unprefixed)])], stdout=PIPE).stdout.decode('utf-8')
                await ctx.send(embed=discord.Embed(title='Bash Terminal', description='Input:```sh\n'+str(unprefixed)+'```**Output:**```sh\n'+str(data)+'```', color=discord.Color.green()))
            except Exception as e:
                await ctx.send(embed=discord.Embed(title='Error on execution', description='Input:```sh\n'+str(unprefixed)+'```**Error:**```py\n'+str(e)+'```', color=discord.Color.red()))
        else:
            await ctx.send(embed=discord.Embed(title='Error on execution', description='Input:```sh\n'+str(unprefixed)+'```**Error:**```py\nDenied by username601.sh```', color=discord.Color.red()).set_footer(text='It is because it is owner only you dumbass'))

def setup(client):
    client.add_cog(owner(client))
