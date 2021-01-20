import discord
from discord.ext import commands
from io import BytesIO
from decorators import *
from aiohttp import ClientSession
from json import loads
from gc import collect

class memes(commands.Cog):
    def __init__(self, client):
        self.meme_templates = loads(open(client.util.json_dir+'/memes.json', 'r').read())
    
    @command(['ferb'])
    @cooldown(7)
    @permissions(bot=['attach_files'])
    async def ferbtv(self, ctx, *args):
        await ctx.trigger_typing()
        ava = await ctx.bot.Parser.parse_image(ctx, args)
        meme = await ctx.bot.canvas.trans_merge({
            'url': ava,
            'filename': 'studying.png',
            'size': (362, 278),
            'pos': (364, 189)
        })
        return await ctx.send_image(meme)
    
    @command()
    @cooldown(7)
    @permissions(bot=['attach_files'])
    async def studying(self, ctx, *args):
        await ctx.trigger_typing()
        ava = await ctx.bot.Parser.parse_image(ctx, args)
        meme = await ctx.bot.canvas.trans_merge({
            'url': ava,
            'filename': 'studying.png',
            'size': (290, 315),
            'pos': (85, 160)
        })
        return await ctx.send_image(meme)
    
    @command(['starvs'])
    @cooldown(7)
    @permissions(bot=['attach_files'])
    async def starvstheforcesof(self, ctx, *args):
        await ctx.trigger_typing()
        ava = await ctx.bot.Parser.parse_image(ctx, args)
        meme = await ctx.bot.canvas.trans_merge({
            'url': ava,
            'filename': 'starvstheforcesof.png',
            'size': (995, 1079),
            'pos': (925, 0)
        })
        return await ctx.send_image(meme)
    
    @command(['respects'])
    @cooldown(7)
    @permissions(bot=['attach_files'])
    async def f(self, ctx, *args):
        await ctx.trigger_typing()
        ava = await ctx.bot.Parser.parse_image(ctx, args)
        meme = await ctx.bot.canvas.trans_merge({
            'url': ava,
            'filename': 'f.png',
            'size': (82, 111),
            'pos': (361, 86)
        })
        return await ctx.send_image(meme)
    
    @command()
    @cooldown(7)
    @permissions(bot=['attach_files'])
    async def disgusting(self, ctx, *args):
        await ctx.trigger_typing()
        ava = await ctx.bot.Parser.parse_image(ctx, args)
        meme = await ctx.bot.canvas.trans_merge({
            'url': ava,
            'filename': 'disgusting.png',
            'size': (614, 407),
            'pos': (179, 24)
        })
        return await ctx.send_image(meme)
    
    @command()
    @cooldown(7)
    @permissions(bot=['attach_files'])
    async def door(self, ctx, *args):
        await ctx.trigger_typing()
        ava = await ctx.bot.Parser.parse_image(ctx, args)
        meme = await ctx.bot.canvas.trans_merge({
            'url': ava,
            'filename': 'door.png',
            'size': (496, 483),
            'pos': (247, 9)
        })
        return await ctx.send_image(meme)
        
    @command(['disaster-girl'])
    @cooldown(5)
    @permissions(bot=['attach_files'])
    async def disastergirl(self, ctx, *args):
        await ctx.trigger_typing()
        url = await ctx.bot.Parser.parse_image(ctx, args)
        buffer = await ctx.bot.Image.disaster_girl(url)
        await ctx.send_image(buffer)
        del buffer, url
        collect()
    
    @command(['oreomeme', 'oreo-meme'])
    @cooldown(5)
    @permissions(bot=['attach_files'])
    async def oreo(self, ctx, *args):
        try:
            my_oreo = ctx.bot.oreo(ctx.bot.util.assets_dir, "".join(args)[:40])
            meme = my_oreo.meme()
            
            await ctx.send_image(meme)
            
            my_oreo.eat()
        except Exception as e:
            raise ctx.error_message(str(e), description=("](" in str(e)))
        collect()
    
    @command()
    @cooldown(3)
    @permissions(bot=['attach_files'])
    async def oliy(self, ctx, *args):
        stretch = False
        parser = ctx.bot.Parser(args)
        parser.parse()
    
        if parser.has("stretch"):
            parser.shift("stretch")
            stretch = True
        
        url = await ctx.bot.Parser.parse_image(ctx, parser.other)
        await ctx.trigger_typing()
        buffer = await ctx.bot.canvas.trans_merge({
            'url': url,
            'filename': 'oliy.png',
            'pos': (-85, 555),
            'size': (460, 460)
        }) if (not stretch) else await ctx.bot.canvas.oliy_stretched(url)
        return await ctx.send_image(buffer)

    @command()
    @cooldown(7)
    @permissions(bot=['attach_files'])
    async def clint(self, ctx, *args):
        url = await ctx.bot.Parser.parse_image(ctx, args)
        await ctx.trigger_typing()
        buffer = await ctx.bot.Image.distort(url, "./assets/pics/clint.png", (((0,0),(899,0),(0,508),(899,508)),((590,127),(839,25),(590,381),(839,497))))
        await ctx.send_image(buffer)
        del buffer, url

    @command(['ltt', 'lienus'])
    @cooldown(7)
    @permissions(bot=['attach_files'])
    async def linus(self, ctx, *args):
        url = await ctx.bot.Parser.parse_image(ctx, args)
        await ctx.trigger_typing()
        buffer = await ctx.bot.Image.distort(url, "./assets/pics/linus.png", (((0,0),(961,0),(0,639),(961,639)),((56,183),(365,139),(106,563),(397,411))))
        await ctx.send_image(buffer)
        del buffer, url
        
    @command(['dir', 'directory'])
    @cooldown(7)
    @permissions(bot=['attach_files'])
    async def folder(self, ctx, *args):
        url = await ctx.bot.Parser.parse_image(ctx, args)
        await ctx.trigger_typing()
        buffer = await ctx.bot.Image.distort(url, "folder.png", (((0,0),(700,0),(0,589),(700,589)),((246,71),(524,137),(246,447),(524,512))))
        await ctx.send_image(buffer)
        del buffer, url
    
    @command(['pass'])
    @cooldown(2)
    @permissions(bot=['attach_files'])
    async def password(self, ctx, *args):
        param = ctx.bot.Parser.split_args(args)
        if not param:
            return await ctx.bot.cmds.invalid_args(ctx)
        await ctx.trigger_typing()
        text1, text2 = param
        i = await ctx.bot.canvas.password(text1, text2)
        await ctx.send_image(i)

    @command(['shred', 'sponge', 'spongebobpaper', 'spongebob'])
    @cooldown(2)
    @permissions(bot=['attach_files'])
    async def burn(self, ctx, *args):
        await ctx.trigger_typing()
        av = await ctx.bot.Parser.parse_image(ctx, args, size=512)
        im = await ctx.bot.canvas.trans_merge({
            'url': av,
            'filename': 'spongebobpaper.png',
            'pos': (29, 58),
            'size': (224, 259)
        })
        return await ctx.send_image(im)

    @command(['ihavefailedyou', 'fail'])
    @cooldown(2)
    @permissions(bot=['attach_files'])
    async def failed(self, ctx, *args):
        await ctx.trigger_typing()
        av = await ctx.bot.Parser.parse_image(ctx, args)
        res = await ctx.bot.canvas.trans_merge({
            'url': av,
            'filename': 'failed.png',
            'size': (155, 241),
            'pos': (254, 18)
        })
        await ctx.send_image(res)

    @command(['worships', 'worshipping'])
    @cooldown(7)
    @permissions(bot=['attach_files'])
    async def worship(self, ctx, *args):
        av = await ctx.bot.Parser.parse_image(ctx, args)
        await ctx.trigger_typing()
        im = await ctx.bot.gif.worship(av)
        await ctx.send_image(im, file_format='gif')

    @command(['disconnect'])
    @cooldown(3)
    @permissions(bot=['attach_files'])
    async def disconnected(self, ctx, *args):
        text = ' '.join(args) if args else 'Forgetting to put the arguments'
        await ctx.trigger_typing()
        im = await ctx.bot.canvas.disconnected(text)
        return await ctx.send_image(im)
        
    @command(['effect'])
    @cooldown(2)
    @permissions(bot=['attach_files'])
    async def affect(self, ctx, *args):
        url = await ctx.bot.Parser.parse_image(ctx, args)
        await ctx.trigger_typing()
        buffer = await ctx.bot.canvas.trans_merge({
            'url': url,
            'filename': 'affect.png',
            'size': (201, 163),
            'pos': (165, 352)
        })
        return await ctx.send_image(buffer)

    @command()
    @cooldown(5)
    @require_args()
    @permissions(bot=['attach_files'])
    async def challenge(self, ctx, *args):
        await ctx.trigger_typing()
        txt = ctx.bot.util.encode_uri(' '.join(args)[:50])
        return await ctx.send_image('https://api.alexflipnote.dev/challenge?text='+txt, alexflipnote=True)
    
    @command(['achievement'])
    @cooldown(5)
    @require_args()
    @permissions(bot=['attach_files'])
    async def achieve(self, ctx, *args):
        await ctx.trigger_typing()
        txt = ctx.bot.util.encode_uri(' '.join(args)[:50])
        return await ctx.send_image('https://api.alexflipnote.dev/achievement?text='+txt, alexflipnote=True)

    @command(['dym'])
    @cooldown(2)
    @permissions(bot=['attach_files'])
    async def didyoumean(self, ctx, *args):
        params = ctx.bot.Parser.split_args(args)
        if not params:
            return await ctx.bot.cmds.invalid_args(ctx)
        txt1, txt2 = params
        url = f'https://api.alexflipnote.dev/didyoumean?top={txt1[:50]}&bottom={txt2[:50]}'
        return await ctx.send_image(url, alexflipnote=True)
    
    @command()
    @cooldown(2)
    @permissions(bot=['attach_files'])
    async def drake(self, ctx, *args):
        params = ctx.bot.Parser.split_args(args)
        if not params:
            return await ctx.bot.cmds.invalid_args(ctx)
        txt1, txt2 = params
        url = "https://api.alexflipnote.dev/drake?top="+ctx.bot.util.encode_uri(txt1[:50])+"&bottom="+ctx.bot.util.encode_uri(txt2[:50])
        return await ctx.send_image(url, alexflipnote=True)
        
    @command()
    @cooldown(2)
    @permissions(bot=['attach_files'])
    async def what(self, ctx, *args):
        image = await ctx.bot.Parser.parse_image(ctx, args, cdn_only=True)
        return await ctx.send_image("https://api.alexflipnote.dev/what?image="+image, alexflipnote=True)

    @command()
    @cooldown(5)
    @permissions(bot=['attach_files'])
    async def ifearnoman(self, ctx, *args):
        await ctx.trigger_typing()
        source, by = await ctx.bot.Parser.parse_image(ctx, args), str(ctx.author.avatar_url_as(format='png', size=512))
        meme = await ctx.bot.canvas.ifearnoman(by, source)
        return await ctx.send_image(meme)

    @command()
    @cooldown(10)
    @permissions(bot=['attach_files'])
    async def triggered(self, ctx, *args):
        ava = await ctx.bot.Parser.parse_image(ctx, args)
        await ctx.trigger_typing()
        data = await ctx.bot.gif.triggered(ava)
        return await ctx.send_image(data, file_format='gif')

    @command(['communism', 'ussr', 'soviet', 'cykablyat', 'cyka-blyat', 'blyat'])
    @cooldown(5)
    @permissions(bot=['attach_files'])
    async def communist(self, ctx, *args):
        await ctx.trigger_typing()
        comrade = await ctx.bot.Parser.parse_image(ctx, args, size=512)
        data = await ctx.bot.gif.communist(comrade)
        return await ctx.send_image(data, file_format='gif')

    @command()
    @cooldown(5)
    @permissions(bot=['attach_files'])
    async def trash(self, ctx, *args):
        await ctx.trigger_typing()
        av = ctx.author.avatar_url_as(format='png')
        toTrash = await ctx.bot.Parser.parse_image(ctx, args, cdn_only=True)
        url='https://api.alexflipnote.dev/trash?face='+str(av)+'&trash='+toTrash
        return await ctx.send_image(url, alexflipnote=True)

    @command(['captchatext', 'generatecaptcha', 'gen-captcha', 'gencaptcha', 'capt'])
    @cooldown(10)
    @require_args()
    @permissions(bot=['attach_files'])
    async def captcha(self, ctx, *args):
        await ctx.trigger_typing()
        image = ctx.bot.Image.captcha(" ".join(args)[:50])
        await ctx.send_image(image)
        del image

    @command(['changedmymind', 'cmm'])
    @cooldown(10)
    @require_args()
    @permissions(bot=['attach_files'])
    async def changemymind(self, ctx, *args):
        await ctx.trigger_typing()
        return await ctx.send_image('https://nekobot.xyz/api/imagegen?type=changemymind&text='+ctx.bot.util.encode_uri(' '.join(args)[:50])+'&raw=1')

    @command(['gimme', 'memz', 'memey'])
    @cooldown(5)
    async def meme(self, ctx):
        data = await ctx.bot.util.request("https://meme-api.herokuapp.com/gimme", json=True)
        await ctx.embed(title=data["title"], url=data["postLink"], footer=("This image is NSFW. So i won't display the image here." if (data["nsfw"] and (not ctx.channel.nsfw)) else None), image=(None if (data["nsfw"] and (not ctx.channel.nsfw)) else data["url"]))
        del data

    @command()
    @cooldown(12)
    @require_args()
    @permissions(bot=['attach_files'])
    async def clyde(self, ctx, *args):
        await ctx.trigger_typing()
        url='https://nekobot.xyz/api/imagegen?type=clyde&text='+ctx.bot.util.encode_uri(' '.join(args)[:50])+'&raw=1'
        return await ctx.send_image(url)

    @command()
    @cooldown(10)
    @require_args()
    @permissions(bot=['attach_files'])
    async def floor(self, ctx, *args):
        auth = str(ctx.author.avatar_url_as(format='png'))
        await ctx.trigger_typing()
        if ctx.message.mentions:
            auth = str(ctx.message.mentions[0].avatar_url_as(format='png'))
            text = " ".join(ctx.message.content.replace(ctx.message.mentions[0].mention, "").split()[1:]) if args[2:] else 'I forgot to put the arguments, oops'
        return await ctx.send_image('https://api.alexflipnote.dev/floor?image='+auth+'&text='+ctx.bot.util.encode_uri(' '.join(args)[:50]), alexflipnote=True)

    @command(['doctor', 'terrifying', 'terrified', 'eye-doctor', 'eyedoctor', 'scary', 'frightening'])
    @cooldown(2)
    @permissions(bot=['attach_files'])
    async def bad(self, ctx, *args):
        ava = await ctx.bot.Parser.parse_image(ctx, args)
        await ctx.trigger_typing()
        im = await ctx.bot.canvas.trans_merge({
            'url': ava,
            'filename': 'doctor.png',
            'pos': (348, 240),
            'size': (93, 107)
        })
        return await ctx.send_image(im)

    async def modern_meme(self, ctx, *args):
        keys = list(self.meme_templates["bottom_image"].keys())
        await ctx.send(embed=discord.Embed(title="Please provide your meme template from the available ones below. (in number)", description="\n".join([
            str(i + 1)+". " + keys[i] for i in range(len(keys))
        ]), color=ctx.me.color))
        wait = ctx.bot.WaitForMessage(ctx, check=(lambda x: x.channel == ctx.channel and x.author == ctx.author and ((x.content in keys) or (x.content.isnumeric() and int(x.content) in range(1, len(keys) + 1)))), timeout=60.0)
        message = await wait.get_message()
        
        if not message:
            raise ctx.error_message("You did not respond in time. Meme-generation canceled.")
        
        link = self.meme_templates["bottom_image"][(keys[int(message.content) - 1] if message.content.isnumeric() else message.content)]
        
        await ctx.send("Now send your text content to be in the meme.")
        wait = ctx.bot.WaitForMessage(ctx, check=(lambda x: x.channel == ctx.channel and x.author == ctx.author), timeout=60.0)
        format_text = await wait.get_message()
        
        if not format_text:
            raise ctx.error_message("You did not respond in time. Meme-generation canceled.")
        await ctx.trigger_typing()
        buffer = await ctx.bot.canvas.bottom_image_meme(link, format_text.content[:150])
        await ctx.send_image(buffer)
        del buffer, format_text, wait, link, message, keys

    async def top_bottom_text_meme(self, ctx, *args):
        keys = list(self.meme_templates["topbottom"].keys())
        await ctx.send(embed=discord.Embed(title="Please provide your meme template from the available ones below. (in number)", description="\n".join([
            str(i + 1)+". " + keys[i] for i in range(len(keys))
        ]), color=ctx.me.color))
        wait = ctx.bot.WaitForMessage(ctx, check=(lambda x: x.channel == ctx.channel and x.author == ctx.author and (x.content in keys or (x.content.isnumeric() and int(x.content) in range(1, len(keys)+1)))), timeout=60.0)
        message = await wait.get_message()
        
        if not message: raise ctx.error_message("You did not respond in time. Meme-generation canceled.")
        link = self.meme_templates["topbottom"][(keys[int(message.content) - 1] if message.content.isnumeric() else message.content)]
        
        await ctx.send("Now send your top text and bottom text. Splitted by either spaces, commas, semicolon, or |.")
        wait = ctx.bot.WaitForMessage(ctx, check=(lambda x: x.channel == ctx.channel and x.author == ctx.author), timeout=60.0)
        format_text = await wait.get_message()
        
        if not format_text:
            raise ctx.error_message("You did not respond in time. Meme-generation canceled.")
        
        text1, text2 = ctx.bot.Parser.split_args(format_text.content.split())
        url = link.replace("{TEXT1}", ctx.bot.util.encode_uri(text1)[:64]).replace("{TEXT2}", ctx.bot.util.encode_uri(text2)[:64])
        await ctx.trigger_typing()
        return await ctx.send_image(url)

    async def custom_image_meme(self, ctx, *args):
        await ctx.send("Please send a **Image URL/Attachment**, or\nSend a **ping/user ID/name** to format as an **avatar.**\nOr send `mine` to use your avatar instead.")
        wait = ctx.bot.WaitForMessage(ctx, check=(lambda x: x.author == ctx.author and x.channel == ctx.channel), timeout=60.0)
        message = await wait.get_message()
        
        if not message: raise ctx.error_message("You did not input a text. Meme making canceled.")
        elif "mine" in message.content.lower(): url = ctx.author.avatar_url_as(size=512, format="png")
        else:
            ctx = await ctx.bot.get_context(message)
            url = await ctx.bot.Parser.parse_image(ctx, tuple(message.content.split()))
        
        await ctx.send("Send top text and bottom text. Splitted by a space, comma, semicolon, or |.")
        wait = ctx.bot.WaitForMessage(ctx, check=(lambda x: x.author == ctx.author and x.channel == ctx.channel), timeout=60.0)
        text = await wait.get_message()
        
        if not text:
            raise ctx.error_message("You did not input a text. Meme making canceled.")
        
        text1, text2 = ctx.bot.Parser.split_args(tuple(text.content.split()))
        await ctx.trigger_typing()
        return await ctx.send_image("https://api.memegen.link/images/custom/{}/{}.png?background={}".format(ctx.bot.util.encode_uri(text1)[:64], ctx.bot.util.encode_uri(text2)[:64], url))

    @command(['mememaker', 'meme-gen', 'meme-editor', 'memeeditor'])
    @cooldown(5)
    @permissions(bot=['attach_files'])
    async def memegen(self, ctx, *args):
        m = await ctx.send(embed=discord.Embed(title="Please select your meme format:", description="**[A] **Classic meme, Top text, bottom text, background image.\n**[B] **Modern meme, Top text, bottom image\n**[C] **Custom classic meme, with a custom background.", color=ctx.me.color))
        
        wait = ctx.bot.WaitForMessage(ctx, check=(lambda x: x.channel == ctx.channel and x.author == ctx.author and len(x.content) == 1 and x.content.lower() in ['a', 'b', 'c']), timeout=40.0)
        message = await wait.get_message()
        del wait
        if not message:
            return await m.edit(embed=discord.Embed(title="Meme-making process canceled.", color=discord.Color.red()))
        elif message.content.lower() == 'a': return await self.top_bottom_text_meme(ctx, *args)
        elif message.content.lower() == 'c': return await self.custom_image_meme(ctx, *args)
        return await self.modern_meme(ctx, *args)

def setup(client):
    client.add_cog(memes(client))