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
        if len(list(args))==0: return await ctx.send('{} | please gimme args, like `{}tv <showname>` or something'.format(self.client.utils.emote(self.client, 'error'), self.client.command_prefix))
        query = self.client.utils.urlify(' '.join(list(args)))
        data = get(f'http://api.tvmaze.com/singlesearch/shows?q={query}')
        if data.status_code==404: return await ctx.send('{} | Oops! did not found any movie.'.format(self.client.utils.emote(self.client, 'error')))
        try:
            data = data.json()
            star = str(':star:'*round(data['rating']['average'])) if data['rating']['average']!=None else 'No star rating provided.'
            em = discord.Embed(title=data['name'], url=data['url'], description=self.client.utils.html2discord(data['summary']), color=self.client.utils.get_embed_color())
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
        ), color=self.client.utils.get_embed_color())
        em.set_thumbnail(url=data['artworkUrl100'])
        em.set_author(name='iTunes', icon_url='https://i.imgur.com/PR29ow0.jpg', url='https://www.apple.com/itunes/')
        await ctx.send(embed=em)

    @command()
    @cooldown(5)
    async def translate(self, ctx, *args):
        wait = await ctx.send(self.client.utils.emote(self.client, 'loading') + ' | Please wait...') ; args = list(args)
        if len(args)>0:
            if self.client.utils.parse_parameter(tuple(args), '--list')['available']:
                lang = ''
                for bahasa in LANGUAGES:
                    lang = lang+str(bahasa)+' ('+str(LANGUAGES[bahasa])+')\n'
                embed = discord.Embed(title='List of supported languages', description=str(lang), colour=self.client.utils.get_embed_color())
                await wait.edit(content='', embed=embed)
            elif len(args)>1:
                destination = args[0]
                try:
                    toTrans = ' '.join(args[1:len(args)])
                except IndexError:
                    await wait.edit(self.client.utils.emote(self.client, 'error')+' | Gimme something to translate!')
                try:
                    translation = gtr.translate(toTrans, dest=destination)
                    embed = discord.Embed(description=translation.text, colour=self.client.utils.get_embed_color())
                    embed.set_footer(text=f'Translated {LANGUAGES[translation.src]} to {LANGUAGES[translation.dest]}.')
                    await wait.edit(content='', embed=embed)
                except Exception as e:
                    await wait.edit(content=self.client.utils.emote(self.client, 'error') + f' | An error occurred! ```py\n{e}```')
            else:
                await wait.edit(content=f'Please add a language! To have the list and their id, type\n`{self.client.command_prefix}translate --list`.')
        else:
            await wait.edit(content=f'Please add translations or\nType `{self.client.command_prefix}translate --list` for supported languages.')
    
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
                embed = discord.Embed(title=pageTitle, url=str(page.fullurl), description=str(explain), colour=self.client.utils.get_embed_color())
                await wait.edit(content='', embed=embed)
    @command()
    @cooldown(5)
    async def imdb(self, ctx, *args):
        wait, args = await ctx.send(self.client.utils.emote(self.client, 'loading') + ' | Please wait...'), list(args)
        if len(args)==0 or self.client.utils.parse_parameter(args, 'help')['available']:
            embed = discord.Embed(title='IMDb command help', description='Searches through the IMDb Movie database.\n{} are Parameters that is **REQUIRED** to get the info.\n\n', colour=self.client.utils.get_embed_color())
            embed.add_field(name='Commands', value=self.client.command_prefix+'imdb --top {NUMBER}\n'+self.client.command_prefix+'imdb help\n'+self.client.command_prefix+'imdb --movie {MOVIE_ID or MOVIE_NAME}', inline='False')
            return await wait.edit(content='', embed=embed)
        top = self.client.utils.parse_parameter(args, '--top', get_second_element=True, singular=True)
        if top['available']:
            try:
                num = int(top['secondparam'])
                if num>30 or num<2: num = 20
                arr = ia.get_top250_movies()
                total = '\n'.join([str(int(i)+1) + '. '+str(arr[i]['title'])+' (`'+str(arr[i].movieID)+'`)' for i in range(num)])
                embed = discord.Embed(title='IMDb Top '+str(num)+':', description=str(total), colour=self.client.utils.get_embed_color())
                return await wait.edit(content='', embed=embed)
            except:
                return await wait.edit(content=self.client.utils.emote(self.client, 'error') +' | Is the top thing you inputted REALLY a number?\nlike, Not top TEN, but top 10.\nGET IT?')
        movie_param = self.client.utils.parse_parameter(args, '--movie', get_second_element=True)
        if movie_param['available']:
            try:
                movieId = int(movie_param['secondparam']) if movie_param['secondparam'].isnumeric() else ia.search_movie(movie_param['secondparam'])[0].movieID
                theID = str(movieId)
                data = ia.get_movie(str(movieId))
                main_data = ia.get_movie_main(theID)
                try:
                    rating, cover, vote_count = main_data['data']['rating'], main_data['data']['cover url'], main_data['data']['votes']
                except KeyError: rating, cover, vote_count = None, None, 0
                embed = discord.Embed(title=data['title'], colour=self.client.utils.get_embed_color())
                await wait.edit(content=self.client.utils.emote(self.client, 'loading') + ' | Please wait... Retrieving data... this may take a while depending on how big the movie is.')
                emoteStar = ' '.join([':star:' for i in range(0, round(rating))]) if rating != None else '???'
                upload_date = ia.get_movie_release_info(str(theID))['data']['raw release dates'][0]['date']
                imdb_url = ia.get_imdbURL(data)
                embed.add_field(name='General Information', value=f'[IMDb URL here]({imdb_url})\n**Upload date: **{upload_date}\n**Written by: **'+main_data['data']['writer'][0]['name']+'\n**Directed by: **'+main_data['data']['director'][0]['name'])
                embed.add_field(name='Ratings', value=emoteStar+'\n**Overall rating: **'+str(rating)+'\n**Rated by '+str(vote_count)+' people**')
                if cover != None: embed.set_image(url=cover)
                return await wait.edit(content='', embed=embed)
            except Exception as e:
                print(e)
                return await wait.edit(content='{} | Oopsies! please input a valid ID/parameter...'.format(self.client.utils.emote(self.client, 'error')))
        await wait.edit(content=self.client.utils.emote(self.client, 'error')+' | Wrong syntax. Use `'+self.client.command_prefix+'imdb help` next time.')

def setup(client):
    client.add_cog(apps(client))