import discord
from discord.ext import commands
import sys
sys.path.append('/app/modules')
import username601 as myself
from username601 import *
import random
import splashes as src
import asyncio
import algorithm
import canvas as Painter

class fun(commands.Cog):
    def __init__(self, client):
        self.client = client
    
    @commands.command(pass_context=True, aliases=['howlove', 'friendship', 'fs'])
    @commands.cooldown(1, 2, commands.BucketType.user)
    async def lovelevel(self, ctx):
        if len(ctx.message.mentions)!=2: await ctx.send(str(self.client.get_emoji(BotEmotes.error))+' | Error: Please give me 2 tags!')
        else:
            result = algorithm.love_finder(ctx.message.mentions[0].id, ctx.message.mentions[1].id)
            await ctx.send('Love level of {} and {} is **{}%!**'.format(ctx.message.mentions[0].name, ctx.message.mentions[1].name, str(result)))
    
    @commands.command(pass_context=True)
    @commands.cooldown(1, 10, commands.BucketType.user)
    async def say(self, ctx, *args):
        if '--h' in ''.join(list(args)): await ctx.message.delete()
        await ctx.send(' '.join(list(args)).replace('--h', ''))
    
    @commands.command(pass_context=True)
    @commands.cooldown(1, 30, commands.BucketType.user)
    async def hack(self, ctx):
        if len(ctx.message.mentions)<1:
            await ctx.send(f'Please tag someone!\nExample: {Config.prefix}hack <@'+str(ctx.message.author.id)+'>')
        else:
            tohack = ctx.message.mentions[0]
            console = 'C:\\Users\\Anonymous601>'
            if len(ctx.message.mentions)>0:
                main = await ctx.send('Opening Console...')
                flow = src.hackflow(tohack)
                for i in range(0, len(flow)):
                    console = console + flow[i][1:]
                    newembed = discord.Embed(title='Anonymous601 Hacking Console', description=f'```{console}```',colour=discord.Colour.from_rgb(201, 160, 112))
                    newembed.set_thumbnail(url=myself.hackfind(flow[i], tohack.avatar_url))
                    await main.edit(content='', embed=newembed)
                    await asyncio.sleep(random.randint(2, 4))
            else:
                console = console + 'hack.exe -u '+str(ctx.message.author.name)+'ERROR: INVALID TAG.\nACCESS DENIED.\n\nHash encoded base64 cipher code:\n'+myself.bin(ctx.message.author.name)+ '\n' + console
                embed = discord.Embed(title='Anonymous601 Hacking Console', description=f'```{console}```',colour=discord.Colour.from_rgb(201, 160, 112))
                await ctx.send(embed=embed)
    
    @commands.command(pass_context=True)
    @commands.cooldown(1, 11, commands.BucketType.user)
    async def tts(self, ctx, *args):
        if len(list(args))==0:
            await ctx.send(str(self.client.get_emoji(BotEmotes.error)) +' | Invalid.')
        else:
            await ctx.send(content=str(' '.join(list(args))), tts=True)
    
    @commands.command(pass_context=True)
    @commands.cooldown(1, 10, commands.BucketType.user)
    async def joke(self, ctx):
        data = myself.api("https://official-joke-api.appspot.com/jokes/general/random")
        embed = discord.Embed(
            title = str(data[0]["setup"]),
            description = '||'+str(data[0]["punchline"])+'||',
            colour = discord.Colour.from_rgb(201, 160, 112)
        )
        await ctx.send(embed=embed)
    
    @commands.command(pass_context=True)
    @commands.cooldown(1, 5, commands.BucketType.user)
    async def slap(self, ctx):
        if len(ctx.message.mentions)<1:
            await ctx.send(str(self.client.get_emoji(BotEmotes.error))+" | Slap who? Tag someone!")
        else:
            await ctx.send(src.slap('msg')+', '+ctx.message.mentions[0].name+'!\n'+src.slap('gif'))

    @commands.command(pass_context=True)
    @commands.cooldown(1, 5, commands.BucketType.user)
    async def hbd(self, ctx):
        if len(ctx.message.mentions)<1:
            await ctx.send(str(self.client.get_emoji(BotEmotes.error))+" | who is having their birthday today?")
        else:
            await ctx.send("Happy birthday, "+ctx.message.mentions[0].name+"!\n"+src.hbd())

    @commands.command(pass_context=True, aliases=["howgay"])
    @commands.cooldown(1, 5, commands.BucketType.user)
    async def gaylevel(self, ctx):
        if len(ctx.message.mentions)<1: await ctx.send('Your gay level is {}%!'.format(str(algorithm.gay_finder(ctx.message.author.id))))
        else: await ctx.send('<@{}>\'s gay level is currently {}%!'.format(ctx.message.mentions[0].id, str(algorithm.gay_finder(ctx.message.mentions[0].id))))

    @commands.command(pass_context=True)
    @commands.cooldown(1, 5, commands.BucketType.user)
    async def randomavatar(self, ctx, *args):
        if len(list(args))<1: name = src.randomhash()
        else: name = ' '.join(list(args))
        url= 'https://api.adorable.io/avatars/285/{}.png'.format(name)
        await ctx.send(file=discord.File(Painter.urltoimage(url), 'random_avatar.png'))

    @commands.command(pass_context=True)
    @commands.cooldown(1, 5, commands.BucketType.user)
    async def secret(self, ctx):
        secretlist = src.getSecrets()
        await ctx.message.author.send('Did you know?\n'+random.choice(ctx.message.guild.members).name+str(random.choice(secretlist))+'\nDon\'t tell this to anybody else.')
        await ctx.send('I shared the secret through DM. don\'t show anyone else! :wink::ok_hand:')

    @commands.command(pass_context=True, aliases=['inspiringquotes', 'lolquote', 'aiquote', 'imagequote', 'imgquote'])
    @commands.cooldown(1, 10, commands.BucketType.user)
    async def inspirobot(self, ctx):
        async with ctx.message.channel.typing():
            img = myself.insp('https://inspirobot.me/api?generate=true')
            await ctx.send(file=discord.File(Painter.urltoimage(img), 'inspirobot.png'))
    
    @commands.command(pass_context=True, name='8ball', aliases=['8b'])
    @commands.cooldown(1, 3, commands.BucketType.user)
    async def _8ball(self, ctx):
        async with ctx.message.channel.typing():
            data = myself.api("https://yesno.wtf/api")
            if data["image"].endswith('.gif'): img, filename = Painter.gif.giffromURL(data["image"], True), 'answer.gif'
            else: img, filename = Painter.urltoimage(data["image"]), 'answer.png'
            await ctx.send(content=data['answer'], file=discord.File(img, filename))

    @commands.command(pass_context=True, aliases=['serverdeathnote', 'dn'])
    @commands.cooldown(1, 20, commands.BucketType.user)
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
    
    @commands.command(pass_context=True)
    @commands.cooldown(1, 5, commands.BucketType.user)
    async def choose(self, ctx, *args):
        if len(list(args))==0 or ',' not in ''.join(list(args)):
            await ctx.send('send in something!\nLike: `choose he is cool, he is not cool`')
        else:
            await ctx.send(random.choice(' '.join(list(args)).split(',')))
    
    @commands.command(pass_context=True)
    @commands.cooldown(1, 5, commands.BucketType.user)
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
    
    @commands.command(pass_context=True, aliases=['fact-core', 'fact-sphere', 'factsphere'])
    @commands.cooldown(1, 5, commands.BucketType.user)
    async def factcore(self, ctx):
        data = myself.jsonisp('https://raw.githubusercontent.com/dragonfire535/xiao/master/assets/json/fact-core.json')
        embed = discord.Embed(title='Fact Core', description=random.choice(data), colour=discord.Colour.from_rgb(201, 160, 112))
        embed.set_thumbnail(url='https://i1.theportalwiki.net/img/thumb/5/55/FactCore.png/300px-FactCore.png')
        await ctx.send(embed=embed)
def setup(client):
    client.add_cog(fun(client))
