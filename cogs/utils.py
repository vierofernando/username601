import discord
from random import randint, choice
from discord.ext import commands
from decorators import *
from json import loads
from io import BytesIO
from time import time
from datetime import datetime as t
from re import search

class utils(commands.Cog):
    def __init__(self):
        self._fact_urls = {
            "cat": ("https://catfact.ninja/fact", "fact", None),
            "dog": ("https://dog-api.kinduff.com/api/facts", "facts", 0)
        }
        self.facts = tuple(loads(open("./assets/json/facts.json", "r").read()))
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
            data = await ctx.bot.util.request(f'https://restcountries.eu/rest/v2/name/{ctx.bot.util.encode_uri(_country)}', json=True)
            assert isinstance(data, list), "No such country with the name `"+_country+"` found."            
            embed = ctx.bot.ChooseEmbed(ctx, data, key=(lambda x: x["name"]))
            res = await embed.run()
            if not res:
                return
            await ctx.embed(title=res["name"], description="Native name: \""+str(res.get("nativeName"))+"\"", fields={
                "Location": "**Latitude Longitude:** `"+(", ".join([str(i) for i in res["latlng"]]))+"`\n**Region:** "+res["region"]+"\n**Subregion: **"+res["subregion"]+"\n**Capital:** "+res["capital"],
                "Detailed Info": "**Population Count: **"+str(res["population"])+"\n**Country Area: **"+str(res.get("area"))+" km²\n**Time Zones: **"+(", ".join(res["timezones"])),
                "Currency": (("\n".join(["**"+currency["name"]+"** ("+currency["code"]+" `"+currency["symbol"]+"`)" for currency in res["currencies"]])) if res["currencies"] else "`doesn't have currency :(`")
            })
            del res, embed, data
        except Exception as e:
            raise ctx.error_message(str(e))
    
    @command()
    @cooldown(3)
    @require_args(2)
    async def gradient(self, ctx, *args):
        try:
            await ctx.trigger_typing()
            left, right = ctx.bot.Parser.split_args(args)
            color_left, color_right = ctx.bot.Parser.parse_color(left), ctx.bot.Parser.parse_color(right)
            assert color_left != color_right
            assert bool(color_left) and bool(color_right)
            res = await ctx.bot.Image.gradient(color_left, color_right)
            await ctx.send_image(res)
            del res, color_left, color_right, left, right
        except:
            return await ctx.bot.cmds.invalid_args(ctx)
    
    @command(['colorthief', 'getcolor', 'accent', 'accentcolor', 'accent-color', 'colorpalette', 'color-palette'])
    @cooldown(3)
    async def palette(self, ctx, *args):
        url = await ctx.bot.Parser.parse_image(ctx, args)
        await ctx.trigger_typing()
        palette = await ctx.bot.canvas.get_palette(ctx.bot.canvas.get_multiple_accents(url))
        await ctx.send_image(palette)
        del palette, url

    @command(['pip'])
    @cooldown(3)
    @require_args()
    async def pypi(self, ctx, *args):
        await ctx.trigger_typing()
        
        data = await ctx.bot.util.request(
            "https://pypi.org/pypi/"+ "-".join(args) +"/json",
            json=True
        )
        
        nl = "\n"
        await ctx.embed(title=data['info']['name'], description=data['info']['summary'], fields={
            "Links": f"**Home Page: **{'[click here]('+data['info']['home_page']+')' if data['info']['home_page'] else '`<no links available>`'}\n**Download Link: **{'[click here]('+data['info']['download_url']+')' if data['info']['download_url'] else '`<no links available>`'}",
            "Author": f"{data['info']['author']} {'('+data['info']['author_email']+')' if data['info']['author_email'] else ''}\n",
            "Version": f"**Current Version: **[{data['info']['version']}]({data['info']['release_url']})\n**Uploaded at: **{ctx.bot.util.timestamp(data['releases'][data['info']['version']][0]['upload_time'])}",
            "Keywords": data['info']['keywords'].replace(',', ', ') if data['info']['keywords'] else '`<no keywords>`'
        }, url=data['info']['package_url'])
        del data, nl

    @command(['isitup', 'webstatus'])
    @cooldown(2)
    @require_args()
    async def isitdown(self, ctx, *args):
        await ctx.trigger_typing()
        web = args[0].replace('<', '').replace('>', '')
        if not web.startswith('http'): web = 'http://' + web
        try:
            a = time()
            ping = await ctx.bot.http._HTTPClient__session.get(web)
            pingtime = round((time() - a)*1000)
            await ctx.embed(title="That website is up.", fields={"Ping": f"{pingtime}ms", "HTTP Status Code": f"{ping.status} {ctx.bot.util.status_codes[str(ping.status)]}", "Content Type": ping.headers['Content-Type']}, color=discord.Color.green())
            del pingtime, ping, a, web
        except:
            await ctx.embed(title="That website is down.", color=discord.Color.red())
    
    @command()
    @cooldown(15)
    async def nasa(self, ctx, *args):
        query = ctx.bot.util.encode_uri(' '.join(args) if args else 'earth')
        await ctx.trigger_typing()
        
        data = await ctx.bot.http._HTTPClient__session.get(f'https://images-api.nasa.gov/search?q={query[:100]}&media_type=image')
        try:
            data = await data.json()
            assert bool(data)
            assert bool(data["collection"]["items"])
        except:
            raise ctx.error_message("Nothing found.")
        
        img = choice(data['collection']['items'])
        await ctx.embed(title=img['data'][0]['title'], description=img['data'][0]["description"], image=img['links'][0]['href'])
        del em, img, data

    @command(['pokemon', 'pokeinfo', 'dex', 'bulbapedia'])
    @cooldown(10)
    @require_args()
    async def pokedex(self, ctx, *args):
        try:
            data = await ctx.bot.util.request(
                'https://bulbapedia.bulbagarden.net/w/api.php',
                json=True,
                action='query',
                titles=' '.join(args)[:100],
                format='json',
                formatversion=2,
                pithumbsize=150,
                prop='extracts|pageimages',
                explaintext='',
                redirects='',
                exintro=''
            )
            
            try: image = data['query']['pages'][0]['thumbnail']['source'].replace("http", "https") # why
            except KeyError: image = None

            _data = {
                "title": data['query']['pages'][0]['title'],
                "url": f'https://bulbapedia.bulbagarden.net/wiki/{data["query"]["pages"][0]["title"].replace(" ", "_")}'
            }
            
            if image:
                _data["thumbnail"] = { "url": image }
            
            paginator = ctx.bot.EmbedPaginator.from_long_string(ctx, data['query']['pages'][0]['extract'], data=_data, max_char_length=1000)
            
            if not paginator:
                _data.pop("thumbnail", None)
                await ctx.embed(description=data['query']['pages'][0]['extract'], thumbnail=image, **_data)
                del image, data, paginator, _data
                return
            del image, data, _data
            return await paginator.execute()
        except:
            raise ctx.error_message("Pokemon not found.")

    @command(['recipes', 'cook'])
    @cooldown(2)
    @require_args()
    async def recipe(self, ctx, *args):
        data = await ctx.bot.util.request(
            "http://www.recipepuppy.com/api/",
            json=True,
            q=' '.join(args)
        )
        if not data['results']: 
            raise ctx.error_message("I did not find anything.")
        
        total = choice([i for i in data['results'] if i['thumbnail']!=''])
        await ctx.embed(title=total['title'], url=total['href'], description=f"Ingredients:\n{total['ingredients']}", image=(total['thumbnail'] if total['thumbnail'] else None))
        del total, data

    @command(['calculator', 'equ', 'equation', 'calculate'])
    @cooldown(3)
    @require_args()
    async def calc(self, ctx, *args):
        if "to" in "".join(args).lower():
            return await ctx.success_embed(ctx.bot.util.convert_length(''.join(args)))
    
        equation = self.python_calc(args)
        if search("[a-zA-Z]", equation): raise ctx.error_message("Please do NOT input something that contains letters. This is not eval, nerd.")
        try:
            res = eval(equation)
            return await ctx.send(f"{equation} = `{str(res)[:1000]}`")
        except Exception as e:
            raise ctx.error_message(f"Error: {str(e)}")
    
    @command()
    @cooldown(7)
    async def quote(self, ctx):
        await ctx.trigger_typing()
        data = await ctx.bot.util.request('https://quotes.herokuapp.com/libraries/math/random')
        text, quoter = data.split(' -- ')[0], data.split(' -- ')[1]
        await ctx.embed(author_name=quoter, description=discord.utils.escape_markdown(text))
        del text, quoter, data

    @command(['rhymes'])
    @cooldown(7)
    @require_args()
    async def rhyme(self, ctx, *args):
        await ctx.trigger_typing()
        
        data = await ctx.bot.util.request(
            'https://rhymebrain.com/talk',
            json=True,
            function='getRhymes',
            word=' '.join(args)
        )
        
        words = [word['word'] for word in data if word['flags'] == 'bc']
        if not words:
            raise ctx.error_message('We did not find any rhyming words corresponding to that letter.')
        
        paginator = ctx.bot.EmbedPaginator.from_long_array(ctx, words, {
            "title": f"Words that rhymes with {' '.join(args)[:15]}:"
        }, char=", ", max_char_length=500)
        
        if not paginator:
            await ctx.embed(title='Words that rhymes with '+' '.join(args)+':', description=str(', '.join(words))[:500])
            del words, data, paginator
            return
        del words, data
        return await paginator.execute()

    @command()
    @cooldown(7)
    async def pandafact(self, ctx):
        data = await ctx.bot.util.request('https://some-random-api.ml/facts/panda', json=True)
        await ctx.embed(title='Did you know?', description=data['fact'], color=discord.Color.green())
        del data
    
    @command(['birdfact'])
    @cooldown(7)
    async def birbfact(self, ctx):
        data = await ctx.bot.util.request('https://some-random-api.ml/facts/bird', json=True)
        await ctx.embed(title='Did you know?', description=data['fact'], color=discord.Color.green())
        del data
    
    @command()
    @cooldown(5)
    async def bored(self, ctx):
        data = await ctx.bot.util.request(
            "https://www.boredapi.com/api/activity",
            json=True,
            participants=1
        )
        await ctx.success_embed(f"Feeling bored? Why don't you {data['activity']}?")
        del data

    @command()
    @cooldown(20)
    async def googledoodle(self, ctx):
        await ctx.trigger_typing()
        data = await ctx.bot.util.request(
            'https://www.google.com/doodles/json/{}/{}'.format(str(t.now().year), str(t.now().month)),
            json=True
        )
        embed = ctx.bot.Embed(ctx, title=data[0]['title'], url='https://www.google.com/doodles/'+data[0]['name'], image='https:'+data[0]['high_res_url'], fields={"Event Date": '/'.join(
            [str(i) for i in data[0]['run_date_array'][::-1]]
        )})
        await embed.send()
        del embed, data

    @command(['fun-fact'])
    @cooldown(5)
    async def funfact(self, ctx):
        return await ctx.success_embed(choice(self.facts))

    @command(['dogfact'])
    @cooldown(6)
    async def catfact(self, ctx):
        key = ctx.bot.util.get_command_name(ctx)[:-4]
        url = self._fact_urls[key]

        result = await ctx.bot.util.request(
            url[0], json=True
        )
        result = result[url[1]]

        if url[2]:
            result = result[url[2]]
        
        embed = await ctx.embed(title=key + " fact!", description=result, color=discord.Color.green())
    
    @command(['em'])
    @cooldown(2)
    @require_args()
    async def embed(self, ctx, *args):
        try:
            parser = ctx.bot.Parser(args)
            parser.parse()
            
            assert (bool(parser["description"]) or bool(parser.other))
            await ctx.embed(
                title=parser["title"],
                description=parser["description"] if parser.has("description") else ' '.join(parser.other)[:1950],
                author_name=parser["author"],
                color=ctx.bot.Parser.parse_color(parser["color"]) if parser["color"] else ctx.me.color,
                footer=parser["footer"]
            )
            del parser
        except:
            return await ctx.bot.cmds.invalid_args(ctx)
    
    @command(['col'])
    @cooldown(3)
    @require_args()
    async def color(self, ctx, *args):
        await ctx.trigger_typing()
        role_name = ctx.bot.Parser.get_value("role")
        if role_name:
            iterate_result = [i.id for i in ctx.guild.roles if role_name.lower() in i.name.lower()]
            if not iterate_result:
                raise ctx.error_message("Role not found.")
            color_image = await ctx.bot.canvas.color(str(ctx.guild.get_role(iterate_result[0]).colour))
            del iterate_result
        else:
            if "random" in args:
                color_image = await ctx.bot.canvas.color(None, (randint(0, 255), randint(0, 255), randint(0, 255)))
            else:
                color_image = await ctx.bot.canvas.color(' '.join(args))
        if not color_image:
            return await ctx.bot.cmds.invalid_args(ctx)
        await ctx.send_image(color_image)
        del color_image, role_name

def setup(client):
    client.add_cog(utils())