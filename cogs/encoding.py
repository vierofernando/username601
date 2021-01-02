import discord
from discord.ext import commands
from decorators import *
from io import BytesIO

class encoding(commands.Cog):
    def __init__(self):
        pass
    
    @command()
    @cooldown(4)
    @require_args()
    async def ascii(self, ctx, *args):
        await ctx.trigger_typing()
        parser = ctx.bot.Parser(args)
        parser.parse()
        hastebin = parser.has("hastebin")
        parser.shift("hastebin")
        
        if (not parser) or (not parser.has("image")):
            if not parser.other:
                del parser, hastebin
                return await ctx.bot.cmds.invalid_args(ctx)
            
            ascii = await ctx.bot.util.get_request(
                "http://artii.herokuapp.com/make",
                raise_errors=True,
                text=' '.join(parser.other)
            )
            if hastebin:
                try:
                    response = await ctx.bot.http._HTTPClient__session.post("https://paste.mod.gg/documents", data=ascii)
                    assert response.status < 400
                    json = await response.json()
                    await ctx.send(embed=discord.Embed(description=f"[**Click here to see the asciified text.**](https://paste.mod.gg/{json['key']})", color=discord.Color.green()))
                    del ascii, image, parser, hastebin, json
                    return
                except AssertionError:
                    pass
            
            await ctx.send(f'```{ascii[0:2000]}```')
            del ascii, parser, hastebin
            return
        
        parser.shift("image")
        image = await ctx.bot.Parser.parse_image(ctx, parser.other)
        string = await ctx.bot.Image.asciify(image)
        if hastebin:
            try:
                response = await ctx.bot.http._HTTPClient__session.post("https://paste.mod.gg/documents", data=string)
                assert response.status < 400
                json = await response.json()
                await ctx.send(embed=discord.Embed(description=f"[**Click here to see the asciified image.**](https://paste.mod.gg/{json['key']})", color=discord.Color.green()))
                del string, image, parser, hastebin, json
                return
            except AssertionError:
                pass
        
        await ctx.send(file=discord.File(BytesIO(bytes(string, 'utf-8')), "asciified.txt"))
        del string, image, parser, hastebin
        return
    
    
    @command()
    @cooldown(5)
    @require_args()
    async def morse(self, ctx, *args):
        await ctx.trigger_typing()
        res = await ctx.bot.util.get_request(
            'https://useless-api.vierofernando.repl.co/encode',
            json=True,
            text=str(" ".join(args))[0:100]
        )
        if not res:
            raise ctx.bot.util.BasicCommandException("The API is temporarily down. Please try again later.")

        await ctx.send(res['ciphers']['morse'])
    
    @command()
    @cooldown(5)
    @require_args()
    async def fliptext(self, ctx, *args):
        await ctx.trigger_typing()
        res = await ctx.bot.util.get_request(
            'https://useless-api.vierofernando.repl.co/encode',
            json=True,
            text=str(" ".join(args))[0:100]
        )
        if not res:
            raise ctx.bot.util.BasicCommandException("The API is temporarily down. Please try again later.")
        
        await ctx.send(res['styles']['upside-down'])
    
    @command()
    @cooldown(5)
    @require_args()
    async def fancy(self, ctx, *args):
        await ctx.trigger_typing()
        res = await ctx.bot.util.get_request(
            'https://useless-api.vierofernando.repl.co/encode',
            json=True,
            text=str(" ".join(args))[0:100]
        )
        if not res:
            raise ctx.bot.util.BasicCommandException("The API is temporarily down. Please try again later.")
        
        await ctx.send(res['styles']['fancy'])
    
    @command()
    @cooldown(5)
    @require_args()
    async def cursive(self, ctx, *args):
        await ctx.trigger_typing()
        res = await ctx.bot.util.get_request(
            'https://useless-api.vierofernando.repl.co/encode',
            json=True,
            text=str(" ".join(args))[0:100]
        )
        if not res:
            raise ctx.bot.util.BasicCommandException("The API is temporarily down. Please try again later.")
        
        await ctx.send(res['styles']['cursive'])
    
    @command()
    @cooldown(5)
    @require_args()
    async def braille(self, ctx, *args):
        await ctx.trigger_typing()
        res = await ctx.bot.util.get_request(
            'https://useless-api.vierofernando.repl.co/encode',
            json=True,
            text=str(" ".join(args))[0:100]
        )
        if not res:
            raise ctx.bot.util.BasicCommandException("The API is temporarily down. Please try again later.")
        
        await ctx.send(res['braille'])
    
    @command()
    @cooldown(2)
    @require_args()
    async def barcode(self, ctx, *args):
        await ctx.trigger_typing()
        return await ctx.bot.util.send_image_attachment(ctx, 'http://www.barcode-generator.org/zint/api.php?bc_number=20&bc_data=' + ctx.bot.util.encode_uri(' '.join(args))[0:75])
    
    @command(['qrcode', 'qr-code'])
    @cooldown(2)
    @require_args()
    async def qr(self, ctx, *args):
        await ctx.trigger_typing()
        return await ctx.bot.util.send_image_attachment(ctx, 'https://api.qrserver.com/v1/create-qr-code/?size=150x150&data=' + ctx.bot.util.encode_uri(' '.join(args))[0:75])

    @command()
    @cooldown(2)
    @require_args()
    async def binary(self, ctx, *args):
        return await ctx.send('```'+ctx.bot.util.binary(' '.join(args))[0:2000]+'```')

    @command()
    @cooldown(2)
    @require_args(2)
    async def caesar(self, ctx, *args):
        offset = ctx.bot.Parser.get_numbers(args)
        if not offset:
            return await ctx.bot.cmds.invalid_args(ctx)
        return await ctx.send(ctx.bot.util.caesar(str(' '.join(args).replace(str(offset[0]), '')), offset[0]), allowed_mentions=ctx.bot.util.no_mentions)
    
    @command()
    @cooldown(2)
    @require_args()
    async def atbash(self, ctx, *args):
        return await ctx.send(ctx.bot.util.atbash(' '.join(args)), allowed_mentions=ctx.bot.util.no_mentions)

    @command()
    @cooldown(2)
    @require_args()
    async def reverse(self, ctx, *args):
        return await ctx.send(' '.join(args)[::-1], allowed_mentions=ctx.bot.util.no_mentions)
    
    @command(['b64'])
    @cooldown(2)
    @require_args()
    async def base64(self, ctx, *args):
        return await ctx.send(ctx.bot.util.base64(' '.join(args)), allowed_mentions=ctx.bot.util.no_mentions)
    
def setup(client):
    client.add_cog(encoding())