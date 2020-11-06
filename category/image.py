import discord
from discord.ext import commands
import sys
from requests import get
from os import getcwd, name, environ
sys.path.append(environ['BOT_MODULES_DIR'])
from decorators import command, cooldown
import random
from io import BytesIO
from aiohttp import ClientSession

class image(commands.Cog):
    def __init__(self, client):
        pass

    async def plode_animated(self, ctx, args, command_name):
        wait = await ctx.send(f"{ctx.bot.loading_emoji} | Please wait... this may take a few seconds.")
        url = ctx.bot.utils.getUserAvatar(ctx, args, size=128)
        data = get(f"https://useless-api.vierofernando.repl.co/{command_name}/animated?image={url}", headers={'superdupersecretkey': environ['USELESSAPI']}).content
        await wait.delete()
        await ctx.send(file=discord.File(BytesIO(data), 'brrr.gif'))

    @command('explode')
    @cooldown(9)
    async def implode(self, ctx, *args):
        command_name = ctx.message.content.split()[0][1:].lower()
        if ("--animated" in args):
            return await self.plode_animated(ctx, args, command_name)

        async with ctx.channel.typing():
            amount = "1" if ("implode" in command_name)  else "-3.5"
            url = ctx.bot.utils.getUserAvatar(ctx, args)
            return await ctx.send(file=discord.File(ctx.bot.canvas.urltoimage(f"https://useless-api.vierofernando.repl.co/implode?image={url}&amount={amount}"), "boom.png"))

    @command('spread,emboss,edge,sketch,swirl,wave')
    @cooldown(8)
    async def charcoal(self, ctx, *args):
        async with ctx.channel.typing():
            command_name = ctx.message.content.split()[0][1:].lower()
            url = ctx.bot.utils.getUserAvatar(ctx, args)
            return await ctx.send(file=discord.File(ctx.bot.canvas.urltoimage(f"https://useless-api.vierofernando.repl.co/{command_name}?image={url}"), "image.png"))    

    @command('combine')
    @cooldown(2)
    async def blend(self, ctx, *args):
        if len(args) == 0: raise ctx.bot.utils.send_error_message("Please input a parameter or something")
        async with ctx.channel.typing():
            parsed_args = ctx.bot.utils.split_parameter_to_two(args)
            if parsed_args is None: 
                first, second = ctx.author.avatar_url_as(format='png'), ctx.bot.utils.getUserAvatar(ctx, args)
            else: first, second = ctx.bot.utils.getUserAvatar(ctx, parsed_args[0]), ctx.bot.utils.getUserAvatar(ctx, parsed_args[1])
            return await ctx.send(file=discord.File(ctx.bot.canvas.blend(first, second), 'blend.png'))
            
    @command('pika')
    @cooldown(2)
    async def pikachu(self, ctx):
        async with ctx.channel.typing():
            async with ctx.bot.bot_session.get(ctx.bot.utils.fetchJSON('https://some-random-api.ml/img/pikachu')['link']) as r:
                res = await r.read()
                await ctx.send(file=discord.File(fp=BytesIO(res), filename="pikachu.gif"))

    @command()
    @cooldown(1)
    async def blur(self, ctx, *args):
        ava = ctx.bot.utils.getUserAvatar(ctx, args, size=512)
        async with ctx.channel.typing():
            im = ctx.bot.canvas.blur(ava)
            await ctx.send(file=discord.File(im, 'blur.png'))

    @command('glitchify,matrix')
    @cooldown(5)
    async def glitch(self, ctx, *args):
        ava = ctx.bot.utils.getUserAvatar(ctx, args, size=128)
        async with ctx.channel.typing():
            im = BytesIO(get("https://useless-api.vierofernando.repl.co/glitch/noratelimit?image="+ava, headers={'token': environ["USELESSAPI"]}).content)
            await ctx.send(file=discord.File(im, 'glitch.png'))

    @command('destroy,destroyava,destroyavatar')
    @cooldown(1)
    async def destroyimg(self, ctx, *args):
        src = ctx.bot.utils.getUserAvatar(ctx, args, size=512)
        async with ctx.channel.typing():
            await ctx.send(file=discord.File(
                ctx.bot.canvas.ruin(src), 'ruinedavatar.png'
            ))

    @command('distortion')
    @cooldown(1)
    async def distort(self, ctx, *args, blacklist=None):
        user, num = ctx.bot.utils.split_parameter_to_two(args)
        if not num.isnumeric(): num = 5
        elif int(num) not in range(999): raise ctx.bot.utils.send_error_message("damn that level is hella weirdd")
        ava = ctx.bot.utils.getUserAvatar(ctx, (user,))
        async with ctx.channel.typing():
            await ctx.send(file=discord.File(
                ctx.bot.canvas.urltoimage('https://nezumiyuiz.glitch.me/api/distort?level={}&image={}'.format(
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
                ctx.bot.canvas.gif2png(
                    "https://d1ejxu6vysztl5.cloudfront.net/comics/garfield/{}/{}-{}-{}.gif".format(
                        year, year, month, day
                    )
                ), "garfield.png"
            ))
        except:
            raise ctx.bot.utils.send_error_message("Ooops! We cannot find the image. Please try again.")

    @command()
    @cooldown(1)
    async def lucario(self, ctx):
        embed = discord.Embed(title='Lucario!', color=ctx.guild.me.roles[::-1][0].color)
        embed.set_image(url=ctx.bot.utils.fetchJSON('http://pics.floofybot.moe/image?token=lucario&category=sfw')['image'])
        await ctx.send(embed=embed)
    
    @command('ducks,quack,duk')
    @cooldown(1)
    async def duck(self, ctx):
        await ctx.send(file=discord.File(ctx.bot.canvas.urltoimage(ctx.bot.utils.fetchJSON('https://random-d.uk/api/v2/random?format=json')['url']), 'duck.png'))

    @command('snek,snakes,python,py')
    @cooldown(1)
    async def snake(self, ctx):
        await ctx.send(file=discord.File(ctx.bot.canvas.urltoimage('https://fur.im/snek/i/'+str(random.randint(1, 874))+'.png'), 'snek.png'))

    @command('imageoftheday')
    @cooldown(21600)
    async def iotd(self, ctx):
        data = ctx.bot.utils.fetchJSON('https://www.bing.com/HPImageArchive.aspx?format=js&idx=0&n=1&mkt=en-US')['images'][0]
        embed = discord.Embed( title=data['copyright'], url=data['copyrightlink'], color=ctx.guild.me.roles[::-1][0].color)
        embed.set_image(url='https://bing.com'+data['url'])
        await ctx.send(embed=embed)

    @command()
    @cooldown(1)
    async def httpcat(self, ctx, *args):
        code = args[0] if (len(args)!=0) else '404'
        await ctx.send(file=discord.File(ctx.bot.canvas.urltoimage('https://http.cat/'+str(code)+'.jpg'), 'httpcat.png'))
    
    @command('httpduck')
    @cooldown(1)
    async def httpdog(self, ctx, *args):
        code = args[0] if (len(args)!=0) else '404'
        url = 'https://random-d.uk/api/http/ABC.jpg' if ('duck' in ctx.message.content) else 'https://httpstatusdogs.com/img/ABC.jpg'
        try:
            await ctx.send(file=discord.File(
                ctx.bot.canvas.urltoimage(url.replace('ABC', code)), 'httpdogduck.png'
            ))
        except:
            raise ctx.bot.utils.send_error_message("404")

    @command()
    @cooldown(1)
    async def goat(self, ctx):
        await ctx.send(file=discord.File(ctx.bot.canvas.urltoimage('https://placegoat.com/'+str(random.randint(500, 700))), 'goat.png'))

    @command()
    @cooldown(1)
    async def rotate(self, ctx, *args):
        async with ctx.channel.typing():
            ava = ctx.bot.utils.getUserAvatar(ctx, args, size=512)
            data = ctx.bot.gif.rotate(ava)
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
                ava = ctx.bot.utils.getUserAvatar(ctx, args, size=512)
                if wh[0]>2000 or wh[1]>2000: raise ctx.bot.utils.send_error_message("Your image is too big!")
                elif wh[0]<300 or wh[1]<300: raise ctx.bot.utils.send_error_message("Your image is too small!")
                else:
                    data = ctx.bot.canvas.resize(ava, wh[0], wh[1])
                    await ctx.send(file=discord.File(data, 'resize.png'))
            else:
                raise ctx.bot.utils.send_error_message("Where are the parameters?")

    @command()
    @cooldown(10)
    async def nature(self, ctx):
        async with ctx.channel.typing():
            await ctx.send(file=discord.File(ctx.bot.canvas.urltoimage('https://source.unsplash.com./1600x900/?nature'), 'nature.png'))

    @command('earth,moon')
    @cooldown(10)
    async def space(self, ctx):
        async with ctx.channel.typing():
            await ctx.send(file=discord.File(ctx.bot.canvas.urltoimage('https://source.unsplash.com./1600x900/?{}'.format(random.choice(['earth', 'moon', 'space']))), 'space.png'))

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
            apiied = ctx.bot.utils.fetchJSON(link.split('|')[0])[link.split('|')[1]]
            data = ctx.bot.canvas.urltoimage(apiied)
            await ctx.send(file=discord.File(data, 'animal.png'))

    @command()
    @cooldown(1)
    async def panda(self, ctx):
        link, col, msg = random.choice(["https://some-random-api.ml/img/panda", "https://some-random-api.ml/img/red_panda"]), ctx.guild.me.roles[::-1][0].color, 'Here is some cute pics of pandas.'
        data = ctx.bot.utils.fetchJSON(link)['link']
        embed = discord.Embed(title=msg, color=col)
        embed.set_image(url=data)
        await ctx.send(embed=embed)
    
    @command()
    @cooldown(1)
    async def shibe(self, ctx):
        async with ctx.channel.typing():
            data = ctx.bot.utils.fetchJSON("http://shibe.online/api/shibes?count=1")[0]
            await ctx.send(file=discord.File(ctx.bot.canvas.smallURL(data), 'shibe.png'))
    
    @command()
    @cooldown(1)
    async def ship(self, ctx, *args):
        if len(args) == 0: raise ctx.bot.utils.send_error_message("Please input a parameter or something")
        async with ctx.channel.typing():
            parsed_args = ctx.bot.utils.split_parameter_to_two(args)
            if parsed_args is None: 
                first, second = ctx.author.avatar_url_as(format='png'), ctx.bot.utils.getUserAvatar(ctx, args)
            else: first, second = ctx.bot.utils.getUserAvatar(ctx, parsed_args[0]), ctx.bot.utils.getUserAvatar(ctx, parsed_args[1])
            url = f'https://api.alexflipnote.dev/ship?user={first}&user2={second}'
            await ctx.send(file=discord.File(ctx.bot.canvas.urltoimage(url), 'ship.png'))

    @command('coffee')
    @cooldown(1)
    async def food(self, ctx, *args):
        if len(args)==0:
            data = ctx.bot.utils.fetchJSON('https://nekobot.xyz/api/image?type='+str(ctx.message.content[1:]))
            link = data['message'].replace('\/', '/')
            if 'food' in ctx.message.content:
                col = int(data['color'])
            elif 'coffee' in ctx.message.content:
                col, num = int(data['color']), random.randint(0, 1)
                if num==0: link = ctx.bot.utils.fetchJSON('https://coffee.alexflipnote.dev/random.json')['file']
                else: link = ctx.bot.utils.fetchJSON('https://nekobot.xyz/api/image?type=coffee')['message'].replace('\/', '/')
            async with ctx.channel.typing():
                data = ctx.bot.canvas.urltoimage(link.replace('\/', '/'))
                await ctx.send(file=discord.File(data, ctx.message.content[1:]+'.png'))

    @command()
    @cooldown(1)
    async def magik(self, ctx, *args):
        source = ctx.bot.utils.getUserAvatar(ctx, args)
        await ctx.channel.trigger_typing()
        await ctx.send(file=discord.File(
            ctx.bot.canvas.urltoimage(f'https://nekobot.xyz/api/imagegen?type=magik&image={source}&raw=1'), 'magik.png'
        ))

    @command()
    @cooldown(1)
    async def invert(self, ctx, *args):
        av = ctx.bot.utils.getUserAvatar(ctx, args)
        return await ctx.send(file=discord.File(ctx.bot.canvas.invert_image(av), 'invert.png'))
        
    @command('grayscale,b&w,bw,classic')
    @cooldown(1)
    async def blackandwhite(self, ctx, *args):
        av = ctx.bot.utils.getUserAvatar(ctx, args)
        return await ctx.send(file=discord.File(ctx.bot.canvas.grayscale(av), 'invert.png'))

    @command('pixelate')
    @cooldown(5)
    async def jpeg(self, ctx, *args):
        async with ctx.channel.typing():
            url = {"jpeg": "https://api.alexflipnote.dev/filter/jpegify?image=<URL>", "pixelate": "https://useless-api.vierofernando.repl.co/pixelate?image=<URL>&amount=<NUM>"}
            command_name = ctx.message.content.split()[0][1:].lower()
            avatar = ctx.bot.utils.getUserAvatar(ctx, args)
            url = url[command_name].replace("<URL>", avatar).replace("<NUM>", random.choice(["16", "32"]))
            return await ctx.send(file=discord.File(ctx.bot.canvas.urltoimage(url), "image.png"))

def setup(client):
    client.add_cog(image(client))
