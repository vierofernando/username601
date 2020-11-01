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
        self.client = client
        
        self.rawMetadata = open(self.client.utils.config('MODULES_DIR')+'/Animation.dat', 'r').read().split('\n')
        self.rageMetadata = [tuple([int(a) for a in i.split(',')]) for i in self.rawMetadata[0].split(';')]
        self.frogMetadata = self.rawMetadata[1].split(':')
        self.meme_templates = loads(open(self.client.utils.config('JSON_DIR')+'/memes.json', 'r').read())

    @command('fakemsgbox,fakemessagebox,messagebox,message-box,msg-box')
    @cooldown(3)
    async def msgbox(self, ctx, *args):
        async with ctx.channel.typing():
            res = self.client.utils.split_parameter_to_two(args)
            if res is None:
                raise self.client.utils.send_error_message("Plesae input two parameters, split by space, comma, semicolon, or |.")
            buffer = self.client.canvas.fake_message_box(res[0], res[1])
            return await ctx.send(file=discord.File(buffer, "msgbox.png"))

    @command('scoobydoo,reveal,revealed,expose,exposed,scooby-doo')
    @cooldown(2)
    async def scooby(self, ctx, *args):
        url = self.client.utils.getUserAvatar(ctx, args)
        async with ctx.channel.typing():
            im = self.client.canvas.scooby(url)
            return await ctx.send(file=discord.File(im, 'exposed.png'))

    @command('petition')
    @cooldown(2)
    async def presentation(self, ctx, *args):
        async with ctx.channel.typing():
            text = f'Petition for {ctx.author.name} to insert parameters' if len(args)==0 else ' '.join(args)
            im = self.client.canvas.presentation(text)
            await ctx.send(file=discord.File(im, 'presentation.png'))

    @command('pass')
    @cooldown(1)
    async def password(self, ctx, *args):
        param = self.client.utils.split_parameter_to_two(args)
        if param is None: raise self.client.utils.send_error_message("Please send two parameters, either split by a space, a comma, or a semicolon.")
        async with ctx.channel.typing():
            text1, text2 = param
            i = self.client.canvas.password(text1, text2)
            await ctx.send(file=discord.File(i, 'password.png'))

    @command('programmerhumor,programmermeme,programming,programmer')
    @cooldown(2)
    async def programmingmeme(self, ctx):
        data = self.client.utils.fetchJSON('https://useless-api.vierofernando.repl.co/programmermeme')['url']
        return await ctx.send(embed=discord.Embed(title='Programmer meme', color=ctx.guild.me.roles[::-1][0].color).set_image(url=data))

    @command('shred,burn,spongebobpaper,paper,spongepaper,sponge-paper,spongebob-paper,spongebob')
    @cooldown(1)
    async def sponge(self, ctx, *args):
        async with ctx.channel.typing():
            av = self.client.utils.getUserAvatar(ctx, args, size=512)
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
            av = self.client.utils.getUserAvatar(ctx, args)
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
        if '; ' not in ' '.join(args): raise self.client.utils.send_error_message('Please send something like:\n`'+self.client.command_prefix+'gru test word 1; test word 2; test word 3` (with semicolons)')
        try:
            text1, text2, text3 = tuple(' '.join(args).split('; '))
        except:
            raise self.client.utils.send_error_message("Invalid arguments. use something like\n`"+self.client.command_prefix+"gru text 1; text2; text3` (with semicolons)")
        async with ctx.channel.typing():
            im = self.client.canvas.gru(text1, text2, text3)
            return await ctx.send(file=discord.File(im, 'gru.png'))

    @command('worships,worshipping')
    @cooldown(3)
    async def worship(self, ctx, *args):
        av = self.client.utils.getUserAvatar(ctx, args)
        async with ctx.channel.typing():
            im = self.client.gif.worship(av)
            await ctx.send(file=discord.File(im, 'worship.gif'))

    @command('crazy-frog,crazyfrogdance,dance,crazy-dance,kiddance,kid-dance')
    @cooldown(7)
    async def crazyfrog(self, ctx, *args):
        im = self.client.utils.getUserAvatar(ctx, args, size=64)
        async with ctx.channel.typing():
            res = self.client.gif.crazy_frog_dance(im, self.frogMetadata)
            await ctx.send(file=discord.File(res, 'crazyfrog.gif'))

    @command('destroycomputer,smash')
    @cooldown(5)
    async def rage(self, ctx, *args):
        im = self.client.utils.getUserAvatar(ctx, args, size=64)
        async with ctx.channel.typing():
            res = self.client.gif.destroy_computer(im, self.rageMetadata)
            await ctx.send(file=discord.File(res, 'rage.gif'))

    @command('disconnect')
    @cooldown(3)
    async def disconnected(self, ctx, *args):
        text = 'Forgotting to put the arguments' if len(args)==0 else ' '.join(args)
        async with ctx.channel.typing():
            im = self.client.canvas.disconnected(text)
            await ctx.send(file=discord.File(im, 'disconnected.png'))

    @command('blowup,blow,death-star')
    @cooldown(10)
    async def deathstar(self, ctx, *args):
        ava = self.client.utils.getUserAvatar(ctx, args, size=128)
        async with ctx.channel.typing():
            gif = self.client.gif.death_star(ava)
            await ctx.send(file=discord.File(fp=gif, filename='boom.gif'))

    @command('effect')
    @cooldown(1)
    async def affect(self, ctx, *args):
        url = self.client.utils.getUserAvatar(ctx, args)
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
        url = self.client.utils.getUserAvatar(ctx, args)
        async with ctx.channel.typing():
            await ctx.send(file=discord.File(
                self.client.canvas.evol(url), 'trashhahaha.png'
            ))

    @command('lookatthisgraph')
    @cooldown(5)
    async def graph(self, ctx, *args):
        src = self.client.utils.getUserAvatar(ctx, args)
        async with ctx.channel.typing():
            await ctx.send(file=discord.File(self.client.canvas.lookatthisgraph(src), 'lookatthisdudelol.png'))
    
    @command('animegif,nj')
    @cooldown(10)
    async def nichijou(self, ctx, *args):
        text = 'LAZY PERSON' if (len(args)==0) else ' '.join(args)
        if len(text) > 22: raise self.client.utils.send_error_message("Text too long ;w;")
        async with ctx.channel.typing():
            async with self.client.bot_session.get("https://i.ode.bz/auto/nichijou?text={}".format(self.client.utils.encode_uri(text))) as r:
                res = await r.read()
                await ctx.send(file=discord.File(fp=BytesIO(res), filename="nichijou.gif"))
    
    @command('ifunny')
    @cooldown(5)
    async def wasted(self, ctx, *args):
        async with ctx.channel.typing():
            source = self.client.utils.getUserAvatar(ctx, args, size=512)
            if 'wasted' in ctx.message.content: data, filename = self.client.canvas.wasted(source), 'wasted.png'
            else: data, filename = self.client.canvas.ifunny(source), 'ifunny.png'
            await ctx.send(file=discord.File(data, filename))
    
    @command('achieve,call')
    @cooldown(5)
    async def challenge(self, ctx, *args):
        if len(args)==0: raise self.client.utils.send_error_message('What is the challenge?')
        else:
            async with ctx.channel.typing():
                txt = self.client.utils.encode_uri(' '.join(args))
                if 'challenge' in str(ctx.message.content).split(' ')[0][1:]: url='https://api.alexflipnote.dev/challenge?text='+str(txt)
                elif 'call' in str(ctx.message.content).split(' ')[0][1:]: url='https://api.alexflipnote.dev/calling?text='+str(txt)
                else: url='https://api.alexflipnote.dev/achievement?text='+str(txt)
                await ctx.send(file=discord.File(self.client.canvas.urltoimage(url), 'minecraft_notice.png'))

    @command('dym')
    @cooldown(2)
    async def didyoumean(self, ctx, *args):
        params = self.client.utils.split_parameter_to_two(args)
        if params is None: raise self.client.utils.send_error_message("Please send two parameters, either split by a space, a comma, or a semicolon.")
        txt1, txt2 = params
        url = f'https://api.alexflipnote.dev/didyoumean?top={txt1}&bottom={txt2}'
        data = self.client.canvas.urltoimage(url)
        await ctx.send(file=discord.File(data, 'drake.png'))
    
    @command()
    @cooldown(2)
    async def drake(self, ctx, *args):
        params = self.client.utils.split_parameter_to_two(args)
        if params is None: raise self.client.utils.send_error_message("Please send two parameters, either split by a space, a comma, or a semicolon.")
        txt1, txt2 = params
        url = f'https://api.alexflipnote.dev/drake?top={txt1}&bottom={txt2}'
        data = self.client.canvas.urltoimage(url)
        await ctx.send(file=discord.File(data, 'drake.png'))
            
    @command()
    @cooldown(1)
    async def salty(self, ctx, *args):
        async with ctx.channel.typing():
            av = self.client.utils.getUserAvatar(ctx, args)
            url = 'https://api.alexflipnote.dev/salty?image='+str(av)
            data = self.client.canvas.urltoimage(url)
            await ctx.send(file=discord.File(data, 'salty.png'))

    @command()
    @cooldown(5)
    async def ifearnoman(self, ctx, *args):
        async with ctx.channel.typing():
            source, by = self.client.utils.getUserAvatar(ctx, args), str(ctx.author.avatar_url_as(format='png', size=512))
            await ctx.send(file=discord.File(self.client.canvas.ifearnoman(by, source), 'i_fear_no_man.png'))

    @command()
    @cooldown(5)
    async def triggered(self, ctx, *args):
        ava = self.client.utils.getUserAvatar(ctx, args)
        test_arr = [i for i in list(args) if i.isnumeric()]
        increment = 5 if len(test_arr)==0 else test_arr[0]
        async with ctx.channel.typing():
            data = self.client.gif.triggered(ava, int(increment))
            await ctx.send(file=discord.File(data, 'triggered.gif'))

    @command('communism,ussr,soviet,cykablyat,cyka-blyat,blyat')
    @cooldown(5)
    async def communist(self, ctx, *args):
        async with ctx.channel.typing():
            comrade = self.client.utils.getUserAvatar(ctx, args, size=512)
            data = self.client.gif.communist(comrade)
            await ctx.send(file=discord.File(data, 'cyka_blyat.gif'))

    @command()
    @cooldown(5)
    async def trash(self, ctx, *args):
        async with ctx.channel.typing():
            av = ctx.author.avatar_url_as(format='png')
            toTrash = self.client.utils.getUserAvatar(ctx, args)
            url='https://api.alexflipnote.dev/trash?face='+str(av)+'&trash='+str(toTrash)
            data = self.client.canvas.urltoimage(url)
            await ctx.send(file=discord.File(data, 'trashed.png'))

    @command()
    @cooldown(8)
    async def squidwardstv(self, ctx, *args):
        source = self.client.utils.getUserAvatar(ctx, args)
        await ctx.send(file=discord.File(self.client.canvas.squidwardstv(source), 'squidtv.png'))
    
    @command('mywaifu,wf,waifuinsult,insultwaifu,waifu-insult')
    @cooldown(7)
    async def waifu(self, ctx, *args):
        source = self.client.utils.getUserAvatar(ctx, args)
        await ctx.send(file=discord.File(self.client.canvas.waifu(source), 'mywaifu.png'))

    @command('worsethanhitler,worstthanhitler')
    @cooldown(5)
    async def hitler(self, ctx, *args):
        async with ctx.channel.typing():
            source = self.client.utils.getUserAvatar(ctx, args)
            im = self.client.gif.hitler(source)
            await ctx.send(file=discord.File(
                im, 'hitler.gif'
            ))

    @command('wanted,chatroulette,frame,art')
    @cooldown(10)
    async def ferbtv(self, ctx, *args):
        async with ctx.channel.typing():
            ava = self.client.utils.getUserAvatar(ctx, args)
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
        if len(args)==0: raise self.client.utils.send_error_message("Error! where is your text?")
        else:
            async with ctx.channel.typing():
                scrolltxt = self.client.utils.encode_uri(' '.join(args))
                embed = discord.Embed(colour=ctx.guild.me.roles[::-1][0].color)
                url='https://api.alexflipnote.dev/scroll?text='+str(scrolltxt)
                data = self.client.canvas.urltoimage(url)
                await ctx.send(file=discord.File(data, 'scroll.png'))
    @command()
    @cooldown(10)
    async def imgcaptcha(self, ctx, *args):
        async with ctx.channel.typing():
            av, nm = self.client.utils.getUserAvatar(ctx, args), self.client.utils.getUser(ctx, args).name
            url = 'http://nekobot.xyz/api/imagegen?type=captcha&username='+nm+'&url='+av+'&raw=1'
            data = self.client.canvas.urltoimage(url)
            await ctx.send(file=discord.File(data, 'your_captcha.png'))

    @command('captchatext,captchatxt,generatecaptcha,gen-captcha,gencaptcha,capt')
    @cooldown(10)
    async def captcha(self, ctx, *args):
        async with ctx.channel.typing():
            capt = 'username601' if len(args)==0 else ' '.join(args)
            await ctx.send(file=discord.File(self.client.canvas.urltoimage('https://useless-api.vierofernando.repl.co/captcha?text={}'.format(capt)), 'captcha.png'))

    @command('baby,clint,wolverine,disgusting,f,studying,starvstheforcesof')
    @cooldown(10)
    async def door(self, ctx, *args):
        # yanderedev OwO
        async with ctx.channel.typing():
            ava = self.client.utils.getUserAvatar(ctx, args)
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
        if len(args)==0: raise self.client.utils.send_error_message("Error! You need a text...")
        else:
            await ctx.message.add_reaction(self.client.loading_emoji)
            async with ctx.channel.typing():
                try:
                    data = self.client.canvas.urltoimage('https://nekobot.xyz/api/imagegen?type=changemymind&text='+self.client.utils.encode_uri(' '.join(args))+'&raw=1')
                    await ctx.send(file=discord.File(data, 'changemymind.png'))
                except Exception as e:
                    raise self.client.utils.send_error_message("Oops! There was an error on generating your meme; `"+str(e)+"`")

    @command('gimme,memz,memey')
    @cooldown(5)
    async def meme(self, ctx):
        data = self.client.utils.fetchJSON("https://meme-api.herokuapp.com/gimme")
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
                url='https://nekobot.xyz/api/imagegen?type='+str(ctx.message.content).split(' ')[0][1:]+'&text='+self.client.utils.encode_uri(' '.join(args))+'&raw=1'
                await ctx.send(file=discord.File(self.client.canvas.urltoimage(url, stream=True), 'yolo.png'))

    @command()
    @cooldown(10)
    async def floor(self, ctx, *args):
        if len(args)==0: text = 'I forgot to put the arguments, oops'
        else: text = str(' '.join(args))
        auth = str(ctx.author.avatar_url_as(format='png'))
        async with ctx.channel.typing():
            if len(ctx.message.mentions)>0:
                auth = str(ctx.message.mentions[0].avatar_url_as(format='png'))
                if len(args)>2: text = str(ctx.message.content).split('> ')[1]
                else: text = 'I forgot to put the arguments, oops'
            await ctx.send(file=discord.File(self.client.canvas.urltoimage('https://api.alexflipnote.dev/floor?image='+auth+'&text='+self.client.utils.encode_uri(text)), 'floor.png'))

    @command('doctor,terrifying,terrified,eye-doctor,eyedoctor,scary,frightening')
    @cooldown(2)
    async def bad(self, ctx, *args):
        ava = self.client.utils.getUserAvatar(ctx, args)
        async with ctx.channel.typing():
            im = self.client.canvas.trans_merge({
                'url': ava,
                'filename': 'doctor.png',
                'pos': (348, 240),
                'size': (93, 107)
            })
            return await ctx.send(file=discord.File(im, 'holyshit.png'))

    @command()
    @cooldown(7)
    async def amiajoke(self, ctx, *args):
        source = self.client.utils.getUserAvatar(ctx, args)
        url = 'https://api.alexflipnote.dev/amiajoke?image='+str(source)
        await ctx.send(file=discord.File(self.client.canvas.urltoimage(url), 'maymays.png'))

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
        message = await self.client.utils.wait_for_message(self, ctx, message=None, func=check, timeout=60.0)
        if message is None: raise self.client.utils.send_error_message("You did not respond in time. Meme-generation canceled.")
        link = self.meme_templates["bottom_image"][(keys[int(message.content) - 1] if message.content.isnumeric() else message.content)]
        format_text = await self.client.utils.wait_for_message(self, ctx, message="Now send your text content to be in the meme.", timeout=60.0)
        if format_text is None: raise self.client.utils.send_error_message("You did not respond in time. Meme-generation canceled.")
        async with ctx.channel.typing():
            return self.client.canvas.bottom_image_meme(link, format_text.content[0:640])

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
        message = await self.client.utils.wait_for_message(self, ctx, message=None, func=check, timeout=60.0)
        if message is None: raise self.client.utils.send_error_message("You did not respond in time. Meme-generation canceled.")
        link = self.meme_templates["topbottom"][(keys[int(message.content) - 1] if message.content.isnumeric() else message.content)]
        format_text = await self.client.utils.wait_for_message(self, ctx, message="Now send your top text and bottom text. Splitted by either spaces, commas, semicolon, or |.", timeout=60.0)
        if format_text is None: raise self.client.utils.send_error_message("You did not respond in time. Meme-generation canceled.")
        text1, text2 = self.client.utils.split_parameter_to_two(format_text.content.split())
        url = link.replace("{TEXT1}", self.client.utils.encode_uri(text1)[0:64]).replace("{TEXT2}", self.client.utils.encode_uri(text2)[0:64])
        async with ctx.channel.typing():
            return self.client.canvas.urltoimage(url)

    async def custom_image_meme(self, ctx, *args):
        message = await self.client.utils.wait_for_message(self, ctx, message="Please send a **Image URL/Attachment**, or\nSend a **ping/user ID/name** to format as an **avatar.**\nOr send `mine` to use your avatar instead.", timeout=60.0)
        if message is None: raise self.client.utils.send_error_message("You did not input a text. Meme making canceled.")
        elif "mine" in message.content.lower(): url = ctx.author.avatar_url_as(size=512, format="png")
        else: url = self.client.utils.getUserAvatar(message, tuple(message.content.split()))
        text = await self.client.utils.wait_for_message(self, ctx, message="Send top text and bottom text. Splitted by a space, comma, semicolon, or |.", timeout=60.0)
        if text is None: raise self.client.utils.send_error_message("You did not input a text. Meme making canceled.")
        text1, text2 = self.client.utils.split_parameter_to_two(tuple(text.content.split()))
        async with ctx.channel.typing():
            return self.client.canvas.urltoimage("https://api.memegen.link/images/custom/{}/{}.png?background={}".format(self.client.utils.encode_uri(text1)[0:64], self.client.utils.encode_uri(text2)[0:64], url))

    @command('memegen,meme-gen,gen-meme,generatememe,generate-meme,meme-editor,meme_editor,memeeditor')
    @cooldown(5)
    async def mememaker(self, ctx, *args):
        m = await ctx.send(embed=discord.Embed(title="Please select your meme format:", description="**[A] **Classic meme, Top text, bottom text, background image.\n**[B] **Modern meme, Top text, bottom image\n**[C] **Custom classic meme, with a custom background.", color=ctx.guild.me.roles[::-1][0].color))
        def check_chosen(m):
            return ((m.channel == ctx.channel) and (m.author == ctx.author) and (len(m.content) == 1) and m.content.lower() in ['a', 'b'])
        message = await self.client.utils.wait_for_message(self, ctx, message=None, timeout=60.0)
        if message is None: return await m.edit(content="", embed=discord.Embed(title="Meme-making process canceled.", color=discord.Color.red()))
        elif message.content.lower() == 'a': res = await self.top_bottom_text_meme(ctx, *args)
        elif message.content.lower() == 'c': res = await self.custom_image_meme(ctx, *args)
        else: res = await self.modern_meme(ctx, *args)
        return await ctx.send(file=discord.File(res, "meme.png"))

def setup(client):
    client.add_cog(memes(client))