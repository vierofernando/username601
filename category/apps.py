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
import random
import wikipediaapi
from googletrans import Translator, LANGUAGES

class apps(commands.Cog):
    def __init__(self, client):
        self.client = client
        self.translator = Translator()

    @command('movie')
    @cooldown(5)
    async def tv(self, ctx, *args):
        if len(args)==0: raise self.client.utils.send_error_message("Please give TV shows as arguments.")
        query = self.client.utils.encode_uri(' '.join(args))
        data = get(f'http://api.tvmaze.com/singlesearch/shows?q={query}')
        if data.status_code==404: raise self.client.utils.send_error_message("Did not found anything.")
        try:
            data = data.json()
            star = str(':star:'*round(data['rating']['average'])) if data['rating']['average']!=None else 'No star rating provided.'
            em = discord.Embed(title=data['name'], url=data['url'], description=self.client.utils.clean_html(data['summary']), color=ctx.guild.me.roles[::-1][0].color)
            em.add_field(name='General Information', value='**Status: **'+data['status']+'\n**Premiered at: **'+data['premiered']+'\n**Type: **'+data['type']+'\n**Language: **'+data['language']+'\n**Rating: **'+str(data['rating']['average'] if data['rating']['average']!=None else 'None')+'\n'+star)
            em.add_field(name='TV Network', value=data['network']['name']+' at '+data['network']['country']['name']+' ('+data['network']['country']['timezone']+')')
            em.add_field(name='Genre', value=str(', '.join(data['genres']) if len(data['genres'])>0 else 'no genre avaliable'))
            em.add_field(name='Schedule', value=', '.join(data['schedule']['days'])+' at '+data['schedule']['time'])
            em.set_image(url=data['image']['original'])
            await ctx.send(embed=em)
        except:
            raise self.client.utils.send_error_message("There was an error on fetching the info.")

    @command('spot,splay,listeningto,sp')
    @cooldown(2)
    async def spotify(self, ctx, *args):
        source, act = self.client.utils.getUser(ctx, tuple([
                i for i in args if '--force' not in i
            ])), None
        if ''.join(args).endswith('--force'):
            force = True
            act = source.activity
        else:
            force = False
            for i in source.activities:
                if isinstance(i, discord.Spotify): act = i
            if act is None: raise self.client.utils.send_error_message(f"Sorry, but  {source.display_name} is not listening to spotify.")
        async with ctx.channel.typing():
            if force:
                try:
                    return await ctx.send(file=discord.File(self.client.canvas.custom_panel(spt=act), 'spotify.png'))
                except: return 
            await ctx.send(file=discord.File(self.client.canvas.custom_panel(spt=act), 'spotify.png'))

    @command()
    @cooldown(5)
    async def itunes(self, ctx, *args):
        if len(args)==0: raise self.client.utils.send_error_message("Please send a search term.")
        async with ctx.channel.typing():
            data = self.client.utils.fetchJSON('https://itunes.apple.com/search?term={}&media=music&entity=song&limit=1&explicit=no'.format(self.client.utils.encode_uri(' '.join(args))))
            if len(data['results'])==0: return await ctx.send('{} | No music found... oop'.format(self.client.error_emoji))
            data = data['results'][0]
            return await ctx.send(file=discord.File(self.client.canvas.custom_panel(title=data['trackName'], subtitle=data['artistName'], description=data['primaryGenreName'], icon=data['artworkUrl100']), 'itunes.png'))

    @command('tr,trans')
    @cooldown(5)
    async def translate(self, ctx, *args):
        wait = await ctx.send(self.client.loading_emoji + ' | Please wait...') ; args = list(args)
        if len(args)>0:
            if self.client.utils.parse_parameter(tuple(args), '--list')['available']:
                lang = "\n".join([str(i)+' ('+str(LANGUAGES[i])+')' for i in LANGUAGES])
                embed = discord.Embed(title='List of supported languages', description=lang, colour=ctx.guild.me.roles[::-1][0].color)
                await wait.edit(content='', embed=embed)
            elif len(args)>1:
                destination = args[0].lower()
                try:
                    toTrans = ' '.join(args[1:])
                    if len(destination) > 2:
                        q = self.client.utils.query(
                            [LANGUAGES[i] for i in list(LANGUAGES)], destination
                        )
                        assert q is not None
                        destination = q
                except (IndexError, AssertionError):
                    raise self.client.utils.send_error_message('Gimme something to translate!')
                try:
                    translation = self.translator.translate(toTrans, dest=destination)
                    embed = discord.Embed(description=translation.text, colour=ctx.guild.me.roles[::-1][0].color)
                    embed.set_footer(text=f'Translated {LANGUAGES[translation.src]} to {LANGUAGES[translation.dest]}.')
                    await wait.edit(content='', embed=embed)
                except Exception as e:
                    raise self.client.utils.send_error_message(f'An error occurred! ```py\n{str(e)}```')
            else:
                await wait.edit(content=f'Please add a language! To have the list and their id, type\n`{self.client.command_prefix}translate --list`.')
        else:
            await wait.edit(content=f'Please add translations or\nType `{self.client.command_prefix}translate --list` for supported languages.')
    
    @command()
    @cooldown(5)
    async def wikipedia(self, ctx, *args):
        if len(args)==0:
            raise self.client.utils.send_error_message("Please input a page name.")
        wait = await ctx.send(self.client.loading_emoji + ' | Please wait...')
        wikipedia = wikipediaapi.Wikipedia('en')
        page = wikipedia.page(' '.join(args))
        if page.exists()==False:
            await wait.edit(content='That page does not exist!')
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
            embed = discord.Embed(title=pageTitle, url=str(page.fullurl), description=str(explain), colour=ctx.guild.me.roles[::-1][0].color)
            await wait.edit(content='', embed=embed)
    @command()
    @cooldown(5)
    async def imdb(self, ctx, *args):
        wait, args = await ctx.send(self.client.loading_emoji + ' | Please wait...'), list(args)
        if len(args)==0 or self.client.utils.parse_parameter(args, 'help')['available']:
            embed = discord.Embed(title='IMDb command help', description='Searches through the IMDb Movie database.\n{} are Parameters that is **REQUIRED** to get the info.\n\n', colour=ctx.guild.me.roles[::-1][0].color)
            embed.add_field(name='Commands', value=self.client.command_prefix+'imdb --top {NUMBER}\n'+self.client.command_prefix+'imdb help\n'+self.client.command_prefix+'imdb --movie {MOVIE_ID or MOVIE_NAME}', inline='False')
            return await wait.edit(content='', embed=embed)
        top = self.client.utils.parse_parameter(args, '--top', get_second_element=True, singular=True)
        if top['available']:
            try:
                num = int(top['secondparam'])
                if num>30 or num<2: num = 20
                arr = ia.get_top250_movies()
                total = '\n'.join([str(int(i)+1) + '. '+str(arr[i]['title'])+' (`'+str(arr[i].movieID)+'`)' for i in range(num)])
                embed = discord.Embed(title='IMDb Top '+str(num)+':', description=str(total), colour=ctx.guild.me.roles[::-1][0].color)
                return await wait.edit(content='', embed=embed)
            except:
                raise self.client.utils.send_error_message('Is the top thing you inputted REALLY a number?\nlike, Not top TEN, but top 10.\nGET IT?')
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
                embed = discord.Embed(title=data['title'], colour=ctx.guild.me.roles[::-1][0].color)
                await wait.edit(content=self.client.loading_emoji + ' | Please wait... Retrieving data... this may take a while depending on how big the movie is.')
                emoteStar = ' '.join([':star:' for i in range(0, round(rating))]) if rating != None else '???'
                upload_date = ia.get_movie_release_info(str(theID))['data']['raw release dates'][0]['date']
                imdb_url = ia.get_imdbURL(data)
                embed.add_field(name='General Information', value=f'[IMDb URL here]({imdb_url})\n**Upload date: **{upload_date}\n**Written by: **'+main_data['data']['writer'][0]['name']+'\n**Directed by: **'+main_data['data']['director'][0]['name'])
                embed.add_field(name='Ratings', value=emoteStar+'\n**Overall rating: **'+str(rating)+'\n**Rated by '+str(vote_count)+' people**')
                if cover != None: embed.set_image(url=cover)
                return await wait.edit(content='', embed=embed)
            except Exception as e:
                print(e)
                raise self.client.utils.send_error_message('Oopsies! please input a valid ID/parameter...')
        raise self.client.utils.send_error_message('Wrong syntax. Use `'+self.client.command_prefix+'imdb help` next time.')

def setup(client):
    client.add_cog(apps(client))