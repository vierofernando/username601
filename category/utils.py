import discord
from discord.ext import commands
import sys
sys.path.append('/home/runner/hosting601/modules')
import username601 as myself
from canvas import Painter
from username601 import *
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
            r'/home/runner/hosting601/assets/pics/',
            r'/home/runner/hosting601/assets/fonts/'
        )
    
    @command('isitup,webstatus')
    @cooldown(2)
    async def isitdown(self, ctx, *args):
        if len(list(args))==0: return await ctx.send('{} | Please send a website link...'.format(self.client.get_emoji(BotEmotes.error)))
        wait = await ctx.send('{} | Pinging...'.format(self.client.get_emoji(BotEmotes.loading)))
        web = list(args)[0].replace('<', '').replace('>', '')
        if not web.startswith('http'): web = 'http://' + web
        try:
            a = t.now()
            ping = get(web, timeout=5)
            pingtime = round((t.now()-a).total_seconds()*1000)
            await wait.edit(content='{} | That website is up.\nPing: {} ms\nStatus code: {}'.format(self.client.get_emoji(BotEmotes.success), pingtime, ping.status_code))
        except:
            await wait.edit(content='{} | Yes. that website is down.'.format(self.client.get_emoji(BotEmotes.error)))
    
    @command('img2ascii,imagetoascii,avascii,avatarascii,avatar2ascii,av2ascii')
    @cooldown(10)
    async def imgascii(self, ctx, *args):
        url = myself.getUserAvatar(ctx, args)
        wait = await ctx.send('{} | Please wait...'.format(self.client.get_emoji(BotEmotes.loading)))
        text = self.canvas.imagetoASCII(url)
        data = post("https://hastebin.com/documents", data=text)
        if data.status_code!=200: return await wait.edit(content="{} | Oops! there was an error on posting it there.".format(self.client.get_emoji(BotEmotes.error)))
        return await wait.edit(content='{} | You can see the results at **https://hastebin.com/{}**!'.format(self.client.get_emoji(BotEmotes.success), data.json()['key']))
    
    @command()
    @cooldown(15)
    async def nasa(self, ctx, *args):
        query = 'earth' if len(list(args))==0 else myself.urlify(' '.join(list(args)))
        data = myself.jsonisp(f'https://images-api.nasa.gov/search?q={query}&media_type=image')
        await ctx.message.channel.trigger_typing()
        if len(data['collection']['items'])==0: return await ctx.send('{} | Nothing found.'.format(self.client.get_emoji(BotEmotes.error)))
        img = random.choice(data['collection']['items'])
        em = discord.Embed(title=img['data'][0]['title'], description=img['data'][0]["description"], color=discord.Colour.from_rgb(201, 160, 112))
        em.set_image(url=img['links'][0]['href'])
        await ctx.send(embed=em)

    @command('pokedex,dex,bulbapedia,pokemoninfo,poke-info,poke-dex,pokepedia')
    @cooldown(10)
    async def pokeinfo(self, ctx, *args):
        query = 'Missingno' if (len(list(args))==0) else myself.urlify(' '.join(list(args)))
        try:
            data = myself.jsonisp('https://bulbapedia.bulbagarden.net/w/api.php?action=query&titles={}&format=json&formatversion=2&pithumbsize=150&prop=extracts|pageimages&explaintext&redirects&exintro'.format(query))
            embed = discord.Embed(
                url='https://bulbapedia.bulbagarden.net/wiki/{}'.format(query),
                color=discord.Colour.from_rgb(201, 160, 112),
                title=data['query']['pages'][0]['title'], description=myself.limitto(data['query']['pages'][0]['extract'], 1000)
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
                str(self.client.get_emoji(BotEmotes.error))
            ))

    @command('recipes,cook')
    @cooldown(2)
    async def recipe(self, ctx, *args):
        if len(list(args))==0:
            await ctx.send(embed=discord.Embed(title='Here is a recipe to cook nothing:', description='1. Do nothing\n2. Profit'))
        else:
            data = myself.jsonisp("http://www.recipepuppy.com/api/?q={}".format(myself.urlify(' '.join(list(args)))))
            if len(data['results'])==0: 
                await ctx.send("{} | Did not find anything.".format(str(self.client.get_emoji(BotEmotes.error))))
            elif len([i for i in data['results'] if i['thumbnail']!=''])==0:
                await ctx.send("{} | Did not find anything with a delicious picture.".format(str(self.client.get_emoji(BotEmotes.error))))
            else:
                total = random.choice([i for i in data['results'] if i['thumbnail']!=''])
                embed = discord.Embed(title=total['title'], url=total['href'], description='Ingredients:\n{}'.format(total['ingredients']), color=discord.Colour.from_rgb(201, 160, 112))
                embed.set_image(url=total['thumbnail'])
                await ctx.send(embed=embed)

    @command()
    @cooldown(5)
    async def time(self, ctx):
        data = myself.api("http://worldtimeapi.org/api/timezone/africa/accra")
        year, time, date = str(data["utc_datetime"])[:-28], str(data["utc_datetime"])[:-22], str(str(data["utc_datetime"])[:-13])[11:]
        if int(year)%4==0: yearType, yearLength = 'It is a leap year.', 366
        else: yearType, yearLength = 'It is not a leap year yet.', 365
        progressDayYear = round(int(data["day_of_year"])/int(yearLength)*100)
        progressDayWeek = round(int(data["day_of_week"])/7*100)
        embed = discord.Embed(
            title = str(date)+' | '+str(time)+' (API)',
            description = str(t.now())[:-7]+' (SYSTEM)\nBoth time above is on UTC.\n**Unix Time:** '+str(data["unixtime"])+'\n**Day of the year: **'+str(data["day_of_year"])+' ('+str(progressDayYear)+'%)\n**Day of the week: **'+str(data["day_of_week"])+' ('+str(progressDayWeek)+'%)\n'+str(yearType),
            colour = discord.Colour.from_rgb(201, 160, 112)
        )
        await ctx.send(embed=embed)
    @command()
    @cooldown(3)
    async def calc(self, ctx, *args):
        if len(list(args))==0: await ctx.send(str(self.client.get_emoji(BotEmotes.error))+" | You need something... i smell no args nearby.")
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
                    await ctx.send(str(self.client.get_emoji(BotEmotes.error))+" | Somehow your calculation returns an error...")             
    @command()
    @cooldown(7)
    async def quote(self, ctx):
        async with ctx.message.channel.typing():
            data = myself.insp('https://quotes.herokuapp.com/libraries/math/random')
            text, quoter = data.split(' -- ')[0], data.split(' -- ')[1]
            await ctx.send(embed=discord.Embed(description=f'***{text}***\n\n-- {quoter} --', color=discord.Colour.from_rgb(201, 160, 112)))

    @command()
    @cooldown(10)
    async def robohash(self, ctx, *args):
        if len(list(args))==0: url='https://robohash.org/'+str(src.randomhash())
        else: url = 'https://robohash.org/'+str(myself.urlify(' '.join(list(args))))
        await ctx.send(file=discord.File(self.canvas.urltoimage(url), 'robohash.png'))

    @command()
    @cooldown(10)
    async def weather(self, ctx, *args):
        if len(list(args))==0: await ctx.send(str(self.client.get_emoji(BotEmotes.error))+" | Please send a location or a city!")
        else: await ctx.send(file=discord.File(self.canvas.urltoimage('https://wttr.in/'+str(myself.urlify(' '.join(list(args))))+'.png?m'), 'weather.png'))

    @command()
    @cooldown(10)
    async def ufo(self, ctx):
        num = str(random.randint(50, 100))
        data = myself.api('http://ufo-api.herokuapp.com/api/sightings/search?limit='+num)
        if data['status']!='OK':
            await ctx.send(str(self.client.get_emoji(BotEmotes.error))+' | There was a problem on retrieving the info.\nThe server said: "'+str(data['status'])+'" :eyes:')
        else:
            ufo = random.choice(data['sightings'])
            embed = discord.Embed(title='UFO Sighting in '+str(ufo['city'])+', '+str(ufo['state']), description='**Summary:** '+str(ufo['summary'])+'\n\n**Shape:** '+str(ufo['shape'])+'\n**Sighting Date: **'+str(ufo['date'])[:-8].replace('T', ' ')+'\n**Duration: **'+str(ufo['duration'])+'\n\n[Article Source]('+str(ufo['url'])+')', colour=discord.Colour.from_rgb(201, 160, 112))
            embed.set_footer(text='Username601 raided area 51 and found this!')
            await ctx.send(embed=embed)
    
    @command('rhymes')
    @cooldown(7)
    async def rhyme(self, ctx, *args):
        if len(list(args))==0: await ctx.send('Please input a word! And we will try to find the word that best rhymes with it.')
        else:
            wait, words = await ctx.send(str(self.client.get_emoji(BotEmotes.loading)) + ' | Please wait... Searching...'), []
            data = myself.api('https://rhymebrain.com/talk?function=getRhymes&word='+str(myself.urlify(' '.join(list(args)))))
            if len(data)<1: await wait.edit(content='We did not find any rhyming words corresponding to that letter.')
            else:
                for i in range(0, len(data)):
                    if data[i]['flags']=='bc': words.append(data[i]['word'])
                words = myself.dearray(words)
                if len(words)>1950:
                    words = myself.limitify(words)
                embed = discord.Embed(title='Words that rhymes with '+str(' '.join(list(args)))+':', description=words, colour=discord.Colour.from_rgb(201, 160, 112))
                await wait.edit(content='', embed=embed)

    @command('sof')
    @cooldown(12)
    async def stackoverflow(self, ctx, *args):
        if len(list(args))==0:
            await ctx.send(str(self.client.get_emoji(BotEmotes.errorr))+' | Hey fellow developer, Try add a question!')
        else:
            try:
                query = myself.urlify(' '.join(list(args)))
                data = myself.jsonisp("https://api.stackexchange.com/2.2/search/advanced?q="+str(query)+"&site=stackoverflow&page=1&answers=1&order=asc&sort=relevance")
                leng = len(data['items'])
                ques = data['items'][0]
                tags = ''
                for i in range(0, len(ques['tags'])):
                    if i==len(ques['tags'])-1:
                        tags += '['+str(ques['tags'][i])+'](https://stackoverflow.com/questions/tagged/'+str(ques['tags'][i])+')'
                        break
                    tags += '['+str(ques['tags'][i])+'](https://stackoverflow.com/questions/tagged/'+str(ques['tags'][i])+') | '
                embed = discord.Embed(title=ques['title'], description='**'+str(ques['view_count'])+' *desperate* developers looked into this post.**\n**TAGS:** '+str(tags), url=ques['link'], colour=discord.Colour.from_rgb(201, 160, 112))
                embed.set_author(name=ques['owner']['display_name'], url=ques['owner']['link'], icon_url=ques['owner']['profile_image'])
                embed.set_footer(text='Shown 1 result out of '+str(leng)+' results!')
                await ctx.send(embed=embed)
            except:
                await ctx.send(str(self.client.get_emoji(BotEmotes.error)) + ' | There was an error on searching! Please check your spelling :eyes:')

    @command('birbfact,birdfact')
    @cooldown(7)
    async def pandafact(self, ctx):
        if 'pandafact' in str(ctx.message.content).lower(): link = 'https://some-random-api.ml/facts/panda'
        else: link = 'https://some-random-api.ml/facts/bird'
        data = myself.jsonisp(link)['fact']
        await ctx.send(embed=discord.Embed(title='Did you know?', description=data, colour=discord.Colour.from_rgb(201, 160, 112)))

    @command()
    @cooldown(2)
    async def iss(self, ctx):
        iss, ppl, total = myself.jsonisp('https://open-notify-api.herokuapp.com/iss-now.json'), myself.jsonisp('https://open-notify-api.herokuapp.com/astros.json'), '```'
        for i in range(0, len(ppl['people'])):
            total += str(i+1) + '. ' + ppl['people'][i]['name'] + ((20-(len(ppl['people'][i]['name'])))*' ') + ppl['people'][i]['craft'] + '\n'
        embed = discord.Embed(title='Position: '+str(iss['iss_position']['latitude'])+' '+str(iss['iss_position']['longitude']), description='**People at craft:**\n\n'+str(total)+'```', colour=discord.Colour.from_rgb(201, 160, 112))
        await ctx.send(embed=embed)

    @command('ghibli')
    @cooldown(5)
    async def ghiblifilms(self, ctx, *args):
        wait = await ctx.send(str(self.client.get_emoji(BotEmotes.loading)) + ' | Please wait... Getting data...')
        data = myself.api('https://ghibliapi.herokuapp.com/films')
        if len(list(args))==0:
            films = ""
            for i in range(0, int(len(data))):
                films = films+'('+str(int(i)+1)+') '+str(data[i]['title']+' ('+str(data[i]['release_date'])+')\n')
            embed = discord.Embed(
                title = 'List of Ghibli Films',
                description = str(films),
                color = discord.Colour.from_rgb(201, 160, 112)
            )
            embed.set_footer(text='Type `'+str(Config.prefix)+'ghibli <number>` to get each movie info.')
            await wait.edit(content='', embed=embed)
        else:
            try:
                num = int([i for i in list(args) if i.isnumeric()][0])-1
                embed = discord.Embed(
                    title = data[num]['title'] + ' ('+str(data[num]['release_date'])+')',
                    description = '**Rotten Tomatoes Rating: '+str(data[num]['rt_score'])+'%**\n'+data[num]['description'],
                    color = discord.Colour.from_rgb(201, 160, 112)
                )
                embed.add_field(name='Directed by', value=data[num]['director'], inline='True')
                embed.add_field(name='Produced by', value=data[num]['producer'], inline='True')
                await wait.edit(content='', embed=embed)
            except: await wait.edit(content=str(self.client.get_emoji(BotEmotes.error))+' | the movie you requested does not exist!?')

    @command()
    @cooldown(10)
    async def steamprofile(self, ctx, *args):
        try:
            getprof = myself.urlify(list(args)[0].lower())
            data = myself.jsonisp('https://api.alexflipnote.dev/steam/user/'+str(getprof))
            state, privacy, url, username, avatar, custom_url, steam_id = data["state"], data["privacy"], data["url"], data["username"], data["avatarfull"], data["customurl"], data["steamid64"]
            embed = discord.Embed(title=username, description='**[Profile Link]('+str(url)+')**\n**Current state: **'+str(state)+'\n**Privacy: **'+str(privacy)+'\n**[Profile pic URL]('+str(avatar)+')**', colour = discord.Color.from_rgb(201, 160, 112))
            embed.set_thumbnail(url=avatar)
            await ctx.send(embed=embed)
        except:
            await ctx.send(str(self.client.get_emoji(BotEmotes.error))+" | Error; profile not found!")

    @command()
    @cooldown(5)
    async def country(self, ctx, *args):
        country = myself.urlify(' '.join(list(args)))
        c = myself.api("https://restcountries.eu/rest/v2/name/"+str(country.lower()))
        if len(c[0]['borders'])==0: borderz = 'No borders.'
        else: borderz = myself.dearray(c[0]['borders'])
        embed = discord.Embed(
            title = c[0]['nativeName'],
            description = '**Capital:** '+str(c[0]['capital'])+'\n**Region: **'+str(c[0]['region'])+'\n**Sub Region: **'+str(c[0]['subregion'])+"\n**Population: **"+str(c[0]['population'])+"\n**Area: **"+str(c[0]['area'])+' km²\n**Time Zones:** '+str(myself.dearray(c[0]['timezones']))+'\n**Borders: **'+str(borderz),
            colour = discord.Colour.from_rgb(201, 160, 112)
        )
        embed.set_author(name=c[0]['name'])
        await ctx.send(embed=embed)

    @command()
    @cooldown(1)
    async def search(self, ctx, *args):
        if len(list(args))==0:
            await ctx.send(str(self.client.get_emoji(BotEmotes.error))+" | Please send something to search for......")
        else:
            data = loads(open("/app/assets/json/search.json", "r").read())
            await ctx.send(embed=discord.Embed(title='Internet searches for '+str(' '.join(list(args)), description=str('\n'.join(data)).replace('{QUERY}', myself.urlify(' '.join(list(args))), color=discord.Colour.from_rgb(201, 160, 112)))))

    @command()
    @cooldown(5)
    async def randomword(self, ctx):
        async with ctx.message.channel.typing():
            await ctx.send(myself.jsonisp("https://random-word-api.herokuapp.com/word?number=1")[0])

    @command()
    @cooldown(5)
    async def bored(self, ctx):
        data = myself.api("https://www.boredapi.com/api/activity?participants=1")
        await ctx.send('**Feeling bored?**\nWhy don\'t you '+str(data['activity'])+'? :wink::ok_hand:')

    @command()
    @cooldown(20)
    async def googledoodle(self, ctx):
        wait = await ctx.send(str(self.client.get_emoji(BotEmotes.loading)) + ' | Please wait... This may take a few moments...')
        data = myself.jsonisp('https://www.google.com/doodles/json/{}/{}'.format(str(t.now().year), str(t.now().month)))[0]
        embed = discord.Embed(title=data['title'], colour=discord.Colour.from_rgb(201, 160, 112), url='https://www.google.com/doodles/'+data['name'])
        embed.set_image(url='https:'+data['high_res_url'])
        embed.set_footer(text='Event date: '+str('/'.join(
            [str(i) for i in data['run_date_array'][::-1]]
        )))
        await wait.edit(content='', embed=embed)

    @command()
    @cooldown(10)
    async def steamapp(self, ctx, *args):
        data = myself.jsonisp('https://store.steampowered.com/api/storesearch?term='+myself.urlify(str(' '.join(list(args))))+'&cc=us&l=en')
        if data['total']==0: await ctx.send(str(self.client.get_emoji(BotEmotes.error))+' | Did not found anything. Maybe that app *doesn\'t exist...*')
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
            embed = discord.Embed(title=data['items'][0]['name'], url='https://store.steampowered.com/'+str(data['items'][0]['type'])+'/'+str(data['items'][0]['id']), description='**Price tag:** '+str(prize)+'\n**Metascore: **'+str(rate)+'\n**This app supports the following OSs: **'+str(myself.dearray(oss_raw)), colour=discord.Colour.from_rgb(201, 160, 112))
            embed.set_image(url=data['items'][0]['tiny_image'])
            await ctx.send(embed=embed)

    @command('dogfact,funfact')
    @cooldown(6)
    async def catfact(self, ctx):
        if 'cat' in str(ctx.message.content).lower(): await ctx.send('**Did you know?**\n'+str(myself.jsonisp("https://catfact.ninja/fact")['fact']))
        elif 'dog' in str(ctx.message.content).lower(): await ctx.send('**Did you know?**\n'+str(myself.jsonisp("https://dog-api.kinduff.com/api/facts")['facts'][0]))
        else:
            await ctx.send('**Did you know?**\n'+str(myself.jsonisp("https://useless-api--vierofernando.repl.co/randomfact")['fact']))

    @command('em')
    @cooldown(2)
    async def embed(self, ctx, *args):
        if '(title:' not in list(args) or '(desc:' not in list(args):
            if len(list(args))==0:
                await message.channel.send(str(self.client.get_emoji(BotEmotes.error))+' | no args for you.')
            else:
                try:
                    await ctx.send(embed=discord.Embed(
                        description=str(' '.join(list(args)))
                    ))
                except:
                    await ctx.send(str(self.client.get_emoji(BotEmotes.error))+' | that is too long.')
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
                    arr = myself.convertrgb(hexer, '0')
                    embed = discord.Embed(title=title_e, description=desc_e, colour=discord.Colour.from_rgb(arr[0], arr[1], arr[2]))
                await message.channel.send(embed=embed)
            except Exception as e:
                await message.channel.send(str(self.client.get_emoji(BotEmotes.error)) + f' | An error occurd. For programmers: ```{e}```')

    @command('colourinfo,color-info,randomcolor,randomcolour,colour-info')
    @cooldown(10)
    async def colorinfo(self, ctx, *args):
        continuing, args = False, list(args)
        if str(ctx.message.content).startswith(Config.prefix+'randomcolor') or str(ctx.message.content).startswith(Config.prefix+'randomcolour'):
            listHex, hexCode = list('0123456789ABCDEF'), ''
            for i in range(0, 6):
                ran = random.choice(listHex)
                hexCode += ran
            continuing = True
        else:
            if len(args)!=1: await ctx.send(str(self.client.get_emoji(BotEmotes.error)) +' | Invalid arguments.')
            elif args[0].startswith('#'): hexCode = args[0][1:] ; continuing = True
            elif args[0] in list('0123456789ABCDEF') and len(args[0])==6: hexCode = args[0] ; continuing = True
            elif args[0].isnumeric(): hexCode = str(myself.tohex(args[0])) ; continuing = True
            elif len(args[0])!=6: await ctx.send(str(self.client.get_emoji(BotEmotes.error))+' | We only accept `HEX CODES` and `INTEGER VALUES` as inputs!')
            else: hexCode = args[0] ; continuing = True
        if continuing:
            rgb = myself.convertrgb(hexCode, '0')
            percentageRgb = myself.convertrgb(hexCode, '1')
            colorInt = int(hexCode, 16)
            embed = discord.Embed(title='#'+str(hexCode), description="**Integer: **`"+str(colorInt)+"`\n**Red:** "+str(rgb[0])+" ("+str(percentageRgb[0])+"%)\n**Green:** "+str(rgb[1])+" ("+str(percentageRgb[1])+"%)\n**Blue:** "+str(rgb[2])+" ("+str(percentageRgb[2])+"%)\n\nPreview is shown on thumbnail. Other similar gradients are shown below.", colour=discord.Colour.from_rgb(int(rgb[0]), int(rgb[1]), int(rgb[2])))
            embed.set_thumbnail(url='https://api.alexflipnote.dev/colour/image/'+str(hexCode))
            embed.set_image(url='https://api.alexflipnote.dev/colour/image/gradient/'+str(hexCode))
            await ctx.send(embed=embed)
    
    @command('fast')
    @cooldown(10)
    async def typingtest(self, ctx):
        async with ctx.message.channel.typing():
            data = myself.api("https://random-word-api.herokuapp.com/word?number=5")
            text, guy, first = myself.arrspace(data), ctx.message.author, t.now().timestamp()
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
            accuracy, cps = round((len(asked)-wrong)/offset*100)
            await ctx.send(embed=discord.Embed(title='TYPING TEST RESULTS', description='**Your time: **'+str(round(offset))+' seconds.\n**Your accuracy: **'+str(accuracy)+'%\n**Your speed: **'+str(cps)+' Characters per second.', colour=discord.Colour.from_rgb(201, 160, 112)))

def setup(client):
    client.add_cog(utils(client))
