import discord
from discord.ext import commands
from decorators import *
import random
from io import BytesIO
from aiohttp import ClientSession

class image(commands.Cog):
    def __init__(self):
        self._links = {
            "dog": "https://api.alexflipnote.dev/dogs|file",
            "cat": "https://api.alexflipnote.dev/cats|file",
            "sadcat": "https://api.alexflipnote.dev/sadcat|file",
            "bird": "https://api.alexflipnote.dev/sadcat|file",
            "fox": 'https://randomfox.ca/floof/?ref=apilist.fun|image'
        }

    @command(['explode'])
    @cooldown(9)
    async def implode(self, ctx, *args):
        await ctx.trigger_typing()
        command_name = ctx.bot.util.get_command_name(ctx)
        url = await ctx.bot.Parser.parse_image(ctx, args)
        if ("--animated" in args):
            return await ctx.bot.util.send_image_attachment(ctx, f"https://useless-api.vierofernando.repl.co/{command_name}/animated?image={url}", uselessapi=True)
        amount = "1" if (command_name == "implode") else "-3.5"
        return await ctx.bot.util.send_image_attachment(ctx, f"https://useless-api.vierofernando.repl.co/implode?image={url}&amount={amount}")

    @command(['spread', 'emboss', 'edge', 'sketch', 'swirl', 'wave'])
    @cooldown(8)
    async def charcoal(self, ctx, *args):
        await ctx.trigger_typing()
        command_name = ctx.bot.util.get_command_name(ctx)
        url = await ctx.bot.Parser.parse_image(ctx, args)
        return await ctx.bot.util.send_image_attachment(ctx, f"https://useless-api.vierofernando.repl.co/{command_name}?image={url}")

    @command(['combine'])
    @cooldown(2)
    @require_args()
    async def blend(self, ctx, *args):
        await ctx.trigger_typing()
        parsed_args = ctx.bot.Parser.split_args(args)
        if parsed_args is None: 
            first, second = ctx.author.avatar_url_as(format='png'), await ctx.bot.Parser.parse_image(ctx, args)
        else: first, second = await ctx.bot.Parser.parse_image(ctx, (parsed_args[0],)), await ctx.bot.Parser.parse_image(ctx, (parsed_args[1],))
        blended = await ctx.bot.canvas.blend(first, second)
        return await ctx.send(file=discord.File(blended, 'blend.png'))
            
    @command(['pika'])
    @cooldown(2)
    async def pikachu(self, ctx):
        await ctx.trigger_typing()
        link = await ctx.bot.util.get_request('https://some-random-api.ml/img/pikachu', json=True, raise_errors=True)
        return await ctx.bot.util.send_image_attachment(ctx, link['link'])

    @command()
    @cooldown(2)
    async def blur(self, ctx, *args):
        ava = await ctx.bot.Parser.parse_image(ctx, args, size=512)
        await ctx.trigger_typing()
        im = await ctx.bot.canvas.blur(ava)
        await ctx.send(file=discord.File(im, 'blur.png'))

    @command(['glitchify', 'matrix'])
    @cooldown(5)
    async def glitch(self, ctx, *args):
        ava = await ctx.bot.Parser.parse_image(ctx, args, size=128)
        await ctx.trigger_typing()
        return await ctx.bot.util.send_image_attachment(ctx, "https://useless-api.vierofernando.repl.co/glitch/noratelimit?image=" + ava, uselessapi=True)

    @command()
    @cooldown(2)
    async def lucario(self, ctx):
        url = await ctx.bot.util.get_request(
            "http://pics.floofybot.moe/image",
            token="lucario",
            category="sfw",
            json=True,
            raise_errors=True
        )
    
        embed = discord.Embed(title='Here\'s a pic of Lucario.', color=ctx.me.color)
        embed.set_image(url=url)
        await ctx.send(embed=embed)
    
    @command(['ducks', 'quack', 'duk'])
    @cooldown(2)
    async def duck(self, ctx):
        _url = await ctx.bot.util.get_request(
            'https://random-d.uk/api/v2/random',
            format='json',
            json=True,
            raise_errors=True
        )
        await ctx.bot.util.send_image_attachment(ctx, _url)

    @command(['snek', 'snakes', 'python', 'py'])
    @cooldown(2)
    async def snake(self, ctx):
        return await ctx.bot.util.send_image_attachment(ctx, 'https://fur.im/snek/i/'+str(random.randint(1, 874))+'.png')

    @command(['imageoftheday'])
    @cooldown(10)
    async def iotd(self, ctx):
        try:
            data = await ctx.bot.util.get_request(
                'https://www.bing.com/HPImageArchive.aspx',
                json=True,
                raise_errors=True,
                format='ks',
                idx=0,
                n=1,
                mkt='en-US'
            )
        except:
            raise ctx.bot.util.BasicCommandException("The API may be down for a while. Try again later!")
        embed = discord.Embed(title=data['copyright'], url=data['copyrightlink'], color=ctx.me.color)
        embed.set_image(url='https://bing.com'+data['images'][0]['url'])
        await ctx.send(embed=embed)

    @command()
    @cooldown(2)
    async def httpcat(self, ctx, *args):
        code = args[0] if (len(args)!=0) or (not args[0].isnumeric()) else '404'
        return await ctx.bot.util.send_image_attachment(ctx, 'https://http.cat/'+str(code)+'.jpg')
    
    @command(['httpduck'])
    @cooldown(2)
    async def httpdog(self, ctx, *args):
        code = args[0] if ((len(args)!=0) or (args[0].isnumeric())) else '404'
        url = 'https://random-d.uk/api/http/ABC.jpg' if (ctx.bot.util.get_command_name(ctx) == "httpduck") else 'https://httpstatusdogs.com/img/ABC.jpg'
        try:
            return await ctx.bot.util.send_image_attachment(ctx, url.replace('ABC', code))
        except:
            raise ctx.bot.util.BasicCommandException("404")

    @command()
    @cooldown(2)
    async def goat(self, ctx):
        return await ctx.bot.util.send_image_attachment(ctx, 'https://placegoat.com/'+str(random.randint(500, 700)))

    @command(['flop'])
    @cooldown(7)
    async def flip(self, ctx, *args):
        await ctx.trigger_typing()
        ava = await ctx.bot.Parser.parse_image(ctx, args, size=512)
        data = await ctx.bot.gif.flip(ava)
        return await ctx.send(file=discord.File(data, 'flip.gif'))

    @command(['spin'])
    @cooldown(7)
    async def rotate(self, ctx, *args):
        await ctx.trigger_typing()
        ava = await ctx.bot.Parser.parse_image(ctx, args, size=512)
        data = await ctx.bot.gif.rotate(ava)
        return await ctx.send(file=discord.File(data, 'rotate.gif'))

    @command()
    @cooldown(2)
    async def resize(self, ctx, *args):
        correct, wh = '', []
        for i in list(args):
            if i.isnumeric():
                correct += 'y'
                wh.append(int(i))
        await ctx.trigger_typing()
        if correct=='yy':
            ava = await ctx.bot.Parser.parse_image(ctx, args, size=512)
            if wh[0]>2000 or wh[1]>2000: raise ctx.bot.util.BasicCommandException("Your image is too big!")
            elif wh[0]<300 or wh[1]<300: raise ctx.bot.util.BasicCommandException("Your image is too small!")
            else:
                data = await ctx.bot.canvas.resize(ava, wh[0], wh[1])
                await ctx.send(file=discord.File(data, 'resize.png'))
        else:
            raise ctx.bot.util.BasicCommandException("Where are the parameters?")

    @command(['cat', 'fox', 'sadcat', 'bird'])
    @cooldown(2)
    async def dog(self, ctx):
        await ctx.trigger_typing()
        command_name = ctx.bot.util.get_command_name(ctx)
        link = self._links[command_name]
        api_url = await ctx.bot.util.get_request(link.split('|')[0], json=True, raise_errors=True, alexflipnote=link.split('|')[0].startswith("https://api.alexflipnote.dev/"))
        return await ctx.bot.util.send_image_attachment(ctx, api_url[link.split('|')[1]])

    @command()
    @cooldown(2)
    async def panda(self, ctx):
        link, col, msg = random.choice(["https://some-random-api.ml/img/panda", "https://some-random-api.ml/img/red_panda"]), ctx.me.color, 'Here is some cute pics of pandas.'
        data = await ctx.bot.util.get_request(link, json=True, raise_errors=True)
        embed = discord.Embed(title=msg, color=col)
        embed.set_image(url=data['link'])
        await ctx.send(embed=embed)
    
    @command()
    @cooldown(2)
    async def shibe(self, ctx):
        await ctx.trigger_typing()
        data = await ctx.bot.util.get_request(
            "http://shibe.online/api/shibes",
            json=True,
            raise_errors=True,
            count=1
        )
        await ctx.bot.util.send_image_attachment(ctx, data[0])
        del data
    
    @command()
    @cooldown(2)
    @require_args()
    async def ship(self, ctx, *args):
        await ctx.trigger_typing()
        parsed_args = ctx.bot.Parser.split_args(args)
        if parsed_args is None: 
            first, second = ctx.author.avatar_url_as(format='png'), await ctx.bot.Parser.parse_image(ctx, args)
        else: first, second = await ctx.bot.Parser.parse_image(ctx, parsed_args[0]), await ctx.bot.Parser.parse_image(ctx, parsed_args[1])
        url = f'https://api.alexflipnote.dev/ship?user={first}&user2={second}'
        return await ctx.bot.util.send_image_attachment(ctx, url, alexflipnote=True)

    @command(['coffee'])
    @cooldown(2)
    async def food(self, ctx, *args):
        command_name = ctx.bot.util.get_command_name(ctx)
        data = await ctx.bot.util.get_request('https://nekobot.xyz/api/image', json=True, raise_errors=True, type=command_name)
        link = data['message'].replace('\/', '/')
        if command_name == 'coffee':
            _random = random.randint(0, 1)
            if _random == 0:
                return await ctx.bot.util.send_image_attachment(ctx, "https://coffee.alexflipnote.dev/random")
        await ctx.trigger_typing()
        return await ctx.bot.util.send_image_attachment(ctx, link.replace('\/', '/'))

    @command()
    @cooldown(2)
    async def magik(self, ctx, *args):
        source = await ctx.bot.Parser.parse_image(ctx, args, cdn_only=True)
        await ctx.channel.trigger_typing()
        return await ctx.bot.util.send_image_attachment(ctx, f'https://api.alexflipnote.dev/filter/magik?image={source}', alexflipnote=True)

    @command(['df'])
    @cooldown(2)
    async def deepfry(self, ctx, *args):
        source = await ctx.bot.Parser.parse_image(ctx, args, default_to_png=False, cdn_only=True)
        await ctx.channel.trigger_typing()
        return await ctx.bot.util.send_image_attachment(ctx, f'https://api.alexflipnote.dev/filter/deepfry?image={source}', alexflipnote=True)

    @command()
    @cooldown(2)
    async def invert(self, ctx, *args):
        source = await ctx.bot.Parser.parse_image(ctx, args, default_to_png=False, cdn_only=True)
        await ctx.channel.trigger_typing()
        return await ctx.bot.util.send_image_attachment(ctx, f'https://api.alexflipnote.dev/filter/invert?image={source}', alexflipnote=True)
        
    @command(['grayscale', 'b&w', 'bw', 'classic', 'gray', 'grey', 'greyscale', 'gray-scale', 'grey-scale'])
    @cooldown(2)
    async def blackandwhite(self, ctx, *args):
        source = await ctx.bot.Parser.parse_image(ctx, args, default_to_png=False, cdn_only=True)
        await ctx.channel.trigger_typing()
        return await ctx.bot.util.send_image_attachment(ctx, f'https://api.alexflipnote.dev/filter/b&w?image={source}', alexflipnote=True)

    @command(['pixelate'])
    @cooldown(5)
    async def jpeg(self, ctx, *args):
        await ctx.trigger_typing()
        url = {"jpeg": "https://api.alexflipnote.dev/filter/jpegify?image=<URL>", "pixelate": "https://useless-api.vierofernando.repl.co/pixelate?image=<URL>&amount=<NUM>"}
        command_name = ctx.bot.util.get_command_name(ctx)
        avatar = await ctx.bot.Parser.parse_image(ctx, args, default_to_png=False, cdn_only=True)
        url = url[command_name].replace("<URL>", avatar).replace("<NUM>", random.choice(["16", "32"]))
        return await ctx.bot.util.send_image_attachment(ctx, url, alexflipnote=True)

def setup(client):
    client.add_cog(image())