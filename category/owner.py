import discord
from discord.ext import commands
import sys
sys.path.append('/app/modules')
import username601 as myself
from username601 import *
from subprocess import run, PIPE
from inspect import isawaitable
import os

class owner(commands.Cog):
    def __init__(self, client):
        self.client = client
        self.protected_files = [ # CONFIDENTIAL FILES
            os.environ['DISCORD_TOKEN'],
            os.environ['DBL_TOKEN']
        ]
    
    @commands.command(pass_context=True)
    async def rp(self, ctx, *args):
        if ctx.message.author.id==Config.owner.id:
            try:
                user_to_send = self.client.get_user(int(args[0]))
                em = discord.Embed(title="Hi, "+user_to_send.name+"! the bot owner sent a response for your feedback.", description=str(ctx.message.content).split(' ')[2], colour=discord.Colour.from_rgb(201, 160, 112))
                em.set_footer(text="Feeling unsatisfied? Then join our support server! ("+str(Config.SupportServer.invite)+")")
                await user_to_send.send(embed=em)
                await ctx.message.add_reaction('✅')
            except Exception as e:
                await ctx.send(str(self.client.get_emoji(BotEmotes.error)) + f' | Error: `{e}`')
        else:
            await ctx.send('You are not the bot owner. Go get a life.')

    @commands.command(pass_context=True)
    async def fbban(self, ctx, *args):
        if ctx.message.channel.id==706459051034279956 and int(ctx.message.author.id)==Config.owner.id:
            await ctx.send('Banned user with ID of: ['+str(list(args)[0])+'] REASON:\"'+str(ctx.message.content)[int(len(list(args)[0])+2):]+'\"')
        else:
            await ctx.send(str(self.client.get_emoji(BotEmotes.error)) +' | Invalid channel/user.')
    @commands.command(pass_context=True, aliases=['ex'])
    async def eval(self, ctx, *args):
        unprefixed = ' '.join(list(args))
        if int(ctx.message.author.id)==Config.owner.id:
            try:
                res = eval(unprefixed.replace('"', "'"))
                for i in self.protected_files:
                    if str(i).lower() in str(res).lower(): res = 'YO MAMA'
                if isawaitable(res): await ctx.send(embed=discord.Embed(title='Evaluation Success', description='Input:```py\n'+unprefixed+'```**Output:**```py\n'+str(await res)+'```Return type:```py\n'+str(type(await res))+'```', color=discord.Colour.green()))
                else: await ctx.send(embed=discord.Embed(title='Evaluation Success', description='Input:```py\n'+unprefixed+'```**Output:**```py\n'+str(res)+'```Return type:```py\n'+str(type(res))+'```', color=discord.Color.green()))
            except Exception as e:
                await ctx.send(embed=discord.Embed(title='Evaluation Caught an Exception', description='Input:```py\n'+unprefixed+'```\nException:```py\n'+str(e)+'```', color=discord.Colour.red()))
        else:
            myself.report(ctx.message.author) # reports to the owner
            await ctx.send(str(self.client.get_emoji(BotEmotes.error))+' | Are you looking for the bots token? Well here you are: `ASKDPASKDOKASODKASODKOASKSDAODSKASD`')

    @commands.command(pass_context=True, aliases=['sh'])
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