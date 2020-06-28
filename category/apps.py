import discord
from discord.ext import commands
import imdb
ia = imdb.IMDb()
import sys
sys.path.append('/app/modules')
import username601 as myself
from username601 import *
import wikipediaapi
from googletrans import Translator, LANGUAGES
gtr = Translator()

class apps(commands.Cog):
    def __init__(self, client):
        self.client = client
    @commands.command(pass_context=True)
    @commands.cooldown(1, 10, commands.BucketType.user)
    async def translate(self, ctx, *args):
        wait = await ctx.send(str(self.client.get_emoji(BotEmotes.loading)) + ' | Please wait...')
        if len(args)>0:
            if args[0]=='--list':
                lang = ''
                for bahasa in LANGUAGES:
                    lang = lang+str(bahasa)+' ('+str(LANGUAGES[bahasa])+')\n'
                embed = discord.Embed(title='List of supported languages', description=str(lang), colour=discord.Colour.from_rgb(201, 160, 112))
                await wait.edit(content='', embed=embed)
            elif len(args)>1:
                destination = args[0]
                toTrans = ' '.join(args[1:len(list(args))])
                try:
                    trans = gtr.translate(toTrans, dest=args[1])
                    embed = discord.Embed(title=f'Translation', description=f'**{trans.text}**', colour=discord.Colour.from_rgb(201, 160, 112))
                    embed.set_footer(text=f'Translated {LANGUAGES[trans.src]} to {LANGUAGES[trans.dest]}')
                    await wait.edit(content='', embed=embed)
                except Exception as e:
                    await wait.edit(content=str(client.get_emoji(BotEmotes.error)) + f' | An error occured! ```py\n{e}```')
            else:
                await wait.edit(content=f'Please add a language! To have the list and their id, type\n`{prefix}translate --list`.')
        else:
            await wait.edit(content=f'Please add translations or\nType `{prefix}translate --list` for supported languages.')
    
    @commands.command(pass_context=True)
    @commands.cooldown(1, 10, commands.BucketType.user)
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
                embed = discord.Embed(title=pageTitle, description=str(explain), colour=discord.Colour.from_rgb(201, 160, 112))
                embed.set_footer(text='Get more info at '+str(page.fullurl))
                await wait.edit(content='', embed=embed)
    @commands.command(pass_context=True)
    @commands.cooldown(1, 10, commands.BucketType.user)
    async def imdb(self, ctx, *args):
        wait, args = await ctx.send(str(self.client.get_emoji(BotEmotes.loading)) + ' | Please wait...'), list(args)
        if len(args)==0 or args[0]=='help' or args[0]=='--help':
            embed = discord.Embed(title='IMDb command help', description='Searches through the IMDb Movie database.\n{} are Parameters that is **REQUIRED** to get the info.\n\n', colour=discord.Colour.from_rgb(201, 160, 112))
            embed.add_field(name='Commands', value=prefix+'imdb --top {NUMBER}\n'+prefix+'imdb --search {TYPE} {QUERY}\n'+prefix+'imdb help\n'+prefix+'imdb --movie {MOVIE_ID or MOVIE_NAME}', inline='False')
            embed.add_field(name='Help', value='*{TYPE} could be "movie", "person", or "company".\n{QUERY} is the movie/person/company name.\n{MOVIE_ID} can be got from the search. Example: `'+prefix+'imdb --search movie Inception`.', inline='False')
            await wait.edit(content='', embed=embed)
        if args[0]=='--top':
            if len(args)==2:
                await wait.edit(content='Please type the number!\nex: --top 5, --top 10, etc.')
            else:
                num = args[1]
                try:
                    if int(num)>30:
                        await wait.edit(content='That\'s too many movies to be listed!')
                    else:
                        arr = ia.get_top250_movies()
                        total = ''
                        for i in range(0, int(num)):
                            total = total + str(int(i)+1) + '. '+str(arr[i]['title'])+' (`'+str(arr[i].movieID)+'`)\n'
                        embed = discord.Embed(title='IMDb Top '+str(num)+':', description=str(total), colour=discord.Colour.from_rgb(201, 160, 112))
                        await wait.edit(content='', embed=embed)
                except ValueError:
                    await wait.edit(content=str(self.client.get_emoji(BotEmotes.error)) +' | Is the top thing you inputted REALLY a number?\nlike, Not top TEN, but top 10.\nGET IT?')
        if args[0]=='--movie':
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
                await wait.edit(content=str(self.client.get_emoji(BotEmotes.error)) + ' | An error occured!\n**Good news, we *may* fix it.**')
                errorQuick = discord.Embed(title=data['title'], colour=discord.Colour.from_rgb(201, 160, 112))
                errorQuick.add_field(name='General Information', value=f'**IMDb URL: **{imdb_url}\n**Upload date: **{upload_date}')

                errorQuick.add_field(name='Ratings', value=emoteStar+'\n**Overall rating: **'+str(ia.get_movie_main(str(theID))['data']['rating'])+'\n**Rated by '+str(ia.get_movie_main(str(theID))['data']['votes'])+' people**')
                errorQuick.set_footer(text='Information given is limited due to Errors and... stuff.')
                await wait.edit(content='', embed=errorQuick)
        if args[0]=='--search':
            query = str(ctx.message.content).split(' ')[2]
            lists = ''
            if args[1].startswith('movie') or args[1].startswith('film'):
                main_name = 'MOVIE'
                movies = ia.search_movie(query)
                for i in range(0, int(len(movies))):
                    if len(lists)>1950:
                        break
                    lists = lists + str(int(i)+1) +'. '+ str(movies[i]['title'])+ ' (`'+str(movies[i].movieID)+'`)\n'
            elif args[1].startswith('company'):
                main_name = 'COMPANY'
                companies = ia.search_company(query)
                for i in range(0, int(len(companies))):
                    if len(lists)>1950:
                        break
                    lists = lists + str(int(i)+1) + '. '+str(companies[i]['name']) + ' (`'+str(companies[i].companyID)+'`)\n'
            elif args[1].startswith('person'):
                main_name = 'PERSON'
                persons = ia.search_person(query)
                for i in range(0, int(len(persons))):
                    if len(lists)>1950:
                        break
                    lists = lists + str(int(i)+1) + '. '+str(persons[i]['name']) + ' (`'+str(persons[i].personID)+'`)\n'
            embed = discord.Embed(title=main_name.lower()+' search for "'+str(query)+'":', description=str(lists), colour=discord.Colour.from_rgb(201, 160, 112))
            if main_name=='MOVIE':
                embed.set_footer(text='Type '+prefix+'imdb --'+str(main_name.lower())+' {'+main_name+'_ID} to show each info.')
            await wait.edit(content='', embed=embed)

def setup(client):
    client.add_cog(apps(client))