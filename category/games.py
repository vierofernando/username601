import discord
from discord.ext import commands
import sys
from requests import get
from os import getcwd, name, environ
sys.path.append(environ['BOT_MODULES_DIR'])
from decorators import command, cooldown
import random
from datetime import datetime as t
import discordgames as Games
import asyncio

class games(commands.Cog):
    def __init__(self, client):
        self.client = client
    
    def get_name_history(self, uuid):
        data = self.client.utils.fetchJSON("https://api.mojang.com/user/profiles/"+uuid+"/names")
        res = ["**Latest: **`"+data[0]["name"]+"`"]
        if len(data) < 2: return res[0]
        count = 0
        for i in data[1:]:
            if count > 20: break
            res.append("**["+str(t.fromtimestamp(i["changedToAt"] / 1000))+"]: **`"+i["name"]+"`")
            count += 1
        return "\n".join(res)
    
    @command('mc')
    @cooldown(5)
    async def minecraft(self, ctx, *args):
        msg = await ctx.send(f"{self.client.loading_emoji} | Fetching data from the minecraft servers...")
        name = self.client.utils.encode_uri("Notch" if len(args)==0 else ' '.join(args))
        data = get(f"https://mc-heads.net/minecraft/profile/{name}")
        if data.status_code != 200: return await msg.edit(content=f"Minecraft for profile: `{name}` not found.")
        data = data.json()
        body, head = discord.File(self.client.canvas.minecraft_body(f"https://mc-heads.net/body/{name}/600", data['id']), "body.png"), discord.File(self.client.canvas.urltoimage(f"https://mc-heads.net/head/{name}/600"), "head.png")
        accent_color = self.client.canvas.get_accent(f"https://mc-heads.net/head/{name}/600")
        names = self.get_name_history(data['id'])
        embed = discord.Embed(title=name, url='https://namemc.com/profile/'+data['id'], description="UUID: `"+data['id']+"`", color=discord.Color.from_rgb(*accent_color))
        embed.set_image(url="attachment://body.png")
        embed.set_thumbnail(url="attachment://head.png")
        embed.add_field(name="Name history", value=names)
        await msg.delete()
        return await ctx.send(embed=embed, files=[body, head])
    
    @command('imposter,among-us,among_us,impostor,crew,crewmate,crew-mate')
    @cooldown(3)
    async def amongus(self, ctx, *args):
        async with ctx.channel.typing():
            url = self.client.utils.getUserAvatar(ctx, args)
            im = self.client.canvas.among_us(url)
            await ctx.send(file=discord.File(im, 'the_impostor.png'))
    
    @command()
    @cooldown(3)
    async def gdlevel(self, ctx, *args):
        if len(args)==0: raise self.client.utils.send_error_message('Please enter a level ID!')
        if not args[0].isnumeric(): raise self.client.utils.send_error_message('That is not a level ID!')
        toEdit = await ctx.send(self.client.loading_emoji+' | Fetching data from the Geometry Dash servers...')
        try:
            data = self.client.canvas.geometry_dash_level(int(list(args)[0]))
            await toEdit.delete()
            await ctx.send(file=discord.File(data, 'gdlevel.png'))
        except:
            raise self.client.utils.send_error_message('Sorry! there is an error with the GD servers.')
    @command()
    @cooldown(3)
    async def gdsearch(self, ctx, *args):
        if len(args)==0:
            raise self.client.utils.send_error_message('Please input a query!')
        else:
            try:
                query = self.client.utils.encode_uri(' '.join(args))
                data = self.client.utils.fetchJSON('https://gdbrowser.com/api/search/'+str(query))
                levels, count = '', 0
                for i in range(0, len(data)):
                    if data[count]['disliked']: like = ':-1:'
                    else: like = ':+1:'
                    levels += str(count+1)+'. **'+data[count]['name']+'** by '+data[count]['author']+' (`'+data[count]['id']+'`)\n:arrow_down: '+data[count]['downloads']+' | '+like+' '+data[count]['likes']+'\n'
                    count += 1
                embedy = discord.Embed(title='Geometry Dash Level searches for "'+str(' '.join(args))+'":', description=levels, colour=ctx.guild.me.roles[::-1][0].color)
                await ctx.send(embed=embedy)
            except:
                raise self.client.utils.send_error_message('Error: Not Found. :four::zero::four:')

    @command()
    @cooldown(3)
    async def gdprofile(self, ctx, *args):
        if len(args)==0: raise self.client.utils.send_error_message('Gimme some ARGS!')
        else:
            try:
                url = self.client.utils.encode_uri(str(' '.join(args)))
                data = self.client.utils.fetchJSON("https://gdbrowser.com/api/profile/"+url)
                embed = discord.Embed(
                    title = data["username"],
                    description = 'Displays user data for '+data["username"]+'.',
                    colour = discord.Colour.orange()
                )
                if data["rank"]=="0": rank = "Not yet defined :("
                else: rank = str(data["rank"])
                if data["cp"]=="0": cp = "This user don't have Creator Points :("
                else: cp = data["cp"]
                embed.add_field(name='ID Stuff', value='Player ID: '+str(data["playerID"])+'\nAccount ID: '+str(data["accountID"]), inline='True')
                embed.add_field(name='Rank', value=rank, inline='True')
                embed.add_field(name='Stats', value=str(data["stars"])+" Stars"+"\n"+str(data["bobux"])+" bobux\n"+str(data["coins"])+" Secret Coins\n"+str(data["userCoins"])+" User Coins\n"+str(data["demons"])+" Demons beaten", inline='False')
                embed.add_field(name='Creator Points', value=cp)
                embed.set_author(name='Display User Information', icon_url="https://gdbrowser.com/icon/"+url)
                await ctx.send(embed=embed)
            except:
                raise self.client.utils.send_error_message('Error, user not found.')
    
    @command()
    @cooldown(3)
    async def gdlogo(self, ctx, *args):
        if len(args)==0:
            raise self.client.utils.send_error_message('Please input a text!')
        else:
            async with ctx.channel.typing():
                text = self.client.utils.encode_uri(' '.join(args))
                url='https://gdcolon.com/tools/gdlogo/img/'+str(text)
                await ctx.send(file=discord.File(self.client.canvas.urltoimage(url), 'gdlogo.png'))
    
    @command()
    @cooldown(3)
    async def gdbox(self, ctx, *args):
        if len(args)==0: raise self.client.utils.send_error_message('Please input a text!')
        else:
            async with ctx.channel.typing():
                text, av = self.client.utils.encode_uri(str(' '.join(args))), ctx.author.avatar_url_as(format='png')
                if len(text)>100: raise self.client.utils.send_error_message('the text is too long!')
                else:
                    if not ctx.author.guild_permissions.manage_guild: color = 'brown'
                    else: color = 'blue'
                    url='https://gdcolon.com/tools/gdtextbox/img/'+str(text)+'?color='+color+'&name='+ctx.author.name+'&url='+str(av)+'&resize=1'
                    await ctx.send(file=discord.File(self.client.canvas.urltoimage(url), 'gdbox.png'))
   
    @command()
    @cooldown(3)
    async def gdcomment(self, ctx, *args):
        async with ctx.channel.typing():
            try:
                byI = str(' '.join(args)).split(' | ')
                text = self.client.utils.encode_uri(byI[0])
                num = int(byI[2])
                if num>9999: num = 601
                elif num<-9999: num = -601
                gdprof = self.client.utils.encode_uri(byI[1])
                if ctx.author.guild_permissions.manage_guild: url='https://gdcolon.com/tools/gdcomment/img/'+str(text)+'?name='+str(gdprof)+'&likes='+str(num)+'&mod=mod&days=1-second'
                else: url='https://gdcolon.com/tools/gdcomment/img/'+str(text)+'?name='+str(gdprof)+'&likes='+str(num)+'&days=1-second'
                await ctx.send(file=discord.File(self.client.canvas.urltoimage(url), 'gdcomment.png'))
            except Exception as e:
                raise self.client.utils.send_error_message(f'Invalid!\nThe flow is this: `{self.client.command_prefix}gdcomment text | name | like count`\nExample: `{self.client.command_prefix}gdcomment I am cool | RobTop | 601`.\n\nFor developers: ```{e}```')

    @command('gdweekly')
    @cooldown(2)
    async def gddaily(self, ctx):
        toEdit = await ctx.send(self.client.loading_emoji+' | Fetching data from the Geometry Dash servers...')
        try:
            data = self.client.canvas.geometry_dash_level(None, daily=True) if 'daily' in ctx.message.content.lower() else self.client.canvas.geometry_dash_level(None, weekly=True)
            await toEdit.delete()
            await ctx.send(file=discord.File(data, 'gdnivel.png'))
        except:
            await toEdit.edit(content=self.client.error_emoji+ ' | Sorry! Geometry dash servers seems to doing... something wrong.')

    @command('rockpaperscissors')
    @cooldown(5)
    async def rps(self, ctx):
        main = await ctx.send(embed=discord.Embed(title='Rock Paper Scissors game.', description='Click the reaction below. And game will begin.', colour=ctx.guild.me.roles[::-1][0].color))
        exp = ['✊', '🖐️', '✌']
        for i in range(0, len(exp)):
            await main.add_reaction(exp[i])
        def check(reaction, user):
            return user == ctx.author
        try:
            reaction, user = await self.client.wait_for('reaction_add', timeout=15.0, check=check)
        except asyncio.TimeoutError:
            await main.add_reaction('😔')
        emojiArray, ran, given, beginGame = None, None, None, False
        if str(reaction.emoji) in exp:
            emotes, num, beginGame = ["fist", "hand_splayed", "v"], exp.index(str(reaction.emoji)), True
            res = self.client.games.rps(emotes[num])
            given, msgId = emotes[num], res[0]
            emojiArray, ran = emotes, res[1]
        messages = ["Congratulations! "+ctx.author.name+" WINS!", "It's a draw.", "Oops, "+ctx.author.name+" lost!"]
        colors = [ctx.guild.me.roles[::-1][0].color, discord.Colour.orange(), ctx.guild.me.roles[::-1][0].color]
        if beginGame:
            embed = discord.Embed(
                title = messages[msgId],
                colour = colors[msgId]
            )
            embed.set_footer(text='Playin\' rock paper scissors w/ '+ctx.author.name)
            embed.set_author(name="Playing Rock Paper Scissors with "+ctx.author.name)
            embed.add_field(name=ctx.author.name, value=':'+given+':', inline="True")
            embed.add_field(name='Username601', value=':'+str(emojiArray[ran])+':', inline="True")
            await main.edit(embed=embed)
            if msgId==1 and self.client.db.Economy.get(ctx.author.id)!=None:
                reward = random.randint(5, 100)
                self.client.db.Economy.addbal(ctx.author.id, reward)
                await ctx.send('thank you for playing! you earned '+str(reward)+' as a prize!')

    @command('dice,flipcoin,flipdice,coinflip,diceflip,rolldice')
    @cooldown(3)
    async def coin(self, ctx, *args):
        if 'coin' in ctx.message.content:
            res = random.choice(['***heads!***', '***tails!***'])
            await ctx.send(res)
            if len(args)>0 and args[0].lower()==res.replace('*', '').replace('!', '') and self.client.db.Economy.get(ctx.author.id)!=None:
                prize = random.randint(50, 200)
                self.client.db.Economy.addbal(ctx.author.id, prize) ; await ctx.send('your bet was right! you get '+str(prize)+' bobux.')
        else:
            arr = ['one', 'two', 'three', 'four', 'five', 'six']
            res = arr[random.randint(0, 5)]
            await ctx.send(':'+res+':')
            if len(args)>0 and (args[0].lower()==res.lower() or args[0].lower() == str(arr.index(res)+1)) and self.client.db.Economy.get(ctx.author.id)!=None:
                prize = random.randint(50, 150)
                self.client.db.Economy.addbal(ctx.author.id, prize) ; await ctx.send('your bet was right! you get '+str(prize)+' bobux.')

    @command('guessav,avatarguess,avguess,avatargame,avgame')
    @cooldown(30)
    async def guessavatar(self, ctx):
        wait = await ctx.send(self.client.loading_emoji + ' | Please wait... generating question...\nThis process may take longer if your server has more members.')
        avatarAll, nameAll = [str(i.avatar_url) for i in ctx.guild.members if i.status.name!='offline'], [i.display_name for i in ctx.guild.members if i.status.name!='offline']
        if len(avatarAll)<=4: raise self.client.utils.send_error_message('Need more online members! :x:')
        numCorrect = random.randint(0, len(avatarAll)-1)
        corr_avatar, corr_name = avatarAll[numCorrect], nameAll[numCorrect]
        nameAll.remove(corr_name)
        wrongArr = []
        for i in range(0, 3):
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
            reaction, user = await self.client.wait_for('reaction_add', check=is_correct, timeout=20.0)
        except asyncio.TimeoutError:
            return await ctx.send(':pensive: No one? Okay then, the answer is: '+str(corr_order)+'. '+str(corr_name))
        if str(reaction.emoji)==str(corr_order):
            await ctx.send(self.client.success_emoji +' | <@'+str(ctx.author.id)+'>, You are correct! :tada:')
            if self.client.db.Economy.get(ctx.author.id)!=None:
                reward = random.randint(5, 100)
                self.client.db.Economy.addbal(ctx.author.id, reward)
                await ctx.send('thanks for playing! You received '+str(reward)+' extra bobux!')
        else:
            raise self.client.utils.send_error_message(f'<@{ctx.author.id}>, Incorrect. The answer is {corr_order}. {corr_name}')

    @command()
    @cooldown(15)
    async def geoquiz(self, ctx):
        wait = await ctx.send(self.client.loading_emoji + ' | Please wait... generating question...')
        data, topic = self.client.utils.fetchJSON("https://restcountries.eu/rest/v2/"), random.choice(['capital', 'region', 'subregion', 'population', 'demonym', 'nativeName'])
        chosen_nation_num = random.randint(0, len(data))
        chosen_nation, wrongs = data[chosen_nation_num], []
        del data[chosen_nation_num]
        correct = str(chosen_nation[topic])
        for i in range(0, 4):
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
        for i in range(0, len(static_emot)):
            await wait.add_reaction(static_emot[i])
        def check(reaction, user):
            return user == guy
        try:
            reaction, user = await self.client.wait_for('reaction_add', timeout=20.0, check=check)
        except asyncio.TimeoutError:
            await main.add_reaction('😔')
        if str(reaction.emoji)==str(corr_order):
            await ctx.send(self.client.success_emoji +' | <@'+str(guy.id)+'>, Congrats! You are correct. :partying_face:')
            if self.client.db.Economy.get(ctx.author.id)!=None:
                reward = random.randint(5, 150)
                self.client.db.Economy.addbal(ctx.author.id, reward)
                await ctx.send('thanks for playing! You obtained '+str(reward)+' bobux in total!')
        else:
            raise self.client.utils.send_error_message(f'<@{guy.id}>, You are incorrect. The answer is {corr_order}.')

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
            trying = await self.client.wait_for('message', check=is_correct, timeout=15.0)
        except asyncio.TimeoutError:
            return await ctx.send(f':pensive: | No one? Okay then, the answer is: {answer}.')
        if str(trying.content)==str(answer):
            await ctx.send(self.client.success_emoji +' | <@'+str(ctx.author.id)+'>, You are correct! :tada:')
            if self.client.db.Economy.get(ctx.author.id)!=None:
                reward = random.randint(5, 50)
                self.client.db.Economy.addbal(ctx.author.id, reward)
                await ctx.send('thanks for playing! we added an extra '+str(reward)+' bobux to your profile.')
        else:
            raise self.client.utils.send_error_message(f'<@{ctx.author.id}>, Incorrect. The answer is {answer}.')

    @command()
    @cooldown(60)
    async def hangman(self, ctx):
        wait = await ctx.send(self.client.loading_emoji + ' | Please wait... generating...')
        the_word = self.client.utils.fetchJSON("https://random-word-api.herokuapp.com/word?number=1")
        main_guess_cor, main_guess_hid = list(the_word[0]), []
        server_id, wrong_guesses = ctx.guild.id, ''
        for i in range(0, len(main_guess_cor)):
            main_guess_hid.append('\_ ')
        guessed, gameplay, playing_with, playing_with_id, level = [], True, ctx.author, int(ctx.author.id), 0
        while gameplay:
            if ctx.message.content==self.client.command_prefix+'hangman' and ctx.author.id!=int(playing_with_id) and ctx.guild.id==server_id:
                await ctx.send('<@'+str(ctx.author.id)+'>, cannot play hangman when a game is currently playing!')
            newembed = discord.Embed(title=''.join(main_guess_hid), description='Wrong guesses: '+str(wrong_guesses), colour=ctx.guild.me.roles[::-1][0].color)
            newembed.set_image(url=f'https://raw.githubusercontent.com/vierofernando/username601/master/assets/pics/hangman_{str(level)}.png')
            newembed.set_footer(text='Type "showanswer" to show the answer and end the game.')
            await ctx.send(embed=newembed)
            if '\_ ' not in ''.join(main_guess_hid):
                await ctx.send(f'Congratulations! <@{str(playing_with_id)}> win! :tada:\nThe answer is "'+str(''.join(main_guess_cor))+'".')
                if self.client.db.Economy.get(ctx.author.id)!=None:
                    reward = random.randint(5, 500)
                    self.client.db.Economy.addbal(ctx.author.id, reward)
                    await ctx.send('thanks for playing! you get an extra '+str(reward)+' bobux!')
                gameplay = False ; break
            if level>7:
                raise self.client.utils.send_error_message(f'<@{playing_with_id}> lost! :(\nThe answer is actually "'+''.join(main_guess_cor)+'".')
                gameplay = False ; break
            def is_not_stranger(m):
                return m.author == playing_with
            try:
                trying = await self.client.wait_for('message', check=is_not_stranger, timeout=20.0)
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
                for i in range(0, len(main_guess_cor)):
                    if main_guess_cor[i].lower()==str(trying.content).lower():
                        main_guess_hid[i] = str(trying.content).lower()
            else:
                level = int(level) + 1
                wrong_guesses = wrong_guesses + str(trying.content).lower() + ', '

    @command()
    @cooldown(2)
    async def slot(self, ctx):
        win, jackpot, slots = False, False, []
        for i in range(0, 3):
            newslot = self.client.games.slot()
            if newslot[1]==newslot[2] and newslot[1]==newslot[3] and newslot[2]==newslot[3]:
                win = True
                if newslot[1]==':flushed:':
                    jackpot = True
            slots.append(self.client.games.slotify(newslot))
        if win:
            msgslot = 'You win!'
            col = ctx.guild.me.roles[::-1][0].color
            if jackpot:
                msgslot = 'JACKPOT!'
                col = ctx.guild.me.roles[::-1][0].color
            if self.client.db.Economy.get(ctx.author.id)!=None:
                reward = random.randint(500, 1000)
                self.client.db.Economy.addbal(ctx.author.id, reward)
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
                trying = await self.client.wait_for('message', check=check_not_stranger, timeout=20.0)
            except asyncio.TimeoutError:
                raise self.client.utils.send_error_message('You did not respond for the next 20 seconds!\nGame ended.')
                gameplay = False
                break
            if trying.content.isnumeric()==False:
                raise self.client.utils.send_error_message('That is not a number!')
                attempts = int(attempts) - 1
            else:
                if int(trying.content)<num:
                    await ctx.send('Higher!')
                    attempts = int(attempts) - 1
                if int(trying.content)>num:
                    await ctx.send('Lower!')
                    attempts = int(attempts) - 1
                if int(trying.content)==num:
                    await ctx.send(self.client.success_emoji +' | You are correct!\n**The answer is '+str(num)+'!**')
                    if self.client.db.Economy.get(ctx.author.id)!=None:
                        reward = random.randint(5, 50)
                        self.client.db.Economy.addbal(ctx.author.id, reward)
                        await ctx.send('thanks for playing! You get an extra '+str(reward)+' bobux!')
                    break

    @command()
    @cooldown(30)
    async def trivia(self, ctx):
        al = None
        try:
            wait = await ctx.send(self.client.loading_emoji + ' | Please wait... generating quiz... This may take a while')
            auth = ctx.author
            data = self.client.utils.fetchJSON('https://wiki-quiz.herokuapp.com/v1/quiz?topics=Science')
            q = random.choice(data['quiz'])
            choices = ''
            for i in range(0, len(q['options'])):
                al = list('🇦🇧🇨🇩')
                if q['answer']==q['options'][i]:
                    corr = al[i]
                choices = choices + al[i] +' '+ q['options'][i]+'\n'
            embed = discord.Embed(title='Trivia!', description='**'+q['question']+'**\n'+choices, colour=ctx.guild.me.roles[::-1][0].color)
            embed.set_footer(text='Answer by clicking the reaction! You have 60 seconds.')
            await wait.edit(content='', embed=embed)
            for i in range(0, len(al)):
                await wait.add_reaction(al[i])
        except Exception as e:
            raise self.client.utils.send_error_message(f'An error occurred!\nReport this using {self.client.command_prefix}feedback.\n```{str(e)}```')
        guy = ctx.author
        def check(reaction, user):
            return user == guy
        try:
            reaction, user = await self.client.wait_for('reaction_add', timeout=60.0, check=check)
        except asyncio.TimeoutError:
            await wait.add_reaction('😔')
        if str(reaction.emoji)==str(corr):
            await ctx.send(self.client.success_emoji +' | <@'+str(guy.id)+'>, Congrats! You are correct. :partying_face:')
            if self.client.db.Economy.get(ctx.author.id)!=None:
                reward = random.randint(250, 400)
                self.client.db.Economy.addbal(ctx.author.id, reward)
                await ctx.send('thanks for playing! You get also a '+str(reward)+' bobux as a prize!')
        else:
            raise self.client.utils.send_error_message(f'<@{guy.id}>, You are incorrect. The answer is {corr}.')

def setup(client):
    client.add_cog(games(client))