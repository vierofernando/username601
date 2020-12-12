import discord
from discord.ext import commands
from decorators import *

class encoding(commands.Cog):
    def __init__(self):
        self.leet = None
    
    async def _get_leet(self, ctx):
        self.leet = await ctx.bot.util.get_request(
            "https://vierofernando.github.io/username601/assets/json/leet.json",
            json=True,
            raise_errors=True
        )
    
    @command()
    @cooldown(2)
    async def ascii(self, ctx, *args):
        text = ' '.join(args) if len(args)>0 else 'ascii text'
        ascii = await ctx.bot.util.get_request(
            "http://artii.herokuapp.com/make",
            raise_errors=True,
            text=text
        )
        
        await ctx.send(f'```{ascii[0:2000]}```')
        del ascii, text
    
    @command('fliptext,fancy,cursive,braille')
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
        command_name = ctx.bot.util.get_command_name(ctx)
        
        if command_name == "fliptext": data = res['styles']['upside-down']
        elif command_name == "cursive": data = res['styles']['cursive']
        elif command_name == "fancy": data = res['styles']['fancy']
        elif command_name == "braille": data = res['braille']
        else: data = res['ciphers']['morse']
        await ctx.send(data)
    
    @command()
    @cooldown(2)
    @require_args()
    async def barcode(self, ctx, *args):
        await ctx.trigger_typing()
        return await ctx.bot.util.send_image_attachment(ctx, 'http://www.barcode-generator.org/zint/api.php?bc_number=20&bc_data=' + ctx.bot.util.encode_uri(' '.join(args))[0:75])
    
    @command('qrcode,qr-code')
    @cooldown(2)
    @require_args()
    async def qr(self, ctx, *args):
        await ctx.trigger_typing()
        return await ctx.bot.util.send_image_attachment(ctx, 'https://api.qrserver.com/v1/create-qr-code/?size=150x150&data=' + ctx.bot.util.encode_uri(' '.join(args))[0:75])

    @command()
    @cooldown(2)
    @require_args()
    async def binary(self, ctx, *args):
        return await ctx.send('```'+str(ctx.bot.util.binary(str(' '.join(args))))[0:2000]+'```')

    @command()
    @cooldown(2)
    async def caesar(self, ctx, *args):
        if len(args)<2:
            raise ctx.bot.util.BasicCommandException(f'Try something like `{ctx.bot.command_prefix}caesar 3 hello world`')
        offset = ctx.bot.Parser.get_numbers(args)
        if not offset:
            raise ctx.bot.util.BasicCommandException(f'Add an offset to your command. Example: `{ctx.bot.command_prefix}caesar 3 hello world`')
        return await ctx.send(ctx.bot.util.caesar(str(' '.join(args).replace(str(offset), '')), offset), allowed_mentions=ctx.bot.util.no_mentions)
    
    @command()
    @cooldown(2)
    @require_args()
    async def atbash(self, ctx, *args):
        return await ctx.send(ctx.bot.util.atbash(' '.join(args)), allowed_mentions=ctx.bot.util.no_mentions)

    @command()
    @cooldown(2)
    @require_args()
    async def reverse(self, ctx, *args):
        return await ctx.send(str(' '.join(args))[::-1], allowed_mentions=ctx.bot.util.no_mentions)
    
    @command('b64')
    @cooldown(2)
    @require_args()
    async def base64(self, ctx, *args):
        return await ctx.send(ctx.bot.util.base64(' '.join(args)), allowed_mentions=ctx.bot.util.no_mentions)
    
    @command('leetspeak')
    @cooldown(2)
    @require_args()
    async def leet(self, ctx, *args):
        await ctx.trigger_typing()
        if not self.leet:
            await self._get_leet(ctx)

        total = ''
        for i in ' '.join(args)[0:100].lower():
            if i.isalpha():
                total += self.leet[i]
            else:
                total += i
        await ctx.send(total, allowed_mentions=ctx.bot.util.no_mentions)
        del total, data

def setup(client):
    client.add_cog(encoding())