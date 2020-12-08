import discord
from discord.ext import commands
from category.decorators import command, cooldown

class encoding(commands.Cog):
    def __init__(self):
        pass
    
    @command()
    @cooldown(2)
    async def ascii(self, ctx, *args):
        text = ' '.join(args) if len(args)>0 else 'ascii text'
        ascii = await ctx.bot.util.get_request(
            "http://artii.herokuapp.com/make",
            raise_errors=True,
            text=text
        )
        
        await ctx.send('```{}```'.format(
            ascii[0:2000]
        ))
    @command('fliptext,fancy,cursive,braille')
    @cooldown(5)
    async def morse(self, ctx, *args):
        if len(args)==0: return await ctx.bot.util.send_error_message(ctx, 'no arguments? Really?')
        await ctx.trigger_typing()
        res = await ctx.bot.util.get_request(
            'https://useless-api--vierofernando.repl.co/encode',
            json=True,
            text=str(" ".join(args))[0:100]
        )
        if res is None: return await ctx.bot.util.send_error_message(ctx, "The API is temporarily down. Please try again later.")
        command_name = ctx.bot.util.get_command_name(ctx)
        
        if command_name == "fliptext": data = res['styles']['upside-down']
        elif command_name == "cursive": data = res['styles']['cursive']
        elif command_name == "fancy": data = res['styles']['fancy']
        elif command_name == "braille": data = res['braille']
        else: data = res['ciphers']['morse']
        await ctx.send(f'{data}')
    
    @command('qr,qrcode,qr-code')
    @cooldown(2)
    async def barcode(self, ctx, *args):
        if len(args)==0:
            return await ctx.bot.util.send_error_message(ctx, 'Please provide a text!')
        else:
            command_name = ctx.bot.util.get_command_name(ctx)
            await ctx.trigger_typing()
            if command_name.startswith("qr"): url = "https://api.qrserver.com/v1/create-qr-code/?size=150x150&data="+str(ctx.bot.util.encode_uri(str(' '.join(args))[0:75]))
            else: url = 'http://www.barcode-generator.org/zint/api.php?bc_number=20&bc_data='+str(ctx.bot.util.encode_uri(str(' '.join(args))[0:75]))
            return await ctx.bot.util.send_image_attachment(ctx, url)
    
    @command()
    @cooldown(2)
    async def binary(self, ctx, *args):
        if len(args)==0:
            return await ctx.bot.util.send_error_message(ctx, 'gimme something.')
        return await ctx.send('```'+str(ctx.bot.util.binary(str(' '.join(args))))[0:2000]+'```')

    @command()
    @cooldown(2)
    async def caesar(self, ctx, *args):
        if len(args)<2:
            return await ctx.bot.util.send_error_message(ctx, f'Try something like `{ctx.bot.command_prefix}caesar 3 hello world`')
        else:
            offset = None
            for i in args:
                if i.isnumeric():
                    offset = int(i); break
            if offset is None:
                return await ctx.bot.util.send_error_message(ctx, 'No offset?')
            else:
                return await ctx.send(ctx.bot.util.caesar(str(' '.join(args).replace(str(offset), '')), int(offset)))
    @command()
    @cooldown(2)
    async def atbash(self, ctx, *args):
        if len(args)==0: return await ctx.bot.util.send_error_message(ctx, 'Invalid. Please give us the word to encode...')
        else: await ctx.send(ctx.bot.util.atbash(' '.join(args)))

    @command()
    @cooldown(2)
    async def reverse(self, ctx, *args):
        if len(args)==0: return await ctx.bot.util.send_error_message(ctx, 'no arguments? rip'[::-1])
        else: await ctx.send(str(' '.join(args))[::-1], allowed_mentions=discord.AllowedMentions(everyone=False, users=False, roles=False))
    
    @command('b64')
    @cooldown(2)
    async def base64(self, ctx, *args):
        if len(args)==0: return await ctx.bot.util.send_error_message(ctx, 'Gimme dat args!')
        else: await ctx.send(ctx.bot.util.base64(' '.join(args)))
    
    @command('leetspeak')
    @cooldown(2)
    async def leet(self, ctx, *args):
        if len(args)==0:
            return await ctx.bot.util.send_error_message(ctx, 'No arguments? ok then! no service it is!')
        else:
            data = await ctx.bot.util.get_request(
                "https://vierofernando.github.io/username601/assets/json/leet.json",
                json=True,
                raise_errors=True
            )
            
            total = ''
            for i in list(' '.join(args)):
                if i.isalpha():
                    total += data[i.lower()]
                else:
                    total += i
            await ctx.send(total)
    

def setup(client):
    client.add_cog(encoding())