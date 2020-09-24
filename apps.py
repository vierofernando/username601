import discord
from discord.ext import commands
import sys
from os import getcwd, name, environ
sys.path.append(environ['BOT_MODULES_DIR'])
import imdb
ia = imdb.IMDb()
from datetime import datetime as t
from decorators import command, cooldown
from requests import get
import wikipediaapi
from googletrans import Translator, LANGUAGES
gtr = Translator()

class apps(commands.Cog):
    def __init__(self, client):
        self.client = client

    @command('movie')
    @cooldown(5)
    async def tv(self, ctx, *args):
        if len(list(args))==0: return await ctx.send('{} | please gimme args',format(self.client.utils.emote(self.client, 'error')))
        query = self.client.utils.urlify(' '.join(list(args)))
        data = get(f'http://api.tvmaze.com/singlesearch/shows?q={query}')
        if data.status_code==404: return await ctx.send('{} | Oops! did not found any movie.'.format(self.client.utils.emote(self.client, 'error')))
        try:
            data = data.json()
            star = str(':star:'*round(data['rating']['average'])) if data['rating']['average']!=None else 'No star rating provided.'
            em = discord.Embed(title=data['name'], url=data['url'], description=self.client.utils.html2discord(data['summary']), color=self.client.utils.get_embed_color(discord))
            em.add_field(name='General Information', value='**Status: **'+data['status']+'\n**Premiered at: **'+data['premiered']+'\n**Type: **'+data['type']+'\n**Language: **'+data['language']+'\n**Rating: **'+str(data['rating']['average'] if data['rating']['average']!=None else 'None')+'\n'+star)
            em.add_field(name='TV Network', value=data['network']['name']+' at '+data['network']['country']['name']+' ('+data['network']['country']['timezone']+')')
            em.add_field(name='Genre', value=str(', '.join(data['genres']) if len(data['genres'])>0 else 'no genre avaliable'))
            em.add_field(name='Schedule', value=', '.join(data['schedule']['days'])+' at '+data['schedule']['time'])
            em.set_image(url=data['image']['original'])
            await ctx.send(embed=em)
        except:
            await ctx.send('{} | Oops! There was an error...'.format(self.client.utils.emote(self.client, 'error')))

    @command('spot,splay,listeningto,sp')
    @cooldown(2)
    async def spotify(self, ctx, *args):
        source, act = self.client.utils.getUser(ctx, args), None
        for i in source.activities:
            if isinstance(i, discord.Spotify): act = i
        if act==None: return await ctx.send(self.client.utils.emote(self.client, 'error')+' | Nope, not listening to spotify.')
        async with ctx.message.channel.typing():
            await ctx.send(file=discord.File(self.client.canvas.spotify({
                'name': act.title,
                'artist': ', '.join(act.artists),
                'album': act.album,
                'url': act.album_cover_url
            }), 'spotify.png'))

    @command()
    @cooldown(5)
    async def itunes(self, ctx, *args):
        if len(list(args))==0: return await ctx.send('{} | Please send a search term!'.format(self.client.utils.emote(self.client, 'error')))
        data = self.client.utils.fetchJSON('https://itunes.apple.com/search?term={}&media=music&entity=song&limit=1&explicit=no'.format(self.client.utils.urlify(' '.join(list(args)))))
        if len(data['results'])==0: return await ctx.send('{} | No music found... oop'.format(self.client.utils.emote(self.client, 'error')))
        data = data['results'][0]
        em = discord.Embed(title=data['trackName'], url=data['trackViewUrl'],description='**Artist: **{}\n**Album: **{}\n**Release Date:** {}\n**Genre: **{}'.format(
            data['artistName'], data['collectionName'], data['releaseDate'].replace('T', ' ').replace('Z', ''), data['primaryGenreName']
        ), color=self.client.utils.get_embed_color(discord))
        em.set_thumbnail(url=data['artworkUrl100'])
        em.set_author(name='iTunes', icon_url='https://i.imgur.com/PR29ow0.jpg', url='https://www.apple.com/itunes/')
        await ctx.send(embed=em)

    @command()
    @cooldown(5)
    async def translate(self, ctx, *args):
        wait = await ctx.send(self.client.utils.emote(self.client, 'loading') + ' | Please wait...') ; args = list(args)
        if len(args)>0:
            if args[0]=='--list':
                lang = ''
                for bahasa in LANGUAGES:
                    lang = lang+str(bahasa)+' ('+str(LANGUAGES[bahasa])+')\n'
                embed = discord.Embed(title='List of supported languages', description=str(lang), colour=self.client.utils.get_embed_color(discord))
                await wait.edit(content='', embed=embed)
            elif len(args)>1:
                destination = args[0]
                try:
                    toTrans = ' '.join(args[1:len(args)])
                except IndexError:
                    await wait.edit(self.client.utils.emote(self.client, 'error')+' | Gimme something to translate!')
                try:
                    translation = gtr.translate(toTrans, dest=destination)
                    embed = discord.Embed(description=translation.text, colour=self.client.utils.get_embed_color(discord))
                    embed.set_footer(text=f'Translated {LANGUAGES[translation.src]} to {LANGUAGES[translation.dest]}.')
                    await wait.edit(content='', embed=embed)
                except Exception as e:
                    await wait.edit(content=self.client.utils.emote(self.client, 'error') + f' | An error occurred! ```py\n{e}```')
            else:
                await wait.edit(content=f'Please add a language! To have the list and their id, type\n`{self.client.utils.prefix}translate --list`.')
        else:
            await wait.edit(content=f'Please add translations or\nType `{self.client.utils.prefix}translate --list` for supported languages.')
    
    @command()
    @cooldown(5)
    async def wikipedia(self, ctx, *args):
        wait = await ctx.send(self.client.utils.emote(self.client, 'loading') + ' | Please wait...')
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
                embed = discord.Embed(title=pageTitle, url=str(page.fullurl), description=str(explain), colour=self.client.utils.get_embed_color(discord))
                await wait.edit(content='', embed=embed)
    @command()
    @cooldown(5)
    async def imdb(self, ctx, *args):
        wait, args = await ctx.send(self.client.utils.emote(self.client, 'loading') + ' | Please wait...'), list(args)
        if len(args)==0 or args[0].lower()=='help' or args[0].lower()=='--help':
            embed = discord.Embed(title='IMDb command help', description='Searches through the IMDb Movie database.\n{} are Parameters that is **REQUIRED** to get the info.\n\n', colour=self.client.utils.get_embed_color(discord))
            embed.add_field(name='Commands', value=self.client.utils.prefix+'imdb --top {NUMBER}\n'+self.client.utils.prefix+'imdb help\n'+self.client.utils.prefix+'imdb --movie {MOVIE_ID or MOVIE_NAME}', inline='False')
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
                        embed = discord.Embed(title='IMDb Top '+str(num)+':', description=str(total), colour=self.client.utils.get_embed_color(discord))
                        await wait.edit(content='', embed=embed)
                except ValueError:
                    await wait.edit(content=self.client.utils.emote(self.client, 'error') +' | Is the top thing you inputted REALLY a number?\nlike, Not top TEN, but top 10.\nGET IT?')
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
                embed = discord.Embed(title=data['title'], colour=self.client.utils.get_embed_color(discord))
                await wait.edit(content=self.client.utils.emote(self.client, 'loading') + ' | Please wait... Retrieving data...')
                emoteStar = ''
                for i in range(0, round(int(ia.get_movie_main(theID)['data']['rating']))):
                    emoteStar = emoteStar + ' :star:'
                upload_date = ia.get_movie_release_info(str(theID))['data']['raw release dates'][0]['date']
                imdb_url = ia.get_imdbURL(data)
                await wait.edit(content=self.client.utils.emote(self.client, 'loading') + ' | Please wait... Creating result...')
                embed.add_field(name='General Information', value=f'**IMDb URL: **{imdb_url}\n**Upload date: **{upload_date}\n**Written by: **'+ia.get_movie_main(str(theID))['data']['writer'][0]['name']+'\n**Directed by: **'+ia.get_movie_main(str(theID))['data']['director'][0]['name'])
                embed.add_field(name='Ratings', value=emoteStar+'\n**Overall rating: **'+str(ia.get_movie_main(str(theID))['data']['rating'])+'\n**Rated by '+str(ia.get_movie_main(str(theID))['data']['votes'])+' people**')
                embed.set_image(url=ia.get_movie_main(str(theID))['data']['cover url'])
                await wait.edit(content='', embed=embed)
            except KeyError:
                await wait.edit(content=self.client.utils.emote(self.client, 'error') + ' | An error occurred!\n**Good news, we *may* fix it.**')
                errorQuick = discord.Embed(title=data['title'], colour=self.client.utils.get_embed_color(discord))
                errorQuick.add_field(name='General Information', value=f'**IMDb URL: **{imdb_url}\n**Upload date: **{upload_date}')

                errorQuick.add_field(name='Ratings', value=emoteStar+'\n**Overall rating: **'+str(ia.get_movie_main(str(theID))['data']['rating'])+'\n**Rated by '+str(ia.get_movie_main(str(theID))['data']['votes'])+' people**')
                errorQuick.set_footer(text='Information given is limited due to Errors and... stuff.')
                await wait.edit(content='', embed=errorQuick)
        else:
            await wait.edit(content=self.client.utils.emote(self.client, 'error')+' | Wrong syntax. Use `'+self.client.utils.prefix+'imdb help` next time.')

def setup(client):
    client.add_cog(apps(client))