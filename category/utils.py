import discord
import sys
import random
from discord.ext import commands
from os import getcwd, name, environ
sys.path.append(environ['BOT_MODULES_DIR'])
from decorators import command, cooldown
from io import BytesIO
from requests import post, get
from json import loads
from datetime import datetime as t
from re import search

class utils(commands.Cog):
    def __init__(self, client):
        pass
    
    @command('trending,news')
    @cooldown(5)
    async def msn(self, ctx, *args):
        try:
            data = ctx.bot.utils.inspect_element("http://cdn.content.prod.cms.msn.com/singletile/summary/alias/experiencebyname/today?market=en-GB&source=appxmanifest&tenant=amp&vertical=news")
            imageURL = data.split('baseUri="')[1].split('"')[0] + data.split('src="')[1].split('?')[0].replace(".img", ".png")
            content = data.split('hint-wrap="true">')[1].split('<')[0]
            embed = discord.Embed(title=content, color=ctx.guild.me.roles[::-1][0].color)
            embed.set_image(url=imageURL)
            embed.set_footer(text="Content provided by msn.com")
            return await ctx.send(embed=embed)
        except Exception as e:
            await ctx.bot.get_user(ctx.bot.utils.config("OWNER_ID", integer=True)).send(f"yo, theres an error: `{str(e)}`")
            raise ctx.bot.utils.send_error_message("Oopsies, there was an error on searching the news.")
    
    @command('prsc,psrc,act,activity')
    @cooldown(3)
    async def presence(self, ctx, *args):
        async with ctx.channel.typing():
            user = ctx.bot.utils.getUser(ctx, args)
            if isinstance(user.activity, discord.Spotify):
                return await ctx.send(file=discord.File(ctx.bot.canvas.custom_panel(spt=user.activity), 'activity.png'))
            if user.activity is None: raise ctx.bot.utils.send_error_message(f"Sorry, but {user.display_name} has no activity...")
            title = "" if (not hasattr(user.activity, 'name')) else user.activity.name
            subtitle = "" if (not hasattr(user.activity, 'details')) else user.activity.details
            desc = "" if (not hasattr(user.activity, 'state')) else user.activity.state
            if ((subtitle == "") and (not desc == "")):
                temp = desc
                subtitle = temp
                desc = ""
            url = "https://cdn.discordapp.com/embed/avatars/0.png" if (not hasattr(user.activity, 'large_image_url')) else user.activity.large_image_url
            return await ctx.send(file=discord.File(ctx.bot.canvas.custom_panel(title=title, subtitle=subtitle, description=desc, icon=url), 'activity.png'))
    @command('colorthief,getcolor,accent,accentcolor,accent-color,colorpalette,color-palette')
    @cooldown(3)
    async def palette(self, ctx, *args):
        url, person = ctx.bot.utils.getUserAvatar(ctx, args), ctx.bot.utils.getUser(ctx, args)
        async with ctx.channel.typing():
            data = ctx.bot.canvas.get_multiple_accents(url)
            return await ctx.send(file=discord.File(ctx.bot.canvas.get_palette(data), 'palette.png'))

    @command('isitup,webstatus')
    @cooldown(2)
    async def isitdown(self, ctx, *args):
        if len(args)==0: raise ctx.bot.utils.send_error_message("Please send a website link.")
        wait = await ctx.send('{} | Pinging...'.format(ctx.bot.loading_emoji))
        web = args[0].replace('<', '').replace('>', '')
        if not web.startswith('http'): web = 'http://' + web
        try:
            a = t.now()
            ping = get(web, timeout=5)
            pingtime = round((t.now()-a).total_seconds()*1000)
            await wait.edit(content='{} | That website is up.\nPing: {} ms\nStatus code: {}'.format(ctx.bot.success_emoji, pingtime, ping.status_code))
        except:
            await wait.edit(content='{} | Yes. that website is down.'.format(ctx.bot.error_emoji))
    
    @command('img2ascii,imagetoascii,avascii,avatarascii,avatar2ascii,av2ascii')
    @cooldown(10)
    async def imgascii(self, ctx, *args):
        parsed_arg = ctx.bot.utils.parse_parameter(args, '--img')
        if parsed_arg['available']:
            args = parsed_arg['parsedarg']
            url = ctx.bot.utils.getUserAvatar(ctx, args)
            async with ctx.channel.typing():
                res_im = ctx.bot.canvas.imagetoASCII_picture(url)
                return await ctx.send(file=discord.File(res_im, 'imgascii.png'))
        url = ctx.bot.utils.getUserAvatar(ctx, args)
        wait = await ctx.send('{} | Please wait...'.format(ctx.bot.loading_emoji))
        text = ctx.bot.canvas.imagetoASCII(url)
        try:
            data = post("https://hastebin.com/documents", data=text, timeout=3)
            assert data.status_code == 200
        except:
            await wait.delete()
            file = discord.File(BytesIO(bytes(text, 'utf-8')), filename='ascii.txt')
            return await ctx.send(content="{} | Oops! there was an error on posting it there. Don't worry, instead i send it as an attachment here:\n(Tip: you can also add `--img` so i send it as an image attachment!)".format(ctx.bot.error_emoji), file=file)
        return await wait.edit(content='{} | You can see the results at **https://hastebin.com/{}**!'.format(ctx.bot.success_emoji, data.json()['key']))
    
    @command()
    @cooldown(15)
    async def nasa(self, ctx, *args):
        query = 'earth' if len(args)==0 else ctx.bot.utils.encode_uri(' '.join(args))
        data = ctx.bot.utils.fetchJSON(f'https://images-api.nasa.gov/search?q={query}&media_type=image')
        await ctx.channel.trigger_typing()
        if len(data['collection']['items'])==0: raise ctx.bot.utils.send_error_message("Nothing found.")
        img = random.choice(data['collection']['items'])
        em = discord.Embed(title=img['data'][0]['title'], description=img['data'][0]["description"], color=ctx.guild.me.roles[::-1][0].color)
        em.set_image(url=img['links'][0]['href'])
        await ctx.send(embed=em)

    @command('pokedex,dex,bulbapedia,pokemoninfo,poke-info,poke-dex,pokepedia')
    @cooldown(10)
    async def pokeinfo(self, ctx, *args):
        query = 'Missingno' if (len(args)==0) else ctx.bot.utils.encode_uri(' '.join(args))
        try:
            data = ctx.bot.utils.fetchJSON('https://bulbapedia.bulbagarden.net/w/api.php?action=query&titles={}&format=json&formatversion=2&pithumbsize=150&prop=extracts|pageimages&explaintext&redirects&exintro'.format(query))
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
            raise ctx.bot.utils.send_error_message("Pokemon not found.")

    @command('recipes,cook')
    @cooldown(2)
    async def recipe(self, ctx, *args):
        if len(args)==0:
            await ctx.send(embed=discord.Embed(title='Here is a recipe to cook nothing:', description='1. Do nothing\n2. Profit'))
        else:
            data = ctx.bot.utils.fetchJSON("http://www.recipepuppy.com/api/?q={}".format(ctx.bot.utils.encode_uri(' '.join(args))))
            if len(data['results'])==0: 
                raise ctx.bot.utils.send_error_message("I did not find anything.")
            elif len([i for i in data['results'] if i['thumbnail']!=''])==0:
                raise ctx.bot.utils.send_error_message("Did not found anything with a delicious picture.")
            else:
                total = random.choice([i for i in data['results'] if i['thumbnail']!=''])
                embed = discord.Embed(title=total['title'], url=total['href'], description='Ingredients:\n{}'.format(total['ingredients']), color=ctx.guild.me.roles[::-1][0].color)
                embed.set_image(url=total['thumbnail'])
                await ctx.send(embed=embed)

    @command('calculator,equ,equation,calculate')
    @cooldown(3)
    async def calc(self, ctx, *args):
        if len(args)==0: raise ctx.bot.utils.send_error_message("You need something... i smell no args nearby.")
        else:
            equation = ' '.join(args)
            replaceWith = "x>*;.>*;?>*;?>/;?>*;plus>+;minus>-;divide>/;multiply>*;divide by>/;times>*;subtract>-;add>+;power>**;powers>**;^>**"
            for rep in replaceWith.split(";"):
                equation = equation.replace(rep.split('>')[0], rep.split('>')[1])
            if search("[a-zA-Z]", equation): raise ctx.bot.utils.send_error_message("Please do NOT input something that contains letters. This is not eval, nerd.")
            try:
                res = eval(equation)
                return await ctx.send("{} | {} = `{}`".format(ctx.bot.success_emoji, equation, str(res)[0:1000]))
            except Exception as e:
                raise ctx.bot.utils.send_error_message(f"Error: {str(e)}")
    @command()
    @cooldown(7)
    async def quote(self, ctx):
        async with ctx.channel.typing():
            data = ctx.bot.utils.inspect_element('https://quotes.herokuapp.com/libraries/math/random')
            text, quoter = data.split(' -- ')[0], data.split(' -- ')[1]
            await ctx.send(embed=discord.Embed(description=f'***{text}***\n\n-- {quoter} --', color=ctx.guild.me.roles[::-1][0].color))

    @command()
    @cooldown(10)
    async def robohash(self, ctx, *args):
        if len(args)==0: url='https://robohash.org/'+str(src.randomhash())
        else: url = 'https://robohash.org/'+str(ctx.bot.utils.encode_uri(' '.join(args)))
        await ctx.send(file=discord.File(ctx.bot.canvas.urltoimage(url), 'robohash.png'))

    @command()
    @cooldown(10)
    async def weather(self, ctx, *args):
        if len(args)==0: raise ctx.bot.utils.send_error_message("Please send a location or a city!")
        else: await ctx.send(file=discord.File(ctx.bot.canvas.urltoimage('https://wttr.in/'+str(ctx.bot.utils.encode_uri(' '.join(args)))+'.png?m'), 'weather.png'))

    @command()
    @cooldown(10)
    async def ufo(self, ctx):
        num = str(random.randint(50, 100))
        data = ctx.bot.utils.fetchJSON('http://ufo-api.herokuapp.com/api/sightings/search?limit='+num)
        if data['status']!='OK':
            raise ctx.bot.utils.send_error_message('There was a problem on retrieving the info.\nThe server said: "'+str(data['status'])+'" :eyes:')
        else:
            ufo = random.choice(data['sightings'])
            embed = discord.Embed(title='UFO Sighting in '+str(ufo['city'])+', '+str(ufo['state']), description='**Summary:** '+str(ufo['summary'])+'\n\n**Shape:** '+str(ufo['shape'])+'\n**Sighting Date: **'+str(ufo['date'])[:-8].replace('T', ' ')+'\n**Duration: **'+str(ufo['duration'])+'\n\n[Article Source]('+str(ufo['url'])+')', colour=ctx.guild.me.roles[::-1][0].color)
            embed.set_footer(text='Username601 raided area 51 and found this!')
            await ctx.send(embed=embed)
    
    @command('rhymes')
    @cooldown(7)
    async def rhyme(self, ctx, *args):
        if len(args)==0: await ctx.send('Please input a word! And we will try to find the word that best rhymes with it.')
        else:
            wait, words = await ctx.send(str(ctx.bot.loading_emoji) + ' | Please wait... Searching...'), []
            data = ctx.bot.utils.fetchJSON('https://rhymebrain.com/talk?function=getRhymes&word='+str(ctx.bot.utils.encode_uri(' '.join(args))))
            if len(data)<1: await wait.edit(content='We did not find any rhyming words corresponding to that letter.')
            else:
                for i in range(len(data)):
                    if data[i]['flags']=='bc': words.append(data[i]['word'])
                words = dearray(words)
                if len(words)>1950:
                    words = limitify(words)
                embed = discord.Embed(title='Words that rhymes with '+str(' '.join(args))+':', description=words, colour=ctx.guild.me.roles[::-1][0].color)
                await wait.edit(content='', embed=embed)

    @command('sof')
    @cooldown(12)
    async def stackoverflow(self, ctx, *args):
        if len(args)==0:
            raise ctx.bot.utils.send_error_message('Hey fellow developer, Try add a question!')
        else:
            try:
                query = ctx.bot.utils.encode_uri(' '.join(args))
                data = ctx.bot.utils.fetchJSON("https://api.stackexchange.com/2.2/search/advanced?q="+str(query)+"&site=stackoverflow&page=1&answers=1&order=asc&sort=relevance")
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
                raise ctx.bot.utils.send_error_message('There was an error on searching! Please check your spelling :eyes:')

    @command('birbfact,birdfact')
    @cooldown(7)
    async def pandafact(self, ctx):
        if 'pandafact' in ctx.message.content.lower(): link = 'https://some-random-api.ml/facts/panda'
        else: link = 'https://some-random-api.ml/facts/bird'
        data = ctx.bot.utils.fetchJSON(link)['fact']
        await ctx.send(embed=discord.Embed(title='Did you know?', description=data, colour=ctx.guild.me.roles[::-1][0].color))

    @command()
    @cooldown(2)
    async def iss(self, ctx):
        iss, ppl, total = ctx.bot.utils.fetchJSON('https://open-notify-api.herokuapp.com/iss-now.json'), ctx.bot.utils.fetchJSON('https://open-notify-api.herokuapp.com/astros.json'), '```'
        for i in range(len(ppl['people'])):
            total += str(i+1) + '. ' + ppl['people'][i]['name'] + ((20-(len(ppl['people'][i]['name'])))*' ') + ppl['people'][i]['craft'] + '\n'
        embed = discord.Embed(title='Position: '+str(iss['iss_position']['latitude'])+' '+str(iss['iss_position']['longitude']), description='**People at craft:**\n\n'+str(total)+'```', colour=ctx.guild.me.roles[::-1][0].color)
        await ctx.send(embed=embed)

    @command('ghibli')
    @cooldown(5)
    async def ghiblifilms(self, ctx, *args):
        wait = await ctx.send(str(ctx.bot.loading_emoji) + ' | Please wait... Getting data...')
        data = ctx.bot.utils.fetchJSON('https://ghibliapi.herokuapp.com/films')
        if len(args)==0:
            films = ""
            for i in range(int(len(data))):
                films = films+'('+str(int(i)+1)+') '+str(data[i]['title']+' ('+str(data[i]['release_date'])+')\n')
            embed = discord.Embed(
                title = 'List of Ghibli Films',
                description = str(films),
                color = ctx.guild.me.roles[::-1][0].color
            )
            embed.set_footer(text='Type `'+str(ctx.bot.command_prefix[0])+'ghibli <number>` to get each movie info.')
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
            except: raise ctx.bot.utils.send_error_message('the movie you requested does not exist!?')

    @command()
    @cooldown(10)
    async def steamprofile(self, ctx, *args):
        try:
            getprof = ctx.bot.utils.encode_uri(args[0].lower())
            data = ctx.bot.utils.fetchJSON('https://api.alexflipnote.dev/steam/user/'+str(getprof))
            state, privacy, url, username, avatar, custom_url, steam_id = data["state"], data["privacy"], data["url"], data["username"], data["avatarfull"], data["customurl"], data["steamid64"]
            embed = discord.Embed(title=username, description='**[Profile Link]('+str(url)+')**\n**Current state: **'+str(state)+'\n**Privacy: **'+str(privacy)+'\n**[Profile pic URL]('+str(avatar)+')**', colour = ctx.guild.me.roles[::-1][0].color)
            embed.set_thumbnail(url=avatar)
            await ctx.send(embed=embed)
        except:
            raise ctx.bot.utils.send_error_message("Error: profile not found!")

    @command('nation')
    @cooldown(5)
    async def country(self, ctx, *args):
        try:
            country = ctx.bot.utils.encode_uri(' '.join(args))
            data = ctx.bot.canvas.country(country)
            file = discord.File(data['buffer'], 'country.png')
            embed = discord.Embed(title=' '.join(args), color=discord.Color.from_rgb(
                data['color'][0], data['color'][1], data['color'][2]
            ))
            embed.set_thumbnail(url=data['image'])
            embed.set_image(url='attachment://country.png')
            return await ctx.send(file=file, embed=embed)
        except:
            raise ctx.bot.utils.send_error_message('Country not found!')

    @command()
    @cooldown(5)
    async def bored(self, ctx):
        data = ctx.bot.utils.fetchJSON("https://www.boredapi.com/api/activity?participants=1")
        await ctx.send('**Feeling bored?**\nWhy don\'t you '+str(data['activity'])+'? :wink::ok_hand:')

    @command()
    @cooldown(20)
    async def googledoodle(self, ctx):
        wait = await ctx.send(str(ctx.bot.loading_emoji) + ' | Please wait... This may take a few moments...')
        data = ctx.bot.utils.fetchJSON('https://www.google.com/doodles/json/{}/{}'.format(str(t.now().year), str(t.now().month)))[0]
        embed = discord.Embed(title=data['title'], colour=ctx.guild.me.roles[::-1][0].color, url='https://www.google.com/doodles/'+data['name'])
        embed.set_image(url='https:'+data['high_res_url'])
        embed.set_footer(text='Event date: '+str('/'.join(
            [str(i) for i in data['run_date_array'][::-1]]
        )))
        await wait.edit(content='', embed=embed)

    @command()
    @cooldown(10)
    async def steamapp(self, ctx, *args):
        data = ctx.bot.utils.fetchJSON('https://store.steampowered.com/api/storesearch?term='+ctx.bot.utils.encode_uri(str(' '.join(args)))+'&cc=us&l=en')
        if data['total']==0: raise ctx.bot.utils.send_error_message('Did not found anything. Maybe that app *doesn\'t exist...*')
        else:
            try:
                prize = data['items'][0]['price']['initial']
                prize = str(prize / 100)+ ' ' + data['items'][0]['price']['currency']
            except KeyError: prize = 'FREE'
            if data['items'][0]['metascore']=="": rate = '???'
            else: rate = str(data['items'][0]['metascore'])
            oss_raw = []
            for i in range(len(data['items'][0]['platforms'])):
                if data['items'][0]['platforms'][str(list(data['items'][0]['platforms'].keys())[i])]==True:
                    oss_raw.append(str(list(data['items'][0]['platforms'].keys())[i]))
            embed = discord.Embed(title=data['items'][0]['name'], url='https://store.steampowered.com/'+str(data['items'][0]['type'])+'/'+str(data['items'][0]['id']), description='**Price tag:** '+str(prize)+'\n**Metascore: **'+str(rate)+'\n**This app supports the following OSs: **'+str(dearray(oss_raw)), colour=ctx.guild.me.roles[::-1][0].color)
            embed.set_image(url=data['items'][0]['tiny_image'])
            await ctx.send(embed=embed)

    @command('dogfact,funfact')
    @cooldown(6)
    async def catfact(self, ctx):
        if 'cat' in ctx.message.content.lower(): await ctx.send('**Did you know?**\n'+str(ctx.bot.utils.fetchJSON("https://catfact.ninja/fact")['fact']))
        elif 'dog' in ctx.message.content.lower(): await ctx.send('**Did you know?**\n'+str(ctx.bot.utils.fetchJSON("https://dog-api.kinduff.com/api/facts")['facts'][0]))
        else:
            await ctx.send('**Did you know?**\n'+str(ctx.bot.utils.fetchJSON("https://useless-api--vierofernando.repl.co/randomfact")['fact']))
    @command('em')
    @cooldown(2)
    async def embed(self, ctx, *args):
        try:
            return await ctx.send(embed=discord.Embed(description=' '.join(args)))
        except:
            return await ctx.message.add_reaction(ctx.bot.error_emoji)
            
    @command('col')
    @cooldown(3)
    async def color(self, ctx, *args):
        if len(args) == 0: raise ctx.bot.utils.send_error_message(f"Invalid argument. use `{ctx.bot.command_prefix[0]}help color` for more info.")
        async with ctx.channel.typing():
            parameter_data = ctx.bot.utils.parse_parameter(args, 'role', get_second_element=True)
            if parameter_data['available']:
                iterate_result = [i.id for i in ctx.guild.roles if parameter_data['secondparam'].lower() in i.name.lower()]
                if len(iterate_result) == 0: raise ctx.bot.utils.send_error_message("Role not found.")
                colim = ctx.bot.canvas.color(str(ctx.guild.get_role(iterate_result[0]).colour))
            else:
                colim = ctx.bot.canvas.color(None, (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))) if ctx.bot.utils.parse_parameter(args, 'random')['available'] else ctx.bot.canvas.color(' '.join(args))
            if colim is None: raise ctx.bot.utils.send_error_message("Please insert a valid Hex.")
            return await ctx.send(file=discord.File(colim, 'color.png'))
    
    @command('fast')
    @cooldown(10)
    async def typingtest(self, ctx):
        async with ctx.channel.typing():
            data = ctx.bot.utils.fetchJSON("https://random-word-api.herokuapp.com/word?number=5")
            text, guy, first = arrspace(data), ctx.author, t.now().timestamp()
            main = await ctx.send(content='**Type the text on the image. (Only command invoker can play)**\nYou have 2 minutes.\n', file=discord.File(ctx.bot.canvas.simpletext(text), 'test.png'))
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
    client.add_cog(utils(client))
