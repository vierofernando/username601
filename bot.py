# LOCAL FILES
from modules.username601 import *
import modules.username601 as myself
import modules.discordgames as Games
import modules.splashes as src
import modules.canvas as Painter

# EXTERNAL PACKAGES
import os
from inspect import isawaitable
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
ia = imdb.IMDb()
client = commands.Bot(command_prefix=Config.prefix)
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
    if member.guild.id==Config.SupportServer.id:
        await member.guild.get_channel(Config.SupportServer.logging).send(':heart: | '+src.welcome('<@'+str(member.id)+'>', client.get_user(Config.owner.id).name))

# ONLY IN SUPPORT SERVER ALSO
@client.event
async def on_member_remove(member):
    if member.guild.id==Config.SupportServer.id:
        await member.guild.get_channel(Config.SupportServer.logging).send(':broken_heart: | '+src.exit(member.name))

@client.event
async def on_message(message):
    no_args, msg, args = False, message.content.lower(), message.content.split(' ')
    unprefixed = message.content[int(len(args[0])+1):]
    if message.author.bot==False and msg.startswith('<@!'+str(Config.id)+'>'):
        await message.channel.send('The prefix is `'+prefix+'`.\n**Commands: **`'+prefix+'help`')
    if len(args)==1: no_args = True
    if myself.accept_message(message.author.id, message.author.bot, msg):
        if cmd(msg, 'ping'):
            ping = str(round(client.latency*1000))
            if int(ping)<100:
                embed = discord.Embed(title=f'Pong! {ping} ms.', colour=discord.Colour.from_rgb(123, 63, 0))
            else:
                embed = discord.Embed(title=f'Pong! {ping} ms.', description='Ping time may be slower due to;\n1. People kept spamming me\n2. My hosting system is slow\n3. I am in too many servers\n4. Discord\'s servers are currectly down\n5. I am snail :snail:', colour=discord.Colour.from_rgb(123, 63, 0))
            embed.set_thumbnail(url='https://i.pinimg.com/originals/21/02/a1/2102a19ea556e1d1c54f40a3eda0d775.gif')
            embed.set_footer(text='Ping and embed sent time may differ.')
            await message.channel.send(embed=embed)
        if cmd(msg, 'say'):
            await message.channel.send(unprefixed)
        if cmd(msg, 'hack'):
            if no_args:
                await message.channel.send(f'Please tag someone!\nExample: {prefix}hack <@'+str(message.author.id)+'>')
            else:
                tohack = message.mentions[0]
                console = 'C:\\Users\\Anonymous601>'
                if args[1].startswith('<@'):
                    main = await message.channel.send('Opening Console...')
                    flow = src.hackflow(tohack)
                    for i in range(0, len(flow)):
                        console = console + flow[i][1:]
                        newembed = discord.Embed(title='Anonymous601 Hacking Console', description=f'```{console}```',colour=discord.Colour.from_rgb(123, 63, 0))
                        newembed.set_thumbnail(url=myself.hackfind(flow[i], tohack.avatar_url))
                        await main.edit(content='', embed=newembed)
                        await asyncio.sleep(random.randint(2, 4))
                else:
                    console = console + 'hack.exe -u '+str(message.author.name)+'ERROR: INVALID TAG.\nACCESS DENIED.\n\nHash encoded base64 cipher code:\n'+myself.bin(message.author.name)+ '\n' + console
                    embed = discord.Embed(title='Anonymous601 Hacking Console', description=f'```{console}```',colour=discord.Colour.from_rgb(123, 63, 0))
                    await message.channel.send(embed=embed)
        if cmd(msg, 'base64'):
            if no_args:
                await message.channel.send(f'Please input something to encode! Like `{prefix}base64 discord.py is better than discord.js`')
            else:
                await message.channel.send(f'```{myself.encodeb64(unprefixed)}```')
        if cmd(msg, 'ufo'):
            num = str(random.randint(50, 100))
            data = myself.api('http://ufo-api.herokuapp.com/api/sightings/search?limit='+num)
            if data['status']!='OK':
                await message.channel.send('There was a problem on retrieving the info.\nThe server said: "'+str(data['status'])+'" :eyes:')
            else:
                ufo = random.choice(data['sightings'])
                embed = discord.Embed(title='UFO Sighting in '+str(ufo['city'])+', '+str(ufo['state']), description='**Summary:** '+str(ufo['summary'])+'\n\n**Shape:** '+str(ufo['shape'])+'\n**Sighting Date: **'+str(ufo['date'])[:-8].replace('T', ' ')+'\n**Duration: **'+str(ufo['duration'])+'\n\n[Article Source]('+str(ufo['url'])+')', colour=discord.Colour.from_rgb(123, 63, 0))
                embed.set_footer(text='Username601 raided Area 51 and found this!')
                await message.channel.send(embed=embed)
        if cmd(msg, 'rotate'):
            async with message.channel.typing():
                if len(message.mentions)==0: ava = str(message.author.avatar_url).replace('.webp?size=1024', '.jpg?size=512')
                else: ava = str(message.mentions[0].avatar_url).replace('.webp?size=1024', '.jpg?size=512')
                data = Painter.gif.rotate(ava)
                await message.channel.send(file=discord.File(data, 'rotate.gif'))
        if cmd(msg, 'changemymind') or cmd(msg, 'changedmymind'):
            if no_args: await message.channel.send(str(client.get_emoji(BotEmotes.error))+" | Error! You need a text...")
            else:
                await message.add_reaction(client.get_emoji(BotEmotes.loading))
                async with message.channel.typing():
                    try:
                        data = Painter.urltoimage('https://nekobot.xyz/api/imagegen?type=changemymind&text='+myself.urlify(unprefixed)+'&raw=1')
                        await message.channel.send(file=discord.File(data, 'changemymind.png'))
                    except Exception as e:
                        await message.channel.send(str(client.get_emoji(BotEmotes.error))+" | Oops! There was an error on generating your meme; `"+str(e)+"`")
        if cmd(msg, 'triggered'):
            increment, accept = None, True
            for i in args:
                if i.isnumeric():
                    increment = int(i)
                    break
            if increment==None: increment = 5
            if increment!=5:
                if increment<1: 
                    accept = False
                    await message.channel.send(str(client.get_emoji(BotEmotes.error)) + " | Increment to small!")
                elif increment>50:
                    accept = False
                    await message.channel.send(str(client.get_emoji(BotEmotes.error)) + " | Increment to big!")
            if accept:
                if len(message.mentions)==0: ava = str(message.author.avatar_url).replace('.webp?size=1024', '.jpg?size=512')
                else: ava = str(message.mentions[0].avatar_url).replace('.webp?size=1024', '.jpg?size=512')
                async with message.channel.typing():
                    data = Painter.gif.triggered(ava, increment)
                    await message.channel.send(file=discord.File(data, 'triggered.gif'))
        if cmd(msg, 'stonks') or cmd(msg, 'pabloescobar') or cmd(msg, 'immaheadout') or cmd(msg, 'homer') or cmd(msg, 'monkeypuppet') or cmd(msg, 'tom') or cmd(msg, 'surprisedpikachu') or cmd(msg, 'meandtheboys'):
            if no_args: await message.channel.send(str(client.get_emoji(BotEmotes.error))+" | Where is the meme's context?")
            else:
                async with message.channel.typing():
                    try:
                        data = Painter.simpleTopMeme(unprefixed, './assets/pics/'+args[0][1:]+'.jpg', 40, 3)
                        fileName = args[0][1:]+'.png'
                        await message.channel.send(file=discord.File(data, fileName))
                    except Exception as e:
                        await message.channel.send('Oopsies! There was an error on creating your chosen meme;\n'+str(e))
        if cmd(msg, 'presentation') or cmd(msg, 'firstwords'):
            if no_args: await message.channel.send(str(client.get_emoji(BotEmotes.error))+" | Where is the meme's context?")
            else:
                async with message.channel.typing():
                    try:
                        if cmd(msg, 'presentation'): data = Painter.presentationMeme(unprefixed, "./assets/pics/presentation.jpg")
                        elif cmd(msg, 'firstwords'): data = Painter.firstwords(unprefixed, "./assets/pics/firstwords.jpg")
                        await message.channel.send(file=discord.File(data, args[0][1:]+'.png'))
                    except Exception as e:
                        await message.channel.send('Oopsies! There was an error on creating your chosen meme;\n'+str(e))
        if cmd(msg, 'embed'):
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
        if args[0]==prefix+'wanted' or args[0]==prefix+'window' or args[0]==prefix+'frame' or args[0]==prefix+'art' or args[0]==prefix+'sacred' or args[0]==prefix+'coffindance' or args[0]==prefix+'ferbtv' or args[0]==prefix+'chatroulette':
            async with message.channel.typing():
                if len(message.mentions)<1:
                    ava = str(message.author.avatar_url).replace('.webp?size=1024', '.jpg?size=512')
                else:
                    ava = str(message.mentions[0].avatar_url).replace('.webp?size=1024', '.jpg?size=512')
                if 'wanted' in args[0]: num1, num2, num3, num4 = 547, 539, 167, 423
                elif 'ferbtv' in args[0]: num1, num2, num3, num4 = 362, 278, 363, 187
                elif 'chatroulette' in args[0]: num1, num2, num3, num4 = 324, 243, 14, 345
                elif 'sacred' in args[0]: num1, num2, num3, num4 = 454, 498, 1210, 986
                elif 'coffindance' in args[0]: num1, num2, num3, num4 = 220, 228, 421, 58
                elif 'frame' in args[0]: num1, num2, num3, num4, ava = 1025, 715, 137, 141, str(ava).replace("=512", "=1024")
                elif 'window' in args[0]: num1, num2, num3, num4 = 219, 199, 4, 21
                if 'art' not in args[0]:
                    image = Painter.putimage(ava, args[0][1:], num1, num2, num3, num4)
                else:
                    image = Painter.art(ava)
                await message.channel.send(file=discord.File(image, args[0][1:]+'.png'))
        if cmd(msg, 'resize'):
            correct = ''
            wh = []
            for i in args:
                if i.isnumeric():
                    correct += 'y'
                    wh.append(int(i))
            async with message.channel.typing():
                if correct=='yy':
                    if len(message.mentions)<1:
                        ava = str(message.author.avatar_url).replace('.webp?size=1024', '.jpg?size=512')
                    else:
                        ava = str(message.mentions[0].avatar_url).replace('.webp?size=1024', '.jpg?size=512')
                    if wh[0]>2000 or wh[1]>2000: await message.channel.send(str(client.get_emoji(BotEmotes.error)) + " | Your image is too big!")
                    elif wh[0]<300 or wh[1]<300: await message.channel.send(str(client.get_emoji(BotEmotes.error)) + " | Your image is too small!")
                    else:
                        data = Painter.resize(ava, wh[0], wh[1])
                        await message.channel.send(file=discord.File(data, 'resize.png'))
                else:
                    await message.channel.send(str(client.get_emoji(BotEmotes.error)) + " | Where are the parameters?")
        if cmd(msg, 'pokequiz'):
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
                newembed = discord.Embed(title='Pokemon Quiz!', description=f'Guess the pokemon\'s name!\nTimeout: 45 seconds.\nHint left: **{str(hint)}** | Attempts left: **{str(attempt)}**', colour=discord.Colour.from_rgb(123, 63, 0))
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
        if cmd(msg, 'ss'):
            if len(args)>1:
                if args[1]=='--help':
                    embed = discord.Embed(title='Special say command help', description='**REQUIRES `MANAGE CHANNELS` PERMISSION**\nThis is a special say command that has the following:\n1. @someone | Tags random people in the server. [On April fools 2018, Discord made this feature, but removed the day after.](https://www.youtube.com/watch?v=BeG5FqTpl9U) (Please use wisely.)\n2. @owner | Tags the server owner. Please don\'t spam this feature.\n3. --ch #{channelname} | Sends a message on a specific channel.', colour=discord.Colour.from_rgb(123, 63, 0))
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
        if cmd(msg, 'inspectservers'):
            if int(message.author.id)==Config.owner.id:
                ee = ''
                for i in range(0, len(client.guilds)):
                    ee = ee + '**' + client.guilds[i].name + '** ('+str(len(client.guilds[i].members))+' Members)\n'
                embed = discord.Embed(title='Heya, here are all the servers i am in.', description=ee, colour=discord.Colour.from_rgb(123, 63, 0))
                await message.author.send(embed=embed)
                await message.channel.send('...k')
            else:
                await message.channel.send('...')
        if cmd(msg, 'pandafact') or cmd(msg, 'birdfact') or cmd(msg, 'birbfact'):
            if cmd(msg, 'pandafact'): link = 'https://some-random-api.ml/facts/panda'
            else: link = 'https://some-random-api.ml/facts/bird'
            data = myself.jsonisp(link)['fact']
            await message.channel.send(embed=discord.Embed(title='Did you know?', description=data, colour=discord.Colour.from_rgb(123, 63, 0)))
        if cmd(msg, 'iss'):
            iss = myself.jsonisp('https://open-notify-api.herokuapp.com/iss-now.json')
            ppl = myself.jsonisp('https://open-notify-api.herokuapp.com/astros.json')
            total = '```'
            for i in range(0, len(ppl['people'])):
                total += str(i+1) + '. ' + ppl['people'][i]['name'] + ((20-(len(ppl['people'][i]['name'])))*' ') + ppl['people'][i]['craft'] + '\n'
            embed = discord.Embed(title='Position: '+str(iss['iss_position']['latitude'])+' '+str(iss['iss_position']['longitude']), description='**People at craft:**\n\n'+str(total)+'```', colour=discord.Colour.from_rgb(123, 63, 0))
            await message.channel.send(embed=embed)
        if cmd(msg, 'qotd'):
            data = myself.jsonisp('https://quotes.rest/qod')['contents']['quotes'][0]
            embed = discord.Embed(title=data['quote'], description=data['author'], color=discord.Colour.from_rgb(123, 63, 0))
            embed.set_image(url=data['background'])
            embed.set_footer(text='New quote will be generated in the next day.')
            await message.channel.send(embed=embed)
        if cmd(msg, 'pika') or args[0]==prefix+'panda' or cmd(msg, 'redpanda'):
            if cmd(msg, 'pika'): link, col, msg = "https://some-random-api.ml/pikachuimg", discord.Colour.from_rgb(255, 255, 0), 'pika pika!'
            elif cmd(msg, 'redpanda'): link, col, msg = "https://some-random-api.ml/img/red_panda", discord.Colour.from_rgb(123, 63, 0), 'Ok, here are some pics of red pandas.'
            else: link, col, msg = "https://some-random-api.ml/img/panda", discord.Colour.from_rgb(123, 63, 0), 'Here is some cute pics of pandas.'
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
        if cmd(msg, 'hangman'):
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
                newembed = discord.Embed(title=''.join(main_guess_hid), description='Wrong guesses: '+str(wrong_guesses), colour=discord.Colour.from_rgb(123, 63, 0))
                newembed.set_image(url=f'https://raw.githubusercontent.com/vierofernando/username601/master/assets/pics/hangman_{str(level)}.png')
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
        if cmd(msg, 'tictactoe'):
            box_nums = list('123456789')
            can_used = list('123456789')
            box = f' {box_nums[0]} | {box_nums[1]} | {box_nums[2]}\n===========\n {box_nums[3]} | {box_nums[4]} | {box_nums[5]}\n===========\n {box_nums[6]} | {box_nums[7]} | {box_nums[8]}\n'
            if no_args:
                embed = discord.Embed(title='TicTacToe™ wtih '+str(src.getTicTacToeHeader()), description=f'Plays tic-tac-toe with the BOT. Very simple.\n\n**To start playing, type;**\n`{prefix}tictactoe X` (To play tictactoe as X)\n`{prefix}tictactoe O` (To play tictactoe as O)', colour=discord.Colour.from_rgb(123, 63, 0))
                embed.set_image(url='https://raw.githubusercontent.com/vierofernando/username601/master/assets/pics/tictactoe.png')
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
                    embed = discord.Embed(title='Playing Tictactoe with '+str(user_name), description=f'Viero Fernando ({user_sym}) | Username601 ({bot_sym})\nType the numbers to fill out the boxes.```{box}```', colour=discord.Colour.from_rgb(123, 63, 0))
                    embed.set_footer(text='Type "endgame" to well, end the game. Or wait for 20 seconds and the game will kill itself! ;)')
                    gameview = await message.channel.send(embed=embed)
                    while gameplay==True:
                        if Games.checkWinner(box_nums, user_sym, bot_sym)=='userwin':
                            await message.channel.send(f'Congrats <@{user_id}>! You won against me! :tada:')
                            gameplay = False
                            break
                        elif Games.checkWinner(box_nums, user_sym, bot_sym)=='botwin':
                            await message.channel.send(f'LOL, i win the tic tac toe! :tada:\nYou lose! :pensive:')
                            gameplay = False
                            break
                        elif Games.checkEndGame(can_used)==True:
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
                            newembed = discord.Embed(title='Playing Tictactoe with '+str(user_name), description=f'Viero Fernando ({user_sym}) | Username601 ({bot_sym})\nType the numbers to fill out the boxes.```{box}```', colour=discord.Colour.from_rgb(123, 63, 0))
                            newembed.set_footer(text='Type "endgame" to well, end the game. Or wait for 20 seconds and the game will kill itself! ;)')
                            await message.channel.send(embed=newembed)
                        elif str(trying.content).lower()=='endgame':
                            await message.channel.send('Game ended.')
                            gameplay = False
                            break
        if cmd(msg, 'randomavatar'):
            gibb_name = ''
            for i in range(0, random.randint(5, 10)):
                gibb_name += random.choice(list('ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz'))
            url=f'https://api.adorable.io/avatars/285/{gibb_name}.png'
            await message.channel.send(file=discord.File(Painter.urltoimage(url), 'random_avatar.png'))
        if cmd(msg, 'mathquiz'):
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
        if cmd(msg, 'guessavatar'):
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
                    embed = discord.Embed(title='What does the avatar below belongs to?', description=':eyes: Click the reactions! **You have 20 seconds.**\n\n'+str(question), colour=discord.Colour.from_rgb(123, 63, 0))
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
        if cmd(msg, 'geoquiz'):
            wait = await message.channel.send(str(client.get_emoji(BotEmotes.loading)) + ' | Please wait... generating question...')
            data = myself.api("https://restcountries.eu/rest/v2/")
            topic = random.choice(src.getGeoQuiz())
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
            embed = discord.Embed(title='Geography: '+str(topic)+' quiz!', description=':nerd: Click on the reaction! **You have 20 seconds.**\n\nWhich '+str(topic)+' belongs to '+str(chosen_nation['name'])+'?\n'+str(question), colour=discord.Colour.from_rgb(123, 63, 0))
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
        if cmd(msg, 'emojiimg'):
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
                if accept:
                    await message.channel.send(file=discord.File(Painter.urltoimage(link), 'emoji.png'))
            else:
                await message.channel.send(str(client.get_emoji(BotEmotes.error)) +' | Invalid parameters.')
        if cmd(msg, 'ban'):
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
        if cmd(msg, 'rp'):
            if message.author.id==Config.owner.id:
                try:
                    user_to_send = client.get_user(int(args[1]))
                    em = discord.Embed(title="Hi, "+user_to_send.name+"! the bot owner sent a response for your feedback.", description=str(message.content[int(len(args[0])+len(args[1])+2):]), colour=discord.Colour.from_rgb(123, 63, 0))
                    em.set_footer(text="Feeling unsatisfied? Then join our support server! ('+str(Config.SupportServer.invite)+')")
                    await user_to_send.send(embed=em)
                    await message.add_reaction('✅')
                except Exception as e:
                    await message.channel.send(str(client.get_emoji(BotEmotes.error)) + f' | Error: `{e}`')
            else:
                await message.channel.send('You are not the bot owner.')
        if cmd(msg, 'feedback'):
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
                            await wait.edit(content='', embed=discord.Embed(title='You are banned', description='Sorry! you are banned from using the `'+prefix+'feedback` command. Reason:```'+i.split('REASON:"')[1].split('"')[0]+'```', colour=discord.Colour.from_rgb(123, 63, 0)))
                            banned = True
                            break
                if not banned:
                    try:
                        fb = unprefixed
                        feedbackCh = client.get_channel(706459051034279956)
                        await feedbackCh.send('<@Config.owner.id>, User with ID: '+str(message.author.id)+' sent a feedback: **"'+str(fb)+'"**')
                        embed = discord.Embed(title='Feedback Successful', description=str(client.get_emoji(BotEmotes.success)) + '** | Success!**\nThanks for the feedback!\n**We will DM you as the response. **If you are unsatisfied, [Join our support server and give us more details.]('+str(Config.SupportServer.invite)+')',colour=discord.Colour.from_rgb(123, 63, 0))
                        await wait.edit(content='', embed=embed)
                    except:
                        await wait.edit(content=str(client.get_emoji(BotEmotes.error)) + ' | Error: There was an error while sending your feedback. Sorry! :(')
        if cmd(msg, 'fbban'):
            if message.channel.id==706459051034279956 and int(message.author.id)==Config.owner.id:
                await message.channel.send('Banned user with ID of: ['+str(args[1])+'] REASON:"'+str(message.content[int(len(args[0])+len(args[1])+2):])+'"')
            else:
                await message.channel.send(str(client.get_emoji(BotEmotes.error)) +' | Invalid channel/user.')
        if cmd(msg, 'gdlevel'):
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
                            colour = discord.Colour.from_rgb(123, 63, 0)
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
        if cmd(msg, 'gdsearch'):
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
                    embedy = discord.Embed(title='Geometry Dash Level searches for "'+str(unprefixed)+'":', description=levels, colour=discord.Colour.from_rgb(123, 63, 0))
                    await message.channel.send(embed=embedy)
                except:
                    await message.channel.send(str(client.get_emoji(BotEmotes.error)) + ' | Error: Not Found. :four::zero::four:')
        if cmd(msg, 'emojiinfo'):
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
                    embedy = discord.Embed(title='Emoji info for :'+str(data.name)+':', description='**Emoji name:** '+str(data.name)+'\n**Emoji ID: **'+str(data.id)+'\n'+anim+'\n**Emoji\'s server ID: **'+str(data.guild_id)+'\n**Emoji creation time: **'+str(data.created_at)[:-7]+' UTC.', colour=discord.Colour.from_rgb(123, 63, 0))
                    embedy.set_thumbnail(url='https://cdn.discordapp.com/emojis/'+str(data.id)+'.png?v=1')
                    await message.channel.send(embed=embedy)
        if args[0]==prefix+'threats' or args[0]==prefix+'deepfry' or args[0]==prefix+'blurpify':
            if no_args:
                await message.channel.send('Please tag someone!')
            else:
                async with message.channel.typing():
                    if args[0].startswith(prefix+'threat'): inputtype = 'url'
                    else: inputtype = 'image'
                    av = message.mentions[0].avatar_url
                    url='https://nekobot.xyz/api/imagegen?type='+str(args[0])[1:]+'&'+inputtype+'='+str(av)[:-15]+'.png&raw=1'
                    await message.channel.send(file=discord.File(Painter.urltoimage(url), 'threat.png'))
        if args[0]==prefix+'clyde' or args[0]==prefix+'trumptweet' or args[0]==prefix+'kannagen':
            if no_args: await message.channel.send('Please input a text...')
            else:
                async with message.channel.typing():
                    url='https://nekobot.xyz/api/imagegen?type='+str(args[0][1:])+'&text='+myself.urlify(str(unprefixed))+'&raw=1'
                    await message.channel.send(file=discord.File(Painter.urltoimage(url), 'clyde.png'))
        if cmd(msg, 'clear') or cmd(msg, 'purge'):
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
            if int(message.author.id)==Config.owner.id:
                command = unprefixed
                try:
                    res = eval(command)
                    if isawaitable(res):
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
            if message.author.guild_permissions.manage_guild==True or int(message.author.id)==Config.owner.id:
                accept = True
            else:
                await message.channel.send(str(client.get_emoji(BotEmotes.error)) +' | <@'+str(message.author.id)+'>, You need to have the MANAGE SERVER permission or  be the bot owner to do this command.\nTo be the bot owner, try creating a bot :v')
                accept = False
            if accept==True:
                await message.channel.send(message.content[3:])
        if cmd(msg, 'addrole') or args[0]==prefix+'ar':
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
        if cmd(msg, 'xpbox'):
            await message.channel.send("this command has been closed for maintenance. sorry.")
            # results = []
            # buttons = []
            # ques = [
            #     'Please input the box title.',
            #     'Please input the message to display.',
            #     'How many buttons shall be in the message box?'
            # ]
            # auth = message.author
            # accept = True
            # for i in range(0, 3):
            #     await message.channel.send(ques[i])
            #     def check(m):
            #         return m.author == auth
            #     try:
            #         trying = await client.wait_for('message', check=check, timeout=30.0)
            #     except:
            #         await message.channel.send('Command canceled. No response after 30 seconds.')
            #     if '/' in str(trying.content) or '?' in str(trying.content) or '&' in str(trying.content):
            #         await message.channel.send(str(client.get_emoji(BotEmotes.error)) +' | Your request contain an invalid symbol. Please try again.')
            #         accept = False
            #         break
            #     else:
            #         results.append(str(trying.content))
            #         if len(results)>2:
            #             for i in range(1, results[3]+1):
            #                 nds = ['st', 'nd', 'rd']
            #                 await message.channel.send('Please input the '+str(i)+str(nds[i-1])+' button.')
            #                 def checkingagain(m):
            #                     return m.author == auth
            #                 try:
            #                     buttonInput = await client.wait_for('message', check=checkingagain, timeout=30.0)
            #                 except:
            #                     await message.channel.send('Command canceled. No response after 30 seconds.')
            #                     accept = False
            #                     break
            #                 buttons.append(str(trying.content))
            # if accept==True:
            #     embed = discord.Embed(title='Error!', colour=discord.Colour.from_rgb(123, 63, 0))
            #     embed.set_image(url='http://atom.smasher.org/error/xp.png.php?icon=Error3&style=xp&title='+str(results[0]).replace(' ', '+')+'&text='+str(results[1]).replace(' ', '+')+'&b1='+str(results[2]).replace(' ', '+'))
            #     await message.channel.send(embed=embed)
        if cmd(msg, 'removerole') or args[0]==prefix+'rr':
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
        if cmd(msg, 'permission') or msg.startswith('perms'):
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
                    permissionsEmbed = discord.Embed(title='User permissions for '+str(message.mentions[0].name)+';', description=str(perm), colour=discord.Colour.from_rgb(123, 63, 0))
                    await message.channel.send(embed=permissionsEmbed)
                except Exception as e:
                    await message.channel.send(str(client.get_emoji(BotEmotes.error)) +' | elol. we have an elol here:```'+str(e)+'```')
        if cmd(msg, 'makechannel'):
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
        if cmd(msg, 'kick'):
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
        if cmd(msg, 'nick'):
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
        if cmd(msg, 'imdb'):
            wait = await message.channel.send(str(client.get_emoji(BotEmotes.loading)) + ' | Please wait...')
            if no_args or args[1]=='help' or args[1]=='--help':
                embed = discord.Embed(title='IMDb command help', description='Searches through the IMDb Movie database.\n{} are Parameters that is **REQUIRED** to get the info.\n\n', colour=discord.Colour.from_rgb(123, 63, 0))
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
                            embed = discord.Embed(title='IMDb Top '+str(num)+':', description=str(total), colour=discord.Colour.from_rgb(123, 63, 0))
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
                    embed = discord.Embed(title=data['title'], colour=discord.Colour.from_rgb(123, 63, 0))
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
                    errorQuick = discord.Embed(title=data['title'], colour=discord.Colour.from_rgb(123, 63, 0))
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
                embed = discord.Embed(title=main_name.lower()+' search for "'+str(query)+'":', description=str(lists), colour=discord.Colour.from_rgb(123, 63, 0))
                if main_name=='MOVIE':
                    embed.set_footer(text='Type '+prefix+'imdb --'+str(main_name.lower())+' {'+main_name+'_ID} to show each info.')
                await wait.edit(content='', embed=embed)
        if cmd(msg, 'dogfact'):
            fact = myself.api('https://dog-api.kinduff.com/api/facts')
            if fact['success']!=True:
                desc = str(client.get_emoji(BotEmotes.error)) + ' | Error getting the fact.'
            else:
                desc = fact['facts'][0]
            embed = discord.Embed(title='Did you know?',description=str(desc))
            await message.channel.send(embed=embed)
        if cmd(msg, 'roleinfo'):
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
            data = myself.jsonisp('https://nekobot.xyz/api/image?type='+str(args[0][1:]))
            link = data['message'].replace('\/', '/')
            if args[0].endswith('food'):
                col = int(data['color'])
            elif args[0].endswith('coffee'):
                col = int(data['color'])
                num = random.randint(0, 1)
                if num==0:
                    link = myself.jsonisp('https://coffee.alexflipnote.dev/random.json')['file']
                else:
                    link = myself.jsonisp('https://nekobot.xyz/api/image?type=coffee')['message'].replace('\/', '/')
            async with message.channel.typing():
                data = Painter.urltoimage(link.replace('\/', '/'))
                await message.channel.send(file=discord.File(data, args[0][1:]+'.png'))
        if cmd(msg, 'fox'):
            async with message.channel.typing():
                img = myself.jsonisp('https://randomfox.ca/floof/?ref=apilist.fun')["image"]
                data = Painter.urltoimage(img)
                await message.channel.send(file=discord.File(data, 'furry.png'))
        if cmd(msg, 'newemote'):
            data = myself.api('https://discordemoji.com/')
            byEmote = data.split('<div class="float-right"><a href="')
            del byEmote[0]
            alls = []
            for i in range(0, len(byEmote)):
                if byEmote[i].startswith('http'):
                    alls.append(byEmote[i].split('"')[0])
            embed = discord.Embed(colour=discord.Colour.from_rgb(123, 63, 0))
            embed.set_image(url=random.choice(alls))
            await message.channel.send(embed=embed)
        if cmd(msg, 'steamprofile'):
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
                    embedColor = discord.Colour.from_rgb(123, 63, 0)
                else:
                    embedColor = discord.Colour.from_rgb(123, 63, 0)
                embed = discord.Embed(title=username, description='**[Profile Link]('+str(url)+')**\n**Current state: **'+str(state)+'\n**Privacy: **'+str(privacy)+'\n**[Profile pic URL]('+str(avatar)+')**', colour = embedColor)
                embed.set_thumbnail(url=avatar)
                await message.channel.send(embed=embed)
        if cmd(msg, 'salty'):
            if len(args)!=2:
                await message.channel.send(str(client.get_emoji(BotEmotes.error)) + ' | Error! Invalid args.')
            else:
                async with message.channel.typing():
                    av = str(message.mentions[0].avatar_url).replace('.webp', '.png')
                    url = 'https://api.alexflipnote.dev/salty?image='+str(av)
                    data = Painter.urltoimage(url)
                    await message.channel.send(file=discord.File(data, 'salty.png'))
        if cmd(msg, 'woosh') or cmd(msg, 'wooosh') or cmd(msg, 'woooosh'):
            if len(args)!=2:
                await message.channel.send(str(client.get_emoji(BotEmotes.error)) + ' | Error! Invalid args.')
            else:
                async with message.channel.typing():
                    av = message.mentions[0].avatar_url
                    data = Painter.urltoimage('https://api.alexflipnote.dev/jokeoverhead?image='+str(av))
                    await message.channel.send(file=discord.File(data, 'wooosh.png'))
        if cmd(msg, 'funfact'):
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
        if cmd(msg, 'supreme'):
            async with message.channel.typing():
                text = myself.urlify(unprefixed)
                url = 'https://api.alexflipnote.dev/supreme?text='+str(text)
                data = Painter.urltoimage(url)
                await message.channel.send(file=discord.File(data, 'supreme.png'))
        if cmd(msg, 'googledoodle'):
            wait = await message.channel.send(str(client.get_emoji(BotEmotes.loading)) + ' | Please wait... This may take a few moments...')
            data = myself.insp('https://google.com/doodles')
            byLatest = data.split('<li class="latest-doodle ">')
            del byLatest[0]
            byTag = ''.join(byLatest).split('<')
            doodle_link = 'https://google.com'+str(byTag[3][8:].split('"\n')[0])
            doodle_img = 'https:'+str(byTag[4][9:].split('" alt="')[0])
            doodle_name = doodle_link[27:].replace('-', ' ')
            embed = discord.Embed(title=doodle_name, description=doodle_link, colour=discord.Colour.from_rgb(123, 63, 0))
            embed.set_image(url=doodle_img)
            await wait.edit(content='', embed=embed)
        if cmd(msg, 'createbot'):
            if no_args:
                tutorials = f'{prefix}createbot --started `Getting started, preparing stuff.`\n{prefix}createbot --say `Say command help.`\n{prefix}createbot --ping `Ping command help. (Client latency).`\n{prefix}createbot --coin `Flip coin game`\n{prefix}createbot --embed `Creating embeds`\n{prefix}createbot --avatar `Avatar commands help.`'
                embed = discord.Embed(title='Createbot; the discord.py bot tutorial', description=f'This is a tutorial on how to create a discord bot.\nEvery thing other than `--started` needs to have the same module or string.\nEach are args on different categories.\n\n{tutorials}', colour=discord.Colour.from_rgb(123, 63, 0))
                await message.channel.send(embed=embed)
            elif args[1]=='--avatar':
                await message.channel.send('```py\nif msg.startswith(\f\'{prefix}avatar\'):\n\tembed = discord.Embed(colour=discord.Colour.from_rgb(123, 63, 0))\n\tembed.set_image(url=message.guild.get_member(int(msg.split()[1][2:][:-1])).avatar_url)\n\tawait message.channel.send(embed=embed)```')
            elif args[1]=='--embed':
                await message.channel.send('Embed example: ```py\nif message.channel.send(f\'{prefix}embedthing\'):\n\tembed = discord.Embed(\n\t\ttitle = \'My embed title\',\n\t\tdescription = \'The embed description and stuff. Lorem ipsum asdf\',\n\t\tcolour = discord.Colour.from_rgb(123, 63, 0)\n\tembed.add_field(name=\'Field name\', value=\'embed field value is here\', inline=\'True\')\n\tembed.set_footer(text=\'this is a footer\')\n\tawait message.channel.send(embed=embed)```')
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
                    colour = discord.Colour.from_rgb(123, 63, 0)
                )
                code = 'import discord\ntoken = \'YOUR TOKEN\'\nclient = discord.Client()\n@client.event\nasync def on_ready():\n\tprint(\'Bot is ready!\')\n@client.event\nasync def on_message(message):\n\tmsg = message.content.lower()\n\tprefix = \'your prefix\'\n\tif cmd(msg, \'command thing\'):\n\t\tawait message.channel.send(\'Message your bot responds with\')\nclient.run(token)'
                embed.add_field(name='A. Preparing stuff', value='1. Install python through http://python.org/downloads \n2. Learn Python programming language first\n3. Open your console, and type \'pip install discord.py\'\n4.Have some text editor (notepad++/VScode/Sublime Text)', inline='False')
                embed.add_field(name='B. Bot Setup', value='1. Go to http://discordapp.com/developers \n2. Click on \'New Application.\'\n3. Type your bot name and click \'Create\'.\n4. Click on \'bot\' tab, and Click \'Add bot.\'\n5. Click \'Yes, do it!\'\n6. If your name is not approved, please change the bot name in the \'General Information Tab.\' Else, congrats!', inline='False')
                embed.add_field(name='C. Invite the bot to your server', value='1. On the \'Oauth2\' Tab, scroll down and on the scopes list, check \'Bot\'.\n2. Check the bot permissions first.\n3. Click on COPY.\n4. Open that link on your browser.\n5. Authorize the bot to your server.\n6. Boom! Your bot joined your server!', inline='False')
                embed.add_field(name='D. Coding time!', value='1. Create a folder.\n2. Open that folder and create a file named \'bot.py\' in .py extension.\n3. Open that file with a text editor.\n4. Code the following above.\n', inline='False')
                embed.add_field(name='E. How to get the Token?', value='1. Open the http://discordapp.com/developers, and click on your bot.\n2. Open the \'Bot\' tab.\n3. On token, click \'Copy\'.\n4. Change the \'YOUR TOKEN\' above by pasting your token.\n5. DON\'T SHARE YOUR TOKEN WITH ANYBODY.', inline='False')
                embed.add_field(name='F. Discord API?', value='https://discordpy.readthedocs.io/en/latest/api.html', inline='False')
                embed.set_footer(text='Enjoy your BOT! ;)')
                await message.channel.send(embed=embed, content='```py\n'+str(code)+'```')
        if cmd(msg, 'channels'):
            channels = ''
            warning = 'No errors found.'
            for i in range(0, int(len(message.guild.text_channels))):
                if len(channels)>2048:
                    warning = str(client.get_emoji(BotEmotes.error)) + ' | Error: Too many channels, some channels may be not listed.'
                channels = channels +'<#'+ str(message.guild.text_channels[i].id) + '> \n'
            embed = discord.Embed(title=message.guild.name+'\'s Text channels:', description=str(channels), inline='True')
            embed.set_footer(text=str(warning))
            await message.channel.send(embed=embed)
        if cmd(msg, 'slot'):
            win = False
            jackpot = False
            slots = []
            for i in range(0, 3):
                newslot = Games.slot()
                if newslot[1]==newslot[2] and newslot[1]==newslot[3] and newslot[2]==newslot[3]:
                    win = True
                    if newslot[1]==':flushed:':
                        jackpot = True
                slots.append(Games.slotify(newslot))
            if win:
                msgslot = 'You win!'
                col = discord.Colour.from_rgb(123, 63, 0)
                if jackpot:
                    msgslot = 'JACKPOT!'
                    col = discord.Colour.from_rgb(123, 63, 0)
            else:
                msgslot = 'You lose... Try again!'
                col = discord.Colour.from_rgb(123, 63, 0)
            embed = discord.Embed(title=msgslot, description=slots[0]+'\n\n'+slots[1]+'\n\n'+slots[2], colour=col)
            await message.channel.send(embed=embed)
        if cmd(msg, 'rolecolor'):
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
                embed = discord.Embed(title='Server role colors OwO', description=res, colour=discord.Colour.from_rgb(123, 63, 0))
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
        if cmd(msg, 'isprime'):
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
        if cmd(msg, 'jpeg') or cmd(msg, 'invert') or cmd(msg, 'magik')or cmd(msg, 'pixelate')or cmd(msg, 'b&w'):
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
                async with message.channel.typing():
                    av = message.mentions[0].avatar_url
                    url='https://api.alexflipnote.dev/filter/'+str(com)+'?image='+str(av).replace('webp', 'png')
                    data = Painter.urltoimage(url)
                    await message.channel.send(file=discord.File(data, 'filtered.png'))
        if cmd(msg, 'drake'):
            if args[1]=='help':
                embed = discord.Embed(
                    title='Drake meme helper help',
                    description='Type the following:\n`'+str(prefix)+'drake [text1] [text2]`\n\nFor example:\n`'+str(prefix)+'drake [test1] [test2]`'
                )
                await message.channel.send(embed=embed)
            else:
                async with message.channel.typing():
                    txt1 = myself.urlify(unprefixed.split('[')[1][:-2])
                    txt2 = myself.urlify(unprefixed.split('[')[2][:-1])
                    url='https://api.alexflipnote.dev/drake?top='+str(txt1)+'&bottom='+str(txt2)
                    data = Painter.urltoimage(url)
                    await message.channel.send(file=discord.File(data, 'drake.png'))
        if cmd(msg, 'ascii'):
            if no_args:
                await message.channel.send(str(client.get_emoji(BotEmotes.error)) +' | Invalid. Please send a word or something.')
            else:
                if '--randomfont' not in msg:
                    query = myself.urlify(str(unprefixed))
                    word = myself.insp("http://artii.herokuapp.com/make?text="+query.replace('--randomfont', ''))
                else:
                    fonts = src.getAsciiFonts()
                    query = myself.urlify(str(unprefixed))
                    query = query.replace('--randomfont ', '')
                    word = myself.insp("http://artii.herokuapp.com/make?text="+query.replace('--randomfont', '')+'&font='+random.choice(fonts))
                if len(word)>1900:
                    await message.channel.send('The word is too long to be displayed!')
                else:
                    embed = discord.Embed(
                        description=f'```{word}```',
                        colour=discord.Colour.from_rgb(123, 63, 0)
                    )
                    embed.set_footer(text='Type --randomfont for umm.. random font to be generated.')
                    await message.channel.send(embed=embed)
        if cmd(msg, 'typingtest'):
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
        if cmd(msg, 'defuse') or cmd(msg, 'bomb'):
            def embedType(a):
                if a==1:
                    return discord.Embed(title='The bomb exploded!', description='Game OVER!', colour=discord.Colour(000))
                elif a==2:
                    return discord.Embed(title='The bomb defused!', description='Congratulations! :grinning:', colour=discord.Colour.from_rgb(123, 63, 0))
            embed = discord.Embed(title='DEFUSE THE BOMB!', description='**Cut the correct wire!\nThe bomb will explode in 15 seconds!**', colour=discord.Colour.from_rgb(123, 63, 0))
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
        if cmd(msg, 'userinfo'):
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
        if cmd(msg, 'wikipedia'):
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
                    embed = discord.Embed(title=pageTitle, description=str(explain), colour=discord.Colour.from_rgb(123, 63, 0))
                    embed.set_footer(text='Get more info at '+str(page.fullurl))
                    await wait.edit(content='', embed=embed)
        if cmd(msg, 'getinvite'):
            if message.author.guild_permissions.create_invite==False:
                await message.channel.send(str(client.get_emoji(BotEmotes.error)) +' | You need to have the permission `Create Invite` to continue!')
            else:
                serverinvite = await message.channel.create_invite(reason='Requested by '+str(message.author.name))
                await message.channel.send('New invite created! Link: **'+str(serverinvite)+'**')
        if cmd(msg, 'avatar'):
            try:
                if len(message.mentions)==0: user = message.author
                else: user = message.mentions[0]
                embed = discord.Embed(title=user.name+'\'s avatar', colour = discord.Colour.from_rgb(123, 63, 0))
                embed.set_image(url=str(user.avatar_url).replace('.webp', '.png'))
                await message.channel.send(embed=embed)
            except:
                await message.channel.send(str(client.get_emoji(BotEmotes.error)) +' | Invalid avatar.')
        if args[0]==prefix+'phcomment':
            if no_args:
                await message.channel.send(str(client.get_emoji(BotEmotes.error)) +f' | Invalid type.\nTry:\n`{prefix}phcomment [text]` or;\n`{prefix}phcomment [tag] [text]`')
            else:
                async with message.channel.typing():
                    if len(message.mentions)==0:
                        text = unprefixed
                        url='https://nekobot.xyz/api/imagegen?type=phcomment&username='+myself.urlify(str(message.author.name))+'&text='+myself.urlify(str(text))+'&image='+str(message.author.avatar_url).replace('.webp?size=1024', '.png')+'&raw=1'
                    else:
                        text = message.content[int(len(args[0])+len(args[1])+2):]
                        url='https://nekobot.xyz/api/imagegen?type=phcomment&username='+myself.urlify(str(message.mentions[0].name))+'&text='+myself.urlify(str(text))+'&image='+str(message.mentions[0].avatar_url).replace('.webp?size=1024', '.png')+'&raw=1'
                    await message.channel.send(file=discord.File(Painter.urltoimage(url), 'ph_comment.png'))
        if args[0]==prefix+'ph':
            if args[1]=='help':
                embed = discord.Embed(title='ph command help', description='Type the following:\n'+prefix+'ph [txt1] [txt2]\n\nFor example:\n'+prefix+'ph [Git] [Hub]', colour=discord.Colour.from_rgb(123, 63, 0))
                await message.channel.send(embed=embed)
            elif '[' in msg:
                async with message.channel.typing():
                    txt1 = myself.urlify(unprefixed.split('[')[1][:-2])
                    txt2 = myself.urlify(unprefixed.split('[')[2][:-1])
                    url='https://api.alexflipnote.dev/pornhub?text='+str(txt1)+'&text2='+str(txt2)
                    await message.channel.send(file=discord.File(data, 'ph.png'))
        if cmd(msg, 'steamapp'):
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
                    embed = discord.Embed(title=data['items'][0]['name'], url='https://store.steampowered.com/'+str(data['items'][0]['type'])+'/'+str(data['items'][0]['id']), description='**Price tag:** '+str(prize)+'\n**Metascore: **'+str(rate)+'\n**This app supports the following OSs: **'+str(myself.dearray(oss_raw)), colour=discord.Colour.from_rgb(123, 63, 0))
                    embed.set_image(url=data['items'][0]['tiny_image'])
                    await message.channel.send(embed=embed)
        if cmd(msg, 'stackoverflow') or cmd(msg, 'sof'):
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
                    embed = discord.Embed(title=ques['title'], description='**'+str(ques['view_count'])+' *desperate* developers looked into this post.**\n**TAGS:** '+str(tags), url=ques['link'], colour=discord.Colour.from_rgb(123, 63, 0))
                    embed.set_author(name=ques['owner']['display_name'], url=ques['owner']['link'], icon_url=ques['owner']['profile_image'])
                    embed.set_footer(text='Shown 1 result out of '+str(leng)+' results!')
                    await message.channel.send(embed=embed)
                except:
                    await message.channel.send(str(client.get_emoji(BotEmotes.error)) + ' | There was an error on searching! Please check your spelling :eyes:')
        if cmd(msg, 'translate'):
            wait = await message.channel.send(str(client.get_emoji(BotEmotes.loading)) + ' | Please wait...')
            if len(args)>1:
                if args[1]=='--list':
                    lang = ''
                    for bahasa in LANGUAGES:
                        lang = lang+str(bahasa)+' ('+str(LANGUAGES[bahasa])+')\n'
                    embed = discord.Embed(title='List of supported languages', description=str(lang), colour=discord.Colour.from_rgb(123, 63, 0))
                    await wait.edit(content='', embed=embed)
                elif len(args)>2:
                    destination = args[1]
                    toTrans = msg[int(len(args[1])+len(args[0])+2):]
                    try:
                        trans = gtr.translate(toTrans, dest=args[1])
                        embed = discord.Embed(title=f'Translation', description=f'**{trans.text}**', colour=discord.Colour.from_rgb(123, 63, 0))
                        embed.set_footer(text=f'Translated {LANGUAGES[trans.src]} to {LANGUAGES[trans.dest]}')
                        await wait.edit(content='', embed=embed)
                    except:
                        await wait.edit(content=str(client.get_emoji(BotEmotes.error)) + ' | An error occured!')
                else:
                    await wait.edit(content=f'Please add a language! To have the list and their id, type\n`{prefix}translate --list`.')
            else:
                await wait.edit(content=f'Please add translations or\nType `{prefix}translate --list` for supported languages.')
        if cmd(msg, 'catfact'):
            catWait = await message.channel.send(str(client.get_emoji(BotEmotes.loading)) + ' | Please wait...')
            data = myself.api("https://catfact.ninja/fact")
            embed = discord.Embed(
                title = 'Did you know;',
                description = data["fact"],
                color = 0x333333
            )
            await catWait.edit(content='', embed=embed)
        if cmd(msg, 'trash'):
            if len(args)!=2:
                await message.channel.send('Please mention someone!\nExample: `'+prefix+'trash <@'+message.author.id+'>`')
            else:
                async with message.channel.typing():
                    av = message.author.avatar_url
                    toTrash = message.mentions[0].avatar_url
                    url='https://api.alexflipnote.dev/trash?face='+str(av).replace('webp', 'png')+'&trash='+str(toTrash).replace('webp', 'png')
                    data = Painter.urltoimage(url)
                    await message.channel.send(file=discord.File(data, 'trashed.png'))
        if args[0]==prefix+'bird' or cmd(msg, 'sadcat'):
            async with message.channel.typing():
                if cmd(msg, 'bird'): getreq = 'birb'
                else: getreq = 'sadcat'
                image_url = myself.jsonisp('https://api.alexflipnote.dev/'+str(getreq))['file']
                data = Painter.urltoimage(image_url)
                await message.channel.send(file=discord.File(data, args[0][1:]+'.png'))
        if cmd(msg, 'ytthumbnail'):
            async with message.channel.typing():
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
                url = 'https://img.youtube.com/vi/'+str(videoid)+'/mqdefault.jpg'
                data = Painter.urltoimage(url)
                await message.channel.send(file=discord.File(data, 'thumbnail.png'))
        if cmd(msg, 'captcha'):
            async with message.channel.typing():
                capt = myself.urlify(unprefixed)
                url = 'https://api.alexflipnote.dev/captcha?text='+str(capt)
                data = Painter.urltoimage(url)
                await message.channel.send(file=discord.File(data, 'captcha.png'))
        if cmd(msg, 'tts'):
            if no_args:
                await message.channel.send(str(client.get_emoji(BotEmotes.error)) +' | Invalid.')
            else:
                await message.channel.send(content=msg[int(args[0]+1):], tts=True)
        if cmd(msg, 'scroll'):
            if no_args: await message.channel.send(str(client.get_emoji(BotEmotes.error))+" | Error! where is your text?")
            else:
                async with message.channel.typing():
                    scrolltxt = myself.urlify(unprefixed)
                    embed = discord.Embed(colour=discord.Colour.from_rgb(123, 63, 0))
                    url='https://api.alexflipnote.dev/scroll?text='+str(scrolltxt)
                    data = Painter.urltoimage(url)
                    await message.channel.send(file=discord.File(data, 'scroll.png'))
        if cmd(msg, 'ship') and no_args:
            async with message.channel.typing():
                member = []
                av = []
                for i in range(0, int(len(message.guild.members))):
                    if message.guild.members[i].name!=message.author.name:
                        member.append(message.guild.members[i].name)
                        av.append(message.guild.members[i].avatar_url)
                num = random.randint(0, len(av))
                ship = member[num]
                avd = av[num]
                url = 'https://api.alexflipnote.dev/ship?user='+str(message.author.avatar_url).replace('webp', 'png')+'&user2='+str(avd).replace('webp', 'png')
                data = Painter.urltoimage(url)
                await message.channel.send(file=discord.File(data, 'ship.png'))
        if cmd(msg, 'ghiblifilms'):
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
        if cmd(msg, 'servericon'):
            if message.guild.is_icon_animated()==True:
                link = 'https://cdn.discordapp.com/icons/'+str(message.guild.id)+'/'+str(message.guild.icon)+'.gif?size=1024'
            else:
                link = 'https://cdn.discordapp.com/icons/'+str(message.guild.id)+'/'+str(message.guild.icon)+'.png?size=1024'
            theEm = discord.Embed(title=message.guild.name+'\'s Icon', colour=discord.Colour.from_rgb(123, 63, 0))
            theEm.set_image(url=link)
            await message.channel.send(embed=theEm)
        if cmd(msg, 'slowmode'):
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
        if cmd(msg, 'inviteme') or cmd(msg, 'invite'):
            if message.guild.id!=264445053596991498:
                embed = discord.Embed(
                    title='Sure thing! Invite this bot to your server using the link below.',
                    description='[Invite link](https://top.gg/bot/'+str(Config.id)+') | [Support Server]('+str(Config.SupportServer.invite)+')',
                    colour=discord.Colour.from_rgb(123, 63, 0)
                )
                await message.channel.send(embed=embed)
        if cmd(msg, 'server'):
            humans, bots, online = 0, 0, 0
            for i in message.guild.members:
                if i.status != 'offline': online += 1
                if i.bot: bots += 1
                if not i.bot: humans += 1
            image = Painter.servercard("./assets/pics/card.jpg", str(message.guild.icon_url).replace(".webp?size=1024", ".jpg?size=128"), message.guild.name, str(message.guild.created_at)[:-7], message.guild.owner.name, str(humans), str(bots), str(len(message.guild.channels)), str(len(message.guild.roles)), str(message.guild.premium_subscription_count), str(message.guild.premium_tier), str(online))
            await message.channel.send(content='Here is the '+message.guild.name+'\'s server card.', file=discord.File(image, message.guild.name+'.png'))
        if cmd(msg, 'factor'):
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
        if cmd(msg, 'multiplication'):
            arr = []
            for i in range(1, 15):
                arr.append(int(args[1])*i)
            await message.channel.send(str(arr))
        if cmd(msg, 'gdcomment'):
            async with message.channel.typing():
                try:
                    byI = unprefixed.split(' | ')
                    text = myself.urlify(byI[0])
                    num = int(byI[2])
                    if num>9999:
                        num = 601
                    elif num<-9999:
                        num = -601
                    gdprof = myself.urlify(byI[1])
                    if message.author.guild_permissions.manage_guild==True: url='https://gdcolon.com/tools/gdcomment/img/'+str(text)+'?name='+str(gdprof)+'&likes='+str(num)+'&mod=mod&days=1-second'
                    else: url='https://gdcolon.com/tools/gdcomment/img/'+str(text)+'?name='+str(gdprof)+'&likes='+str(num)+'&days=1-second'
                    await message.channel.send(file=discord.File(Painter.urltoimage(url), 'gdcomment.png'))
                except Exception as e:
                    print('https://gdcolon.com/tools/gdcomment/img/'+str(text)+'?name='+str(gdprof)+'&likes='+str(num)+'&days=1-second')
                    await message.channel.send(str(client.get_emoji(BotEmotes.error)) +f' | Invalid!\nThe flow is this: `{prefix}gdcomment text | name | like count`\nExample: `{prefix}gdcomment I am cool | RobTop | 601`.\n\nFor developers: ```{e}```')
        if cmd(msg, 'gdbox'):
            if no_args: await message.channel.send('Please input a text!')
            else:
                async with message.channel.typing():
                    text = myself.urlify(unprefixed)
                    av = message.author.avatar_url
                    if len(text)>100:
                        await message.channel.send(str(client.get_emoji(BotEmotes.error)) +' | the text is too long!')
                    else:
                        if not message.author.guild_permissions.manage_guild: color = 'brown'
                        else: color = 'blue'
                        url='https://gdcolon.com/tools/gdtextbox/img/'+str(text)+'?color='+color+'&name='+str(message.author.name)+'&url='+str(av).replace('webp', 'png')+'&resize=1'
                        await message.channel.send(file=discord.File(Painter.urltoimage(url), 'gdbox.png'))
        if cmd(msg, 'serveremojis'):
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
                        colour = discord.Colour.from_rgb(123, 63, 0)
                    )
                    if staticemo=="":
                        staticemo = 'No emojis found :('
                    if animateemo=="":
                        animateemo = 'No emojis found :('
                    embed.add_field(name='Static Emojis ('+str(staticcount)+')', value=str(staticemo), inline='False')
                    embed.add_field(name='Animated Emojis ('+str(animatecount)+')', value=str(animateemo), inline='False')
                    embed.set_footer(text=str(warning))
                    await message.channel.send(embed=embed)
        if cmd(msg, 'id'):
            var = args[1][:-1]
            if args[1].startswith('<#'):
                var = var[2:]
                if len(message.mentions)>0:
                    var = message.mentions[0].id
            elif (args[1].startswith('<@&')):
                var = var[3:]
            await message.channel.send(str(var))
        if cmd(msg, 'robohash'):
            async with message.channel.typing():
                if no_args:
                    gib = ''
                    for i in range(0, random.randint(5, 10)):
                        gib = gib + random.choice(list('ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz'))
                else:
                    gib = msg[int(len(args[0])+1):]
                url='https://robohash.org/'+str(gib)
                await message.channel.send(file=discord.File(Painter.urltoimage(url), 'robohash.png'))
        if cmd(msg, 'gdlogo'):
            if no_args:
                await message.channel.send('Please input a text!')
            else:
                async with message.channel.typing():
                    text = myself.urlify(unprefixed)
                    url='https://gdcolon.com/tools/gdlogo/img/'+str(text)
                    await message.channel.send(file=discord.File(Painter.urltoimage(url), 'gdlogo.png'))
        if cmd(msg, 'lockdown'):
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
                ban = False
                for i in range(0, len(unprefixed.lower())):
                    for j in list("ABCDEFGHIJKLMNOPQRSTUVWXYZ."):
                        if j in unprefixed.upper()[i]:
                            ban = True
                            break
                    if ban: break
                if ban:
                    await message.channel.send(client.get_emoji(BotEmotes.error)+' | Invalid calculation.')
                else:
                    try:
                        await message.channel.send(embed=discord.Embed(description=f'**Result:**\n```{eval(unprefixed)}```', colour=discord.Colour.from_rgb(123, 63, 0)))
                    except ZeroDivisionError:
                        await message.channel.send(embed=discord.Embed(description=f'**Result:**\n```yo mama```', colour=discord.Colour.from_rgb(123, 63, 0)))
        if cmd(msg, "flipdice") or cmd(msg, "dice"):
            arr = ["one", "two", "three", "four", "five", "six"]
            ran = random.randint(0, 5)
            await message.channel.send(":"+arr[ran]+":")
        if cmd(msg, "flipcoin") or cmd(msg, "coin"):
            ran = random.randint(0, 1)
            if (ran==0):
                await message.channel.send("HEADS")
            elif (ran==1):
                await message.channel.send("TAILS")
        if cmd(msg, 'ship') and len(args)>1:
            if len(args)<3:
                await message.channel.send(':x: Please tag 2 people!')
            elif len(args)==3:
                async with message.channel.typing():
                    if args[1].startswith('<@!'): av1 = message.mentions[0].avatar_url
                    else: av1 = message.mentions[0].avatar_url
                    if args[2].startswith('<@!'): av2 = message.mentions[1].avatar_url
                    else: av2 = message.mentions[1].avatar_url
                    url='https://api.alexflipnote.dev/ship?user='+str(av1).replace('webp', 'png')+'&user2='+str(av2).replace('webp', 'png')
                    data = Painter.urltoimage(url)
                    await message.channel.send(file=discord.File(data, 'shippies.png'))
        if args[0]==prefix+"dog":
            async with message.channel.typing():
                apiied = myself.api("https://random.dog/woof.json")['url']
                data = Painter.urltoimage(apiied)
                await message.channel.send(file=discord.File(data, 'dog.png'))
        if args[0]==prefix+"cat" or cmd(msg, "cats"):
            async with message.channel.typing():
                apiied = myself.api("https://aws.random.cat/meow")['file']
                data = Painter.urltoimage(apiied)
                await message.channel.send(file=discord.File(data, 'cat.png'))
        if cmd(msg, 'imgcaptcha'):
            async with message.channel.typing():
                if len(message.mentions)==0: av, nm = str(message.author.avatar_url).replace('.webp?size=1024', '.png'), myself.urlify(str(message.author.name))
                else: av, nm = str(message.mentions[0].avatar_url).replace('.webp?size=1024', '.png'), myself.urlify(str(message.mentions[0].name))
                url = 'http://nekobot.xyz/api/imagegen?type=captcha&username='+nm+'&url='+av+'&raw=1'
                data = Painter.urltoimage(url)
                await message.channel.send(file=discord.File(data, 'your_captcha.png'))
        if cmd(msg, 'whowouldwin'):
            if len(message.mentions)!=2:
                await message.channel.send('Please tag TWO people!')
            else:
                async with message.channel.typing():
                    url='http://nekobot.xyz/api/imagegen?type=whowouldwin&raw=1&user1='+str(message.mentions[0].avatar_url).replace('.webp?size=1024', '.png')+'&user2='+str(message.mentions[1].avatar_url).replace('.webp?size=1024', '.png')
                    await message.channel.send(discord.File(Painter.urltoimage(url), 'whowouldwin.png'))
        if cmd(msg, 'trap'):
            if no_args or len(message.mentions)==0:
                await message.channel.send(str(client.get_emoji(BotEmotes.error)) +f' | Wrong.\nPlease try the correct like following:\n`{prefix}trap [tag]`')
            else:
                async with message.channel.typing():
                    url='http://nekobot.xyz/api/imagegen?type=trap&name='+myself.urlify(str(message.mentions[0].name))+'&author='+myself.urlify(str(message.author.name))+'&image='+str(message.mentions[0].avatar_url).replace('.webp?size=1024', '.png')+'&raw=1'
                    await message.channel.send(discord.File(Painter.urltoimage(url), 'trap.png'))
        if cmd(msg, 'roles'):
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
                    color = discord.Colour.from_rgb(123, 63, 0)
                )
                embed.set_footer(text=str(warning))
                await message.channel.send(embed=embed)
        if cmd(msg, "gddaily"):
            toEdit = await message.channel.send("Retrieving Data...")
            data = myself.api("https://gdbrowser.com/api/level/daily")
            image = 'https://gdbrowser.com/icon/'+data["author"]
            embed = discord.Embed(
                title = data["name"]+' ('+str(data["id"])+')',
                description = data["description"],
                colour = discord.Colour.from_rgb(123, 63, 0)
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
        if cmd(msg, 'botmembers'):
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
                colour = discord.Colour.from_rgb(123, 63, 0)
            )
            embed.set_footer(text=warning)
            await message.channel.send(embed=embed)
        if cmd(msg, "gdweekly"):
            toEdit = await message.channel.send("Retrieving Data...")
            data = myself.api("https://gdbrowser.com/api/level/weekly")
            image = 'https://gdbrowser.com/icon/'+data["author"]
            embed = discord.Embed(
                title = data["name"]+' ('+str(data["id"])+')',
                description = data["description"],
                colour = discord.Colour.from_rgb(123, 63, 0)
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
        if args[0]==prefix+'facts':
            if no_args: await message.channel.send(str(client.get_emoji(BotEmotes.error))+" | where are the facts?!")
            else:
                async with message.channel.typing():
                    url='https://api.alexflipnote.dev/facts?text='+myself.urlify(unprefixed)
                    await message.channel.send(discord.File(Painter.urltoimage(url), 'facts.png'))
        if cmd(msg, "gdprofile"):
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
        if cmd(msg, "rps"):
            main = await message.channel.send(embed=discord.Embed(title='Rock Paper Scissors game.', description='Click the reaction below. And game will begin.', colour=discord.Colour.from_rgb(123, 63, 0)))
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
                res = Games.rps(emotes[num])
                given = emotes[num]
                msgId = res[0]
                emojiArray = emotes
                ran = res[1]
            messages = ["Congratulations! "+str(message.author.name)+" WINS!", "It's a draw.", "Oops, "+str(message.author.name)+" lost!"]
            colors = [discord.Colour.from_rgb(123, 63, 0), discord.Colour.orange(), discord.Colour.from_rgb(123, 63, 0)]
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
        if cmd(msg, "randomcase"):
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
        if cmd(msg, 'guessnum') or cmd(msg, 'gn'):
            num = random.randint(5, 100)
            username = message.author.display_name
            user_class = message.author
            embed = discord.Embed(title='Starting the game!', description='You have to guess a *secret* number between 5 and 100!\n\nYou have 20 attempts, and 20 second timer in each attempt!\n\n**G O O D  L U C K**', colour=discord.Colour.from_rgb(123, 63, 0))
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
        if cmd(msg, "randomcolor") or cmd(msg, 'colorinfo') or cmd(msg, 'colourinfo'):
            continuing = False
            if cmd(msg, 'randomcolor'):
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
        if cmd(msg, 'call'):
            if no_args: await message.channel.send(str(client.get_emoji(BotEmotes.error))+' | Where are the arguments?!'))
            else:
                async with message.channel.typing():
                    call = myself.urlify(unprefixed)
                    url='https://api.alexflipnote.dev/calling?text='+str(call)
                    await message.channel.send(discord.File(Painter.urltoimage(url), 'call.png'))
        if cmd(msg, 'achieve'):
            if no_args: await message.channel.send(str(client.get_emoji(BotEmotes.error))+' | Where are the arguments?!'))
            else:
                async with message.channel.typing():
                    txt = myself.urlify(unprefixed)
                    url='https://api.alexflipnote.dev/achievement?text='+str(txt)
                    await message.channel.send(discord.File(Painter.urltoimage(url), 'achievement.png'))
        if cmd(msg, "country"):
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
        if cmd(msg, 'commands') or cmd(msg, 'help'):
            data = myself.jsonisp("https://vierofernando.github.io/username601/assets/json/commands.json")
            types = Config.cmdtypes
            if no_args:
                cate = ''
                for i in range(0, len(types)):
                    cate += f'**{str(i+1)}. **{prefix}help {str(types[i])}\n'
                embed = discord.Embed(
                    title='Username601\'s commands',
                    description='[Join the support server]('+str(Config.SupportServer.invite)+') | [Vote us on top.gg](https://top.gg/bot/'+str(Config.id)+'/vote)\n\n**[More information on our website here.](https://vierofernando.github.io/username601/commands)**\n**Command Categories:** \n'+str(cate),
                    colour=discord.Colour.from_rgb(123, 63, 0)
                )
                embed.set_footer(text=f'Type {prefix}help <command/category> for more details.')
                await message.channel.send(embed=embed)
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
                        embed = discord.Embed(title='Category help for '+str(category_name)+':', description='**Commands:** \n```'+str(cmds)+'```', colour=discord.Colour.from_rgb(123, 63, 0))
                    if typ=='Command':
                        parameters = 'No parameters required.'
                        if len(source['p'])>0:
                            parameters = ''
                            for i in range(0, len(source['p'])):
                                parameters += '**'+source['p'][i]+'**\n'
                        embed = discord.Embed(title='Command help for '+str(source['n'])+':', description='**Function: **'+str(source['f'])+'\n**Parameters:** \n'+str(parameters), colour=discord.Colour.from_rgb(123, 63, 0))
                    await message.channel.send(embed=embed)
        if cmd(msg, 'uptime'):
            embed = discord.Embed(title=str(datetime.datetime.now()-latest_update)[:-7], description='Last time down: '+str(latest_update)[:-7], color=discord.Colour.from_rgb(123, 63, 0))
            embed.set_footer(text='Don\'t worry! 99% Uptime guaranteed.\nUnless there is an big error/on development.')
            await message.channel.send(embed=embed)
        if cmd(msg, 'about'):
            if message.guild.id!=264445053596991498:
                messageRandom = src.getAbout()
                # osinfo = myself.platform()
                if str(client.get_guild(Config.SupportServer.id).get_member(Config.owner.id).status)=='offline':
                    devstatus = 'Offline'
                else:
                    devstatus = 'Online'
                embed = discord.Embed(
                    title = 'About this seemingly normal bot.',
                    description = random.choice(messageRandom),
                    colour = 0xff0000
                )
                embed.add_field(name='Bot general Info', value='**Bot name: ** Username601\n**Programmed in: **Discord.py (Python)\n**Created in: **6 April 2020.\n**Successor of: **somebot56.\n**Default prefix: ** 1', inline='True')
                embed.add_field(name='Programmer info', value='**Programmed by: **'+Config.owner.name+'. ('+client.get_user(Config.owner.id).name+'#'+str(client.get_user(Config.owner.id).discriminator)+') \n**Best languages: **~~HTML, CSS,~~ VB .NET, JavaScript, Python\n**Current Discord Status:** '+devstatus+'\n**Social links:**\n[Discord Server]('+str(Config.SupportServer.invite)+')\n[GitHub](http://github.com/vierofernando)\n[Top.gg](https://top.gg/user/'+str(Config.owner.id)+')\n[SoloLearn](https://www.sololearn.com/Profile/17267145)\n[Brainly (Indonesia)](http://bit.ly/vierofernandobrainly)\n[Geometry Dash](https://gdbrowser.com/profile/knowncreator56)', inline='True')
                embed.add_field(name='Version Info', value='**Bot version: ** '+Config.Version.number+'\n**Changelog: **'+Config.Version.changelog+'\n\n**Discord.py version: **'+str(discord.__version__)+'\n**Python version: **'+str(sys.version).split(' (default')[0])#+'\n'+str(osinfo))
                embed.add_field(name='Links', value='[Invite this bot to your server!](http://vierofernando.github.io/programs/username601) | [Source code](http://github.com/vierofernando/username601) | [The support server!]('+str(Config.SupportServer.invite)+') | [Vote us on top.gg](https://top.gg/bot/'+str(Config.id)+'/vote) | [Official Website](https://vierofernando.github.io/username601)', inline='False')
                embed.set_thumbnail(url='https://raw.githubusercontent.com/vierofernando/username601/master/assets/pics/pfp.png')
                embed.set_footer(text='© Viero Fernando Programming, 2018-2020. All rights reserved.')
                await message.channel.send(embed=embed)
        if cmd(msg, 'vote'):
            embed = discord.Embed(title='Support by Voting us at top.gg!', description='Sure thing, mate! [Vote us at top.gg by clicking me!](https://top.gg/bot/'+str(Config.id)+'/vote)', colour=discord.Colour.from_rgb(123, 63, 0))
            await message.channel.send(embed=embed)
        if cmd(msg, 'time') or cmd(msg, 'utc'):
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
                colour = discord.Colour.from_rgb(123, 63, 0)
            )
            await message.channel.send(embed=embed)
        if cmd(msg, 'joke') or cmd(msg, 'jokes'):
            data = myself.api("https://official-joke-api.appspot.com/jokes/general/random")
            embed = discord.Embed(
                title = str(data[0]["setup"]),
                description = '||'+str(data[0]["punchline"])+'||',
                colour = discord.Colour.from_rgb(123, 63, 0)
            )
            await message.channel.send(embed=embed)
        if cmd(msg, 'qr'):
            async with message.channel.typing():
                if no_args: content = 'nothing'
                else: content = myself.urlify(unprefixed)
                link = "https://api.qrserver.com/v1/create-qr-code/?size=150x150&data="+str(content.lower())
                await message.channel.send(file=discord.File(Painter.urltoimage(link), 'qr.png'))
        if cmd(msg, 'didyoumean'):
            if args[1]=='help':
                embed = discord.Embed(title='didyoumean command help', description='Type like the following\n'+prefix+'didyoumean [text1] [text2]\n\nFor example:\n'+prefix+'didyoumean [i am gay] [i am guy]', colour=discord.Colour.from_rgb(123, 63, 0))
                await message.channel.send(embed=embed)
            else:
                async with message.channel.typing():
                    txt1, txt2 = myself.urlify(message.content.split('[')[1][:-2]), myself.urlify(message.content.split('[')[2][:-1])
                    url='https://api.alexflipnote.dev/didyoumean?top='+str(txt1)+'&bottom='+str(txt2)
                    await message.channel.send(file=discord.File(Painter.urltoimage(url), 'didyoumean.png'))
        if cmd(msg, 'challenge'):
            if no_args: await message.channel.send(str(client.get_emoji(BotEmotes.error))+' | What is the challenge?')
            else:
                async with message.channel.typing():
                    txt = myself.urlify(unprefixed)
                    url='https://api.alexflipnote.dev/challenge?text='+str(txt)
                    await message.channel.send(file=discord.File(Painter.urltoimage(url), 'challenge.png'))
        if cmd(msg, 'median') or cmd(msg, 'mean'):
            numArray = []
            i = 1
            try:
                while args[i]!="":
                    numArray.append(args[i])
                    i = int(i)+1
            except IndexError:
                print("Reached the limit.")
            if cmd(msg, 'median'):
                if len(numArray)%2==0:
                    first = int(len(numArray))/2
                    second = int(first)
                    first = int(first)-1
                    result = int(int(numArray[first])+int(numArray[second]))/2
                else:
                    resultPosition = int(len(numArray))-int(((len(numArray))-1)/2)
                    result = numArray[int(resultPosition)-1]
            if cmd(msg, 'mean'):
                temp = 0
                for i in range(0, int(len(numArray))):
                    temp = int(temp)+int(numArray[i])
                result = int(temp)/int(len(numArray))
            await message.channel.send(str(result))
        if cmd(msg, "sqrt"):
            num = int(args[1])
            await message.channel.send(str(math.sqrt(int(num))))
        if cmd(msg, 'reactnum'):
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
        if cmd(msg, 'morse') or cmd(msg, 'temmie'):
            if no_args: await message.channel.send(str(client.get_emoji(BotEmotes.error))+' | Please send something to be encoded.')
            else:
                if cmd(msg, 'morse'): await message.channel.send('This command is closed for maintenance.')
                elif cmd(msg, 'temmie'): 
                    link, num = 'https://raw.githubusercontent.com/dragonfire535/xiao/master/assets/json/temmie.json', 1
                    data = myself.jsonisp(link)
                    keyz = list(data.keys())
                    if cmd(msg, 'temmie'):
                        total = ''
                        for j in range(num, len(keyz)):
                            if total=='': total = unprefixed
                            total = total.replace(keyz[j], data[keyz[j]])
                # else:
                #     word = list(unprefixed)
                #     total = []
                #     for i in word:
                #         for x in range(num, len(keyz)):
                #             i.replace(keyz[x], data[keyz[x]])
                #         total.append(i)
                if cmd(msg, 'temmie'): await message.channel.send(total)
                # else: await message.channel.send(' '.join(total))
        if cmd(msg, 'slap'):
            if no_args:
                await message.channel.send(str(client.get_emoji(BotEmotes.error))+" | Slap who? Tag someone!")
            else:
                await message.channel.send(src.slap('msg')+', '+message.mentions[0].name+'!\n'+src.slap('gif'))
        if cmd(msg, 'fact-core') or cmd(msg, 'fact') or cmd(msg, 'factcore') or cmd(msg, 'fact-sphere') or cmd(msg, 'factsphere'):
            data = myself.jsonisp('https://raw.githubusercontent.com/dragonfire535/xiao/master/assets/json/fact-core.json')
            embed = discord.Embed(title='Fact Core', description=random.choice(data), colour=discord.Colour.from_rgb(123, 63, 0))
            embed.set_thumbnail(url='https://i1.theportalwiki.net/img/thumb/5/55/FactCore.png/300px-FactCore.png')
            await message.channel.send(embed=embed)
        if cmd(msg, 'hbd'):
            if no_args:
                await message.channel.send(str(client.get_emoji(BotEmotes.error))+" | who is having their birthday today?")
            else:
                await message.channel.send("Happy birthday, "+message.mentions[0].name+"!\n"+src.hbd())
        if cmd(msg, 'choose'):
            array = []
            i = 1
            try:
                while args[i]!="":
                    array.append(args[i])
                    i = int(i)+1
            except IndexError:
                print("Reached the limit.")
            await message.channel.send(random.choice(array))
        if cmd(msg, 'search'):
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
        if cmd(msg, 'emojify'):
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
        if cmd(msg, 'leet'):
            array = list(unprefixed)
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
        if cmd(msg, 'length'):
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
        if cmd(msg, 'randomword'):
            toEdit = await message.channel.send(str(client.get_emoji(BotEmotes.loading)) + ' | Please wait...')
            data = myself.api("https://random-word-api.herokuapp.com/word?number=1")
            await toEdit.edit(content=str(data[0]))
        if cmd(msg, 'inspirobot'):
            async with message.channel.typing():
                img = myself.insp('https://inspirobot.me/api?generate=true')
                await message.channel.send(file=discord.File(Painter.urltoimage(img), 'inspirobot.png'))
        if cmd(msg, 'meme'):
            data = myself.api("https://meme-api.herokuapp.com/gimme")
            embed = discord.Embed(colour = 0x00ff00)
            embed.set_author(name=data["title"], url=data["postLink"])
            if data["nsfw"]:
                embed.set_footer(text='WARNING: IMAGE IS NSFW.')
            else:
                embed.set_image(url=data["url"])
            await message.channel.send(embed=embed)
        if cmd(msg, 'atbash'):
            if no_args:
                await message.channel.send(str(client.get_emoji(BotEmotes.error)) + ' | Invalid. Please give us the word to encode...')
            else:
                await message.channel.send(myself.atbash(unprefixed))
        if cmd(msg, 'caesar'):
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
        if cmd(msg, 'binary'):
            if no_args:
                await message.channel.send(f'Please send something to encode to binary!\nExample: `{prefix}binary {message.author.name}`')
            else:
                text = unprefixed
                if len(myself.bin(text))>4096:
                    await message.channel.send('The binary result is too long... '+myself.bin('lol uwu'))
                else:
                    await message.channel.send(f'```{myself.bin(text)}```')
        if cmd(msg, 'bored'):
            data = myself.api("https://www.boredapi.com/api/activity?participants=1")
            await message.channel.send('**Feeling bored?**\nWhy don\'t you '+str(data['activity'])+'? :wink::ok_hand:')
        if cmd(msg, '8ball'):
            async with message.channel.typing():
                data = myself.api("https://yesno.wtf/api")
                await message.channel.send(content=data['answer'], file=discord.File(Painter.urltoimage(data['image']), data['answer']+'.png'))
        if cmd(msg, 'deathnote'):
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
        if cmd(msg, 'lovelevel'):
            nums = list(range(0, 100))
            if no_args:
                await message.channel.send(str(client.get_emoji(BotEmotes.error)) + ' | Error: Please mention someone you love (lenny)')
            elif len(args)==2:
                await message.channel.send('Love level of '+message.author.name+' with <@!'+str(args[1][3:][:-1])+'> is **'+str(random.choice(nums))+'%.**')
        if cmd(msg, 'gaylevel'):
            if no_args:
                await message.channel.send(str(client.get_emoji(BotEmotes.error)) + ' | SomeoneError: Say/mention someone!')
            else:
                nums = list(range(0, 101))
                await message.channel.send('The gayness level of '+msg[10:]+' is **'+str(random.choice(nums))+'%.**')
        if cmd(msg, 'secret'):
            member = []
            for i in range(0, int(len(message.guild.members))):
                if message.guild.members[i].name!=message.author.name and message.guild.members[i].name!=message.author.name:
                    member.append(message.guild.members[i].name)
            secretlist = src.getSecrets()
            await message.author.send('Did you know?\n'+random.choice(member)+str(random.choice(secretlist))+'\nDon\'t tell this to anybody else.')
            await message.channel.send('I shared the secret through DM. don\'t show anyone else! :wink::ok_hand:')
        if cmd(msg, 'reactmsg'):
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
        if cmd(msg, 'wonka') or cmd(msg, 'avmeme') or cmd(msg, 'buzz') or cmd(msg, 'doge') or cmd(msg, 'fry') or cmd(msg, 'philosoraptor') or cmd(msg, 'money'):
            if cmd(msg, 'avmeme'):
                async with message.channel.typing():
                    try:
                        av = message.mentions[0].avatar_url
                        mes = message.content[int(len(args[0])+len(args[1])+1):]
                        top = myself.urlify(mes.split('[')[1].split(']')[0])
                        bott = myself.urlify(mes.split('[')[2].split(']')[0])
                        name = 'custom'
                        extr = '?alt='+str(av).replace('webp', 'png')
                        url='https://memegen.link/'+str(name)+'/'+str(top)+'/'+str(bott)+'.jpg'+str(extr)
                        await message.channel.send(file=discord.File(Painter.urltoimage(url), 'avmeme.png'))
                    except Exception as e:
                        await message.channel.send(str(client.get_emoji(BotEmotes.error)) +f' | Error!\n```{e}```Invalid parameters. Example: `{prefix}avmeme <tag someone> [top text] [bottom text]`')
            else:
                async with message.channel.typing():
                    try:
                        top = myself.urlify(unprefixed.split('[')[1].split(']')[0])
                        bott = myself.urlify(unprefixed.split('[')[2].split(']')[0])
                        name = args[0][1:]
                        url='https://memegen.link/'+str(name)+'/'+str(top)+'/'+str(bott)+'.jpg?watermark=none'
                        await message.channel.send(file=discord.File(Painter.urltoimage(url), args[0][1:]+'.png'))
                    except Exception as e:
                        await message.channel.send(str(client.get_emoji(BotEmotes.error)) +f' | Error!\n```{e}```Invalid parameters.')
        if cmd(msg, 'barcode'):
            if no_args:
                await message.channel.send('Please provide a text!')
            else:
                if '/' in msg or '?' in msg:
                    await message.channel.send('Please input one without `/` or `?`!')
                else:
                    async with message.channel.typing():
                        url='http://www.barcode-generator.org/zint/api.php?bc_number=20&bc_data='+str(myself.urlify(unprefixed))
                        await message.channel.send(file=discord.File(Painter.urltoimage(url), 'barcode.png'))
        if cmd(msg, 'weather'):
            if no_args:
                await message.channel.send(f'Please send a **City name!**\nExample: `{prefix}weather New York`')
            else:
                url='https://wttr.in/'+str(myself.urlify(unprefixed))+'.png?m'
                await message.channel.send(file=discord.File(Painter.urltoimage(url), 'weather.png'))
        if cmd(msg, 'github'):
            embed = discord.Embed(title="Click me to visit the Bot's github page.", colour=discord.Colour.from_rgb(123, 63, 0), url='https://github.com/vierofernando/username601')
            await message.channel.send(embed=embed)
        if cmd(msg, 'quote'):
            data = myself.insp('https://quotes.herokuapp.com/libraries/math/random')
            text = data.split(' -- ')[0]
            quoter = data.split(' -- ')[1]
            embed = discord.Embed(title='Quotes', description=text+'\n\n - '+quoter+' - ', colour=discord.Colour.from_rgb(123, 63, 0))
            await message.channel.send(embed=embed)
        if cmd(msg, 'trivia'):
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
                embed = discord.Embed(title='Trivia!', description='**'+q['question']+'**\n'+choices, colour=discord.Colour.from_rgb(123, 63, 0))
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
        if cmd(msg, 'rhyme'):
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
                        embed = discord.Embed(title='Words that rhymes with '+msg[int(len(args[0])+1):]+':', description=words, colour=discord.Colour.from_rgb(123, 63, 0))
                        await wait.edit(content='', embed=embed)

print('Logging in to discord...')
client.run(fetchdata['DISCORD_TOKEN'])