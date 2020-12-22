import discord
from discord.ext import commands
from PIL import ImageColor
from decorators import *
import random
from io import BytesIO
from aiohttp import ClientSession
from json import loads

class image(commands.Cog):
    def __init__(self):
        pass
    
    @command(['dogs'])
    @cooldown(3)
    async def dog(self, ctx):
        await ctx.trigger_typing()
        data = await ctx.bot.util.get_request("https://api.alexflipnote.dev/dogs", json=True, raise_errors=True, alexflipnote=True)
        return await ctx.bot.util.send_image_attachment(ctx, data["file"])
    
    @command(['cats'])
    @cooldown(3)
    async def cat(self, ctx):
        await ctx.trigger_typing()
        data = await ctx.bot.util.get_request("https://api.alexflipnote.dev/cats", json=True, raise_errors=True, alexflipnote=True)
        return await ctx.bot.util.send_image_attachment(ctx, data["file"])
    
    @command(['birb', 'birbs', 'birds'])
    @cooldown(3)
    async def bird(self, ctx):
        await ctx.trigger_typing()
        data = await ctx.bot.util.get_request("https://api.alexflipnote.dev/birb", json=True, raise_errors=True, alexflipnote=True)
        return await ctx.bot.util.send_image_attachment(ctx, data["file"])
    
    @command(['foxes', 'furry', 'furries'])
    @cooldown(3)
    async def fox(self, ctx):
        await ctx.trigger_typing()
        data = await ctx.bot.util.get_request("https://randomfox.ca/floof", json=True, raise_errors=True)
        return await ctx.bot.util.send_image_attachment(ctx, data["image"])

    @command(['colourify'])
    @cooldown(5)
    @require_args()
    async def colorify(self, ctx, *args):
        await ctx.trigger_typing()
        try:
            if len(args) == 1:
                color = ImageColor.getrgb(args[0])
                image = str(ctx.author.avatar_url_as(format="png", size=1024))
            else:
                parsed_args = ctx.bot.Parser.split_args(args)
                color = ImageColor.getrgb(parsed_args[0])
                image = await ctx.bot.Parser.parse_image(ctx, (parsed_args[1],))
        except:
            return await ctx.bot.cmds.invalid_args(ctx)
        
        image = await ctx.bot.Image.colorify(image, color, session=ctx.bot.util.default_client)
        await ctx.send(file=discord.File(image, "%02x%02x%02x.png" % color))
        del resp, byte, image, color

    @command(['legofy'])
    @cooldown(10)
    async def lego(self, ctx, *args):
        await ctx.trigger_typing()
        
        image_url = await ctx.bot.Parser.parse_image(ctx, args)
        lego_image = await ctx.bot.lego(image_url, session=ctx.bot.util.default_client)
        await ctx.send(file=discord.File(lego_image, "lego.png"))
        del image_url, lego_image

    @command()
    @cooldown(9)
    async def implode(self, ctx, *args):
        await ctx.trigger_typing()
        parser = ctx.bot.Parser(args)
        parser.parse()
        animated = parser.has("animated")
        
        if animated:
            parser.shift("animated")
        
        url = await ctx.bot.Parser.parse_image(ctx, ' '.join(parser.other))
        if animated:
            del parser, animated
            return await ctx.bot.util.send_image_attachment(ctx, f"https://useless-api.vierofernando.repl.co/implode/animated?image={url}", uselessapi=True)
        result, format = await ctx.bot.Image.implode(url, amount=1, session=ctx.bot.util.default_client)
        await ctx.send(file=discord.File(result, f"file.{format}"))
        del result, format, url, parser, animated
        
    @command()
    @cooldown(9)
    async def explode(self, ctx, *args):
        await ctx.trigger_typing()
        parser = ctx.bot.Parser(args)
        parser.parse()
        animated = parser.has("animated")
        
        if animated:
            parser.shift("animated")
        
        url = await ctx.bot.Parser.parse_image(ctx, ' '.join(parser.other))
        if animated:
            del parser, animated
            return await ctx.bot.util.send_image_attachment(ctx, f"https://useless-api.vierofernando.repl.co/explode/animated?image={url}", uselessapi=True)
        result, format = await ctx.bot.Image.implode(url, amount=-3.5, session=ctx.bot.util.default_client)
        await ctx.send(file=discord.File(result, f"file.{format}"))
        del result, format, url, parser, animated
        
    @command()
    @cooldown(8)
    async def charcoal(self, ctx, *args):
        await ctx.trigger_typing()
        url = await ctx.bot.Parser.parse_image(ctx, args)
        buffer, format = await ctx.bot.Image.charcoal(url, session=ctx.bot.util.default_client)
        await ctx.send(file=discord.File(buffer, f"file.{format}"))
        del buffer, format, url
    
    @command()
    @cooldown(8)
    async def spread(self, ctx, *args):
        await ctx.trigger_typing()
        url = await ctx.bot.Parser.parse_image(ctx, args)
        buffer, format = await ctx.bot.Image.spread(url, session=ctx.bot.util.default_client)
        await ctx.send(file=discord.File(buffer, f"file.{format}"))
        del buffer, format, url
    
    @command()
    @cooldown(8)
    async def emboss(self, ctx, *args):
        await ctx.trigger_typing()
        url = await ctx.bot.Parser.parse_image(ctx, args)
        buffer, format = await ctx.bot.Image.emboss(url, session=ctx.bot.util.default_client)
        await ctx.send(file=discord.File(buffer, f"file.{format}"))
        del buffer, format, url
    
    @command()
    @cooldown(8)
    async def edge(self, ctx, *args):
        await ctx.trigger_typing()
        url = await ctx.bot.Parser.parse_image(ctx, args)
        buffer, format = await ctx.bot.Image.edge(url, session=ctx.bot.util.default_client)
        await ctx.send(file=discord.File(buffer, f"file.{format}"))
        del buffer, format, url
    
    @command()
    @cooldown(8)
    async def sketch(self, ctx, *args):
        await ctx.trigger_typing()
        url = await ctx.bot.Parser.parse_image(ctx, args)
        buffer, format = await ctx.bot.Image.sketch(url, session=ctx.bot.util.default_client)
        await ctx.send(file=discord.File(buffer, f"file.{format}"))
        del buffer, format, url
    
    @command()
    @cooldown(8)
    async def wave(self, ctx, *args):
        await ctx.trigger_typing()
        number = ctx.bot.Parser.get_numbers(args)
        if number and (int(number[0]) in range(0, 50)):
            l = list(args)
            l.pop(args.index(str(number[0])))
            args = tuple(l)
            del l
        else:
            number = [10]
        url = await ctx.bot.Parser.parse_image(ctx, args)
        buffer, format = await ctx.bot.Image.wave(url, amount=number[0], session=ctx.bot.util.default_client)
        await ctx.send(file=discord.File(buffer, f"file.{format}"))
        del number, buffer, format, url
    
    @command()
    @cooldown(8)
    async def swirl(self, ctx, *args):
        await ctx.trigger_typing()
        number = ctx.bot.Parser.get_numbers(args)
        if number and (int(number[0]) in range(0, 361)):
            l = list(args)
            l.pop(args.index(str(number[0])))
            args = tuple(l)
            del l
        else:
            number = [360]
        url = await ctx.bot.Parser.parse_image(ctx, args)
        buffer, format = await ctx.bot.Image.swirl(url, degree=number[0], session=ctx.bot.util.default_client)
        await ctx.send(file=discord.File(buffer, f"file.{format}"))
        del number, buffer, format, url
    
    @command(['combine'])
    @cooldown(2)
    @require_args()
    async def blend(self, ctx, *args):
        await ctx.trigger_typing()
        parsed_args = ctx.bot.Parser.split_args(args)
        if not parsed_args:
            first = ctx.author.avatar_url_as(format='png')
            second = await ctx.bot.Parser.parse_image(ctx, args)
        else:
            first = await ctx.bot.Parser.parse_image(ctx, (parsed_args[0],))
            second = await ctx.bot.Parser.parse_image(ctx, (parsed_args[1],))
        
        blended = await ctx.bot.Image.blend(first, second, session=ctx.bot.util.default_client)
        return await ctx.send(file=discord.File(blended, 'blend.png'))

    @command()
    @cooldown(2)
    async def blur(self, ctx, *args):
        await ctx.trigger_typing()
        url = await ctx.bot.Parser.parse_image(ctx, args, size=512)
        im = await ctx.bot.Image.blur(url, session=ctx.bot.util.default_client)
        await ctx.send(file=discord.File(im, 'blur.png'))
        del im, url

    @command(['glitchify', 'matrix'])
    @cooldown(5)
    async def glitch(self, ctx, *args):
        ava = await ctx.bot.Parser.parse_image(ctx, args, size=128)
        await ctx.trigger_typing()
        return await ctx.bot.util.send_image_attachment(ctx, "https://useless-api.vierofernando.repl.co/glitch/noratelimit?image=" + ava, uselessapi=True)
    
    @command(['ducks', 'quack', 'duk'])
    @cooldown(2)
    async def duck(self, ctx):
        _url = await ctx.bot.util.get_request(
            'https://random-d.uk/api/v2/random',
            format='json',
            json=True,
            raise_errors=True
        )
        await ctx.bot.util.send_image_attachment(ctx, _url["url"])

    @command(['snek', 'snakes', 'python', 'py'])
    @cooldown(2)
    async def snake(self, ctx):
        return await ctx.bot.util.send_image_attachment(ctx, 'https://fur.im/snek/i/'+str(random.randint(1, 874))+'.png')

    @command(['imageoftheday', 'pod', 'pictureoftheday', 'iod'])
    @cooldown(10)
    async def iotd(self, ctx):
        try:
            data = await ctx.bot.util.get_request(
                'https://www.bing.com/HPImageArchive.aspx',
                raise_errors=True,
                format='ks',
                idx=0,
                n=1,
                mkt='en-US'
            )
        except:
            raise ctx.bot.util.BasicCommandException("The API may be down for a while. Try again later!")

        embed = ctx.bot.Embed(
            ctx,
            title=data.split('copyright>')[1].split("</")[0],
            url=data.split('copyrightlink>')[1].split("</")[0],
            image='https://bing.com'+data.split("url>")[1].split("</")[0]
        )
        await embed.send()
        del embed, data

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
    @require_args(3)
    async def resize(self, ctx, *args):
        try:
            width, height = args[:2]
            assert int(width) in range(2, 2000)
            assert int(height) in range(2, 2000)
            url = await ctx.bot.Parser.parse_image(ctx, args[2:])
            image = await ctx.bot.Image.resize(url, int(width), int(height), session=ctx.bot.util.default_client)
            await ctx.send(file=discord.File(image, "resize.png"))
        except:
            return await ctx.bot.cmds.invalid_args(ctx)

    @command()
    @cooldown(3)
    async def panda(self, ctx):
        link = random.choice(["https://some-random-api.ml/img/panda", "https://some-random-api.ml/img/red_panda"])
        data = await ctx.bot.util.get_request(link, json=True, raise_errors=True)
        await ctx.bot.util.send_image_attachment(ctx, data['link'])
        del link, data
    
    @command()
    @cooldown(3)
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
        if not parsed_args: 
            first, second = ctx.author.avatar_url_as(format='png'), await ctx.bot.Parser.parse_image(ctx, args)
        else: first, second = await ctx.bot.Parser.parse_image(ctx, parsed_args[0]), await ctx.bot.Parser.parse_image(ctx, parsed_args[1])
        url = f'https://api.alexflipnote.dev/ship?user={first}&user2={second}'
        return await ctx.bot.util.send_image_attachment(ctx, url, alexflipnote=True)

    @command(['hungry'])
    @cooldown(2)
    async def food(self, ctx):
        await ctx.trigger_typing()
        data = await ctx.bot.util.get_request('https://nekobot.xyz/api/image', json=True, raise_errors=True, type="food")
        return await ctx.bot.util.send_image_attachment(ctx, data['message'].replace('\/', '/'))

    @command()
    @cooldown(2)
    async def coffee(self, ctx):
        await ctx.trigger_typing()
        seed = random.randint(0, 1)
        if not seed:
            data = await ctx.bot.util.get_request('https://nekobot.xyz/api/image', json=True, raise_errors=True, type="coffee")
            return await ctx.bot.util.send_image_attachment(ctx, data["message"].replace('\/', '/'))
        return await ctx.bot.util.send_image_attachment(ctx, 'https://coffee.alexflipnote.dev/random', alexflipnote=True)

    @command(['pixel', '8-bit', '8bit'])
    @cooldown(3)
    async def pixelate(self, ctx, *args):
        await ctx.trigger_typing()
        number = ctx.bot.Parser.get_numbers(args)
        if number:
            l = list(args)
            l.pop(args.index(str(number[0])))
            args = tuple(l)
            del l
        else:
            number = [32]
        url = await ctx.bot.Parser.parse_image(ctx, args)
        image = await ctx.bot.Image.pixelate(url, amount=number[0], session=ctx.bot.util.default_client)
        await ctx.send(file=discord.File(image, "pixels.png"))
        del image, url, number

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

    @command(['jpegify'])
    @cooldown(5)
    async def jpeg(self, ctx, *args):
        await ctx.trigger_typing()
        url = await ctx.bot.Parser.parse_image(ctx, args, default_to_png=False, cdn_only=True)
        return await ctx.bot.util.send_image_attachment(ctx, "https://api.alexflipnote.dev/filter/jpegify?image="+url, alexflipnote=True)

def setup(client):
    client.add_cog(image())