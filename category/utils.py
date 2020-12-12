import discord
import random
from discord.ext import commands
from decorators import *
from io import BytesIO
from json import loads
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

    @command('nation')
    @cooldown(5)
    async def country(self, ctx, *args):
        _country = " ".join(args)
        try:
            assert _country is not None, "Send a country name!"
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
                    "Currency": (("\n".join(["**"+currency["name"]+"** ("+currency["code"]+" `"+currency["symbol"]+"`)" for currency in res["currencies"]])) if len(res["currencies"]) > 0 else "`doesn't have currency :(`")
                }
            )
            return await embed.send()
        except Exception as e:
            raise ctx.bot.util.BasicCommandException(str(e))
    
    @command()
    @cooldown(3)
    async def gradient(self, ctx, *args):
        await ctx.trigger_typing()
        try:
            assert len(args) > 0
            if len(args) == 1:
                color_left, color_right = ImageColor.getrgb(args[0]), None
            else:
                left, right = ctx.bot.Parser.split_args(args)
                color_left, color_right = ImageColor.getrgb(left), ImageColor.getrgb(right)
        except:
            raise ctx.bot.util.BasicCommandException("Please input a valid color.")
        if color_left == color_right:
            raise ctx.bot.util.BasicCommandException("Those two colors are the same :/")
        res = await ctx.bot.canvas.gradient(color_left, color_right)
        return await ctx.send(file=discord.File(res, "gradient.png"))
    
    @command('trending,news')
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
            embed = discord.Embed(title=content, color=ctx.guild.me.roles[::-1][0].color)
            embed.set_image(url=imageURL)
            embed.set_footer(text="Content provided by msn.com")
            return await ctx.send(embed=embed)
        except Exception as e:
            await ctx.bot.get_user(ctx.bot.util.owner_id).send(f"yo, theres an error: `{str(e)}`")
            raise ctx.bot.util.BasicCommandException("Oopsies, there was an error on searching the news.")
    
    @command('prsc,psrc,act,activity')
    @cooldown(3)
    async def presence(self, ctx, *args):
        await ctx.trigger_typing()
        user = ctx.bot.Parser.parse_user(ctx, args)
        if isinstance(user.activity, discord.Spotify):
            spotify = ctx.bot.Panel(ctx, spotify=user.activity)
            await spotify.draw()
            await spotify.send_as_attachment()
            spotify.close()
            return
        
        if user.activity is None: raise ctx.bot.util.BasicCommandException(f"Sorry, but {user.display_name} has no activity...")
        title = "" if (not hasattr(user.activity, 'name')) else user.activity.name
        subtitle = "" if (not hasattr(user.activity, 'details')) else user.activity.details
        desc = "" if (not hasattr(user.activity, 'state')) else user.activity.state
        if ((subtitle == "") and (not desc == "")):
            temp = desc
            subtitle = temp
            desc = ""
        url = "https://cdn.discordapp.com/embed/avatars/0.png" if (not hasattr(user.activity, 'large_image_url')) else user.activity.large_image_url
        panel = ctx.bot.Panel(ctx, title=title, subtitle=subtitle, description=desc, icon=url)
        await panel.draw()
        await panel.send_as_attachment()
        panel.close()
    
    @command('colorthief,getcolor,accent,accentcolor,accent-color,colorpalette,color-palette')
    @cooldown(3)
    async def palette(self, ctx, *args):
        url, person = await ctx.bot.Parser.parse_image(ctx, args), ctx.bot.Parser.parse_user(ctx, args)
        await ctx.trigger_typing()
        palette = await ctx.bot.canvas.get_palette(ctx.bot.canvas.get_multiple_accents(url))
        return await ctx.send(file=discord.File(palette, 'palette.png'))

    @command('isitup,webstatus')
    @cooldown(2)
    @require_args()
    async def isitdown(self, ctx, *args):
        wait = await ctx.send('{} | Pinging...'.format(ctx.bot.util.loading_emoji))
        web = args[0].replace('<', '').replace('>', '')
        if not web.startswith('http'): web = 'http://' + web
        try:
            a = t.now()
            ping = get(web, timeout=5)
            pingtime = round((t.now()-a).total_seconds()*1000)
            await wait.edit(content='{} | That website is up.\nPing: {} ms\nStatus code: {}'.format(ctx.bot.util.success_emoji, pingtime, ping.status_code))
        except:
            await wait.edit(content='{} | Yes. that website is down.'.format(ctx.bot.util.error_emoji))
    
    @command('img2ascii,imagetoascii,avascii,avatarascii,avatar2ascii,av2ascii')
    @cooldown(10)
    async def imgascii(self, ctx, *args):
        input = ctx.bot.Parser.get_input(args)
        
        if "--img" in input:
            args = ctx.bot.Parser.without("--img")
            url = await ctx.bot.Parser.parse_image(ctx, args)
            await ctx.trigger_typing()
            res_im = await ctx.bot.canvas.imagetoASCII_picture(url)
            await ctx.send(file=discord.File(res_im, 'imgascii.png'))
            del res_im
            return
        
        url = await ctx.bot.Parser.parse_image(ctx, args)
        wait = await ctx.send('{} | Please wait...'.format(ctx.bot.util.loading_emoji))
        text = await ctx.bot.canvas.imagetoASCII(url)
        try:
            data = await ctx.bot.util.default_client.post("https://hastebin.com/documents", data=text)
            assert data.status == 200
        except:
            await wait.delete()
            file = discord.File(BytesIO(bytes(text, 'utf-8')), filename='ascii.txt')
            return await ctx.send(file=file)
        return await wait.edit(content='{} | You can see the results at **https://hastebin.com/{}**!'.format(ctx.bot.util.success_emoji, data.json()['key']))
    
    @command()
    @cooldown(15)
    async def nasa(self, ctx, *args):
        query = 'earth' if len(args)==0 else ' '.join(args)
        await ctx.trigger_typing()
        
        data = await ctx.bot.util.get_request(
            f'https://images-api.nasa.gov/search',
            json=True,
            raise_errors=True,
            q=query[0:100],
            media_type='image'
        )
        if (data is None) or len(data['collection']['items'])==0:
            raise ctx.bot.util.BasicCommandException("Nothing found.")
        img = random.choice(data['collection']['items'])
        em = discord.Embed(title=img['data'][0]['title'], description=img['data'][0]["description"], color=ctx.guild.me.roles[::-1][0].color)
        em.set_image(url=img['links'][0]['href'])
        return await ctx.send(embed=em)

    @command('pokedex,dex,bulbapedia,pokemoninfo,poke-info,poke-dex,pokepedia')
    @cooldown(10)
    async def pokeinfo(self, ctx, *args):
        query = 'Missingno' if (len(args)==0) else ctx.bot.util.encode_uri(' '.join(args))
        try:
            data = await ctx.bot.util.get_request(
                'https://bulbapedia.bulbagarden.net/w/api.php',
                json=True,
                raise_errors=True,
                action='query',
                titles=query,
                format='json',
                formatversion=2,
                pithumbsize=150,
                prop='extracts|pageimages',
                explaintext='',
                redirects='',
                exintro=''
            )
            
            embed = discord.Embed(
                url='https://bulbapedia.bulbagarden.net/wiki/{}'.format(query),
                color=ctx.guild.me.roles[::-1][0].color,
                title=data['query']['pages'][0]['title'], description=data['query']['pages'][0]['extract'][0:1000]
            )
            try:
                pokeimg = data['query']['pages'][0]['thumbnail']['source']
                embed.set_thumbnail(url=pokeimg)
            except: pass
            await ctx.send(embed=embed)
        except Exception as e:
            print(e)
            raise ctx.bot.util.BasicCommandException("Pokemon not found.")

    @command('recipes,cook')
    @cooldown(2)
    @require_args()
    async def recipe(self, ctx, *args):
        data = await ctx.bot.util.get_request(
            "http://www.recipepuppy.com/api/",
            json=True,
            raise_errors=True,
            q=' '.join(args)
        )
        if len(data['results'])==0: 
            raise ctx.bot.util.BasicCommandException("I did not find anything.")
        
        total = random.choice([i for i in data['results'] if i['thumbnail']!=''])
        embed = discord.Embed(title=total['title'], url=total['href'], description='Ingredients:\n{}'.format(total['ingredients']), color=ctx.guild.me.roles[::-1][0].color)
        if total['thumbnail'] != "":
            embed.set_image(url=total['thumbnail'])
        await ctx.send(embed=embed)

    @command('calculator,equ,equation,calculate')
    @cooldown(3)
    @require_args()
    async def calc(self, ctx, *args):
        equation = ' '.join(args)
        replaceWith = "x>*;.>*;?>*;?>/;?>*;plus>+;minus>-;divide>/;multiply>*;divide by>/;times>*;subtract>-;add>+;power>**;powers>**;^>**"
        for rep in replaceWith.split(";"):
            equation = equation.replace(rep.split('>')[0], rep.split('>')[1])
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
        await ctx.send(embed=discord.Embed(description=f'***{text}***\n\n-- {quoter} --', color=ctx.guild.me.roles[::-1][0].color))

    @command()
    @cooldown(10)
    async def robohash(self, ctx, *args):
        if len(args)==0: url='https://robohash.org/'+str(src.randomhash())
        else: url = 'https://robohash.org/'+str(ctx.bot.util.encode_uri(' '.join(args)))
        return await ctx.bot.util.send_image_attachment(ctx, url)

    @command()
    @cooldown(10)
    @require_args()
    async def weather(self, ctx, *args):
        return await ctx.bot.util.send_image_attachment(ctx, 'https://wttr.in/'+str(ctx.bot.util.encode_uri(' '.join(args)))+'.png')

    @command()
    @cooldown(10)
    async def ufo(self, ctx):
        num = str(random.randint(50, 100))
        data = await ctx.bot.util.get_request(
            'http://ufo-api.herokuapp.com/api/sightings/search',
            json=True,
            raise_errors=True,
            limit=num
        )
        if data['status']!='OK':
            raise ctx.bot.util.BasicCommandException('There was a problem on retrieving the info.\nThe server said: "'+str(data['status'])+'" :eyes:')
        else:
            ufo = random.choice(data['sightings'])
            embed = discord.Embed(title='UFO Sighting in '+str(ufo['city'])+', '+str(ufo['state']), description='**Summary:** '+str(ufo['summary'])+'\n\n**Shape:** '+str(ufo['shape'])+'\n**Sighting Date: **'+str(ufo['date'])[:-8].replace('T', ' ')+'\n**Duration: **'+str(ufo['duration'])+'\n\n[Article Source]('+str(ufo['url'])+')', colour=ctx.guild.me.roles[::-1][0].color)
            embed.set_footer(text='Username601 raided area 51 and found this!')
            await ctx.send(embed=embed)
    
    @command('rhymes')
    @cooldown(7)
    @require_args()
    async def rhyme(self, ctx, *args):
        await ctx.bot.trigger_typing()
        
        data = await ctx.bot.util.get_request(
            'https://rhymebrain.com/talk?function=getRhymes&word=',
            json=True,
            raise_errors=True,
            function='getRhymes',
            word=' '.join(args)
        )
        
        if len(data)<1: await wait.edit(content='We did not find any rhyming words corresponding to that letter.')
        else:
            words = [word['word'] for word in data if word['flags'] == 'bc']
            embed = discord.Embed(title='Words that rhymes with '+str(' '.join(args))+':', description=str(' '.join(words))[0:1950], colour=ctx.guild.me.roles[::-1][0].color)
            await wait.edit(content='', embed=embed)

    @command('sof')
    @cooldown(12)
    @require_args()
    async def stackoverflow(self, ctx, *args):
        try:
            query = ctx.bot.util.encode_uri(' '.join(args))
            data = await ctx.bot.util.get_request(
                "https://api.stackexchange.com/2.2/search/advanced",
                json=True,
                raise_errors=True,
                q=' '.join(args),
                site='stackoverflow',
                page=1,
                answers=1,
                order='asc',
                sort='relevance'
            )
            leng = len(data['items'])
            ques = data['items'][0]
            tags = ''
            for i in range(len(ques['tags'])):
                if i==len(ques['tags'])-1:
                    tags += '['+str(ques['tags'][i])+'](https://stackoverflow.com/questions/tagged/'+str(ques['tags'][i])+')'
                    break
                tags += '['+str(ques['tags'][i])+'](https://stackoverflow.com/questions/tagged/'+str(ques['tags'][i])+') | '
            embed = discord.Embed(title=ques['title'], description='**'+str(ques['view_count'])+' *desperate* developers looked into this post.**\n**TAGS:** '+str(tags), url=ques['link'], colour=ctx.guild.me.roles[::-1][0].color)
            embed.set_author(name=ques['owner']['display_name'], url=ques['owner']['link'], icon_url=ques['owner']['profile_image'])
            embed.set_footer(text='Shown 1 result out of '+str(leng)+' results!')
            await ctx.send(embed=embed)
        except:
            raise ctx.bot.util.BasicCommandException('There was an error on searching! Please check your spelling :eyes:')

    @command('birbfact,birdfact')
    @cooldown(7)
    async def pandafact(self, ctx):
        if ctx.bot.util.get_command_name(ctx) == 'pandafact': link = 'https://some-random-api.ml/facts/panda'
        else: link = 'https://some-random-api.ml/facts/bird'
        data = await ctx.bot.util.get_request(link, json=True, raise_errors=True)
        await ctx.send(embed=discord.Embed(title='Did you know?', description=data['fact'], colour=ctx.guild.me.roles[::-1][0].color))

    @command()
    @cooldown(2)
    async def iss(self, ctx):
        iss, ppl, total = await ctx.bot.util.get_request(
            'https://open-notify-api.herokuapp.com/iss-now.json', json=True, raise_errors=True
        ), await ctx.bot.util.get_request(
            'https://open-notify-api.herokuapp.com/astros.json', json=True, raise_errors=True
        ), '```'
        for i in range(len(ppl['people'])):
            total += str(i+1) + '. ' + ppl['people'][i]['name'] + ((20-(len(ppl['people'][i]['name'])))*' ') + ppl['people'][i]['craft'] + '\n'
        embed = discord.Embed(title='Position: '+str(iss['iss_position']['latitude'])+' '+str(iss['iss_position']['longitude']), description='**People at craft:**\n\n'+str(total)+'```', colour=ctx.guild.me.roles[::-1][0].color)
        await ctx.send(embed=embed)

    @command('ghibli')
    @cooldown(5)
    async def ghiblifilms(self, ctx, *args):
        wait = await ctx.send(str(ctx.bot.util.loading_emoji) + ' | Please wait... Getting data...')
        data = await ctx.bot.util.get_request(
            'https://ghibliapi.herokuapp.com/films',
            json=True,
            raise_errors=True
        )
        if len(args)==0:
            films = ""
            for i in range(len(data)):
                films = films+'('+str(int(i)+1)+') '+str(data[i]['title']+' ('+str(data[i]['release_date'])+')\n')
            embed = discord.Embed(
                title = 'List of Ghibli Films',
                description = str(films),
                color = ctx.guild.me.roles[::-1][0].color
            )
            embed.set_footer(text='Type `'+ctx.bot.command_prefix+'ghibli <number>` to get each movie info.')
            await wait.edit(content='', embed=embed)
        else:
            try:
                num = int([i for i in list(args) if i.isnumeric()][0])-1
                embed = discord.Embed(
                    title = data[num]['title'] + ' ('+str(data[num]['release_date'])+')',
                    description = '**Rotten Tomatoes Rating: '+str(data[num]['rt_score'])+'%**\n'+data[num]['description'],
                    color = ctx.guild.me.roles[::-1][0].color
                )
                embed.add_field(name='Directed by', value=data[num]['director'], inline='True')
                embed.add_field(name='Produced by', value=data[num]['producer'], inline='True')
                await wait.edit(content='', embed=embed)
            except: raise ctx.bot.util.BasicCommandException('the movie you requested does not exist!?')

    @command()
    @cooldown(5)
    async def bored(self, ctx):
        data = await ctx.bot.util.get_request(
            "https://www.boredapi.com/api/activity",
            json=True,
            raise_errors=True,
            participants=1
        )
        await ctx.send('**Feeling bored?**\nWhy don\'t you '+str(data['activity'])+'? :wink::ok_hand:')

    @command()
    @cooldown(20)
    async def googledoodle(self, ctx):
        wait = await ctx.send(str(ctx.bot.util.loading_emoji) + ' | Please wait... This may take a few moments...')
        data = await ctx.bot.util.get_request(
            'https://www.google.com/doodles/json/{}/{}'.format(str(t.now().year), str(t.now().month)),
            json=True,
            raise_errors=True
        )
        embed = discord.Embed(title=data[0]['title'], colour=ctx.guild.me.roles[::-1][0].color, url='https://www.google.com/doodles/'+data[0]['name'])
        embed.set_image(url='https:'+data[0]['high_res_url'])
        embed.set_footer(text='Event date: '+str('/'.join(
            [str(i) for i in data[0]['run_date_array'][::-1]]
        )))
        await wait.edit(content='', embed=embed)

    @command('dogfact,funfact')
    @cooldown(6)
    async def catfact(self, ctx):
        key = ctx.bot.util.get_command_name(ctx)[:-4]
        url = self._fact_urls[key]

        result = await ctx.bot.util.get_request(
            url[0], json=True, raise_errors=True
        )
        result = result[url[1]]

        if url[2] is not None:
            result = result[url[2]]
        
        embed = ctx.bot.Embed(ctx, title=key + " fact!", desc=result)
        return await embed.send()
    
    @command('em')
    @cooldown(2)
    async def embed(self, ctx, *args):
        try:
            return await ctx.send(embed=discord.Embed(description=' '.join(args)))
        except:
            return await ctx.message.add_reaction(ctx.bot.util.error_emoji)
            
    @command('col')
    @cooldown(3)
    @require_args()
    async def color(self, ctx, *args):
        await ctx.trigger_typing()
        role_name = ctx.bot.Parser.get_value("role")
        if role_name:
            iterate_result = [i.id for i in ctx.guild.roles if role_name.lower() in i.name.lower()]
            if len(iterate_result) == 0:
                raise ctx.bot.util.BasicCommandException("Role not found.")
            color_image = await ctx.bot.canvas.color(str(ctx.guild.get_role(iterate_result[0]).colour))
            del iterate_result
        else:
            color_image = await ctx.bot.canvas.color(None, (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))) if ctx.bot.utils.parse_parameter(args, 'random')['available'] else await ctx.bot.canvas.color(' '.join(args))
        if not color_image:
            raise ctx.bot.util.BasicCommandException("Please insert a valid Hex.")
        await ctx.send(file=discord.File(color_image, 'color.png'))
        del color_image
        del role_name
    
    @command('fast')
    @cooldown(10)
    async def typingtest(self, ctx):
        await ctx.trigger_typing()
        data = await ctx.bot.util.get_request(
            "https://random-word-api.herokuapp.com/word",
            json=True,
            raise_errors=True,
            number=5
        )
        text, guy, first = " ".join(data), ctx.author, t.now().timestamp()
        text = await ctx.bot.canvas.simpletext(text)
        main = await ctx.send(content='**Type the text on the image. (Only command invoker can play)**\nYou have 2 minutes.\n', file=discord.File(text, 'test.png'))
        def check(m):
            return m.author == guy
        try:
            trying = await ctx.bot.wait_for('message', check=check, timeout=120.0)
        except:
            await main.edit(content='Time is up.')
        if str(trying.content) is not None:
            offset = t.now().timestamp()-first
            asked, answered, wrong = text.lower(), str(trying.content).lower(), 0
            for i in range(len(asked)):
                try:
                    if asked[i]!=answered[i]: wrong += 1
                except: break
            try: accuracy, cps = round((len(asked)-wrong)/len(asked)*100), round(len(answered)/offset)
            except: accuracy, cps = "???", "???"
            await ctx.send(embed=discord.Embed(title='TYPING TEST RESULTS', description='**Your time: **'+str(round(offset))+' seconds.\n**Your accuracy: **'+str(accuracy)+'%\n**Your speed: **'+str(cps)+' Characters per second.', colour=ctx.guild.me.roles[::-1][0].color))

def setup(client):
    client.add_cog(utils())