import discord
from discord.ext import commands
import sys
sys.path.append('/home/runner/hosting601/modules')
import username601 as myself
from username601 import *
from database import *
from decorators import command, cooldown
# MAKE SURE OWNER HAS ACCESS TO "EVERYTHING"
import discordgames as Games
from canvas import *
import algorithm
from subprocess import run, PIPE
from inspect import isawaitable
from asyncio import sleep
import os

totallyrealtoken = 'asdoaskdokasdokasodkasodkasodkasdkasodkaosdkoaskdoadk'

class owner(commands.Cog):
    def __init__(self, client):
        self.client = client
        self.protected_files = [ # CONFIDENTIAL FILES
            os.getenv('DISCORD_TOKEN'),
            os.getenv('DBL_TOKEN'),
            os.getenv('DB_LINK'),
            os.getenv('KSOFT_TOKEN'),
            os.getenv('UPTIMEROBOT_TOKEN'),
            os.getenv('BOTSFORDISCORD_TOKEN'),
            os.getenv('DISCORDBOTLIST_TOKEN')
        ]
        self.canvas = Painter(
            r'/home/runner/hosting601/assets/pics/',
            r'/home/runner/hosting601/assets/fonts/'
        )
        self.gif = GifGenerator(
            r'/home/runner/hosting601/assets/pics/',
            r'/home/runner/hosting601/assets/fonts/'
        )

    @command()
    async def setbal(self, ctx, *args):
        if ctx.message.author.id==Config.owner.id:
            await ctx.message.add_reaction(self.client.get_emoji(BotEmotes.loading))
            resp = Economy.setbal(int(list(args)[0]), int(list(args)[1]))
            await ctx.send(resp)
        else:
            await ctx.send('no u.')
    
    @command()
    async def cont(self, ctx):
        if ctx.message.author.id==Config.owner.id:
            owners, c = [i.owner.id for i in self.client.guilds], 0
            for i in self.client.get_guild(Config.SupportServer.id).members:
                if i.id in owners:
                    await self.client.get_guild(Config.SupportServer.id).get_member(i.id).add_roles(self.client.get_guild(Config.SupportServer.id).get_role(727667048645394492))
                    await sleep(1)
                    c += 1
            await ctx.send(f"found {str(c)} new conts!")

    @command()
    async def rp(self, ctx, *args):
        if ctx.message.author.id==Config.owner.id:
            try:
                user_to_send = self.client.get_user(int(args[0]))
                em = discord.Embed(title="Hi, "+user_to_send.name+"! the bot owner sent a response for your feedback.", description=' '.join(list(args)[1:len(list(args))]), colour=discord.Colour.from_rgb(201, 160, 112))
                await user_to_send.send(embed=em)
                await ctx.message.add_reaction('✅')
            except Exception as e:
                await ctx.send(str(self.client.get_emoji(BotEmotes.error)) + f' | Error: `{e}`')
        else:
            await ctx.send('You are not the bot owner. Go get a life.')

    @command()
    async def fban(self, ctx, *args):
        if int(ctx.message.author.id)==Config.owner.id:
            selfDB.feedback_ban(int(list(args)[0]), str(' '.join(list(args)[1:len(list(args))])))
            await ctx.message.add_reaction(self.client.get_emoji(BotEmotes.success))
        else:
            await ctx.send(str(self.client.get_emoji(BotEmotes.error)) +' | You are not the owner, nerd.')
    @command()
    async def funban(self, ctx, *args):
        if int(ctx.message.author.id)==Config.owner.id:
            data = selfDB.feedback_unban(int(list(args)[0]))
            if data=='200': await ctx.message.add_reaction(self.client.get_emoji(BotEmotes.success))
            else: await ctx.message.add_reaction(self.client.get_emoji(BotEmotes.error))
        else:
            await ctx.send(str(self.client.get_emoji(BotEmotes.error)) +' | Invalid person.')
    @command('ex,eval')
    async def evaluate(self, ctx, *args):
        unprefixed = ' '.join(list(args))
        if int(ctx.message.author.id)==Config.owner.id:
            try:
                res = eval(unprefixed.replace('"', "'"))
                for i in self.protected_files:
                    if str(i).lower() in str(res).lower(): res = 'YO MAMA'
                    elif str(i).lower() in str(' '.join(list(args))).lower():
                        res = 'YO MAMA'
                if isawaitable(res): await ctx.send(embed=discord.Embed(title='Evaluation Success', description='Input:```py\n'+unprefixed+'```**Output:**```py\n'+str(await res)+'```Return type:```py\n'+str(type(await res))+'```', color=discord.Colour.green()))
                else: await ctx.send(embed=discord.Embed(title='Evaluation Success', description='Input:```py\n'+unprefixed+'```**Output:**```py\n'+str(res)+'```Return type:```py\n'+str(type(res))+'```', color=discord.Color.green()))
            except Exception as e:
                if 'cannot reuse already awaited coroutine' in str(e): return
                await ctx.send(embed=discord.Embed(title='Evaluation Caught an Exception', description='Input:```py\n'+unprefixed+'```\nException:```py\n'+str(e)+'```', color=discord.Colour.red()), delete_after=5)
        else:
            myself.report(ctx.message.author) # reports to the owner
            await ctx.send(str(self.client.get_emoji(BotEmotes.error))+' | Are you looking for the bots token? Well here you are: `'+totallyrealtoken+'`')

    @command()
    async def token(self, ctx):
        await ctx.send(totallyrealtoken)

    @command('sh')
    async def bash(self, ctx, *args):
        unprefixed = ' '.join(list(args))
        if int(ctx.message.author.id)==Config.owner.id:
            try:
                if len(list(args))==0: raise OSError('you are gay')
                if len(unprefixed.split())==1: data = run([unprefixed], stdout=PIPE).stdout.decode('utf-8')
                else: data = run([unprefixed.split()[0], ' '.join(unprefixed.split()[1:len(unprefixed)])], stdout=PIPE).stdout.decode('utf-8')
                await ctx.send(embed=discord.Embed(title='Bash Terminal', description='Input:```sh\n'+str(unprefixed)+'```**Output:**```sh\n'+str(data)+'```', color=discord.Color.green()))
            except Exception as e:
                await ctx.send(embed=discord.Embed(title='Error on execution', description='Input:```sh\n'+str(unprefixed)+'```**Error:**```py\n'+str(e)+'```', color=discord.Color.red()))
        else:
            await ctx.send(embed=discord.Embed(title='Error on execution', description='Input:```sh\n'+str(unprefixed)+'```**Error:**```py\nDenied by username601.sh```', color=discord.Color.red()))

def setup(client):
    client.add_cog(owner(client))
