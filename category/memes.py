import discord
from discord.ext import commands
import sys
sys.path.append('/home/runner/hosting601/modules')
import canvas as Painter
from io import BytesIO
from decorators import command, cooldown
import username601 as myself
from username601 import *
from requests import get
from aiohttp import ClientSession

class memes(commands.Cog):
    def __init__(self, client):
        self.client = client
        self.session = ClientSession()
        self.rawMetadata = open(r'/home/runner/hosting601/modules/Animation.dat', 'r').read().split(';')
        self.rageMetadata = [tuple([int(a) for a in i.split(',')]) for i in self.rawMetadata]

    @command('destroycomputer,smash')
    @cooldown(5)
    async def rage(self, ctx, *args):
        im = myself.getUserAvatar(ctx, args, size=64)
        async with ctx.message.channel.typing():
            res = Painter.gif.destroy_computer(im, self.rageMetadata)
            await ctx.send(file=discord.File(res, 'rage.gif'))

    @command('disconnect')
    @cooldown(3)
    async def disconnected(self, ctx, *args):
        text = 'Forgotting to put the arguments' if len(list(args))==0 else ' '.join(list(args))
        async with ctx.message.channel.typing():
            im = Painter.disconnected(text)
            await ctx.send(file=discord.File(im, 'disconnected.png'))

    @command('blowup,blow,death-star')
    @cooldown(10)
    async def deathstar(self, ctx, *args):
        ava = myself.getUserAvatar(ctx, args, size=128)
        async with ctx.message.channel.typing():
            gif = Painter.gif.death_star(ava)
            await ctx.send(file=discord.File(fp=gif, filename='boom.gif'))

    @command('evol,trashevol,evoltrash,evolutiontrash')
    @cooldown(5)
    async def trashevolution(self, ctx, *args):
        url = myself.getUserAvatar(ctx, args)
        async with ctx.message.channel.typing():
            await ctx.send(file=discord.File(
                Painter.evol(url), 'trashhahaha.png'
            ))

    @command('nostonks,notstonk,nostonk')
    @cooldown(5)
    async def notstonks(self, ctx, *args):
        text = str(' '.join(list(args))) if (len(list(args))!=0) else "When you forgot to put the args:"
        if len(ctx.message.mentions)>0:
            url = "https://nezumiyuiz.glitch.me/api/notstonks?text={}&avatar={}".format(text.replace(ctx.message.mentions[0].mention, ""), str(ctx.message.mentions[0].avatar_url).replace('.gif', '.webp').replace('.webp?size=1024', '.png?size=512'))
        else:
            url = "https://nezumiyuiz.glitch.me/api/notstonks?text={}".format(text)
        try:
            async with ctx.message.channel.typing():
                await ctx.send(file=discord.File(
                    Painter.urltoimage(url), 'nostonks.png'
                ))
        except:
            await ctx.send('erorr')

    @command('lookatthisgraph')
    @cooldown(5)
    async def graph(self, ctx, *args):
        src = myself.getUserAvatar(ctx, args)
        async with ctx.message.channel.typing():
            await ctx.send(file=discord.File(Painter.lookatthisgraph(src), 'lookatthisdudelol.png'))
    
    @command('animegif,nj')
    @cooldown(10)
    async def nichijou(self, ctx, *args):
        text = 'LAZY PERSON' if (len(list(args))==0) else ' '.join(list(args))
        if len(text) > 22:
            await ctx.send("{} | Text too long ;w;".format(str(self.client.get_emoji(BotEmotes.error))))
            return
        async with ctx.message.channel.typing():
            async with self.session.get("https://i.ode.bz/auto/nichijou?text={}".format(myself.urlify(text))) as r:
                res = await r.read()
                await ctx.send(file=discord.File(fp=BytesIO(res), filename="nichijou.gif"))
    
    @command('ifunny')
    @cooldown(5)
    async def wasted(self, ctx, *args):
        async with ctx.message.channel.typing():
            source = myself.getUserAvatar(ctx, args, size=512)
            if 'wasted' in ctx.message.content: data, filename = Painter.wasted(source), 'wasted.png'
            else: data, filename = Painter.ifunny(source), 'ifunny.png'
            await ctx.send(file=discord.File(data, filename))
    
    @command('achieve,call')
    @cooldown(5)
    async def challenge(self, ctx, *args):
        if len(list(args))==0: await ctx.send(str(self.client.get_emoji(BotEmotes.error))+' | What is the challenge?')
        else:
            async with ctx.message.channel.typing():
                txt = myself.urlify(' '.join(args))
                if 'challenge' in str(ctx.message.content).split(' ')[0][1:]: url='https://api.alexflipnote.dev/challenge?text='+str(txt)
                elif 'call' in str(ctx.message.content).split(' ')[0][1:]: url='https://api.alexflipnote.dev/calling?text='+str(txt)
                else: url='https://api.alexflipnote.dev/achievement?text='+str(txt)
                await ctx.send(file=discord.File(Painter.urltoimage(url), 'minecraft_notice.png'))
    @command('dym')
    @cooldown(5)
    async def didyoumean(self, ctx, *args):
        if list(args)[0]=='help' or len(list(args))==0:
            embed = discord.Embed(title='didyoumean command help', description='Type like the following\n'+prefix+'didyoumean [text1] [text2]\n\nFor example:\n'+prefix+'didyoumean [i am gay] [i am guy]', colour=discord.Colour.from_rgb(201, 160, 112))
            await ctx.send(embed=embed)
        else:
            try:
                async with ctx.message.channel.typing():
                    txt1, txt2 = myself.urlify(str(ctx.message.content).split('[')[1][:-2]), myself.urlify(str(ctx.message.content).split('[')[2][:-1])
                    url='https://api.alexflipnote.dev/didyoumean?top='+str(txt1)+'&bottom='+str(txt2)
                    await ctx.send(file=discord.File(Painter.urltoimage(url), 'didyoumean.png'))
            except IndexError:
                await ctx.send(str(self.client.get_emoji(BotEmotes.error))+' | error! invalid args!')
    @command()
    @cooldown(5)
    async def drake(self, ctx, *args):
        unprefixed = ' '.join(list(args))
        if list(args)[0]=='help' or len(list(args))==0:
            embed = discord.Embed(
                title='Drake meme helper help',
                description='Type the following:\n`'+str(Config.prefix)+'drake [text1] [text2]`\n\nFor example:\n`'+str(Config.prefix)+'drake [test1] [test2]`'
            )
            await ctx.send(embed=embed)
        else:
            try:
                async with ctx.message.channel.typing():
                    txt1 = myself.urlify(unprefixed.split('[')[1][:-2])
                    txt2 = myself.urlify(unprefixed.split('[')[2][:-1])
                    url='https://api.alexflipnote.dev/drake?top='+str(txt1)+'&bottom='+str(txt2)
                    data = Painter.urltoimage(url)
                    await ctx.send(file=discord.File(data, 'drake.png'))
            except IndexError:
                await ctx.send(str(self.client.get_emoji(BotEmotes.error))+" | Please send something like {}drake [test 1] [test2]!".format(Config.prefix))
    
    @command()
    @cooldown(1)
    async def salty(self, ctx, *args):
        async with ctx.message.channel.typing():
            av = myself.getUserAvatar(ctx, args)
            url = 'https://api.alexflipnote.dev/salty?image='+str(av)
            data = Painter.urltoimage(url)
            await ctx.send(file=discord.File(data, 'salty.png'))

    @command()
    @cooldown(5)
    async def ifearnoman(self, ctx, *args):
        async with ctx.message.channel.typing():
            source, by = myself.getUserAvatar(ctx, args), str(ctx.author.avatar_url).replace('.webp?size=1024', '.png?size=512')
            await ctx.send(file=discord.File(Painter.ifearnoman(by, source), 'i_fear_no_man.png'))

    @command('presentation')
    @cooldown(5)
    async def firstwords(self, ctx, *args):
        unprefixed = ' '.join(list(args))
        if len(list(args))==0: await ctx.send(str(self.client.get_emoji(BotEmotes.error))+" | Where is the meme's context?")
        else:
            async with ctx.message.channel.typing():
                try:
                    if 'presentation' in ctx.message.content: data = Painter.presentationMeme(unprefixed, "./assets/pics/presentation.jpg")
                    else: data = Painter.firstwords(unprefixed, "./assets/pics/firstwords.jpg")
                    await ctx.send(file=discord.File(data, 'lol.png'))
                except Exception as e:
                    await ctx.send('Oopsies! There was an error on creating your chosen meme;\n'+str(e))

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
                await ctx.send(str(self.client.get_emoji(BotEmotes.error)) + " | Increment to small!")
            elif increment>50:
                accept = False
                await ctx.send(str(self.client.get_emoji(BotEmotes.error)) + " | Increment to big!")
        if accept:
            if len(ctx.message.mentions)==0: ava = str(ctx.message.author.avatar_url).replace('.webp?size=1024', '.jpg?size=512')
            else: ava = str(ctx.message.mentions[0].avatar_url).replace('.webp?size=1024', '.jpg?size=512')
            async with ctx.message.channel.typing():
                data = Painter.gif.triggered(ava, increment)
                await ctx.send(file=discord.File(data, 'triggered.gif'))

    @command('communism,ussr,soviet,cykablyat,cyka-blyat,blyat')
    @cooldown(5)
    async def communist(self, ctx, *args):
        async with ctx.message.channel.typing():
            comrade = myself.getUserAvatar(ctx, args, size=512)
            data = Painter.gif.communist(comrade)
            await ctx.send(file=discord.File(data, 'cyka_blyat.gif'))

    @command()
    @cooldown(5)
    async def trash(self, ctx):
        if len(ctx.message.mentions)==0: await ctx.send(str(self.client.get_emoji(BotEmotes.error))+' | Please mention someone....')
        else:
            async with ctx.message.channel.typing():
                av = ctx.message.author.avatar_url
                toTrash = ctx.message.mentions[0].avatar_url
                url='https://api.alexflipnote.dev/trash?face='+str(av).replace('webp', 'png')+'&trash='+str(toTrash).replace('webp', 'png')
                data = Painter.urltoimage(url)
                await ctx.send(file=discord.File(data, 'trashed.png'))

    @command()
    @cooldown(5)
    async def trap(self, ctx, *args):
        if len(ctx.message.mentions)==0:
            await ctx.send(str(self.client.get_emoji(BotEmotes.error)) +f' | Wrong.\nPlease try the correct like following:\n`{prefix}trap [tag]`')
        else:
            async with ctx.message.channel.typing():
                guy = myself.getUser(ctx, args)
                ava = myself.getUserAvatar(ctx, args)
                url='http://nekobot.xyz/api/imagegen?type=trap&name='+myself.urlify(guy.name)+'&author='+myself.urlify(ctx.author.name)+'&image='+ava+'&raw=1'
                await ctx.send(file=discord.File(Painter.urltoimage(url), 'trap.png'))

    @command('winorlose')
    @cooldown(10)
    async def whowouldwin(self, ctx):
        if len(ctx.message.mentions)!=2:
            await ctx.send('Please tag TWO people!')
        else:
            async with ctx.message.channel.typing():
                url='http://nekobot.xyz/api/imagegen?type=whowouldwin&raw=1&user1='+str(ctx.message.mentions[0].avatar_url).replace('.webp?size=1024', '.png')+'&user2='+str(ctx.message.mentions[1].avatar_url).replace('.webp?size=1024', '.png')
                await ctx.send(file=discord.File(Painter.urltoimage(url), 'whowouldwin.png'))

    @command()
    @cooldown(8)
    async def squidwardstv(self, ctx, *args):
        source = myself.getUserAvatar(ctx, *args)
        await ctx.send(file=discord.File(Painter.squidwardstv(source), 'squidtv.png'))
    
    @command('mywaifu,wf,waifuinsult,insultwaifu,waifu-insult')
    @cooldown(7)
    async def waifu(self, ctx, *args):
        source = myself.getUserAvatar(ctx, args)
        await ctx.send(file=discord.File(Painter.waifu(source), 'mywaifu.png'))

    @command('worsethanhitler,worstthanhitler')
    @cooldown(5)
    async def hitler(self, ctx, *args):
        source = myself.getUserAvatar(ctx, args)
        async with ctx.message.channel.typing():
            await ctx.send(file=discord.File(
                Painter.hitler(source), 'hitler.png'
            ))

    @command('wanted,chatroulette,frame,art')
    @cooldown(10)
    async def ferbtv(self, ctx, *args):
        async with ctx.message.channel.typing():
            filename = str(ctx.message.content).split()[0][1:].lower()
            ava = myself.getUserAvatar(ctx, args)
            if 'wanted' in ctx.message.content: num1, num2, num3, num4 = 547, 539, 167, 423
            elif 'ferbtv' in ctx.message.content: num1, num2, num3, num4 = 362, 278, 363, 187
            elif 'chatroulette' in ctx.message.content: num1, num2, num3, num4 = 324, 243, 14, 345
            elif 'frame' in ctx.message.content: num1, num2, num3, num4, ava = 1025, 715, 137, 141, str(ava).replace("=512", "=1024")
            if 'art' not in ctx.message.content: image = Painter.putimage(ava, filename, num1, num2, num3, num4)
            else: image = Painter.art(ava)
            await ctx.send(file=discord.File(image, str(ctx.message.content)[1:].replace(' ', '')+'.png'))

    
    @command()
    @cooldown(10)
    async def scroll(self, ctx, *args):
        if len(list(args))==0: await ctx.send(str(self.client.get_emoji(BotEmotes.error))+" | Error! where is your text?")
        else:
            async with ctx.message.channel.typing():
                scrolltxt = myself.urlify(' '.join(list(args)))
                embed = discord.Embed(colour=discord.Colour.from_rgb(201, 160, 112))
                url='https://api.alexflipnote.dev/scroll?text='+str(scrolltxt)
                data = Painter.urltoimage(url)
                await ctx.send(file=discord.File(data, 'scroll.png'))
    @command()
    @cooldown(10)
    async def imgcaptcha(self, ctx, *args):
        async with ctx.message.channel.typing():
            av, nm = myself.getUserAvatar(ctx, args), myself.getUser(ctx, args).name
            url = 'http://nekobot.xyz/api/imagegen?type=captcha&username='+nm+'&url='+av+'&raw=1'
            data = Painter.urltoimage(url)
            await ctx.send(file=discord.File(data, 'your_captcha.png'))
    
    @command()
    @cooldown(10)
    async def captcha(self, ctx, *args):
        async with ctx.message.channel.typing():
            capt = myself.urlify(' '.join(args))
            data = Painter.urltoimage('https://api.alexflipnote.dev/captcha?text='+str(capt))
            await ctx.send(file=discord.File(data, 'captcha.png'))

    @command('baby,clint,wolverine,disgusting,f,studying,starvstheforcesof')
    @cooldown(10)
    async def door(self, ctx, *args):
		# yanderedev OwO
        async with ctx.message.channel.typing():
            ava = myself.getUserAvatar(ctx, args)
            if 'door' in ctx.message.content: await ctx.send(file=discord.File(Painter.put_transparent(ava, "door", 1000, 479, 496, 483, 247, 9), 'door.png'))
            elif 'studying' in ctx.message.content: await ctx.send(file=discord.File(Painter.put_transparent(ava, "studying", 563, 999, 290, 315, 85, 160), "studying.png")) 
            elif 'clint' in ctx.message.content: await ctx.send(file=discord.File(Painter.put_transparent(ava, "clint", 1200, 675, 339, 629, 777, 29), 'clintclint.png'))
            elif 'starvstheforcesof' in ctx.message.content: await ctx.send(file=discord.File(Painter.put_transparent(ava, "starvstheforcesof", 1920, 1080, 995, 1079, 925, 0), "starvstheforcesof.png")) 
            elif 'wolverine' in ctx.message.content: await ctx.send(file=discord.File(Painter.put_transparent(ava, "wolverine", 450, 698, 368, 316, 85, 373), 'wolverine.png'))
            elif 'disgusting' in ctx.message.content: await ctx.send(file=discord.File(Painter.put_transparent(ava, "disgusting", 1024, 1080, 614, 407, 179, 24), 'disgusting.png'))
            elif 'f' in ctx.message.content and len(str(ctx.message.content).split(' ')[0])==2: await ctx.send(file=discord.File(Painter.f(ava), 'f.png'))
            else: await ctx.send(file=discord.File(Painter.baby(ava), 'lolmeme.png'))

    @command('changedmymind')
    @cooldown(10)
    async def changemymind(self, ctx, *args):
        if len(list(args))==0: await ctx.send(str(self.client.get_emoji(BotEmotes.error))+" | Error! You need a text...")
        else:
            await ctx.message.add_reaction(self.client.get_emoji(BotEmotes.loading))
            async with ctx.message.channel.typing():
                try:
                    data = Painter.urltoimage('https://nekobot.xyz/api/imagegen?type=changemymind&text='+myself.urlify(' '.join(list(args)))+'&raw=1')
                    await ctx.send(file=discord.File(data, 'changemymind.png'))
                except Exception as e:
                    await ctx.send(str(self.client.get_emoji(BotEmotes.error))+" | Oops! There was an error on generating your meme; `"+str(e)+"`")

    @command('gimme,memz,memey')
    @cooldown(5)
    async def meme(self, ctx):
        data = myself.api("https://meme-api.herokuapp.com/gimme")
        embed = discord.Embed(colour = discord.Colour.from_rgb(201, 160, 112))
        embed.set_author(name=data["title"], url=data["postLink"])
        if data["nsfw"]:
            embed.set_footer(text='WARNING: IMAGE IS NSFW.')
        else:
            embed.set_image(url=data["url"])
        await ctx.send(embed=embed)

    @command('trumptweet,kannagen')
    @cooldown(12)
    async def clyde(self, ctx, *args):
        if len(list(args))==0: await ctx.send('Please input a text...')
        else:
            async with ctx.message.channel.typing():
                url='https://nekobot.xyz/api/imagegen?type='+str(ctx.message.content).split(' ')[0][1:]+'&text='+myself.urlify(' '.join(list(args)))+'&raw=1'
                await ctx.send(file=discord.File(Painter.urltoimage(url), 'lawl.png'))

    @command()
    @cooldown(10)
    async def floor(self, ctx, *args):
        if len(list(args))==0: text = 'I forgot to put the arguments, oops'
        else: text = str(' '.join(args))
        auth = str(ctx.message.author.avatar_url).replace('.gif', '.webp').replace('.webp', '.png')
        async with ctx.message.channel.typing():
            if len(ctx.message.mentions)>0:
                auth = str(ctx.message.mentions[0].avatar_url).replace('.gif', '.webp').replace('.webp', '.png')
                if len(args)>2: text = str(ctx.message.content).split('> ')[1]
                else: text = 'I forgot to put the arguments, oops'
            await ctx.send(file=discord.File(Painter.urltoimage('https://api.alexflipnote.dev/floor?image='+auth+'&text='+myself.urlify(text)), 'floor.png'))

    @command('bad')
    @cooldown(7)
    async def amiajoke(self, ctx, *args):
        source = myself.getUserAvatar(ctx, args)
        if 'bad' in ctx.message.content: url = 'https://api.alexflipnote.dev/bad?image='+str(source)
        else: url = 'https://api.alexflipnote.dev/amiajoke?image='+str(source)
        await ctx.send(file=discord.File(Painter.urltoimage(url), 'maymays.png'))

    @command('avmeme,philosoraptor,money,doge,fry')
    @cooldown(12)
    async def wonka(self, ctx, *args):
        if 'avmeme' in ctx.message.content:
            async with ctx.message.channel.typing():
                try:
                    av = ctx.message.mentions[0].avatar_url
                    mes = ctx.message.content[int(len(args[0])+len(args[1])+1):]
                    top = myself.urlify(str(ctx.message.content).split('[')[1].split(']')[0])
                    bott = myself.urlify(str(ctx.message.content).split('[')[2].split(']')[0])
                    name = 'custom'
                    extr = '?alt='+str(av).replace('webp', 'png')
                    url='https://memegen.link/'+str(name)+'/'+str(top)+'/'+str(bott)+'.jpg'+str(extr)
                    await ctx.send(file=discord.File(Painter.memegen(url), 'avmeme.png'))
                except Exception as e:
                    await ctx.send(str(self.client.get_emoji(BotEmotes.error)) +f' | Error!\n```{e}```Invalid parameters. Example: `{prefix}avmeme <tag someone> [top text] [bottom text]`')
        else:
            async with ctx.message.channel.typing():
                try:
                    top = myself.urlify(str(ctx.message.content).split('[')[1].split(']')[0])
                    bott = myself.urlify(str(ctx.message.content).split('[')[2].split(']')[0])
                    name = str(ctx.message.content).split(Config.prefix)[1].split(' ')[0]
                    url='https://memegen.link/'+str(name)+'/'+str(top)+'/'+str(bott)+'.jpg?watermark=none'
                    await ctx.send(file=discord.File(Painter.memegen(url), args[0][1:]+'.png'))
                except Exception as e:
                    await ctx.send(str(self.client.get_emoji(BotEmotes.error)) +f' | Error!\n```{e}```Invalid parameters.')
def setup(client):
    client.add_cog(memes(client))
