import discord
from discord.ext import commands
import sys
from os import getcwd, name
dirname = getcwd()+'\\..' if name=='nt' else getcwd()+'/..'
sys.path.append(dirname)
del dirname
from username601 import *
sys.path.append(cfg('MODULES_DIR'))
from io import BytesIO
from decorators import command, cooldown
from requests import get
from aiohttp import ClientSession

class memes(commands.Cog):
    def __init__(self, client):
        self.client = client
        self.session = ClientSession()
        self.rawMetadata = open(cfg('MODULES_DIR')+'/Animation.dat', 'r').read().split('\n')
        self.rageMetadata = [tuple([int(a) for a in i.split(',')]) for i in self.rawMetadata[0].split(';')]
        self.frogMetadata = self.rawMetadata[1].split(':')

    @command('petition')
    @cooldown(2)
    async def presentation(self, ctx, *args):
        async with ctx.channel.typing():
            text = f'Petition for {ctx.author.name} to insert parameters' if len(list(args))==0 else ' '.join(list(args))
            im = self.client.canvas.presentation(text)
            await ctx.send(file=discord.File(im, 'presentation.png'))

    @command('pass')
    @cooldown(1)
    async def password(self, ctx, *args):
        param = ' '.join(list(args))
        async with ctx.channel.typing():
            if '|' in param: text1, text2 = param.split('|')[0], param.split('|')[1:len(param.split('|'))]
            elif ', ' in param: text1, text2 = param.split(', ')[0], param.split(', ')[1:len(param.split(', '))]
            elif ',' in param: text1, text2 = param.split(',')[0], param.split(',')[1:len(param.split(','))]
            elif ' ' in param and len(param.split())==2: text1, text2 = param.split()[0], param.split()[1]
            else: text1, text2 = 'use the correct', 'parameters smh'
            i = self.client.canvas.password(text1, text2)
            await ctx.send(file=discord.File(i, 'password.png'))

    @command('programmerhumor,programmermeme,programming,programmer')
    @cooldown(2)
    async def programmingmeme(self, ctx):
        data = fetchJSON('https://useless-api.vierofernando.repl.co/programmermeme')['url']
        return await ctx.send(embed=discord.Embed(title='Programmer meme', color=get_embed_color(discord)).set_image(url=data))

    @command('shred,burn,spongebobpaper,paper,spongepaper,sponge-paper,spongebob-paper,spongebob')
    @cooldown(1)
    async def sponge(self, ctx, *args):
        async with ctx.channel.typing():
            av = getUserAvatar(ctx, args, size=512)
            im = self.client.canvas.trans_merge({
                'url': av,
                'filename': 'spongebobpaper.png',
                'pos': (29, 58),
                'size': (224, 259)
            })
            return await ctx.send(file=discord.File(im, 'haha-you-got-burned.png'))

    @command('ihavefailedyou,fail')
    @cooldown(1)
    async def failed(self, ctx, *args):
        async with ctx.channel.typing():
            av = getUserAvatar(ctx, args)
            res = self.client.canvas.trans_merge({
                'url': av,
                'filename': 'failed.png',
                'size': (155, 241),
                'pos': (254, 18)
            })
            await ctx.send(file=discord.File(res, 'failed.png'))

    @command('gruplan,plan')
    @cooldown(4)
    async def gru(self, ctx, *args):
        if '; ' not in ' '.join(list(args)): return await ctx.send(emote(self.client, 'error')+' | Please send something like:\n`'+cfg('PREFIX')+'gru test word 1; test word 2; test word 3` (with semicolons)')
        try:
            text1, text2, text3 = tuple(' '.join(list(args)).split('; '))
        except:
            return await ctx.send("Invalid arguments. use something like\n`"+cfg('PREFIX')+"gru text 1; text2; text3` (with semicolons)")
        async with ctx.channel.typing():
            im = self.client.canvas.gru(text1, text2, text3)
            return await ctx.send(file=discord.File(im, 'gru.png'))

    @command('worships,worshipping')
    @cooldown(3)
    async def worship(self, ctx, *args):
        av = getUserAvatar(ctx, args)
        async with ctx.channel.typing():
            im = self.client.gif.worship(av)
            await ctx.send(file=discord.File(im, 'worship.gif'))

    @command('crazy-frog,crazyfrogdance,dance,crazy-dance,kiddance,kid-dance')
    @cooldown(7)
    async def crazyfrog(self, ctx, *args):
        im = getUserAvatar(ctx, args, size=64)
        async with ctx.channel.typing():
            res = self.client.gif.crazy_frog_dance(im, self.frogMetadata)
            await ctx.send(file=discord.File(res, 'crazyfrog.gif'))

    @command('destroycomputer,smash')
    @cooldown(5)
    async def rage(self, ctx, *args):
        im = getUserAvatar(ctx, args, size=64)
        async with ctx.channel.typing():
            res = self.client.gif.destroy_computer(im, self.rageMetadata)
            await ctx.send(file=discord.File(res, 'rage.gif'))

    @command('disconnect')
    @cooldown(3)
    async def disconnected(self, ctx, *args):
        text = 'Forgotting to put the arguments' if len(list(args))==0 else ' '.join(list(args))
        async with ctx.channel.typing():
            im = self.client.canvas.disconnected(text)
            await ctx.send(file=discord.File(im, 'disconnected.png'))

    @command('blowup,blow,death-star')
    @cooldown(10)
    async def deathstar(self, ctx, *args):
        ava = getUserAvatar(ctx, args, size=128)
        async with ctx.channel.typing():
            gif = self.client.gif.death_star(ava)
            await ctx.send(file=discord.File(fp=gif, filename='boom.gif'))

    @command('effect')
    @cooldown(1)
    async def affect(self, ctx, *args):
        url = getUserAvatar(ctx, args)
        async with ctx.channel.typing():
            await ctx.send(file=discord.File(self.client.canvas.trans_merge({
                'url': url,
                'filename': 'affect.png',
                'size': (201, 163),
                'pos': (165, 352)
            }), 'affect.png'))

    @command('evol,trashevol,evoltrash,evolutiontrash')
    @cooldown(5)
    async def trashevolution(self, ctx, *args):
        url = getUserAvatar(ctx, args)
        async with ctx.channel.typing():
            await ctx.send(file=discord.File(
                self.client.canvas.evol(url), 'trashhahaha.png'
            ))

    @command('lookatthisgraph')
    @cooldown(5)
    async def graph(self, ctx, *args):
        src = getUserAvatar(ctx, args)
        async with ctx.channel.typing():
            await ctx.send(file=discord.File(self.client.canvas.lookatthisgraph(src), 'lookatthisdudelol.png'))
    
    @command('animegif,nj')
    @cooldown(10)
    async def nichijou(self, ctx, *args):
        text = 'LAZY PERSON' if (len(list(args))==0) else ' '.join(list(args))
        if len(text) > 22: return await ctx.send("{} | Text too long ;w;".format(emote(self.client, 'error')))
        async with ctx.channel.typing():
            async with self.session.get("https://i.ode.bz/auto/nichijou?text={}".format(urlify(text))) as r:
                res = await r.read()
                await ctx.send(file=discord.File(fp=BytesIO(res), filename="nichijou.gif"))
    
    @command('ifunny')
    @cooldown(5)
    async def wasted(self, ctx, *args):
        async with ctx.channel.typing():
            source = getUserAvatar(ctx, args, size=512)
            if 'wasted' in ctx.message.content: data, filename = self.client.canvas.wasted(source), 'wasted.png'
            else: data, filename = self.client.canvas.ifunny(source), 'ifunny.png'
            await ctx.send(file=discord.File(data, filename))
    
    @command('achieve,call')
    @cooldown(5)
    async def challenge(self, ctx, *args):
        if len(list(args))==0: await ctx.send(str(emote(self.client, 'error')+' | What is the challenge?'))
        else:
            async with ctx.channel.typing():
                txt = urlify(' '.join(args))
                if 'challenge' in str(ctx.message.content).split(' ')[0][1:]: url='https://api.alexflipnote.dev/challenge?text='+str(txt)
                elif 'call' in str(ctx.message.content).split(' ')[0][1:]: url='https://api.alexflipnote.dev/calling?text='+str(txt)
                else: url='https://api.alexflipnote.dev/achievement?text='+str(txt)
                await ctx.send(file=discord.File(self.client.canvas.urltoimage(url), 'minecraft_notice.png'))
    @command('dym')
    @cooldown(5)
    async def didyoumean(self, ctx, *args):
        if list(args)[0]=='help' or len(list(args))==0:
            embed = discord.Embed(title='didyoumean command help', description='Type like the following\n'+prefix+'didyoumean [text1] [text2]\n\nFor example:\n'+prefix+'didyoumean [i am gay] [i am guy]', colour=get_embed_color(discord))
            await ctx.send(embed=embed)
        else:
            try:
                async with ctx.channel.typing():
                    txt1, txt2 = urlify(str(ctx.message.content).split('[')[1][:-2]), urlify(str(ctx.message.content).split('[')[2][:-1])
                    url='https://api.alexflipnote.dev/didyoumean?top='+str(txt1)+'&bottom='+str(txt2)
                    await ctx.send(file=discord.File(self.client.canvas.urltoimage(url), 'didyoumean.png'))
            except IndexError:
                await ctx.send(str(emote(self.client, 'error')+' | error! invalid args!'))
    @command()
    @cooldown(5)
    async def drake(self, ctx, *args):
        unprefixed = ' '.join(list(args))
        if list(args)[0]=='help' or len(list(args))==0:
            embed = discord.Embed(
                title='Drake meme helper help',
                description='Type the following:\n`'+str(prefix)+'drake [text1] [text2]`\n\nFor example:\n`'+str(prefix)+'drake [test1] [test2]`'
            )
            await ctx.send(embed=embed)
        else:
            try:
                async with ctx.channel.typing():
                    txt1 = urlify(unprefixed.split('[')[1][:-2])
                    txt2 = urlify(unprefixed.split('[')[2][:-1])
                    url='https://api.alexflipnote.dev/drake?top='+str(txt1)+'&bottom='+str(txt2)
                    data = self.client.canvas.urltoimage(url)
                    await ctx.send(file=discord.File(data, 'drake.png'))
            except IndexError:
                await ctx.send(str(emote(self.client, 'error')+" | Please send something like {}drake [test 1] [test2]!".format(prefix)))
    
    @command()
    @cooldown(1)
    async def salty(self, ctx, *args):
        async with ctx.channel.typing():
            av = getUserAvatar(ctx, args)
            url = 'https://api.alexflipnote.dev/salty?image='+str(av)
            data = self.client.canvas.urltoimage(url)
            await ctx.send(file=discord.File(data, 'salty.png'))

    @command()
    @cooldown(5)
    async def ifearnoman(self, ctx, *args):
        async with ctx.channel.typing():
            source, by = getUserAvatar(ctx, args), str(ctx.author.avatar_url).replace('.webp?size=1024', '.png?size=512')
            await ctx.send(file=discord.File(self.client.canvas.ifearnoman(by, source), 'i_fear_no_man.png'))

    @command()
    @cooldown(5)
    async def triggered(self, ctx, *args):
        increment, accept = None, True
        for i in list(args):
            if i.isnumeric():
                increment = int(i)
                break
        if increment==None: increment = 5
        if increment!=5:
            if increment<1: 
                accept = False
                await ctx.send(str(emote(self.client, 'error') + " | Increment to small!"))
            elif increment>50:
                accept = False
                await ctx.send(str(emote(self.client, 'error') + " | Increment too big!"))
        if accept:
            if len(ctx.message.mentions)==0: ava = str(ctx.author.avatar_url).replace('.webp?size=1024', '.jpg?size=512')
            else: ava = str(ctx.message.mentions[0].avatar_url).replace('.webp?size=1024', '.jpg?size=512')
            async with ctx.channel.typing():
                data = self.client.gif.triggered(ava, increment)
                await ctx.send(file=discord.File(data, 'triggered.gif'))

    @command('communism,ussr,soviet,cykablyat,cyka-blyat,blyat')
    @cooldown(5)
    async def communist(self, ctx, *args):
        async with ctx.channel.typing():
            comrade = getUserAvatar(ctx, args, size=512)
            data = self.client.gif.communist(comrade)
            await ctx.send(file=discord.File(data, 'cyka_blyat.gif'))

    @command()
    @cooldown(5)
    async def trash(self, ctx, *args):
        async with ctx.channel.typing():
            av = ctx.author.avatar_url
            toTrash = getUserAvatar(ctx, args)
            url='https://api.alexflipnote.dev/trash?face='+str(av).replace('webp', 'png')+'&trash='+str(toTrash).replace('webp', 'png')
            data = self.client.canvas.urltoimage(url)
            await ctx.send(file=discord.File(data, 'trashed.png'))

    @command()
    @cooldown(8)
    async def squidwardstv(self, ctx, *args):
        source = getUserAvatar(ctx, args)
        await ctx.send(file=discord.File(self.client.canvas.squidwardstv(source), 'squidtv.png'))
    
    @command('mywaifu,wf,waifuinsult,insultwaifu,waifu-insult')
    @cooldown(7)
    async def waifu(self, ctx, *args):
        source = getUserAvatar(ctx, args)
        await ctx.send(file=discord.File(self.client.canvas.waifu(source), 'mywaifu.png'))

    @command('worsethanhitler,worstthanhitler')
    @cooldown(5)
    async def hitler(self, ctx, *args):
        async with ctx.channel.typing():
            source = getUserAvatar(ctx, args)
            im = self.client.gif.hitler(source)
            await ctx.send(file=discord.File(
                im, 'hitler.gif'
            ))

    @command('wanted,chatroulette,frame,art')
    @cooldown(10)
    async def ferbtv(self, ctx, *args):
        async with ctx.channel.typing():
            ava = getUserAvatar(ctx, args)
            if 'wanted' in ctx.message.content: size, pos = (547, 539), (167, 423)
            elif 'ferbtv' in ctx.message.content: size, pos = (362, 278), (364, 189)
            elif 'chatroulette' in ctx.message.content: size, pos = (324, 243), (14, 345)
            elif 'frame' in ctx.message.content: size, pos, ava = (1025, 715), (137, 141), str(ava).replace("=512", "=1024")
            if 'art' not in ctx.message.content: image = self.client.canvas.merge({
                'filename': ctx.message.content.split()[0][1:]+'.jpg',
                'url': ava,
                'size': size,
                'pos': pos
            })
            else: image = self.client.canvas.art(ava)
            await ctx.send(file=discord.File(image, 'memey.png'))

    
    @command()
    @cooldown(10)
    async def scroll(self, ctx, *args):
        if len(list(args))==0: await ctx.send(emote(self.client, 'error')+" | Error! where is your text?")
        else:
            async with ctx.channel.typing():
                scrolltxt = urlify(' '.join(list(args)))
                embed = discord.Embed(colour=get_embed_color(discord))
                url='https://api.alexflipnote.dev/scroll?text='+str(scrolltxt)
                data = self.client.canvas.urltoimage(url)
                await ctx.send(file=discord.File(data, 'scroll.png'))
    @command()
    @cooldown(10)
    async def imgcaptcha(self, ctx, *args):
        async with ctx.channel.typing():
            av, nm = getUserAvatar(ctx, args), getUser(ctx, args).name
            url = 'http://nekobot.xyz/api/imagegen?type=captcha&username='+nm+'&url='+av+'&raw=1'
            data = self.client.canvas.urltoimage(url)
            await ctx.send(file=discord.File(data, 'your_captcha.png'))

    @command('captchatext,captchatxt,generatecaptcha,gen-captcha,gencaptcha,capt')
    @cooldown(10)
    async def captcha(self, ctx, *args):
        async with ctx.channel.typing():
            capt = 'username601' if len(list(args))==0 else ' '.join(list(args))
            await ctx.send(file=discord.File(self.client.canvas.urltoimage('https://useless-api.vierofernando.repl.co/captcha?text={}'.format(capt)), 'captcha.png'))

    @command('baby,clint,wolverine,disgusting,f,studying,starvstheforcesof')
    @cooldown(10)
    async def door(self, ctx, *args):
        # yanderedev OwO
        async with ctx.channel.typing():
            ava = getUserAvatar(ctx, args)
            if 'door' in ctx.message.content: size, pos = (496, 483), (247, 9)
            elif 'studying' in ctx.message.content: size, pos = (290, 315), (85, 160)
            elif 'clint' in ctx.message.content: size, pos = (339, 629), (777, 29)
            elif 'starvstheforcesof' in ctx.message.content: size, pos = (995, 1079), (925, 0)
            elif 'wolverine' in ctx.message.content: size, pos = (368, 316), (85, 373)
            elif 'disgusting' in ctx.message.content: size, pos = (614, 407), (179, 24)
            elif 'f' in ctx.message.content and len(str(ctx.message.content).split(' ')[0])==2: size, pos = (82, 111), (361, 86)
            else: return await ctx.send(file=discord.File(self.client.canvas.baby(ava), 'lolmeme.png'))
            return await ctx.send(file=discord.File(self.client.canvas.trans_merge({
                'url': ava,
                'filename': ctx.message.content.split()[0][1:]+'.png',
                'size': size,
                'pos': pos
            }), 'meme.png'))

    @command('changedmymind')
    @cooldown(10)
    async def changemymind(self, ctx, *args):
        if len(list(args))==0: await ctx.send(emote(self.client, 'error')+" | Error! You need a text...")
        else:
            await ctx.message.add_reaction(emote(self.client, 'loading'))
            async with ctx.channel.typing():
                try:
                    data = self.client.canvas.urltoimage('https://nekobot.xyz/api/imagegen?type=changemymind&text='+urlify(' '.join(list(args)))+'&raw=1')
                    await ctx.send(file=discord.File(data, 'changemymind.png'))
                except Exception as e:
                    await ctx.send(emote(self.client, 'error')+" | Oops! There was an error on generating your meme; `"+str(e)+"`")

    @command('gimme,memz,memey')
    @cooldown(5)
    async def meme(self, ctx):
        data = fetchJSON("https://meme-api.herokuapp.com/gimme")
        embed = discord.Embed(colour = get_embed_color(discord))
        embed.set_author(name=data["title"], url=data["postLink"])
        if data["nsfw"]:
            embed.set_footer(text='WARNING: IMAGE IS NSFW.')
        else:
            embed.set_image(url=data["url"])
        await ctx.send(embed=embed)

    @command('kannagen')
    @cooldown(12)
    async def clyde(self, ctx, *args):
        if len(list(args))==0: await ctx.send('Please input a text...')
        else:
            async with ctx.channel.typing():
                url='https://nekobot.xyz/api/imagegen?type='+str(ctx.message.content).split(' ')[0][1:]+'&text='+urlify(' '.join(list(args)))+'&raw=1'
                await ctx.send(file=discord.File(self.client.canvas.urltoimage(url, stream=True), 'yolo.png'))

    @command()
    @cooldown(10)
    async def floor(self, ctx, *args):
        if len(list(args))==0: text = 'I forgot to put the arguments, oops'
        else: text = str(' '.join(args))
        auth = str(ctx.author.avatar_url).replace('.gif', '.webp').replace('.webp', '.png')
        async with ctx.channel.typing():
            if len(ctx.message.mentions)>0:
                auth = str(ctx.message.mentions[0].avatar_url).replace('.gif', '.webp').replace('.webp', '.png')
                if len(args)>2: text = str(ctx.message.content).split('> ')[1]
                else: text = 'I forgot to put the arguments, oops'
            await ctx.send(file=discord.File(self.client.canvas.urltoimage('https://api.alexflipnote.dev/floor?image='+auth+'&text='+urlify(text)), 'floor.png'))

    @command('bad')
    @cooldown(7)
    async def amiajoke(self, ctx, *args):
        source = getUserAvatar(ctx, args)
        if 'bad' in ctx.message.content: url = 'https://api.alexflipnote.dev/bad?image='+str(source)
        else: url = 'https://api.alexflipnote.dev/amiajoke?image='+str(source)
        await ctx.send(file=discord.File(self.client.canvas.urltoimage(url), 'maymays.png'))

    @command('avmeme,philosoraptor,money,doge,fry')
    @cooldown(12)
    async def wonka(self, ctx, *args):
        if 'avmeme' in ctx.message.content:
            async with ctx.channel.typing():
                try:
                    av = ctx.message.mentions[0].avatar_url
                    mes = ctx.message.content[int(len(args[0])+len(args[1])+1):]
                    top = urlify(str(ctx.message.content).split('[')[1].split(']')[0])
                    bott = urlify(str(ctx.message.content).split('[')[2].split(']')[0])
                    name = 'custom'
                    extr = '?alt='+str(av).replace('webp', 'png')
                    url='https://memegen.link/'+str(name)+'/'+str(top)+'/'+str(bott)+'.jpg'+str(extr)
                    await ctx.send(file=discord.File(self.client.canvas.memegen(url), 'avmeme.png'))
                except Exception as e:
                    await ctx.send(emote(self.client, 'error') +f' | Error!\n```{e}```Invalid parameters. Example: `{prefix}avmeme <tag someone> [top text] [bottom text]`')
        else:
            async with ctx.channel.typing():
                try:
                    top = urlify(str(ctx.message.content).split('[')[1].split(']')[0])
                    bott = urlify(str(ctx.message.content).split('[')[2].split(']')[0])
                    name = str(ctx.message.content).split(prefix)[1].split(' ')[0]
                    url='https://memegen.link/'+str(name)+'/'+str(top)+'/'+str(bott)+'.jpg?watermark=none'
                    await ctx.send(file=discord.File(self.client.canvas.memegen(url), args[0][1:]+'.png'))
                except Exception as e:
                    await ctx.send(emote(self.client, 'error') +f' | Error!\n```{e}```Invalid parameters.')
def setup(client):
    client.add_cog(memes(client))
