import discord
import random
from os import environ
from discord.ext import commands
from decorators import *
from aiohttp import ClientSession
from io import BytesIO
from json import dumps

class fun(commands.Cog):
    def __init__(self):
        self.connection = ClientSession(headers={'Authorization': 'Bot '+environ['DISCORD_TOKEN'], 'Content-Type': 'application/json'})      

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
        data = await ctx.bot.util.get_request(
            "https://official-joke-api.appspot.com/jokes/general/random",
            json=True,
            raise_errors=True
        )
        embed = ctx.bot.Embed(
            ctx,
            title = data[0]["setup"],
            desc = '||'+data[0]["punchline"]+'||'
        )
        await embed.send()
        del embed, data

    @command(['inspiringquotes', 'lolquote', 'aiquote', 'imagequote', 'imgquote'])
    @cooldown(10)
    async def inspirobot(self, ctx):
        await ctx.trigger_typing()
        img = await ctx.bot.util.get_request('https://inspirobot.me/api', raise_errors=True, generate="true")
        await ctx.bot.util.send_image_attachment(ctx, img)
        del img
    
    @command(['randomcase'])
    @cooldown(2)
    async def mock(self, ctx, *args):
        text = 'i am a dumbass that forgot to put the arguments' if len(args)==0 else ' '.join(args)
        return await ctx.send(''.join([random.choice([i.upper(), i.lower()]) for i in list(text)]))

    @command(['8ball', '8b'])
    @cooldown(3)
    @require_args(name="8ball")
    async def _8ball(self, ctx, *args):
        res = ctx.bot.util.eight_ball(ctx)
        embed = ctx.bot.Embed(ctx, title="The 8-Ball", fields={
            "Question": '*"'+ discord.utils.escape_markdown(" ".join(args)) +'"*',
            "Answer": f'***{res}***'
        })
        return await embed.send()
    
    @command()
    @cooldown(2)
    async def choose(self, ctx, *args):
        if len(args)==0 or ',' not in ''.join(args):
            return await ctx.bot.cmds.invalid_args(ctx)
        return await ctx.send(random.choice(' '.join(args).split(',')))
    
    @command(['fact-core', 'fact-sphere', 'factsphere'])
    @cooldown(2)
    async def factcore(self, ctx):
        data = await ctx.bot.util.get_request(
            'https://raw.githubusercontent.com/dragonfire535/xiao/master/assets/json/fact-core.json',
            json=True,
            raise_errors=True
        )
        embed = ctx.bot.Embed(
            ctx,
            title='Fact Core',
            desc=random.choice(data),
            thumbnail='https://i1.theportalwiki.net/img/thumb/5/55/FactCore.png/300px-FactCore.png'
        )
        await embed.send()
        del data, embed

def setup(client):
    client.add_cog(fun())