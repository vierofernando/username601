import discord
import random
from os import environ
from discord.ext import commands
from category.decorators import command, cooldown
from aiohttp import ClientSession
from io import BytesIO
import asyncio
from gtts import gTTS
from json import dumps

class fun(commands.Cog):
    def __init__(self):
        self.connection = ClientSession(headers={'Authorization': 'Bot '+environ['DISCORD_TOKEN'], 'Content-Type': 'application/json'})      

    @command('talk,gtts,texttospeech,text-to-speech')
    @cooldown(5)
    async def tts(self, ctx, *args):
        ctx.bot.Parser.require_args(ctx, args)
        res = BytesIO()
        tts = gTTS(text=' '.join(args), lang='en', slow=False)
        tts.write_to_fp(res)
        res.seek(0)
        await ctx.send(file=discord.File(fp=res, filename='tts.mp3'))
        del res
        del tts

    @command('edit')
    @cooldown(2)
    async def edited(self, ctx, *args):
        msg = await ctx.send('...')
        if len(args)==0 or '|' not in ' '.join(args):
            return await msg.edit(content='Please use | to place where the \u202b will be. \u202b')
        await msg.edit(content=' '.join(args).replace('|', '\u202b')+' \u202b')

    @command('howlove,friendship,fs')
    @cooldown(2)
    async def lovelevel(self, ctx, *args):
        res = ctx.bot.Parser.split_content_to_two(args)
        if res is None: raise ctx.bot.util.BasicCommandException('Please send a valid two user ids/names/mentions!')
        user1, user2 = ctx.bot.Parser.parse_user(res[0]), ctx.bot.Parser.parse_user(res[1])
        result = ctx.bot.algorithm.love_finder(user1.id, user2.id)
        await ctx.send('Love level of {} and {} is **{}%!**'.format(user1.display_name, user2.display_name, result))
    
    @command('echo,reply')
    @cooldown(5)
    async def say(self, ctx, *args):
        if len(args) == 0: return await ctx.send("Send `something`.")
        text = ' '.join(args).lower()[0:1999]
        if ctx.bot.util.get_command_name(ctx) == "reply":
            res = await self.connection.post(
                f'https://discord.com/api/v8/channels/{ctx.channel.id}/messages',
                data=dumps({'content': text, 'message_reference': {'message_id': str(ctx.message.id), 'guild_id': str(ctx.guild.id)}, 'allowed_mentions': {'replied_user': False}})
            )
            if res.status != 200:
                return await ctx.send(text, allowed_mentions=ctx.bot.util.no_mentions)
            return
        if '--h' in text:
            try: await ctx.message.delete()
            except: pass
        await ctx.send(text.replace('--h', ''), allowed_mentions=ctx.bot.util.no_mentions)
    
    @command()
    @cooldown(2)
    async def joke(self, ctx):
        data = await ctx.bot.util.get_request(
            "https://official-joke-api.appspot.com/jokes/general/random",
            json=True,
            raise_errors=True
        )
        embed = discord.Embed(
            title = str(data[0]["setup"]),
            description = '||'+str(data[0]["punchline"])+'||',
            colour = ctx.guild.me.roles[::-1][0].color
        )
        await ctx.send(embed=embed)

    @command("howgay")
    @cooldown(5)
    async def gaylevel(self, ctx, *args):
        data = ctx.bot.Parser.parse_user(ctx, args)
        name = data.display_name+'\'s' if data!=ctx.author else 'Your'
        await ctx.send('{} gay level is currently {}%!'.format(name, str(ctx.bot.algorithm.gay_finder(data.id))))

    @command('inspiringquotes,lolquote,aiquote,imagequote,imgquote')
    @cooldown(10)
    async def inspirobot(self, ctx):
        await ctx.trigger_typing()
        img = await ctx.bot.util.get_request('https://inspirobot.me/api', raise_errors=True, generate="true")
        return await ctx.bot.util.send_image_attachment(ctx, img)
    
    @command('randomcase')
    @cooldown(2)
    async def mock(self, ctx, *args):
        text = 'i am a dumbass that forgot to put the arguments' if len(args)==0 else str(' '.join(args))
        return await ctx.send(''.join([random.choice([i.upper(), i.lower()]) for i in list(text)]))

    @command('8ball,8b')
    @cooldown(3)
    async def _8ball(self, ctx, *args):
        if len(args) == 0: raise ctx.bot.util.BasicCommandException("Please send a question!")
        
        res = ctx.bot.util.eight_ball(ctx)
        embed = ctx.bot.Embed(ctx, title="The 8-Ball", fields={
            "Question": '*"'+ discord.utils.escape_markdown(" ".join(args)) +'"*',
            "Answer": f'***{res}***'
        })
        return await embed.send()

    @command('serverdeathnote,dn')
    @cooldown(10)
    async def deathnote(self, ctx):
        if ctx.guild.member_count>500: raise ctx.bot.util.BasicCommandException('This server has soo many members')
        member, in_the_note, notecount, membercount = [], "", 0, 0
        for i in range(ctx.guild.member_count):
            if ctx.guild.members[i].display_name!=ctx.author.display_name:
                member.append(ctx.guild.members[i].name)
                membercount = int(membercount) + 1
        chances = ['ab', 'abc', 'abcd']
        strRandomizer = random.choice(chances)
        for i in range(int(membercount)):
            if random.choice(list(strRandomizer))=='b':
                notecount = int(notecount) + 1
                in_the_note = in_the_note+str(notecount)+'. '+ str(member[i]) + '\n'
        death, count = random.choice(member), random.choice(list(range(int(membercount))))
        embed = discord.Embed(
            title=ctx.guild.name+'\'s death note',
            description=str(in_the_note),
            colour = ctx.guild.me.roles[::-1][0].color
        )
        await ctx.send(embed=embed)
    
    @command('useless,uselesssites,uselessweb,uselesswebsites,uselesswebsite')
    @cooldown(3)
    async def uselesswebs(self, ctx):
        try:
            url = await ctx.bot.util.get_request(
                'https://useless-api.vierofernando.repl.co/uselesssites',
                json=True,
                raise_errors=True
            )
            await ctx.send(ctx.bot.util.success_emoji+f' | **{url["url"]}**')
        except:
            raise ctx.bot.util.BasicCommandException(f'oops. there is some error, meanwhile look at this useless site: <https://top.gg/bot/{ctx.bot.user.id}/vote>')
    
    @command()
    @cooldown(2)
    async def choose(self, ctx, *args):
        if len(args)==0 or ',' not in ''.join(args):
            raise ctx.bot.util.BasicCommandException(f'send in something!\nLike: `{ctx.bot.command_prefix}choose he is cool, he is not cool`')
        return await ctx.send(random.choice(' '.join(args).split(',')))
    
    @command()
    @cooldown(2)
    async def temmie(self, ctx, *args):
        ctx.bot.Parser.require_args(ctx, args)
        link, num = 'https://raw.githubusercontent.com/dragonfire535/xiao/master/assets/json/temmie.json', 1
        data = await ctx.bot.util.get_request(
            link,
            json=True,
            raise_errors=True
        )
        keyz = list(data.keys())
        total = ''
        for j in range(num, len(keyz)):
            if total=='': total = ' '.join(args)
            total = total.replace(keyz[j], data[keyz[j]])
        await ctx.send(total)
    
    @command('fact-core,fact-sphere,factsphere')
    @cooldown(2)
    async def factcore(self, ctx):
        data = await ctx.bot.util.get_request(
            'https://raw.githubusercontent.com/dragonfire535/xiao/master/assets/json/fact-core.json',
            json=True,
            raise_errors=True
        )
        embed = discord.Embed(title='Fact Core', description=random.choice(data), colour=ctx.guild.me.roles[::-1][0].color)
        embed.set_thumbnail(url='https://i1.theportalwiki.net/img/thumb/5/55/FactCore.png/300px-FactCore.png')
        await ctx.send(embed=embed)
def setup(client):
    client.add_cog(fun())