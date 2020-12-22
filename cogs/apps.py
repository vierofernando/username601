import discord
from discord.ext import commands
import imdb
from decorators import *
import random
import wikipediaapi
from googletrans import Translator, LANGUAGES

class apps(commands.Cog):
    def __init__(self):
        self.translator = Translator(service_urls=['translate.googleapis.com'])
        self.Wikipedia = wikipediaapi.Wikipedia('en')
        self.ia = imdb.IMDb()

    @command(['urban-dictionary', 'define'])
    @cooldown(8)
    @require_args()
    async def urban(self, ctx, *args):
        search = False
        parser = ctx.bot.Parser(args)
        parser.parse()
        
        try:
            if parser.has("search"):
                parser.shift("search")
                args, search = tuple(parser.other), True
            
            data = await ctx.bot.util.get_request(
                "https://api.urbandictionary.com/v0/define",
                term=' '.join(args)[0:100],
                json=True,
                raise_errors=True
            )
            
            if search:
                embed_list = ctx.bot.ChooseEmbed(ctx, data["list"][0:10], key=(lambda x: f'{x["word"]} by {x["author"]} [{x["thumbs_up"]:,} :+1:, {x["thumbs_down"]:,} :-1:]'))
                result = await embed_list.run()
                del embed_list
                if not result:
                    return
            else:
                result = data["list"][0]
            
            embed = ctx.bot.Embed(
                ctx,
                title=result["word"],
                fields={
                    "Post Info": f"**Author: **{result['author']}" + "\n" + f"{result['thumbs_up']:,} :+1: | {result['thumbs_down']:,} :-1:",
                    "Definition": result["definition"].replace("\\\\", "\\"),
                    "Written in": result['written_on'].replace("T", " ")[:-5],
                    "Example": result["example"]
                },
                url=result['permalink']
            )
            
            await embed.send()
            del embed, result, search, data
            
        except:
            raise ctx.bot.util.BasicCommandException("Did not found anything corresponding to your search.")

    @command(['git'])
    @cooldown(10)
    @require_args(2)
    async def github(self, ctx, *args):
        try:
            nl = "\n" 
            if (args[0].lower() in ["user", "users", "profile"]):
                data = await ctx.bot.util.get_request(
                    "https://api.github.com/users/" + " ".join(args[1:]),
                    github=True,
                    json=True,
                    raise_errors=True
                )
                embed = ctx.bot.Embed(
                    ctx,
                    title=data["login"],
                    fields={
                        "General": f"**ID: **`{data['id']}`{nl}**Created at: **{data['created_at'].replace('T', ' ')[:-1]}{nl}**Updated at: **{data['updated_at'].replace('T', ' ')[:-1]}",
                        "Bio": data["bio"] if data.get("bio") else "`<no bio>`",
                        "Stats": f"**Followers: **{data['followers']}{nl}**Following: **{data['following']}{nl}**Public Repositories: **{data['public_repos']}{nl}**Public Gists: **{data['public_gists']}"
                    },
                    thumbnail=data["avatar_url"],
                    url=data["html_url"]
                )
                await embed.send()
                del embed, data, nl
                return
            elif (args[0].lower() in ["repos", "repositories"]):
                data = await ctx.bot.util.get_request(
                    "https://api.github.com/users/" + " ".join(args[1:]) + "/repos",
                    github=True,
                    json=True,
                    raise_errors=True
                )
                
                desc = ""
                for repo in data:
                    if len(desc) >= 1900:
                        break
                    
                    desc += f"{'[ '+repo['language']+' ]' if repo['language'] else '[ ??? ]'} [{repo['full_name']}]({repo['html_url']}){' :fork_and_knife:' if repo['fork'] else ''}{nl}"
                
                embed = ctx.bot.Embed(ctx, title=' '.join(args[1:]) + f"'s repositories [{len(data):,}]", desc=desc, thumbnail=data[0]["owner"]["avatar_url"])
                
                await embed.send()
                del embed, desc, data, nl
                return
            elif (args[0].lower() in ["repo", "repository"]):
                assert " ".join(args[1:]).count("/")
                data = await ctx.bot.util.get_request(
                    "https://api.github.com/repos/" + " ".join(args[1:]),
                    github=True,
                    json=True,
                    raise_errors=True
                )
                
                embed = ctx.bot.Embed(
                    ctx,
                    title=data["full_name"] + (' [Fork of '+data['parent']['full_name']+']' if data['fork'] else ''),
                    url=data["html_url"],
                    fields={
                        'General': f"**Created at: **{data['created_at'].replace('T', ' ')[:-1]}{nl}**Updated at: **{data['updated_at'].replace('T', ' ')[:-1]}{nl}**Pushed at: **{data['pushed_at'].replace('T', ' ')[:-1]}{nl}**Programming Language: **{data['language'] if data.get('language') else '???'}{nl + '**License: **' + data['license']['name'] if data.get('license') else ''}",
                        'Description': data['description'] if data.get('description') else 'This repo is without description.', # haha nice reference there null
                        'Stats': f"**Stars: **{data['stargazers_count']}{nl}**Forks: **{data['forks_count']}{nl}**Watchers: **{data['watchers_count']}{nl}**Open Issues: **{data['open_issues_count']}"
                    },
                    thumbnail=data["owner"]["avatar_url"]
                )
                await embed.send()
                
                del embed, data, nl
                return
            assert False
        except:
            return await ctx.bot.cmds.invalid_args(ctx)

    @command()
    @cooldown(5)
    @require_args()
    async def tv(self, ctx, *args):
        data = await ctx.bot.util.get_request(
            f'http://api.tvmaze.com/singlesearch/shows',
            json=True,
            q=' '.join(args)
        )
        if not data:
            raise ctx.bot.util.BasicCommandException("Did not found anything corresponding to your query.")
        
        try:
            star = str(':star:'*round(data['rating']['average'])) if data['rating']['average'] else 'No star rating provided.'
            embed = ctx.bot.Embed(
                ctx,
                title=data['name'],
                url=data['url'],
                desc=ctx.bot.Parser.html_to_markdown(data['summary']),
                fields={
                    'General Information': '**Status: **'+data['status']+'\n**Premiered at: **'+data['premiered']+'\n**Type: **'+data['type']+'\n**Language: **'+data['language']+'\n**Rating: **'+str(data['rating']['average'] if data['rating']['average'] else '`<not available>`')+'\n'+star,
                    'TV Network': data['network']['name']+' at '+data['network']['country']['name']+' ('+data['network']['country']['timezone']+')',
                    'Genre': str(', '.join(data['genres']) if len(data['genres'])>0 else 'no genre avaliable'),
                    'Schedule': ', '.join(data['schedule']['days'])+' at '+data['schedule']['time']
                },
                image=data['image']['original']
            )
            await embed.send()
            del embed
        except:
            raise ctx.bot.util.BasicCommandException("There was an error on fetching the info.")

    @command(['spy', 'spot', 'splay', 'listeningto', 'sp'])
    @cooldown(2)
    async def spotify(self, ctx, *args):
        user = ctx.bot.Parser.parse_user(ctx, args)
        act = [i for i in user.activities if isinstance(i, discord.Spotify)]
        if not act: raise ctx.bot.util.BasicCommandException(f"Sorry, but {user.display_name} is not listening to spotify.")
        await ctx.trigger_typing()
        panel = ctx.bot.Panel(ctx, spotify=act[0])
        await panel.draw()
        await panel.send_as_attachment()
        panel.close()

    @command()
    @cooldown(5)
    @require_args()
    async def itunes(self, ctx, *args):
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

    @command(['tr', 'trans'])
    @cooldown(5)
    @require_args(2)
    async def translate(self, ctx, *args):
        await ctx.trigger_typing()
        try:
            toTrans = ' '.join(args[1:])
            if len(args[0]) > 2:
                try:
                    _filter = list(filter(
                        lambda x: args[0].lower() in x.lower(), [LANGUAGES[x] for x in list(LANGUAGES)]
                    ))
                    assert _filter
                    del _filter
                    destination = _filter[0]
                except:
                    return await ctx.bot.cmds.invalid_args(ctx)
            else:
                destination = args[0].lower()
            translation = self.translator.translate(toTrans[0:1000], dest=destination)
            embed = ctx.bot.Embed(ctx, title=f"{LANGUAGES[translation.src]} to {LANGUAGES[translation.dest]}", desc=translation.text[0:1900])
            await embed.send()
            del embed, translation, destination, toTrans
        except:
            return await ctx.bot.cmds.invalid_args(ctx)

    @command(['wiki'])
    @cooldown(5)
    @require_args()
    async def wikipedia(self, ctx, *args):
        await ctx.trigger_typing()
        
        page = self.Wikipedia.page(' '.join(args))
        if not page.exists():
            return await ctx.send(content='That page does not exist!')
        
        embed = ctx.bot.Embed(ctx, title=page.title, url=page.fullurl, desc=page.summary[0:2000])
        return await embed.send()
    
    @command(['movie', 'film'])
    @cooldown(5)
    @require_args()
    async def imdb(self, ctx, *args):
        await ctx.trigger_typing()
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
            raise ctx.bot.util.BasicCommandException("The movie query does not exist.\n" + str(e))
        
def setup(client):
    client.add_cog(apps())