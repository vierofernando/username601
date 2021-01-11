import discord
from discord.ext import commands
from decorators import *
from random import randint, choice
from io import BytesIO
from gc import collect
from json import loads
from time import time

class games(commands.Cog):
    def __init__(self, client):
        self.db = client.db
        self._get_guess_context = (lambda c: {
            ("avatar", "avatar", "pfp"): ("GuessAvatar", (c,), "start", ()),
            ("geo", "geography"): ("GeoQuiz", (c.bot.http._HTTPClient__session,), "play", (c,)),
            ("num", "number"): ("GuessMyNumber", (), "play", (c,)),
            ("flag", "country-flag", "flags"): ("GuessTheFlag", (c,), "start", ())
        })
        
        self.words = tuple(loads(open("./assets/json/words.json", "r").read()))

    @command()
    @cooldown(8, channel_wide=True)
    async def fast(self, ctx, *args):
        await ctx.trigger_typing()
        parser = ctx.bot.Parser(args)
        parser.parse()
        data = choice(self.words)
        
        if parser.has_multiple("reverse", "reversed"):
            answer, message = choice([data, data[::-1]]), "Send the reversed version of the text below!"
            buffer = ctx.bot.Image.text(answer[::-1])
        elif parser.has_multiple("index", "alphabet", "alpha"):
            answer, buffer = choice(list(data)), ctx.bot.Image.text(data)
            index = data.index(answer)
            message = f"Find the {index + 1}{(['st', 'nd', 'rd', 'th'][index] if index < 4 else 'th')} alphabet in this word!"
            del index
        elif parser.has_multiple("bot", "captcha"):
            answer, message, buffer = data, "Are you a bot? Solve the captcha below!", ctx.bot.Image.captcha(data)
        else:
            answer, message, buffer = data, "Send the text displayed here!", ctx.bot.Image.text(data)
        
        a = time()
        await ctx.send(message, file=discord.File(buffer, "fast.png"))
        wait = ctx.bot.WaitForMessage(ctx, timeout=20.0, check=(lambda x: x.channel == ctx.channel and (not x.author.bot) and (x.content.lower() == answer)))
        _message = await wait.get_message()
        if not _message:
            raise ctx.bot.util.error_message(f"No one sent an answer! The answer is actually {answer}.")
        
        _time = time() - a
        embed = ctx.bot.Embed(ctx, title=f"Congratulations! {_message.author.display_name} got it first!", fields={"Time taken": str(_time) + " seconds", "Answer": answer}, footer="Try again later if you lost lol")
        
        if self.db.exist("economy", {"userid": _message.author.id}):
            reward = round((20 - _time) * 100)
            embed.description = f"**You also get {reward:,} bobux as a reward!**"
            self.db.modify("economy", self.db.types.INCREMENT, {"userid": _message.author.id}, {"bal": reward})
            del reward
        await embed.send()
        del message, wait, a, buffer, data, answer, embed, parser

    @command(['ttt'])
    @cooldown(15, server_wide=True)
    @require_args()
    async def tictactoe(self, ctx, *args):
        user = ctx.bot.Parser.parse_user(ctx, args)
        if user == ctx.author:
            raise ctx.bot.util.error_message("You need to add a `mention/user ID/username` for someone to join your game as well.")
        elif user.bot: 
            raise ctx.bot.util.error_message("Sorry! There was an error on executing the tictactoe:\n`discord.DiscordAPIError: "+str(user)+" is a botum`")

        wait_for = ctx.bot.WaitForMessage(ctx, timeout=20.0, check=(lambda x: x.author == ctx.author and x.channel == ctx.channel and (x.content.lower() in ['yes', 'no'])))
        response = await wait_for.get_message()

        if not response:
            raise ctx.bot.util.error_message(user.display_name+" did not respond in 20 seconds! Game invitation ended.")
        elif response.content.lower() == "no":
            raise ctx.bot.util.error_message(f"Well, {user.display_name} denied your request! Try requesting someone else?")

        characters = (ctx.author, user)
        game = ctx.bot.TicTacToe()
        
        embed = ctx.bot.Embed(ctx, title="Tic-tac-toe Game", desc="["+str(ctx.author)+"'s (O) turn]```"+game.show()+"```")
        message = await embed.send()
        current = 0
        
        while True:
            try:
                msg = await ctx.bot.wait_for("message", check=(
                    lambda x: (x.author == characters[current]) and (x.channel == ctx.channel) and x.content.isnumeric() and (len(x.content) == 1)
                ), timeout=20.0)
            except:
                raise ctx.bot.util.error_message(str(characters[current]) + " did not respond in 20 seconds! game ended.")
            
            try:
                res = game.add_move(int(msg.content), bool(current))
                assert res
            except:
                current = 0 if current else 1
                continue
            
            check = game.check_if_win()
            if check:
                if check == "?":
                    return await ctx.send(embed=discord.Embed(title="No one wins! It's a draw!", color=discord.Color.orange()))
                winner = str(characters[0 if (current == 1) else 1])
                return await ctx.success_embed(str(characters[current]) + " won the game!")
            
            current = 0 if current else 1
            embed.description = "["+str(characters[current])+"'s ("+game.current_turn+") turn]```" + game.show() + "```"
            await embed.edit_to(message)
    
    async def get_name_history(self, uuid, ctx):
        data = await ctx.bot.util.request(
            f"https://api.mojang.com/user/profiles/{uuid}/names",
            json=True
        )
        res = ["**Latest: **`"+data[0]["name"]+"`"]
        if len(data) < 2: return res[0]
        count = 0
        for i in data[1:]:
            if count > 20: break
            res.append("**["+str(t.fromtimestamp(i["changedToAt"] / 1000))+"]: **`"+i["name"]+"`")
            count += 1
        del count, data
        return "\n".join(res)
    
    @command(['mc', 'skin'])
    @cooldown(5)
    async def minecraft(self, ctx, *args):
        await ctx.trigger_typing()
        name = ctx.bot.util.encode_uri(' '.join(args) if args else ctx.author.display_name)
        data = await ctx.bot.http._HTTPClient__session.get(f"https://mc-heads.net/minecraft/profile/{name}")
        if data.status != 200:
            raise ctx.bot.util.error_message(f"Minecraft for profile: `{name}` not found.")
        data = await data.json()
        
        _buffer = await ctx.bot.canvas.minecraft_body(f"https://mc-heads.net/body/{name}/600", data['id'])
        names = await self.get_name_history(data['id'], ctx)
        embed = ctx.bot.Embed(
            ctx,
            title=name,
            url='https://namemc.com/profile/'+data['id'],
            attachment=_buffer,
            thumbnail=f"https://mc-heads.net/head/{name}/600",
            fields={
                'UUID': data['id'],
                'Name history': names
            }
        )
        await embed.send()
        del embed, names, _buffer, data
    
    @command(['imposter', 'among-us', 'among_us', 'impostor', 'crew', 'crewmate', 'crew-mate'])
    @cooldown(3)
    async def amongus(self, ctx, *args):
        await ctx.trigger_typing()
        url = await ctx.bot.Parser.parse_image(ctx, args)
        im = await ctx.bot.Image.among_us(url)
        await ctx.send(file=discord.File(im, 'the_impostor.png'))
        del im, url

    async def geometry_dash_profile(self, ctx, args):
        try:
            data = await ctx.bot.util.request(
                "https://gdbrowser.com/api/profile/"+' '.join(args)[:32],
                json=True
            )
            
            embed = ctx.bot.Embed(
                ctx,
                title=data["username"],
                fields={
                    "Account info": f"**Player ID: **{data['playerID']}\n**Account ID: **{data['accountID']}",
                    "Stats": f"**Rank: **{(data['rank'] if data['rank'] else '`<not available>`')}\n**Stars: **{data['stars']}\n**Diamonds: **{data['diamonds']}\n**Secret Coins: **{data['coins']}\n**Demons: **{data['demons']}\n**Creator Points: **{data['cp']}",
                    "Links": f"{('[YouTube channel](https://youtube.com/channel/'+data['youtube']+')' if data['youtube'] else '`<YouTube not available>`')}\n{('[Twitter Profile](https://twitter.com/'+data['twitter']+')' if data['twitter'] else '`<Twitter not available>`')}\n{('[Twitch Channel](https://twitch.tv/'+data['twitch']+')' if data['twitch'] else '`<Twitch not available>`')}"
                },
                thumbnail=f"https://gdbrowser.com/icon/{'%20'.join(args)[:32]}?form=cube"
            )
            await embed.send()
            del embed
        except:
            raise ctx.bot.util.error_message('Error, user not found.')
    
    async def geometry_dash_comment(self, ctx, args):
        parser = ctx.bot.Parser(args)
        parser.parse()
        try:
            text = ctx.bot.util.encode_uri(" ".join(parser.other))
            _from = ctx.bot.util.encode_uri(parser["from"]) if parser["from"] else "knowncreator56"
            likes = int(parser["likes"]) if parser.has("likes") else 601
            if likes not in range(-99999, 100000):
                likes = 601
            
            percentage = int(parser['percentage']) if parser.has('percentage') else ""
            if percentage and (percentage not in range(0, 1000)):
                percentage = 69
            
            assert bool(text)
            return await ctx.send_image(f'https://gdcolon.com/tools/gdcomment/img/{text}?name={_from}&likes={likes}&days=1-second{("&mod=mod" if parser.has("mod") else ("&mod=elder" if parser.has("elder-mod") else ""))}{("&uhd" if parser.has("uhd") else "")}{(f"&%={percentage}" if percentage else "")}{("&deletable" if parser.has("delete") else "")}')
        except:
            return await ctx.bot.cmds.invalid_args(ctx)
    
    async def geometry_dash_level(self, ctx, args):
        _input = args[0].lower()
        if _input == "daily":
            try:
                assert False
                #levelBuilder = ctx.bot.GDLevel(ctx, level_query="daily", font_title=ctx.bot.util.fonts_dir + "/PUSAB__.otf", font_other=ctx.bot.util.fonts_dir + "/Aller.ttf")
                #daily = await levelBuilder.draw()
                #del levelBuilder
                #return await ctx.send(file=discord.File(daily, "level.png"))
            except:
                raise ctx.bot.util.error_message("This sub command is temporary closed because the section is API is temporarily blocked by RobTop.")
                #raise ctx.bot.util.error_message("The Geometry dash servers seems to be down. Please try again later.")
        elif _input == "weekly":
            try:
                assert False
                #levelBuilder = ctx.bot.GDLevel(ctx, level_query="weekly", font_title=ctx.bot.util.fonts_dir + "/PUSAB__.otf", font_other=ctx.bot.util.fonts_dir + "/Aller.ttf")
                #weekly = await levelBuilder.draw()
                #del levelBuilder
                #return await ctx.send(file=discord.File(weekly, "level.png"))
            except:
                raise ctx.bot.util.error_message("This sub command is temporary closed because the section is API is temporarily blocked by RobTop.")
                #raise ctx.bot.util.error_message("The Geometry dash servers seems to be down. Please try again later.")
        elif _input.isnumeric():
            try:
                levelBuilder = ctx.bot.GDLevel(ctx, level_query=_input, font_title=ctx.bot.util.fonts_dir + "/PUSAB__.otf", font_other=ctx.bot.util.fonts_dir + "/Aller.ttf")
                level = await levelBuilder.draw()
                del levelBuilder
                return await ctx.send(file=discord.File(level, "level.png"))
            except:
                raise ctx.bot.util.error_message(f"Level with the ID: {_input} not found.")
        
        result = await ctx.bot.util.request(
            "https://gdbrowser.com/api/search/" + ctx.bot.util.encode_uri(" ".join(args)),
            json=True
        )

        embed = ctx.bot.ChooseEmbed(ctx, result, key=(lambda x: "**"+x['name']+"** by "+x['author']))
        result = await embed.run()

        if not result:
            return
        
        await ctx.trigger_typing()
        try:
            levelBuilder = ctx.bot.GDLevel(ctx, level_query=result['id'], font_title=ctx.bot.util.fonts_dir + "/PUSAB__.otf", font_other=ctx.bot.util.fonts_dir + "/Aller.ttf")
            buffer = await levelBuilder.draw()
            del levelBuilder
            return await ctx.send(file=discord.File(buffer, "level.png"))
        except Exception as e:
            print(str(e))
            raise ctx.bot.util.error_message("The Geometry Dash servers may be down. Please blame RobTop for this :)")

    @command(['geometrydash', 'geometry-dash', 'gmd'])
    @cooldown(5)
    @require_args()
    async def gd(self, ctx, *args):
        await ctx.trigger_typing()
        _input = args[0].lower()
        if _input.startswith("level"):
            return await self.geometry_dash_level(ctx, args[1:])
        elif _input.startswith("profile") or _input.startswith("user"):
            return await self.geometry_dash_profile(ctx, args[1:])
        elif _input.startswith("logo"):
            return await ctx.send_image('https://gdcolon.com/tools/gdlogo/img/'+ctx.bot.util.encode_uri(' '.join(args[1:])))
        elif _input.startswith("box"):
            return await ctx.send_image('https://gdcolon.com/tools/gdtextbox/img/'+ctx.bot.util.encode_uri(' '.join(args[1:]))[:100]+'?color='+('blue' if ctx.author.guild_permissions.manage_guild else 'brown')+'&name='+ctx.author.display_name+'&url='+str(ctx.author.avatar_url_as(format='png'))+'&resize=1')
        elif _input.startswith("comment"):
            return await self.geometry_dash_comment(ctx, args[1:])
        elif _input.startswith("icon"):
            if not args[1:]:
                return await ctx.bot.cmds.invalid_args(ctx)
            buffer = await ctx.bot.Image.geometry_dash_icons(" ".join(args[1:]))
            await ctx.send(file=discord.File(buffer, "icon.png"))
            del buffer
            return
        return await ctx.bot.cmds.invalid_args(ctx)

    @command(['rockpaperscissors'])
    @cooldown(5, channel_wide=True)
    async def rps(self, ctx):
        game = ctx.bot.rps(ctx)
        res = await game.play()
        del game

        if not res:
            return
        
        if res == 1 and self.db.exist("economy", {"userid": ctx.author.id}):
            reward = randint(5, 100)
            await ctx.success_embed(f'Thanks for playing! you earned {reward:,} bobux as a prize!')
            self.db.modify("economy", self.db.types.INCREMENT, {"userid": ctx.author.id}, {"bal": reward})

    @command(['dice', 'flipcoin', 'flipdice', 'coinflip', 'diceflip', 'rolldice'])
    @cooldown(3)
    async def coin(self, ctx, *args):
        if "coin" in ctx.bot.util.get_command_name(ctx):
            res = choice(['***heads!***', '***tails!***'])
            await ctx.send(res)
            if args and args[0].lower() == res[3:-4] and self.db.exist("economy", {"userid": ctx.author.id}):
                prize = randint(50, 200)
                await ctx.success_embed(f'Your bet was right! you get {prize:,} bobux.')
                self.db.modify("economy", self.db.types.INCREMENT, {"userid": ctx.author.id}, {"bal": prize})
        else:
            arr = ['one', 'two', 'three', 'four', 'five', 'six']
            res = arr[randint(0, 5)]
            await ctx.send(':'+res+':')
            if args and (args[0].lower()==res.lower() or args[0].lower() == str(arr.index(res)+1)) and self.db.exist("economy", {"userid": ctx.author.id}):
                prize = randint(50, 150)
                await ctx.success_embed(f'Your bet was right! you get {prize:,} bobux.')
                self.db.modify("economy", self.db.types.INCREMENT, {"userid": ctx.author.id}, {"bal": prize})

    @command(['guessinggame', 'guessing-game'])
    @cooldown(10, channel_wide=True)
    async def guess(self, ctx, *args):
        try:
            assert bool(args)
            Context, game = self._get_guess_context(ctx), None
            for arg in Context.keys():
                if args[0].lower() not in arg: continue
                
                object_name, object_args, play_func, play_args = Context[arg]
                game = getattr(ctx.bot, object_name)(*object_args)
                win = await getattr(game, play_func)(*play_args)
                break
            
            assert bool(game)
            if (not win) or (not self.db.exist("economy", {"userid": ctx.author.id})):
                return
            reward = randint(100, 1000)
            await ctx.success_embed(f"Thanks for playing! You received {reward:,} bobux.")
            self.db.modify("economy", self.db.types.INCREMENT, {"userid": ctx.author.id}, {"bal": reward})
            del game, win, object_name, object_args, play_func, play_args, Context, reward
        except AssertionError:
            embed = ctx.bot.Embed(
                ctx,
                title="Guessing Game!",
                desc="`guess <avatar|av|pfp>` Guessing game about guessing random people's avatars in the server!\n`guess <geo|geography>` Guess the correct information of a country!\n`guess <num|number>` Starts a \"guess my number\" game!\n`guess <flag|flags|country-flag>` Guess the country from a flag!"
            )
            await embed.send()
            del embed
        except Exception as e:
            raise ctx.bot.util.error_message(str(e))

    @command()
    @cooldown(4, channel_wide=True)
    async def mathquiz(self, ctx):
        quiz = ctx.bot.MathQuiz()
        quiz.generate_question()
        
        embed = ctx.bot.Embed(ctx, title=quiz.question)
        message = await embed.send()
        del embed
        
        wait_for = ctx.bot.WaitForMessage(ctx, timeout=30.0, check=(lambda x: x.channel == ctx.channel and x.author == ctx.author and x.content.replace("-", "").isnumeric()))
        answer = await wait_for.get_message()
        del wait_for
        
        if not answer:
            del quiz
            return await message.edit(embed=discord.Embed(title="Quiz canceled.", color=discord.Color.red()))
        
        try:
            correct = (int(answer.content) == quiz.answer)
        except:
            correct = False
        
        if correct:
            await message.edit(embed=discord.Embed(title="Correct!", color=discord.Color.green()))
            if self.db.exist("economy", {"userid": ctx.author.id}):
                reward = randint(5, 50)
                await ctx.success_embed(f'Thanks for playing! we added an extra {reward:,} bobux to your profile.')
                self.db.modify("economy", self.db.types.INCREMENT, {"userid": ctx.author.id}, {"bal": reward})
        return await message.edit(embed=discord.Embed(title=f"Wrong. The answer is {quiz.answer}", color=discord.Color.red()))

    @command()
    @cooldown(60, server_wide=True)
    async def hangman(self, ctx):
        await ctx.trigger_typing()
        
        game = ctx.bot.Hangman(ctx, session=ctx.bot.http._HTTPClient__session)
        result = await game.play()
        del game
        
        if not result:
            return
            
        if self.db.exist("economy", {"userid": ctx.author.id}):
            reward = randint(150, 300)
            await ctx.success_embed(f'Thanks for playing! You get also a {reward:,} bobux as a prize!')
            self.db.modify("economy", self.db.types.INCREMENT, {"userid": ctx.author.id}, {"bal": reward})

    @command()
    @cooldown(2, channel_wide=True)
    async def slot(self, ctx):
        slot = ctx.bot.slot()
        reward = await slot.play(ctx)
        del slot
        
        if not reward:
            return
        
        if self.db.exist("economy", {"userid": ctx.author.id}):
            await ctx.success_embed(f'Thanks for playing! You get also a {reward:,} bobux as a prize!')
            self.db.modify("economy", self.db.types.INCREMENT, {"userid": ctx.author.id}, {"bal": reward})

    @command()
    @cooldown(30, server_wide=True)
    async def trivia(self, ctx, *args):
        await ctx.trigger_typing()
        try:
            trivia = ctx.bot.Trivia(" ".join(args)[:50] if args else "Apple", session=ctx.bot.http._HTTPClient__session)
        except Exception as e:
            raise ctx.bot.util.error_message(str(e))
        correct = await trivia.start(ctx)
        del trivia
        
        if correct and self.db.exist("economy", {"userid": ctx.author.id}):
            reward = randint(250, 400)
            await ctx.success_embed(f'Thanks for playing! You get also a {reward:,} bobux as a prize!')
            self.db.modify("economy", self.db.types.INCREMENT, {"userid": ctx.author.id}, {"bal": reward})

def setup(client):
    client.add_cog(games(client))
