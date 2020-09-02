import discord
from discord.ext import commands
import sys
from username601 import *
sys.path.append(cfg('MODULES_DIR'))
from decorators import command, cooldown
from canvas import Painter

class encoding(commands.Cog):
    def __init__(self, client):
        self.client = client
        self.canvas = Painter(
            cfg('ASSETS_DIR'),
            cfg('FONTS_DIR')
        )
    
    @command()
    @cooldown(2)
    async def ascii(self, ctx, *args):
        text = urlify(' '.join(list(args))) if len(list(args))>0 else 'ascii%20text'
        try:
            await ctx.send('```{}```'.format(
                insp('http://artii.herokuapp.com/make?text={}'.format(text))
            ))
        except:
            await ctx.send('{} | Your text is too long to be processed!'.format(emote(self.client, 'error')))

    @command('fliptext,fancy,cursive,braille')
    @cooldown(5)
    async def morse(self, ctx, *args):
        if len(list(args))==0: await ctx.send(emote(self.client, 'error')+' | no arguments? Really?')
        elif len(' '.join(list(args))) > 100:
            await ctx.send(emote(self.client, 'error')+' | too long....')
        else:
            async with ctx.channel.typing():
                res = jsonisp('https://useless-api--vierofernando.repl.co/encode?text='+urlify(' '.join(list(args))))
                if 'fliptext' in str(ctx.message.content).split(' ')[0][1:]: data = res['styles']['upside-down']
                elif 'cursive' in str(ctx.message.content).split(' ')[0][1:]: data = res['styles']['cursive']
                elif 'fancy' in str(ctx.message.content).split(' ')[0][1:]: data = res['styles']['fancy']
                elif 'braille' in str(ctx.message.content).split(' ')[0][1:]: data = res['braille']
                else: data = res['ciphers']['morse']
                await ctx.send(f'{data}')
    @command('qr,qrcode,qr-code')
    @cooldown(1)
    async def barcode(self, ctx, *args):
        if len(list(args))==0:
            await ctx.send(emote(self.client, 'error')+' | Please provide a text!')
        elif len(' '.join(list(args))) > 50:
            await ctx.send(emote(self.client, 'error')+' | too longggggggggg')
        else:
            async with ctx.channel.typing():
                if 'qr' in str(ctx.message.content).split(' ')[0][1:]: url = "https://api.qrserver.com/v1/create-qr-code/?size=150x150&data="+str(urlify(str(' '.join(list(args)))))
                else: url= 'http://www.barcode-generator.org/zint/api.php?bc_number=20&bc_data='+str(urlify(str(' '.join(list(args)))))
                await ctx.send(file=discord.File(self.canvas.urltoimage(url), 'qr_or_barcode.png'))
    
    @command()
    @cooldown(1)
    async def binary(self, ctx, *args):
        if len(list(args))==0:
            await ctx.send(emote(self.client, 'error')+' | gimme something.')
        elif len(' '.join(list(args))) > 50:
            await ctx.send(emote(self.client, 'error')+' | too long.')
        else:
            if len(bin(str(' '.join(list(args)))))>4000: await ctx.send(emote(self.client, 'error')+' | the result is too long for discord to proccess...')
            else: await ctx.send('```'+str(bin(str(' '.join(list(args)))))+'```')
    @command()
    @cooldown(1)
    async def caesar(self, ctx, *args):
        if len(list(args))<2:
            await ctx.send(emote(self.client, 'error')+f' | Try something like `{prefix}caesar 3 hello world`')
        else:
            offset = None
            for i in args:
                if i.isnumeric():
                    offset = int(i)
                    break
            if offset==None:
                await ctx.send(emote(self.client, 'error')+' | No offset?')
            else:
                await ctx.send(caesar(str(' '.join(list(args)).replace(str(offset), '')), int(offset)))
    @command()
    @cooldown(1)
    async def atbash(self, ctx, *args):
        if len(list(args))==0: await ctx.send(emote(self.client, 'error') + ' | Invalid. Please give us the word to encode...')
        else: await ctx.send(atbash(' '.join(list(args))))

    @command()
    @cooldown(1)
    async def reverse(self, ctx, *args):
        if len(list(args))==0: await ctx.send('no arguments? rip'[::-1])
        else: await ctx.send(str(' '.join(list(args)))[::-1])
    
    @command('b64')
    @cooldown(1)
    async def base64(self, ctx, *args):
        if len(list(args))==0: await ctx.send(emote(self.client, 'error')+' | Gimme dat args!')
        else: await ctx.send(encodeb64(' '.join(args)))
    
    @command('leetspeak')
    @cooldown(1)
    async def leet(self, ctx, *args):
        if len(list(args))==0:
            await ctx.send(emote(self.client, 'error')+' | No arguments? ok then! no service it is!')
        else:
            data = jsonisp("https://vierofernando.github.io/username601/assets/json/leet.json")
            total = ''
            text = ' '.join(list(args))
            for i in list(text):
                if i.lower() in list('abcdefghijklmnopqrstuvwxyz'):
                    total += data[i]
                    continue
                total += i
            await ctx.send(total)
    

def setup(client):
    client.add_cog(encoding(client))