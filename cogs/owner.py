import discord
import sys
import os
import gc
from random import randint
from pympler import muppy, summary
from decorators import *
from discord.ext import commands
from datetime import datetime as t
from subprocess import run, PIPE
from inspect import isawaitable, getsource
from asyncio import sleep
totallyrealtoken = 'Ng5NDU4MjY5NTI2Mjk0MTc1.AkxrpC.MyB2BEHJLXuZ8h0wY0Qro6Pwi8'

class owner(commands.Cog):
    def __init__(self, client):
        self.protected_files = [ # CONFIDENTIAL FILES
            os.environ['DISCORD_TOKEN'],
            os.environ['DBL_TOKEN'],
            os.environ['DB_LINK'],
            os.environ['USELESSAPI'],
            os.environ['ALEXFLIPNOTE_TOKEN']
        ]
        self.db = client.db

    @command()
    @owner_only()
    async def memstats(self, ctx):
        d = summary.print_(summary.summarize(muppy.get_objects()))
        return await ctx.send(f'Muppy result:```py\n{d}```\nGarbage Collector:\n```py\n{str(gc.get_stats())}```')

    @command()
    @owner_only()
    async def selfpurge(self, ctx):
        messages = list(filter(lambda x: x.author == ctx.me and x.guild == ctx.guild, ctx.bot.cached_messages))
        for message in messages[:10]:
            await message.delete()
            await sleep(2)
        del messages
    
    @command(['ann', 'announcement'])
    @cooldown(2)
    @owner_only()
    async def announce(self, ctx, *args):
        self.db.modify("config", self.db.types.APPEND, {"h": True}, {"changelog": "`["+str(t.now())[:-7]+" UTC]` "+" ".join(args)})
        await ctx.send("OK, added to db!")

    @command(['src'])
    @owner_only()
    async def source(self, ctx, *args):
        try:
            source = eval("getsource({})".format(' '.join(args)))
            return await ctx.send('```py\n'+str(source)[0:1900]+'```')
        except Exception as e:
            raise ctx.bot.util.error_message(str(e))

    @command()
    @owner_only()
    async def rp(self, ctx, *args):
        try:
            user_to_send = ctx.bot.get_user(int(args[0]))
            em = discord.Embed(title="Hi, "+user_to_send.name+"! the bot owner sent a response for your feedback.", description=' '.join(args[1:]), colour=ctx.me.color)
            await user_to_send.send(embed=em)
            await ctx.message.add_reaction('✅')
        except Exception as e:
            raise ctx.bot.util.error_message(f'Error: `{str(e)}`')

    @command()
    @owner_only()
    async def fban(self, ctx, *args):
        self.db.modify("config", self.db.types.APPEND, {"h": True}, {"bans": args[0]+"|"+" ".join(args[1:])})
        await ctx.message.add_reaction(ctx.bot.util.success_emoji)
    
    @command()
    @owner_only()
    async def funban(self, ctx, *args):
        data = self.db.get("config", {"h": True})["bans"]
        self.db.modify("config", self.db.types.CHANGE, {"h": True}, {"bans": [i for i in data if int(args[0]) != int(i.split("|")[0])]})
        await ctx.message.add_reaction(ctx.bot.util.success_emoji)
    
    @command(['ex', 'eval'])
    @cooldown(1)
    async def evaluate(self, ctx, *args): # this code can be messy because its owner and i dont care
        iwanttostealsometoken = False
        parser = ctx.bot.Parser(args)
        parser.parse()
        
        if ctx.author.id == ctx.bot.util.owner_id:
            if parser.has("simple"):
                parser.shift("simple")
                value = eval(" ".join(parser.other))
                return await ctx.send(str(value))
            
            try:
                time_then = t.now().timestamp()
                res = eval(" ".join(parser.other))
                time = (t.now().timestamp() - time_then) * 1000
                for i in self.protected_files:
                    if i.lower() in str(res).lower(): res = totallyrealtoken
                    elif i.lower() in ' '.join(args).lower():
                        res = totallyrealtoken
                if parser.has("silent"):
                    del parser, time, res
                    return
                if isawaitable(res): await ctx.send(embed=discord.Embed(title='Evaluation Success', description='Input:```py\n'+' '.join(parser.other)+'```**Output:**```py\n'+str(await res)[0:1990]+'```\n**Return type:** '+str(type(await res).__name__)+'\n**Execution time: **'+str(time)+' ms.', color=discord.Color.green()))
                else: await ctx.send(embed=discord.Embed(title='Evaluation Success', description='Input:```py\n'+' '.join(parser.other)+'```**Output:**```py\n'+str(res)[0:1990]+'```\n**Return type:** '+str(type(res).__name__)+'\n**Execution time: **'+str(time)+' ms.', color=discord.Color.green()))
            except Exception as e:
                if 'cannot reuse already awaited coroutine' in str(e): return
                await ctx.send(embed=discord.Embed(title='Evaluation Caught an Exception', description='Input:```py\n'+' '.join(parser.other)+'```\nException:```py\n'+str(e)+'```', color=discord.Color.red()), delete_after=5)
        else:
            try:
                time = randint(500, 1000) / 100
                if 'token' in ''.join(parser.other).lower(): iwanttostealsometoken = True
                elif 'secret' in ''.join(parser.other).lower(): iwanttostealsometoken = True
                if iwanttostealsometoken:
                    return await ctx.send(embed=discord.Embed(title='Evaluation Success', description='Input:```py\n'+' '.join(parser.other)[0:1990]+'```**Output:**```py\n'+totallyrealtoken+'```\n**Return type:** str\n**Execution time:** '+str(time)+' ms.', color=discord.Color.green()))
                query = ' '.join(parser.other)[0:1990].split('(')[0].split('[')[0].split('.')[0].split(' ')[0].split(';')[0]
                fake_err = f"name '{query}' is not defined"
                return await ctx.send(embed=discord.Embed(title='Evaluation Caught an Exception', description='Input:```py\n'+' '.join(parser.other)+'```\nException:```py\n'+str(fake_err)+'```', color=discord.Color.red()))
            except Exception as e:
                print(e)
                return await ctx.send('there was an error on evaluating that. please use \' instead of "')

    @command()
    async def token(self, ctx):
        await ctx.send(totallyrealtoken)

    @command(['sh'])
    async def bash(self, ctx, *args):
        command = " ".join(args)[0:100] if args else "echo hello world"
        if ctx.author.id == ctx.bot.util.owner_id:
            try:
                await ctx.message.add_reaction(ctx.bot.util.loading_emoji)
                data = await ctx.bot.util.execute(command)
                await ctx.send(embed=discord.Embed(title='Bash Terminal', description='Input:```sh\n'+command+'```**Output:**```sh\n'+str(data)[0:2000]+'```', color=discord.Color.green()))
            except Exception as e:
                await ctx.send(embed=discord.Embed(title='Error on execution', description='Input:```sh\n'+command+'```**Error:**```py\n'+str(e)+'```', color=discord.Color.red()))
        else:
            await ctx.send(embed=discord.Embed(title='Error on execution', description='Input:```sh\n'+command+'```**Error:**```py\nDenied by username601.sh```', color=discord.Color.red()).set_footer(text='It is because it is owner only you dumbass'))

def setup(client):
    client.add_cog(owner(client))