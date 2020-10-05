import discord
from discord.ext import commands
import sys
from os import getcwd, name, environ
sys.path.append(environ['BOT_MODULES_DIR'])
from decorators import command, cooldown
import random
from io import BytesIO
from aiohttp import ClientSession

class image(commands.Cog):
    def __init__(self, client):
        self.client = client
        self.session = ClientSession()

    @command('pika')
    @cooldown(2)
    async def pikachu(self, ctx):
        async with ctx.channel.typing():
            async with self.session.get(self.client.utils.fetchJSON('https://some-random-api.ml/img/pikachu')['link']) as r:
                res = await r.read()
                await ctx.send(file=discord.File(fp=BytesIO(res), filename="pikachu.gif"))

    @command()
    @cooldown(1)
    async def blur(self, ctx, *args):
        ava = self.client.utils.getUserAvatar(ctx, args, size=512)
        async with ctx.channel.typing():
            im = self.client.canvas.blur(ava)
            await ctx.send(file=discord.File(im, 'blur.png'))

    @command('glitchify,matrix')
    @cooldown(1)
    async def glitch(self, ctx, *args):
        ava = self.client.utils.getUserAvatar(ctx, args, size=512)
        async with ctx.channel.typing():
            im = self.client.canvas.glitch(ava)
            await ctx.send(file=discord.File(im, 'glitch.png'))

    @command('destroy,destroyava,destroyavatar')
    @cooldown(1)
    async def destroyimg(self, ctx, *args):
        src = self.client.utils.getUserAvatar(ctx, args, size=512)
        async with ctx.channel.typing():
            await ctx.send(file=discord.File(
                self.client.canvas.ruin(src), 'ruinedavatar.png'
            ))

    @command('distortion')
    @cooldown(1)
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
                self.client.error_emoji
            ))
        ava = self.client.utils.getUserAvatar(ctx, args)
        async with ctx.channel.typing():
            await ctx.send(file=discord.File(
                self.client.canvas.urltoimage('https://nezumiyuiz.glitch.me/api/distort?level={}&image={}'.format(
                    str(num), str(ava)
                )), 'distort.png'
            ))

    @command()
    @cooldown(1)
    async def garfield(self, ctx):
        try:
            year, month, day = str(random.randint(1979, 2019)), str(random.randint(1, 12)), str(random.randint(1, 28))
            month = month if (len(month)==2) else "0"+month
            day = day if (len(day)==2) else "0"+day
            await ctx.send(file=discord.File(
                self.client.canvas.gif2png(
                    "https://d1ejxu6vysztl5.cloudfront.net/comics/garfield/{}/{}-{}-{}.gif".format(
                        year, year, month, day
                    )
                ), "garfield.png"
            ))
        except:
            await ctx.send("{} | Ooops! We cannot find the image. Please try again.".format(
                self.client.error_emoji
            ))

    @command()
    @cooldown(1)
    async def lucario(self, ctx):
        embed = discord.Embed(title='Lucario!', color=self.client.utils.get_embed_color())
        embed.set_image(url=self.client.utils.fetchJSON('http://pics.floofybot.moe/image?token=lucario&category=sfw')['image'])
        await ctx.send(embed=embed)
    
    @command('ducks,quack,duk')
    @cooldown(1)
    async def duck(self, ctx):
        await ctx.send(file=discord.File(self.client.canvas.urltoimage(self.client.utils.fetchJSON('https://random-d.uk/api/v2/random?format=json')['url']), 'duck.png'))

    @command('snek,snakes,python,py')
    @cooldown(1)
    async def snake(self, ctx):
        await ctx.send(file=discord.File(self.client.canvas.urltoimage('https://fur.im/snek/i/'+str(random.randint(1, 874))+'.png'), 'snek.png'))

    @command('imageoftheday')
    @cooldown(21600)
    async def iotd(self, ctx):
        data = self.client.utils.fetchJSON('https://www.bing.com/HPImageArchive.aspx?format=js&idx=0&n=1&mkt=en-US')['images'][0]
        embed = discord.Embed( title=data['copyright'], url=data['copyrightlink'], color=self.client.utils.get_embed_color())
        embed.set_image(url='https://bing.com'+data['url'])
        await ctx.send(embed=embed)

    @command()
    @cooldown(1)
    async def httpcat(self, ctx, *args):
        code = list(args)[0] if (len(list(args))!=0) else '404'
        await ctx.send(file=discord.File(self.client.canvas.urltoimage('https://http.cat/'+str(code)+'.jpg'), 'httpcat.png'))
    
    @command('httpduck')
    @cooldown(1)
    async def httpdog(self, ctx, *args):
        code = list(args)[0] if (len(list(args))!=0) else '404'
        url = 'https://random-d.uk/api/http/ABC.jpg' if ('duck' in ctx.message.content) else 'https://httpstatusdogs.com/img/ABC.jpg'
        try:
            await ctx.send(file=discord.File(
                self.client.canvas.urltoimage(url.replace('ABC', code)), 'httpdogduck.png'
            ))
        except:
            await ctx.send('{} | 404'.format(
                self.client.error_emoji
            ))

    @command()
    @cooldown(1)
    async def goat(self, ctx):
        await ctx.send(file=discord.File(self.client.canvas.urltoimage('https://placegoat.com/'+str(random.randint(500, 700))), 'goat.png'))

    @command()
    @cooldown(1)
    async def rotate(self, ctx, *args):
        async with ctx.channel.typing():
            ava = self.client.utils.getUserAvatar(ctx, args, size=512)
            data = self.client.gif.rotate(ava)
            await ctx.send(file=discord.File(data, 'rotate.gif'))

    @command()
    @cooldown(1)
    async def resize(self, ctx, *args):
        correct, wh = '', []
        for i in list(args):
            if i.isnumeric():
                correct += 'y'
                wh.append(int(i))
        async with ctx.channel.typing():
            if correct=='yy':
                ava = self.client.utils.getUserAvatar(ctx, args, size=512)
                if wh[0]>2000 or wh[1]>2000: await ctx.send(self.client.error_emoji + " | Your image is too big!")
                elif wh[0]<300 or wh[1]<300: await ctx.send(self.client.error_emoji + " | Your image is too small!")
                else:
                    data = self.client.canvas.resize(ava, wh[0], wh[1])
                    await ctx.send(file=discord.File(data, 'resize.png'))
            else:
                await ctx.send(self.client.error_emoji + " | Where are the parameters?")

    @command()
    @cooldown(10)
    async def nature(self, ctx):
        async with ctx.channel.typing():
            await ctx.send(file=discord.File(self.client.canvas.urltoimage('https://source.unsplash.com./1600x900/?nature'), 'nature.png'))

    @command('earth,moon')
    @cooldown(10)
    async def space(self, ctx):
        async with ctx.channel.typing():
            await ctx.send(file=discord.File(self.client.canvas.urltoimage('https://source.unsplash.com./1600x900/?{}'.format(random.choice(['earth', 'moon', 'space']))), 'space.png'))

    @command('cat,fox,sadcat,bird')
    @cooldown(1)
    async def dog(self, ctx):
        async with ctx.channel.typing():
            links = {
                "dog": "https://api.alexflipnote.dev/dogs|file",
                "cat": "https://api.alexflipnote.dev/cats|file",
                "sadcat": "https://api.alexflipnote.dev/sadcat|file",
                "bird": "https://api.alexflipnote.dev/sadcat|file",
                "fox": 'https://randomfox.ca/floof/?ref=apilist.fun|image'
            }
            for i in list(links.keys()):
                if str(ctx.message.content[1:]).lower().replace(' ', '')==i: link = links[i] ; break
            apiied = self.client.utils.fetchJSON(link.split('|')[0])[link.split('|')[1]]
            data = self.client.canvas.urltoimage(apiied)
            await ctx.send(file=discord.File(data, 'animal.png'))

    @command()
    @cooldown(1)
    async def panda(self, ctx):
        link, col, msg = random.choice(["https://some-random-api.ml/img/panda", "https://some-random-api.ml/img/red_panda"]), self.client.utils.get_embed_color(), 'Here is some cute pics of pandas.'
        data = self.client.utils.fetchJSON(link)['link']
        embed = discord.Embed(title=msg, color=col)
        embed.set_image(url=data)
        await ctx.send(embed=embed)
    
    @command()
    @cooldown(1)
    async def shibe(self, ctx):
        async with ctx.channel.typing():
            data = self.client.utils.fetchJSON("http://shibe.online/api/shibes?count=1")[0]
            await ctx.send(file=discord.File(self.client.canvas.smallURL(data), 'shibe.png'))
    
    @command()
    @cooldown(1)
    async def ship(self, ctx, *args):
        if len(args) == 0: return await ctx.send("{} | Please input a parameter or something".format(self.client.error_emoji))
        async with ctx.channel.typing():
            parsed_args = self.client.utils.split_parameter_to_two(args)
            print(parsed_args)
            if parsed_args == None: 
                first, second = ctx.author.avatar_url_as(format='png'), self.client.utils.getUserAvatar(ctx, args)
            else: first, second = self.client.utils.getUserAvatar(ctx, parsed_args[0]), self.client.utils.getUserAvatar(ctx, parsed_args[1])
            print(first, second)
            url = f'https://api.alexflipnote.dev/ship?user={first}&user2={second}'
            await ctx.send(file=discord.File(self.client.canvas.urltoimage(url), 'ship.png'))

    @command('coffee')
    @cooldown(1)
    async def food(self, ctx, *args):
        if len(list(args))==0:
            data = self.client.utils.fetchJSON('https://nekobot.xyz/api/image?type='+str(ctx.message.content[1:]))
            link = data['message'].replace('\/', '/')
            if 'food' in ctx.message.content:
                col = int(data['color'])
            elif 'coffee' in ctx.message.content:
                col, num = int(data['color']), random.randint(0, 1)
                if num==0: link = self.client.utils.fetchJSON('https://coffee.alexflipnote.dev/random.json')['file']
                else: link = self.client.utils.fetchJSON('https://nekobot.xyz/api/image?type=coffee')['message'].replace('\/', '/')
            async with ctx.channel.typing():
                data = self.client.canvas.urltoimage(link.replace('\/', '/'))
                await ctx.send(file=discord.File(data, ctx.message.content[1:]+'.png'))

    @command()
    @cooldown(1)
    async def magik(self, ctx, *args):
        source = self.client.utils.getUserAvatar(ctx, args)
        await ctx.channel.trigger_typing()
        await ctx.send(file=discord.File(
            self.client.canvas.urltoimage(f'https://nekobot.xyz/api/imagegen?type=magik&image={source}&raw=1&intensity={random.randint(5, 10)}'), 'magik.png'
        ))

    @command()
    @cooldown(1)
    async def invert(self, ctx, *args):
        av = self.client.utils.getUserAvatar(ctx, args)
        return await ctx.send(file=discord.File(self.client.canvas.invert_image(av), 'invert.png'))
        
    @command('grayscale,b&w,bw,classic')
    @cooldown(1)
    async def blackandwhite(self, ctx, *args):
        av = self.client.utils.getUserAvatar(ctx, args)
        return await ctx.send(file=discord.File(self.client.canvas.grayscale(av), 'invert.png'))

    @command('pixelate')
    @cooldown(1)
    async def jpeg(self, ctx, *args):
        com = str(ctx.message.content).split()[0].replace('jpeg', 'jpegify')[1:]
        source = self.client.utils.getUserAvatar(ctx, args)
        await ctx.channel.trigger_typing()
        await ctx.send(file=discord.File(
            self.client.canvas.urltoimage(f'https://nekobot.xyz/api/imagegen?type={com.lower()}&image={source}&raw=1'), 'lmao-nice.png'
        ))
def setup(client):
    client.add_cog(image(client))
