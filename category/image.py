import discord
from discord.ext import commands
import sys
sys.path.append('/home/runner/hosting601/modules')
from canvas import Painter, GifGenerator
from decorators import command, cooldown
import random
from io import BytesIO
import username601 as myself
from aiohttp import ClientSession
from username601 import *

class image(commands.Cog):
    def __init__(self, client):
        self.client = client
        self.canvas = Painter(
            r'/home/runner/hosting601/assets/pics/',
            r'/home/runner/hosting601/assets/fonts/'
        )
        self.gif = GifGenerator(
            r'/home/runner/hosting601/assets/pics/',
            r'/home/runner/hosting601/assets/fonts/'
        )
        self.session = ClientSession()

    @command('pika')
    @cooldown(2)
    async def pikachu(self, ctx):
        async with ctx.message.channel.typing():
            async with self.session.get(myself.jsonisp('https://some-random-api.ml/img/pikachu')['link']) as r:
                res = await r.read()
                await ctx.send(file=discord.File(fp=BytesIO(res), filename="pikachu.gif"))

    @command()
    @cooldown(5)
    async def blur(self, ctx, *args):
        ava = myself.getUserAvatar(ctx, args, size=512)
        async with ctx.message.channel.typing():
            im = self.canvas.blur(ava)
            await ctx.send(file=discord.File(im, 'blur.png'))

    @command('glitchify,matrix')
    @cooldown(5)
    async def glitch(self, ctx, *args):
        ava = myself.getUserAvatar(ctx, args, size=512)
        async with ctx.message.channel.typing():
            im = self.canvas.glitch(ava)
            await ctx.send(file=discord.File(im, 'glitch.png'))

    @command('destroy,destroyava,destroyavatar')
    @cooldown(5)
    async def destroyimg(self, ctx, *args):
        src = myself.getUserAvatar(ctx, args, size=512)
        async with ctx.message.channel.typing():
            await ctx.send(file=discord.File(
                self.canvas.ruin(src), 'ruinedavatar.png'
            ))

    @command('application')
    @cooldown(5)
    async def app(self, ctx, *args):
        src = myself.getUserAvatar(ctx, args, size=512)
        elem = myself.getUser(ctx, args)
        async with ctx.message.channel.typing():
            await ctx.send(file=discord.File(
                self.canvas.app(src, elem.name), 'app.exe.png'
            ))


    @command('distortion')
    @cooldown(5)
    async def distort(self, ctx, *args, blacklist=None):
        num = 5
        try:
            for i in range(len(list(args))):
                if list(args)[i].isnumeric():
                    num, blacklist = int(list(args)[i]), i
                    break
            if blacklist!=None: del list(args)[blacklist]
        except: num = 5
        if num not in range(0, 999):
            return await ctx.send("{} | damn that level is hella weirdd".format(
                str(self.client.get_emoji(BotEmotes.error))
            ))
        ava = myself.getUserAvatar(ctx, args)
        async with ctx.message.channel.typing():
            await ctx.send(file=discord.File(
                self.canvas.urltoimage('https://nezumiyuiz.glitch.me/api/distort?level={}&image={}'.format(
                    str(num), str(ava)
                )), 'distort.png'
            ))

    @command()
    @cooldown(5)
    async def garfield(self, ctx):
        try:
            year, month, day = str(random.randint(1979, 2019)), str(random.randint(1, 12)), str(random.randint(1, 28))
            month = month if (len(month)==2) else "0"+month
            day = day if (len(day)==2) else "0"+day
            await ctx.send(file=discord.File(
                self.canvas.gif2png(
                    "https://d1ejxu6vysztl5.cloudfront.net/comics/garfield/{}/{}-{}-{}.gif".format(
                        year, year, month, day
                    )
                ), "garfield.png"
            ))
        except:
            await ctx.send("{} | Ooops! We cannot find the image. Please try again.".format(
                str(self.client.get_emoji(BotEmotes.error))
            ))

    @command()
    @cooldown(5)
    async def lucario(self, ctx):
        embed = discord.Embed(title='Lucario!', color=discord.Color.from_rgb(201, 160, 112))
        embed.set_image(url=myself.jsonisp('http://pics.floofybot.moe/image?token=lucario&category=sfw')['image'])
        await ctx.send(embed=embed)
    
    @command('ducks,quack,duk')
    @cooldown(5)
    async def duck(self, ctx):
        await ctx.send(file=discord.File(self.canvas.urltoimage(myself.jsonisp('https://random-d.uk/api/v2/random?format=json')['url']), 'duck.png'))

    @command('snek,snakes,python,py')
    @cooldown(5)
    async def snake(self, ctx):
        await ctx.send(file=discord.File(self.canvas.urltoimage('https://fur.im/snek/i/'+str(random.randint(1, 874))+'.png'), 'snek.png'))

    @command('imageoftheday')
    @cooldown(21600)
    async def iotd(self, ctx):
        data = myself.jsonisp('https://www.bing.com/HPImageArchive.aspx?format=js&idx=0&n=1&mkt=en-US')['images'][0]
        embed = discord.Embed( title=data['copyright'], url=data['copyrightlink'], color=discord.Color.from_rgb(201, 160, 112))
        embed.set_image(url='https://bing.com'+data['url'])
        await ctx.send(embed=embed)

    @command()
    @cooldown(5)
    async def httpcat(self, ctx, *args):
        code = list(args)[0] if (len(list(args))!=0) else '404'
        await ctx.send(file=discord.File(self.canvas.urltoimage('https://http.cat/'+str(code)+'.jpg'), 'httpcat.png'))
    
    @command('httpduck')
    @cooldown(5)
    async def httpdog(self, ctx, *args):
        code = list(args)[0] if (len(list(args))!=0) else '404'
        url = 'https://random-d.uk/api/http/ABC.jpg' if ('duck' in ctx.message.content) else 'https://httpstatusdogs.com/img/ABC.jpg'
        try:
            await ctx.send(file=discord.File(
                self.canvas.urltoimage(url.replace('ABC', code)), 'httpdogduck.png'
            ))
        except:
            await ctx.send('{} | 404'.format(
                str(self.client.get_emoji(BotEmotes.error))
            ))

    @command()
    @cooldown(5)
    async def goat(self, ctx):
        await ctx.send(file=discord.File(self.canvas.urltoimage('https://placegoat.com/'+str(random.randint(500, 700))), 'goat.png'))

    @command()
    @cooldown(5)
    async def rotate(self, ctx, *args):
        async with ctx.message.channel.typing():
            ava = myself.getUserAvatar(ctx, args, size=512)
            data = self.gif.rotate(ava)
            await ctx.send(file=discord.File(data, 'rotate.gif'))

    @command()
    @cooldown(5)
    async def resize(self, ctx, *args):
        correct, wh = '', []
        for i in list(args):
            if i.isnumeric():
                correct += 'y'
                wh.append(int(i))
        async with ctx.message.channel.typing():
            if correct=='yy':
                ava = myself.getUserAvatar(ctx, args, size=512)
                if wh[0]>2000 or wh[1]>2000: await ctx.send(str(self.client.get_emoji(BotEmotes.error)) + " | Your image is too big!")
                elif wh[0]<300 or wh[1]<300: await ctx.send(str(self.client.get_emoji(BotEmotes.error)) + " | Your image is too small!")
                else:
                    data = self.canvas.resize(ava, wh[0], wh[1])
                    await ctx.send(file=discord.File(data, 'resize.png'))
            else:
                await ctx.send(str(self.client.get_emoji(BotEmotes.error)) + " | Where are the parameters?")

    @command()
    @cooldown(10)
    async def nature(self, ctx):
        async with ctx.message.channel.typing():
            await ctx.send(file=discord.File(self.canvas.urltoimage('https://source.unsplash.com./1600x900/?nature'), 'nature.png'))

    @command('earth,moon')
    @cooldown(10)
    async def space(self, ctx):
        async with ctx.message.channel.typing():
            await ctx.send(file=discord.File(self.canvas.urltoimage('https://source.unsplash.com./1600x900/?{}'.format(random.choice(['earth', 'moon', 'space']))), 'space.png'))

    @command()
    @cooldown(5)
    async def ytthumbnail(self, ctx, *args):
        if len(list(args))!=0:
            videoid = 'dQw4w9WgXcQ'
            async with ctx.message.channel.typing():
                args = tuple(
                    ',,'.join(list(args)).replace('<', '').replace('>', '').split(',,')
                )
                if list(args)[0].endswith('/'): list(args)[0] = list(args)[0][:-1]
                if 'https://' in list(args)[0]: list(args)[0] = list(args)[0].replace('https://', '')
                elif 'http://' in list(args)[0]: list(args)[0] = list(args)[0].replace('http://', '')
                if '/watch?v=' in list(args)[0]: videoid = list(args)[0].split('/watch?v=')[1]
                else: videoid = list(args)[0].split('/')[1]
                url = 'https://img.youtube.com/vi/'+str(videoid)+'/mqdefault.jpg'
                data = self.canvas.urltoimage(url)
                await ctx.send(file=discord.File(data, 'thumbnail.png'))
        else: await ctx.send(str(self.client.get_emoji(BotEmotes.error))+' | gimme something to work with! Like a youtube url!')
    @command('cat,fox,sadcat,bird')
    @cooldown(5)
    async def dog(self, ctx):
        async with ctx.message.channel.typing():
            links = {
                "dog": "https://api.alexflipnote.dev/dogs|file",
                "cat": "https://api.alexflipnote.dev/cats|file",
                "sadcat": "https://api.alexflipnote.dev/sadcat|file",
                "bird": "https://api.alexflipnote.dev/sadcat|file",
                "fox": 'https://randomfox.ca/floof/?ref=apilist.fun|image'
            }
            for i in list(links.keys()):
                if str(ctx.message.content[1:]).lower().replace(' ', '')==i: link = links[i] ; break
            apiied = myself.jsonisp(link.split('|')[0])[link.split('|')[1]]
            data = self.canvas.urltoimage(apiied)
            await ctx.send(file=discord.File(data, 'animal.png'))

    @command()
    @cooldown(5)
    async def panda(self, ctx):
        link, col, msg = random.choice(["https://some-random-api.ml/img/panda", "https://some-random-api.ml/img/red_panda"]), discord.Colour.from_rgb(201, 160, 112), 'Here is some cute pics of pandas.'
        data = myself.jsonisp(link)['link']
        embed = discord.Embed(title=msg, color=col)
        embed.set_image(url=data)
        await ctx.send(embed=embed)
    
    @command()
    @cooldown(5)
    async def shibe(self, ctx):
        async with ctx.message.channel.typing():
            data = myself.jsonisp("http://shibe.online/api/shibes?count=1")[0]
            await ctx.send(file=discord.File(self.canvas.smallURL(data), 'shibe.png'))
    
    @command()
    @cooldown(5)
    async def ship(self, ctx):
        async with ctx.message.channel.typing():
            if len(ctx.message.mentions)!=2:
                first, second = str(ctx.message.author.avatar_url).replace('webp', 'png'), str(random.choice(i.avatar_url for i in ctx.message.guild.members).replace('webp', 'png'))
            else:
                first, second = str(ctx.message.mentions[0].avatar_url).replace('webp', 'png'), str(ctx.message.mentions[1].avatar_url).replace('webp', 'png')
            url = f'https://api.alexflipnote.dev/ship?user={first}&user2={second}'
            await ctx.send(file=discord.File(self.canvas.urltoimage(url), 'ship.png'))

    @command('coffee')
    @cooldown(5)
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
                data = self.canvas.urltoimage(link.replace('\/', '/'))
                await ctx.send(file=discord.File(data, ctx.message.content[1:]+'.png'))

    @command()
    @cooldown(5)
    async def magik(self, ctx, *args):
        source = myself.getUserAvatar(ctx, args)
        await ctx.message.channel.trigger_typing()
        await ctx.send(file=discord.File(
            self.canvas.urltoimage(f'https://nekobot.xyz/api/imagegen?type=magik&image={source}&raw=1&intensity={random.randint(5, 10)}'), 'magik.png'
        ))

    @command('invert,pixelate,b&w')
    @cooldown(5)
    async def jpeg(self, ctx, *args):
        com = str(ctx.message.content).split()[0].replace('jpeg', 'jpegify')[1:]
        source = myself.getUserAvatar(ctx, args)
        await ctx.message.channel.trigger_typing()
        await ctx.send(file=discord.File(
            self.canvas.urltoimage(f'https://nekobot.xyz/api/imagegen?type=magik&image={source}&raw=1&intensity={random.randint(5, 10)}'), 'magik.png'
        ))
def setup(client):
    client.add_cog(image(client))
