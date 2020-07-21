import discord
from discord.ext import commands
import sys
sys.path.append('/app/modules')
import canvas as Painter
import random
import username601 as myself
from username601 import *

class image(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.command(pass_context=True)
    @commands.cooldown(1, 5, commands.BucketType.user)
    async def lucario(self, ctx):
        embed = discord.Embed(title='Lucario!', color=discord.Color.from_rgb(201, 160, 112))
        embed.set_image(url=myself.jsonisp('http://pics.floofybot.moe/image?token=lucario&category=sfw')['image'])
        await ctx.send(embed=embed)
    
    @commands.command(pass_context=True, aliases=['ducks', 'quack', 'duk'])
    @commands.cooldown(1, 5, commands.BucketType.user)
    async def duck(self, ctx):
        await ctx.send(file=discord.File(Painter.urltoimage(myself.jsonisp('https://random-d.uk/api/v2/random?format=json')['url']), 'duck.png'))

    @commands.command(pass_context=True, aliases=['snek', 'snakes', 'python', 'py'])
    @commands.cooldown(1, 5, commands.BucketType.user)
    async def snake(self, ctx):
        await ctx.send(file=discord.File(Painter.urltoimage('https://fur.im/snek/i/'+str(random.randint(1, 874))+'.png'), 'snek.png'))

    @commands.command(pass_context=True, aliases=['imageoftheday'])
    @commands.cooldown(1, 21600, commands.BucketType.user)
    async def iotd(self, ctx):
        data = myself.jsonisp('https://www.bing.com/HPImageArchive.aspx?format=js&idx=0&n=1&mkt=en-US')['images'][0]
        embed = discord.Embed( title=data['copyright'], url=data['copyrightlink'], color=discord.Color.from_rgb(201, 160, 112))
        embed.set_image(url='https://bing.com'+data['url'])
        await ctx.send(embed=embed)

    @commands.command(pass_context=True)
    @commands.cooldown(1, 5, commands.BucketType.user)
    async def httpcat(self, ctx, *args):
        if len(list(args))==0: code = str(random.randint(200, 550))
        else: code = str(' '.join(list(args)))
        await ctx.send(file=discord.File(Painter.urltoimage('https://http.cat/'+str(code)+'.jpg'), 'httpcat.png'))

    @commands.command(pass_context=True)
    @commands.cooldown(1, 5, commands.BucketType.user)
    async def goat(self, ctx):
        await ctx.send(file=discord.File(Painter.urltoimage('https://placegoat.com/'+str(random.randint(500, 700))), 'goat.png'))

    @commands.command(pass_context=True)
    @commands.cooldown(1, 5, commands.BucketType.user)
    async def rotate(self, ctx):
        async with ctx.message.channel.typing():
            if len(ctx.message.mentions)==0: ava = str(ctx.message.author.avatar_url).replace('.webp?size=1024', '.jpg?size=512')
            else: ava = str(ctx.message.mentions[0].avatar_url).replace('.webp?size=1024', '.jpg?size=512')
            data = Painter.gif.rotate(ava)
            await ctx.send(file=discord.File(data, 'rotate.gif'))

    @commands.command(pass_context=True)
    @commands.cooldown(1, 5, commands.BucketType.user)
    async def resize(self, ctx, *args):
        correct, wh = '', []
        for i in list(args):
            if i.isnumeric():
                correct += 'y'
                wh.append(int(i))
        async with ctx.message.channel.typing():
            if correct=='yy':
                if len(ctx.message.mentions)<1: ava = str(ctx.message.author.avatar_url).replace('.webp?size=1024', '.jpg?size=512')
                else: ava = str(ctx.message.mentions[0].avatar_url).replace('.webp?size=1024', '.jpg?size=512')
                if wh[0]>2000 or wh[1]>2000: await ctx.send(str(self.client.get_emoji(BotEmotes.error)) + " | Your image is too big!")
                elif wh[0]<300 or wh[1]<300: await ctx.send(str(self.client.get_emoji(BotEmotes.error)) + " | Your image is too small!")
                else:
                    data = Painter.resize(ava, wh[0], wh[1])
                    await ctx.send(file=discord.File(data, 'resize.png'))
            else:
                await ctx.send(str(self.client.get_emoji(BotEmotes.error)) + " | Where are the parameters?")

    @commands.command(pass_context=True)
    @commands.cooldown(1, 10, commands.BucketType.user)
    async def nature(self, ctx):
        async with ctx.message.typing():
            await ctx.send(file=discord.File(Painter.urltoimage('https://source.unsplash.com./1600x900/?nature'), 'nature.png'))

    @commands.command(pass_context=True, aliases=['earth', 'moon'])
    @commands.cooldown(1, 10, commands.BucketType.user)
    async def space(self, ctx):
        async with ctx.message.typing():
            await ctx.send(file=discord.File(Painter.urltoimage('https://source.unsplash.com./1600x900/?{}'.format(random.choice(['earth', 'moon', 'space']))), 'nature.png'))

    @commands.command(pass_context=True)
    @commands.cooldown(1, 5, commands.BucketType.user)
    async def ytthumbnail(self, ctx, *args):
        if len(list(args))!=0:
            videoid = 'dQw4w9WgXcQ'
            async with ctx.message.channel.typing():
                if list(args)[0].endswith('/'): list(args)[0] = list(args)[0][:-1]
                if 'https://' in list(args)[0]: list(args)[0] = list(args)[0].replace('https://', '')
                elif 'http://' in list(args)[0]: list(args)[0] = list(args)[0].replace('http://', '')
                if '/watch?v=' in list(args)[0]: videoid = list(args)[0].split('/watch?v=')[1]
                else: videoid = list(args)[0].split('/')[1]
                url = 'https://img.youtube.com/vi/'+str(videoid)+'/mqdefault.jpg'
                data = Painter.urltoimage(url)
                await ctx.send(file=discord.File(data, 'thumbnail.png'))
        else: await ctx.send(str(self.client.get_emoji(BotEmotes.error))+' | gimme something to work with! Like a youtube url!')
    @commands.command(pass_context=True, aliases=['cat', 'fox', 'sadcat', 'bird'])
    @commands.cooldown(1, 5, commands.BucketType.user)
    async def dog(self, ctx):
        async with ctx.message.channel.typing():
            links = {
                "dog": "https://random.dog/woof.json|url",
                "cat": "https://api.alexflipnote.dev/cats|file",
                "sadcat": "https://api.alexflipnote.dev/sadcat|file",
                "bird": "https://api.alexflipnote.dev/sadcat|file",
                "fox": 'https://randomfox.ca/floof/?ref=apilist.fun|image'
            }
            for i in list(links.keys()):
                if str(ctx.message.content[1:]).lower().replace(' ', '')==i: link = links[i] ; break
            apiied = myself.jsonisp(link.split('|')[0])[link.split('|')[1]]
            data = Painter.urltoimage(apiied)
            await ctx.send(file=discord.File(data, 'animal.png'))

    @commands.command(pass_context=True)
    @commands.cooldown(1, 5, commands.BucketType.user)
    async def panda(self, ctx):
        link, col, msg = random.choice(["https://some-random-api.ml/img/panda", "https://some-random-api.ml/img/red_panda"]), discord.Colour.from_rgb(201, 160, 112), 'Here is some cute pics of pandas.'
        data = myself.jsonisp(link)['link']
        embed = discord.Embed(title=msg, color=col)
        embed.set_image(url=data)
        await ctx.send(embed=embed)
    
    @commands.command(pass_context=True)
    @commands.cooldown(1, 5, commands.BucketType.user)
    async def shibe(self, ctx):
        async with ctx.message.channel.typing():
            data = myself.jsonisp("http://shibe.online/api/shibes?count=1")[0]
            await ctx.send(file=discord.File(Painter.smallURL(data), 'shibe.png'))
    
    @commands.command(pass_context=True)
    @commands.cooldown(1, 5, commands.BucketType.user)
    async def ship(self, ctx):
        async with ctx.message.channel.typing():
            if len(ctx.message.mentions)!=2:
                first, second = str(ctx.message.author.avatar_url).replace('webp', 'png'), str(random.choice(i.avatar_url for i in ctx.message.guild.members).replace('webp', 'png'))
            else:
                first, second = str(ctx.message.mentions[0].avatar_url).replace('webp', 'png'), str(ctx.message.mentions[1].avatar_url).replace('webp', 'png')
            url = f'https://api.alexflipnote.dev/ship?user={first}&user2={second}'
            await ctx.send(file=discord.File(Painter.urltoimage(url), 'ship.png'))

    @commands.command(pass_context=True, aliases=['coffee'])
    @commands.cooldown(1, 5, commands.BucketType.user)
    async def food(self, ctx, *args):
        if len(list(args))==0:
            data = myself.jsonisp('https://nekobot.xyz/api/image?type='+str(ctx.message.content[1:]))
            link = data['message'].replace('\/', '/')
            if 'food' in ctx.message.content:
                col = int(data['color'])
            elif 'coffee' in ctx.message.content:
                col, num = int(data['color']), random.randint(0, 1)
                if num==0: link = myself.jsonisp('https://coffee.alexflipnote.dev/random.json')['file']
                else: link = myself.jsonisp('https://nekobot.xyz/api/image?type=coffee')['message'].replace('\/', '/')
            async with ctx.message.channel.typing():
                data = Painter.urltoimage(link.replace('\/', '/'))
                await ctx.send(file=discord.File(data, ctx.message.content[1:]+'.png'))

    @commands.command(pass_context=True, aliases=['blurpify', 'threats'])
    @commands.cooldown(1, 5, commands.BucketType.user)
    async def deepfry(self, ctx, *args):
        if len(ctx.message.mentions)==0:
            await ctx.send('Please tag someone!')
        else:
            if len(list(args))==1:
                async with ctx.message.channel.typing():
                    if 'threat' in ctx.message.content: inputtype = 'url'
                    else: inputtype = 'image'
                    av = ctx.message.mentions[0].avatar_url
                    url='https://nekobot.xyz/api/imagegen?type='+str(str(ctx.message.content).split()[0])[1:]+'&'+inputtype+'='+str(av)[:-15]+'&raw=1'
                    await ctx.send(file=discord.File(Painter.urltoimage(url), 'lol.png'))
            else:
                await ctx.send(str(self.client.get_emoji(BotEmotes.error))+' | We do not accept more than 1 arguments!')

    @commands.command(pass_context=True, aliases=['invert', 'magik', 'pixelate', 'b&w'])
    @commands.cooldown(1, 5, commands.BucketType.user)
    async def jpeg(self, ctx):
        com = str(ctx.message.content).split()[0].replace('jpeg', 'jpegify')[1:]
        if len(ctx.message.mentions)==0: avatar = str(ctx.message.author.avatar_url).replace('webp', 'png')
        else: avatar = str(ctx.message.mentions[0].avatar_url).replace('.webp', '.png')
        await ctx.send(file=discord.File(Painter.urltoimage(f'https://api.alexflipnote.dev/filter/{com}?image={avatar}'), 'filtered.png'))
def setup(client):
    client.add_cog(image(client))
