import discord
import random
from discord.ext import commands
from decorators import *
from io import BytesIO
from json import loads
from time import time
from datetime import datetime as t
from re import search
from PIL import ImageColor

class utils(commands.Cog):
    def __init__(self):
        self._fact_urls = {
            "cat": ("https://catfact.ninja/fact", "fact", None),
            "dog": ("https://dog-api.kinduff.com/api/facts", "facts", 0),
            "fun": ("https://useless-api--vierofernando.repl.co/randomfact", "fact", None)
        }
        self.replaceWith = "x>*;.>*;?>*;?>/;?>*;plus>+;minus>-;divide>/;multiply>*;divide by>/;times>*;subtract>-;add>+;power>**;powers>**;^>**"

    def python_calc(self, args):
        equation = ' '.join(args)
        for rep in self.replaceWith.split(";"):
            equation = equation.replace(rep.split('>')[0], rep.split('>')[1])
        return equation

    @command(['nation'])
    @cooldown(5)
    async def country(self, ctx, *args):
        _country = " ".join(args)
        try:
            assert _country, "Send a country name!"
            data = await ctx.bot.util.get_request(f'https://restcountries.eu/rest/v2/name/{ctx.bot.util.encode_uri(_country)}', json=True, raise_errors=True)
            assert isinstance(data, list), "No such country with the name `"+_country+"` found."            
            embed = ctx.bot.ChooseEmbed(ctx, data, key=(lambda x: x["name"]))
            res = await embed.run()
            if not res:
                return
            embed = ctx.bot.Embed(
                ctx,
                title=res["name"],
                desc="Native name: \""+str(res.get("nativeName"))+"\"",
                fields={
                    "Location": "**Latitude Longitude:** `"+(", ".join([str(i) for i in res["latlng"]]))+"`\n**Region:** "+res["region"]+"\n**Subregion: **"+res["subregion"]+"\n**Capital:** "+res["capital"],
                    "Detailed Info": "**Population Count: **"+str(res["population"])+"\n**Country Area: **"+str(res.get("area"))+" km²\n**Time Zones: **"+(", ".join(res["timezones"])),
                    "Currency": (("\n".join(["**"+currency["name"]+"** ("+currency["code"]+" `"+currency["symbol"]+"`)" for currency in res["currencies"]])) if res["currencies"] else "`doesn't have currency :(`")
                }
            )
            return await embed.send()
        except Exception as e:
            raise ctx.bot.util.BasicCommandException(str(e))
    
    @command()
    @cooldown(3)
    @require_args()
    async def gradient(self, ctx, *args):
        await ctx.trigger_typing()
        if len(args) == 1:
            color_left, color_right = ImageColor.getrgb(args[0]), None
        else:
            left, right = ctx.bot.Parser.split_args(args)
            color_left, color_right = ImageColor.getrgb(left), ImageColor.getrgb(right)
        if color_left == color_right:
            raise ctx.bot.util.BasicCommandException("Those two colors are the same :/")
        res = await ctx.bot.canvas.gradient(color_left, color_right)
        await ctx.send(file=discord.File(res, "gradient.png"))
        del res, color_left, color_right
    
    @command(['trending', 'news'])
    @cooldown(5)
    async def msn(self, ctx, *args):
        try:
            data = await ctx.bot.util.get_request(
                "http://cdn.content.prod.cms.msn.com/singletile/summary/alias/experiencebyname/today",
                raise_errors=True,
                market="en-GB",
                source="appxmanifest",
                tenant="amp",
                vertical="news"
            )
            imageURL = data.split('baseUri="')[1].split('"')[0] + data.split('src="')[1].split('?')[0].replace(".img", ".png")
            content = data.split('hint-wrap="true">')[1].split('<')[0]
            embed = ctx.bot.Embed(ctx, title=content, image=imageURL)
            await embed.send()
            del embed, content, imageURL, data
        except Exception as e:
            await ctx.bot.get_user(ctx.bot.util.owner_id).send(f"yo, theres an error: `{str(e)}`")
            raise ctx.bot.util.BasicCommandException("Oopsies, there was an error on searching the news.")
    
    @command(['colorthief', 'getcolor', 'accent', 'accentcolor', 'accent-color', 'colorpalette', 'color-palette'])
    @cooldown(3)
    async def palette(self, ctx, *args):
        url = await ctx.bot.Parser.parse_image(ctx, args)
        await ctx.trigger_typing()
        palette = await ctx.bot.canvas.get_palette(ctx.bot.canvas.get_multiple_accents(url))
        await ctx.send(file=discord.File(palette, 'palette.png'))
        del palette, url

    @command(['pip'])
    @cooldown(3)
    @require_args()
    async def pypi(self, ctx, *args):
        await ctx.trigger_typing()
        
        data = await ctx.bot.util.get_request(
            "https://pypi.org/pypi/"+ "-".join(args) +"/json",
            json=True,
            raise_errors=True
        )
        
        nl = "\n"
        embed = ctx.bot.Embed(
            ctx,
            title=data['info']['name'],
            desc=data['info']['summary'],
            fields={
                "Links": f"**Home Page: **{'[click here]('+data['info']['home_page']+')' if data['info']['home_page'] else '`<no links available>`'}{nl}**Download Link: **{'[click here]('+data['info']['download_url']+')' if data['info']['download_url'] else '`<no links available>`'}",
                "Author": f"{data['info']['author']} {'('+data['info']['author_email']+')' if data['info']['author_email'] else ''}{nl}",
                "Version": f"**Current Version: **[{data['info']['version']}]({data['info']['release_url']}){nl}**Uploaded at: **{data['releases'][data['info']['version']][0]['upload_time'].replace('T', ' ')}",
                "Keywords": data['info']['keywords'].replace(',', ', ') if data['info']['keywords'] else '`<no keywords>`'
            },
            url=data['info']['package_url']
        )
        await embed.send()
        
        del embed, data, nl

    @command(['isitup', 'webstatus'])
    @cooldown(2)
    @require_args()
    async def isitdown(self, ctx, *args):
        wait = await ctx.send('{} | Pinging...'.format(ctx.bot.util.loading_emoji))
        web = args[0].replace('<', '').replace('>', '')
        if not web.startswith('http'): web = 'http://' + web
        try:
            a = time()
            ping = await ctx.bot.util.default_client.get(web)
            pingtime = round((time() - a)*1000)
            embed = ctx.bot.Embed(ctx, title="That website is up.", fields={"Ping": f"{pingtime}ms", "HTTP Status Code": f"{ping.status} {ctx.bot.util.status_codes[str(ping.status)]}", "Content Type": ping.headers['Content-Type']}, color=discord.Color.green())
            await embed.edit_to(wait)
            del embed, pingtime, ping, a, web, wait
        except:
            embed = ctx.bot.Embed(ctx, title="That website is down.", color=discord.Color.red())
            await embed.edit_to(wait)

    @command(['img2ascii', 'imagetoascii', 'avascii', 'avatarascii', 'avatar2ascii', 'av2ascii', 'asciify'])
    @cooldown(10)
    async def imgascii(self, ctx, *args):
        input = ctx.bot.Parser.get_input(args)
        
        if "--img" in input:
            args = ctx.bot.Parser.without(args, "--img")
            url = await ctx.bot.Parser.parse_image(ctx, args)
            await ctx.trigger_typing()
            res_im = await ctx.bot.canvas.imagetoASCII_picture(url)
            await ctx.send(file=discord.File(res_im, 'imgascii.png'))
            del res_im, url, args
            return
        
        url = await ctx.bot.Parser.parse_image(ctx, args)
        text = await ctx.bot.canvas.imagetoASCII(url)
        await ctx.send(file=discord.File(BytesIO(bytes(text, 'utf-8')), filename='ascii.txt'))
        del url, text, input
    
    @command()
    @cooldown(15)
    async def nasa(self, ctx, *args):
        query = ctx.bot.util.encode_uri('earth' if len(args)==0 else ' '.join(args))
        await ctx.trigger_typing()
        
        data = await ctx.bot.util.default_client.get(f'https://images-api.nasa.gov/search?q={query[0:100]}&media_type=image')
        try: data = await data.json()
        except: data = None
        if (data is None) or len(data['collection']['items'])==0:
            raise ctx.bot.util.BasicCommandException("Nothing found.")
        img = random.choice(data['collection']['items'])
        em = ctx.bot.Embed(
            ctx,
            title=img['data'][0]['title'],
            desc=img['data'][0]["description"],
            image=img['links'][0]['href']
        )
        await embed.send()
        del em, img, data

    @command(['pokemon', 'pokeinfo', 'dex', 'bulbapedia'])
    @cooldown(10)
    @require_args()
    async def pokedex(self, ctx, *args):
        try:
            data = await ctx.bot.util.get_request(
                'https://bulbapedia.bulbagarden.net/w/api.php',
                json=True,
                raise_errors=True,
                action='query',
                titles=' '.join(args)[0:100],
                format='json',
                formatversion=2,
                pithumbsize=150,
                prop='extracts|pageimages',
                explaintext='',
                redirects='',
                exintro=''
            )
            
            try: image = data['query']['pages'][0]['thumbnail']['source']
            except: image = None

            embed = ctx.bot.Embed(
                ctx,
                url=f'https://bulbapedia.bulbagarden.net/wiki/{data["query"]["pages"][0]["title"].replace(" ", "_")}',
                title=data['query']['pages'][0]['title'],
                desc=data['query']['pages'][0]['extract'][0:1000],
                image=image
            )
            await ctx.send(embed=embed)
            del embed, image, data
        except:
            raise ctx.bot.util.BasicCommandException("Pokemon not found.")

    @command(['recipes', 'cook'])
    @cooldown(2)
    @require_args()
    async def recipe(self, ctx, *args):
        data = await ctx.bot.util.get_request(
            "http://www.recipepuppy.com/api/",
            json=True,
            raise_errors=True,
            force_json=True,
            q=' '.join(args)
        )
        if len(data['results'])==0: 
            raise ctx.bot.util.BasicCommandException("I did not find anything.")
        
        total = random.choice([i for i in data['results'] if i['thumbnail']!=''])
        embed = ctx.bot.Embed(
            ctx,
            title=total['title'],
            url=total['href'],
            desc='Ingredients:\n{}'.format(total['ingredients']),
            image=(total['thumbnail'] if total['thumbnail'] != "" else None)
        )
        await embed.send()
        del embed, total, data

    @command(['calculator', 'equ', 'equation', 'calculate'])
    @cooldown(3)
    @require_args()
    async def calc(self, ctx, *args):
        equation = self.python_calc(args)
        if search("[a-zA-Z]", equation): raise ctx.bot.util.BasicCommandException("Please do NOT input something that contains letters. This is not eval, nerd.")
        try:
            res = eval(equation)
            return await ctx.send("{} | {} = `{}`".format(ctx.bot.util.success_emoji, equation, str(res)[0:1000]))
        except Exception as e:
            raise ctx.bot.util.BasicCommandException(f"Error: {str(e)}")
    
    @command()
    @cooldown(7)
    async def quote(self, ctx):
        await ctx.trigger_typing()
        data = await ctx.bot.util.get_request('https://quotes.herokuapp.com/libraries/math/random', raise_errors=True)
        text, quoter = data.split(' -- ')[0], data.split(' -- ')[1]
        embed = ctx.bot.Embed(ctx, author_name=quoter, desc=discord.utils.escape_markdown(text))
        await embed.send()
        del embed, text, quoter, data
    
    @command()
    @cooldown(5)
    async def robohash(self, ctx, *args):
        url = "https://robohash.org/" + ctx.bot.util.encode_uri(" ".join(args)) if args else 'https://robohash.org/' + ctx.bot.util.encode_uri(str(hash(str(time()))))
        await ctx.bot.util.send_image_attachment(ctx, url)
        del url

    @command()
    @cooldown(5)
    @require_args()
    async def weather(self, ctx, *args):
        return await ctx.bot.util.send_image_attachment(ctx, 'https://wttr.in/'+str(ctx.bot.util.encode_uri(' '.join(args)))+'.png')
    
    @command(['rhymes'])
    @cooldown(7)
    @require_args()
    async def rhyme(self, ctx, *args):
        await ctx.trigger_typing()
        
        data = await ctx.bot.util.get_request(
            'https://rhymebrain.com/talk',
            json=True,
            raise_errors=True,
            function='getRhymes',
            word=' '.join(args)
        )
        
        words = [word['word'] for word in data if word['flags'] == 'bc']
        if not words:
            raise ctx.bot.util.BasicCommandException('We did not find any rhyming words corresponding to that letter.')
        embed = ctx.bot.Embed(ctx, title='Words that rhymes with '+' '.join(args)+':', desc=str(' '.join(words))[0:500])
        await embed.send()
        del embed, words, data

    @command()
    @cooldown(7)
    async def pandafact(self, ctx):
        data = await ctx.bot.util.get_request('https://some-random-api.ml/facts/panda', json=True, raise_errors=True)
        embed = ctx.bot.Embed(
            ctx,
            title='Did you know?',
            desc=data['fact'],
        )
        await embed.send()
        del embed, data
    
    @command(['birdfact'])
    @cooldown(7)
    async def birbfact(self, ctx):
        data = await ctx.bot.util.get_request('https://some-random-api.ml/facts/bird', json=True, raise_errors=True)
        embed = ctx.bot.Embed(
            ctx,
            title='Did you know?',
            desc=data['fact'],
        )
        await embed.send()
        del embed, data
    
    @command()
    @cooldown(5)
    async def bored(self, ctx):
        data = await ctx.bot.util.get_request(
            "https://www.boredapi.com/api/activity",
            json=True,
            raise_errors=True,
            participants=1
        )
        embed = ctx.bot.Embed(ctx, title=f"Feeling bored? Why don't you {data['activity']}?")
        await embed.send()
        del embed, data

    @command()
    @cooldown(20)
    async def googledoodle(self, ctx):
        await ctx.trigger_typing()
        data = await ctx.bot.util.get_request(
            'https://www.google.com/doodles/json/{}/{}'.format(str(t.now().year), str(t.now().month)),
            json=True,
            raise_errors=True
        )
        embed = ctx.bot.Embed(ctx, title=data[0]['title'], url='https://www.google.com/doodles/'+data[0]['name'], image='https:'+data[0]['high_res_url'], fields={"Event Date": '/'.join(
            [str(i) for i in data[0]['run_date_array'][::-1]]
        )})
        await embed.send()
        del embed, data

    @command(['dogfact', 'funfact'])
    @cooldown(6)
    async def catfact(self, ctx):
        key = ctx.bot.util.get_command_name(ctx)[:-4]
        url = self._fact_urls[key]

        result = await ctx.bot.util.get_request(
            url[0], json=True, raise_errors=True
        )
        result = result[url[1]]

        if url[2]:
            result = result[url[2]]
        
        embed = ctx.bot.Embed(ctx, title=key + " fact!", desc=result)
        return await embed.send()
    
    @command(['em'])
    @cooldown(2)
    @require_args()
    async def embed(self, ctx, *args):
        embed = ctx.bot.Embed(ctx, desc=' '.join(args)[0:1950])
        await embed.send()
        del embed
    
    @command(['col'])
    @cooldown(3)
    @require_args()
    async def color(self, ctx, *args):
        await ctx.trigger_typing()
        role_name = ctx.bot.Parser.get_value("role")
        if role_name:
            iterate_result = [i.id for i in ctx.guild.roles if role_name.lower() in i.name.lower()]
            if not iterate_result:
                raise ctx.bot.util.BasicCommandException("Role not found.")
            color_image = await ctx.bot.canvas.color(str(ctx.guild.get_role(iterate_result[0]).colour))
            del iterate_result
        else:
            color_image = await ctx.bot.canvas.color(None, (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))) if ctx.bot.utils.parse_parameter(args, 'random')['available'] else await ctx.bot.canvas.color(' '.join(args))
        if not color_image:
            return await ctx.bot.cmds.invalid_args(ctx)
        await ctx.send(file=discord.File(color_image, 'color.png'))
        del color_image, role_name
    
    @command(['fast'])
    @cooldown(5)
    async def typingtest(self, ctx):
        await ctx.trigger_typing()
        data = await ctx.bot.util.get_request(
            "https://useless-api.vierofernando.repl.co/randomword",
            json=True,
            raise_errors=True
        )
        buffer = await ctx.bot.canvas.simpletext(data['word'])
        a = time()
        await ctx.send(file=discord.File(buffer, "fast.webp"))
        wait = ctx.bot.WaitForMessage(ctx, timeout=20.0, check=(lambda x: x.channel == ctx.channel and (not x.author.bot) and (x.content.lower() == data['word'])))
        message = await wait.get_message()
        if not message:
            return
        embed = ctx.bot.Embed(ctx, title=f"Congratulations! {message.author.display_name} got it first!", fields={"Time taken": str((time() - a) * 1000) + " s", "Word": data['word']}, footer="Try again later if you lost lol")
        await embed.send()
        del message, wait, a, buffer, data

def setup(client):
    client.add_cog(utils())