import username601 as myself
from username601 import *
import os
import discordgames
import splashes
import inspect
import dbl

print('Please wait...')
import pokebase as pb
import youtube_dl
import datetime
latest_update = datetime.datetime.now()
from os import environ as fetchdata
import discord
from discord.ext import commands
import wikipediaapi
import random
import sys
import imdb
import asyncio
import math
from json import decoder
from googletrans import Translator, LANGUAGES
gtr = Translator()
client = commands.Bot(command_prefix='1')
ia = imdb.IMDb()
topgg = dbl.DBLClient(client, fetchdata['DBL_TOKEN'])

@client.event
async def on_ready():
    print('Bot is online.')
    while True:
        await asyncio.sleep(1800)
        myAct = discord.Activity(name=str(len(client.users))+' strangers in '+str(len(client.guilds))+' cults.', type=discord.ActivityType.watching)
        await client.change_presence(activity=myAct)
        try:
            await topgg.post_guild_count()
        except Exception as e:
            print(e)

# ONLY IN SUPPORT SERVER
@client.event
async def on_member_join(member):
    if member.guild.id==688373853889495044:
        await member.guild.get_channel(694521383908016188).send(':heart: | '+splashes.welcome('<@'+str(member.id)+'>', client.get_user(661200758510977084).name))

# ONLY IN SUPPORT SERVER ALSO
@client.event
async def on_member_remove(member):
    if member.guild.id==688373853889495044:
        await member.guild.get_channel(694521383908016188).send(':broken_heart: | '+splashes.exit(member.name))

@client.command(pass_context=True, name='hell')
async def hell(ctx):
    await ctx.send("HELLLLLLLLLLLLLLLLLLLLLLL")

@client.event
async def on_message(message):
    checkprefix, no_args = False, False
    if message.author.bot==False and '<@!696973408000409626>' in message.content or '<@696973408000409626>' in message.content:
        await message.channel.send('The prefix is `'+prefix+'`.\n**Commands: **`'+prefix+'help`')
        checkprefix = True
    if message.author.bot==False:
        if message.content==prefix+"ping":
            wait = await message.channel.send('Pinging... :thinking:')
            ping = str(round(client.latency*1000))
            if int(ping)<100:
                embed = discord.Embed(title=f'Pong! {ping} ms.', colour=discord.Colour.red())
            else:
                embed = discord.Embed(title=f'Pong! {ping} ms.', description='Ping time may be slower due to;\n1. People kept spamming me\n2. My hosting system is slow\n3. I am in too many servers\n4. Discord\'s servers are currectly down\n5. I am snail :snail:', colour=discord.Colour.red())
            embed.set_thumbnail(url='https://i.pinimg.com/originals/21/02/a1/2102a19ea556e1d1c54f40a3eda0d775.gif')
            embed.set_footer(text='Ping and embed sent time may differ.')
            await wait.edit(content='', embed=embed)
    sayTag = splashes.getTag()
    msg = message.content.lower()
    args = message.content.split(' ')
    unprefixed = message.content[int(len(args[0])+1):]
    if len(args)==1: no_args = True
    i_dont_know_what_this_means_but_i_am_declaring_it_anyway = 0
    if msg.startswith(prefix) and message.author.bot==False and len(args[0])!=1:
        if msg.startswith(prefix+'say'):
            await message.channel.send(unprefixed)
        if msg.startswith(prefix+'hack'):
            if no_args:
                await message.channel.send(f'Please tag someone!\nExample: {prefix}hack <@'+str(message.author.id)+'>')
            else:
                tohack = message.mentions[0]
                console = 'C:\\Users\\Anonymous601>'
                if args[1].startswith('<@'):
                    main = await message.channel.send('Opening Console...')
                    flow = splashes.hackflow(tohack)
                    for i in range(0, len(flow)):
                        console = console + flow[i][1:]
                        newembed = discord.Embed(title='Anonymous601 Hacking Console', description=f'```{console}```',colour=discord.Colour.green())
                        newembed.set_thumbnail(url=myself.hackfind(flow[i], tohack.avatar_url))
                        await main.edit(content='', embed=newembed)
                        await asyncio.sleep(random.randint(2, 4))
                else:
                    console = console + 'hack.exe -u '+str(message.author.name)+'ERROR: INVALID TAG.\nACCESS DENIED.\n\nHash encoded base64 cipher code:\n'+myself.bin(message.author.name)+ '\n' + console
                    embed = discord.Embed(title='Anonymous601 Hacking Console', description=f'```{console}```',colour=discord.Colour.green())
                    await message.channel.send(embed=embed)
        if msg.startswith(prefix+'base64'):
            if no_args:
                await message.channel.send(f'Please input something to encode! Like `{prefix}base64 discord.py is better than discord.js`')
            else:
                await message.channel.send(f'```{myself.encodeb64(unprefixed)}```')
        if msg.startswith(prefix+'ufo'):
            num = str(random.randint(50, 100))
            data = myself.api('http://ufo-api.herokuapp.com/api/sightings/search?limit='+num)
            if data['status']!='OK':
                await message.channel.send('There was a problem on retrieving the info.\nThe server said: "'+str(data['status'])+'" :eyes:')
            else:
                ufo = random.choice(data['sightings'])
                embed = discord.Embed(title='UFO Sighting in '+str(ufo['city'])+', '+str(ufo['state']), description='**Summary:** '+str(ufo['summary'])+'\n\n**Shape:** '+str(ufo['shape'])+'\n**Sighting Date: **'+str(ufo['date'])[:-8].replace('T', ' ')+'\n**Duration: **'+str(ufo['duration'])+'\n\n[Article Source]('+str(ufo['url'])+')', colour=discord.Colour.green())
                embed.set_footer(text='Username601 raided Area 51 and found this!')
                await message.channel.send(embed=embed)
        if msg.startswith(prefix+'embed'):
            if '(title:' not in msg or '(desc:' not in msg:
                await message.channel.send('An embed requires title and description.\nFor example: `'+prefix+'embed (title:this is a title) (desc:this is a description)`\n\nOptional; `footer, auth, hex`')
            else:
                try:
                    title_e = msg.split('(title:')[1].split(')')[0]
                    desc_e = msg.split('(desc:')[1].split(')')[0]
                    if '(footer:' in msg:
                        foot = msg.split('(footer:')[1].split(')')[0]
                        embed.set_footer(text=foot)
                    if '(auth:' in msg:
                        auth = msg.split('(auth:')[1].split(')')[0]
                        embed.set_author(name=auth)
                    if '(hex:' not in msg:
                        embed = discord.Embed(title=title_e, description=desc_e, colour=discord.Colour.from_rgb(random.randint(0, 255), random.randint(0, 255), random.randint(0, 255)))
                    else:
                        if msg.split('(hex:')[1].split(')')[0].startswith('#'):
                            hexer = msg.split('(hex:')[1].split(')')[0][1:]
                        else:
                            hexer = msg.split('(hex:')[1].split(')')[0]
                        arr = myself.convertrgb(hexer, '0')
                        embed = discord.Embed(title=title_e, description=desc_e, colour=discord.Colour.from_rgb(arr[0], arr[1], arr[2]))
                    await message.channel.send(embed=embed)
                except Exception as e:
                    await message.channel.send(str(client.get_emoji(BotEmotes.error)) + f' | An error occurd. For programmers: ```{e}```')
        if msg.startswith(prefix+'pokequiz'):
            wait = await message.channel.send(str(client.get_emoji(BotEmotes.loading)) + ' | Please wait... Generating quiz...')
            num = random.randint(1, 800)
            try:
                corr = pb.pokemon(str(num)).name
            except Exception as e:
                await wait.edit(content=str(client.get_emoji(BotEmotes.error)) + f' | An error occured! ```{e}```')
            hint = 2
            attempt = 10
            gameplay = True
            guy = message.author
            while gameplay==True:
                newembed = discord.Embed(title='Pokemon Quiz!', description=f'Guess the pokemon\'s name!\nTimeout: 45 seconds.\nHint left: **{str(hint)}** | Attempts left: **{str(attempt)}**', colour=discord.Colour.green())
                newembed.set_image(url=f'https://assets.pokemon.com/assets/cms2/img/pokedex/full/{str(num)}.png')
                newembed.set_footer(text='Type "hint" to give.. uh... the HINT! :D')
                newembed.set_thumbnail(url=f'https://raw.githubusercontent.com/PokeAPI/sprites/master/sprites/pokemon/{str(num)}.png')
                await wait.edit(content='', embed=newembed)
                if int(attempt)<1:
                    await message.channel.send('You lose! The pokemon is **'+str(corr)+'**!')
                    gameplay = False
                    break
                def checking(m):
                    return m.author == guy
                try:
                    guessing = await client.wait_for('message', check=checking, timeout=45.0)
                except asyncio.TimeoutError:
                    attempt = int(attempt) - 1
                    await message.channel.send('Too late! Game ended... :pensive:')
                    gameplay = False
                    break
                if str(guessing.content).lower()==corr:
                    currentmsg = guessing
                    await currentmsg.add_reaction('✅')
                    await message.channel.send(str(client.get_emoji(BotEmotes.success)) +' | You are correct! The pokemon is **'+str(corr)+'**')
                    gameplay = False
                    break
                elif str(guessing.content).lower()=='hint':
                    currentmsg = guessing
                    if hint<1:
                        await currentmsg.add_reaction('❌')
                        attempt = int(attempt) - 1
                    else:
                        await currentmsg.add_reaction('✅')
                        thehint = random.choice([myself.hintify(corr), 'Pokemon name starts with "'+str(list(corr)[0])+'"', 'Pokemon name has '+str(len(corr))+' letters!', 'Pokemon name ends with "'+str(list(corr)[len(corr)-1])+'"'])
                        await message.channel.send('Hint: '+thehint+'!')
                        hint = int(hint) - 1
                        attempt = int(attempt) - 1
                else:
                    if attempt!=0:
                        await guessing.add_reaction('❌')
                        attempt = int(attempt) - 1
                    else:
                        await guessing.add_reaction('❌')
                        await message.channel.send('You lose! The pokemon is **'+str(corr)+'**!')
                        gameplay = False
                        break
        if msg.startswith(prefix+'ss'):
            if len(args)>1:
                if args[1]=='--help':
                    embed = discord.Embed(title='Special say command help', description='**REQUIRES `MANAGE CHANNELS` PERMISSION**\nThis is a special say command that has the following:\n1. @someone | Tags random people in the server. [On April fools 2018, Discord made this feature, but removed the day after.](https://www.youtube.com/watch?v=BeG5FqTpl9U) (Please use wisely.)\n2. @owner | Tags the server owner. Please don\'t spam this feature.\n3. --ch #{channelname} | Sends a message on a specific channel.', colour=discord.Colour.green())
                    await message.channel.send(embed=embed)
                else:
                    if message.author.guild_permissions.manage_channels==False:
                        await message.channel.send(str(client.get_emoji(BotEmotes.error)) +' | You need to have the `Manage channels` permission.')
                    else:
                        randomppl = random.choice(message.guild.members).id
                        if args[1]=='--ch':
                            try:
                                ch = client.get_channel(int(args[2][2:][:-1]))
                                await ch.send(msg[int(len(args[0])+len(args[1])+len(args[2])+3):].replace('@someone', '<@'+str(randomppl)+'>').replace('@owner', '<@'+str(message.guild.owner.id)+'>'))
                            except:
                                await message.channel.send(str(client.get_emoji(BotEmotes.error)) + ' | An error occured! :x:')
                        else:
                            await message.channel.send(msg[int(len(args[0])+1):].replace('@someone', f'<@{str(randomppl)}>').replace('@owner', '<@'+str(message.guild.owner.id)+'>'))
        if msg.startswith(prefix+'inspectservers'):
            if int(message.author.id)==661200758510977084:
                ee = ''
                for i in range(0, len(client.guilds)):
                    ee = ee + '**' + client.guilds[i].name + '** ('+str(len(client.guilds[i].members))+' Members)\n'
                embed = discord.Embed(title='Heya, here are all the servers i am in.', description=ee, colour=discord.Colour.blue())
                await message.author.send(embed=embed)
                await message.channel.send('...k')
            else:
                await message.channel.send('...')
        if msg.startswith(prefix+'pandafact') or msg.startswith(prefix+'birdfact') or msg.startswith(prefix+'birbfact'):
            if msg.startswith(prefix+'pandafact'): link = 'https://some-random-api.ml/facts/panda'
            else: link = 'https://some-random-api.ml/facts/bird'
            data = myself.jsonisp(link)['fact']
            await message.channel.send(embed=discord.Embed(title='Did you know?', description=data, colour=discord.Colour.red()))
        if msg.startswith(prefix+'iss'):
            iss = myself.jsonisp('https://open-notify-api.herokuapp.com/iss-now.json')
            ppl = myself.jsonisp('https://open-notify-api.herokuapp.com/astros.json')
            total = '```'
            for i in range(0, len(ppl['people'])):
                total += str(i+1) + '. ' + ppl['people'][i]['name'] + ((20-(len(ppl['people'][i]['name'])))*' ') + ppl['people'][i]['craft'] + '\n'
            embed = discord.Embed(title='Position: '+str(iss['iss_position']['latitude'])+' '+str(iss['iss_position']['longitude']), description='**People at craft:**\n\n'+str(total)+'```', colour=discord.Colour.red())
            await message.channel.send(embed=embed)
        if msg.startswith(prefix+'qotd'):
            data = myself.jsonisp('https://quotes.rest/qod')['contents']['quotes'][0]
            embed = discord.Embed(title=data['quote'], description=data['author'], color=discord.Colour.blue())
            embed.set_image(url=data['background'])
            embed.set_footer(text='New quote will be generated in the next day.')
            await message.channel.send(embed=embed)
        if msg.startswith(prefix+'pika') or args[0]==prefix+'panda' or msg.startswith(prefix+'redpanda'):
            if msg.startswith(prefix+'pika'): link, col, msg = "https://some-random-api.ml/pikachuimg", discord.Colour.from_rgb(255, 255, 0), 'pika pika!'
            elif msg.startswith(prefix+'redpanda'): link, col, msg = "https://some-random-api.ml/img/red_panda", discord.Colour.red(), 'Ok, here are some pics of red pandas.'
            else: link, col, msg = "https://some-random-api.ml/img/panda", discord.Colour.green(), 'Here is some cute pics of pandas.'
            data = myself.jsonisp(link)['link']
            embed = discord.Embed(title=msg, color=col)
            embed.set_image(url=data)
            await message.channel.send(embed=embed)
        if args[0]==prefix+'chat':
            if no_args:
                await message.channel.send('Please send me a chat! And i will respond to it.')
            else:
                wait = await message.channel.send(str(client.get_emoji(BotEmotes.loading)) + ' | Please wait... Responding...')
                try:
                    data = myself.jsonisp('https://some-random-api.ml/chatbot?message='+str(myself.urlify(unprefixed)))['response']
                    await wait.edit(content=data)
                except:
                    await wait.edit(content='I am sorry. I do not understand your message.')
        if msg.startswith(prefix+'hangman'):
            wait = await message.channel.send(str(client.get_emoji(BotEmotes.loading)) + ' | Please wait... generating...')
            the_word = myself.api("https://random-word-api.herokuapp.com/word?number=1")
            main_guess_cor = list(the_word[0])
            main_guess_hid = []
            server_id = message.guild.id
            wrong_guesses = ''
            for i in range(0, len(main_guess_cor)):
                main_guess_hid.append('\_ ')
            gameplay = True
            guessed = []
            level = 0
            playing_with = message.author
            playing_with_id = int(message.author.id)
            while gameplay==True:
                print(''.join(main_guess_cor))
                print(''.join(main_guess_hid))
                if message.content==prefix+'hangman' and message.author.id!=int(playing_with_id) and message.guild.id==server_id:
                    await message.channel.send('<@'+str(message.author.id)+'>, cannot play hangman when a game is currently playing!')
                newembed = discord.Embed(title=''.join(main_guess_hid), description='Wrong guesses: '+str(wrong_guesses), colour=discord.Colour.red())
                newembed.set_image(url=f'https://raw.githubusercontent.com/vierofernando/username601/master/assets/hangman_{str(level)}.png')
                newembed.set_footer(text='Type "showanswer" to show the answer and end the game.')
                await message.channel.send(embed=newembed)
                if '\_ ' not in ''.join(main_guess_hid):
                    await message.channel.send(f'Congratulations! <@{str(playing_with_id)}> win! :tada:\nThe answer is "'+str(''.join(main_guess_cor))+'".')
                    gameplay = False
                    break
                if level>7:
                    await message.channel.send(f'<@{str(playing_with_id)}> lost! :(\nThe answer is actually "'+str(''.join(main_guess_cor))+'".')
                    gameplay = False
                    break
                def is_not_stranger(m):
                    return m.author == playing_with
                try:
                    trying = await client.wait_for('message', check=is_not_stranger, timeout=20.0)
                except asyncio.TimeoutError:
                    await message.channel.send(f'<@{str(playing_with_id)}> did not response in 20 seconds so i ended the game. Keep un-AFK!\nOh and btw, the answer is '+str(''.join(main_guess_cor))+'. :smirk:')
                    gameplay = False
                    break
                if str(trying.content).lower()=='showanswer':
                    await message.channel.send('The answer is actually '+str(''.join(main_guess_cor)+'.'))
                    gameplay = False
                    break
                elif len(str(trying.content))>1:
                    await message.channel.send('One word at a time. Game ended :rage:')
                    gameplay = False
                    break
                elif str(trying.content).lower() in guessed:
                    await message.channel.send(f'<@{str(playing_with_id)}>, You have guessed that letter!')
                    level = int(level)+1
                elif str(trying.content).lower() in ''.join(main_guess_cor).lower():
                    guessed.append(str(trying.content).lower())
                    for i in range(0, len(main_guess_cor)):
                        if main_guess_cor[i].lower()==str(trying.content).lower():
                            main_guess_hid[i] = str(trying.content).lower()
                else:
                    level = int(level) + 1
                    wrong_guesses = wrong_guesses + str(trying.content).lower() + ', '
        if msg.startswith(prefix+'tictactoe'):
            box_nums = list('123456789')
            can_used = list('123456789')
            box = f' {box_nums[0]} | {box_nums[1]} | {box_nums[2]}\n===========\n {box_nums[3]} | {box_nums[4]} | {box_nums[5]}\n===========\n {box_nums[6]} | {box_nums[7]} | {box_nums[8]}\n'
            if no_args:
                embed = discord.Embed(title='TicTacToe™ wtih '+str(splashes.getTicTacToeHeader()), description=f'Plays tic-tac-toe with the BOT. Very simple.\n\n**To start playing, type;**\n`{prefix}tictactoe X` (To play tictactoe as X)\n`{prefix}tictactoe O` (To play tictactoe as O)', colour=discord.Colour.red())
                embed.set_image(url='https://raw.githubusercontent.com/vierofernando/username601/master/assets/tictactoe.png')
                await message.channel.send(embed=embed)
            else:
                if args[1].lower() not in list('xo'):
                    await message.channel.send('Must be X or O!')
                else:
                    if args[1].lower()=='x':
                        user_sym = 'X'
                        bot_sym = 'O'
                    else:
                        user_sym = 'O'
                        bot_sym = 'X'
                    playing_with = message.author
                    user_id = int(message.author.id)
                    user_name = message.guild.get_member(user_id).display_name
                    gameplay = True
                    usedByUser = []
                    usedByBot = []
                    embed = discord.Embed(title='Playing Tictactoe with '+str(user_name), description=f'Viero Fernando ({user_sym}) | Username601 ({bot_sym})\nType the numbers to fill out the boxes.```{box}```', colour=discord.Colour.green())
                    embed.set_footer(text='Type "endgame" to well, end the game. Or wait for 20 seconds and the game will kill itself! ;)')
                    gameview = await message.channel.send(embed=embed)
                    while gameplay==True:
                        if discordgames.checkWinner(box_nums, user_sym, bot_sym)=='userwin':
                            await message.channel.send(f'Congrats <@{user_id}>! You won against me! :tada:')
                            gameplay = False
                            break
                        elif discordgames.checkWinner(box_nums, user_sym, bot_sym)=='botwin':
                            await message.channel.send(f'LOL, i win the tic tac toe! :tada:\nYou lose! :pensive:')
                            gameplay = False
                            break
                        elif discordgames.checkEndGame(can_used)==True:
                            await message.channel.send('Nobody wins? OK... :neutral_face:')
                            gameplay = False
                            break
                        def is_not_stranger(m):
                            return m.author == playing_with
                        try:
                            trying = await client.wait_for('message', check=is_not_stranger, timeout=20.0)
                        except asyncio.TimeoutError:
                            await message.channel.send(f'<@{user_id}> did not response in 20 seconds so i ended the game. Keep un-AFK!')
                            gameplay = False
                            break
                        if str(trying.content) in can_used:
                            for i in range(0, len(box_nums)):
                                if box_nums[i]==trying.content:
                                    usedByUser.append(box_nums[i])
                                    box_nums[i] = user_sym
                                    for j in range(0, len(can_used)):
                                        if j==box_nums[i]:
                                            del can_used[j]
                                            break
                                    break
                            bot_select = ''
                            while bot_select=='' and len(can_used)>1:
                                bot_select = random.choice(can_used)
                            print('I SELECT: '+bot_select)
                            for i in range(0, len(can_used)):
                                if can_used[i]==bot_select:
                                    for j in range(0, len(box_nums)):
                                        if box_nums[j]==can_used[i]:
                                            box_nums[j] = bot_sym
                                            break
                                    usedByBot.append(can_used[i])
                                    del can_used[i]
                                    break
                            box = f' {box_nums[0]} | {box_nums[1]} | {box_nums[2]}\n===========\n {box_nums[3]} | {box_nums[4]} | {box_nums[5]}\n===========\n {box_nums[6]} | {box_nums[7]} | {box_nums[8]}\n'
                            newembed = discord.Embed(title='Playing Tictactoe with '+str(user_name), description=f'Viero Fernando ({user_sym}) | Username601 ({bot_sym})\nType the numbers to fill out the boxes.```{box}```', colour=discord.Colour.green())
                            newembed.set_footer(text='Type "endgame" to well, end the game. Or wait for 20 seconds and the game will kill itself! ;)')
                            await message.channel.send(embed=newembed)
                        elif str(trying.content).lower()=='endgame':
                            await message.channel.send('Game ended.')
                            gameplay = False
                            break
        if msg.startswith(prefix+'randomavatar'):
            gibb_name = ''
            for i in range(0, random.randint(5, 10)):
                gibb_name = gibb_name + random.choice(list('ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz'))
            embed = discord.Embed(colour=discord.Colour.green())
            embed.set_image(url=f'https://api.adorable.io/avatars/285/{gibb_name}.png')
            await message.channel.send(embed=embed)
        if msg.startswith(prefix+'mathquiz'):
            num1 = random.randint(1, 100)
            num2 = random.randint(1, 100)
            symArray = ['+', '-', 'x', ':', '^']
            ansArray = [num1+num2, num1-num2, num1*num2, num1/num2, num1**num2]
            arrayId = random.randint(0, 4)
            sym = symArray[arrayId]
            await message.channel.send('**MATH QUIZ (15 seconds)**\n'+str(num1)+' '+str(sym)+' '+str(num2)+' = ???')
            def is_correct(m):
                return m.author == message.author
            answer = int(ansArray[arrayId])
            try:
                trying = await client.wait_for('message', check=is_correct, timeout=15.0)
            except asyncio.TimeoutError:
                return await message.channel.send(':pensive: No one? Okay then, the answer is: {}.'.format(answer))
            if str(trying.content)==str(answer):
                await message.channel.send(str(client.get_emoji(BotEmotes.success)) +' | <@'+str(message.author.id)+'>, You are correct! :tada:')
            else:
                await message.channel.send(str(client.get_emoji(BotEmotes.error)) +' | <@'+str(message.author.id)+'>, Incorrect. The answer is {}.'.format(answer))
        if msg.startswith(prefix+'guessavatar'):
            if len(message.guild.members)>500:
                await message.channel.send('Sorry, to protect some people\'s privacy, this command is not available for Large servers. (over 500 members)')
            else:
                wait = await message.channel.send(str(client.get_emoji(BotEmotes.loading)) + ' | Please wait... generating question...\nThis process may take longer if your server has more members.')
                avatarAll = []
                nameAll = []
                for ppl in message.guild.members:
                    if message.guild.get_member(int(ppl.id)).status.name!='offline':
                        avatarAll.append(str(ppl.avatar_url).replace('webp', 'png'))
                        nameAll.append(ppl.display_name)
                if len(avatarAll)<=4:
                    await message.channel.send(str(client.get_emoji(BotEmotes.error)) +' | Need more online members! :x:')
                else:
                    numCorrect = random.randint(0, len(avatarAll)-1)
                    corr_avatar = avatarAll[numCorrect]
                    corr_name = nameAll[numCorrect]
                    nameAll.remove(corr_name)
                    wrongArr = []
                    for i in range(0, 3):
                        wrongArr.append(random.choice(nameAll))
                    abcs, emots = list('🇦🇧🇨🇩'), list('🇦🇧🇨🇩')
                    randomInt = random.randint(0, 3)
                    corr_order = random.choice(abcs[randomInt])
                    abcs[randomInt] = '0'
                    question = ''
                    chooseCount = 0
                    for assign in abcs:
                        if assign!='0':
                            question = question + '**'+ str(assign) + '.** '+str(wrongArr[chooseCount])+ '\n'
                            chooseCount = int(chooseCount) + 1
                        else:
                            question = question + '**'+ str(corr_order) + '.** '+str(corr_name)+ '\n'
                    embed = discord.Embed(title='What does the avatar below belongs to?', description=':eyes: Click the reactions! **You have 20 seconds.**\n\n'+str(question), colour=discord.Colour.green())
                    embed.set_footer(text='For privacy reasons, the people displayed above are online users.')
                    embed.set_image(url=corr_avatar)
                    main = await message.channel.send(embed=embed)
                    for i in emots: await main.add_reaction(i)
                    def is_correct(reaction, user):
                        return user == message.author
                    try:
                        reaction, user = await client.wait_for('reaction_add', check=is_correct, timeout=20.0)
                    except asyncio.TimeoutError:
                        return await message.channel.send(':pensive: No one? Okay then, the answer is: '+str(corr_order)+'. '+str(corr_name))
                    if str(reaction.emoji)==str(corr_order):
                        await message.channel.send(str(client.get_emoji(BotEmotes.error)) +' | <@'+str(message.author.id)+'>, You are correct! :tada:')
                    else:
                        await message.channel.send(str(client.get_emoji(BotEmotes.success)) +' | <@'+str(message.author.id)+'>, Incorrect. The answer is '+str(corr_order)+'. '+str(corr_name))
        if msg.startswith(prefix+'geoquiz'):
            wait = await message.channel.send(str(client.get_emoji(BotEmotes.loading)) + ' | Please wait... generating question...')
            data = myself.api("https://restcountries.eu/rest/v2/")
            topic = random.choice(splashes.getGeoQuiz())
            chosen_nation_num = random.randint(0, len(data))
            chosen_nation = data[chosen_nation_num]
            data.remove(data[chosen_nation_num])
            wrongs = []
            correct = str(chosen_nation[topic])
            for i in range(0, 4):
                integer = random.randint(0, len(data))
                wrongs.append(str(data[integer][str(topic)]))
                data.remove(data[integer])
            emot = list('🇦🇧🇨🇩')
            static_emot = list('🇦🇧🇨🇩')
            corr_order_num = random.randint(0, 3)
            corr_order = emot[corr_order_num]
            emot[corr_order_num] = '0'
            question = ''
            for emote in emot:
                if emote!='0':
                    added = random.choice(wrongs)
                    question = question + emote + ' ' + added + '\n'
                    wrongs.remove(added)
                else:
                    question = question + corr_order + ' ' + correct + '\n'
            embed = discord.Embed(title='Geography: '+str(topic)+' quiz!', description=':nerd: Click on the reaction! **You have 20 seconds.**\n\nWhich '+str(topic)+' belongs to '+str(chosen_nation['name'])+'?\n'+str(question), colour=discord.Colour.blue())
            await wait.edit(content='', embed=embed)
            for i in range(0, len(static_emot)):
                await wait.add_reaction(static_emot[i])
            guy = message.author
            def check(reaction, user):
                return user == guy
            try:
                reaction, user = await client.wait_for('reaction_add', timeout=20.0, check=check)
            except asyncio.TimeoutError:
                await main.add_reaction('😔')
            if str(reaction.emoji)==str(corr_order):
                await message.channel.send(str(client.get_emoji(BotEmotes.success)) +' | <@'+str(guy.id)+'>, Congrats! You are correct. :partying_face:')
            else:
                await message.channel.send(str(client.get_emoji(BotEmotes.error)) +' | <@'+str(guy.id)+'>, You are incorrect. The answer is '+str(corr_order)+'.')
        if msg.startswith(prefix+'emojiimg'):
            if no_args:
                await message.channel.send('Please send a custom emoji!')
            elif len(args)==2:
                emoji = args[1].split(':')
                try:
                    emoji_id = emoji[2][:-1]
                except IndexError:
                    accept = False
                    await message.channel.send(str(client.get_emoji(BotEmotes.error)) +' | For some reason, we cannot proccess default emojis. Sorry!')
                try:
                    if client.get_emoji(int(emoji_id)).animated==False:
                        link = 'https://cdn.discordapp.com/emojis/'+str(emoji_id)+'.png?v=1'
                        accept = True
                    else:
                        await message.channel.send(str(client.get_emoji(BotEmotes.error)) + ' | Error processing it.')
                        accept = False
                except:
                    await message.channel.send(str(client.get_emoji(BotEmotes.error)) + ' | Oops! There are an error *for some reason.*')
                if accept==True:
                    embed = discord.Embed(title='Emoji pic for ID of '+str(emoji_id), colour=discord.Colour.red())
                    embed.set_image(url=link)
                    await message.channel.send(embed=embed)
            else:
                await message.channel.send(str(client.get_emoji(BotEmotes.error)) +' | Invalid parameters.')
        if msg.startswith(prefix+'ban'):
            begin = True
            if no_args:
                await message.channel.send(str(client.get_emoji(BotEmotes.error)) + ' | Please mention someone!')
                begin = False
            else:
                perms = message.author.guild_permissions.ban_members
                if perms==False:
                    begin = False
                    await message.channel.send(str(client.get_emoji(BotEmotes.error)) + f' | <@{str(message.author.id)}>, you don\'t have the `Ban Members` permission! :rage:')
                else:
                    try:
                        if args[1].startswith('<@!'):
                            criminal = message.guild.get_member(int(args[1][3:][:-1]))
                        else:
                            criminal = message.guild.get_member(int(args[1][2:][:-1]))
                        if criminal.id==message.author.id:
                            await message.channel.send(str(client.get_emoji(BotEmotes.error)) +' | What a weirdo. Banning yourself.')
                            begin = False
                    except:
                        await message.channel.send(str(client.get_emoji(BotEmotes.error)) +' | Invalid mention.')
                    if criminal.guild_permissions.administrator==True or criminal.guild_permissions.manage_guild==True or criminal.guild_permissions.manage_permissions==True:
                        await message.channel.send(str(client.get_emoji(BotEmotes.error)) +' | You cannot ban a moderator.')
                        begin = False
                    if begin==True:
                        if len(args)<3:
                            reas = 'Unspecified'
                        else:
                            reas = msg[int(len(args[1])+len(args[0])+2):]
                        try:
                            await message.guild.ban(criminal, reason=reas)
                            msgs = [
                                "It is time. "+criminal.name+".",
                                criminal.name+", Get. OUT.",
                                "[BOT] Successfully executed kill"+criminal.name+"().",
                                'It was fun, now is time for '+criminal.name+' to leave.',
                                'We don\'t even need '+criminal.name+' anymore.',
                                'Bye bye, '+criminal.name+'.'
                            ]
                            await message.channel.send(str(client.get_emoji(BotEmotes.success)) + ' | '+random.choice(msgs))
                        except:
                            await message.channel.send(str(client.get_emoji(BotEmotes.error)) + ' | There was an error on banning '+criminal.name+'.')
        if msg.startswith(prefix+'rp'):
            if message.author.id==661200758510977084:
                try:
                    user_to_send = client.get_user(int(args[1]))
                    em = discord.Embed(title="Hi, "+user_to_send.name+"! the bot owner sent a response for your feedback.", description=str(message.content[int(len(args[0])+len(args[1])+2):]), colour=discord.Colour.green())
                    em.set_footer(text="Feeling unsatisfied? Then join our support server! (discord.gg/HhAPkD8)")
                    await user_to_send.send(embed=em)
                    await message.add_reaction('✅')
                except Exception as e:
                    await message.channel.send(str(client.get_emoji(BotEmotes.error)) + f' | Error: `{e}`')
            else:
                await message.channel.send('You are not the bot owner.')
        if msg.startswith(prefix+'feedback'):
            if no_args:
                await message.channel.send('Where\'s the feedback? :(')
            elif len(list(args))>1000:
                await message.channel.send('That\'s too long! Please provide a simpler description.')
            else:
                wait = await message.channel.send(str(client.get_emoji(BotEmotes.loading)) + ' | Please wait... Transmitting data to owner...')
                bans = []
                async for messages in client.get_channel(706459051034279956).history():
                    if messages.content.startswith('Banned user with ID of: ['): bans.append(messages.content)
                banned = False
                if len(bans)>0:
                    for i in bans:
                        if int(message.author.id)==int(i.split('[')[1].split(']')[0]):
                            await wait.edit(content='', embed=discord.Embed(title='You are banned', description='Sorry! you are banned from using the `'+prefix+'feedback` command. Reason:```'+i.split('REASON:"')[1].split('"')[0]+'```', colour=discord.Colour.red()))
                            banned = True
                            break
                if not banned:
                    try:
                        fb = unprefixed
                        feedbackCh = client.get_channel(706459051034279956)
                        await feedbackCh.send('<@661200758510977084>, User with ID: '+str(message.author.id)+' sent a feedback: **"'+str(fb)+'"**')
                        embed = discord.Embed(title='Feedback Successful', description=str(client.get_emoji(BotEmotes.success)) + '** | Success!**\nThanks for the feedback!\n**We will DM you as the response. **If you are unsatisfied, [Join our support server and give us more details.](https://discord.gg/HhAPkD8)',colour=discord.Colour.green())
                        await wait.edit(content='', embed=embed)
                    except:
                        await wait.edit(content=str(client.get_emoji(BotEmotes.error)) + ' | Error: There was an error while sending your feedback. Sorry! :(')
        if msg.startswith(prefix+'fbban'):
            if message.channel.id==706459051034279956 and int(message.author.id)==661200758510977084:
                await message.channel.send('Banned user with ID of: ['+str(args[1])+'] REASON:"'+str(message.content[int(len(args[0])+len(args[1])+2):])+'"')
            else:
                await message.channel.send(str(client.get_emoji(BotEmotes.error)) +' | Invalid channel/user.')
        if msg.startswith(prefix+'gdlevel'):
            if no_args:
                await message.channel.send(':x: Please enter a level ID!')
            else:
                if args[1].isnumeric()==False:
                    await message.channel.send(':x: That is not a level ID!')
                else:
                    try:
                        levelid = str(args[1])
                        toEdit = await message.channel.send("Retrieving Data...")
                        data = myself.api("https://gdbrowser.com/api/level/"+str(levelid))
                        image = 'https://gdbrowser.com/icon/'+data["author"]
                        embed = discord.Embed(
                            title = data["name"]+' ('+str(data["id"])+')',
                            description = data["description"],
                            colour = discord.Colour.blue()
                        )
                        embed.set_author(name=data["author"], icon_url=image)
                        embed.add_field(name='Difficulty', value=data["difficulty"])
                        gesture = ':+1:'
                        if data['disliked']==True:
                            gesture = ':-1:'
                        embed.add_field(name='Level Stats', value=str(data["likes"])+' '+gesture+'\n'+str(data["downloads"])+" :arrow_down:", inline='False')
                        embed.add_field(name='Level Rewards', value=str(data["stars"])+" :star:\n"+str(data["orbs"])+" orbs\n"+str(data["diamonds"])+" :gem:")
                        await toEdit.edit(content='', embed=embed)
                    except Exception as e:
                        await toEdit.edit(content=f'```{e}```')
        if msg.startswith(prefix+'gdsearch'):
            if no_args:
                await message.channel.send(':x: Please input a query!')
            else:
                try:
                    query = myself.urlify(unprefixed)
                    data = myself.api('https://gdbrowser.com/api/search/'+str(query))
                    levels = ''
                    count = 0
                    for i in range(0, len(data)):
                        if data[count]['disliked']==True:
                            like = ':-1:'
                        else:
                            like = ':+1:'
                        levels = levels + str(count+1)+'. **'+data[count]['name']+'** by '+data[count]['author']+' (`'+data[count]['id']+'`)\n:arrow_down: '+data[count]['downloads']+' | '+like+' '+data[count]['likes']+'\n'
                        count = int(count) + 1
                    embedy = discord.Embed(title='Geometry Dash Level searches for "'+str(unprefixed)+'":', description=levels, colour=discord.Colour.blue())
                    await message.channel.send(embed=embedy)
                except:
                    await message.channel.send(str(client.get_emoji(BotEmotes.error)) + ' | Error: Not Found. :four::zero::four:')
        if msg.startswith(prefix+'emojiinfo'):
            test = 0
            if test==0:
                try:
                    erry = False
                    emojiid = int(args[1].split(':')[2][:-1])
                    data = client.get_emoji(emojiid)
                except:
                    erry = True
                    await message.channel.send(':x: For some reason, we cannot process your emoji ;(')
                if erry==False:
                    if data.animated==True:
                        anim = 'This emoji is an animated emoji. **Only nitro users can use it.**'
                    else:
                        anim = 'This emoji is a static emoji. **Everyone can use it (except if limited by role)**'
                    embedy = discord.Embed(title='Emoji info for :'+str(data.name)+':', description='**Emoji name:** '+str(data.name)+'\n**Emoji ID: **'+str(data.id)+'\n'+anim+'\n**Emoji\'s server ID: **'+str(data.guild_id)+'\n**Emoji creation time: **'+str(data.created_at)[:-7]+' UTC.', colour=discord.Colour.magenta())
                    embedy.set_thumbnail(url='https://cdn.discordapp.com/emojis/'+str(data.id)+'.png?v=1')
                    await message.channel.send(embed=embedy)
        if args[0]==prefix+'threats' or args[0]==prefix+'deepfry' or args[0]==prefix+'blurpify':
            if no_args:
                await message.channel.send('Please tag someone!')
            else:
                if args[0].startswith(prefix+'threat'):
                    inputtype = 'url'
                else:
                    inputtype = 'image'
                av = message.mentions[0].avatar_url
                embed = discord.Embed(colour=discord.Colour.red())
                embed.set_image(url='https://nekobot.xyz/api/imagegen?type='+str(args[0])[1:]+'&'+inputtype+'='+str(av)[:-15]+'.png&raw=1')
                await message.channel.send(embed=embed)
        if args[0]==prefix+'clyde' or args[0]==prefix+'trumptweet' or args[0]==prefix+'kannagen':
            if no_args:
                await message.channel.send('Please input a text...')
            else:
                embed = discord.Embed(colour=discord.Colour.blue())
                embed.set_image(url='https://nekobot.xyz/api/imagegen?type='+str(args[0][1:])+'&text='+myself.urlify(str(unprefixed))+'&raw=1')
                await message.channel.send(embed=embed)
        if msg.startswith(prefix+'clear') or msg.startswith(prefix+'purge'):
            checky = message.author.guild_permissions.manage_messages
            req = message.author.name
            if checky==False:
                await message.channel.send(str(client.get_emoji(BotEmotes.error)) +' | You don\'t have the permission `Manage Messages` to do this command \>:(')
            else:
                contin = True
                if args[1].isnumeric()==True:
                    try:
                        count = int(args[1])+1
                        if count>500:
                            await message.channel.send('That\'s **TOO MANY** messages to be deleted!\nJust clone the channel and delete the old one.\neasy peasy.')
                            contin = False
                    except:
                        await message.channel.send('That is NOT a number!')
                        contin = False
                if contin==True:
                    if args[1].isnumeric()==True:
                        try:
                            deleted_messages = await message.channel.purge(limit=count)
                            await message.channel.send('**Requested by '+req+':** Deleted '+str(len(deleted_messages)-1)+' messages in <#'+str(message.channel.id)+'>.', delete_after=3)
                        except Exception as e:
                            await message.channel.send(str(client.get_emoji(BotEmotes.error)) + ' | An error occured during purging. ```'+str(e)+'```')
                    elif args[1].startswith('<@'):
                        check_guy = message.mentions[0]
                        try:
                            def forperson(m):
                                return m.author == check_guy
                            deleted_messages = await message.channel.purge(check=forperson, limit=500)
                            await message.channel.send('**Requested by '+req+':** Deleted '+str(len(deleted_messages))+' messages in <#'+str(message.channel.id)+'>.\nSpecifically for messages by <@'+str(check_guy.id)+'>.', delete_after=10)
                        except Exception as e:
                            await message.channel.send(str(client.get_emoji(BotEmotes.error)) + ' | An error occured during purging. ```'+str(e)+'```')
        if args[0]==prefix+'ex' or args[0]==prefix+'eval':
            if int(message.author.id)==661200758510977084:
                command = unprefixed
                try:
                    res = eval(command)
                    if inspect.isawaitable(res):
                        await message.channel.send('```py\n'+await res+'```')
                    else:
                        await message.channel.send('```py\n'+str(res)+'```')
                except Exception as e:
                    await message.channel.send(f'Oops! We got an error here, nerd!\n```{e}```')
            else:
                await message.channel.send('This command somehow doesn\'t work in discord.py.\nTry discord.js instead.')
        if args[0]==prefix+'s':
            await message.delete()
            member = message.guild.get_member(int(message.author.id))
            if message.author.guild_permissions.manage_guild==True or int(message.author.id)==661200758510977084:
                accept = True
            else:
                await message.channel.send(str(client.get_emoji(BotEmotes.error)) +' | <@'+str(message.author.id)+'>, You need to have the MANAGE SERVER permission or  be the bot owner to do this command.\nTo be the bot owner, try creating a bot :v')
                accept = False
            if accept==True:
                await message.channel.send(message.content[3:])
        if msg.startswith(prefix+'addrole') or args[0]==prefix+'ar':
            if message.author.guild_permissions.manage_roles==False:
                await message.channel.send(str(client.get_emoji(BotEmotes.error)) +f' | <@{str(message.author.id)}>, you don\'t have the `Manage Roles` permission!')
            else:
                toadd = None
                if args[2].startswith('<@&'):
                    toadd = message.guild.get_role(int(args[2][3:][:-1]))
                else:
                    for i in message.guild.roles:
                        if str(i.name).lower()==msg[int(len(args[0])+len(args[1])+2):]:
                            toadd = message.guild.get_role(i.id)
                            break
                try:
                    if toadd==None:
                        raise ValueError('Invalid input, NERD!')
                    aruser = message.mentions[0]
                    await aruser.add_roles(toadd)
                    await message.channel.send('Congratulations, '+aruser.name+', you now have the '+toadd.name+' role! :tada:')
                except Exception as e:
                    await message.channel.send(str(client.get_emoji(BotEmotes.error)) + f' | An error occured. :x:```{str(e)}```')
        if msg.startswith(prefix+'xpbox'):
            results = []
            buttons = []
            ques = [
                'Please input the box title.',
                'Please input the message to display.',
                'How many buttons shall be in the message box?'
            ]
            auth = message.author
            accept = True
            for i in range(0, 3):
                await message.channel.send(ques[i])
                def check(m):
                    return m.author == auth
                try:
                    trying = await client.wait_for('message', check=check, timeout=30.0)
                except:
                    await message.channel.send('Command canceled. No response after 30 seconds.')
                if '/' in str(trying.content) or '?' in str(trying.content) or '&' in str(trying.content):
                    await message.channel.send(str(client.get_emoji(BotEmotes.error)) +' | Your request contain an invalid symbol. Please try again.')
                    accept = False
                    break
                else:
                    results.append(str(trying.content))
                    if len(results)>2:
                        for i in range(1, results[3]+1):
                            nds = ['st', 'nd', 'rd']
                            await message.channel.send('Please input the '+str(i)+str(nds[i-1])+' button.')
                            def checkingagain(m):
                                return m.author == auth
                            try:
                                buttonInput = await client.wait_for('message', check=checkingagain, timeout=30.0)
                            except:
                                await message.channel.send('Command canceled. No response after 30 seconds.')
                                accept = False
                                break
                            buttons.append(str(trying.content))
            if accept==True:
                embed = discord.Embed(title='Error!', colour=discord.Colour.red())
                embed.set_image(url='http://atom.smasher.org/error/xp.png.php?icon=Error3&style=xp&title='+str(results[0]).replace(' ', '+')+'&text='+str(results[1]).replace(' ', '+')+'&b1='+str(results[2]).replace(' ', '+'))
                await message.channel.send(embed=embed)
        if msg.startswith(prefix+'removerole') or args[0]==prefix+'rr':
            if message.author.guild_permissions.manage_roles==False:
                await message.channel.send(str(client.get_emoji(BotEmotes.error)) +f' | <@{str(message.author.id)}>, you don\'t have the `Manage Roles` permission!')
            else:
                aruser = message.mentions[0]
                toadd = None
                if args[2].startswith('<@&'):
                    toadd = message.guild.get_role(int(args[2][3:][:-1]))
                else:
                    for i in message.guild.roles:
                        if str(i.name).lower()==msg[int(len(args[0])+len(args[1])+2):]:
                            toadd = message.guild.get_role(i.id)
                            break
                try:
                    if toadd==None:
                        raise ValueError('Invalid input, NERD!')
                    await aruser.remove_roles(toadd)
                    await message.channel.send(aruser.name+', you lost the '+toadd.name+' role. :pensive:')
                except Exception as e:
                    await message.channel.send(f'An error occured. :x: ```{e}```')
        if msg.startswith(prefix+'permission') or msg.startswith('perms'):
            if len(args)!=2:
                await message.channel.send(str(client.get_emoji(BotEmotes.error)) +' | Please mention someone!\nExample:\n'+prefix+'permissions <@'+str(message.author.id)+'>')
            else:
                member = message.mentions[0]
                perm = ''
                permCheck = [member.guild_permissions.manage_guild, member.guild_permissions.kick_members, member.guild_permissions.ban_members, member.guild_permissions.administrator, member.guild_permissions.change_nickname, member.guild_permissions.manage_nicknames, member.guild_permissions.manage_channels, member.guild_permissions.view_audit_log, member.guild_permissions.manage_messages]
                permString = ['Manage Server', 'Kick Members', 'Ban Members', 'Admin', 'Change their Nickname', 'Manage member\'s nicknames', 'Manage Channels', 'View Audit Log', 'Manage Messages']
                for i in range(0, int(len(permString))):
                    if permCheck[i]==True:
                        perm += ':white_check_mark: '+str(permString[i])+'\n'
                    else:
                        perm += ':x: '+str(permString[i])+'\n'
                try:
                    permissionsEmbed = discord.Embed(title='User permissions for '+str(message.mentions[0].name)+';', description=str(perm), colour=discord.Colour.blue())
                    await message.channel.send(embed=permissionsEmbed)
                except Exception as e:
                    await message.channel.send(str(client.get_emoji(BotEmotes.error)) +' | elol. we have an elol here:```'+str(e)+'```')
        if msg.startswith(prefix+'makechannel'):
            if message.author.guild_permissions.manage_channels==False:
                await message.channel.send(str(client.get_emoji(BotEmotes.error)) +' | You don\'t have the permission `Manage Channel`. Which is required.')
                acceptId = 1
            else:
                acceptId = 0
            if acceptId==0:
                trashCrap = ['text', 'voice']
                if len(args)<3:
                    await message.channel.send(str(client.get_emoji(BotEmotes.error)) +' | Invalid arguments.')
                elif args[1] not in trashCrap:
                    await message.channel.send(str(client.get_emoji(BotEmotes.error)) +' | Invalid type. Please add `text` or `voice`.')
                elif args[1]=='text':
                    try:
                        await message.guild.create_text_channel(msg[int(len(args[0])+len(args[1])+2):].replace(' ', '-'))
                        await message.channel.send(':white_check_mark: Done! Created a text channel: '+str(msg[int(len(args[0])+len(args[1])+2):]))
                    except:
                        await message.channel.send(str(client.get_emoji(BotEmotes.error)) + ' | Oops! It seemed that we have a problem creating a text channel. :(')
                elif args[1]=='voice':
                    await message.guild.create_voice_channel(msg[int(len(args[0])+len(args[1])+2):])
                    await message.channel.send(':white_check_mark: Done! Created a voice channel: '+str(msg[int(len(args[0])+len(args[1])+2):]))
                else:
                    await message.channel.send(str(client.get_emoji(BotEmotes.error)) + ' | error. (not 404)')
        if msg.startswith(prefix+'kick'):
            if no_args:
                await message.channel.send(str(client.get_emoji(BotEmotes.error)) +' | Please mention someone!!1!11')
            else:
                if args[1].startswith('<@!'):
                    idiot = message.guild.get_member(int(args[1][3:][:-1]))
                else:
                    idiot = message.guild.get_member(int(args[1][2:][:-1]))
                misterKicker = message.guild.get_member(int(message.author.id))
                if misterKicker.guild_permissions.kick_members==False:
                    await message.channel.send(str(client.get_emoji(BotEmotes.error)) +' | You cannot kick '+str(idiot.name)+', because you don\'t even have the `Kick Members` permission!')
                    acceptId = 1
                elif idiot.guild_permissions.administrator==True or idiot.guild_permissions.manage_guild==True:
                    await message.channel.send(str(client.get_emoji(BotEmotes.error)) +' | **You want me to kick an mod/admin?!**\nCome on, you gotta be kidding me.')
                    acceptId = 1
                elif idiot.id==message.author.id:
                    await message.channel.send(str(client.get_emoji(BotEmotes.error)) +' | Don\'t be a weirdo, kicking urself. If you want, just leave the server! That\'s easy! :grinning:')
                    acceptId = 1
                else:
                    acceptId = 0
                if acceptId==0:
                    msgs = [
                        'Sayonara, '+idiot.name,
                        'Mr.Kicker kicked '+idiot.name+'!',
                        'F\'s in the chat for '+idiot.name+', because he got kicked.',
                        'Heh, bye-bye '+idiot.name+'! lul',
                        'Game over, '+idiot.name+'.',
                        'It\'s time to stop, '+idiot.name+'.'
                    ]
                    if len(args)==2:
                        reas = 'Unspecified by kicker.'
                    else:
                        reas = msg[int(len(args[1])+len(args[0])+2):]
                    await message.guild.kick(idiot, reason=str(reas))
                    await message.channel.send(str(client.get_emoji(BotEmotes.success)) + ' | ' +random.choice(msgs))
                else:
                    await message.channel.send(str(client.get_emoji(BotEmotes.error)) +' | Kick declined by myself.')
        if msg.startswith(prefix+'nick'):
            acceptId = 0
            if no_args:
                await message.channel.send('Where\'s da paramaters!?!')
                acceptId = 1
            else:
                if args[1].startswith('<@') and args[1].endswith('>'):
                    try:
                        if args[1].startswith('<@!'):
                            changethem = message.guild.get_member(int(args[1][3:][:-1]))
                        else:
                            changethem = message.guild.get_member(int(args[1][2:][:-1]))
                    except ValueError:
                        await message.channel.send(str(client.get_emoji(BotEmotes.error)) + ' | Error with the tag. :x: :(')
                        acceptId = 1
                    finally:
                        if message.author.guild_permissions.manage_nicknames==False:
                            await message.channel.send(str(client.get_emoji(BotEmotes.error)) +' | You need the `Manage Nicknames` permissions to do this command.')
                            acceptId = 1
                else:
                    changethem = message.guild.get_member(int(message.author.id))
                    if changethem.guild_permissions.change_nickname==False:
                        acceptId = 1
                        await message.channel.send(str(client.get_emoji(BotEmotes.error)) +' | You need the `Change Nickname` permission to change your, nickname, DUH')
                if acceptId==0:
                    newnick = message.content[int(len(args[1])+len(args[0])+2):]
                    try:
                        await changethem.edit(nick=newnick)
                        await message.channel.send('Change the '+changethem.name+'\'s nickname to `'+str(newnick)+'`. Nice name!')
                    except:
                        await message.channel.send(str(client.get_emoji(BotEmotes.error)) +' | So umm, i wanted to change their nickname and...\nDiscord says: `Missing Permissions`\nMe and '+str(message.author.name)+': :neutral_face:')
        if msg.startswith(prefix+'imdb'):
            wait = await message.channel.send(str(client.get_emoji(BotEmotes.loading)) + ' | Please wait...')
            if no_args or args[1]=='help' or args[1]=='--help':
                embed = discord.Embed(title='IMDb command help', description='Searches through the IMDb Movie database.\n{} are Parameters that is **REQUIRED** to get the info.\n\n', colour=discord.Colour.red())
                embed.add_field(name='Commands', value=prefix+'imdb --top {NUMBER}\n'+prefix+'imdb --search {TYPE} {QUERY}\n'+prefix+'imdb help\n'+prefix+'imdb --movie {MOVIE_ID or MOVIE_NAME}', inline='False')
                embed.add_field(name='Help', value='*{TYPE} could be "movie", "person", or "company".\n{QUERY} is the movie/person/company name.\n{MOVIE_ID} can be got from the search. Example: `'+prefix+'imdb --search movie Inception`.', inline='False')
                await wait.edit(content='', embed=embed)
            if args[1]=='--top':
                if len(args)==2:
                    await wait.edit(content='Please type the number!\nex: --top 5, --top 10, etc.')
                else:
                    num = args[2]
                    try:
                        if int(num)>30:
                            await wait.edit(content='That\'s too many movies to be listed!')
                        else:
                            arr = ia.get_top250_movies()
                            total = ''
                            for i in range(0, int(num)):
                                total = total + str(int(i)+1) + '. '+str(arr[i]['title'])+' (`'+str(arr[i].movieID)+'`)\n'
                            embed = discord.Embed(title='IMDb Top '+str(num)+':', description=str(total), colour=discord.Colour.red())
                            await wait.edit(content='', embed=embed)
                    except ValueError:
                        await wait.edit(content=str(client.get_emoji(BotEmotes.error)) +' | Is the top thing you inputted REALLY a number?\nlike, Not top TEN, but top 10.\nGET IT?')
            if args[1]=='--movie':
                if args[1]=='--movie' and len(args)==2:
                    await wait.edit(content='Where\'s the ID?!?!?!')
                else:
                    if args[2].isnumeric()==True:
                        movieId = args[2]
                        theID = str(movieId)
                    else:
                        movieId = ia.search_movie(msg[int(len(args[0])+len(args[1])+2):])[0].movieID
                        theID = str(movieId)
                    data = ia.get_movie(str(movieId))
                try:
                    embed = discord.Embed(title=data['title'], colour=discord.Colour.red())
                    await wait.edit(content=str(client.get_emoji(BotEmotes.loading)) + ' | Please wait... Retrieving data...')
                    emoteStar = ''
                    for i in range(0, round(int(ia.get_movie_main(theID)['data']['rating']))):
                        emoteStar = emoteStar + ' :star:'
                    upload_date = ia.get_movie_release_info(str(theID))['data']['raw release dates'][0]['date']
                    imdb_url = ia.get_imdbURL(data)
                    await wait.edit(content=str(client.get_emoji(BotEmotes.loading)) + ' | Please wait... Creating result...')
                    embed.add_field(name='General Information', value=f'**IMDb URL: **{imdb_url}\n**Upload date: **{upload_date}\n**Written by: **'+ia.get_movie_main(str(theID))['data']['writer'][0]['name']+'\n**Directed by: **'+ia.get_movie_main(str(theID))['data']['director'][0]['name'])
                    embed.add_field(name='Ratings', value=emoteStar+'\n**Overall rating: **'+str(ia.get_movie_main(str(theID))['data']['rating'])+'\n**Rated by '+str(ia.get_movie_main(str(theID))['data']['votes'])+' people**')
                    embed.set_image(url=ia.get_movie_main(str(theID))['data']['cover url'])
                    await wait.edit(content='', embed=embed)
                except KeyError:
                    await wait.edit(content=str(client.get_emoji(BotEmotes.error)) + ' | An error occured!\n**Good news, we *may* fix it.**')
                    errorQuick = discord.Embed(title=data['title'], colour=discord.Colour.red())
                    errorQuick.add_field(name='General Information', value=f'**IMDb URL: **{imdb_url}\n**Upload date: **{upload_date}')
                    errorQuick.add_field(name='Ratings', value=emoteStar+'\n**Overall rating: **'+str(ia.get_movie_main(str(theID))['data']['rating'])+'\n**Rated by '+str(ia.get_movie_main(str(theID))['data']['votes'])+' people**')
                    errorQuick.set_footer(text='Information given is limited due to Errors and... stuff.')
                    await wait.edit(content='', embed=errorQuick)
            if args[1]=='--search':
                query = len(args[0])+len(args[1])+len(args[2])+3
                query = msg[query:]
                lists = ''
                if args[2].startswith('movie') or args[2].startswith('film'):
                    main_name = 'MOVIE'
                    movies = ia.search_movie(query)
                    for i in range(0, int(len(movies))):
                        if len(lists)>1950:
                            break
                        lists = lists + str(int(i)+1) +'. '+ str(movies[i]['title'])+ ' (`'+str(movies[i].movieID)+'`)\n'
                elif args[2].startswith('company'):
                    main_name = 'COMPANY'
                    companies = ia.search_company(query)
                    for i in range(0, int(len(companies))):
                        if len(lists)>1950:
                            break
                        lists = lists + str(int(i)+1) + '. '+str(companies[i]['name']) + ' (`'+str(companies[i].companyID)+'`)\n'
                elif args[2].startswith('person'):
                    main_name = 'PERSON'
                    persons = ia.search_person(query)
                    for i in range(0, int(len(persons))):
                        if len(lists)>1950:
                            break
                        lists = lists + str(int(i)+1) + '. '+str(persons[i]['name']) + ' (`'+str(persons[i].personID)+'`)\n'
                embed = discord.Embed(title=main_name.lower()+' search for "'+str(query)+'":', description=str(lists), colour=discord.Colour.red())
                if main_name=='MOVIE':
                    embed.set_footer(text='Type '+prefix+'imdb --'+str(main_name.lower())+' {'+main_name+'_ID} to show each info.')
                await wait.edit(content='', embed=embed)
        if msg.startswith(prefix+'dogfact'):
            fact = myself.api('https://dog-api.kinduff.com/api/facts')
            if fact['success']!=True:
                desc = str(client.get_emoji(BotEmotes.error)) + ' | Error getting the fact.'
            else:
                desc = fact['facts'][0]
            embed = discord.Embed(title='Did you know?',description=str(desc))
            await message.channel.send(embed=embed)
        if msg.startswith(prefix+'roleinfo'):
            if len(args)>1:
                data = None
                if args[1].startswith('<@&'):
                    await message.delete()
                    data = message.guild.get_role(int(args[1][3:][:-1]))
                else:
                    for i in message.guild.roles:
                        if str(i.name).lower()==str(unprefixed).lower():
                            data = message.guild.get_role(i.id)
                            break
                if data==None:
                    await message.channel.send(str(client.get_emoji(BotEmotes.error)) +' | Your input seemed to be invalid. Please try again.')
                else:
                    if data.permissions.administrator==True:
                        perm = ':white_check_mark: Server Administrator'
                    else:
                        perm = ':x: Server Administrator'
                    if data.mentionable==True:
                        men = ':warning: You can mention this role and they can get pinged.'
                    else:
                        men = ':v: You can mention this role and they will not get pinged! ;)'
                    embedrole = discord.Embed(title='Role info for role: '+str(data.name), description='**Role ID: **'+str(data.id)+'\n**Role created at: **'+str(data.created_at)[:-7]+' UTC\n**Role position: **'+str(data.position)+'\n**Members having this role: **'+str(len(data.members))+'\n'+str(men)+'\nPermissions Value: '+str(data.permissions.value)+'\n'+str(perm), colour=data.colour)
                    embedrole.add_field(name='Role Colour', value='**Color hex: **#'+str(myself.tohex(data.color.value))+'\n**Color integer: **'+str(data.color.value)+'\n**Color RGB: **'+str(myself.dearray(list(data.color.to_rgb()))))
                    await message.channel.send(embed=embedrole)
        if args[0]==prefix+'food' or args[0]==prefix+'coffee':
            data = myself.insp('https://nekobot.xyz/api/image?type='+str(args[0][1:]))
            link = data.split('"message":"')[1].split('"')[0]
            if args[0].endswith('food'):
                col = int(data.split('"color":')[1].split(',')[0])
                msgtitle = 'hungry?'
            elif args[0].endswith('coffee'):
                col = int(data.split('"color":')[1][:-1])
                msgtitle = 'get caffeinated uwu'
                num = random.randint(0, 1)
                if num==0:
                    link = myself.jsonisp('https://coffee.alexflipnote.dev/random.json')['file']
            embed = discord.Embed(title=msgtitle, colour=discord.Color(col))
            embed.set_image(url=link.replace('\/', '/'))
            await message.channel.send(embed=embed)
        if msg.startswith(prefix+'fox'):
            img = myself.insp('https://randomfox.ca/floof/?ref=apilist.fun').split('"image":"')[1].split('"')[0].replace('\/', '/')
            embed = discord.Embed(colour=discord.Colour.red())
            embed.set_image(url=img)
            await message.channel.send(embed=embed)
        if msg.startswith(prefix+'newemote'):
            data = myself.api('https://discordemoji.com/')
            byEmote = data.split('<div class="float-right"><a href="')
            del byEmote[0]
            alls = []
            for i in range(0, len(byEmote)):
                if byEmote[i].startswith('http'):
                    alls.append(byEmote[i].split('"')[0])
            embed = discord.Embed(colour=discord.Colour.blue())
            embed.set_image(url=random.choice(alls))
            await message.channel.send(embed=embed)
        if msg.startswith(prefix+'steamprofile'):
            getprof = myself.urlify(unprefixed)
            data = myself.insp('https://api.alexflipnote.dev/steam/user/'+str(getprof))
            if '<title>404 Not Found</title>' in data:
                await message.channel.send(str(client.get_emoji(BotEmotes.error)) + ' | Error **404**! `not found...`')
            else:
                steam_id = data.split('"steamid64":')[1].split(',')[0][1:]
                custom_url = data.split('"customurl":')[1].split('},')[0][1:]
                avatar = data.split('"avatarfull": "')[1].split('"')[0]
                username = data.split('"username": "')[1].split('"')[0]
                url = data.split('"url": "')[1].split('"')[0]
                state = data.split('"state": "')[1].split('"')[0]
                privacy = data.split('"privacy": "')[1].split('"')[0]
                if state=='Offline':
                    embedColor = discord.Colour.dark_blue()
                else:
                    embedColor = discord.Colour.red()
                embed = discord.Embed(title=username, description='**[Profile Link]('+str(url)+')**\n**Current state: **'+str(state)+'\n**Privacy: **'+str(privacy)+'\n**[Profile pic URL]('+str(avatar)+')**', colour = embedColor)
                embed.set_thumbnail(url=avatar)
                await message.channel.send(embed=embed)
        if msg.startswith(prefix+'salty'):
            if len(args)!=2:
                await message.channel.send(str(client.get_emoji(BotEmotes.error)) + ' | Error! Invalid args.')
            else:
                av = message.mentions[0].avatar_url
                embed = discord.Embed(colour=discord.Colour.magenta())
                embed.set_image(url='https://api.alexflipnote.dev/salty?image='+str(av))
                await message.channel.send(embed=embed)
        if msg.startswith(prefix+'woosh') or msg.startswith(prefix+'wooosh') or msg.startswith(prefix+'woooosh'):
            if len(args)!=2:
                await message.channel.send(str(client.get_emoji(BotEmotes.error)) + ' | Error! Invalid args.')
            else:
                av = message.mentions[0].avatar_url
                embed = discord.Embed(colour=discord.Colour.magenta())
                embed.set_image(url='https://api.alexflipnote.dev/jokeoverhead?image='+str(av))
                await message.channel.send(embed=embed)
        if msg.startswith(prefix+'funfact'):
            wait = await message.channel.send(str(client.get_emoji(BotEmotes.loading)) + ' | Please wait...')
            data = myself.insp('https://bestlPlease waitifeonline.com/random-fun-facts/')
            byFact = data.split('<div class="title ">')
            accepted = False
            facts = []
            for a in byFact:
                if a.split('</div')[0].startswith('Superman'):
                    accepted = True
                if accepted==True:
                    facts.append(a.split('</div>')[0])
                else:
                    continue
            await wait.edit(content='Did you know?\n**'+str(random.choice(facts))+'**')
        if msg.startswith(prefix+'supreme'):
            text = myself.urlify(message.content[9:])
            embed = discord.Embed(colour=discord.Colour.magenta())
            embed.set_image(url='https://api.alexflipnote.dev/supreme?text='+str(text))
            await message.channel.send(embed=embed)
        if msg.startswith(prefix+'googledoodle'):
            wait = await message.channel.send(str(client.get_emoji(BotEmotes.loading)) + ' | Please wait... This may take a few moments...')
            data = myself.insp('https://google.com/doodles')
            byLatest = data.split('<li class="latest-doodle ">')
            del byLatest[0]
            byTag = ''.join(byLatest).split('<')
            doodle_link = 'https://google.com'+str(byTag[3][8:].split('"\n')[0])
            doodle_img = 'https:'+str(byTag[4][9:].split('" alt="')[0])
            doodle_name = doodle_link[27:].replace('-', ' ')
            embed = discord.Embed(title=doodle_name, description=doodle_link, colour=discord.Colour.blue())
            embed.set_image(url=doodle_img)
            await wait.edit(content='', embed=embed)
        if msg.startswith(prefix+'createbot'):
            if no_args:
                tutorials = f'{prefix}createbot --started `Getting started, preparing stuff.`\n{prefix}createbot --say `Say command help.`\n{prefix}createbot --ping `Ping command help. (Client latency).`\n{prefix}createbot --coin `Flip coin game`\n{prefix}createbot --embed `Creating embeds`\n{prefix}createbot --avatar `Avatar commands help.`'
                embed = discord.Embed(title='Createbot; the discord.py bot tutorial', description=f'This is a tutorial on how to create a discord bot.\nEvery thing other than `--started` needs to have the same module or string.\nEach are args on different categories.\n\n{tutorials}', colour=discord.Colour.red())
                await message.channel.send(embed=embed)
            elif args[1]=='--avatar':
                await message.channel.send('```py\nif msg.startswith(\f\'{prefix}avatar\'):\n\tembed = discord.Embed(colour=discord.Colour.magenta())\n\tembed.set_image(url=message.guild.get_member(int(msg.split()[1][2:][:-1])).avatar_url)\n\tawait message.channel.send(embed=embed)```')
            elif args[1]=='--embed':
                await message.channel.send('Embed example: ```py\nif message.channel.send(f\'{prefix}embedthing\'):\n\tembed = discord.Embed(\n\t\ttitle = \'My embed title\',\n\t\tdescription = \'The embed description and stuff. Lorem ipsum asdf\',\n\t\tcolour = discord.Colour.blue()\n\tembed.add_field(name=\'Field name\', value=\'embed field value is here\', inline=\'True\')\n\tembed.set_footer(text=\'this is a footer\')\n\tawait message.channel.send(embed=embed)```')
            elif args[1]=='--coin':
                await message.channel.send('Requires: `Random module`\nType the following at the first line of your code;```py\nimport random```Then type the if statement:```py\nif msg.startswith(f\'{prefix}coinflip\'):\n\tawait message.channel.send(random.choice([\'HEADS!\', \'TAILS!\']))```')
            elif args[1]=='--ping':
                await message.channel.send('```py\nif msg.startswith(f\'{prefix}ping\'):\n\tawait message.channel.send(\'**Pong!**\\n\'+str(round(client.latency*1000))+\' ms.\')```')
            elif args[1]=='--say':
                await message.channel.send('```py\nif msg.startswith(f\'{prefix}say\'):\n\tawait message.channel.send(msg[int(len(msg.split()[0])+1):])```')
            elif args[1]=='--started':
                embed = discord.Embed(
                    title='How to create a discord BOT with Discord.py',
                    description='This is how you make a BOT using Discord.py\nAccording to the dev! ;)',
                    colour = discord.Colour.dark_blue()
                )
                code = 'import discord\ntoken = \'YOUR TOKEN\'\nclient = discord.Client()\n@client.event\nasync def on_ready():\n\tprint(\'Bot is ready!\')\n@client.event\nasync def on_message(message):\n\tmsg = message.content.lower()\n\tprefix = \'your prefix\'\n\tif msg.startswith(prefix+\'command thing\'):\n\t\tawait message.channel.send(\'Message your bot responds with\')\nclient.run(token)'
                embed.add_field(name='A. Preparing stuff', value='1. Install python through http://python.org/downloads \n2. Learn Python programming language first\n3. Open your console, and type \'pip install discord.py\'\n4.Have some text editor (notepad++/VScode/Sublime Text)', inline='False')
                embed.add_field(name='B. Bot Setup', value='1. Go to http://discordapp.com/developers \n2. Click on \'New Application.\'\n3. Type your bot name and click \'Create\'.\n4. Click on \'bot\' tab, and Click \'Add bot.\'\n5. Click \'Yes, do it!\'\n6. If your name is not approved, please change the bot name in the \'General Information Tab.\' Else, congrats!', inline='False')
                embed.add_field(name='C. Invite the bot to your server', value='1. On the \'Oauth2\' Tab, scroll down and on the scopes list, check \'Bot\'.\n2. Check the bot permissions first.\n3. Click on COPY.\n4. Open that link on your browser.\n5. Authorize the bot to your server.\n6. Boom! Your bot joined your server!', inline='False')
                embed.add_field(name='D. Coding time!', value='1. Create a folder.\n2. Open that folder and create a file named \'bot.py\' in .py extension.\n3. Open that file with a text editor.\n4. Code the following above.\n', inline='False')
                embed.add_field(name='E. How to get the Token?', value='1. Open the http://discordapp.com/developers, and click on your bot.\n2. Open the \'Bot\' tab.\n3. On token, click \'Copy\'.\n4. Change the \'YOUR TOKEN\' above by pasting your token.\n5. DON\'T SHARE YOUR TOKEN WITH ANYBODY.', inline='False')
                embed.add_field(name='F. Discord API?', value='https://discordpy.readthedocs.io/en/latest/api.html', inline='False')
                embed.set_footer(text='Enjoy your BOT! ;)')
                await message.channel.send(embed=embed, content='```py\n'+str(code)+'```')
        if msg.startswith(prefix+'channels'):
            channels = ''
            warning = 'No errors found.'
            for i in range(0, int(len(message.guild.text_channels))):
                if len(channels)>2048:
                    warning = str(client.get_emoji(BotEmotes.error)) + ' | Error: Too many channels, some channels may be not listed.'
                channels = channels +'<#'+ str(message.guild.text_channels[i].id) + '> \n'
            embed = discord.Embed(title=message.guild.name+'\'s Text channels:', description=str(channels), inline='True')
            embed.set_footer(text=str(warning))
            await message.channel.send(embed=embed)
        if msg.startswith(prefix+'slot'):
            win = False
            jackpot = False
            slots = []
            for i in range(0, 3):
                newslot = discordgames.slot()
                if newslot[1]==newslot[2] and newslot[1]==newslot[3] and newslot[2]==newslot[3]:
                    win = True
                    if newslot[1]==':flushed:':
                        jackpot = True
                slots.append(discordgames.slotify(newslot))
            if win:
                msgslot = 'You win!'
                col = discord.Colour.blue()
                if jackpot:
                    msgslot = 'JACKPOT!'
                    col = discord.Colour.green()
            else:
                msgslot = 'You lose... Try again!'
                col = discord.Colour.red()
            embed = discord.Embed(title=msgslot, description=slots[0]+'\n\n'+slots[1]+'\n\n'+slots[2], colour=col)
            await message.channel.send(embed=embed)
        if msg.startswith(prefix+'rolecolor'):
            if no_args:
                res = ''
                exc = 0
                for i in range(0, len(message.guild.roles)):
                    if myself.tohex(message.guild.roles[i].color.value)=='0':
                        exc += 1
                        continue
                    if len(res)>1950:
                        break
                    res += '<@&'+str(message.guild.roles[i].id)+'> #'+str(myself.tohex(message.guild.roles[i].color.value))+'\n'
                embed = discord.Embed(title='Server role colors OwO', description=res, colour=discord.Colour.blue())
                embed.set_footer(text=f'This excludes normal default color roles. ({str(exc)})\nTIP: try {prefix}rolecolor [role name] [#hex]*\n*make sure the hex starts with #!')
                await message.channel.send(embed=embed)
            else:
                if len(unprefixed.split('#'))==1:
                    await message.channel.send(f'Please provide a hex!\nExample: {prefix}rolecolor {random.choice(message.guild.roles).name} #ff0000')
                else:
                    if message.author.guild_permissions.manage_roles==False:
                        await message.channel.send(str(client.get_emoji(BotEmotes.error)) +' | You need the `MANAGE ROLES` permission to change role colors!')
                    else:
                        role = None
                        for i in message.guild.roles:
                            if unprefixed.split('#')[0][:-1].lower()==str(i.name).lower():
                                role = i
                                break
                        if role==None:
                            await message.channel.send(str(client.get_emoji(BotEmotes.error)) +' | Invalid role input! :(')
                        else:
                            try:
                                colint = myself.toint(unprefixed.split('#')[1].lower())
                                await role.edit(colour=discord.Colour(colint))
                                await message.channel.send('Color of '+role.name+' role has been changed.', delete_after=10)
                            except Exception as e:
                                await message.channel.send(str(client.get_emoji(BotEmotes.error)) + f' | An error occured while editing role:```{e}```')
        if msg.startswith(prefix+'isprime'):
            if int(args[1])<999999:
                numsArray = range(2, int(args[1]))
                id = 0
                canBeDividedBy = []
                for k in range(0, int(len(numsArray))):
                    if int(args[1])%numsArray[k]==0:
                        id = 1
                        canBeDividedBy.append(str(numsArray[k]))
                if id==0:
                    await message.channel.send("YES. "+str(args[1])+" is a prime number.")
                else:
                    await message.channel.send("NO. "+str(args[1])+" can be divided by "+str(myself.dearray(canBeDividedBy))+".")
            else:
                await message.channel.send(str(client.get_emoji(BotEmotes.error)) + ' | OverloadInputError: Beyond the limit of 999999')
        if msg.startswith(prefix+'jpeg') or msg.startswith(prefix+'invert') or msg.startswith(prefix+'magik')or msg.startswith(prefix+'pixelate')or msg.startswith(prefix+'b&w'):
            if args[0][1:]=='jpeg':
                com = 'jpegify'
            elif args[0][1:]=='invert':
                com = 'invert'
            elif args[0][1:]=='magik':
                com = 'magik'
            elif args[0][1:]=='pixelate':
                com = 'pixelate'
            elif args[0][1:]=='b&w':
                com = 'b&w'
            if len(args)!=2:
                await message.channel.send('Please tag someone!')
            else:
                av = message.mentions[0].avatar_url
                embed = discord.Embed(colour=discord.Colour.magenta())
                embed.set_image(url='https://api.alexflipnote.dev/filter/'+str(com)+'?image='+str(av).replace('webp', 'png'))
                await message.channel.send(embed=embed)
        if msg.startswith(prefix+'drake'):
            if args[1]=='help':
                embed = discord.Embed(
                    title='Drake meme helper help',
                    description='Type the following:\n`'+str(prefix)+'drake [text1] [text2]`\n\nFor example:\n`'+str(prefix)+'drake [doing it yourself] [getting the help]`'
                )
                embed.set_image(url='https://api.alexflipnote.dev/drake?top=doing%20it%20yourself&bottom=getting%20the%20help')
                await message.channel.send(embed=embed)
            else:
                txt1 = myself.urlify(msg[5:].split('[')[1][:-2])
                txt2 = myself.urlify(msg[5:].split('[')[2][:-1])
                embed = discord.Embed(colour=discord.Colour.blue())
                embed.set_image(url='https://api.alexflipnote.dev/drake?top='+str(txt1)+'&bottom='+str(txt2))
                print('https://api.alexflipnote.dev/drake?top='+str(txt1)+'&bottom='+str(txt2))
                await message.channel.send(embed=embed)
        if msg.startswith(prefix+'ascii'):
            if no_args:
                await message.channel.send(str(client.get_emoji(BotEmotes.error)) +' | Invalid. Please send a word or something.')
            else:
                if '--randomfont' not in msg:
                    query = myself.urlify(str(unprefixed))
                    word = myself.insp("http://artii.herokuapp.com/make?text="+query.replace('--randomfont', ''))
                else:
                    fonts = splashes.getAsciiFonts()
                    query = myself.urlify(str(unprefixed))
                    query = query.replace('--randomfont ', '')
                    word = myself.insp("http://artii.herokuapp.com/make?text="+query.replace('--randomfont', '')+'&font='+random.choice(fonts))
                if len(word)>1900:
                    await message.channel.send('The word is too long to be displayed!')
                else:
                    embed = discord.Embed(
                        description=f'```{word}```',
                        colour=discord.Colour.red()
                    )
                    embed.set_footer(text='Type --randomfont for umm.. random font to be generated.')
                    await message.channel.send(embed=embed)
        if msg.startswith(prefix+'typingtest'):
            wait = await message.channel.send(str(client.get_emoji(BotEmotes.loading)) + ' | Please wait...')
            data = myself.api("https://random-word-api.herokuapp.com/word?number=10")
            text = myself.arrspace(data)
            guy = message.author
            first = datetime.datetime.now()
            main = await message.channel.send('Please type the following:\n`'+str(text)+'`')
            def check(m):
                return m.author == guy
            try:
                trying = await client.wait_for('message', check=check, timeout=60.0)
            except:
                await main.edit(content='Time is up.')
            if str(trying.content).lower()==text.lower():
                await message.channel.send(str(client.get_emoji(BotEmotes.success)) +' | Correct!\nYour time: **'+str(datetime.datetime.now()-first)[:-7]+'**')
            else:
                await message.channel.send(str(client.get_emoji(BotEmotes.error)) +' | Did you do a typo or something?\nYour time: **'+str(datetime.datetime.now()-first)[:-7]+'**')
        if msg.startswith(prefix+'defuse') or msg.startswith(prefix+'bomb'):
            def embedType(a):
                if a==1:
                    return discord.Embed(title='The bomb exploded!', description='Game OVER!', colour=discord.Colour(000))
                elif a==2:
                    return discord.Embed(title='The bomb defused!', description='Congratulations! :grinning:', colour=discord.Colour.green())
            embed = discord.Embed(title='DEFUSE THE BOMB!', description='**Cut the correct wire!\nThe bomb will explode in 15 seconds!**', colour=discord.Colour.red())
            main = await message.channel.send(embed=embed)
            buttons = ['🔴', '🟡', '🔵', '🟢']
            for i in range(0, len(buttons)):
                await main.add_reaction(buttons[i])
            correct = random.choice(buttons)

            def check(reaction, user):
                return user == message.author

            try:
                reaction, user = await client.wait_for('reaction_add', timeout=15.0, check=check)
            except asyncio.TimeoutError:
                await main.edit(content='', embed=embedType(1))
            if str(reaction.emoji)!=correct:
                await main.edit(content='', embed=embedType(1))
            else:
                await main.edit(content='', embed=embedType(2))
        if msg.startswith(prefix+'userinfo'):
            acceptId = 0
            if acceptId==0:
                if no_args:
                    userid = int(message.author.id)
                    user = client.get_user(int(message.author.id))
                elif len(args)==2:
                    if len(message.mentions)>0:
                        userid = message.mentions[0].id
                        user = message.mentions[0]
                    else:
                        userid = message.author.id
                        user = message.author
                guy = message.guild.get_member(int(userid))
                if guy.status.name=='dnd':
                    status = 'do not disturb'
                else:
                    status = guy.status.name
                percentage = round(int(len(guy.roles))/int(len(message.guild.roles))*100)
                userrole = ''
                for i in range(0, int(len(guy.roles))):
                    if len(userrole)>899:
                        break
                    userrole +='<@&'+str(guy.roles[i].id)+'> '
                if user.bot==True:
                    thing = 'Bot'
                else:
                    thing = 'User'
                embed = discord.Embed(
                    title=user.name,
                    colour = guy.colour
                )
                joinServer = guy.joined_at
                embed.add_field(name='General info.', value='**'+thing+' name: **'+str(user.name)+'\n**'+thing+' ID: **'+str(user.id)+'\n**Discriminator: **'+str(user.discriminator)+'\n**'+thing+' creation: **'+str(user.created_at)[:-7]+'\n**Status:** '+str(status)+'\n**Current activity: **'+str(message.guild.get_member(user.id).activity), inline='True')
                embed.add_field(name='Server specific', value='**'+thing+' nickname: **'+str(guy.display_name)+'\n**'+thing+' roles: **'+str(userrole)+'\nThis user owns '+str(percentage)+'% of all roles in this server.\n**Joined this server at: **'+str(joinServer)[:-7])
                embed.set_thumbnail(url=user.avatar_url)
                await message.channel.send(embed=embed)
        if msg.startswith(prefix+'wikipedia'):
            wait = await message.channel.send(str(client.get_emoji(BotEmotes.loading)) + ' | Please wait...')
            if no_args:
                await wait.edit(content='Please input a page name!')
            else:
                wikipedia = wikipediaapi.Wikipedia('en')
                page = wikipedia.page(msg[11:])
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
                    embed = discord.Embed(title=pageTitle, description=str(explain), colour=discord.Colour.blue())
                    embed.set_footer(text='Get more info at '+str(page.fullurl))
                    await wait.edit(content='', embed=embed)
        if msg.startswith(prefix+'getinvite'):
            if message.author.guild_permissions.create_invite==False:
                await message.channel.send(str(client.get_emoji(BotEmotes.error)) +' | You need to have the permission `Create Invite` to continue!')
            else:
                serverinvite = await message.channel.create_invite(reason='Requested by '+str(message.author.name))
                await message.channel.send('New invite created! Link: **'+str(serverinvite)+'**')
        if msg.startswith(prefix+'avatar'):
            try:
                if len(message.mentions)==0: user = message.author
                else: user = message.mentions[0]
                embed = discord.Embed(title=user.name+'\'s avatar', colour = discord.Colour.dark_blue())
                embed.set_image(url=str(user.avatar_url).replace('.webp', '.png'))
                await message.channel.send(embed=embed)
            except:
                await message.channel.send(str(client.get_emoji(BotEmotes.error)) +' | Invalid avatar.')
        if args[0]==prefix+'phcomment':
            if no_args:
                await message.channel.send(str(client.get_emoji(BotEmotes.error)) +f' | Invalid type.\nTry:\n`{prefix}phcomment [text]` or;\n`{prefix}phcomment [tag] [text]`')
            else:
                if len(message.mentions)==0:
                    text = unprefixed
                    embed = discord.Embed(colour=discord.Colour.green())
                    embed.set_image(url='https://nekobot.xyz/api/imagegen?type=phcomment&username='+myself.urlify(str(message.author.name))+'&text='+myself.urlify(str(text))+'&image='+str(message.author.avatar_url).replace('.webp?size=1024', '.png')+'&raw=1')
                else:
                    text = message.content[int(len(args[0])+len(args[1])+2):]
                    embed = discord.Embed(colour=discord.Colour.green())
                    embed.set_image(url='https://nekobot.xyz/api/imagegen?type=phcomment&username='+myself.urlify(str(message.mentions[0].name))+'&text='+myself.urlify(str(text))+'&image='+str(message.mentions[0].avatar_url).replace('.webp?size=1024', '.png')+'&raw=1')
                await message.channel.send(embed=embed)
        if args[0]==prefix+'ph':
            if args[1]=='help':
                embed = discord.Embed(title='ph command help', description='Type the following:\n'+prefix+'ph [txt1] [txt2]\n\nFor example:\n'+prefix+'ph [Git] [Hub]', colour=discord.Colour.red())
                embed.set_image(url='https://api.alexflipnote.dev/pornhub?text=Git&text2=Hub')
                await message.channel.send(embed=embed)
            elif '[' in msg:
                txt1 = myself.urlify(msg.split('[')[1][:-2])
                txt2 = myself.urlify(msg.split('[')[2][:-1])
                embed = discord.Embed(colour=discord.Colour.red())
                embed.set_image(url='https://api.alexflipnote.dev/pornhub?text='+str(txt1)+'&text2='+str(txt2))
                await message.channel.send(embed=embed)
        if msg.startswith(prefix+'steamapp'):
            if no_args:
                await message.channel.send('Please insert an app name.')
            else:
                data = myself.jsonisp('https://store.steampowered.com/api/storesearch?term='+myself.urlify(str(unprefixed))+'&cc=us&l=en')
                if data['total']==0:
                    await message.channel.send('Did not found anything. Maybe that app *doesn\'t exist...*')
                else:
                    try:
                        prize = data['items'][0]['price']['initial']
                        prize = str(prize / 100)+ ' ' + data['items'][0]['price']['currency']
                    except KeyError:
                        prize = 'FREE'
                    if data['items'][0]['metascore']=="":
                        rate = '???'
                    else:
                        rate = str(data['items'][0]['metascore'])
                    oss_raw = []
                    for i in range(0, len(data['items'][0]['platforms'])):
                        if data['items'][0]['platforms'][str(list(data['items'][0]['platforms'].keys())[i])]==True:
                            oss_raw.append(str(list(data['items'][0]['platforms'].keys())[i]))
                    embed = discord.Embed(title=data['items'][0]['name'], url='https://store.steampowered.com/'+str(data['items'][0]['type'])+'/'+str(data['items'][0]['id']), description='**Price tag:** '+str(prize)+'\n**Metascore: **'+str(rate)+'\n**This app supports the following OSs: **'+str(myself.dearray(oss_raw)), colour=discord.Colour.red())
                    embed.set_image(url=data['items'][0]['tiny_image'])
                    await message.channel.send(embed=embed)
        if msg.startswith(prefix+'stackoverflow') or msg.startswith(prefix+'sof'):
            if no_args:
                await message.channel.send('Hey fellow developer, Try add a question!')
            else:
                try:
                    query = myself.urlify(unprefixed)
                    data = myself.jsonisp("https://api.stackexchange.com/2.2/search/advanced?q="+str(query)+"&site=stackoverflow&page=1&answers=1&order=asc&sort=relevance")
                    leng = len(data['items'])
                    ques = data['items'][0]
                    tags = ''
                    for i in range(0, len(ques['tags'])):
                        if i==len(ques['tags'])-1:
                            tags += '['+str(ques['tags'][i])+'](https://stackoverflow.com/questions/tagged/'+str(ques['tags'][i])+')'
                            break
                        tags += '['+str(ques['tags'][i])+'](https://stackoverflow.com/questions/tagged/'+str(ques['tags'][i])+') | '
                    embed = discord.Embed(title=ques['title'], description='**'+str(ques['view_count'])+' *desperate* developers looked into this post.**\n**TAGS:** '+str(tags), url=ques['link'], colour=discord.Colour.green())
                    embed.set_author(name=ques['owner']['display_name'], url=ques['owner']['link'], icon_url=ques['owner']['profile_image'])
                    embed.set_footer(text='Shown 1 result out of '+str(leng)+' results!')
                    await message.channel.send(embed=embed)
                except:
                    await message.channel.send(str(client.get_emoji(BotEmotes.error)) + ' | There was an error on searching! Please check your spelling :eyes:')
        if msg.startswith(prefix+'translate'):
            wait = await message.channel.send(str(client.get_emoji(BotEmotes.loading)) + ' | Please wait...')
            if len(args)>1:
                if args[1]=='--list':
                    lang = ''
                    for bahasa in LANGUAGES:
                        lang = lang+str(bahasa)+' ('+str(LANGUAGES[bahasa])+')\n'
                    embed = discord.Embed(title='List of supported languages', description=str(lang), colour=discord.Colour.blue())
                    await wait.edit(content='', embed=embed)
                elif len(args)>2:
                    destination = args[1]
                    toTrans = msg[int(len(args[1])+len(args[0])+2):]
                    try:
                        trans = gtr.translate(toTrans, dest=args[1])
                        embed = discord.Embed(title=f'Translation', description=f'**{trans.text}**', colour=discord.Colour.blue())
                        embed.set_footer(text=f'Translated {LANGUAGES[trans.src]} to {LANGUAGES[trans.dest]}')
                        await wait.edit(content='', embed=embed)
                    except:
                        await wait.edit(content=str(client.get_emoji(BotEmotes.error)) + ' | An error occured!')
                else:
                    await wait.edit(content=f'Please add a language! To have the list and their id, type\n`{prefix}translate --list`.')
            else:
                await wait.edit(content=f'Please add translations or\nType `{prefix}translate --list` for supported languages.')
        if msg.startswith(prefix+'catfact'):
            catWait = await message.channel.send(str(client.get_emoji(BotEmotes.loading)) + ' | Please wait...')
            data = myself.api("https://catfact.ninja/fact")
            embed = discord.Embed(
                title = 'Did you know;',
                description = data["fact"],
                color = 0x333333
            )
            await catWait.edit(content='', embed=embed)
        if msg.startswith(prefix+'trash'):
            if len(args)!=2:
                await message.channel.send('Please mention someone!\nExample: `'+prefix+'trash <@'+message.author.id+'>`')
            else:
                av = message.author.avatar_url
                toTrash = message.mentions[0].avatar_url
                embed = discord.Embed(colour=discord.Colour.magenta())
                embed.set_image(url='https://api.alexflipnote.dev/trash?face='+str(av).replace('webp', 'png')+'&trash='+str(toTrash).replace('webp', 'png'))
                await message.channel.send(embed=embed)
        if args[0]==prefix+'bird' or msg.startswith(prefix+'sadcat'):
            if msg.startswith(prefix+'bird'):
                getreq = 'birb'
            else:
                getreq = 'sadcat'
            image_url = myself.insp('https://api.alexflipnote.dev/'+str(getreq)).split('"file": "')[1].split('"')[0]
            embed = discord.Embed(colour=discord.Colour.magenta())
            embed.set_image(url=image_url)
            await message.channel.send(embed=embed)
        if msg.startswith(prefix+'ytthumbnail'):
            if args[1].startswith('https://youtu.be/'):
                videoid = args[1][17:]
            elif args[1].startswith('http://youtu.be/'):
                videoid = args[1][16:]
            elif args[1].startswith('https://youtube.com/watch?v='):
                videoid = args[1][28:]
            elif args[1].startswith('https://www.youtube.com/watch?v='):
                videoid = args[1][32:]
            else:
                videoid = 'dQw4w9WgXcQ'
            await message.delete()
            embed = discord.Embed(title='Thumbnail for '+str(args[1]), color=0xff0000)
            embed.set_image(url='https://img.youtube.com/vi/'+str(videoid)+'/mqdefault.jpg')
            await message.channel.send(embed=embed)
        if msg.startswith(prefix+'captcha'):
            capt = myself.urlify(message.content[int(len(args[1])+1):])
            embed = discord.Embed(colour=discord.Colour.blue())
            embed.set_image(url='https://api.alexflipnote.dev/captcha?text='+str(capt))
            await message.channel.send(embed=embed)
        if msg.startswith(prefix+'tts'):
            if no_args:
                await message.channel.send(str(client.get_emoji(BotEmotes.error)) +' | Invalid.')
            else:
                await message.channel.send(content=msg[int(args[0]+1):], tts=True)
        if msg.startswith(prefix+'scroll'):
            scrolltxt = myself.urlify(unprefixed)
            embed = discord.Embed(colour=discord.Colour.red())
            embed.set_image(url='https://api.alexflipnote.dev/scroll?text='+str(scrolltxt))
            await message.channel.send(embed=embed)
        if msg.startswith(prefix+'ship') and no_args:
            member = []
            av = []
            for i in range(0, int(len(message.guild.members))):
                if message.guild.members[i].name!=message.author.name:
                    member.append(message.guild.members[i].name)
                    av.append(message.guild.members[i].avatar_url)
            num = random.randint(0, len(av))
            ship = member[num]
            avd = av[num]
            embed = discord.Embed(title=message.author.name+', i ship you with **'+str(ship)+'**!', colour=discord.Colour.magenta())
            embed.set_image(url='https://api.alexflipnote.dev/ship?user='+str(message.author.avatar_url).replace('webp', 'png')+'&user2='+str(avd).replace('webp', 'png'))
            embed.set_footer(text=f'Type {prefix}ship [tag1] [tag2] for cooler ones instead of just random!')
            await message.channel.send(embed=embed)
        if msg.startswith(prefix+'ghiblifilms'):
            wait = await message.channel.send(str(client.get_emoji(BotEmotes.loading)) + ' | Please wait... Getting data...')
            data = myself.api('https://ghibliapi.herokuapp.com/films')
            if no_args:
                films = ""
                for i in range(0, int(len(data))):
                    films = films+'('+str(int(i)+1)+') '+str(data[i]['title']+' ('+str(data[i]['release_date'])+')\n')
                embed = discord.Embed(
                    title = 'List of Ghibli Films',
                    description = str(films),
                    color = 0x00ff00
                )
                embed.set_footer(text='Type `'+str(prefix)+'ghiblifilms <number>` to get each movie info.')
                await wait.edit(content='', embed=embed)
            else:
                num = int(args[1])-1
                embed = discord.Embed(
                    title = data[num]['title'] + ' ('+str(data[num]['release_date'])+')',
                    description = '**Rotten Tomatoes Rating: '+str(data[num]['rt_score'])+'%**\n'+data[num]['description'],
                    color = 0x00ff00
                )
                embed.add_field(name='Directed by', value=data[num]['director'], inline='True')
                embed.add_field(name='Produced by', value=data[num]['producer'], inline='True')
                await wait.edit(content='', embed=embed)
        if msg.startswith(prefix+'servericon'):
            if message.guild.is_icon_animated()==True:
                link = 'https://cdn.discordapp.com/icons/'+str(message.guild.id)+'/'+str(message.guild.icon)+'.gif?size=1024'
            else:
                link = 'https://cdn.discordapp.com/icons/'+str(message.guild.id)+'/'+str(message.guild.icon)+'.png?size=1024'
            theEm = discord.Embed(title=message.guild.name+'\'s Icon', colour=discord.Colour.blue())
            theEm.set_image(url=link)
            await message.channel.send(embed=theEm)
        if msg.startswith(prefix+'slowmode'):
            if len(args)!=2:
                await message.channel.send(str(client.get_emoji(BotEmotes.error)) +' | Invalid setup.')
            else:
                if message.author.guild_permissions.manage_channels==False:
                    await message.channel.send(str(client.get_emoji(BotEmotes.error)) +' | <@'+str(message.author.id)+'> you need the `Manage channels` permission.')
                else:
                    try:
                        global delay
                        delay = int(args[1])
                    except ValueError:
                        await message.channel.send(str(client.get_emoji(BotEmotes.error)) +' | Invalid number!')
                    if delay>21600:
                        await message.channel.send(str(client.get_emoji(BotEmotes.error)) +' | That\'s too long! You must be an insane admin to do this :flushed:')
                    elif delay<0:
                        await message.channel.send(str(client.get_emoji(BotEmotes.error)) +f' | Nope, you expect me to minus slowmode?\n\n**To disable slowmode, type {prefix}slowmode 0 instead.**')
                    else:
                        await message.channel.edit(slowmode_delay=delay)
                        if delay==0:
                            await message.channel.send(str(client.get_emoji(BotEmotes.success)) + ' | Successfully disabled slowmode.')
                        else:
                            await message.channel.send(str(client.get_emoji(BotEmotes.success)) + ' | Successfully changed the slowmode delay of this channel to '+str(delay)+' seconds.')
        if msg.startswith(prefix+'inviteme') or msg.startswith(prefix+'invite'):
            if message.guild.id!=264445053596991498:
                embed = discord.Embed(
                    title='Sure thing! Invite this bot to your server using the link below.',
                    description='[Invite link](https://top.gg/bot/696973408000409626) | [Support Server](http://discord.gg/HhAPkD8)',
                    colour=discord.Colour.green()
                )
                await message.channel.send(embed=embed)
        if msg.startswith(prefix+'serverinfo'):
            acceptId = 0
            o_web = 0
            o_desk = 0
            o_pho = 0
            botcount = 0
            online = 0
            idle = 0
            dnd = 0
            offline = 0
            if acceptId==0:
                for i in range(0, int(len(message.guild.members))):
                    if message.guild.get_member(int(message.guild.members[i].id)).desktop_status.name!='offline':
                        o_desk = int(o_desk)+1
                    elif message.guild.get_member(int(message.guild.members[i].id)).mobile_status.name!='offline':
                        o_pho = int(o_pho)+1
                    elif message.guild.get_member(int(message.guild.members[i].id)).web_status.name!='offline':
                        o_web = int(o_web)+1
                    if message.guild.members[i].bot==True:
                        botcount = int(botcount)+1
                    memstat = message.guild.get_member(int(message.guild.members[i].id)).status.name
                    if memstat=='online':
                        online = online + 1
                    elif memstat=='idle':
                        idle = idle + 1
                    elif memstat=='dnd':
                        dnd = dnd + 1
                    else:
                        offline = int(offline) + 1
                total_on = online + idle + dnd
                onperc = round(total_on/len(message.guild.members)*100)
                humans = int(len(message.guild.members))-int(botcount)
                embed = discord.Embed(
                    title=str(message.guild.name),
                    description='Shows the information about '+str(message.guild.name),
                    color=0x000000
                )
                embed.add_field(name='General Info', value='**Region:** '+str(message.guild.region)+'\n**Server ID: **'+str(message.guild.id)+'\n**Server created at: **'+str(message.guild.created_at)[:-7]+' UTC\n**Verification Level: **'+str(message.guild.verification_level)+'\n**Notification level:  **'+str(message.guild.default_notifications)[18:].replace("_", " ")+'\n**Explicit Content Filter:**'+str(message.guild.explicit_content_filter)+'\n**AFK timeout: **'+str(message.guild.afk_timeout)+' seconds\n**Description: **"'+str(message.guild.description)+'"', inline='True')
                embed.add_field(name='Channel Info', value='**Text Channels: **'+str(len(message.guild.text_channels))+'\n**Voice channels: **'+str(len(message.guild.voice_channels))+'\n**Channel categories: **'+str(len(message.guild.categories))+'\n**AFK Channel: **'+str(message.guild.afk_channel), inline='True')
                embed.add_field(name='Members Info', value='**Server owner: **'+str(message.guild.owner)[:-5]+'\n**Members count: **'+str(len(message.guild.members))+'\n**Server Boosters: **'+str(len(message.guild.premium_subscribers))+'\n**Role Count: **'+str(len(message.guild.roles))+'\n**Bot accounts: **'+str(botcount)+'\n**Human accounts: **'+str(humans), inline='True')
                embed.add_field(name='Member Status', value=':green_circle: '+str(online)+' :orange_circle: '+str(idle)+' :red_circle: '+str(dnd)+' :black_circle: '+str(offline)+'\n:grinning: '+str(total_on)+' ('+str(onperc)+'%) | :sleeping: '+str(offline)+' ('+str(100-int(onperc))+'%)\n:iphone: '+str(o_pho)+' | :computer: '+str(o_desk)+' | :globe_with_meridians: '+str(o_web))
                serverurl = 'https://discordapp.com/channels/'+str(message.guild.id)
                if message.guild.is_icon_animated()==False:
                    servericonurl = str('https://cdn.discordapp.com/icons/'+str(message.guild.id)+'/'+str(message.guild.icon)+'.png?size=1024')
                else:
                    servericonurl = str('https://cdn.discordapp.com/icons/'+str(message.guild.id)+'/'+str(message.guild.icon)+'.gif?size=1024')
                embed.add_field(name='URL stuff', value=f'[Server URL]({serverurl}) | [Server Icon URL]({servericonurl})')
                embed.set_thumbnail(url=str('https://cdn.discordapp.com/icons/'+str(message.guild.id)+'/'+str(message.guild.icon)+'.png?size=1024'))
                embed.set_image(url='https://discord.com/api/guilds/'+str(message.guild.id)+'/embed.png?style=banner1')
                await message.channel.send(embed=embed)
        if msg.startswith(prefix+'factor'):
            if int(args[1])<999999:
                numList = range(1, int(args[1]))
                factor = []
                for i in range(0, int(len(numList))):
                    if int(args[1])%int(numList[i])==0:
                        factor.append(numList[i])
                factor.append(int(args[1]))
                await message.channel.send(str(factor))
            else:
                await message.channel.send(str(client.get_emoji(BotEmotes.error)) + ' | OverloadInputError: Beyond the limit of 999999.')
        if msg.startswith(prefix+'multiplication'):
            arr = []
            for i in range(1, 15):
                arr.append(int(args[1])*i)
            await message.channel.send(str(arr))
        if msg.startswith(prefix+'gdcomment'):
            try:
                byI = unprefixed.split(' | ')
                text = myself.urlify(byI[0])
                num = int(byI[2])
                if num>9999:
                    num = 601
                elif num<-9999:
                    num = -601
                gdprof = myself.urlify(byI[1])
                embed = discord.Embed(colour=discord.Colour.green())
                if message.author.guild_permissions.manage_guild==True:
                    embed.set_image(url='https://gdcolon.com/tools/gdcomment/img/'+str(text)+'?name='+str(gdprof)+'&likes='+str(num)+'&mod=mod&days=1-second')
                else:
                    embed.set_image(url='https://gdcolon.com/tools/gdcomment/img/'+str(text)+'?name='+str(gdprof)+'&likes='+str(num)+'&days=1-second')
                await message.channel.send(embed=embed)
            except Exception as e:
                print('https://gdcolon.com/tools/gdcomment/img/'+str(text)+'?name='+str(gdprof)+'&likes='+str(num)+'&days=1-second')
                await message.channel.send(str(client.get_emoji(BotEmotes.error)) +f' | Invalid!\nThe flow is this: `{prefix}gdcomment text | name | like count`\nExample: `{prefix}gdcomment I am cool | RobTop | 601`.\n\nFor developers: ```{e}```')
        if msg.startswith(prefix+'gdbox'):
            if no_args:
                await message.channel.send('Please input a text!')
            else:
                wait = await message.channel.send(str(client.get_emoji(BotEmotes.loading)) + ' | Please wait...')
                text = myself.urlify(unprefixed)
                av = message.author.avatar_url
                if len(text)>100:
                    await message.channel.send(str(client.get_emoji(BotEmotes.error)) +' | the text is too long!')
                else:
                    if message.author.guild_permissions.manage_guild==False:
                        color = 'brown'
                    else:
                        color = 'blue'
                    embed = discord.Embed(colour=discord.Colour.green())
                    embed.set_image(url='https://gdcolon.com/tools/gdtextbox/img/'+str(text)+'?color='+color+'&name='+str(message.author.name)+'&url='+str(av).replace('webp', 'png')+'&resize=1')
                    await wait.edit(content='', embed=embed)
        if msg.startswith(prefix+'serveremojis'):
            acceptId = 0
            if acceptId==0:
                if len(args)==2 and args[1]=='--short':
                    all = ''
                    for i in range(0, len(message.guild.emojis)):
                        if len(all)>1960:
                            break
                        if message.guild.emojis[i].animated==True:
                            all = all + ' <a:'+str(message.guild.emojis[i].name)+':'+str(message.guild.emojis[i].id)+'> '
                        else:
                            all = all + ' <:'+str(message.guild.emojis[i].name)+':'+str(message.guild.emojis[i].id)+'> '
                    await message.channel.send(str(all))
                else:
                    staticemo = ""
                    animateemo = ""
                    staticcount = 0
                    animatecount = 0
                    warning = 'No errors found.'
                    for i in range(0, int(len(message.guild.emojis))):
                        if message.guild.emojis[i].animated==True:
                            animatecount = int(animatecount) + 1
                        else:
                            staticcount = int(staticcount) + 1
                        if len(staticemo)>950 or len(animateemo)>950:
                            warning = 'Error: Too many emojis, some emojis may remain unlisted above.\nInstead type '+str(prefix+'serveremojis --short')
                            break
                        if message.guild.emojis[i].animated==True:
                            animateemo = animateemo + '<a:'+str(message.guild.emojis[i].name)+':'+str(message.guild.emojis[i].id)+'> ('+str(message.guild.emojis[i].name)+') \n'
                        else:
                            staticemo = staticemo + '<:'+str(message.guild.emojis[i].name)+':'+str(message.guild.emojis[i].id)+'> ('+str(message.guild.emojis[i].name)+') \n'
                    embed = discord.Embed(
                        title = message.guild.name+'\'s emojis',
                        colour = discord.Colour.red()
                    )
                    if staticemo=="":
                        staticemo = 'No emojis found :('
                    if animateemo=="":
                        animateemo = 'No emojis found :('
                    embed.add_field(name='Static Emojis ('+str(staticcount)+')', value=str(staticemo), inline='False')
                    embed.add_field(name='Animated Emojis ('+str(animatecount)+')', value=str(animateemo), inline='False')
                    embed.set_footer(text=str(warning))
                    await message.channel.send(embed=embed)
        if msg.startswith(prefix+'id'):
            var = args[1][:-1]
            if args[1].startswith('<#'):
                var = var[2:]
                if len(message.mentions)>0:
                    var = message.mentions[0].id
            elif (args[1].startswith('<@&')):
                var = var[3:]
            await message.channel.send(str(var))
        if msg.startswith(prefix+'robohash'):
            if no_args:
                gib = ''
                for i in range(0, random.randint(5, 10)):
                    gib = gib + random.choice(list('ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz'))
            else:
                gib = msg[int(len(args[0])+1):]
            embed = discord.Embed(title='Here is some robohash for you.', colour=discord.Colour.magenta())
            embed.set_image(url='https://robohash.org/'+str(gib))
            await message.channel.send(embed=embed)
        if msg.startswith(prefix+'gdlogo'):
            if no_args:
                await message.channel.send('Please input a text!')
            else:
                text = myself.urlify(unprefixed)
                embed = discord.Embed(colour=discord.Colour.green())
                embed.set_image(url='https://gdcolon.com/tools/gdlogo/img/'+str(text))
                await message.channel.send(embed=embed)
        if msg.startswith(prefix+'lockdown'):
            if len(args)!=2:
                await message.channel.send(str(client.get_emoji(BotEmotes.error)) +f' | Invalid parameters. Correct Example: `{prefix}lockdown [seconds]`\nMinimum: 10, Maximum: 900')
            else:
                if args[1].isnumeric()==False:
                    await message.channel.send(str(client.get_emoji(BotEmotes.error)) +' | Invalid time.')
                elif int(args[1])<10 or int(args[1])>900:
                    await message.channel.send(str(client.get_emoji(BotEmotes.error)) +' | Invalid: off-limits.')
                elif message.author.guild_permissions.administrator==False:
                    await message.channel.send(str(client.get_emoji(BotEmotes.error)) +' | You need the administrator permission to do this!')
                else:
                    try:
                        await message.channel.send('Everyone, <#'+str(message.channel.id)+'> is on lockdown for '+str(args[1])+' seconds! No one except administrators can chat! :x:')
                        await message.channel.set_permissions(message.guild.default_role, send_messages=False)
                        await asyncio.sleep(int(args[1]))
                        await message.channel.set_permissions(message.guild.default_role, send_messages=True)
                        await message.channel.send('Lockdown ended.')
                    except:
                        await message.channel.send(str(client.get_emoji(BotEmotes.error)) +' | For some reason, i cannot lock this channel :(')
        if args[0]==prefix+"math" or args[0]==prefix+'calc':
            if no_args:
                await message.channel.send("No math problem? Ok no fix.")
            else:
                ban = True
                for i in range(0, len(unprefixed.lower())):
                    if unprefixed.lower()[i] in list("ABCDEFGHIJKLMNOPQRSTUVWXYZ."):
                        ban = True
                        break
                if ban:
                    await message.channel.send('This command has closed down for maintenance. It will be open again in the future. Sorry!')
                else:
                    try:
                        await message.channel.send(embed=discord.Embed(title="Equation result", description=f'**Equation:** ```{unprefixed}```\n**Result:**\n```{eval(unprefixed)}```', colour=discord.Colour.red()))
                    except ZeroDivisionError:
                        await message.channel.send(embed=discord.Embed(title="Equation result", description=f'**Equation:** ```{unprefixed}```\n**Result:**\n```yo mama```', colour=discord.Colour.red()))
            beginning = int(args[1])
            ending = int(args[2])
            ran = random.randint(int(beginning), int(ending))
            await message.channel.send(str(ran))
        if msg.startswith(prefix+"flipdice") or msg.startswith(prefix+"dice"):
            arr = ["one", "two", "three", "four", "five", "six"]
            ran = random.randint(0, 5)
            await message.channel.send(":"+arr[ran]+":")
        if msg.startswith(prefix+"flipcoin") or msg.startswith(prefix+"coin"):
            ran = random.randint(0, 1)
            if (ran==0):
                await message.channel.send("HEADS")
            elif (ran==1):
                await message.channel.send("TAILS")
        if msg.startswith(prefix+'ship') and len(args)>1:
            if len(args)<3:
                await message.channel.send(':x: Please tag 2 people!')
            elif len(args)==3:
                if args[1].startswith('<@!'):
                    av1 = message.guild.get_member(message.mentions[0].id).avatar_url
                else:
                    av1 = message.guild.get_member(message.mentions[0].id).avatar_url
                if args[2].startswith('<@!'):
                    av2 = message.guild.get_member(message.mentions[1].id).avatar_url
                else:
                    av2 = message.guild.get_member(message.mentions[1].id).avatar_url
                embed = discord.Embed(colour=discord.Colour.magenta())
                embed.set_image(url='https://api.alexflipnote.dev/ship?user='+str(av1).replace('webp', 'png')+'&user2='+str(av2).replace('webp', 'png'))
                await message.channel.send(embed=embed)
        if msg==prefix+"dog":
            data = myself.api("https://random.dog/woof.json")
            img = data['url']
            embed = discord.Embed(colour=discord.Colour.magenta())
            embed.set_image(url=img)
            await message.channel.send(embed=embed)
        if msg==prefix+"cat" or msg.startswith(prefix+"cats"):
            data = myself.api("https://aws.random.cat/meow")
            embed = discord.Embed(colour=discord.Colour.magenta())
            embed.set_image(url=data['file'])
            await message.channel.send(embed=embed)
        if msg.startswith(prefix+'imgcaptcha'):
            if len(message.mentions)==0:
                av = str(message.author.avatar_url).replace('.webp?size=1024', '.png')
                nm = myself.urlify(str(message.author.name))
            else:
                av = str(message.mentions[0].avatar_url).replace('.webp?size=1024', '.png')
                nm = myself.urlify(str(message.mentions[0].name))
            embed = discord.Embed(colour=discord.Colour.green())
            embed.set_image(url='http://nekobot.xyz/api/imagegen?type=captcha&username='+nm+'&url='+av+'&raw=1')
            await message.channel.send(embed=embed)
        if msg.startswith(prefix+'whowouldwin'):
            if len(message.mentions)!=2:
                await message.channel.send('Please tag TWO people!')
            else:
                embed = discord.Embed(colour=discord.Colour.red())
                embed.set_image(url='http://nekobot.xyz/api/imagegen?type=whowouldwin&raw=1&user1='+str(message.mentions[0].avatar_url).replace('.webp?size=1024', '.png')+'&user2='+str(message.mentions[1].avatar_url).replace('.webp?size=1024', '.png'))
                await message.channel.send(embed=embed)
        if msg.startswith(prefix+'trap'):
            if no_args or len(message.mentions)==0:
                await message.channel.send(str(client.get_emoji(BotEmotes.error)) +f' | Wrong.\nPlease try the correct like following:\n`{prefix}trap [tag]`')
            else:
                embed = discord.Embed(colour=discord.Colour.magenta())
                embed.set_image(url='http://nekobot.xyz/api/imagegen?type=trap&name='+myself.urlify(str(message.mentions[0].name))+'&author='+myself.urlify(str(message.author.name))+'&image='+str(message.mentions[0].avatar_url).replace('.webp?size=1024', '.png')+'&raw=1')
                await message.channel.send(embed=embed)
        if msg.startswith(prefix+'roles'):
            acceptId = 0
            if acceptId==0:
                serverroles = ""
                warning = "No warnings available."
                for i in range(1, int(len(message.guild.roles))):
                    num = int(len(message.guild.roles))-int(i)
                    if len(serverroles)>1990:
                        warning = 'Roles pass the limit of discord Description. This means that some roles are not listed above.'
                        break
                    serverroles = serverroles + str(message.guild.roles[num].name)+'\n'
                embed = discord.Embed(
                    title = 'Server roles of '+message.guild.name+' (From top to bottom.)',
                    description = str(serverroles),
                    color = discord.Colour.dark_blue()
                )
                embed.set_footer(text=str(warning))
                await message.channel.send(embed=embed)
        if msg.startswith(prefix+"gddaily"):
            toEdit = await message.channel.send("Retrieving Data...")
            data = myself.api("https://gdbrowser.com/api/level/daily")
            image = 'https://gdbrowser.com/icon/'+data["author"]
            embed = discord.Embed(
                title = data["name"]+' ('+str(data["id"])+')',
                description = data["description"],
                colour = discord.Colour.blue()
            )
            embed.set_author(name=data["author"], icon_url=image)
            embed.add_field(name='Uploaded at', value=data["uploaded"], inline='True')
            embed.add_field(name='Updated at', value=data["updated"]+" (Version "+data["version"]+")", inline='True')
            embed.add_field(name='Difficulty', value=data["difficulty"])
            gesture = ':+1:'
            if data['disliked']==True:
                gesture = ':-1:'
            embed.add_field(name='Level Stats', value=str(data["likes"])+' '+gesture+'\n'+str(data["downloads"])+" :arrow_down:", inline='False')
            embed.add_field(name='Level Rewards', value=str(data["stars"])+" :star:\n"+str(data["orbs"])+" orbs\n"+str(data["diamonds"])+" :gem:")
            await toEdit.edit(content='', embed=embed)
        if msg.startswith(prefix+'botmembers'):
            botmembers = ""
            warning = 'Down triangles means that the bot is down. And up triangles mean the bot is well... up.'
            for i in range(0, int(len(message.guild.members))):
                if len(botmembers)>2048:
                    warning = str(client.get_emoji(BotEmotes.error)) + ' | Error: Too many bots, some bot are not listed above.'
                    break
                if message.guild.members[i].bot==True:
                    if str(message.guild.members[i].status)=='offline':
                        botmembers += ':small_red_triangle_down: '+ message.guild.members[i].name + '\n'
                    else:
                        botmembers += ':small_red_triangle: ' + message.guild.members[i].name + '\n'
            embed = discord.Embed(
                title = 'Bot members of '+message.guild.name+':',
                description = str(botmembers),
                colour = discord.Colour.dark_blue()
            )
            embed.set_footer(text=warning)
            await message.channel.send(embed=embed)
        if msg.startswith(prefix+"gdweekly"):
            toEdit = await message.channel.send("Retrieving Data...")
            data = myself.api("https://gdbrowser.com/api/level/weekly")
            image = 'https://gdbrowser.com/icon/'+data["author"]
            embed = discord.Embed(
                title = data["name"]+' ('+str(data["id"])+')',
                description = data["description"],
                colour = discord.Colour.red()
            )
            embed.set_author(name=data["author"], icon_url=image)
            embed.add_field(name='Uploaded at', value=data["uploaded"], inline='True')
            embed.add_field(name='Updated at', value=data["updated"]+" (Version "+data["version"]+")", inline='True')
            embed.add_field(name='Difficulty', value=data["difficulty"])
            gesture = ':+1:'
            if data['disliked']==True:
                gesture = ':-1:'
            embed.add_field(name='Level Stats', value=str(data["likes"])+' '+gesture+'\n'+str(data["downloads"])+" :arrow_down:", inline='False')
            embed.add_field(name='Level Rewards', value=str(data["stars"])+" :star:\n"+str(data["orbs"])+" orbs\n"+str(data["diamonds"])+" :gem:")
            await toEdit.edit(content='', embed=embed)
        if msg.startswith(prefix+'facts'):
            embed = discord.Embed(colour=discord.Colour.magenta())
            embed.set_image(url='https://api.alexflipnote.dev/facts?text='+myself.urlify(unprefixed))
            await message.channel.send(embed=embed)
        if msg.startswith(prefix+"gdprofile"):
            url = myself.urlify(unprefixed)
            data = myself.api("https://gdbrowser.com/api/profile/"+url)
            embed = discord.Embed(
                title = data["username"],
                description = 'Displays user data for '+data["username"]+'.',
                colour = discord.Colour.orange()
            )
            if data["rank"]=="0":
                rank = "Not yet defined :("
            else:
                rank = str(data["rank"])
            if data["cp"]=="0":
                cp = "This user don't have Creator Points :("
            else:
                cp = data["cp"]
            embed.add_field(name='ID Stuff', value='Player ID: '+str(data["playerID"])+'\nAccount ID: '+str(data["accountID"]), inline='True')
            embed.add_field(name='Rank', value=rank, inline='True')
            embed.add_field(name='Stats', value=str(data["stars"])+" Stars"+"\n"+str(data["diamonds"])+" Diamonds\n"+str(data["coins"])+" Secret Coins\n"+str(data["userCoins"])+" User Coins\n"+str(data["demons"])+" Demons beaten", inline='False')
            embed.add_field(name='Creator Points', value=cp)
            embed.set_author(name='Display User Information', icon_url="https://gdbrowser.com/icon/"+url)
            await message.channel.send(embed=embed)
        if msg.startswith(prefix+"rps"):
            main = await message.channel.send(embed=discord.Embed(title='Rock Paper Scissors game.', description='Click the reaction below. And game will begin.', colour=discord.Colour.green()))
            exp = ['✊', '🖐️', '✌']
            for i in range(0, len(exp)):
                await main.add_reaction(exp[i])
            def check(reaction, user):
                return user == message.author
            try:
                reaction, user = await client.wait_for('reaction_add', timeout=15.0, check=check)
            except asyncio.TimeoutError:
                await main.add_reaction('😔')
            beginGame = False
            given = None
            emojiArray = None
            ran = None
            if str(reaction.emoji) in exp:
                emotes = ["fist", "hand_splayed", "v"]
                num = myself.findNum(str(reaction.emoji), exp)
                beginGame = True
                res = discordgames.rps(emotes[num])
                given = emotes[num]
                msgId = res[0]
                emojiArray = emotes
                ran = res[1]
            messages = ["Congratulations! "+str(message.author.name)+" WINS!", "It's a draw.", "Oops, "+str(message.author.name)+" lost!"]
            colors = [discord.Colour.green(), discord.Colour.orange(), discord.Colour.red()]
            if beginGame:
                embed = discord.Embed(
                    title = messages[msgId],
                    colour = colors[msgId]
                )
                embed.set_footer(text='Playin\' rock paper scissors w/ '+str(message.author.name))
                embed.set_author(name="Playing Rock Paper Scissors with "+str(message.author.name))
                embed.add_field(name=str(message.author.name), value=':'+given+':', inline="True")
                embed.add_field(name='Username601', value=':'+str(emojiArray[ran])+':', inline="True")
                await main.edit(embed=embed)
        if msg.startswith(prefix+"randomcase"):
            statement = []
            for i in range(1, int(len(args))):
                statement.append(args[i])
                thing = ' '.join(statement)
            result = []
            letterArr = list(thing)
            for i in range(0, len(thing)):
                ran = random.randint(0, 1)
                if ran==0:
                    result.append(letterArr[i].upper())
                elif ran==1:
                    result.append(letterArr[i].lower())
            await message.channel.send("".join(result))
        if msg.startswith(prefix+'guessnum') or msg.startswith(prefix+'gn'):
            num = random.randint(5, 100)
            username = message.author.display_name
            user_class = message.author
            embed = discord.Embed(title='Starting the game!', description='You have to guess a *secret* number between 5 and 100!\n\nYou have 20 attempts, and 20 second timer in each attempt!\n\n**G O O D  L U C K**', colour=discord.Colour.green())
            await message.channel.send(embed=embed)
            gameplay = True
            attempts = 20
            while gameplay==True:
                if attempts<1:
                    await message.channel.send('Time is up! The answer is **'+str(num)+'.**')
                    gameplay = False
                    break
                def check_not_stranger(m):
                    return m.author == user_class
                try:
                    trying = await client.wait_for('message', check=check_not_stranger, timeout=20.0)
                except asyncio.TimeoutError:
                    await message.channel.send(str(client.get_emoji(BotEmotes.error)) +' | You did not respond for the next 20 seconds!\nGame ended.')
                    gameplay = False
                    break
                if trying.content.isnumeric()==False:
                    await message.channel.send('That is not a number!')
                    attempts = int(attempts) - 1
                else:
                    if int(trying.content)<num:
                        await message.channel.send('Higher!')
                        attempts = int(attempts) - 1
                    if int(trying.content)>num:
                        await message.channel.send('Lower!')
                        attempts = int(attempts) - 1
                    if int(trying.content)==num:
                        await message.channel.send(str(client.get_emoji(BotEmotes.success)) +' | You are correct!\n**The answer is '+str(num)+'!**')
                        gameplay = False
                        break
        if msg.startswith(prefix+"randomcolor") or msg.startswith(prefix+'colorinfo') or msg.startswith(prefix+'colourinfo'):
            continuing = False
            if msg.startswith(prefix+'randomcolor'):
                listHex = list('0123456789ABCDEF')
                hexCode = ''
                for i in range(0, 6):
                    ran = random.choice(listHex)
                    hexCode = hexCode + ran
                continuing = True
            else:
                if len(args)!=2:
                    await message.channel.send(str(client.get_emoji(BotEmotes.error)) +' | Invalid arguments.')
                elif args[1].startswith('#'):
                    hexCode = args[1][1:]
                    continuing = True
                elif args[1] in list('0123456789ABCDEF') and len(args[1])==6:
                    hexCode = args[1]
                    continuing = True
                elif args[1].isnumeric()==True:
                    hexCode = str(myself.tohex(args[1]))
                    continuing = True
                elif len(args[1])!=6:
                    await message.channel.send('We only accept `HEX CODES` and `INTEGER VALUES` as inputs!')
                else:
                    hexCode = args[1]
                    continuing = True
            if continuing==True:
                rgb = myself.convertrgb(hexCode, '0')
                percentageRgb = myself.convertrgb(hexCode, '1')
                colorInt = int(hexCode, 16)
                embed = discord.Embed(title='#'+str(hexCode), description="**Integer: **`"+str(colorInt)+"`\n**Red:** "+str(rgb[0])+" ("+str(percentageRgb[0])+"%)\n**Green:** "+str(rgb[1])+" ("+str(percentageRgb[1])+"%)\n**Blue:** "+str(rgb[2])+" ("+str(percentageRgb[2])+"%)\n\nPreview is shown on thumbnail. Other similar gradients are shown below.", colour=discord.Colour.from_rgb(int(rgb[0]), int(rgb[1]), int(rgb[2])))
                embed.set_thumbnail(url='https://api.alexflipnote.dev/colour/image/'+str(hexCode))
                embed.set_image(url='https://api.alexflipnote.dev/colour/image/gradient/'+str(hexCode))
                await message.channel.send(embed=embed)
        if msg.startswith(prefix+'call'):
            call = myself.urlify(msg[6:])
            embed = discord.Embed(colour=discord.Colour.blue())
            embed.set_image(url='https://api.alexflipnote.dev/calling?text='+str(call))
            await message.channel.send(embed=embed)
        if msg.startswith(prefix+'achieve'):
            txt = myself.urlify(unprefixed)
            embed = discord.Embed(colour=discord.Colour.blue())
            embed.set_image(url='https://api.alexflipnote.dev/achievement?text='+str(txt))
            await message.channel.send(embed=embed)
        if msg.startswith(prefix+"country"):
            country = myself.urlify(unprefixed)
            c = myself.api("https://restcountries.eu/rest/v2/name/"+str(country.lower()))
            if len(c[0]['borders'])==0: borderz = 'No borders.'
            else: borderz = myself.dearray(c[0]['borders'])
            embed = discord.Embed(
                title = c[0]['nativeName'],
                description = '**Capital:** '+str(c[0]['capital'])+'\n**Region: **'+str(c[0]['region'])+'\n**Sub Region: **'+str(c[0]['subregion'])+"\n**Population: **"+str(c[0]['population'])+"\n**Area: **"+str(c[0]['area'])+' km²\n**Time Zones:** '+str(myself.dearray(c[0]['timezones']))+'\n**Borders: **'+str(borderz),
                colour = 0xffffff
            )
            embed.set_author(name=c[0]['name'])
            await message.channel.send(embed=embed)
        if msg.startswith(prefix+'commands') or msg.startswith(prefix+'help'):
            data = myself.jsonisp("https://raw.githubusercontent.com/vierofernando/username601/master/commands.json")
            types = ['Bot Help', 'Moderation', 'Utilities', 'Math', 'Fun', 'Games', 'Encoding', 'Memes', 'Images', 'Apps']
            if no_args:
                if message.guild.id!=264445053596991498:
                    cate = ''
                    for i in range(0, len(types)):
                        cate += f'**{str(i+1)}. **{prefix}help {str(types[i])}\n'
                    embed = discord.Embed(
                        title='Username601\'s commands',
                        description='[Join the support server](https://discord.gg/HhAPkD8) | [Vote us on top.gg](https://top.gg/bot/696973408000409626/vote)\n\n**[More information on our website here.](https://vierofernando.github.io/username601/commands)**\n**Command Categories:** \n'+str(cate),
                        colour=discord.Colour.dark_blue()
                    )
                    embed.set_footer(text=f'Type {prefix}help <command/category> for more details.')
                    await message.channel.send(embed=embed)
                else:
                    await message.channel.send(embed=discord.Embed(title='Bot commands', description='[All commands are here.](https://vierofernando.github.io/username601/commands)'), colour=discord.Colour.blue())
            else:
                source = None
                typ = ''
                category_name = None
                query = msg[int(len(args[0])+1):]
                for i in range(0, len(types)):
                    if query==types[i].lower():
                        source = data[i][types[i]]
                        typ = 'Category'
                        category_name = types[i]
                        break
                if source==None:
                    for i in range(0, len(data)):
                        for j in range(0, len(data[i][types[i]])):
                            if query==data[i][types[i]][j]['n'].lower():
                                source = data[i][types[i]][j]
                                typ = 'Command'
                                break
                        if not typ=='':
                            break
                if source==None:
                    await message.channel.send('Oops... Your command doesn\'t seem to exist.')
                else:
                    if typ=='Category':
                        cmds = []
                        for i in range(0, len(source)):
                            cmds.append(source[i]['n'])
                        cmds = myself.dearray(cmds)
                        embed = discord.Embed(title='Category help for '+str(category_name)+':', description='**Commands:** \n```'+str(cmds)+'```', colour=discord.Colour.red())
                    if typ=='Command':
                        parameters = 'No parameters required.'
                        if len(source['p'])>0:
                            parameters = ''
                            for i in range(0, len(source['p'])):
                                parameters += '**'+source['p'][i]+'**\n'
                        embed = discord.Embed(title='Command help for '+str(source['n'])+':', description='**Function: **'+str(source['f'])+'\n**Parameters:** \n'+str(parameters), colour=discord.Colour.red())
                    await message.channel.send(embed=embed)
        if msg.startswith(prefix+'uptime'):
            embed = discord.Embed(title=str(datetime.datetime.now()-latest_update)[:-7], description='Last time down: '+str(latest_update)[:-7], color=discord.Colour.red())
            embed.set_footer(text='Don\'t worry! 99% Uptime guaranteed.\nUnless there is an big error/on development.')
            await message.channel.send(embed=embed)
        if msg.startswith(prefix+'about'):
            if message.guild.id!=264445053596991498:
                messageRandom = splashes.getAbout()
                # osinfo = myself.platform()
                if str(client.get_guild(688373853889495044).get_member(661200758510977084).status)=='offline':
                    devstatus = 'Offline'
                else:
                    devstatus = 'Online'
                embed = discord.Embed(
                    title = 'About this seemingly normal bot.',
                    description = random.choice(messageRandom),
                    colour = 0xff0000
                )
                embed.add_field(name='Bot general Info', value='**Bot name: ** Username601\n**Programmed in: **Discord.py (Python)\n**Created in: **6 April 2020.\n**Successor of: **somebot56.\n**Default prefix: ** 1', inline='True')
                embed.add_field(name='Programmer info', value='**Programmed by: **Viero Fernando. ('+client.get_user(661200758510977084).name+'#'+str(client.get_user(661200758510977084).discriminator)+') \n**Best languages: **~~HTML, CSS,~~ VB .NET, JavaScript, Python\n**Current Discord Status:** '+devstatus+'\n**Social links:**\n[Discord Server](http://discord.gg/HhAPkD8)\n[GitHub](http://github.com/vierofernando)\n[Top.gg](https://top.gg/user/661200758510977084)\n[SoloLearn](https://www.sololearn.com/Profile/17267145)\n[Brainly (Indonesia)](http://bit.ly/vierofernandobrainly)\n[Geometry Dash](https://gdbrowser.com/profile/knowncreator56)', inline='True')
                embed.add_field(name='Version Info', value='**Bot version: ** '+bot_ver+'\n**Changelog: **'+bot_changelog+'\n\n**Discord.py version: **'+str(discord.__version__)+'\n**Python version: **'+str(sys.version).split(' (default')[0])#+'\n'+str(osinfo))
                embed.add_field(name='Links', value='[Invite this bot to your server!](http://vierofernando.github.io/programs/username601) | [Source code](http://github.com/vierofernando/username601) | [The support server!](http://discord.gg/HhAPkD8) | [Vote us on top.gg](https://top.gg/bot/696973408000409626/vote) | [Official Website](https://vierofernando.github.io/username601)', inline='False')
                embed.set_thumbnail(url='https://raw.githubusercontent.com/vierofernando/username601/master/pfp.png')
                embed.set_footer(text='© Viero Fernando Programming, 2018-2020. All rights reserved.')
                await message.channel.send(embed=embed)
        if msg.startswith(prefix+'vote'):
            embed = discord.Embed(title='Support by Voting us at top.gg!', description='Sure thing, mate! [Vote us at top.gg by clicking me!](https://top.gg/bot/696973408000409626/vote)', colour=discord.Colour.blue())
            await message.channel.send(embed=embed)
        if msg.startswith(prefix+'space'):
            embed = discord.Embed(colour=discord.Colour.dark_blue())
            embed.set_image(url='https://source.unsplash.com/500x500/?space')
            await message.channel.send(embed=embed)
        if msg.startswith(prefix+'time') or msg.startswith(prefix+'utc'):
            data = myself.api("http://worldtimeapi.org/api/timezone/africa/accra")
            year = str(data["utc_datetime"])[:-28]
            time = str(data["utc_datetime"])[:-22]
            date = str(data["utc_datetime"])[:-13]
            date = str(date)[11:]
            if int(year)%4==0:
                yearType = 'It is a leap year.'
                yearLength = 366
            else:
                yearType = 'It is not a leap year yet.'
                yearLength = 365
            progressDayYear = round(int(data["day_of_year"])/int(yearLength)*100)
            progressDayWeek = round(int(data["day_of_week"])/7*100)
            embed = discord.Embed(
                title = str(date)+' | '+str(time)+' (API)',
                description = str(datetime.datetime.now())[:-7]+'(SYSTEM)\nBoth time above is on UTC.\n**Unix Time:** '+str(data["unixtime"])+'\n**Day of the year: **'+str(data["day_of_year"])+' ('+str(progressDayYear)+'%)\n**Day of the week: **'+str(data["day_of_week"])+' ('+str(progressDayWeek)+'%)\n'+str(yearType),
                colour = discord.Colour.green()
            )
            await message.channel.send(embed=embed)
        if msg.startswith(prefix+'joke') or msg.startswith(prefix+'jokes'):
            data = myself.api("https://official-joke-api.appspot.com/jokes/general/random")
            embed = discord.Embed(
                title = str(data[0]["setup"]),
                description = '||'+str(data[0]["punchline"])+'||',
                colour = discord.Colour.blue()
            )
            await message.channel.send(embed=embed)
        if msg.startswith(prefix+'qr'):
            content = myself.urlify(unprefixed)
            link = "https://api.qrserver.com/v1/create-qr-code/?size=150x150&data="+str(content.lower())
            embed = discord.Embed(
                colour = 0xffffff
            )
            embed.set_author(name="Image not appearing? Try using this link.", url=str(link))
            embed.set_image(url=str(link))
            await message.channel.send(embed=embed)
        if msg.startswith(prefix+'didyoumean'):
            if args[1]=='help':
                embed = discord.Embed(title='didyoumean command help', description='Type like the following\n'+prefix+'didyoumean [text1] [text2]\n\nFor example:\n'+prefix+'didyoumean [i am gay] [i am guy]', colour=discord.Colour.blue())
                embed.set_image(url='https://api.alexflipnote.dev/didyoumean?top=i%20am%20gay&bottom=i%20am%20guy')
            else:
                txt1 = myself.urlify(message.content.split('[')[1][:-2])
                txt2 = myself.urlify(message.content.split('[')[2][:-1])
                embed = discord.Embed(colour=discord.Colour.blue())
                embed.set_image(url='https://api.alexflipnote.dev/didyoumean?top='+str(txt1)+'&bottom='+str(txt2))
            await message.channel.send(embed=embed)
        if msg.startswith(prefix+'challenge'):
            txt = myself.urlify(unprefixed)
            embed = discord.Embed(colour=discord.Colour.blue())
            embed.set_image(url='https://api.alexflipnote.dev/challenge?text='+str(txt))
            await message.channel.send(embed=embed)
        if msg.startswith(prefix+'median') or msg.startswith(prefix+'mean'):
            numArray = []
            i = 1
            try:
                while args[i]!="":
                    numArray.append(args[i])
                    i = int(i)+1
            except IndexError:
                print("Reached the limit.")
            if msg.startswith(prefix+'median'):
                if len(numArray)%2==0:
                    first = int(len(numArray))/2
                    second = int(first)
                    first = int(first)-1
                    result = int(int(numArray[first])+int(numArray[second]))/2
                else:
                    resultPosition = int(len(numArray))-int(((len(numArray))-1)/2)
                    result = numArray[int(resultPosition)-1]
            if msg.startswith(prefix+'mean'):
                temp = 0
                for i in range(0, int(len(numArray))):
                    temp = int(temp)+int(numArray[i])
                result = int(temp)/int(len(numArray))
            await message.channel.send(str(result))
        if msg.startswith(prefix+"sqrt"):
            num = int(args[1])
            await message.channel.send(str(math.sqrt(int(num))))
        if msg.startswith(prefix+'reactnum'):
            emojiArr = ['0️⃣', '1️⃣', '2️⃣', '3️⃣', '4️⃣', '5️⃣', '6️⃣', '7️⃣', '8️⃣', '9️⃣']
            begin = int(args[1])
            end = int(args[2])+1
            errorLevel = 0
            if int(args[1])>10 or int(args[1])<0 or int(args[2])>10 or int(args[2])<0:
                errorLevel = 1
            if errorLevel==0:
                for i in range(int(begin), int(end)):
                    await message.add_reaction(emojiArr[i])
            elif errorLevel==1:
                await message.channel.send(str(client.get_emoji(BotEmotes.error)) + ' | Error: Invalid Integer.')
        if msg.startswith(prefix+'morse') or msg.startswith(prefix+'temmie'):
            if no_args: await message.channel.send(str(client.get_emoji(BotEmotes.error))+' | Please send something to be encoded.')
            else:
                if msg.startswith(prefix+'morse'): link, toenc = 'https://raw.githubusercontent.com/dragonfire535/xiao/master/assets/json/morse.json', list(unprefixed)
                elif msg.startswith(prefix+'temmie'): link, toenc = 'https://raw.githubusercontent.com/dragonfire535/xiao/master/assets/json/temmie.json', unprefixed.split(' ')
                data = myself.jsonisp(link)
                keyz = list(data.keys())
                for i in range(0, len(toenc)):
                    for j in range(0, len(keyz)):
                        toenc[i].replace(keyz[j], data[keyz[j]])
                if msg.startswith(prefix+'morse'): res = ' '.join(toenc)
                else: res = ''.join(toenc)
                await message.channel.send(''.join(toenc))
        if msg.startswith(prefix+'slap'):
            if no_args:
                await message.channel.send(str(client.get_emoji(BotEmotes.error))+" | Slap who? Tag someone!")
            else:
                await message.channel.send(splashes.slap('msg')+', '+message.mentions[0].name+'!\n'+splashes.slap('gif'))
        if msg.startswith(prefix+'fact-core') or msg.startswith(prefix+'fact') or msg.startswith(prefix+'factcore') or msg.startswith(prefix+'fact-sphere') or msg.startswith(prefix+'factsphere'):
            data = myself.jsonisp('https://raw.githubusercontent.com/dragonfire535/xiao/master/assets/json/fact-core.json')
            embed = discord.Embed(title='Fact Core', description=random.choice(data), colour=discord.Colour.green())
            embed.set_thumbnail(url='https://i1.theportalwiki.net/img/thumb/5/55/FactCore.png/300px-FactCore.png')
            await message.channel.send(embed=embed)
        if msg.startswith(prefix+'hbd'):
            if no_args:
                await message.channel.send(str(client.get_emoji(BotEmotes.error))+" | who is having their birthday today?")
            else:
                await message.channel.send("Happy birthday, "+message.mentions[0].name+"!\n"+splashes.hbd())
        if msg.startswith(prefix+'choose'):
            array = []
            i = 1
            try:
                while args[i]!="":
                    array.append(args[i])
                    i = int(i)+1
            except IndexError:
                print("Reached the limit.")
            await message.channel.send(random.choice(array))
        if msg.startswith(prefix+'search'):
            query = myself.urlify(unprefixed)
            searches = [
                "[Google Search](http://google.com/search?q="+str(query),
                "[Google Image Search](https://www.google.com/search?tbm=isch&q="+str(query),
                "[YouTube Search](http://youtube.com/results?q="+str(query),
                "[Wikipedia Search](https://en.wikipedia.org/w/index.php?cirrusUserTesting=control&search="+str(query)+"&title=Special%3ASearch&go=Go&ns0=1",
                "[Instagram Tag Search](https://www.instagram.com/explore/tags/"+str(query),
                "[Creative Commons Search](https://search.creativecommons.org/search?q="+str(query),
                "[WikiHow Search](https://www.wikihow.com/wikiHowTo?search="+str(query),
                "[Stackoverflow Search](https://stackoverflow.com/search?q="+str(query)
            ]
            total = ''
            for i in range(0, len(searches)): total += str(i+1) + '. **' + searches[i] + ')**\n'
            embed = discord.Embed(title = 'Internet Searches for '+str(unprefixed), description=total, color = 0xff0000)
            await message.channel.send(embed=embed)
        if msg.startswith(prefix+'emojify'):
            emojified = []
            emojiid = 0
            listed = list(msg[9:])
            for i in range(0, int(len(listed))):
                a = listed[i]
                if (a.isalpha()) == True:
                    emojified.append(":regional_indicator_"+str(a)+":")
                else:
                    numArr = [":zero:", ":one:", ":two:", ":three:", ":four:", ":five:", ":six:", ":seven:", ":eight:", ":nine:"]
                    if a=="1" or a=="2" or a=="3" or a=="4" or a=="5" or a=="6" or a=="7" or a=="8" or a=="9" or a=="0":
                        emojified.append(numArr[int(a)])
                    elif a=="?":
                        emojified.append(":question:")
                    elif a=="!":
                        emojified.append(":exclamation:")
                    elif a==" ":
                        emojified.append(' ')
                    else:
                        emojiid = 1
            total = ' '.join(emojified)
            if emojiid==0:
                await message.channel.send(total)
            else:
                await message.channel.send(str(client.get_emoji(BotEmotes.error)) + ' | BadSymbolError: Error! You added an invalid symbol\nthat cannot be converted to emojis. Sorry.')
        if args[0]==prefix+'reverse':
            word = msg[9:]
            await message.channel.send(word[::-1])
        if msg.startswith(prefix+'leet'):
            array = list(str(msg)[6:])
            alph = list("abcdefghijklmnopqrstuvwxyz")
            total = []
            leeted = ["4", "6", "(", "cl", "3", "I=", "9", "/-/", "1", ")", "|<", "!", "^^", "^/", "0", "I°", "()_", "l^", "5", "-|_", "V", "VV", "><", "=|", "2", " "]
            for i in range(0, int(len(array))):
                for j in range(0, 28):
                    if array[i] in alph:
                        if array[i]==alph[j]:
                            posId = 0
                            chosePosition = int(j)-1
                            break
                    elif array[i]==" ":
                        posId = 1
                        chosePosition = 26
                        break
                if array[i] in alph and posId==0:
                    total.append(leeted[j])
                elif posId==1:
                    total.append(" ")
                else:
                    total.append(array[i])
            await message.channel.send("".join(total))
        if msg.startswith(prefix+'length'):
            word = str(msg)[8:]
            withSpaces = 0
            withoutSpaces = 0
            for i in range(0, len(word)):
                if list(word)[i]==" ":
                    withSpaces = int(withSpaces)+1
                else:
                    withSpaces = int(withSpaces)+1
                    withoutSpaces = int(withoutSpaces)+1
            await message.channel.send("**With Spaces:** "+str(withSpaces)+"\n**Without Spaces:**"+str(withoutSpaces))
        if msg.startswith(prefix+'randomword'):
            toEdit = await message.channel.send(str(client.get_emoji(BotEmotes.loading)) + ' | Please wait...')
            data = myself.api("https://random-word-api.herokuapp.com/word?number=1")
            await toEdit.edit(content=str(data[0]))
        if msg.startswith(prefix+'inspirobot'):
            img = myself.insp('https://inspirobot.me/api?generate=true')
            embed = discord.Embed(
                colour = 0xff0000
            )
            embed.set_image(url=str(img))
            await message.channel.send(embed=embed)
        if msg.startswith(prefix+'meme'):
            data = myself.api("https://meme-api.herokuapp.com/gimme")
            embed = discord.Embed(
                colour = 0x00ff00
            )
            embed.set_author(name=data["title"], url=data["postLink"])
            if data["nsfw"]:
                embed.set_footer(text='WARNING: IMAGE IS NSFW.')
            else:
                embed.set_image(url=data["url"])
            await message.channel.send(embed=embed)
        if msg.startswith(prefix+'atbash'):
            if no_args:
                await message.channel.send(str(client.get_emoji(BotEmotes.error)) + ' | Invalid. Please give us the word to encode...')
            else:
                await message.channel.send(myself.atbash(unprefixed))
        if msg.startswith(prefix+'caesar'):
            if len(args)<3:
                await message.channel.send(str(client.get_emoji(BotEmotes.error)) +f' | Invalid.\nPlease input:\n`{prefix}caesar [offset] [text]`\nExample: `{prefix}caesar 3 Hello world!`')
            else:
                if args[1].isnumeric()==False:
                    await message.channel.send('That offset is NOT a number!')
                else:
                    try:
                        await message.channel.send(myself.caesar(message.content[int(len(args[0])+len(args[1])+2):], int(args[1])))
                    except Exception as e:
                        await message.channel.send(str(client.get_emoji(BotEmotes.error)) + f' | Error!\n```{e}```Look at dat error tho :flushed:')
        if msg.startswith(prefix+'binary'):
            if no_args:
                await message.channel.send(f'Please send something to encode to binary!\nExample: `{prefix}binary {message.author.name}`')
            else:
                text = unprefixed
                if len(myself.bin(text))>4096:
                    await message.channel.send('The binary result is too long... '+myself.bin('lol uwu'))
                else:
                    await message.channel.send(f'```{myself.bin(text)}```')
        if msg.startswith(prefix+'bored'):
            data = myself.api("https://www.boredapi.com/api/activity?participants=1")
            await message.channel.send('**Feeling bored?**\nWhy don\'t you '+str(data['activity'])+'? :wink::ok_hand:')
        if msg.startswith(prefix+'8ball'):
            data = myself.api("https://yesno.wtf/api")
            if data['answer']=='no':
                colorhex = discord.Colour.red()
            else:
                colorhex = discord.Colour.blue()
            embed = discord.Embed(title=data['answer'], colour=colorhex)
            embed.set_image(url=data['image'])
            await message.channel.send(embed=embed)
        if msg.startswith(prefix+'deathnote'):
            member = []
            in_the_note = ""
            notecount = 0
            membercount = 0
            for i in range(0, int(len(message.guild.members))):
                if message.guild.members[i].name!=message.author.name:
                    member.append(message.guild.members[i].name)
                    membercount = int(membercount) + 1
            chances = ['ab', 'abc', 'abcd']
            strRandomizer = random.choice(chances)
            for i in range(0, int(membercount)):
                if random.choice(list(strRandomizer))=='b':
                    notecount = int(notecount) + 1
                    in_the_note = in_the_note+str(notecount)+'. '+ str(member[i]) + '\n'
            death = random.choice(member)
            count = random.choice(list(range(0, int(membercount))))
            embed = discord.Embed(
                title=message.guild.name+'\'s death note',
                description=str(in_the_note),
                colour = discord.Colour.from_rgb(255, 255, 0)
            )
            await message.channel.send(embed=embed)
        if msg.startswith(prefix+'lovelevel'):
            nums = list(range(0, 100))
            if no_args:
                await message.channel.send(str(client.get_emoji(BotEmotes.error)) + ' | Error: Please mention someone you love (lenny)')
            elif len(args)==2:
                await message.channel.send('Love level of '+message.author.name+' with <@!'+str(args[1][3:][:-1])+'> is **'+str(random.choice(nums))+'%.**')
        if msg.startswith(prefix+'gaylevel'):
            if no_args:
                await message.channel.send(str(client.get_emoji(BotEmotes.error)) + ' | SomeoneError: Say/mention someone!')
            else:
                nums = list(range(0, 101))
                await message.channel.send('The gayness level of '+msg[10:]+' is **'+str(random.choice(nums))+'%.**')
        if msg.startswith(prefix+'secret'):
            member = []
            for i in range(0, int(len(message.guild.members))):
                if message.guild.members[i].name!=message.author.name and message.guild.members[i].name!=message.author.name:
                    member.append(message.guild.members[i].name)
            secretlist = splashes.getSecrets()
            await message.author.send('Did you know?\n'+random.choice(member)+str(random.choice(secretlist))+'\nDon\'t tell this to anybody else.')
            await message.channel.send('I shared the secret through DM. don\'t show anyone else! :wink::ok_hand:')
        if msg.startswith(prefix+'reactmsg'):
            messageReact = list(msg[10:])
            used = []
            order = list("abcdefghijklmnopqrstuvwxyz!?0123456789 ")
            validId = 0
            emo = ["🇦", "🇧", "🇨", "🇩", "🇪", "🇫", "🇬", "🇭", "🇮", "🇯", "🇰", "🇱", "🇲", "🇳", "🇴", "🇵", "🇶", "🇷", "🇸", "🇹", "🇺", "🇻", "🇼", "🇽", "🇾", "🇿", "❗", "❓", '0️⃣', '1️⃣', '2️⃣', '3️⃣', '4️⃣', '5️⃣', '6️⃣', '7️⃣', '8️⃣', '9️⃣', '▪️']
            if len(messageReact)<20:
                for i in range(0, int(len(messageReact))):
                    if messageReact[i] in used:
                        await message.channel.send(str(client.get_emoji(BotEmotes.error)) + ' | Error: Your message contain multiple characters. Which is not allowed on reactions.')
                        validId = 1
                        break
                    else:
                        if messageReact[i] in order:
                            for j in range(0, int(len(order))):
                                if messageReact[i]==str(order[j]):
                                    used.append(emo[j])
                        else:
                            await message.channel.send(str(client.get_emoji(BotEmotes.error)) + ' | Error: Your message contain invalid symbols.\nValid: Alphabet Number ? ! space')
                            break
            else:
                await message.channel.send(str(client.get_emoji(BotEmotes.error)) + ' | Error! Your message contain more than 20 characters.\nWhich is the react message limit.')
            if validId==0:
                for i in range(0, int(len(used))):
                    await message.add_reaction(used[i])
        if msg.startswith(prefix+'wonka') or msg.startswith(prefix+'avmeme') or msg.startswith(prefix+'buzz') or msg.startswith(prefix+'doge') or msg.startswith(prefix+'fry') or msg.startswith(prefix+'philosoraptor') or msg.startswith(prefix+'money'):
            if msg.startswith(prefix+'avmeme'):
                try:
                    av = message.mentions[0].avatar_url
                    mes = myself.urlify(message.content[int(len(args[0])+len(args[1])+1):])
                    top = mes.split('[')[1].split(']')[0]
                    bott = mes.split('[')[2].split(']')[0]
                    name = 'custom'
                    extr = '?alt='+str(av).replace('webp', 'png')
                    embed = discord.Embed(colour=discord.Colour.green())
                    print('https://memegen.link/'+str(name)+'/'+str(top)+'/'+str(bott)+'.jpg'+str(extr))
                    embed.set_image(url='https://memegen.link/'+str(name)+'/'+str(top)+'/'+str(bott)+'.jpg'+str(extr))
                    await message.channel.send(embed=embed)
                except Exception as e:
                    await message.channel.send(str(client.get_emoji(BotEmotes.error)) +f' | Error!\n```{e}```Invalid parameters. Example: `{prefix}avmeme <tag someone> [top text] [bottom text]`')
            else:
                try:
                    mes = myself.urlify(unprefixed)
                    top = mes.split('[')[1].split(']')[0]
                    bott = mes.split('[')[2].split(']')[0]
                    name = args[0][1:]
                    embed = discord.Embed(colour=discord.Colour.green())
                    embed.set_image(url='https://memegen.link/'+str(name)+'/'+str(top)+'/'+str(bott)+'.jpg?watermark=none')
                    await message.channel.send(embed=embed)
                except Exception as e:
                    await message.channel.send(str(client.get_emoji(BotEmotes.error)) +f' | Error!\n```{e}```Invalid parameters.')
        if msg.startswith(prefix+'barcode'):
            if no_args:
                await message.channel.send('Please provide a text!')
            else:
                if '/' in msg or '?' in msg:
                    await message.channel.send('Please input one without `/` or `?`!')
                else:
                    embed = discord.Embed(title='Barcode for '+str(msg[int(len(args[0])+1):]), colour=discord.Colour.blue())
                    embed.set_image(url='http://www.barcode-generator.org/zint/api.php?bc_number=20&bc_data='+str(myself.urlify(unprefixed)))
                    await message.channel.send(embed=embed)
        if msg.startswith(prefix+'weather'):
            if no_args:
                await message.channel.send(f'Please send a **City name!**\nExample: `{prefix}weather New York`')
            else:
                embed = discord.Embed(
                    title='Weather Report in '+str(msg[int(len(args[0])+1):]),
                    colour=discord.Colour.blue()
                )
                embed.set_image(url='https://wttr.in/'+str(myself.urlify(unprefixed))+'.png?m')
                await message.channel.send(embed=embed)
        if msg.startswith(prefix+'github'):
            git = ''
            for i in range(0, len(github_object['files'])):
                git = git + '**'+github_object['files'][i]['name']+'** = '+github_object['files'][i]['type']+'\n'
            embed = discord.Embed(
                title=splashes.getGitMsg(),
                description='To visit my github, [Click this link.](http://github.com/vierofernando/username601).\nYou as a dev can see *how bad i am at programming, detect codes that i copied from stackoverflow, and probably copy-paste my bot\'s code to your bot :wink:*\n\n'+str(git),
                colour=discord.Colour.red()
            )
            await message.channel.send(embed=embed)
        if msg.startswith(prefix+'quote'):
            data = myself.insp('https://quotes.herokuapp.com/libraries/math/random')
            text = data.split(' -- ')[0]
            quoter = data.split(' -- ')[1]
            embed = discord.Embed(title='Quotes', description=text+'\n\n - '+quoter+' - ', colour=discord.Colour.blue())
            await message.channel.send(embed=embed)
        if msg.startswith(prefix+'trivia'):
            al = None
            try:
                wait = await message.channel.send(str(client.get_emoji(BotEmotes.loading)) + ' | Please wait... generating quiz...')
                auth = message.author
                data = myself.api('https://wiki-quiz.herokuapp.com/v1/quiz?topics=Science')
                q = random.choice(data['quiz'])
                choices = ''
                for i in range(0, len(q['options'])):
                    al = list('🇦🇧🇨🇩')
                    if q['answer']==q['options'][i]:
                        corr = al[i]
                    choices = choices + al[i] +' '+ q['options'][i]+'\n'
                embed = discord.Embed(title='Trivia!', description='**'+q['question']+'**\n'+choices, colour=discord.Colour.green())
                embed.set_footer(text='Answer by clicking the reaction! You have 60 seconds.')
                await wait.edit(content='', embed=embed)
                for i in range(0, len(al)):
                    await wait.add_reaction(al[i])
            except Exception as e:
                await wait.edit(content=str(client.get_emoji(BotEmotes.error)) + f' | An error occured!\nReport this using {prefix}feedback.\n```{e}```')
            guy = message.author
            def check(reaction, user):
                return user == guy
            try:
                reaction, user = await client.wait_for('reaction_add', timeout=60.0, check=check)
            except asyncio.TimeoutError:
                await main.add_reaction('😔')
            if str(reaction.emoji)==str(corr):
                await message.channel.send(str(client.get_emoji(BotEmotes.success)) +' | <@'+str(guy.id)+'>, Congrats! You are correct. :partying_face:')
            else:
                await message.channel.send(str(client.get_emoji(BotEmotes.error)) +' | <@'+str(guy.id)+'>, You are incorrect. The answer is '+str(corr)+'.')
        if msg.startswith(prefix+'rhyme'):
            if no_args:
                await message.channel.send('Please input a word! And we will try to find the word that best rhymes with it.')
            else:
                wait = await message.channel.send(str(client.get_emoji(BotEmotes.loading)) + ' | Please wait... Searching...')
                data = myself.api('https://rhymebrain.com/talk?function=getRhymes&word='+str(myself.urlify(unprefixed)))
                words = ''
                if len(data)<1:
                    await wait.edit(content='We did not find any rhyming words corresponding to that letter.')
                else:
                    for i in range(0, len(data)):
                        if data[i]['flags']=='bc':
                            words = words + data[i]['word']+ ', '
                    if len(words)>1950:
                        await wait.edit(content=str(client.get_emoji(BotEmotes.error)) + ' | There seemed to be *so many* words to be listed. Sorry.')
                    else:
                        embed = discord.Embed(title='Words that rhymes with '+msg[int(len(args[0])+1):]+':', description=words, colour=discord.Colour.blue())
                        await wait.edit(content='', embed=embed)
print('Logging in to discord...')
client.run(fetchdata['DISCORD_TOKEN'])
