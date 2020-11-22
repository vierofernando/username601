import discord
from discord.ext import commands
import sys
from os import environ
sys.path.append(environ['BOT_MODULES_DIR'])
from io import BytesIO
from decorators import command, cooldown
from requests import get
from aiohttp import ClientSession
from json import loads

class memes(commands.Cog):
    def __init__(self, client):
        self.rawMetadata = open(client.utils.config('MODULES_DIR')+'/Animation.dat', 'r').read().split('\n')
        self.rageMetadata = list(map(
            lambda i: tuple(map(lambda a: int(a), i.split(','))),
            self.rawMetadata[0].split(';')
        ))
        self.frogMetadata = self.rawMetadata[1].split(':')
        self.meme_templates = loads(open(client.utils.config('JSON_DIR')+'/memes.json', 'r').read())

    @command()
    @cooldown(3)
    async def durv(self, ctx, *args):
        url = ctx.bot.utils.getUserAvatar(ctx, args)
        async with ctx.channel.typing():
            buffer = ctx.bot.canvas.trans_merge({
                'url': url,
                'filename': 'durv.png',
                'pos': (3, 1),
                'size': (158, 226)
            })
            return await ctx.send(file=discord.File(buffer, "durv.png"))

    @command()
    @cooldown(7)
    async def clint(self, ctx, *args):
        url = ctx.bot.utils.getUserAvatar(ctx, args)
        async with ctx.channel.typing():
            res = get("https://useless-api.vierofernando.repl.co/clint?image="+url, headers={"superdupersecretkey": environ["USELESSAPI"]}).content
            await ctx.send(file=discord.File(BytesIO(res), "clint.png"))

    @command("ltt,lienus")
    @cooldown(7)
    async def linus(self, ctx, *args):
        url = ctx.bot.utils.getUserAvatar(ctx, args)
        async with ctx.channel.typing():
            res = get("https://useless-api.vierofernando.repl.co/linus?image="+url, headers={"superdupersecretkey": environ["USELESSAPI"]}).content
            await ctx.send(file=discord.File(BytesIO(res), "lienus.png"))
    
    @command()
    @cooldown(7)
    async def folder(self, ctx, *args):
        url = ctx.bot.utils.getUserAvatar(ctx, args)
        async with ctx.channel.typing():
            res = get("https://useless-api.vierofernando.repl.co/folder?image="+url, headers={"superdupersecretkey": environ["USELESSAPI"]}).content
            await ctx.send(file=discord.File(BytesIO(res), "your_homework_folder.png"))

    @command('scoobydoo,reveal,revealed,expose,exposed,scooby-doo')
    @cooldown(2)
    async def scooby(self, ctx, *args):
        url = ctx.bot.utils.getUserAvatar(ctx, args)
        async with ctx.channel.typing():
            im = ctx.bot.canvas.scooby(url)
            return await ctx.send(file=discord.File(im, 'exposed.png'))

    @command('petition')
    @cooldown(2)
    async def presentation(self, ctx, *args):
        async with ctx.channel.typing():
            text = f'Petition for {ctx.author.name} to insert parameters' if len(args)==0 else ' '.join(args)
            im = ctx.bot.canvas.presentation(text)
            await ctx.send(file=discord.File(im, 'presentation.png'))

    @command('pass')
    @cooldown(1)
    async def password(self, ctx, *args):
        param = ctx.bot.utils.split_parameter_to_two(args)
        if param is None: raise ctx.bot.utils.send_error_message("Please send two parameters, either split by a space, a comma, or a semicolon.")
        async with ctx.channel.typing():
            text1, text2 = param
            i = ctx.bot.canvas.password(text1, text2)
            await ctx.send(file=discord.File(i, 'password.png'))

    @command('programmerhumor,programmermeme,programming,programmer')
    @cooldown(2)
    async def programmingmeme(self, ctx):
        data = ctx.bot.utils.fetchJSON('https://useless-api.vierofernando.repl.co/programmermeme')['url']
        return await ctx.send(embed=discord.Embed(title='Programmer meme', color=ctx.guild.me.roles[::-1][0].color).set_image(url=data))

    @command('shred,burn,spongebobpaper,paper,spongepaper,sponge-paper,spongebob-paper,spongebob')
    @cooldown(1)
    async def sponge(self, ctx, *args):
        async with ctx.channel.typing():
            av = ctx.bot.utils.getUserAvatar(ctx, args, size=512)
            im = ctx.bot.canvas.trans_merge({
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
            av = ctx.bot.utils.getUserAvatar(ctx, args)
            res = ctx.bot.canvas.trans_merge({
                'url': av,
                'filename': 'failed.png',
                'size': (155, 241),
                'pos': (254, 18)
            })
            await ctx.send(file=discord.File(res, 'failed.png'))

    @command('gruplan,plan')
    @cooldown(4)
    async def gru(self, ctx, *args):
        if '; ' not in ' '.join(args): raise ctx.bot.utils.send_error_message('Please send something like:\n`'+ctx.bot.command_prefix[0]+'gru test word 1; test word 2; test word 3` (with semicolons)')
        try:
            text1, text2, text3 = tuple(' '.join(args).split('; '))
        except:
            raise ctx.bot.utils.send_error_message("Invalid arguments. use something like\n`"+ctx.bot.command_prefix[0]+"gru text 1; text2; text3` (with semicolons)")
        async with ctx.channel.typing():
            im = ctx.bot.canvas.gru(text1, text2, text3)
            return await ctx.send(file=discord.File(im, 'gru.png'))

    @command('worships,worshipping')
    @cooldown(7)
    async def worship(self, ctx, *args):
        av = ctx.bot.utils.getUserAvatar(ctx, args)
        async with ctx.channel.typing():
            im = ctx.bot.gif.worship(av)
            await ctx.send(file=discord.File(im, 'worship.gif'))

    @command('crazy-frog,crazyfrogdance,dance,crazy-dance,kiddance,kid-dance')
    @cooldown(7)
    async def crazyfrog(self, ctx, *args):
        im = ctx.bot.utils.getUserAvatar(ctx, args, size=64)
        async with ctx.channel.typing():
            res = ctx.bot.gif.crazy_frog_dance(im, self.frogMetadata)
            await ctx.send(file=discord.File(res, 'crazyfrog.gif'))

    @command('destroycomputer,smash')
    @cooldown(5)
    async def rage(self, ctx, *args):
        im = ctx.bot.utils.getUserAvatar(ctx, args, size=64)
        async with ctx.channel.typing():
            res = ctx.bot.gif.destroy_computer(im, self.rageMetadata)
            await ctx.send(file=discord.File(res, 'rage.gif'))

    @command('disconnect')
    @cooldown(3)
    async def disconnected(self, ctx, *args):
        text = 'Forgotting to put the arguments' if len(args)==0 else ' '.join(args)
        async with ctx.channel.typing():
            im = ctx.bot.canvas.disconnected(text)
            await ctx.send(file=discord.File(im, 'disconnected.png'))

    @command('blowup,blow,death-star')
    @cooldown(10)
    async def deathstar(self, ctx, *args):
        ava = ctx.bot.utils.getUserAvatar(ctx, args, size=128)
        async with ctx.channel.typing():
            gif = ctx.bot.gif.death_star(ava)
            await ctx.send(file=discord.File(fp=gif, filename='boom.gif'))

    @command('effect')
    @cooldown(1)
    async def affect(self, ctx, *args):
        url = ctx.bot.utils.getUserAvatar(ctx, args)
        async with ctx.channel.typing():
            await ctx.send(file=discord.File(ctx.bot.canvas.trans_merge({
                'url': url,
                'filename': 'affect.png',
                'size': (201, 163),
                'pos': (165, 352)
            }), 'affect.png'))

    @command('evol,trashevol,evoltrash,evolutiontrash')
    @cooldown(5)
    async def trashevolution(self, ctx, *args):
        url = ctx.bot.utils.getUserAvatar(ctx, args)
        async with ctx.channel.typing():
            await ctx.send(file=discord.File(
                ctx.bot.canvas.evol(url), 'trashhahaha.png'
            ))

    @command('lookatthisgraph')
    @cooldown(5)
    async def graph(self, ctx, *args):
        src = ctx.bot.utils.getUserAvatar(ctx, args)
        async with ctx.channel.typing():
            await ctx.send(file=discord.File(ctx.bot.canvas.lookatthisgraph(src), 'lookatthisdudelol.png'))
    
    @command('animegif,nj')
    @cooldown(10)
    async def nichijou(self, ctx, *args):
        text = 'LAZY PERSON' if (len(args)==0) else ' '.join(args)
        if len(text) > 22: raise ctx.bot.utils.send_error_message("Text too long ;w;")
        async with ctx.channel.typing():
            async with ctx.bot.bot_session.get("https://i.ode.bz/auto/nichijou?text={}".format(ctx.bot.utils.encode_uri(text))) as r:
                res = await r.read()
                await ctx.send(file=discord.File(fp=BytesIO(res), filename="nichijou.gif"))
    
    @command('achieve,call')
    @cooldown(5)
    async def challenge(self, ctx, *args):
        if len(args)==0: raise ctx.bot.utils.send_error_message('What is the challenge?')
        else:
            async with ctx.channel.typing():
                txt = ctx.bot.utils.encode_uri(' '.join(args))
                if 'challenge' in ctx.message.content.split(' ')[0][1:]: url='https://api.alexflipnote.dev/challenge?text='+str(txt)
                elif 'call' in ctx.message.content.split(' ')[0][1:]: url='https://api.alexflipnote.dev/calling?text='+str(txt)
                else: url='https://api.alexflipnote.dev/achievement?text='+str(txt)
                return await ctx.bot.send_image_attachment(ctx, url, alexflipnote=True)

    @command('dym')
    @cooldown(2)
    async def didyoumean(self, ctx, *args):
        params = ctx.bot.utils.split_parameter_to_two(args)
        if params is None: raise ctx.bot.utils.send_error_message("Please send two parameters, either split by a space, a comma, or a semicolon.")
        txt1, txt2 = params
        url = f'https://api.alexflipnote.dev/didyoumean?top={txt1}&bottom={txt2}'
        return await ctx.bot.send_image_attachment(ctx, url, alexflipnote=True)
    
    @command()
    @cooldown(2)
    async def drake(self, ctx, *args):
        params = ctx.bot.utils.split_parameter_to_two(args)
        if params is None: raise ctx.bot.utils.send_error_message("Please send two parameters, either split by a space, a comma, or a semicolon.")
        txt1, txt2 = params
        url = "https://api.alexflipnote.dev/drake?top"+ctx.bot.utils.encode_uri(txt1)+"&bottom="+ctx.bot.utils.encode_uri(txt2)
        return await ctx.bot.send_image_attachment(ctx, url, alexflipnote=True)
            
    @command()
    @cooldown(1)
    async def salty(self, ctx, *args):
        async with ctx.channel.typing():
            av = ctx.bot.utils.getUserAvatar(ctx, args)
            url = 'https://api.alexflipnote.dev/salty?image='+str(av)
            return await ctx.bot.send_image_attachment(ctx, url, alexflipnote=True)

    @command()
    @cooldown(5)
    async def ifearnoman(self, ctx, *args):
        async with ctx.channel.typing():
            source, by = ctx.bot.utils.getUserAvatar(ctx, args), str(ctx.author.avatar_url_as(format='png', size=512))
            await ctx.send(file=discord.File(ctx.bot.canvas.ifearnoman(by, source), 'i_fear_no_man.png'))

    @command()
    @cooldown(10)
    async def triggered(self, ctx, *args):
        ava = ctx.bot.utils.getUserAvatar(ctx, args)
        async with ctx.channel.typing():
            data = ctx.bot.gif.triggered(ava)
            await ctx.send(file=discord.File(data, 'triggered.gif'))

    @command('communism,ussr,soviet,cykablyat,cyka-blyat,blyat')
    @cooldown(5)
    async def communist(self, ctx, *args):
        async with ctx.channel.typing():
            comrade = ctx.bot.utils.getUserAvatar(ctx, args, size=512)
            data = ctx.bot.gif.communist(comrade)
            await ctx.send(file=discord.File(data, 'cyka_blyat.gif'))

    @command()
    @cooldown(5)
    async def trash(self, ctx, *args):
        async with ctx.channel.typing():
            av = ctx.author.avatar_url_as(format='png')
            toTrash = ctx.bot.utils.getUserAvatar(ctx, args)
            url='https://api.alexflipnote.dev/trash?face='+str(av)+'&trash='+str(toTrash)
            return await ctx.bot.send_image_attachment(ctx, url, alexflipnote=True)

    @command()
    @cooldown(8)
    async def squidwardstv(self, ctx, *args):
        source = ctx.bot.utils.getUserAvatar(ctx, args)
        await ctx.send(file=discord.File(ctx.bot.canvas.squidwardstv(source), 'squidtv.png'))
    
    @command('mywaifu,wf,waifuinsult,insultwaifu,waifu-insult')
    @cooldown(7)
    async def waifu(self, ctx, *args):
        source = ctx.bot.utils.getUserAvatar(ctx, args)
        await ctx.send(file=discord.File(ctx.bot.canvas.waifu(source), 'mywaifu.png'))

    @command('worsethanhitler,worstthanhitler')
    @cooldown(5)
    async def hitler(self, ctx, *args):
        async with ctx.channel.typing():
            source = ctx.bot.utils.getUserAvatar(ctx, args)
            im = ctx.bot.gif.hitler(source)
            await ctx.send(file=discord.File(
                im, 'hitler.gif'
            ))

    @command('wanted,chatroulette,frame,art')
    @cooldown(10)
    async def ferbtv(self, ctx, *args):
        async with ctx.channel.typing():
            ava = ctx.bot.utils.getUserAvatar(ctx, args)
            if 'wanted' in ctx.message.content: size, pos = (547, 539), (167, 423)
            elif 'ferbtv' in ctx.message.content: size, pos = (362, 278), (364, 189)
            elif 'chatroulette' in ctx.message.content: size, pos = (324, 243), (14, 345)
            elif 'frame' in ctx.message.content: size, pos, ava = (1025, 715), (137, 141), str(ava).replace("=512", "=1024")
            if 'art' not in ctx.message.content: image = ctx.bot.canvas.merge({
                'filename': ctx.message.content.split()[0][1:]+'.jpg',
                'url': ava,
                'size': size,
                'pos': pos
            })
            else: image = ctx.bot.canvas.art(ava)
            await ctx.send(file=discord.File(image, 'memey.png'))

    
    @command()
    @cooldown(10)
    async def scroll(self, ctx, *args):
        if len(args)==0: raise ctx.bot.utils.send_error_message("Error! where is your text?")
        else:
            async with ctx.channel.typing():
                scrolltxt = ctx.bot.utils.encode_uri(' '.join(args))
                embed = discord.Embed(colour=ctx.guild.me.roles[::-1][0].color)
                url='https://api.alexflipnote.dev/scroll?text='+scrolltxt
                return await ctx.bot.send_image_attachment(ctx, url, alexflipnote=True)
    @command()
    @cooldown(10)
    async def imgcaptcha(self, ctx, *args):
        async with ctx.channel.typing():
            av, nm = ctx.bot.utils.getUserAvatar(ctx, args), ctx.bot.utils.getUser(ctx, args).name
            url = 'http://nekobot.xyz/api/imagegen?type=captcha&username='+nm+'&url='+av+'&raw=1'
            return await ctx.bot.send_image_attachment(ctx, url)

    @command('captchatext,captchatxt,generatecaptcha,gen-captcha,gencaptcha,capt')
    @cooldown(10)
    async def captcha(self, ctx, *args):
        async with ctx.channel.typing():
            capt = 'username601' if len(args)==0 else ' '.join(args)
            return await ctx.bot.send_image_attachment(ctx, 'https://useless-api.vierofernando.repl.co/captcha?text={}'.format(capt))

    @command('baby,wolverine,disgusting,f,studying,starvstheforcesof')
    @cooldown(10)
    async def door(self, ctx, *args):
        # yanderedev OwO
        async with ctx.channel.typing():
            ava = ctx.bot.utils.getUserAvatar(ctx, args)
            if 'door' in ctx.message.content: size, pos = (496, 483), (247, 9)
            elif 'studying' in ctx.message.content: size, pos = (290, 315), (85, 160)
            elif 'starvstheforcesof' in ctx.message.content: size, pos = (995, 1079), (925, 0)
            elif 'wolverine' in ctx.message.content: size, pos = (368, 316), (85, 373)
            elif 'disgusting' in ctx.message.content: size, pos = (614, 407), (179, 24)
            elif 'f' in ctx.message.content and len(ctx.message.content.split(' ')[0])==2: size, pos = (82, 111), (361, 86)
            else: return await ctx.send(file=discord.File(ctx.bot.canvas.baby(ava), 'lolmeme.png'))
            return await ctx.send(file=discord.File(ctx.bot.canvas.trans_merge({
                'url': ava,
                'filename': ctx.message.content.split()[0][1:]+'.png',
                'size': size,
                'pos': pos
            }), 'meme.png'))

    @command('changedmymind')
    @cooldown(10)
    async def changemymind(self, ctx, *args):
        if len(args)==0: raise ctx.bot.utils.send_error_message("Error! You need a text...")
        else:
            await ctx.message.add_reaction(ctx.bot.loading_emoji)
            async with ctx.channel.typing():
                return await ctx.bot.send_image_attachment(ctx, 'https://nekobot.xyz/api/imagegen?type=changemymind&text='+ctx.bot.utils.encode_uri(' '.join(args))+'&raw=1')

    @command('gimme,memz,memey')
    @cooldown(5)
    async def meme(self, ctx):
        data = ctx.bot.utils.fetchJSON("https://meme-api.herokuapp.com/gimme")
        embed = discord.Embed(colour = ctx.guild.me.roles[::-1][0].color)
        embed.set_author(name=data["title"], url=data["postLink"])
        if data["nsfw"]:
            embed.set_footer(text='WARNING: IMAGE IS NSFW.')
        else:
            embed.set_image(url=data["url"])
        await ctx.send(embed=embed)

    @command('kannagen')
    @cooldown(12)
    async def clyde(self, ctx, *args):
        if len(args)==0: await ctx.send('Please input a text...')
        else:
            async with ctx.channel.typing():
                url='https://nekobot.xyz/api/imagegen?type='+ctx.message.content.split(' ')[0][1:]+'&text='+ctx.bot.utils.encode_uri(' '.join(args))+'&raw=1'
                return await ctx.bot.send_image_attachment(ctx, url)

    @command()
    @cooldown(10)
    async def floor(self, ctx, *args):
        if len(args)==0: text = 'I forgot to put the arguments, oops'
        else: text = str(' '.join(args))
        auth = str(ctx.author.avatar_url_as(format='png'))
        async with ctx.channel.typing():
            if len(ctx.message.mentions)>0:
                auth = str(ctx.message.mentions[0].avatar_url_as(format='png'))
                if len(args)>2: text = ctx.message.content.split('> ')[1]
                else: text = 'I forgot to put the arguments, oops'
            return await ctx.bot.send_image_attachment(ctx, 'https://api.alexflipnote.dev/floor?image='+auth+'&text='+ctx.bot.utils.encode_uri(text), alexflipnote=True)

    @command('doctor,terrifying,terrified,eye-doctor,eyedoctor,scary,frightening')
    @cooldown(2)
    async def bad(self, ctx, *args):
        ava = ctx.bot.utils.getUserAvatar(ctx, args)
        async with ctx.channel.typing():
            im = ctx.bot.canvas.trans_merge({
                'url': ava,
                'filename': 'doctor.png',
                'pos': (348, 240),
                'size': (93, 107)
            })
            return await ctx.send(file=discord.File(im, 'holyshit.png'))

    @command()
    @cooldown(7)
    async def amiajoke(self, ctx, *args):
        source = ctx.bot.utils.getUserAvatar(ctx, args)
        url = 'https://api.alexflipnote.dev/amiajoke?image='+str(source)
        return await ctx.bot.send_image_attachment(ctx, url, alexflipnote=True)

    async def modern_meme(self, ctx, *args):
        keys = list(self.meme_templates["bottom_image"].keys())
        def check(m):
            if ((m.channel != ctx.channel) or (m.author != ctx.author)): return False
            elif (m.content in keys) and (not m.content.isnumeric()): return True
            elif (m.content.isnumeric()):
                if int(m.content) in range(1, len(keys)+1): return True
            return False
        await ctx.send(embed=discord.Embed(title="Please provide your meme template from the available ones below. (in number)", description="\n".join([
            str(i + 1)+". " + keys[i] for i in range(len(keys))
        ]), color=ctx.guild.me.roles[::-1][0].color))
        message = await ctx.bot.utils.wait_for_message(ctx, message=None, func=check, timeout=60.0)
        if message is None: raise ctx.bot.utils.send_error_message("You did not respond in time. Meme-generation canceled.")
        link = self.meme_templates["bottom_image"][(keys[int(message.content) - 1] if message.content.isnumeric() else message.content)]
        format_text = await ctx.bot.utils.wait_for_message(ctx, message="Now send your text content to be in the meme.", timeout=60.0)
        if format_text is None: raise ctx.bot.utils.send_error_message("You did not respond in time. Meme-generation canceled.")
        async with ctx.channel.typing():
            return ctx.bot.canvas.bottom_image_meme(link, format_text.content[0:640])

    async def top_bottom_text_meme(self, ctx, *args):
        keys = list(self.meme_templates["topbottom"].keys())
        def check(m):
            if ((m.channel != ctx.channel) or (m.author != ctx.author)): return False
            elif (m.content in keys) and (not m.content.isnumeric()): return True
            elif (m.content.isnumeric()):
                if int(m.content) in range(1, len(keys)+1): return True
            return False
        await ctx.send(embed=discord.Embed(title="Please provide your meme template from the available ones below. (in number)", description="\n".join([
            str(i + 1)+". " + keys[i] for i in range(len(keys))
        ]), color=ctx.guild.me.roles[::-1][0].color))
        message = await ctx.bot.utils.wait_for_message(ctx, message=None, func=check, timeout=60.0)
        if message is None: raise ctx.bot.utils.send_error_message("You did not respond in time. Meme-generation canceled.")
        link = self.meme_templates["topbottom"][(keys[int(message.content) - 1] if message.content.isnumeric() else message.content)]
        format_text = await ctx.bot.utils.wait_for_message(ctx, message="Now send your top text and bottom text. Splitted by either spaces, commas, semicolon, or |.", timeout=60.0)
        if format_text is None: raise ctx.bot.utils.send_error_message("You did not respond in time. Meme-generation canceled.")
        text1, text2 = ctx.bot.utils.split_parameter_to_two(format_text.content.split())
        url = link.replace("{TEXT1}", ctx.bot.utils.encode_uri(text1)[0:64]).replace("{TEXT2}", ctx.bot.utils.encode_uri(text2)[0:64])
        async with ctx.channel.typing():
            return await ctx.bot.send_image_attachment(ctx, url)

    async def custom_image_meme(self, ctx, *args):
        message = await ctx.bot.utils.wait_for_message(ctx, message="Please send a **Image URL/Attachment**, or\nSend a **ping/user ID/name** to format as an **avatar.**\nOr send `mine` to use your avatar instead.", timeout=60.0)
        if message is None: raise ctx.bot.utils.send_error_message("You did not input a text. Meme making canceled.")
        elif "mine" in message.content.lower(): url = ctx.author.avatar_url_as(size=512, format="png")
        else: url = ctx.bot.utils.getUserAvatar(message, tuple(message.content.split()))
        text = await ctx.bot.utils.wait_for_message(ctx, message="Send top text and bottom text. Splitted by a space, comma, semicolon, or |.", timeout=60.0)
        if text is None: raise ctx.bot.utils.send_error_message("You did not input a text. Meme making canceled.")
        text1, text2 = ctx.bot.utils.split_parameter_to_two(tuple(text.content.split()))
        async with ctx.channel.typing():
            return await ctx.bot.send_image_attachment(ctx, "https://api.memegen.link/images/custom/{}/{}.png?background={}".format(ctx.bot.utils.encode_uri(text1)[0:64], ctx.bot.utils.encode_uri(text2)[0:64], url))

    @command('memegen,meme-gen,gen-meme,generatememe,generate-meme,meme-editor,meme_editor,memeeditor')
    @cooldown(5)
    async def mememaker(self, ctx, *args):
        m = await ctx.send(embed=discord.Embed(title="Please select your meme format:", description="**[A] **Classic meme, Top text, bottom text, background image.\n**[B] **Modern meme, Top text, bottom image\n**[C] **Custom classic meme, with a custom background.", color=ctx.guild.me.roles[::-1][0].color))
        def check_chosen(m):
            return ((m.channel == ctx.channel) and (m.author == ctx.author) and (len(m.content) == 1) and m.content.lower() in ['a', 'b'])
        message = await ctx.bot.utils.wait_for_message(ctx, message=None, timeout=60.0)
        if message is None: return await m.edit(content='', embed=discord.Embed(title="Meme-making process canceled.", color=discord.Color.red()))
        elif message.content.lower() == 'a': res = await self.top_bottom_text_meme(ctx, *args)
        elif message.content.lower() == 'c': res = await self.custom_image_meme(ctx, *args)
        else: res = await self.modern_meme(ctx, *args)
        return await ctx.send(file=discord.File(res, "meme.png"))

def setup(client):
    client.add_cog(memes(client))