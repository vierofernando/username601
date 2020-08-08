import discord
from discord.ext import commands
import sys
sys.path.append('/home/runner/hosting601/modules')
import username601 as myself
from username601 import *
import random
from decorators import command, cooldown
import splashes as src
import asyncio
import algorithm
import canvas as Painter

class fun(commands.Cog):
    def __init__(self, client):
        self.client = client
    
    @command('howlove,friendship,fs')
    @cooldown(2)
    async def lovelevel(self, ctx):
        if len(ctx.message.mentions)!=2: await ctx.send(str(self.client.get_emoji(BotEmotes.error))+' | Error: Please give me 2 tags!')
        else:
            result = algorithm.love_finder(ctx.message.mentions[0].id, ctx.message.mentions[1].id)
            await ctx.send('Love level of {} and {} is **{}%!**'.format(ctx.message.mentions[0].name, ctx.message.mentions[1].name, str(result)))
    
    @command()
    @cooldown(10)
    async def say(self, ctx, *args):
        if '--h' in ''.join(list(args)): await ctx.message.delete()
        await ctx.send(' '.join(list(args)).replace('--h', '').replace('@everyone', '<everyone>').replace('@here', '<here>'))
    
    @command()
    @cooldown(30)
    async def hack(self, ctx, *args):
        foundArgs, tohack = False, None
        try:
            tohack = ctx.guild.get_member(int(list(args)[0]))
            assert tohack!=None
            foundArgs = True
        except: pass
        if len(ctx.message.mentions)<1 and not foundArgs:
            await ctx.send(f'Please tag someone!\nExample: {Config.prefix}hack <@'+str(ctx.message.author.id)+'>')
        else:
            if tohack==None: tohack = ctx.message.mentions[0]
            console = 'username601@HACKERMAN:/$ '
            if len(ctx.message.mentions)>0 or foundArgs:
                main = await ctx.send('Opening Console...\n```bash\nloading...```')
                flow = src.hackflow(tohack)
                for i in range(0, len(flow)):
                    console = console + flow[i][1:]
                    await main.edit(content=f"```bash\n{console}```")
                    await asyncio.sleep(random.randint(2, 4))
            else:
                console += 'ERROR: INVALID TAG.\nACCESS DENIED.\n\nHash encoded base64 cipher code:\n'+myself.bin(ctx.message.author.name)+ '\n' + console
                await ctx.send(f'```bash\n{console}```')
    
    @command()
    @cooldown(11)
    async def tts(self, ctx, *args):
        if len(list(args))==0:
            await ctx.send(str(self.client.get_emoji(BotEmotes.error)) +' | Invalid.')
        else:
            await ctx.send(content=str(' '.join(list(args))), tts=True)
    
    @command()
    @cooldown(10)
    async def joke(self, ctx):
        data = myself.api("https://official-joke-api.appspot.com/jokes/general/random")
        embed = discord.Embed(
            title = str(data[0]["setup"]),
            description = '||'+str(data[0]["punchline"])+'||',
            colour = discord.Colour.from_rgb(201, 160, 112)
        )
        await ctx.send(embed=embed)
    
    @command()
    @cooldown(5)
    async def slap(self, ctx):
        if len(ctx.message.mentions)<1:
            await ctx.send(str(self.client.get_emoji(BotEmotes.error))+" | Slap who? Tag someone!")
        else:
            await ctx.send(src.slap('msg')+', '+ctx.message.mentions[0].name+'!\n'+src.slap('gif'))

    @command()
    @cooldown(5)
    async def hbd(self, ctx):
        if len(ctx.message.mentions)<1:
            await ctx.send(str(self.client.get_emoji(BotEmotes.error))+" | who is having their birthday today?")
        else:
            await ctx.send("Happy birthday, "+ctx.message.mentions[0].name+"!\n"+src.hbd())

    @command("howgay")
    @cooldown(5)
    async def gaylevel(self, ctx):
        if len(ctx.message.mentions)<1: await ctx.send('Your gay level is {}%!'.format(str(algorithm.gay_finder(ctx.message.author.id))))
        else: await ctx.send('<@{}>\'s gay level is currently {}%!'.format(ctx.message.mentions[0].id, str(algorithm.gay_finder(ctx.message.mentions[0].id))))

    @command()
    @cooldown(5)
    async def randomavatar(self, ctx, *args):
        if len(list(args))<1: name = src.randomhash()
        else: name = ' '.join(list(args))
        url= 'https://api.adorable.io/avatars/285/{}.png'.format(name)
        await ctx.send(file=discord.File(Painter.urltoimage(url), 'random_avatar.png'))

    @command()
    @cooldown(5)
    async def secret(self, ctx):
        secretlist = src.getSecrets()
        await ctx.message.author.send('Did you know?\n'+random.choice(ctx.message.guild.members).name+str(random.choice(secretlist))+'\nDon\'t tell this to anybody else.')
        await ctx.send('I shared the secret through DM. don\'t show anyone else! :wink::ok_hand:')

    @command('inspiringquotes,lolquote,aiquote,imagequote,imgquote')
    @cooldown(10)
    async def inspirobot(self, ctx):
        async with ctx.message.channel.typing():
            img = myself.insp('https://inspirobot.me/api?generate=true')
            await ctx.send(file=discord.File(Painter.urltoimage(img), 'inspirobot.png'))
    
    @command('8ball,8b')
    @cooldown(3)
    async def _8ball(self, ctx):
        async with ctx.message.channel.typing():
            data = myself.api("https://yesno.wtf/api")
            if data["image"].endswith('.gif'): img, filename = Painter.gif.giffromURL(data["image"], True), 'answer.gif'
            else: img, filename = Painter.urltoimage(data["image"]), 'answer.png'
            await ctx.send(content=data['answer'], file=discord.File(img, filename))

    @command('serverdeathnote,dn')
    @cooldown(20)
    async def deathnote(self, ctx):
        member, in_the_note, notecount, membercount = [], "", 0, 0
        for i in range(0, int(len(ctx.message.guild.members))):
            if ctx.message.guild.members[i].name!=ctx.message.author.name:
                member.append(ctx.message.guild.members[i].name)
                membercount = int(membercount) + 1
        chances = ['ab', 'abc', 'abcd']
        strRandomizer = random.choice(chances)
        for i in range(0, int(membercount)):
            if random.choice(list(strRandomizer))=='b':
                notecount = int(notecount) + 1
                in_the_note = in_the_note+str(notecount)+'. '+ str(member[i]) + '\n'
        death, count = random.choice(member), random.choice(list(range(0, int(membercount))))
        embed = discord.Embed(
            title=ctx.message.guild.name+'\'s death note',
            description=str(in_the_note),
            colour = discord.Colour.from_rgb(201, 160, 112)
        )
        await ctx.send(embed=embed)
    
    @command()
    @cooldown(5)
    async def choose(self, ctx, *args):
        if len(list(args))==0 or ',' not in ''.join(list(args)):
            await ctx.send('send in something!\nLike: `choose he is cool, he is not cool`')
        else:
            await ctx.send(random.choice(' '.join(list(args)).split(',')))
    
    @command()
    @cooldown(5)
    async def temmie(self, ctx, *args):
        if len(list(args))==0: await ctx.send(str(self.client.get_emoji(BotEmotes.error))+' | Please send something to be encoded.')
        else:
            link, num = 'https://raw.githubusercontent.com/dragonfire535/xiao/master/assets/json/temmie.json', 1
            data = myself.jsonisp(link)
            keyz = list(data.keys())
            total = ''
            for j in range(num, len(keyz)):
                if total=='': total = ' '.join(list(args))
                total = total.replace(keyz[j], data[keyz[j]])
            await ctx.send(total)
    
    @command('fact-core,fact-sphere,factsphere')
    @cooldown(5)
    async def factcore(self, ctx):
        data = myself.jsonisp('https://raw.githubusercontent.com/dragonfire535/xiao/master/assets/json/fact-core.json')
        embed = discord.Embed(title='Fact Core', description=random.choice(data), colour=discord.Colour.from_rgb(201, 160, 112))
        embed.set_thumbnail(url='https://i1.theportalwiki.net/img/thumb/5/55/FactCore.png/300px-FactCore.png')
        await ctx.send(embed=embed)
def setup(client):
    client.add_cog(fun(client))
