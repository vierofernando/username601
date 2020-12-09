import discord
from discord.ext import commands
from category.decorators import command, cooldown
import random
from io import BytesIO
from datetime import datetime as t
import asyncio

class games(commands.Cog):
    def __init__(self):
        self.urltoimage = (lambda url: BytesIO(get(url).content))
        self.countries = None
    
    async def generate_countries(self, ctx):
        res = await ctx.bot.util.default_client.get("https://restcountries.eu/rest/v2")
        self.countries = await res.json()
        del res

    async def wait_for_user(self, ctx, user):
        check = (lambda x: (x.channel == ctx.channel) and (x.author == user) and (x.content.lower() in ["yes", "no"]))
        await ctx.send(str(user)+", "+str(ctx.author)+" Invited you to a tic-tac-toe game!\nType `yes` to accept, or `no` to decline.")
        try:
            response = await ctx.bot.wait_for("message", check=check, timeout=20.0)
        except:
            return None
        return ("yes" in response.content.lower())

    @command("ttt")
    @cooldown(15)
    async def tictactoe(self, ctx, *args):
        ctx.bot.Parser.require_args(ctx, args)
        
        user = ctx.bot.Parser.parse_user(ctx, *args)
        if user == ctx.author: raise ctx.bot.util.BasicCommandException("You need to add a `mention/user ID/username` for someone to join your game as well.")
        response = await self.wait_for_user(ctx, user)
        if response is None: raise ctx.bot.util.BasicCommandException(str(user)+" did not respond in 20 seconds! Game invitation ended.")
    
        characters = (ctx.author, user)
        game = ctx.bot.TicTacToe()
        
        if user.bot: 
            raise ctx.bot.util.BasicCommandException("Sorry! There was an error on executing the tictactoe:\n`discord.DiscordAPIError: "+str(user)+" is a botum`")
        
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
                    await ctx.send(embed=discord.Embed(title="No one wins! It's a draw!", color=discord.Colour.orange()))
                    break
                winner = str(characters[0 if (current == 1) else 1])
                await ctx.send(embed=discord.Embed(color=discord.Color.green(), title=str(characters[current]) + " won the game!"))
                break
            
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
        return "\n".join(res)
    
    @command('mc,skin')
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
    
    @command('imposter,among-us,among_us,impostor,crew,crewmate,crew-mate')
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
                "https://gdbrowser.com/api/profile/"+str(' '.join(args))[0:32],
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

    @command('geometrydash,geometry-dash,gmd')
    @cooldown(5)
    async def gd(self, ctx, *args):
        ctx.bot.Parser.require_args(ctx, args)

        await ctx.trigger_typing()
        _input = args[0].lower()
        if _input.startswith("level"):
            return await self.geometry_dash_level(ctx, args[1:])
        elif _input.startswith("profile") or _input.startswith("user"):
            return await self.geometry_dash_profile(ctx, args[1:])
        elif _input.startswith("logo"):
            return await ctx.bot.util.send_image_attachment(ctx, 'https://gdcolon.com/tools/gdlogo/img/'+ctx.bot.util.encode_uri(' '.join(args)))
        elif _input.startswith("box"):
            return await ctx.bot.util.send_image_attachment(ctx, 'https://gdcolon.com/tools/gdtextbox/img/'+ctx.bot.util.encode_uri(' '.join(args))[0:100]+'?color='+('blue' if ctx.author.guild_permissions.manage_guild else 'brown')+'&name='+ctx.author.display_name+'&url='+str(ctx.author.avatar_url_as(format='png'))+'&resize=1')
        elif _input.startswith("comment"):
            return await self.geometry_dash_comment(ctx, args[1:])

    @command('rockpaperscissors')
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

    @command('dice,flipcoin,flipdice,coinflip,diceflip,rolldice')
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

    @command('guessav,avatarguess,avguess,avatargame,avgame')
    @cooldown(30)
    async def guessavatar(self, ctx):
        wait = await ctx.send(ctx.bot.util.loading_emoji + ' | Please wait... generating question...\nThis process may take longer if your server has more members.')
        avatarAll, nameAll = [str(i.avatar_url) for i in ctx.guild.members if i.status.name!='offline'], [i.display_name for i in ctx.guild.members if i.status.name!='offline']
        if len(avatarAll)<=4: raise ctx.bot.util.BasicCommandException('Need more online members! :x:')
        numCorrect = random.randint(0, len(avatarAll)-1)
        corr_avatar, corr_name = avatarAll[numCorrect], nameAll[numCorrect]
        nameAll.remove(corr_name)
        wrongArr = []
        for i in range(3):
            wrongArr.append(random.choice(nameAll))
        abcs, emots = list('🇦🇧🇨🇩'), list('🇦🇧🇨🇩')
        randomInt = random.randint(0, 3)
        corr_order = random.choice(abcs[randomInt])
        abcs[randomInt] = '0'
        question, chooseCount = '', 0
        for assign in abcs:
            if assign!='0':
                question += '**'+ str(assign) + '.** '+str(wrongArr[chooseCount])+ '\n'
                chooseCount += 1
            else:
                question += '**'+ str(corr_order) + '.** '+str(corr_name)+ '\n'
        embed = discord.Embed(title='What does the avatar below belongs to?', description=':eyes: Click the reactions! **You have 20 seconds.**\n\n'+str(question), colour=ctx.guild.me.roles[::-1][0].color)
        embed.set_footer(text='For privacy reasons, the people displayed above are online users.')
        embed.set_image(url=corr_avatar)
        main = await ctx.send(embed=embed)
        for i in emots: await main.add_reaction(i)
        def is_correct(reaction, user):
            return user == ctx.author
        try:
            reaction, user = await ctx.bot.wait_for('reaction_add', check=is_correct, timeout=20.0)
        except asyncio.TimeoutError:
            return await ctx.send(':pensive: No one? Okay then, the answer is: '+str(corr_order)+'. '+str(corr_name))
        if str(reaction.emoji)==str(corr_order):
            await ctx.send(ctx.bot.util.success_emoji +' | <@'+str(ctx.author.id)+'>, You are correct! :tada:')
            if ctx.bot.db.Economy.get(ctx.author.id) is not None:
                reward = random.randint(5, 100)
                ctx.bot.db.Economy.addbal(ctx.author.id, reward)
                await ctx.send('thanks for playing! You received '+str(reward)+' extra bobux!')
        else:
            raise ctx.bot.util.BasicCommandException(f'<@{ctx.author.id}>, Incorrect. The answer is {corr_order}. {corr_name}')

    @command()
    @cooldown(15)
    async def geoquiz(self, ctx):
        if not self.countries:
            await self.generate_countries(ctx)
    
        wait = await ctx.send(ctx.bot.util.loading_emoji + ' | Please wait... generating question...')
        data, topic = self.countries, random.choice(['capital', 'region', 'subregion', 'population', 'demonym', 'nativeName'])
        chosen_nation_num = random.randint(0, len(data))
        chosen_nation, wrongs = data[chosen_nation_num], []
        del data[chosen_nation_num]
        correct = str(chosen_nation[topic])
        for i in range(4):
            integer = random.randint(0, len(data))
            wrongs.append(str(data[integer][str(topic)]))
            data.remove(data[integer])
        emot, static_emot, corr_order_num = list('🇦🇧🇨🇩'), list('🇦🇧🇨🇩'), random.randint(0, 3)
        corr_order = emot[corr_order_num]
        emot[corr_order_num], question, guy = '0', '', ctx.author
        for each_emote in emot:
            if each_emote!='0':
                added = random.choice(wrongs)
                question += each_emote + ' ' + added + '\n'
                wrongs.remove(added)
            else:
                question += corr_order + ' ' + correct + '\n'
        embed = discord.Embed(title='Geography: '+str(topic)+' quiz!', description=':nerd: Click on the reaction! **You have 20 seconds.**\n\nWhich '+str(topic)+' belongs to '+str(chosen_nation['name'])+'?\n'+str(question), colour=ctx.guild.me.roles[::-1][0].color)
        await wait.edit(content='', embed=embed)
        for i in range(len(static_emot)):
            await wait.add_reaction(static_emot[i])
        def check(reaction, user):
            return user == guy
        try:
            reaction, user = await ctx.bot.wait_for('reaction_add', timeout=20.0, check=check)
        except asyncio.TimeoutError:
            await main.add_reaction('😔')
        if str(reaction.emoji)==str(corr_order):
            await ctx.send(ctx.bot.util.success_emoji +' | <@'+str(guy.id)+'>, Congrats! You are correct. :partying_face:')
            if ctx.bot.db.Economy.get(ctx.author.id) is not None:
                reward = random.randint(5, 150)
                ctx.bot.db.Economy.addbal(ctx.author.id, reward)
                await ctx.send('thanks for playing! You obtained '+str(reward)+' bobux in total!')
        else:
            raise ctx.bot.util.BasicCommandException(f'<@{guy.id}>, You are incorrect. The answer is {corr_order}.')

    @command()
    @cooldown(4)
    async def mathquiz(self, ctx):
        arrayId, num1, num2, symArray = random.randint(0, 3), random.randint(1, 500), random.randint(1, 500), ['+', '-', 'x', '÷']
        ansArray = [num1+num2, num1-num2, num1*num2, num1/num2]
        sym = symArray[arrayId]
        await ctx.send('**MATH QUIZ (15 seconds, answer rounded)**\n'+str(num1)+' '+str(sym)+' '+str(num2)+' = ???')
        def is_correct(m):
            return m.author == ctx.author
        answer = round(ansArray[arrayId])
        try:
            trying = await ctx.bot.wait_for('message', check=is_correct, timeout=15.0)
        except asyncio.TimeoutError:
            return await ctx.send(f':pensive: | No one? Okay then, the answer is: {answer}.')
        if str(trying.content)==str(answer):
            await ctx.send(ctx.bot.util.success_emoji +' | <@'+str(ctx.author.id)+'>, You are correct! :tada:')
            if ctx.bot.db.Economy.get(ctx.author.id) is not None:
                reward = random.randint(5, 50)
                ctx.bot.db.Economy.addbal(ctx.author.id, reward)
                await ctx.send('thanks for playing! we added an extra '+str(reward)+' bobux to your profile.')
        else:
            raise ctx.bot.util.BasicCommandException(f'<@{ctx.author.id}>, Incorrect. The answer is {answer}.')

    @command()
    @cooldown(60)
    async def hangman(self, ctx):
        wait = await ctx.send(ctx.bot.util.loading_emoji + ' | Please wait... generating...')
        the_word = await ctx.bot.util.get_request("https://useless-api.vierofernando.repl.co/randomword", json=True, raise_errors=True)
        the_word = the_word["word"]
        main_guess_cor, main_guess_hid = list(the_word), []
        server_id, wrong_guesses = ctx.guild.id, ''
        for i in range(len(main_guess_cor)):
            main_guess_hid.append('\_ ')
        guessed, gameplay, playing_with, playing_with_id, level = [], True, ctx.author, ctx.author.id, 0
        while gameplay:
            if ctx.message.content == (ctx.bot.command_prefix + 'hangman') and ctx.author.id!=int(playing_with_id) and ctx.guild.id==server_id:
                await ctx.send('<@'+str(ctx.author.id)+'>, cannot play hangman when a game is currently playing!')
            newembed = discord.Embed(title=''.join(main_guess_hid), description='Wrong guesses: '+str(wrong_guesses), colour=ctx.guild.me.roles[::-1][0].color)
            newembed.set_image(url=f'https://raw.githubusercontent.com/vierofernando/username601/master/assets/pics/hangman_{str(level)}.png')
            newembed.set_footer(text='Type "showanswer" to show the answer and end the game.')
            await ctx.send(embed=newembed)
            if '\_ ' not in ''.join(main_guess_hid):
                await ctx.send(f'Congratulations! <@{str(playing_with_id)}> win! :tada:\nThe answer is "'+str(''.join(main_guess_cor))+'".')
                if ctx.bot.db.Economy.get(ctx.author.id) is not None:
                    reward = random.randint(5, 500)
                    ctx.bot.db.Economy.addbal(ctx.author.id, reward)
                    await ctx.send('thanks for playing! you get an extra '+str(reward)+' bobux!')
                gameplay = False ; break
            if level>7:
                raise ctx.bot.util.BasicCommandException(f'<@{playing_with_id}> lost! :(\nThe answer is actually "'+''.join(main_guess_cor)+'".')
                gameplay = False ; break
            def is_not_stranger(m):
                return m.author == playing_with
            try:
                trying = await ctx.bot.wait_for('message', check=is_not_stranger, timeout=20.0)
            except asyncio.TimeoutError:
                await ctx.send(f'<@{str(playing_with_id)}> did not response in 20 seconds so i ended the game. Keep un-AFK!\nOh and btw, the answer is '+str(''.join(main_guess_cor))+'. :smirk:')
                gameplay = False ; break
            if str(trying.content).lower()=='showanswer':
                await ctx.send('The answer is actually '+str(''.join(main_guess_cor)+'.'))
                gameplay = False ; break
            elif len(str(trying.content))>1:
                await ctx.send('One word at a time. Game ended!')
                gameplay = False ; break
            elif str(trying.content).lower() in guessed:
                await ctx.send(f'<@{str(playing_with_id)}>, You have guessed that letter!')
                level = int(level)+1
            elif str(trying.content).lower() in ''.join(main_guess_cor).lower():
                guessed.append(str(trying.content).lower())
                for i in range(len(main_guess_cor)):
                    if main_guess_cor[i].lower()==str(trying.content).lower():
                        main_guess_hid[i] = str(trying.content).lower()
            else:
                level = int(level) + 1
                wrong_guesses = wrong_guesses + str(trying.content).lower() + ', '

    @command()
    @cooldown(2)
    async def slot(self, ctx):
        win, jackpot, slots = False, False, []
        for i in range(3):
            newslot = ctx.bot.games.slot()
            if newslot[1]==newslot[2] and newslot[1]==newslot[3] and newslot[2]==newslot[3]:
                win = True
                if newslot[1]==':flushed:':
                    jackpot = True
            slots.append(ctx.bot.games.slotify(newslot))
        if win:
            msgslot = 'You win!'
            col = ctx.guild.me.roles[::-1][0].color
            if jackpot:
                msgslot = 'JACKPOT!'
                col = ctx.guild.me.roles[::-1][0].color
            if ctx.bot.db.Economy.get(ctx.author.id) is not None:
                reward = random.randint(500, 1000)
                ctx.bot.db.Economy.addbal(ctx.author.id, reward)
                await ctx.send('thanks for playing! you received a whopping '+str(reward)+' bobux!')
        else:
            msgslot = 'You lose... Try again!'
            col = ctx.guild.me.roles[::-1][0].color
        embed = discord.Embed(title=msgslot, description=slots[0]+'\n\n'+slots[1]+'\n\n'+slots[2], colour=col)
        await ctx.send(embed=embed)

    @command('gn,guessnumber')
    @cooldown(30)
    async def guessnum(self, ctx):
        num = random.randint(5, 100)
        username = ctx.author.display_name
        user_class = ctx.author
        embed = discord.Embed(title='Starting the game!', description='You have to guess a *secret* number between 5 and 100!\n\nYou have 8 attempts, and 20 second timer in each attempt!\n\n**G O O D  L U C K**', colour=ctx.guild.me.roles[::-1][0].color)
        await ctx.send(embed=embed)
        gameplay = True
        attempts = 8
        while gameplay:
            if attempts<1:
                await ctx.send('Time is up! The answer is **'+str(num)+'.**')
                gameplay = False
                break
            def check_not_stranger(m):
                return m.author == user_class
            try:
                trying = await ctx.bot.wait_for('message', check=check_not_stranger, timeout=20.0)
            except asyncio.TimeoutError:
                raise ctx.bot.util.BasicCommandException('You did not respond for the next 20 seconds!\nGame ended.')
                gameplay = False
                break
            if trying.content.isnumeric()==False:
                raise ctx.bot.util.BasicCommandException('That is not a number!')
                attempts = int(attempts) - 1
            else:
                if int(trying.content)<num:
                    await ctx.send('Higher!')
                    attempts = int(attempts) - 1
                if int(trying.content)>num:
                    await ctx.send('Lower!')
                    attempts = int(attempts) - 1
                if int(trying.content)==num:
                    await ctx.send(ctx.bot.util.success_emoji +' | You are correct!\n**The answer is '+str(num)+'!**')
                    if ctx.bot.db.Economy.get(ctx.author.id) is not None:
                        reward = random.randint(5, 50)
                        ctx.bot.db.Economy.addbal(ctx.author.id, reward)
                        await ctx.send('thanks for playing! You get an extra '+str(reward)+' bobux!')
                    break

    @command()
    @cooldown(30)
    async def trivia(self, ctx):
        al = None
        try:
            wait = await ctx.send(ctx.bot.util.loading_emoji + ' | Please wait... generating quiz... This may take a while')
            auth = ctx.author
            data = await ctx.bot.util.get_request('https://wiki-quiz.herokuapp.com/v1/quiz', json=True, raise_errors=True, topics='science')
            q = random.choice(data['quiz'])
            choices = ''
            for i in range(len(q['options'])):
                al = list('🇦🇧🇨🇩')
                if q['answer']==q['options'][i]:
                    corr = al[i]
                choices = choices + al[i] +' '+ q['options'][i]+'\n'
            embed = discord.Embed(title='Trivia!', description='**'+q['question']+'**\n'+choices, colour=ctx.guild.me.roles[::-1][0].color)
            embed.set_footer(text='Answer by clicking the reaction! You have 60 seconds.')
            await wait.edit(content='', embed=embed)
            for i in range(len(al)):
                await wait.add_reaction(al[i])
        except Exception as e:
            raise ctx.bot.util.BasicCommandException(f'An error occurred!\nReport this using {ctx.bot.command_prefix}feedback.\n```{str(e)}```')
        guy = ctx.author
        def check(reaction, user):
            return user == guy
        try:
            reaction, user = await ctx.bot.wait_for('reaction_add', timeout=60.0, check=check)
        except asyncio.TimeoutError:
            await wait.add_reaction('😔')
        if str(reaction.emoji)==str(corr):
            await ctx.send(ctx.bot.util.success_emoji +' | <@'+str(guy.id)+'>, Congrats! You are correct. :partying_face:')
            if ctx.bot.db.Economy.get(ctx.author.id) is not None:
                reward = random.randint(250, 400)
                ctx.bot.db.Economy.addbal(ctx.author.id, reward)
                await ctx.send('thanks for playing! You get also a '+str(reward)+' bobux as a prize!')
        else:
            raise ctx.bot.util.BasicCommandException(f'<@{guy.id}>, You are incorrect. The answer is {corr}.')

def setup(client):
    client.add_cog(games())