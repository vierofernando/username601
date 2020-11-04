import discord
import sys
import random
from discord.ext import commands
from os import getcwd, name, environ
sys.path.append(environ['BOT_MODULES_DIR'])
from decorators import command, cooldown
from aiohttp import ClientSession
from io import BytesIO
import asyncio
from gtts import gTTS

class fun(commands.Cog):
    def __init__(self, client):
        self.client = client        

    @command('talk,gtts,texttospeech,text-to-speech')
    @cooldown(5)
    async def tts(self, ctx, *args):
        if len(args)==0: raise self.client.utils.send_error_message('Please send arguments!')
        res = BytesIO()
        tts = gTTS(text=' '.join(args), lang='en', slow=False)
        tts.write_to_fp(res)
        res.seek(0)
        await ctx.send(file=discord.File(fp=res, filename='tts.mp3'))

    @command()
    @cooldown(6)
    async def flip(self, ctx, *args):
        av = self.client.utils.getUserAvatar(ctx, args)
        async with ctx.channel.typing():
            im = self.client.gif.flip(av)
            return await ctx.send(file=discord.File(im, 'flip.gif'))

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
        res = self.client.utils.split_parameter_to_two(args)
        if res is None: raise self.client.utils.send_error_message('Please send a valid two user ids/names/mentions!')
        user1, user2 = self.client.utils.getUser(res[0]), self.client.utils.getUser(res[1])
        result = self.client.algorithm.love_finder(user1.id, user2.id)
        await ctx.send('Love level of {} and {} is **{}%!**'.format(ctx.message.mentions[0].name, ctx.message.mentions[1].name, str(result)))
    
    @command('echo,reply')
    @cooldown(1)
    async def say(self, ctx, *args):
        if '--h' in ''.join(args):
            try: await ctx.message.delete()
            except: pass
        await ctx.send(' '.join(args).replace('--h', ''), allowed_mentions=discord.AllowedMentions(everyone=False, users=False, roles=False))
    
    @command()
    @cooldown(1)
    async def joke(self, ctx):
        data = self.client.utils.fetchJSON("https://official-joke-api.appspot.com/jokes/general/random")
        embed = discord.Embed(
            title = str(data[0]["setup"]),
            description = '||'+str(data[0]["punchline"])+'||',
            colour = ctx.guild.me.roles[::-1][0].color
        )
        await ctx.send(embed=embed)

    @command("howgay")
    @cooldown(5)
    async def gaylevel(self, ctx, *args):
        data = self.client.utils.getUser(ctx, args)
        name = data.name+'\'s' if data!=ctx.author else 'Your'
        await ctx.send('{} gay level is currently {}%!'.format(name, str(self.client.algorithm.gay_finder(data.id))))

    @command()
    @cooldown(5)
    async def randomavatar(self, ctx, *args):
        if len(args)<1: name = 'your mom'
        else: name = ' '.join(args)
        url= 'https://api.adorable.io/avatars/285/{}.png'.format(self.client.utils.encode_uri(name))
        await ctx.send(file=discord.File(self.client.canvas.urltoimage(url), 'random_avatar.png'))

    @command('inspiringquotes,lolquote,aiquote,imagequote,imgquote')
    @cooldown(10)
    async def inspirobot(self, ctx):
        async with ctx.channel.typing():
            img = self.client.utils.inspect_element('https://inspirobot.me/api?generate=true')
            await ctx.send(file=discord.File(self.client.canvas.urltoimage(img), 'inspirobot.png'))
    
    @command('randomcase')
    @cooldown(1)
    async def mock(self, ctx, *args):
        text = 'i am a dumbass that forgot to put the arguments' if len(args)==0 else str(' '.join(args))
        return await ctx.send(''.join([random.choice([i.upper(), i.lower()]) for i in list(text)]))

    @command('8ball,8b')
    @cooldown(3)
    async def _8ball(self, ctx):
        async with ctx.channel.typing():
            data = self.client.utils.fetchJSON("https://yesno.wtf/api")
            async with self.client.bot_session.get(data['image']) as r:
                res = await r.read()
                await ctx.send(content='**'+data['answer'].upper()+'**', file=discord.File(fp=BytesIO(res), filename=data['answer'].upper()+".gif"))

    @command('serverdeathnote,dn')
    @cooldown(10)
    async def deathnote(self, ctx):
        if ctx.guild.member_count>500: raise self.client.utils.send_error_message('This server has soo many members')
        member, in_the_note, notecount, membercount = [], "", 0, 0
        for i in range(ctx.guild.member_count):
            if ctx.guild.members[i].name!=ctx.author.name:
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
            url = requests.get('https://useless-api.vierofernando.repl.co/useless-sites').json()['url']
            await ctx.send(self.client.success_emoji+f' | **{url}**')
        except:
            raise self.client.utils.send_error_message(f'oops. there is some error, meanwhile look at this useless site: <https://top.gg/bot/{self.client.user.id}/vote>')
    
    @command()
    @cooldown(2)
    async def choose(self, ctx, *args):
        if len(args)==0 or ',' not in ''.join(args):
            raise self.client.utils.send_error_message(f'send in something!\nLike: `{self.client.command_prefix}choose he is cool, he is not cool`')
        else:
            await ctx.send(random.choice(' '.join(args).split(',')))
    
    @command()
    @cooldown(2)
    async def temmie(self, ctx, *args):
        if len(args)==0: raise self.client.utils.send_error_message('Please send something to be encoded.')
        else:
            link, num = 'https://raw.githubusercontent.com/dragonfire535/xiao/master/assets/json/temmie.json', 1
            data = self.client.utils.fetchJSON(link)
            keyz = list(data.keys())
            total = ''
            for j in range(num, len(keyz)):
                if total=='': total = ' '.join(args)
                total = total.replace(keyz[j], data[keyz[j]])
            await ctx.send(total)
    
    @command('fact-core,fact-sphere,factsphere')
    @cooldown(2)
    async def factcore(self, ctx):
        data = self.client.utils.fetchJSON('https://raw.githubusercontent.com/dragonfire535/xiao/master/assets/json/fact-core.json')
        embed = discord.Embed(title='Fact Core', description=random.choice(data), colour=ctx.guild.me.roles[::-1][0].color)
        embed.set_thumbnail(url='https://i1.theportalwiki.net/img/thumb/5/55/FactCore.png/300px-FactCore.png')
        await ctx.send(embed=embed)
def setup(client):
    client.add_cog(fun(client))