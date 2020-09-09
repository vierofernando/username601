import discord
from discord.ext import commands
import sys
from os import getcwd, name
dirname = getcwd()+'\\..' if name=='nt' else getcwd()+'/..'
sys.path.append(dirname)
del dirname
from username601 import *
sys.path.append(cfg('MODULES_DIR'))
from canvas import Painter
from decorators import command, cooldown
import random
from requests import post, get
import splashes as src
from json import loads
from datetime import datetime as t

class utils(commands.Cog):
    def __init__(self, client):
        self.client = client
        self.canvas = Painter(
            cfg('ASSETS_DIR'),
            cfg('FONTS_DIR')
        )
    
    @command('colorthief,getcolor,accent,accentcolor,accent-color,colorpalette,color-palette')
    @cooldown(3)
    async def palette(self, ctx, *args):
        url, person = getUserAvatar(ctx, args), getUser(ctx, args)
        async with ctx.channel.typing():
            data = self.canvas.get_multiple_accents(url)
            file = discord.File(self.canvas.get_palette(data), 'palette.png')
            em = discord.Embed(title=f'{person.name}\'s avatar color palette', color=discord.Colour.from_rgb(
                data[0]['r'], data[0]['g'], data[0]['b']
            )).set_thumbnail(url=url).set_image(url='attachment://palette.png')
            return await ctx.send(file=file, embed=em)

    @command('isitup,webstatus')
    @cooldown(2)
    async def isitdown(self, ctx, *args):
        if len(list(args))==0: return await ctx.send('{} | Please send a website link...'.format(emote(self.client, 'error')))
        wait = await ctx.send('{} | Pinging...'.format(emote(self.client, 'loading')))
        web = list(args)[0].replace('<', '').replace('>', '')
        if not web.startswith('http'): web = 'http://' + web
        try:
            a = t.now()
            ping = get(web, timeout=5)
            pingtime = round((t.now()-a).total_seconds()*1000)
            await wait.edit(content='{} | That website is up.\nPing: {} ms\nStatus code: {}'.format(emote(self.client, 'success'), pingtime, ping.status_code))
        except:
            await wait.edit(content='{} | Yes. that website is down.'.format(emote(self.client, 'error')))
    
    @command('img2ascii,imagetoascii,avascii,avatarascii,avatar2ascii,av2ascii')
    @cooldown(5)
    async def imgascii(self, ctx, *args):
        url = getUserAvatar(ctx, args)
        wait = await ctx.send('{} | Please wait...'.format(emote(self.client, 'loading')))
        text = self.canvas.imagetoASCII(url)
        data = post("https://hastebin.com/documents", data=text)
        if data.status_code!=200: return await wait.edit(content="{} | Oops! there was an error on posting it there.".format(emote(self.client, 'error')))
        return await wait.edit(content='{} | You can see the results at **https://hastebin.com/{}**!'.format(emote(self.client, 'success'), data.json()['key']))
    
    @command()
    @cooldown(6)
    async def nasa(self, ctx, *args):
        query = 'earth' if len(list(args))==0 else urlify(' '.join(list(args)))
        data = fetchJSON(f'https://images-api.nasa.gov/search?q={query}&media_type=image')
        await ctx.channel.trigger_typing()
        if len(data['collection']['items'])==0: return await ctx.send('{} | Nothing found.'.format(emote(self.client, 'error')))
        img = random.choice(data['collection']['items'])
        em = discord.Embed(title=img['data'][0]['title'], description=img['data'][0]["description"], color=get_embed_color(discord))
        em.set_image(url=img['links'][0]['href'])
        await ctx.send(embed=em)

    @command('pokedex,dex,bulbapedia,pokemoninfo,poke-info,poke-dex,pokepedia')
    @cooldown(5)
    async def pokeinfo(self, ctx, *args):
        query = 'Missingno' if (len(list(args))==0) else urlify(' '.join(list(args)))
        try:
            data = fetchJSON('https://bulbapedia.bulbagarden.net/w/api.php?action=query&titles={}&format=json&formatversion=2&pithumbsize=150&prop=extracts|pageimages&explaintext&redirects&exintro'.format(query))
            embed = discord.Embed(
                url='https://bulbapedia.bulbagarden.net/wiki/{}'.format(query),
                color=get_embed_color(discord),
                title=data['query']['pages'][0]['title'], description=limitto(data['query']['pages'][0]['extract'], 1000)
            )
            try:
                pokeimg = data['query']['pages'][0]['thumbnail']['source']
                embed.set_thumbnail(url=pokeimg)
            except:
                pass
            await ctx.send(embed=embed)
        except Exception as e:
            print(e)
            return await ctx.send("{} | Pokemon not found!".format(
                emote(self.client, 'error')
            ))

    @command('recipes,cook')
    @cooldown(2)
    async def recipe(self, ctx, *args):
        if len(list(args))==0:
            await ctx.send(embed=discord.Embed(title='Here is a recipe to cook nothing:', description='1. Do nothing\n2. Profit'))
        else:
            data = fetchJSON("http://www.recipepuppy.com/api/?q={}".format(urlify(' '.join(list(args)))))
            if len(data['results'])==0: 
                await ctx.send("{} | Did not find anything.".format(emote(self.client, 'error')))
            elif len([i for i in data['results'] if i['thumbnail']!=''])==0:
                await ctx.send("{} | Did not find anything with a delicious picture.".format(emote(self.client, 'error')))
            else:
                total = random.choice([i for i in data['results'] if i['thumbnail']!=''])
                embed = discord.Embed(title=total['title'], url=total['href'], description='Ingredients:\n{}'.format(total['ingredients']), color=get_embed_color(discord))
                embed.set_image(url=total['thumbnail'])
                await ctx.send(embed=embed)

    @command()
    @cooldown(3)
    async def time(self, ctx):
        data = fetchJSON("http://worldtimeapi.org/api/timezone/africa/accra")
        year, time, date = str(data["utc_datetime"])[:-28], str(data["utc_datetime"])[:-22], str(str(data["utc_datetime"])[:-13])[11:]
        if int(year)%4==0: yearType, yearLength = 'It is a leap year.', 366
        else: yearType, yearLength = 'It is not a leap year yet.', 365
        progressDayYear = round(int(data["day_of_year"])/int(yearLength)*100)
        progressDayWeek = round(int(data["day_of_week"])/7*100)
        embed = discord.Embed(
            title = str(date)+' | '+str(time)+' (API)',
            description = str(t.now())[:-7]+' (SYSTEM)\nBoth time above is on UTC.\n**Unix Time:** '+str(data["unixtime"])+'\n**Day of the year: **'+str(data["day_of_year"])+' ('+str(progressDayYear)+'%)\n**Day of the week: **'+str(data["day_of_week"])+' ('+str(progressDayWeek)+'%)\n'+str(yearType),
            colour = get_embed_color(discord)
        )
        await ctx.send(embed=embed)
    @command()
    @cooldown(3)
    async def calc(self, ctx, *args):
        if len(list(args))==0: await ctx.send(emote(self.client, 'error')+" | You need something... i smell no args nearby.")
        else:
            start_counting = True
            for i in list('abcdefghijklmnopqrstuvwxyz.'):
                if i in ''.join(list(args)).lower():
                    start_counting = False
                    break
            if start_counting:
                try: # i know it's eval, but at least it is protected
                    result = eval(' '.join(list(args)))
                    await ctx.send('`'+str(result)+'`')
                except:
                    await ctx.send(emote(self.client, 'error')+" | Somehow your calculation returns an error...")             
            else:
                return await ctx.message.add_reaction(emote(self.client, 'error'))
    @command()
    @cooldown(3)
    async def quote(self, ctx):
        async with ctx.channel.typing():
            data = insp('https://quotes.herokuapp.com/libraries/math/random')
            text, quoter = data.split(' -- ')[0].replace('`', ''), data.split(' -- ')[1]
            await ctx.send(embed=discord.Embed(description=f'***{text}***\n\n-- {quoter} --', color=get_embed_color(discord)))

    @command()
    @cooldown(5)
    async def robohash(self, ctx, *args):
        if len(list(args))==0: url='https://robohash.org/'+str(src.randomhash())
        else: url = 'https://robohash.org/'+str(urlify(' '.join(list(args))))
        await ctx.send(file=discord.File(self.canvas.urltoimage(url), 'robohash.png'))

    @command()
    @cooldown(5)
    async def weather(self, ctx, *args):
        if len(list(args))==0: await ctx.send(emote(self.client, 'error')+" | Please send a location or a city!")
        else: await ctx.send(file=discord.File(self.canvas.urltoimage('https://wttr.in/'+str(urlify(' '.join(list(args))))+'.png?m'), 'weather.png'))

    @command()
    @cooldown(5)
    async def ufo(self, ctx):
        num = str(random.randint(50, 100))
        data = fetchJSON('http://ufo-api.herokuapp.com/api/sightings/search?limit='+num)
        if data['status']!='OK':
            await ctx.send(emote(self.client, 'error')+' | There was a problem on retrieving the info.\nThe server said: "'+str(data['status'])+'" :eyes:')
        else:
            ufo = random.choice(data['sightings'])
            embed = discord.Embed(title='UFO Sighting in '+str(ufo['city'])+', '+str(ufo['state']), description='**Summary:** '+str(ufo['summary'])+'\n\n**Shape:** '+str(ufo['shape'])+'\n**Sighting Date: **'+str(ufo['date'])[:-8].replace('T', ' ')+'\n**Duration: **'+str(ufo['duration'])+'\n\n[Article Source]('+str(ufo['url'])+')', colour=get_embed_color(discord))
            embed.set_footer(text='Username601 raided area 51 and found this!')
            await ctx.send(embed=embed)
    
    @command('rhymes')
    @cooldown(7)
    async def rhyme(self, ctx, *args):
        if len(list(args))==0: await ctx.send('Please input a word! And we will try to find the word that best rhymes with it.')
        else:
            wait, words = await ctx.send(emote(self.client, 'loading') + ' | Please wait... Searching...'), []
            data = fetchJSON('https://rhymebrain.com/talk?function=getRhymes&word='+str(urlify(' '.join(list(args)))))
            if len(data)<1: await wait.edit(content='We did not find any rhyming words corresponding to that letter.')
            else:
                for i in range(0, len(data)):
                    if data[i]['flags']=='bc': words.append(data[i]['word'])
                words = dearray(words)
                if len(words)>1950:
                    words = limitify(words)
                embed = discord.Embed(title='Words that rhymes with '+str(' '.join(list(args)))+':', description=words, colour=get_embed_color(discord))
                await wait.edit(content='', embed=embed)

    @command('sof')
    @cooldown(5)
    async def stackoverflow(self, ctx, *args):
        if len(list(args))==0:
            await ctx.send(emote(self.client, 'error')+' | Hey fellow developer, Try add a question!')
        else:
            try:
                query = urlify(' '.join(list(args)))
                data = fetchJSON("https://api.stackexchange.com/2.2/search/advanced?q="+str(query)+"&site=stackoverflow&page=1&answers=1&order=asc&sort=relevance")
                leng = len(data['items'])
                ques = data['items'][0]
                tags = ''
                for i in range(0, len(ques['tags'])):
                    if i==len(ques['tags'])-1:
                        tags += '['+str(ques['tags'][i])+'](https://stackoverflow.com/questions/tagged/'+str(ques['tags'][i])+')'
                        break
                    tags += '['+str(ques['tags'][i])+'](https://stackoverflow.com/questions/tagged/'+str(ques['tags'][i])+') | '
                embed = discord.Embed(title=ques['title'], description='**'+str(ques['view_count'])+' *desperate* developers looked into this post.**\n**TAGS:** '+str(tags), url=ques['link'], colour=get_embed_color(discord))
                embed.set_author(name=ques['owner']['display_name'], url=ques['owner']['link'], icon_url=ques['owner']['profile_image'])
                embed.set_footer(text='Shown 1 result out of '+str(leng)+' results!')
                await ctx.send(embed=embed)
            except:
                await ctx.send(emote(self.client, 'error') + ' | There was an error on searching! Please check your spelling :eyes:')

    @command('birbfact,birdfact')
    @cooldown(7)
    async def pandafact(self, ctx):
        if 'pandafact' in str(ctx.message.content).lower(): link = 'https://some-random-api.ml/facts/panda'
        else: link = 'https://some-random-api.ml/facts/bird'
        data = fetchJSON(link)['fact']
        await ctx.send(embed=discord.Embed(title='Did you know?', description=data, colour=get_embed_color(discord)))

    @command()
    @cooldown(2)
    async def iss(self, ctx):
        iss, ppl, total = fetchJSON('https://open-notify-api.herokuapp.com/iss-now.json'), fetchJSON('https://open-notify-api.herokuapp.com/astros.json'), '```'
        for i in range(0, len(ppl['people'])):
            total += str(i+1) + '. ' + ppl['people'][i]['name'] + ((20-(len(ppl['people'][i]['name'])))*' ') + ppl['people'][i]['craft'] + '\n'
        embed = discord.Embed(title='Position: '+str(iss['iss_position']['latitude'])+' '+str(iss['iss_position']['longitude']), description='**People at craft:**\n\n'+str(total)+'```', colour=get_embed_color(discord))
        await ctx.send(embed=embed)

    @command('ghibli')
    @cooldown(5)
    async def ghiblifilms(self, ctx, *args):
        wait = await ctx.send(emote(self.client, 'loading') + ' | Please wait... Getting data...')
        data = fetchJSON('https://ghibliapi.herokuapp.com/films')
        if len(list(args))==0:
            films = ""
            for i in range(0, int(len(data))):
                films = films+'('+str(int(i)+1)+') '+str(data[i]['title']+' ('+str(data[i]['release_date'])+')\n')
            embed = discord.Embed(
                title = 'List of Ghibli Films',
                description = str(films),
                color = get_embed_color(discord)
            )
            embed.set_footer(text='Type `'+str(prefix)+'ghibli <number>` to get each movie info.')
            await wait.edit(content='', embed=embed)
        else:
            try:
                num = int([i for i in list(args) if i.isnumeric()][0])-1
                embed = discord.Embed(
                    title = data[num]['title'] + ' ('+str(data[num]['release_date'])+')',
                    description = '**Rotten Tomatoes Rating: '+str(data[num]['rt_score'])+'%**\n'+data[num]['description'],
                    color = get_embed_color(discord)
                )
                embed.add_field(name='Directed by', value=data[num]['director'], inline='True')
                embed.add_field(name='Produced by', value=data[num]['producer'], inline='True')
                await wait.edit(content='', embed=embed)
            except: await wait.edit(content=emote(self.client, 'error')+' | the movie you requested does not exist!?')

    @command()
    @cooldown(5)
    async def steamprofile(self, ctx, *args):
        try:
            getprof = urlify(list(args)[0].lower())
            data = fetchJSON('https://api.alexflipnote.dev/steam/user/'+str(getprof))
            state, privacy, url, username, avatar, custom_url, steam_id = data["state"], data["privacy"], data["url"], data["username"], data["avatarfull"], data["customurl"], data["steamid64"]
            embed = discord.Embed(title=username, description='**[Profile Link]('+str(url)+')**\n**Current state: **'+str(state)+'\n**Privacy: **'+str(privacy)+'\n**[Profile pic URL]('+str(avatar)+')**', colour = get_embed_color(discord))
            embed.set_thumbnail(url=avatar)
            await ctx.send(embed=embed)
        except:
            await ctx.send(emote(self.client, 'error')+" | Error; profile not found!")

    @command('nation')
    @cooldown(5)
    async def country(self, ctx, *args):
        try:
            country = urlify(' '.join(list(args)))
            data = self.canvas.country(country)
            file = discord.File(data['buffer'], 'country.png')
            embed = discord.Embed(title=' '.join(list(args)), color=discord.Color.from_rgb(
                data['color'][0], data['color'][1], data['color'][2]
            ))
            embed.set_thumbnail(url=data['image'])
            embed.set_image(url='attachment://country.png')
            return await ctx.send(file=file, embed=embed)
        except:
            return await ctx.send('{} | Country not found!'.format(emote(self.client, 'error')))

    @command()
    @cooldown(1)
    async def search(self, ctx, *args):
        if len(list(args))==0:
            await ctx.send(emote(self.client, 'error')+" | Please send something to search for......")
        else:
            data = loads(open("/app/assets/json/search.json", "r").read())
            await ctx.send(embed=discord.Embed(title='Internet searches for '+str(' '.join(list(args)), description=str('\n'.join(data)).replace('{QUERY}', urlify(' '.join(list(args))), color=get_embed_color(discord)))))

    @command()
    @cooldown(5)
    async def randomword(self, ctx):
        async with ctx.channel.typing():
            await ctx.send(fetchJSON("https://random-word-api.herokuapp.com/word?number=1")[0])

    @command()
    @cooldown(5)
    async def bored(self, ctx):
        data = fetchJSON("https://www.boredapi.com/api/activity?participants=1")
        await ctx.send('**Feeling bored?**\nWhy don\'t you '+str(data['activity'])+'? :wink::ok_hand:')

    @command()
    @cooldown(10)
    async def googledoodle(self, ctx):
        wait = await ctx.send(emote(self.client, 'loading') + ' | Please wait... This may take a few moments...')
        data = fetchJSON('https://www.google.com/doodles/json/{}/{}'.format(str(t.now().year), str(t.now().month)))[0]
        embed = discord.Embed(title=data['title'], colour=get_embed_color(discord), url='https://www.google.com/doodles/'+data['name'])
        embed.set_image(url='https:'+data['high_res_url'])
        embed.set_footer(text='Event date: '+str('/'.join(
            [str(i) for i in data['run_date_array'][::-1]]
        )))
        await wait.edit(content='', embed=embed)

    @command()
    @cooldown(6)
    async def steamapp(self, ctx, *args):
        data = fetchJSON('https://store.steampowered.com/api/storesearch?term='+urlify(str(' '.join(list(args))))+'&cc=us&l=en')
        if data['total']==0: await ctx.send(emote(self.client, 'error')+' | Did not found anything. Maybe that app *doesn\'t exist...*')
        else:
            try:
                prize = data['items'][0]['price']['initial']
                prize = str(prize / 100)+ ' ' + data['items'][0]['price']['currency']
            except KeyError: prize = 'FREE'
            if data['items'][0]['metascore']=="": rate = '???'
            else: rate = str(data['items'][0]['metascore'])
            oss_raw = []
            for i in range(0, len(data['items'][0]['platforms'])):
                if data['items'][0]['platforms'][str(list(data['items'][0]['platforms'].keys())[i])]==True:
                    oss_raw.append(str(list(data['items'][0]['platforms'].keys())[i]))
            embed = discord.Embed(title=data['items'][0]['name'], url='https://store.steampowered.com/'+str(data['items'][0]['type'])+'/'+str(data['items'][0]['id']), description='**Price tag:** '+str(prize)+'\n**Metascore: **'+str(rate)+'\n**This app supports the following OSs: **'+str(dearray(oss_raw)), colour=get_embed_color(discord))
            embed.set_image(url=data['items'][0]['tiny_image'])
            await ctx.send(embed=embed)

    @command('dogfact,funfact')
    @cooldown(6)
    async def catfact(self, ctx):
        if 'cat' in str(ctx.message.content).lower(): await ctx.send('**Did you know?**\n'+str(fetchJSON("https://catfact.ninja/fact")['fact']))
        elif 'dog' in str(ctx.message.content).lower(): await ctx.send('**Did you know?**\n'+str(fetchJSON("https://dog-api.kinduff.com/api/facts")['facts'][0]))
        else:
            await ctx.send('**Did you know?**\n'+str(fetchJSON("https://useless-api--vierofernando.repl.co/randomfact")['fact']))

    @command('em')
    @cooldown(2)
    async def embed(self, ctx, *args):
        if '(title:' not in list(args) or '(desc:' not in list(args):
            if len(list(args))==0:
                await message.channel.send(emote(self.client, 'error')+' | no args for you.')
            else:
                try:
                    await ctx.send(embed=discord.Embed(
                        description=str(' '.join(list(args)))
                    ))
                except:
                    await ctx.send(emote(self.client, 'error')+' | that is too long.')
        else:
            msg = str(' '.join(list(args)))
            try:
                title_e, desc_e = msg.split('(title:')[1].split(')')[0], msg.split('(desc:')[1].split(')')[0]
                if '(footer:' in msg:
                    foot = msg.split('(footer:')[1].split(')')[0]
                    embed.set_footer(text=foot)
                if '(auth:' in msg:
                    auth = msg.split('(auth:')[1].split(')')[0]
                    embed.set_author(name=auth)
                if '(hex:' not in msg:
                    embed = discord.Embed(title=title_e, description=desc_e, colour=discord.Colour.from_rgb(random.randint(0, 255), random.randint(0, 255), random.randint(0, 255)))
                else:
                    if msg.split('(hex:')[1].split(')')[0].startswith('#'): hexer = msg.split('(hex:')[1].split(')')[0][1:]
                    else: hexer = msg.split('(hex:')[1].split(')')[0]
                    arr = convertrgb(hexer, '0')
                    embed = discord.Embed(title=title_e, description=desc_e, colour=discord.Colour.from_rgb(arr[0], arr[1], arr[2]))
                await message.channel.send(embed=embed)
            except Exception as e:
                await message.channel.send(emote(self.client, 'error') + f' | An error occurd. For programmers: ```{e}```')

    @command('colourinfo,color-info,randomcolor,randomcolour,colour-info')
    @cooldown(10)
    async def colorinfo(self, ctx, *args):
        continuing, args = False, list(args)
        if str(ctx.message.content).startswith(prefix+'randomcolor') or str(ctx.message.content).startswith(prefix+'randomcolour'):
            listHex, hexCode = list('0123456789ABCDEF'), ''
            for i in range(0, 6):
                ran = random.choice(listHex)
                hexCode += ran
            continuing = True
        else:
            if len(args)!=1: await ctx.send(emote(self.client, 'error') +' | Invalid arguments.')
            elif args[0].startswith('#'): hexCode = args[0][1:] ; continuing = True
            elif args[0] in list('0123456789ABCDEF') and len(args[0])==6: hexCode = args[0] ; continuing = True
            elif args[0].isnumeric(): hexCode = str(tohex(args[0])) ; continuing = True
            elif len(args[0])!=6: await ctx.send(emote(self.client, 'error')+' | We only accept `HEX CODES` and `INTEGER VALUES` as inputs!')
            else: hexCode = args[0] ; continuing = True
        if continuing:
            rgb = convertrgb(hexCode, '0')
            percentageRgb = convertrgb(hexCode, '1')
            colorInt = int(hexCode, 16)
            embed = discord.Embed(title='#'+str(hexCode), description="**Integer: **`"+str(colorInt)+"`\n**Red:** "+str(rgb[0])+" ("+str(percentageRgb[0])+"%)\n**Green:** "+str(rgb[1])+" ("+str(percentageRgb[1])+"%)\n**Blue:** "+str(rgb[2])+" ("+str(percentageRgb[2])+"%)\n\nPreview is shown on thumbnail. Other similar gradients are shown below.", colour=discord.Colour.from_rgb(int(rgb[0]), int(rgb[1]), int(rgb[2])))
            embed.set_thumbnail(url='https://api.alexflipnote.dev/colour/image/'+str(hexCode))
            embed.set_image(url='https://api.alexflipnote.dev/colour/image/gradient/'+str(hexCode))
            await ctx.send(embed=embed)
    
    @command('fast')
    @cooldown(10)
    async def typingtest(self, ctx):
        async with ctx.channel.typing():
            data = fetchJSON("https://random-word-api.herokuapp.com/word?number=5")
            text, guy, first = arrspace(data), ctx.author, t.now().timestamp()
            main = await ctx.send(content='**Type the text on the image. (Only command invoker can play)**\nYou have 2 minutes.\n', file=discord.File(self.canvas.simpletext(text), 'test.png'))
        def check(m):
            return m.author == guy
        try:
            trying = await self.client.wait_for('message', check=check, timeout=120.0)
        except:
            await main.edit(content='Time is up.')
        if str(trying.content)!=None:
            offset = t.now().timestamp()-first
            asked, answered, wrong = text.lower(), str(trying.content).lower(), 0
            for i in range(len(asked)):
                try:
                    if asked[i]!=answered[i]: wrong += 1
                except: break
            try: accuracy, cps = round((len(asked)-wrong)/len(asked)*100), round(len(answered)/offset)
            except: accuracy, cps = "???", "???"
            await ctx.send(embed=discord.Embed(title='TYPING TEST RESULTS', description='**Your time: **'+str(round(offset))+' seconds.\n**Your accuracy: **'+str(accuracy)+'%\n**Your speed: **'+str(cps)+' Characters per second.', colour=get_embed_color(discord)))

def setup(client):
    client.add_cog(utils(client))
