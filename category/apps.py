import discord
from discord.ext import commands
import imdb
ia = imdb.IMDb()
from datetime import datetime as t
import sys
sys.path.append('/home/runner/hosting601/modules')
from decorators import command, cooldown
import username601 as myself
from requests import get
from canvas import Painter
from username601 import *
import wikipediaapi
from googletrans import Translator, LANGUAGES
gtr = Translator()

class apps(commands.Cog):
    def __init__(self, client):
        self.client = client
        self.canvas = Painter(
            r'/home/runner/hosting601/assets/pics/',
            r'/home/runner/hosting601/assets/fonts/'
        )

    @command('movie')
    @cooldown(10)
    async def tv(self, ctx, *args):
        if len(list(args))==0: return await ctx.send('{} | please gimme args',format(str(self.client.get_emoji(BotEmotes.error))))
        query = myself.urlify(' '.join(list(args)))
        data = get(f'http://api.tvmaze.com/singlesearch/shows?q={query}')
        if data.status_code==404: return await ctx.send('{} | Oops! did not found any movie.'.format(str(self.client.get_emoji(BotEmotes.error))))
        try:
            data = data.json()
            star = str(':star:'*round(data['rating']['average'])) if data['rating']['average']!=None else 'No star rating provided.'
            em = discord.Embed(title=data['name'], url=data['url'], description=myself.html2discord(data['summary']), color=discord.Colour.from_rgb(201, 160, 112))
            em.add_field(name='General Information', value='**Status: **'+data['status']+'\n**Premiered at: **'+data['premiered']+'\n**Type: **'+data['type']+'\n**Language: **'+data['language']+'\n**Rating: **'+str(data['rating']['average'] if data['rating']['average']!=None else 'None')+'\n'+star)
            em.add_field(name='TV Network', value=data['network']['name']+' at '+data['network']['country']['name']+' ('+data['network']['country']['timezone']+')')
            em.add_field(name='Genre', value=str(myself.dearray(data['genres']) if len(data['genres'])>0 else 'no genre avaliable'))
            em.add_field(name='Schedule', value=myself.dearray(data['schedule']['days'])+' at '+data['schedule']['time'])
            em.set_image(url=data['image']['original'])
            await ctx.send(embed=em)
        except:
            await ctx.send('{} | Oops! There was an error...'.format(str(self.client.get_emoji(BotEmotes.error))))

    @command('spot,splay,listeningto')
    @cooldown(5)
    async def spotify(self, ctx, *args):
        source = myself.getUser(ctx, args)
        if str(source.activity).lower()!='spotify': await ctx.send(str(self.client.get_emoji(BotEmotes.error))+' | Nope, not listening to spotify. Please show spotify as your presence\nor turn off your custom status if you have it.')
        else:
            async with ctx.message.channel.typing():
                await ctx.send(file=discord.File(self.canvas.spotify({
                    'name': source.activity.title,
                    'artist': myself.dearray(source.activity.artists),
                    'album': source.activity.album,
                    'url': source.activity.album_cover_url
                }), 'spotify.png'))

    @command()
    @cooldown(10)
    async def itunes(self, ctx, *args):
        if len(list(args))==0: return await ctx.send('{} | Please send a search term!'.format(str(self.client.get_emoji(BotEmotes.error))))
        data = myself.jsonisp('https://itunes.apple.com/search?term={}&media=music&entity=song&limit=1&explicit=no'.format(myself.urlify(' '.join(list(args)))))
        if len(data['results'])==0: return await ctx.send('{} | No music found... oop'.format(self.client.get_emoji(BotEmotes.error)))
        data = data['results'][0]
        em = discord.Embed(title=data['trackName'], url=data['trackViewUrl'],description='**Artist: **{}\n**Album: **{}\n**Release Date:** {}\n**Genre: **{}'.format(
            data['artistName'], data['collectionName'], data['releaseDate'].replace('T', ' ').replace('Z', ''), data['primaryGenreName']
        ), color=discord.Color.from_rgb(201, 160, 112))
        em.set_thumbnail(url=data['artworkUrl100'])
        em.set_author(name='iTunes', icon_url='https://i.imgur.com/PR29ow0.jpg', url='https://www.apple.com/itunes/')
        await ctx.send(embed=em)

    @command()
    @cooldown(10)
    async def translate(self, ctx, *args):
        wait = await ctx.send(str(self.client.get_emoji(BotEmotes.loading)) + ' | Please wait...') ; args = list(args)
        if len(args)>0:
            if args[0]=='--list':
                lang = ''
                for bahasa in LANGUAGES:
                    lang = lang+str(bahasa)+' ('+str(LANGUAGES[bahasa])+')\n'
                embed = discord.Embed(title='List of supported languages', description=str(lang), colour=discord.Colour.from_rgb(201, 160, 112))
                await wait.edit(content='', embed=embed)
            elif len(args)>1:
                destination = args[0]
                try:
                    toTrans = ' '.join(args[1:len(args)])
                except IndexError:
                    await wait.edit(str(self.client.get_emoji(BotEmotes.error))+' | Gimme something to translate!')
                try:
                    translation = gtr.translate(toTrans, dest=destination)
                    embed = discord.Embed(description=translation.text, colour=discord.Colour.from_rgb(201, 160, 112))
                    embed.set_footer(text=f'Translated {LANGUAGES[translation.src]} to {LANGUAGES[translation.dest]}.')
                    await wait.edit(content='', embed=embed)
                except Exception as e:
                    await wait.edit(content=str(self.client.get_emoji(BotEmotes.error)) + f' | An error occurred! ```py\n{e}```')
            else:
                await wait.edit(content=f'Please add a language! To have the list and their id, type\n`{prefix}translate --list`.')
        else:
            await wait.edit(content=f'Please add translations or\nType `{prefix}translate --list` for supported languages.')
    
    @command()
    @cooldown(10)
    async def wikipedia(self, ctx, *args):
        wait = await ctx.send(str(self.client.get_emoji(BotEmotes.loading)) + ' | Please wait...')
        if len(list(args))==0:
            await wait.edit(content='Please input a page name!')
        else:
            wikipedia = wikipediaapi.Wikipedia('en')
            page = wikipedia.page(' '.join(list(args)))
            if page.exists()==False:
                await wait.edit(content='That page does not exist!\n40404040404040404040404')
            else:
                if ' may refer to:' in page.text:
                    byCategory = page.text.split('\n\n')
                    del byCategory[0]
                    temp = ''
                    totalCount = 0
                    for b in byCategory:
                        if b.startswith('See also') or len(temp)>950:
                            break
                        totalCount = int(totalCount)+1
                        temp = temp + str(totalCount)+'. ' + str(b) + '\n\n'
                    explain = temp
                    pageTitle = 'The page you may be refering to may be;'
                else:
                    pageTitle = page.title
                    explain = ''
                    count = 0
                    limit = random.choice(list(range(2, 4)))
                    for i in range(0, len(page.summary)):
                        if count==limit or len(explain)>900:
                            break
                        explain = explain + str(list(page.summary)[i])
                        if list(page.summary)[i]=='.':
                            count = int(count) + 1
                embed = discord.Embed(title=pageTitle, url=str(page.fullurl), description=str(explain), colour=discord.Colour.from_rgb(201, 160, 112))
                await wait.edit(content='', embed=embed)
    @command()
    @cooldown(10)
    async def imdb(self, ctx, *args):
        wait, args = await ctx.send(str(self.client.get_emoji(BotEmotes.loading)) + ' | Please wait...'), list(args)
        if len(args)==0 or args[0].lower()=='help' or args[0].lower()=='--help':
            embed = discord.Embed(title='IMDb command help', description='Searches through the IMDb Movie database.\n{} are Parameters that is **REQUIRED** to get the info.\n\n', colour=discord.Colour.from_rgb(201, 160, 112))
            embed.add_field(name='Commands', value=prefix+'imdb --top {NUMBER}\n'+prefix+'imdb help\n'+prefix+'imdb --movie {MOVIE_ID or MOVIE_NAME}', inline='False')
            await wait.edit(content='', embed=embed)
        elif args[0].lower()=='--top':
            if len(args)==1:
                await wait.edit(content='Please type the number!\nex: --top 5, --top 10, etc.')
            else:
                num = args[1]
                try:
                    if int(num)>30:
                        await wait.edit(content='That\'s too many movies to be listed!')
                    else:
                        arr, total = ia.get_top250_movies(), ''
                        for i in range(0, int(num)):
                            total = total + str(int(i)+1) + '. '+str(arr[i]['title'])+' (`'+str(arr[i].movieID)+'`)\n'
                        embed = discord.Embed(title='IMDb Top '+str(num)+':', description=str(total), colour=discord.Colour.from_rgb(201, 160, 112))
                        await wait.edit(content='', embed=embed)
                except ValueError:
                    await wait.edit(content=str(self.client.get_emoji(BotEmotes.error)) +' | Is the top thing you inputted REALLY a number?\nlike, Not top TEN, but top 10.\nGET IT?')
        elif args[0].lower()=='--movie':
            if args[0]=='--movie' and len(args)==1:
                await wait.edit(content='Where\'s the ID or movie name?!?!?!')
            else:
                if args[1].isnumeric()==True:
                    movieId = args[1]
                    theID = str(movieId)
                else:
                    q = ' '.join(list(args)[1:len(list(args))])
                    movieId = ia.search_movie(q)[0].movieID
                    theID = str(movieId)
                data = ia.get_movie(str(movieId))
            try:
                embed = discord.Embed(title=data['title'], colour=discord.Colour.from_rgb(201, 160, 112))
                await wait.edit(content=str(self.client.get_emoji(BotEmotes.loading)) + ' | Please wait... Retrieving data...')
                emoteStar = ''
                for i in range(0, round(int(ia.get_movie_main(theID)['data']['rating']))):
                    emoteStar = emoteStar + ' :star:'
                upload_date = ia.get_movie_release_info(str(theID))['data']['raw release dates'][0]['date']
                imdb_url = ia.get_imdbURL(data)
                await wait.edit(content=str(self.client.get_emoji(BotEmotes.loading)) + ' | Please wait... Creating result...')
                embed.add_field(name='General Information', value=f'**IMDb URL: **{imdb_url}\n**Upload date: **{upload_date}\n**Written by: **'+ia.get_movie_main(str(theID))['data']['writer'][0]['name']+'\n**Directed by: **'+ia.get_movie_main(str(theID))['data']['director'][0]['name'])
                embed.add_field(name='Ratings', value=emoteStar+'\n**Overall rating: **'+str(ia.get_movie_main(str(theID))['data']['rating'])+'\n**Rated by '+str(ia.get_movie_main(str(theID))['data']['votes'])+' people**')
                embed.set_image(url=ia.get_movie_main(str(theID))['data']['cover url'])
                await wait.edit(content='', embed=embed)
            except KeyError:
                await wait.edit(content=str(self.client.get_emoji(BotEmotes.error)) + ' | An error occurred!\n**Good news, we *may* fix it.**')
                errorQuick = discord.Embed(title=data['title'], colour=discord.Colour.from_rgb(201, 160, 112))
                errorQuick.add_field(name='General Information', value=f'**IMDb URL: **{imdb_url}\n**Upload date: **{upload_date}')

                errorQuick.add_field(name='Ratings', value=emoteStar+'\n**Overall rating: **'+str(ia.get_movie_main(str(theID))['data']['rating'])+'\n**Rated by '+str(ia.get_movie_main(str(theID))['data']['votes'])+' people**')
                errorQuick.set_footer(text='Information given is limited due to Errors and... stuff.')
                await wait.edit(content='', embed=errorQuick)
        else:
            await wait.edit(content=str(self.client.get_emoji(BotEmotes.error))+' | Wrong syntax. Use `'+Config.prefix+'imdb help` next time.')

def setup(client):
    client.add_cog(apps(client))