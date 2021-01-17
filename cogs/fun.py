import discord
from random import randint, choice
from os import environ
from discord.ext import commands
from decorators import *
from aiohttp import ClientSession
from io import BytesIO
from json import dumps

class fun(commands.Cog):
    def __init__(self):
        self.connection = ClientSession(headers={'Authorization': 'Bot '+environ['DISCORD_TOKEN'], 'Content-Type': 'application/json'})      

    @command(['xckd', 'xcdk', 'xkdc'])
    @cooldown(5)
    async def xkcd(self, ctx, *args):
        await ctx.trigger_typing()
        
        parser = ctx.bot.Parser(args)
        parser.parse()
        
        comic = await ctx.bot.util.request("https://xkcd.com/info.0.json", json=True)
        if parser.has("random"):
            comic_num = randint(1, comic['num'])
            comic = await ctx.bot.util.request(f"https://xkcd.com/{comic_num}/info.0.json", json=True)
            del comic_num
        
        await ctx.embed(title=f"{comic['num']} - {comic['title']}", url=f"https://xkcd.com/{comic['num']}", fields={
            "Transcript": comic['transcript'] if comic['transcript'] else comic['alt'],
            "Post Date": f"{comic['day']}/{comic['month']}/{comic['year']}"
        }, image=comic['img'])
        del comic, parser

    @command(['edited'])
    @cooldown(3)
    @require_args(2)
    async def edit(self, ctx, *args):
        res = ctx.bot.Parser.split_args(args)
        msg = await ctx.send('...')
        await msg.edit(content=res[0] + '\u202b '+ res[1] + ' \u202b')

    @command(['echo'])
    @cooldown(5)
    @require_args()
    async def say(self, ctx, *args):
        parser = ctx.bot.Parser(args)
        parser.parse()
        
        for key in parser.flags.keys():
            if key.lower() != "reply":
                parser.shift(key)
        
        text = " ".join(parser.other) if parser.other else "???"
        if parser.has("reply"):
            res = await self.connection.post(
                f'https://discord.com/api/v8/channels/{ctx.channel.id}/messages',
                data=dumps({'content': text, 'message_reference': {'message_id': str(ctx.message.id), 'guild_id': str(ctx.guild.id)}, 'allowed_mentions': {'replied_user': False}})
            )
            if res.status != 200:
                return await ctx.send(text, allowed_mentions=ctx.bot.util.no_mentions)
            return
        await ctx.send(text, allowed_mentions=ctx.bot.util.no_mentions)
        del parser, text
    
    @command()
    @cooldown(2)
    async def joke(self, ctx):
        await ctx.trigger_typing()
        data = await ctx.bot.util.request(
            "https://official-joke-api.appspot.com/jokes/general/random",
            json=True
        )
        await ctx.embed(title=data[0]["setup"], description='||'+data[0]["punchline"]+'||')
        del data

    @command(['inspiringquotes', 'lolquote', 'aiquote', 'imagequote', 'imgquote'])
    @cooldown(10)
    @permissions(bot=['attach_files'])
    async def inspirobot(self, ctx):
        await ctx.trigger_typing()
        img = await ctx.bot.util.request('https://inspirobot.me/api', generate="true")
        await ctx.send_image(img)
        del img
    
    @command(['randomcase'])
    @cooldown(2)
    async def mock(self, ctx, *args):
        text = ' '.join(args) if args else 'i am a dumbass that forgot to put the arguments'
        return await ctx.send(''.join([choice([i.upper(), i.lower()]) for i in list(text)]))

    @command(['8ball', '8b'])
    @cooldown(3)
    @require_args(name="8ball")
    async def _8ball(self, ctx, *args):
        res = ctx.bot.util.eight_ball(ctx)
        return await ctx.embed(title="The 8-Ball", fields={
            "Question": '*"'+ discord.utils.escape_markdown(" ".join(args)) +'"*',
            "Answer": f'***{res}***'
        })
    
    @command()
    @cooldown(2)
    async def choose(self, ctx, *args):
        if (not args) or ',' not in ''.join(args):
            return await ctx.bot.cmds.invalid_args(ctx)
        return await ctx.send(choice(' '.join(args).split(',')))
    
    @command(['fact-core', 'fact-sphere', 'factsphere'])
    @cooldown(2)
    async def factcore(self, ctx):
        data = await ctx.bot.util.request(
            'https://raw.githubusercontent.com/dragonfire535/xiao/master/assets/json/fact-core.json',
            json=True
        )
        await ctx.embed(title='Fact Core', description=choice(data), thumbnail='https://i1.theportalwiki.net/img/thumb/5/55/FactCore.png/300px-FactCore.png')
        del data

def setup(client):
    client.add_cog(fun())