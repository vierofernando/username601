import discord
from discord.ext import commands
from decorators import *
import random
from io import BytesIO
from datetime import datetime as t
import asyncio

class games(commands.Cog):
    def __init__(self):
        pass

    @command(['ttt'])
    @cooldown(15)
    @require_args()
    async def tictactoe(self, ctx, *args):
        user = ctx.bot.Parser.parse_user(ctx, args)
        if user == ctx.author:
            raise ctx.bot.util.BasicCommandException("You need to add a `mention/user ID/username` for someone to join your game as well.")
        elif user.bot: 
            raise ctx.bot.util.BasicCommandException("Sorry! There was an error on executing the tictactoe:\n`discord.DiscordAPIError: "+str(user)+" is a botum`")

        wait_for = ctx.bot.WaitForMessage(ctx, timeout=20.0, check=(lambda x: x.author == ctx.author and x.channel == ctx.channel and (x.content.lower() in ['yes', 'no'])))
        response = await wait_for.get_message()

        if response is None:
            raise ctx.bot.util.BasicCommandException(user.display_name+" did not respond in 20 seconds! Game invitation ended.")
        elif response.content.lower() == "no":
            raise ctx.bot.util.BasicCommandException(f"Well, {user.display_name} denied your request! Try requesting someone else?")

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
                await ctx.send(embed=discord.Embed(color=discord.Color.red(), title=str(characters[current]) + " did not respond in 20 seconds! game ended."))
                break
            
            try:
                res = game.add_move(int(msg.content), bool(current))
                assert res is not None
            except:
                current = 1 if (current == 0) else 0
                continue
            
            check = game.check_if_win()
            if check is not None:
                if check == "?":
                    return await ctx.send(embed=discord.Embed(title="No one wins! It's a draw!", color=discord.Colour.orange()))
                winner = str(characters[0 if (current == 1) else 1])
                return await ctx.send(embed=discord.Embed(color=discord.Color.green(), title=str(characters[current]) + " won the game!"))
            
            current = 1 if (current == 0) else 0
            embed.description = "["+str(characters[current])+"'s ("+game.current_turn+") turn]```" + game.show() + "```"
            await embed.edit_to(message)
    
    async def get_name_history(self, uuid, ctx):
        data = await ctx.bot.util.get_request(
            f"https://api.mojang.com/user/profiles/{uuid}/names",
            json=True,
            raise_errors=True
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
        name = ctx.bot.util.encode_uri(ctx.author.display_name if len(args)==0 else ' '.join(args))
        data = await ctx.bot.util.default_client.get(f"https://mc-heads.net/minecraft/profile/{name}")
        if data.status != 200:
            raise ctx.bot.util.BasicCommandException(f"Minecraft for profile: `{name}` not found.")
        data = await data.json()
        
        _buffer = await ctx.bot.canvas.minecraft_body(f"https://mc-heads.net/body/{name}/600", data['id'])
        body = discord.File(_buffer, "body.png")
        names = await self.get_name_history(data['id'], ctx)
        embed = ctx.bot.Embed(
            ctx,
            title=name,
            url='https://namemc.com/profile/'+data['id'],
            attachment=body,
            thumbnail=f"https://mc-heads.net/head/{name}/600",
            fields={
                'UUID': data['id'],
                'Name history': names
            }
        )
        await embed.send()
        del embed, body, names, _buffer, data
    
    @command(['imposter', 'among-us', 'among_us', 'impostor', 'crew', 'crewmate', 'crew-mate'])
    @cooldown(3)
    async def amongus(self, ctx, *args):
        await ctx.trigger_typing()
        url = await ctx.bot.Parser.parse_image(ctx, args)
        im = await ctx.bot.canvas.among_us(ctx, url)
        await ctx.send(file=discord.File(im, 'the_impostor.png'))
        del im, url

    async def geometry_dash_profile(self, ctx, args):
        try:
            data = await ctx.bot.util.get_request(
                "https://gdbrowser.com/api/profile/"+' '.join(args)[0:32],
                json=True,
                raise_errors=True
            )
            
            icons = await ctx.bot.canvas.geometry_dash_icons(data["username"])
            
            embed = ctx.bot.Embed(
                ctx,
                title=data["username"],
                fields={
                    "Account info": f"**Player ID: **{data['playerID']}\n**Account ID: **{data['accountID']}",
                    "Stats": f"**Rank: **{('`<not available>`' if data['rank'] == 0 else data['rank'])}\n**Stars: **{data['stars']}\n**Diamonds: **{data['diamonds']}\n**Secret Coins: **{data['coins']}\n**Demons: **{data['demons']}\n**Creator Points: **{data['cp']}",
                    "Links": f"{('[YouTube channel](https://youtube.com/channel/'+data['youtube']+')' if data['youtube'] else '`<YouTube not available>`')}\n{('[Twitter Profile](https://twitter.com/'+data['twitter']+')' if data['twitter'] else '`<Twitter not available>`')}\n{('[Twitch Channel](https://twitch.tv/'+data['twitch']+')' if data['twitch'] else '`<Twitch not available>`')}"
                },
                attachment=icons
            )
            await embed.send()
            del embed, icons
        except:
            raise ctx.bot.util.BasicCommandException('Error, user not found.')
    
    async def geometry_dash_comment(self, ctx, args):
        try:
            _split = ' '.join(args).split(' | ')
            text, num, user_name = ctx.bot.util.encode_uri(_split[0])[0:100], int(_split[2]), ctx.bot.util.encode_uri(_split[1])[0:32]
            if num not in range(-99999, 100000): num = 601
            return await ctx.bot.util.send_image_attachment(ctx, f'https://gdcolon.com/tools/gdcomment/img/{text}?name={user_name}&likes={num}&days=1-second{("&mod=mod" if ctx.author.guild_permissions.manage_guild else "")}')
        except Exception as e:
            raise ctx.bot.util.BasicCommandException(f'Invalid arguments!\nThe flow is this: {ctx.bot.command_prefix}gd comment <text> | <username> | <like count>')

    async def geometry_dash_level(self, ctx, args):
        _input = args[0].lower()
        if _input == "daily":
            try:
                daily = await ctx.bot.canvas.geometry_dash_level(None, daily=True)
                return await ctx.send(file=discord.File(daily, "level.png"))
            except:
                raise ctx.bot.util.BasicCommandException("The Geometry dash servers seems to be down. Please try again later.")
        elif _input == "weekly":
            try:
                weekly = await ctx.bot.canvas.geometry_dash_level(None, weekly=True)
                return await ctx.send(file=discord.File(weekly, "level.png"))
            except:
                raise ctx.bot.util.BasicCommandException("The Geometry dash servers seems to be down. Please try again later.")
        elif _input.isnumeric():
            try:
                level = await ctx.bot.canvas.geometry_dash_level(int(_input))
                return await ctx.send(file=discord.File(level, "level.png"))
            except:
                raise ctx.bot.util.BasicCommandException(f"Level with the ID: {_input} not found.")
        
        result = await ctx.bot.util.get_request(
            "https://gdbrowser.com/api/search/" + ctx.bot.util.encode_uri(" ".join(args)),
            json=True,
            raise_errors=True
        )

        embed = ctx.bot.ChooseEmbed(ctx, result, key=(lambda x: "**"+x['name']+"** by "+x['author']))
        result = await embed.run()

        if result is None:
            return
        
        await ctx.trigger_typing()
        try:
            buffer = await ctx.bot.canvas.geometry_dash_level(int(result['id']))
            return await ctx.send(file=discord.File(buffer, "level.png"))
        except:
            raise ctx.bot.util.BasicCommandException("The Geometry Dash servers may be down. Please blame RobTop for this :)")

    @command(['geometrydash', 'geometry-dash', 'gmd'])
    @cooldown(5)
    @require_args()
    async def gd(self, ctx, *args):
        await ctx.trigger_typing()
        try:
            _input = args[0].lower()
            if _input.startswith("level"):
                return await self.geometry_dash_level(ctx, args[1:])
            elif _input.startswith("profile") or _input.startswith("user"):
                return await self.geometry_dash_profile(ctx, args[1:])
            elif _input.startswith("logo"):
                return await ctx.bot.util.send_image_attachment(ctx, 'https://gdcolon.com/tools/gdlogo/img/'+ctx.bot.util.encode_uri(' '.join(args[1:])))
            elif _input.startswith("box"):
                return await ctx.bot.util.send_image_attachment(ctx, 'https://gdcolon.com/tools/gdtextbox/img/'+ctx.bot.util.encode_uri(' '.join(args[1:]))[0:100]+'?color='+('blue' if ctx.author.guild_permissions.manage_guild else 'brown')+'&name='+ctx.author.display_name+'&url='+str(ctx.author.avatar_url_as(format='png'))+'&resize=1')
            elif _input.startswith("comment"):
                return await self.geometry_dash_comment(ctx, args[1:])
            assert False
        except:
            raise ctx.bot.util.BasicCommandException(f"Invalid arguments. Try `{ctx.bot.command_prefix}help gd`")

    @command(['rockpaperscissors'])
    @cooldown(5)
    async def rps(self, ctx):
        game = ctx.bot.rps(ctx)
        res = await game.play()
        del game

        if res is None:
            return
        if res == 1 and ctx.bot.db.Economy.get(ctx.author.id) is not None:
            reward = random.randint(5, 100)
            ctx.bot.db.Economy.addbal(ctx.author.id, reward)
            return await ctx.send(f'Thanks for playing! you earned {reward} bobux as a prize!')

    @command(['dice', 'flipcoin', 'flipdice', 'coinflip', 'diceflip', 'rolldice'])
    @cooldown(3)
    async def coin(self, ctx, *args):
        if "coin" in ctx.bot.util.get_command_name(ctx):
            res = random.choice(['***heads!***', '***tails!***'])
            await ctx.send(res)
            if len(args)>0 and args[0].lower()==res.replace('*', '').replace('!', '') and ctx.bot.db.Economy.get(ctx.author.id) is not None:
                prize = random.randint(50, 200)
                ctx.bot.db.Economy.addbal(ctx.author.id, prize) ; await ctx.send('your bet was right! you get '+str(prize)+' bobux.')
        else:
            arr = ['one', 'two', 'three', 'four', 'five', 'six']
            res = arr[random.randint(0, 5)]
            await ctx.send(':'+res+':')
            if len(args)>0 and (args[0].lower()==res.lower() or args[0].lower() == str(arr.index(res)+1)) and ctx.bot.db.Economy.get(ctx.author.id) is not None:
                prize = random.randint(50, 150)
                ctx.bot.db.Economy.addbal(ctx.author.id, prize) ; await ctx.send('your bet was right! you get '+str(prize)+' bobux.')

    @command(['guessav', 'avatarguess', 'avguess', 'avatargame', 'avgame'])
    @cooldown(15)
    async def guessavatar(self, ctx):
        try:
            game = ctx.bot.GuessAvatar(ctx)
        except Exception as e:
            raise ctx.bot.util.BasicCommandException(str(e))
        win = await game.start()
        
        if win and ctx.bot.db.Economy.get(ctx.author.id) is not None:
            reward = random.randint(5, 100)
            ctx.bot.db.Economy.addbal(ctx.author.id, reward)
            await ctx.send(f'Thanks for playing! You received {reward} extra bobux!')
        
    @command()
    @cooldown(15)
    async def geoquiz(self, ctx):
        await ctx.trigger_typing()

        quizClient = ctx.bot.GeoQuiz(session=ctx.bot.util.default_client)
        win = await quizClient.play(ctx)

        if win is None:
            return

        await quizClient.end()
        del quizClient

        if win and (ctx.bot.db.Economy.get(ctx.author.id) is not None):
            reward = random.randint(5, 150)
            ctx.bot.db.Economy.addbal(ctx.author.id, reward)
            await ctx.send(f'Thanks for playing! You obtained {reward} bobux in total!')
        
    @command()
    @cooldown(4)
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
            if ctx.bot.db.Economy.get(ctx.author.id) is not None:
                reward = random.randint(5, 50)
                ctx.bot.db.Economy.addbal(ctx.author.id, reward)
                return await ctx.send(f'Thanks for playing! we added an extra {reward} bobux to your profile.')
        return await message.edit(embed=discord.Embed(title=f"Wrong. The answer is {quiz.answer}", color=discord.Color.red()))

    @command()
    @cooldown(60)
    async def hangman(self, ctx):
        await ctx.trigger_typing()
        
        game = ctx.bot.Hangman()
        await game.initiate()
        result = await game.play(ctx)
        del game
        
        if not result:
            return
            
        if ctx.bot.db.Economy.get(ctx.author.id) is not None:
            reward = random.randint(150, 300)
            ctx.bot.db.Economy.addbal(ctx.author.id, reward)
            await ctx.send(f'Thanks for playing! You get also a {reward} bobux as a prize!')

    @command()
    @cooldown(2)
    async def slot(self, ctx):
        slot = ctx.bot.slot()
        reward = await slot.play(ctx)
        del slot
        
        if reward == 0:
            return
        
        if ctx.bot.db.Economy.get(ctx.author.id) is not None:
            ctx.bot.db.Economy.addbal(ctx.author.id, reward)
            await ctx.send(f'Thanks for playing! You get also a {reward} bobux as a prize!')

    @command(['gn', 'guessnumber'])
    @cooldown(30)
    async def guessnum(self, ctx):
        game = ctx.bot.GuessMyNumber()
        result = await game.play(ctx)
        del game
        
        if result and ctx.bot.db.Economy.get(ctx.author.id) is not None:
            reward = random.randint(150, 300)
            ctx.bot.db.Economy.addbal(ctx.author.id, reward)
            await ctx.send(f'Thanks for playing! You get also a {reward} bobux as a prize!')

    @command()
    @cooldown(30)
    async def trivia(self, ctx, *args):
        await ctx.trigger_typing()
        try:
            trivia = ctx.bot.Trivia(" ".join(args)[0:50] if len(args)>0 else "Apple", session=ctx.bot.util.default_client)
        except Exception as e:
            raise ctx.bot.util.BasicCommandException(str(e))
        correct = await trivia.start(ctx)
        del trivia
        
        if correct and ctx.bot.db.Economy.get(ctx.author.id) is not None:
            reward = random.randint(250, 400)
            ctx.bot.db.Economy.addbal(ctx.author.id, reward)
            await ctx.send(f'Thanks for playing! You get also a {reward} bobux as a prize!')

def setup(client):
    client.add_cog(games())