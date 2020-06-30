import discord
from discord.ext import commands
import sys
sys.path.append('/app/modules')
import username601 as myself

class encoding(commands.Cog):
    def __init__(self, client):
        self.client = client
    
    @commands.command(pass_context=True, aliases=['fliptext', 'fancy', 'cursive', 'braille'])
    @commands.cooldown(1, 1, commands.BucketType.user)
    async def morse(self, ctx, *args):
        if 'fliptext' in str(ctx.message.content).split(' ')[0][1:]: data = myself.jsonisp("https://raw.githubusercontent.com/dragonfire535/xiao/master/assets/json/upside-down.json")
        elif 'cursive' in str(ctx.message.content).split(' ')[0][1:]: data = myself.jsonisp("https://raw.githubusercontent.com/dragonfire535/xiao/master/assets/json/cursive.json")
        elif 'fancy' in str(ctx.message.content).split(' ')[0][1:]: data = myself.jsonisp("https://raw.githubusercontent.com/dragonfire535/xiao/master/assets/json/fancy.json")
        elif 'braille' in str(ctx.message.content).split(' ')[0][1:]: data = myself.jsonisp("https://raw.githubusercontent.com/dragonfire535/xiao/master/assets/json/braille.json")
        else: data = myself.jsonisp("https://raw.githubusercontent.com/dragonfire535/xiao/master/assets/json/morse.json")
        total = ''
        for i in list(str(' '.join(list(args))).lower()):
            for j in range(0, len(list(data.keys()))):
                if i.lower()==list(data.keys())[j].lower():
                    i = i.replace(list(data.keys())[j], data[list(data.keys())[j]])
                    break
                else:
                    continue
            if 'morse' in str(ctx.message.content).split(' ')[0]:
                if i==' ': i = '/'
                else: i += ' '
                total += i
        await ctx.send(total)
    @commands.command(pass_context=True, aliases=['qr', 'qrcode', 'qr-code'])
    @commands.cooldown(1, 1, commands.BucketType.user)
    async def barcode(self, ctx, *args):
        if len(list(args))==0:
            await ctx.send(str(self.client.get_emoji(BotEmotes.error))+' | Please provide a text!')
        else:
            async with ctx.message.channel.typing():
                if 'qr' in str(ctx.message.content).split(' ')[0][1:]: url = "https://api.qrserver.com/v1/create-qr-code/?size=150x150&data="+str(myself.urlify(str(' '.join(list(args)))))
                else: url= 'http://www.barcode-generator.org/zint/api.php?bc_number=20&bc_data='+str(myself.urlify(str(' '.join(list(args)))))
                await ctx.send(file=discord.File(Painter.urltoimage(url), 'qr_or_barcode.png'))
    
    @commands.command(pass_context=True)
    @commands.cooldown(1, 1, commands.BucketType.user)
    async def binary(self, ctx, *args):
        if len(list(args))==0:
            await ctx.send(str(self.client.get_emoji(BotEmotes.error))+' | gimme something.')
        else:
            if len(myself.bin(str(' '.join(list(args)))))>4000: await ctx.send(str(self.client.get_emoji(BotEmotes.error))+' | the result is too long for discord to proccess...')
            else: await ctx.send('```'+str(myself.bin(str(' '.join(list(args)))))+'```')
    @commands.command(pass_context=True)
    @commands.cooldown(1, 1, commands.BucketType.user)
    async def caesar(self, ctx, *args):
        if len(list(args))==0:
            await ctx.send(str(self.client.get_emoji(BotEmotes.error))+' | gimme something.')
        else:
            offset = None
            for i in args:
                if i.isnumeric():
                    offset = int(i)
                    break
            if offset==None:
                await ctx.send(str(self.client.get_emoji(BotEmotes.error))+' | No offset?')
            else:
                await ctx.send(myself.caesar(str(' '.join(list(args)).replace(str(offset), ''), int(offset))))
    @commands.command(pass_context=True)
    @commands.cooldown(1, 1, commands.BucketType.user)
    async def atbash(self, ctx, *args):
        if len(list(args))==0: await ctx.send(str(self.client.get_emoji(BotEmotes.error)) + ' | Invalid. Please give us the word to encode...')
        else: await ctx.send(myself.atbash(' '.join(list(args))))

    @commands.command(pass_context=True)
    @commands.cooldown(1, 1, commands.BucketType.user)
    async def reverse(self, ctx, *args):
        if len(list(args))==0: await ctx.send('no arguments? rip'[::-1])
        else: await ctx.send(str(' '.join(list(args)))[::-1])
    
    @commands.command(pass_context=True, rewrite=['b64'])
    @commands.cooldown(1, 1, commands.BucketType.user)
    async def base64(self, ctx, *args):
        if len(list(args)): await ctx.send(str(self.client.get_emoji(BotEmotes.error))+' | Gimme dat args!')
        else: await ctx.send(myself.encodeb4(' '.join(args)))
    
    @commands.command(pass_context=True, rewrite=['leetspeak'])
    @commands.cooldown(1, 1, commands.BucketType.user)
    async def leet(self, ctx, *args):
        if len(list(args))==0:
            await ctx.send(str(self.client.get_emoji(BotEmotes.error))+' | No arguments? ok then! no service it is!')
        else:
            data = myself.jsonisp("https://vierofernando.github.io/username601/assets/json/leet.json")
            total = ''
            for i in range(0, len(' '.join(list(args)))):
                for j in list(data.keys()):
                    if str(' '.join(list(args)))[i].lower()==j.lower():
                        total += data[list(data.keys())[i]]
                        break
                if len(total)==i: total += str(' '.join(list(args)))[i]
            await ctx.send(total)
    

def setup(client):
    client.add_cog(encoding(client))