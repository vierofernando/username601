import discord
from discord.ext import commands
import imdb
from datetime import datetime as t
from category.decorators import command, cooldown
import random
import wikipediaapi
from googletrans import Translator, LANGUAGES

class apps(commands.Cog):
    def __init__(self):
        self.translator = Translator(service_urls=['translate.googleapis.com'])
        self.Wikipedia = wikipediaapi.Wikipedia('en')
        self.ia = imdb.IMDb()

    @command('movie')
    @cooldown(5)
    async def tv(self, ctx, *args):
        if len(args)==0: return await ctx.bot.util.send_error_message(ctx, "Please give TV shows as arguments.")
        data = await ctx.bot.util.get_request(
            f'http://api.tvmaze.com/singlesearch/shows',
            json=True,
            q=' '.join(args)
        )
        if data is None: return await ctx.bot.util.send_error_message(ctx, "Did not found anything.")
        try:
            star = str(':star:'*round(data['rating']['average'])) if data['rating']['average'] is not None else 'No star rating provided.'
            em = discord.Embed(title=data['name'], url=data['url'], description=ctx.bot.Parser.html_to_markdown(data['summary']), color=ctx.guild.me.roles[::-1][0].color)
            em.add_field(name='General Information', value='**Status: **'+data['status']+'\n**Premiered at: **'+data['premiered']+'\n**Type: **'+data['type']+'\n**Language: **'+data['language']+'\n**Rating: **'+str(data['rating']['average'] if data['rating']['average'] is not None else 'None')+'\n'+star)
            em.add_field(name='TV Network', value=data['network']['name']+' at '+data['network']['country']['name']+' ('+data['network']['country']['timezone']+')')
            em.add_field(name='Genre', value=str(', '.join(data['genres']) if len(data['genres'])>0 else 'no genre avaliable'))
            em.add_field(name='Schedule', value=', '.join(data['schedule']['days'])+' at '+data['schedule']['time'])
            em.set_image(url=data['image']['original'])
            await ctx.send(embed=em)
        except:
            return await ctx.bot.util.send_error_message(ctx, "There was an error on fetching the info.")

    @command('spy,spot,splay,listeningto,sp')
    @cooldown(2)
    async def spotify(self, ctx, *args):
        user = ctx.bot.Parser.parse_user(ctx, args)
        act = [i for i in user.activities if isinstance(i, discord.Spotify)]
        if len(act) == 0: return await ctx.bot.util.send_error_message(ctx, f"Sorry, but {user.display_name} is not listening to spotify.")
        await ctx.trigger_typing()
        panel = ctx.bot.Panel(ctx, spotify=act[0])
        await panel.draw()
        await panel.send_as_attachment()
        panel.close()

    @command()
    @cooldown(5)
    async def itunes(self, ctx, *args):
        if len(args)==0: return await ctx.bot.util.send_error_message(ctx, "Please send a search term.")
        await ctx.trigger_typing()
        data = await ctx.bot.util.get_request(
            'https://itunes.apple.com/search',
            json=True,
            raise_errors=True,
            force_json=True,
            term=' '.join(args),
            media='music',
            entity='song',
            limit=10,
            explicit='no'
        )
        if len(data['results'])==0: return await ctx.send('{} | No music found... oop'.format(ctx.bot.util.error_emoji))
        choose = ctx.bot.ChooseEmbed(ctx, data['results'], key=(lambda x: "["+x["trackName"]+"]("+x["trackViewUrl"]+")"))
        data = await choose.run()
        if not data: return
        
        panel = ctx.bot.Panel(ctx, title=data['trackName'], subtitle=data['artistName'], description=data['primaryGenreName'], icon=data['artworkUrl100'])
        await panel.draw()
        await panel.send_as_attachment()
        panel.close()

    @command('tr,trans')
    @cooldown(5)
    async def translate(self, ctx, *args):
        await ctx.trigger_typing()
        if len(args)>1:
            destination = args[0].lower()
            try:
                toTrans = ' '.join(args[1:])
                if len(destination) > 2:
                    q = list(filter(
                        lambda x: destination in x.lower(), [LANGUAGES[x] for x in list(LANGUAGES)]
                    ))
                    assert len(q) > 0
                    destination = q[0]
            except (IndexError, AssertionError):
                return await ctx.bot.util.send_error_message(ctx, 'Please insert a valid language.')
            try:
                translation = self.translator.translate(toTrans[0:1000], dest=destination)
                embed = ctx.bot.Embed(ctx, title=f"{LANGUAGES[translation.src]} to {LANGUAGES[translation.dest]}", desc=translation.text[0:1900])
                return await embed.send()
            except Exception as e:
                return await ctx.bot.util.send_error_message(ctx, f'An error occurred! ```py\n{str(e)}```')
        return await ctx.bot.util.send_error_message(ctx, f'Please add a language and a text!')

    @command()
    @cooldown(5)
    async def wikipedia(self, ctx, *args):
        if len(args) == 0:
            return await ctx.bot.util.send_error_message(ctx, "Please input a page name.")
        await ctx.trigger_typing()
        
        page = self.Wikipedia.page(' '.join(args))
        if not page.exists():
            return await ctx.send(content='That page does not exist!')
        
        embed = ctx.bot.Embed(ctx, title=page.title, url=page.fullurl, desc=page.summary[0:2000])
        return await embed.send()
    
    @command()
    @cooldown(5)
    async def imdb(self, ctx, *args):
        await ctx.trigger_typing()
        if len(args) < 2 or args[0] == "help":
            return await ctx.bot.util.send_error_message(ctx, "Please input a movie name.")
        
        try:
            query = " ".join(args[1:])
            res = self.ia.search_movie(query)
            
            choose = ctx.bot.ChooseEmbed(ctx, res[0:10], key=(lambda x: x["long imdb title"]))
            movie = await choose.run()
            
            if not movie:
                return
            await ctx.trigger_typing()
            
            data = self.ia.get_movie_main(movie.movieID)["data"]
            votes = (":star:" * round(data["rating"])) + f' ({data["rating"]}, {data["votes"]} votes)' if (data.get("votes") and data.get("rating")) else "<data not available>"

            embed = ctx.bot.Embed(
                ctx,
                title=movie["long imdb title"],
                url=self.ia.get_imdbURL(movie),
                image=movie["full-size cover url"],
                fields={
                    "Plot": data["plot outline"].split(".")[0][0:1000],
                    "Movie Ratings": votes,
                    "Directors": ", ".join([i["name"] for i in data["directors"] if i.get("name")]),
                    "Producers": ", ".join([i["name"] for i in data["producers"] if i.get("name")]),
                    "Writers": ", ".join([i["name"] for i in data["writers"] if i.get("name")])
                }
            )
            await embed.send()
            del res, data, embed, votes, choose, movie, query
        except Exception as e:
            return await ctx.bot.util.send_error_message(ctx, "The movie query does not exist.\n" + str(e))
        
def setup(client):
    client.add_cog(apps())