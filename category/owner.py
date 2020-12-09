import discord
import sys
import os
import random
from category.decorators import command, cooldown
from discord.ext import commands
from datetime import datetime as t
from subprocess import run, PIPE
from inspect import isawaitable, getsource
from asyncio import sleep
#from twemoji_parser import TwemojiParser
#import PIL as p

totallyrealtoken = 'Ng5NDU4MjY5NTI2Mjk0MTc1.AkxrpC.MyB2BEHJLXuZ8h0wY0Qro6Pwi8'

class owner(commands.Cog):
    def __init__(self):
        self.protected_files = [ # CONFIDENTIAL FILES
            os.environ['DISCORD_TOKEN'],
            os.environ['DBL_TOKEN'],
            os.environ['DB_LINK'],
            os.environ['USELESSAPI'],
            os.environ['ALEXFLIPNOTE_TOKEN']
        ]

    @command()
    @cooldown(1)
    async def test(self, ctx, *args):
        if ctx.author.id not in [661200758510977084, 766952708602331137]: return
        return
        
        #a = p.Image.new("RGB", (1000, 500), color=(255, 255, 255))
        #_p = TwemojiParser(a, parse_discord_emoji=True)
        #f = p.ImageFont.truetype("/app/assets/fonts/NotoSansDisplay-Bold.otf", 40)
        #await _p.draw_text((5, 5), " ".join(args), font=f, fill=(0, 0, 0))
        #await _p.close()
        #buff = ctx.bot.canvas.buffer(a)
        #await ctx.send(file=discord.File(buff, "test.png"))
        #del buff

    @command()
    @cooldown(2)
    async def leave(self, ctx, *args):
        if ctx.author.id not in [661200758510977084, 766952708602331137]: return
        server_id = int(list(args)[1])
        await ctx.bot.get_guild(server_id).leave()
        return await ctx.send('ok')
    
    @command('ann,announcement')
    @cooldown(2)
    async def announce(self, ctx, *args):
        if ctx.author.id not in [661200758510977084, 766952708602331137]: return
        await ctx.message.add_reaction(ctx.bot.util.loading_emoji)
        data, wr, sc = ctx.bot.db.Dashboard.get_subscribers(), 0, 0
        for i in data:
            try:
                web = discord.Webhook.from_url(
                    i['url'], adapter=discord.RequestsWebhookAdapter()
                )
                web.send(
                    embed=discord.Embed(title=f'Username601 News: {str(t.now())[:-7]}', description=' '.join(args).replace('\\n', '\n'), color=discord.Color.green()),
                    username='Username601 News',
                    avatar_url=ctx.bot.user.avatar_url
                )
                sc += 1
            except:
                wr += 1
                ctx.bot.db.Dashboard.subscribe(None, i['serverid'], reset=True)
            await sleep(1)
        await ctx.send(f'Done with {sc} success and {wr} fails')
    
    @command('src')
    async def source(self, ctx, *args):
        try:
            assert ctx.author.id == ctx.bot.util.owner_id, 'Source code not available'
            source = eval("getsource({})".format(' '.join(args)))
            return await ctx.send('```py\n'+str(source)[0:1900]+'```')
        except Exception as e:
            raise ctx.bot.util.BasicCommandException(str(e))
    
    @command('pm')
    async def postmeme(self, ctx, *args):
        if ctx.author.id!=ctx.bot.util.owner_id:
            return await ctx.message.add_reaction(ctx.bot.util.error_emoji)
        url = ''.join(args)
        if url.startswith('<'): url = url[1:]
        if url.endswith('>'): url = url[:-1]
        if "/https/" in url:
            url = "https://" + url.split("/https/")[1].split("?")[0]
        data = await ctx.bot.util.useless_client.post('https://useless-api--vierofernando.repl.co/postprogrammermeme?url=' + url, headers={
            'superdupersecretkey': os.environ['USELESSAPI']
        })
        data = await data.json()
        try:
            if data['success']: return await ctx.message.add_reaction(ctx.bot.util.success_emoji)
        except Exception as e:
            await ctx.author.send(str(e))

    @command()
    async def rp(self, ctx, *args):
        if ctx.author.id==ctx.bot.util.owner_id:
            try:
                user_to_send = ctx.bot.get_user(int(args[0]))
                em = discord.Embed(title="Hi, "+user_to_send.name+"! the bot owner sent a response for your feedback.", description=' '.join(args[1:]), colour=ctx.guild.me.roles[::-1][0].color)
                await user_to_send.send(embed=em)
                await ctx.message.add_reaction('✅')
            except Exception as e:
                raise ctx.bot.util.BasicCommandException(f'Error: `{str(e)}`')
        else:
            await ctx.send('You are not the bot owner. Go get a life.')

    @command()
    async def fban(self, ctx, *args):
        if ctx.author.id==ctx.bot.util.owner_id:
            ctx.bot.db.selfDB.feedback_ban(int(args[0]), str(' '.join(list(args)[1:])))
            await ctx.message.add_reaction(ctx.bot.util.success_emoji)
        else:
            raise ctx.bot.util.BasicCommandException('You are not the owner, nerd.')
    @command()
    async def funban(self, ctx, *args):
        if ctx.author.id==ctx.bot.util.owner_id:
            data = ctx.bot.db.selfDB.feedback_unban(int(args[0]))
            if data=='200': await ctx.message.add_reaction(ctx.bot.util.success_emoji)
            else: await ctx.message.add_reaction(ctx.bot.util.error_emoji)
        else:
            raise ctx.bot.util.BasicCommandException('Invalid person.')
    @command('ex,eval')
    async def evaluate(self, ctx, *args):
        iwanttostealsometoken = False
        unprefixed = ' '.join(args).replace("`", "").replace('"', "'").replace("--silent", "") if len(args)!=0 else 'undefined'
        if ctx.author.id in [661200758510977084, 766952708602331137]:
            try:
                is_silent = "--silent" in args
                time_then = t.now().timestamp()
                res = eval(unprefixed)
                time = (t.now().timestamp() - time_then) * 1000
                for i in self.protected_files:
                    if str(i).lower() in str(res).lower(): res = totallyrealtoken
                    elif str(i).lower() in str(' '.join(args)).lower():
                        res = totallyrealtoken
                if is_silent: return
                if isawaitable(res): await ctx.send(embed=discord.Embed(title='Evaluation Success', description='Input:```py\n'+unprefixed+'```**Output:**```py\n'+str(await res)[0:1990]+'```\n**Return type:** '+str(type(await res).__name__)+'\n**Execution time: **'+str(time)+' ms.', color=discord.Colour.green()))
                else: await ctx.send(embed=discord.Embed(title='Evaluation Success', description='Input:```py\n'+unprefixed+'```**Output:**```py\n'+str(res)[0:1990]+'```\n**Return type:** '+str(type(res).__name__)+'\n**Execution time: **'+str(time)+' ms.', color=discord.Color.green()))
            except Exception as e:
                if 'cannot reuse already awaited coroutine' in str(e): return
                await ctx.send(embed=discord.Embed(title='Evaluation Caught an Exception', description='Input:```py\n'+unprefixed+'```\nException:```py\n'+str(e)+'```', color=discord.Colour.red()), delete_after=5)
        else:
            try:
                time = random.randint(500, 1000) / 100
                if 'token' in unprefixed.lower(): iwanttostealsometoken = True
                elif 'secret' in unprefixed.lower(): iwanttostealsometoken = True
                if iwanttostealsometoken:
                    return await ctx.send(embed=discord.Embed(title='Evaluation Success', description='Input:```py\n'+unprefixed[0:1990]+'```**Output:**```py\n'+totallyrealtoken+'```\n**Return type:** str\n**Execution time:** '+str(time)+' ms.', color=discord.Color.green()))
                query = unprefixed[0:1990].split('(')[0].split('[')[0].split('.')[0]
                fake_err = f"name '{query}' is not defined"
                return await ctx.send(embed=discord.Embed(title='Evaluation Caught an Exception', description='Input:```py\n'+unprefixed+'```\nException:```py\n'+str(fake_err)+'```', color=discord.Colour.red()))
            except Exception as e:
                print(e)
                return await ctx.send('there was an error on evaluating that. please use \' instead of "')

    @command()
    async def token(self, ctx):
        await ctx.send(totallyrealtoken)

    @command('sh')
    async def bash(self, ctx, *args):
        unprefixed = ' '.join(args)
        if unprefixed == '': unprefixed = 'echo hello world'
        if ctx.author.id==ctx.bot.util.owner_id:
            try:
                if len(args) == 0: raise OSError('you are gay')
                
                await ctx.message.add_reaction(ctx.bot.util.loading_emoji)
                data = await ctx.bot.util.execute(" ".join(args))
                await ctx.send(embed=discord.Embed(title='Bash Terminal', description='Input:```sh\n'+str(unprefixed)+'```**Output:**```sh\n'+str(data)[0:2000]+'```', color=discord.Color.green()))
            except Exception as e:
                await ctx.send(embed=discord.Embed(title='Error on execution', description='Input:```sh\n'+str(unprefixed)+'```**Error:**```py\n'+str(e)+'```', color=discord.Color.red()))
        else:
            await ctx.send(embed=discord.Embed(title='Error on execution', description='Input:```sh\n'+str(unprefixed)+'```**Error:**```py\nDenied by username601.sh```', color=discord.Color.red()).set_footer(text='It is because it is owner only you dumbass'))

def setup(client):
    client.add_cog(owner())
