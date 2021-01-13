import discord
from discord.ext import commands
from decorators import *
from random import randint, choice
from io import BytesIO
from aiohttp import ClientSession
from json import loads
from time import time
from os import environ
from gc import collect

class image(commands.Cog):
    def __init__(self):
        self.aeon_count = None
        self.last_aeon = 0
        self.aeon_url = environ["AEON_API_URL"]
    
    @command(['aun', 'æon'])
    @cooldown(3)
    async def aeon(self, ctx):
        if (time() - self.last_aeon) >= 10800: # this API is sacred so i'm not giving you the URL
            resp = await ctx.bot.util.request(self.aeon_url)
            self.aeon_count = int(resp)
            self.last_aeon = time()
            del resp
        return await ctx.send_image(f"{self.aeon_url}{randint(1, self.aeon_count)}.png")
    
    @command(['dogs'])
    @cooldown(3)
    async def dog(self, ctx):
        await ctx.trigger_typing()
        data = await ctx.bot.util.request("https://api.alexflipnote.dev/dogs", json=True, alexflipnote=True)
        return await ctx.send_image(data["file"])
    
    @command(['cats'])
    @cooldown(3)
    async def cat(self, ctx):
        await ctx.trigger_typing()
        data = await ctx.bot.util.request("https://api.alexflipnote.dev/cats", json=True, alexflipnote=True)
        return await ctx.send_image(data["file"])
    
    @command(['birb', 'birbs', 'birds'])
    @cooldown(3)
    async def bird(self, ctx):
        await ctx.trigger_typing()
        data = await ctx.bot.util.request("https://api.alexflipnote.dev/birb", json=True, alexflipnote=True)
        return await ctx.send_image(data["file"])
    
    @command(['foxes', 'furry', 'furries'])
    @cooldown(3)
    async def fox(self, ctx):
        await ctx.trigger_typing()
        data = await ctx.bot.util.request("https://randomfox.ca/floof", json=True)
        return await ctx.send_image(data["image"])

    @command(['colourify', 'colorize', 'colourize'])
    @cooldown(5)
    @require_args()
    async def colorify(self, ctx, *args):
        await ctx.trigger_typing()
        try:
            if not args[1:]:
                color = ctx.bot.Parser.parse_color(args[0])
                image = str(ctx.author.avatar_url_as(format=("gif" if ctx.author.is_avatar_animated() else "png"), size=512))
            else:
                parsed_args = ctx.bot.Parser.split_args(args)
                color = ctx.bot.Parser.parse_color(parsed_args[0])
                image = await ctx.bot.Parser.parse_image(ctx, (parsed_args[1],), default_to_png=False)
                del parsed_args
            assert bool(color)
        except:
            return await ctx.bot.cmds.invalid_args(ctx)
        
        image, format = await ctx.bot.Image.colorify(image, color)
        await ctx.send(file=discord.File(image, f"file.{format.lower()}"))
        del color, image, format
        collect()

    @command(['legofy'])
    @cooldown(10)
    async def lego(self, ctx, *args):
        await ctx.trigger_typing()
        
        image_url = await ctx.bot.Parser.parse_image(ctx, args)
        lego_image = await ctx.bot.lego(image_url, ctx.bot.http._HTTPClient__session)
        await ctx.send(file=discord.File(lego_image, "lego.png"))
        del image_url, lego_image
        collect()

    @command(["moob"])
    @cooldown(9)
    async def implode(self, ctx, *args):
        await ctx.trigger_typing()
        parser = ctx.bot.Parser(args)
        parser.parse()
        animated = parser.has("animated")
        
        if animated:
            parser.shift("animated")
        
        url = await ctx.bot.Parser.parse_image(ctx, parser.other)
        if animated:
            del parser, animated
            buffer = await ctx.bot.Image.explode_animated(url, True)
            return await ctx.send(file=discord.File(buffer, "moob.gif"))
        
        result, format = await ctx.bot.Image.implode(url, amount=1)
        await ctx.send(file=discord.File(result, f"file.{format.lower()}"))
        del result, format, url, parser, animated
        
    @command(["blow-up", "blowup", "boom"])
    @cooldown(9)
    async def explode(self, ctx, *args):
        await ctx.trigger_typing()
        parser = ctx.bot.Parser(args)
        parser.parse()
        animated = parser.has("animated")
        
        if animated:
            parser.shift("animated")
        
        url = await ctx.bot.Parser.parse_image(ctx, parser.other)
        if animated:
            del parser, animated
            buffer = await ctx.bot.Image.explode_animated(url)
            return await ctx.send(file=discord.File(buffer, "boom.gif"))
        result, format = await ctx.bot.Image.implode(url, amount=-3.5)
        await ctx.send(file=discord.File(result, f"file.{format.lower()}"))
        del result, format, url, parser, animated
        
    @command(["disintegrate"])
    @cooldown(5)
    async def dissolve(self, ctx, *args):
        await ctx.trigger_typing()
        url = await ctx.bot.Parser.parse_image(ctx, args)
        buffer = await ctx.bot.Image.dissolve(url)
        await ctx.send(file=discord.File(buffer, "mr-stark-i-dont-feel-so-good.png"))
        del url, buffer
        collect()
        
    @command()
    @cooldown(8)
    async def charcoal(self, ctx, *args):
        await ctx.trigger_typing()
        url = await ctx.bot.Parser.parse_image(ctx, args)
        buffer, format = await ctx.bot.Image.charcoal(url)
        await ctx.send(file=discord.File(buffer, f"file.{format.lower()}"))
        del buffer, format, url
    
    @command(["oil-image", "oilify"])
    @cooldown(8)
    async def oil(self, ctx, *args):
        await ctx.trigger_typing()
        url = await ctx.bot.Parser.parse_image(ctx, args)
        buffer, format = await ctx.bot.Image.oil(url)
        await ctx.send(file=discord.File(buffer, f"file.{format.lower()}"))
        del buffer, format, url
        collect()
    
    @command(["noice"])
    @cooldown(8)
    async def noise(self, ctx, *args):
        await ctx.trigger_typing()
        url = await ctx.bot.Parser.parse_image(ctx, args, default_to_png=False)
        buffer, format = await ctx.bot.Image.noise(url)
        await ctx.send(file=discord.File(buffer, f"file.{format.lower()}"))
        del buffer, format, url
        collect()
    
    @command(["solarise"])
    @cooldown(8)
    async def solarize(self, ctx, *args):
        await ctx.trigger_typing()
        url = await ctx.bot.Parser.parse_image(ctx, args, default_to_png=False)
        buffer, format = await ctx.bot.Image.solarize(url)
        await ctx.send(file=discord.File(buffer, f"file.{format.lower()}"))
        del buffer, format, url
        collect()
    
    @command()
    @cooldown(8)
    async def spread(self, ctx, *args):
        await ctx.trigger_typing()
        url = await ctx.bot.Parser.parse_image(ctx, args, default_to_png=False)
        buffer, format = await ctx.bot.Image.spread(url)
        await ctx.send(file=discord.File(buffer, f"file.{format.lower()}"))
        del buffer, format, url
        collect()
    
    @command()
    @cooldown(8)
    async def emboss(self, ctx, *args):
        await ctx.trigger_typing()
        url = await ctx.bot.Parser.parse_image(ctx, args)
        buffer, format = await ctx.bot.Image.emboss(url)
        await ctx.send(file=discord.File(buffer, f"file.{format.lower()}"))
        del buffer, format, url
    
    @command()
    @cooldown(8)
    async def edge(self, ctx, *args):
        await ctx.trigger_typing()
        url = await ctx.bot.Parser.parse_image(ctx, args, default_to_png=False)
        buffer, format = await ctx.bot.Image.edge(url)
        await ctx.send(file=discord.File(buffer, f"file.{format.lower()}"))
        del buffer, format, url
        collect()
    
    @command()
    @cooldown(8)
    async def sketch(self, ctx, *args):
        await ctx.trigger_typing()
        url = await ctx.bot.Parser.parse_image(ctx, args)
        buffer, format = await ctx.bot.Image.sketch(url)
        await ctx.send(file=discord.File(buffer, f"file.{format.lower()}"))
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
        buffer, format = await ctx.bot.Image.wave(url, amount=number[0])
        await ctx.send(file=discord.File(buffer, f"file.{format.lower()}"))
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
        url = await ctx.bot.Parser.parse_image(ctx, args, default_to_png=False)
        buffer, format = await ctx.bot.Image.swirl(url, degree=number[0])
        await ctx.send(file=discord.File(buffer, f"file.{format.lower()}"))
        del number, buffer, format, url
        collect()
    
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
        
        blended = await ctx.bot.Image.blend(first, second)
        return await ctx.send(file=discord.File(blended, 'blend.png'))

    @command()
    @cooldown(2)
    async def blur(self, ctx, *args):
        await ctx.trigger_typing()
        
        try:
            parser = ctx.bot.Parser(args)
            parser.parse()
            
            image = await ctx.bot.Parser.parse_image(ctx, tuple(parser.other), default_to_png=False)
            blur_class = ctx.bot.Blur(ctx.bot, image)
            
            if parser.has_multiple("gaussian", "gaussian-blur"):
                image, format = await blur_class.blur(ctx.bot.Blur.GAUSSIAN_BLUR)
            elif parser.has_multiple("motion", "motion-blur"):
                image, format = await blur_class.blur(ctx.bot.Blur.MOTION_BLUR)
            elif parser.has_multiple("rotate", "rotational", "rotational-blur"):
                image, format = await blur_class.blur(ctx.bot.Blur.ROTATIONAL_BLUR)
            else:
                image, format = await blur_class.blur(0)
            
            await ctx.send(file=discord.File(image, f"file.{format.lower()}"))
            del image, format, blur_class, parser
            
        except:
            return await ctx.bot.cmds.invalid_args(ctx)

    @command(['glitchify', 'matrix'])
    @cooldown(5)
    async def glitch(self, ctx, *args):
        await ctx.trigger_typing()
        ava = await ctx.bot.Parser.parse_image(ctx, args, size=128)
        try:
            buffer = await ctx.bot.Image.glitch(ava)
        except AssertionError as a:
            raise ctx.bot.util.error_message(str(a))
        await ctx.send(file=discord.File(buffer, "glitch.png"))
        del buffer, ava
        collect()
   
    @command(['ducks', 'quack', 'duk'])
    @cooldown(2)
    async def duck(self, ctx):
        _url = await ctx.bot.util.request(
            'https://random-d.uk/api/v2/random',
            format='json',
            json=True
        )
        await ctx.send_image(_url["url"])

    @command(['snek', 'snakes', 'python', 'py'])
    @cooldown(2)
    async def snake(self, ctx):
        return await ctx.send_image('https://fur.im/snek/i/'+str(randint(1, 874))+'.png')

    @command(['imageoftheday', 'pod', 'pictureoftheday', 'iod'])
    @cooldown(10)
    async def iotd(self, ctx):
        try:
            data = await ctx.bot.util.request(
                'https://www.bing.com/HPImageArchive.aspx',
                xml=True,
                format='ks',
                idx=0,
                n=1,
                mkt='en-US'
            )
        except:
            raise ctx.bot.util.error_message("The API may be down for a while. Try again later!")

        embed = ctx.bot.Embed(
            ctx,
            title=data["images"]["image"]["copyright"],
            url=data["images"]["image"]["copyrightlink"],
            image='https://bing.com'+data["images"]["image"]["url"]
        )
        await embed.send()
        del embed, data

    @command()
    @cooldown(2)
    async def httpcat(self, ctx, *args):
        code = args[0] if ((not args) or (not args[0].isnumeric())) else '404'
        return await ctx.send_image('https://http.cat/'+str(code)+'.jpg')
    
    @command(['httpduck'])
    @cooldown(2)
    async def httpdog(self, ctx, *args):
        code = args[0] if ((not args) or (not args[0].isnumeric())) else '404'
        url = 'https://random-d.uk/api/http/ABC.jpg' if (ctx.bot.util.get_command_name(ctx) == "httpduck") else 'https://httpstatusdogs.com/img/ABC.jpg'
        try:
            return await ctx.send_image(url.replace('ABC', code))
        except:
            raise ctx.bot.util.error_message("404")

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
            image = await ctx.bot.Image.resize(url, int(width), int(height))
            await ctx.send(file=discord.File(image, "resize.png"))
        except:
            return await ctx.bot.cmds.invalid_args(ctx)

    @command()
    @cooldown(3)
    async def panda(self, ctx):
        link = choice(["https://some-random-api.ml/img/panda", "https://some-random-api.ml/img/red_panda"])
        data = await ctx.bot.util.request(link, json=True)
        await ctx.send_image(data['link'])
        del link, data
    
    @command()
    @cooldown(3)
    async def shibe(self, ctx):
        await ctx.trigger_typing()
        data = await ctx.bot.util.request(
            "http://shibe.online/api/shibes",
            json=True,
            count=1
        )
        await ctx.send_image(data[0])
        del data

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
        image = await ctx.bot.Image.pixelate(url, amount=number[0])
        await ctx.send(file=discord.File(image, "pixels.png"))
        del image, url, number

    @command()
    @cooldown(2)
    async def magik(self, ctx, *args):
        source = await ctx.bot.Parser.parse_image(ctx, args, cdn_only=True)
        await ctx.channel.trigger_typing()
        return await ctx.send_image(f'https://api.alexflipnote.dev/filter/magik?image={source}', alexflipnote=True)

    @command(['df'])
    @cooldown(2)
    async def deepfry(self, ctx, *args):
        source = await ctx.bot.Parser.parse_image(ctx, args, default_to_png=False, cdn_only=True)
        await ctx.channel.trigger_typing()
        return await ctx.send_image(f'https://api.alexflipnote.dev/filter/deepfry?image={source}', alexflipnote=True)

    @command()
    @cooldown(2)
    async def invert(self, ctx, *args):
        source = await ctx.bot.Parser.parse_image(ctx, args, default_to_png=False, cdn_only=True)
        await ctx.channel.trigger_typing()
        return await ctx.send_image(f'https://api.alexflipnote.dev/filter/invert?image={source}', alexflipnote=True)
        
    @command(['grayscale', 'b&w', 'bw', 'classic', 'gray', 'grey', 'greyscale', 'gray-scale', 'grey-scale'])
    @cooldown(2)
    async def blackandwhite(self, ctx, *args):
        source = await ctx.bot.Parser.parse_image(ctx, args, default_to_png=False, cdn_only=True)
        await ctx.channel.trigger_typing()
        return await ctx.send_image(f'https://api.alexflipnote.dev/filter/b&w?image={source}', alexflipnote=True)

    @command(['jpegify'])
    @cooldown(5)
    async def jpeg(self, ctx, *args):
        await ctx.trigger_typing()
        url = await ctx.bot.Parser.parse_image(ctx, args, default_to_png=False, cdn_only=True)
        return await ctx.send_image("https://api.alexflipnote.dev/filter/jpegify?image="+url, alexflipnote=True)

def setup(client):
    client.add_cog(image())