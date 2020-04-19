print('Please wait...')
import json
with open('brain.json', 'r') as note:
    components = json.load(note)
    prefix = components["prefix"]
    token = components["token"]
from discord.utils import get
import os
import discord
import urllib.request
import random
import math
import requests
import time
import PIL
import PIL.Image as Image
import PIL.ImageDraw as ImageDraw
import PIL.ImageFont as ImageFont
from discord.ext.commands import Bot
from discord.ext import commands
client = discord.Client()
clientOld = Bot(command_prefix=prefix)

@client.event
async def on_ready():
    game = discord.Game("with YOU")
    await client.change_presence(status=discord.Status.online, activity=game)
    print('Bot is online.\n=== USERNAME601 CONSOLE ===\nBuilt using Python by Viero Fernando (c) 2020.\n\n'.format(client))

@client.event
async def on_message(message):
    if message.content==prefix+"ping":
        await message.channel.send('**Pong!**\n'+str(round(client.latency*1000))+' ms.')
    sayTag = ["ya liek tagz?", "we don't accept services with tags, sorry.", "tag me? lol NO.", 'why command me with a tag? that is so unnecessary!', 'NO TAG, ~~NO~~ YES SERVICE.', 'MORE TAG, LESS SERVICE.', 'Everybody gangsta until somebody tagged username601', 'Taggy taggy tag tag!', 'Playin\' with tagz, bro?', 'So uhh i heard u liek tagz', 'What kind of word is that?']
    #GENERAL
    msgAuthor = message.author
    msgAuthor = str(msgAuthor)[:-5]
    msg = message.content.lower()
    null = " "
    splitted = message.content.split()
    #MAIN COMMANDS
    if '<@!696973408000409626>' in msg and msg.startswith(prefix):
        print('[BOT sugg. by: '+str(msgAuthor)+'] Doing commands... PINGED ('+str(splitted[0][1:])+')')
        await message.channel.send(random.choice(sayTag))
    elif msg.startswith(prefix):
        print('[BOT sugg. by: '+str(msgAuthor)+'] Doing commands... ('+str(splitted[0][1:])+')')
        if msg.startswith(prefix+'say'):
            if splitted[1]=='hide':
                await message.delete()
                say = msg[10:]
            else:
                say = msg[5:]
            await message.channel.send(str(say))
        if msg.startswith(prefix+'isprime'):
            if int(splitted[1])<999999:
                numsArray = range(2, int(splitted[1]))
                id = 0
                canBeDividedBy = []
                for k in range(0, int(len(numsArray))):
                    if int(splitted[1])%numsArray[k]==0:
                        id = 1
                        canBeDividedBy.append(str(numsArray[k]))
                if id==0:
                    await message.channel.send("YES. "+str(splitted[1])+" is a prime number.")
                else:
                    await message.channel.send("NO. "+str(splitted[1])+" can be divided by "+str(canBeDividedBy)+".")
            else:
                await message.channel.send('OverloadInputError: Beyond the limit of 999999')
        if msg.startswith(prefix+'catfact'):
            catWait = await message.channel.send('Please wait...')
            response = urllib.request.urlopen("https://catfact.ninja/fact")
            data = json.loads(response.read())
            embed = discord.Embed(
                title = 'Did you know;',
                description = data["fact"],
                color = 0x333333
            )
            await catWait.edit(content='', embed=embed)
        if msg.startswith(prefix+'ytthumbnail'):
            if splitted[1].startswith('https://youtu.be/'):
                videoid = splitted[1][17:]
            elif splitted[1].startswith('http://youtu.be/'):
                videoid = splitted[1][16:]
            elif splitted[1].startswith('https://youtube.com/watch?v='):
                videoid = splitted[1][28:]
            elif splitted[1].startswith('https://www.youtube.com/watch?v='):
                videoid = splitted[1][32:]
            else:
                videoid = 'dQw4w9WgXcQ'
            await message.delete()
            embed = discord.Embed(title='Thumbnail for '+str(splitted[1]), color=0xff0000)
            embed.set_image(url='https://img.youtube.com/vi/'+str(videoid)+'/mqdefault.jpg')
            await message.channel.send(embed=embed)
        if msg.startswith(prefix+'hack'):
            wait = await message.channel.send('Hacking...  Please wait...')
            response = urllib.request.urlopen('https://randomuser.me/api')
            data = json.loads(response.read())
            if data['results'][0]['gender']=='male':
                colorhex = discord.Colour.blue()
            else:
                colorhex = discord.Colour.magenta()
            phone = str(data['results'][0]['phone'][:-4])+'\*\*\*\*'
            username = data['results'][0]['login']['username']
            email = data['results'][0]['email'].replace('example', 'hacked')
            password = ''
            for i in range(0, int(len(data['results'][0]['login']['password']))):
                password = password+str('\*')
            embed = discord.Embed (
                title = str(data['results'][0]['name']['title'])+'. '+str(str(data['results'][0]['name']['first']))+' '+str(data['results'][0]['name']['last']),
                color = colorhex
            )
            embed.add_field(name='Location', value='**'+str(data['results'][0]['location']['street']['number'])+' '+str(data['results'][0]['location']['street']['name'])+'**\n**'+str(data['results'][0]['location']['postcode'])+' '+str(data['results'][0]['location']['city'])+', '+str(data['results'][0]['location']['state'])+', '+str(data['results'][0]['location']['country'])+'**\n**'+str(data['results'][0]['location']['coordinates']['latitude'])+', '+str(data['results'][0]['location']['coordinates']['longitude'])+'**', inline='True')
            embed.add_field(name='Login Information', value='**E-mail address: **'+str(email)+'\n**Username: **'+str(username)+'\n**Password: **'+str(password), inline='True')
            embed.add_field(name='Personal Information', value='**Date of Birth: **'+str(data['results'][0]['dob']['date'][:-14])+'\n**Phone Number: **'+str(phone), inline='True')
            embed.set_thumbnail(url=data['results'][0]['picture']['thumbnail'])
            await wait.edit(content='', embed=embed)
        if msg.startswith(prefix+'ghiblifilms'):
            wait = await message.channel.send('Please wait... Getting data...')
            response = urllib.request.urlopen('https://ghibliapi.herokuapp.com/films')
            data = json.loads(response.read())
            if len(splitted)==1:
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
                num = int(splitted[1])-1
                embed = discord.Embed(
                    title = data[num]['title'] + ' ('+str(data[num]['release_date'])+')',
                    description = '**Rotten Tomatoes Rating: '+str(data[num]['rt_score'])+'%**\n'+data[num]['description'],
                    color = 0x00ff00
                )
                embed.add_field(name='Directed by', value=data[num]['director'], inline='True')
                embed.add_field(name='Produced by', value=data[num]['producer'], inline='True')
                await wait.edit(content='', embed=embed)
        if msg.startswith(prefix+'test'):
            thing = await client.fetch_emojis()
            print(thing)
        if msg.startswith(prefix+'servericon'):
            if message.guild.is_icon_animated()==True:
                await message.channel.send('https://cdn.discordapp.com/icons/'+str(message.guild.id)+'/'+str(message.guild.icon)+'.gif?size=128')
            else:
                await message.channel.send('https://cdn.discordapp.com/icons/'+str(message.guild.id)+'/'+str(message.guild.icon)+'.png?size=128')
        if msg.startswith(prefix+'serverinfo'):
            botcount = 0
            for i in range(0, int(len(message.guild.members))):
                if message.guild.members[i].bot==True:
                    botcount = int(botcount)+1
            humans = int(len(message.guild.members))-int(botcount)
            embed = discord.Embed(
                title=str(message.guild.name),
                description='Shows the information about '+str(message.guild.name),
                color=0x000000
            )
            embed.add_field(name='General Info', value='**Region:** '+str(message.guild.region)+'\n**Server ID: **'+str(message.guild.id)+'\n**Server Icon ID: **'+str(message.guild.icon)+'\n**Verification Level: **'+str(message.guild.verification_level)+'\n**Notification level:  **'+str(message.guild.default_notifications)[18:].replace("_", " ")+'\n**Explicit Content Filter:**'+str(message.guild.explicit_content_filter)+'\n**AFK timeout: **'+str(message.guild.afk_timeout)+' seconds\n**Description: **"'+str(message.guild.description)+'"', inline='True')
            embed.add_field(name='Channel Info', value='**Text Channels: **'+str(len(message.guild.text_channels))+'\n**Voice channels: **'+str(len(message.guild.voice_channels))+'\n**Channel categories: **'+str(len(message.guild.categories))+'\n**AFK Channel: **'+str(message.guild.afk_channel), inline='True')
            embed.add_field(name='Members Info', value='**Server owner: **'+str(message.guild.owner)[:-5]+'\n**Members count: **'+str(len(message.guild.members))+'\n**Server Boosters: **'+str(len(message.guild.premium_subscribers))+'\n**Role Count: **'+str(len(message.guild.roles))+'\n**Bot accounts: **'+str(botcount)+'\n**Human accounts: **'+str(humans), inline='True')
            embed.add_field(name='URL stuff', value='**Server URL: **'+str('https://discordapp.com/channels/'+str(message.guild.id))+'\n**Server Icon URL (static): **'+str('https://cdn.discordapp.com/icons/'+str(message.guild.id)+'/'+str(message.guild.icon)+'.png?size=128'))
            embed.set_thumbnail(url=str('https://cdn.discordapp.com/icons/'+str(message.guild.id)+'/'+str(message.guild.icon)+'.png?size=128'))
            await message.channel.send(embed=embed)
        if msg.startswith(prefix+'factor'):
            if int(splitted[1])<999999:
                numList = range(1, int(splitted[1]))
                factor = []
                for i in range(0, int(len(numList))):
                    if int(splitted[1])%int(numList[i])==0:
                        factor.append(numList[i])
                factor.append(int(splitted[1]))
                await message.channel.send(str(factor))
            else:
                await message.channel.send('OverloadInputError: Beyond the limit of 999999.')
        if msg.startswith(prefix+'multiplication'):
            arr = []
            for i in range(1, 15):
                arr.append(int(splitted[1])*i)
            await message.channel.send(str(arr))
        if msg.startswith(prefix+'id'):
            var = splitted[1]
            if (splitted[1].startswith('<#')):
                var = var[2:]
            else:
                var = var[3:]
            var = var[:-1]
            await message.channel.send(str(var))
        if msg.startswith(prefix+"math"):
            if int(len(splitted))>4:
                await message.channel.send("OverloadEquationError: So far this bot only accept one equation.")
            else:
                num1 = int(splitted[1])
                num2 = int(splitted[3])
                inputtedSym = str(splitted[2])
                if inputtedSym=="+":
                    sym = "+"
                elif inputtedSym=="-":
                    sym = "-"
                elif inputtedSym=="*" or inputtedSym=="x" or inputtedSym=="×":
                    sym = "*"
                elif inputtedSym=="/" or inputtedSym==":" or inputtedSym=="÷":
                    sym = "/"
                elif inputtedSym=="^" or inputtedSym=="**":
                    sym = "**"
                else:
                    await message.channel.send("InvalidSymbolError: Invalid symbol for equation.\nSupported symbol: `+ - * x × / : ÷ ^ **`")
                if sym=="+":
                    result = int(num1)+int(num2)
                    symId = 0
                elif sym=="-":
                    result = int(num1)-int(num2)
                    symId = 0
                elif sym=="*":
                    symId = 0
                    result = int(num1)*int(num2)
                elif sym=="/":
                    symId = 1
                    result = int(num1)/int(num2)
                    rounded = round(int(result))
                elif sym=="**":
                    symId = 0
                    result = int(num1)**int(num2)
                if symId==0:
                    await message.channel.send(str(num1)+" "+str(sym)+" "+str(num2)+" = "+str(result))
                elif symId==1:
                    await message.channel.send(str(num1)+" "+str(sym)+" "+str(num2)+" = "+str(result)+"\nRound number: "+str(rounded))
        if msg.startswith(prefix+"rng") or msg.startswith(prefix+"randomnumber") or msg.startswith(prefix+"randint"):
            beginning = int(splitted[1])
            ending = int(splitted[2])
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
        if msg.startswith(prefix+"dog") or msg.startswith(prefix+"dogs"):
            response = urllib.request.urlopen("https://random.dog/woof.json")
            data = json.loads(response.read())
            if int(data["fileSizeBytes"])>1000000:
                size = int(data["fileSizeBytes"])/1000000
                await message.channel.send(data["url"]+" ("+str(size)+" MB)")
            else:
                size = int(data["fileSizeBytes"])/1000
                await message.channel.send(data["url"]+" ("+str(size)+" KB)")
        if msg==prefix+"cat" or msg.startswith(prefix+"cats"):
            response = urllib.request.urlopen("https://aws.random.cat/meow")
            data = json.loads(response.read())
            await message.channel.send(data["file"])
        if msg.startswith(prefix+'roles'):
            serverroles = ""
            warning = "No warnings available."
            for i in range(1, int(len(message.guild.roles))):
                num = int(len(message.guild.roles))-int(i)
                if len(serverroles)>2048:
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
            response = urllib.request.urlopen("https://gdbrowser.com/api/level/daily")
            data = json.loads(response.read())
            responseLeaderboard = urllib.request.urlopen("https://gdbrowser.com/api/leaderboardLevel/"+str(data["id"]))
            leader = json.loads(responseLeaderboard.read())
            image = 'https://gdbrowser.com/icon/'+data["author"]
            embed = discord.Embed(
                title = data["name"]+' ('+data["id"]+')',
                description = data["description"],
                colour = discord.Colour.blue()
            )
            embed.set_author(name=data["author"], icon_url=image)
            embed.add_field(name='Uploaded at', value=data["uploaded"], inline='True')
            embed.add_field(name='Updated at', value=data["updated"]+" (Version "+data["version"]+")", inline='True')
            embed.add_field(name='Difficulty', value=data["difficulty"])
            embed.add_field(name='Level Stats', value=str(data["likes"])+' likes\n'+str(data["downloads"])+" downloads", inline='False')
            embed.add_field(name='Level Rewards', value=str(data["stars"])+" stars\n"+str(data["orbs"])+" orbs\n"+str(data["diamonds"])+" diamonds")
            embed.add_field(name='Leaderboard', value="**Rank #1: "+str(leader[1]["username"])+"** "+str(leader[1]["percent"])+"% | "+str(leader[1]["date"])+"\n**Rank #2: "+str(leader[2]["username"])+"** "+str(leader[2]["percent"])+"% | "+str(leader[2]["date"])+"\n**Rank #3: "+str(leader[3]["username"])+"** "+str(leader[3]["percent"])+"% | "+str(leader[3]["date"]))
            await toEdit.edit(content='', embed=embed)
        if msg.startswith(prefix+'botmembers'):
            botmembers = ""
            warning = 'No errors found. Congrats! ^_^'
            for i in range(0, int(len(message.guild.members))):
                if len(botmembers)>2048:
                    warning = 'Error: Too many bots, some bot are not listed above.'
                if message.guild.members[i].bot==True:
                    botmembers = botmembers + message.guild.members[i].name + '\n'
            embed = discord.Embed(
                title = 'Bot members of '+message.guild.name+':',
                description = str(botmembers),
                colour = discord.Colour.dark_blue()
            )
            embed.set_footer(text=warning)
            await message.channel.send(embed=embed)
        if msg.startswith(prefix+"gdweekly"):
            toEdit = await message.channel.send("Retrieving Data...")
            response = urllib.request.urlopen("https://gdbrowser.com/api/level/weekly")
            data = json.loads(response.read())
            responseLeaderboard = urllib.request.urlopen("https://gdbrowser.com/api/leaderboardLevel/"+str(data["id"]))
            leader = json.loads(responseLeaderboard.read())
            image = 'https://gdbrowser.com/icon/'+data["author"]
            embed = discord.Embed(
                title = data["name"]+' ('+data["id"]+')',
                description = data["description"],
                colour = discord.Colour.red()
            )
            embed.set_author(name=data["author"], icon_url=image)
            embed.add_field(name='Uploaded at', value=data["uploaded"], inline='True')
            embed.add_field(name='Updated at', value=data["updated"]+" (Version "+data["version"]+")", inline='True')
            embed.add_field(name='Difficulty', value=data["difficulty"])
            embed.add_field(name='Level Stats', value=str(data["likes"])+' likes\n'+str(data["downloads"])+" downloads", inline='False')
            embed.add_field(name='Level Rewards', value=str(data["stars"])+" stars\n"+str(data["orbs"])+" orbs\n"+str(data["diamonds"])+" diamonds")
            embed.add_field(name='Leaderboard', value="**Rank #1: "+str(leader[1]["username"])+"** "+str(leader[1]["percent"])+"% | "+str(leader[1]["date"])+"\n**Rank #2: "+str(leader[2]["username"])+"** "+str(leader[2]["percent"])+"% | "+str(leader[2]["date"])+"\n**Rank #3: "+str(leader[3]["username"])+"** "+str(leader[3]["percent"])+"% | "+str(leader[3]["date"]))
            await toEdit.edit(content='', embed=embed)
        if msg.startswith(prefix+"gdprofile"):
            url = msg[11:].replace(" ", "%20")
            response = urllib.request.urlopen("https://gdbrowser.com/api/profile/"+url)
            data = json.loads(response.read())
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
        if msg.startswith(prefix+"rock") or msg.startswith(prefix+"paper") or msg.startswith(prefix+"scissor") or msg.startswith(prefix+"scissors"):
            if msg.startswith(prefix+"rock"):
                given = "fist"
            elif msg.startswith(prefix+"paper"):
                given = "hand_splayed"
            elif msg.startswith(prefix+"scissor") or msg.startswith(prefix+"scissors"):
                given = "v"
            messages = ["Congratulations! "+str(msgAuthor)+" WIN!", "It's a draw.", "Oops, "+str(msgAuthor)+" lost!"]
            emojiArray = ["fist", "hand_splayed", "v"]
            ran = random.randint(0, 2)
            if ran==0:
                if given=="fist":
                    msgId = 1
                elif given=="hand_splayed":
                    msgId = 0
                elif given=="v":
                    msgId = 2
            elif ran==1:
                if given=="fist":
                    msgId = 2
                elif given=="hand_splayed":
                    msgId = 1
                elif given=="v":
                    msgId = 0
            elif ran==2:
                if given=="fist":
                    msgId = 0
                elif given=="hand_splayed":
                    msgId = 2
                elif given=="v":
                    msgId = 1
            colors = [discord.Colour.green(), discord.Colour.orange(), discord.Colour.red()]
            embed = discord.Embed(
                title = messages[msgId],
                colour = colors[msgId]
            )
            embed.set_footer(text='Playin\' rock paper scissors w/ '+str(msgAuthor))
            embed.set_author(name="Playing Rock Paper Scissors with "+str(msgAuthor))
            embed.add_field(name=str(msgAuthor), value=':'+given+':', inline="True")
            embed.add_field(name='Username601', value=':'+str(emojiArray[ran])+':', inline="True")
            await message.channel.send(embed=embed)
        if msg.startswith(prefix+"randomcase"):
            statement = []
            for i in range(1, int(len(splitted))):
                statement.append(splitted[i])
                thing = null.join(statement)
            result = []
            letterArr = list(thing)
            for i in range(0, len(thing)):
                ran = random.randint(0, 1)
                if ran==0:
                    result.append(letterArr[i].upper())
                elif ran==1:
                    result.append(letterArr[i].lower())
            await message.channel.send("".join(result))
        if msg.startswith(prefix+"randomcolor"):
            listHex = ["0","1","2","3","4","5","6","7","8","9","A","B","C","D","E","F"]
            hexCode = []
            for i in range(0, 6):
                ran = random.choice(listHex)
                hexCode.append(ran)
            hexCode = "".join(hexCode)
            #CONVERT TO DECIMAL
            uselessArray = list(hexCode)
            part1 = str(uselessArray[0])+str(uselessArray[1])
            part2 = str(uselessArray[2])+str(uselessArray[3])
            part3 = str(uselessArray[4])+str(uselessArray[5])
            partsArray = [part1, part2, part3]
            rgb = []
            percentageRgb = []
            for i in range(0, 3):
                toConvert = partsArray[i]
                stackOverFlow = int(toConvert, 16)
                rgb.append(stackOverFlow)
                percentageRgbAdd = int(rgb[i])/255*100
                percentageRgb.append(round(percentageRgbAdd))
            colorInt = int(hexCode, 16)
            embed = discord.Embed(title='#'+str(hexCode), description="**Integer: **`"+str(colorInt)+"`\n**Red:** "+str(rgb[0])+" ("+str(percentageRgb[0])+"%)\n**Green:** "+str(rgb[1])+" ("+str(percentageRgb[1])+"%)\n**Blue:** "+str(rgb[2])+" ("+str(percentageRgb[2])+"%)", colour=discord.Colour.from_rgb(int(rgb[0]), int(rgb[1]), int(rgb[2])))
            await message.channel.send(embed=embed)
        if msg.startswith(prefix+"country"):
            country = msg[9:].replace(" ", "%20")
            link = "https://restcountries.eu/rest/v2/name/"+str(country.lower())
            print(link)
            response = urllib.request.urlopen(link)
            c = json.loads(response.read())
            embed = discord.Embed(
                title = c[0]['nativeName'],
                description = '**Capital:** '+str(c[0]['capital'])+'\n**Region: **'+str(c[0]['region'])+'\n**Sub Region: **'+str(c[0]['subregion'])+"\n**Population: **"+str(c[0]['population'])+"\n**Area: **"+str(c[0]['area'])+' km²\n**Time Zones:** '+str(c[0]['timezones'])+'\n**Borders: **'+str(c[0]['borders']),
                colour = 0xffffff
            )
            embed.set_author(name=c[0]['name'])
            await message.channel.send(embed=embed)
        if msg.startswith(prefix+'commands'):
            commands = open("commands.txt", "r")
            await message.channel.send(file=discord.File('commands.txt'))
        if msg.startswith(prefix+'help'):
            with open('version.json', 'r') as f:
                verInfo = json.load(f)
            messageRandom = ['Traceback (most recent call last)','I liek memes','601 in my name means BOT in leetspeak.\n*THE MORE YOU KNOW*', 'Hello, discordians! It\'s-a-me. Bot. Which may look stupid the fact that\nthere are THOUSANS of discord bots out there, so *let\'s get straight into it.* (no meme intended)', 'Wha? ME? okay then, here ya go.', 'Here are some silly lil information.', 'Beep boop, beep beep?', 'JavaScript is bad.', 'MEE6 vs Dyno, which is better?', 'MEEx6=MEEMEEMEEMEEMEEMEE', 'my token is = \*Slams head on keyboard*', 'HELP? HELP MEE!!!', 'Don\'t be a broom. Use discord.', 'Discard the discord right away!', 'Garbage bot giving some information here.', 'look, i have challenge for you. Can you read this without blinking?', 'Don\'t laugh at me.', 'Python is for nerds.', 'Everybody gangsta until username601 become self-aware', 'Coding is not fun, but it will pay off.']
            embed = discord.Embed(
                title = 'About this seemingly normal bot.',
                description = random.choice(messageRandom),
                colour = 0xff0000
            )
            embed.add_field(name='Bot general Info', value='**Bot name: ** Username601\n**Programmed in: **Discord.py (Python)\n**Created in: **6 April 2020.\n**Successor of: **somebot56.\n**Default prefix: **>\n**Commands: **Just type >commands.', inline='True')
            embed.add_field(name='Programmer info', value='**Programmed by: **Viero Fernando.\n**Server: **discord.gg/HhAPkD8.\n**Is programming hard? **I dunno', inline='True')
            embed.add_field(name='Version Information', value='**Current Version: **'+verInfo["ver"]+'\n**Update time: **'+verInfo["time"]+'\n**Changelog: **'+verInfo["changelog"], inline='True')
            embed.add_field(name='Join this useless bot to your server!', value='http://vierofernando.github.io/programs/username601', inline='False')
            embed.add_field(name='Open Source Project! Source code here.', value='http://github.com/vierofernando/username601', inline='False')
            embed.add_field(name='Join our support server!', value='http://discord.gg/HhAPkD8', inline='False')
            await message.channel.send(embed=embed)
        if msg.startswith(prefix+'time') or msg.startswith(prefix+'utc'):
            response = urllib.request.urlopen("http://worldtimeapi.org/api/timezone/africa/accra")
            data = json.loads(response.read())
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
                title = str(date)+' | '+str(time),
                description = 'The current time showed is on UTC.\n**Unix Time:** '+str(data["unixtime"])+'\n**Day of the year: **'+str(data["day_of_year"])+' ('+str(progressDayYear)+'%)\n**Day of the week: **'+str(data["day_of_week"])+' ('+str(progressDayWeek)+'%)\n'+str(yearType),
                colour = discord.Colour.green()
            )
            await message.channel.send(embed=embed)
        if msg.startswith(prefix+'joke') or msg.startswith(prefix+'jokes'):
            response = urllib.request.urlopen("https://official-joke-api.appspot.com/jokes/general/random")
            data = json.loads(response.read())
            embed = discord.Embed(
                title = str(data[0]["setup"]),
                description = '||'+str(data[0]["punchline"])+'||',
                colour = discord.Colour.blue()
            )
            await message.channel.send(embed=embed)
        if msg.startswith(prefix+'qr'):
            content = msg[4:].replace(" ", "%20")
            link = "https://api.qrserver.com/v1/create-qr-code/?size=150x150&data="+str(content.lower())
            embed = discord.Embed(
                colour = 0xffffff
            )
            embed.set_author(name="Image not appearing? Try using this link.", url=str(link))
            embed.set_image(url=str(link))
            await message.channel.send(embed=embed)
        if msg.startswith(prefix+'median') or msg.startswith(prefix+'mean'):
            numArray = []
            i = 1
            try:
                while splitted[i]!="":
                    numArray.append(splitted[i])
                    i = int(i)+1
            except IndexError:
                print("Reached the limit.")
            if msg.startswith(prefix+'median'):
                if len(numArray)%2==0:
                    first = int(len(numArray))/2
                    second = int(first) # 1 2 3 4
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
            num = int(splitted[1])
            await message.channel.send(str(math.sqrt(int(num))))
        if msg.startswith(prefix+'reactnum'):
            emojiArr = ['0️⃣', '1️⃣', '2️⃣', '3️⃣', '4️⃣', '5️⃣', '6️⃣', '7️⃣', '8️⃣', '9️⃣']
            begin = int(splitted[1])
            end = int(splitted[2])+1
            errorLevel = 0
            if int(splitted[1])>10 or int(splitted[1])<0 or int(splitted[2])>10 or int(splitted[2])<0:
                errorLevel = 1
            if errorLevel==0:
                for i in range(int(begin), int(end)):
                    await message.add_reaction(emojiArr[i])
            elif errorLevel==1:
                await message.channel.send('Error: Invalid Integer.')
        if msg.startswith(prefix+'slap'):
            gifArr = ["https://tenor.com/vEDn.gif ", "https://tenor.com/QZpI.gif", "https://tenor.com/6i12.gif", "https://tenor.com/RTqL.gif", "https://tenor.com/rhrz.gif", "https://giphy.com/gifs/mary-steenburgen-vxvNnIYFcYqEE", "https://giphy.com/gifs/sweet-penguin-penguins-mEtSQlxqBtWWA", "https://giphy.com/gifs/sherlock-snape-gif-kTBjwh6IWbLPy", "https://giphy.com/gifs/slap-dog-slapping-lX03hULhgCYQ8", "https://tenor.com/QklT.gif", "https://tenor.com/1jyY.gif", "https://tenor.com/6zwG.gif"]
            msgArr = ["Slapped in the face!", "Lemme slap your face for a bit.", "Come here... **SLAP!**", "One slap for you,", "May i slap you?", "SLAP TIME!", "Press F, cuz we just slapped", "GIMME YOUR SLAPPABLE FACE,", "What time is it? **SLAP TIME!**"]
            await message.channel.send(random.choice(msgArr)+" "+str(splitted[1])+"\n"+random.choice(gifArr))
        if msg.startswith(prefix+'hbd'):
            gifArr = ["https://tenor.com/bcdeQ.gif", "https://tenor.com/4flE.gif", "https://tenor.com/3toj.gif", "https://tenor.com/SZbC.gif", "https://tenor.com/1C6f.gif", "https://tenor.com/rzE6.gif", "https://tenor.com/beutC.gif", "https://tenor.com/z9js.gif", "https://tenor.com/v353.gif", "https://tenor.com/wFWQ.gif", "https://tenor.com/OmS5.gif", "https://tenor.com/6BKT.gif", "https://tenor.com/scB9.gif", "https://tenor.com/bc2rQ.gif", "https://tenor.com/paQT.gif", "https://tenor.com/1C6f.gif", "https://tenor.com/GYmM.gif"]
            await message.channel.send("Happy birthday, "+str(splitted[1])+"!\n"+random.choice(gifArr))
        if msg.startswith(prefix+'choose'):
            array = []
            i = 1
            try:
                while splitted[i]!="":
                    array.append(splitted[i])
                    i = int(i)+1
            except IndexError:
                print("Reached the limit.")
            await message.channel.send(random.choice(array))
        if msg.startswith(prefix+'programmer') or msg.startswith(prefix+'whomakeme'):
            embed = discord.Embed(
                title = 'Viero Fernando',
                description = 'Viero Fernando is the author/programmer of this lil\'bot.\n**No, i don\'t team with anyone else, except for StackOverFlow \:)**',
                color = 0x000000
            )
            embed.add_field(name='About the programmar:', value='**Born date: ** 22 April 200X\n**Hobby: **Programming and gaming (and *Discording* probably)\n**Developed:** Individual/Indie-developed.\n**Best Languages: **Python, JavaScript', inline='True')
            embed.add_field(name='Social media:', value='**Discord Server:** discord.gg/HhAPkD8\n**Discord Username:** vierofernando#8620\n**Brainly (ID): **bit.ly/vierofernandobrainly\n**Geometry Dash: **gdbrowser.com/profile/knowncreator56\nThat\'s *ALL* i got, nerd.', inline='True')
            embed.add_field(name='Special Thanks', value='**StackOverFlow**\nDiscord\nDiscord.py and-or Python itself\nYOU for using this bot :)', inline='False')
            await message.channel.send(embed=embed)
        if msg.startswith(prefix+'search'):
            query = msg[8:].replace(" ", "%20")
            embed = discord.Embed(
                title = 'Internet Searches for '+str(msg[8:]),
                color = 0xff0000
            ) # https://en.wikipedia.org/w/index.php?cirrusUserTesting=control&search=adasdssdasasd&title=Special%3ASearch&go=Go&ns0=1
            embed.add_field(name='Google Search', value='http://google.com/search?q='+str(query))
            embed.add_field(name='YouTube results', value='http://youtube.com/results?q='+str(query))
            embed.add_field(name='Wikipedia search', value='https://en.wikipedia.org/w/index.php?cirrusUserTesting=control&search='+str(query)+'&title=Special%3ASearch&go=Go&ns0=1')
            embed.add_field(name='\nInstagram Tag Search', value='https://www.instagram.com/explore/tags/'+str(query)+'/', inline="True")
            embed.add_field(name='Creative Commons Search', value='https://search.creativecommons.org/search?q='+str(query), inline="True")
            embed.add_field(name='WikiHow Search', value='https://www.wikihow.com/wikiHowTo?search='+str(query), inline="True")
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
                        emojified.append(null)
                    else:
                        emojiid = 1
            total = null.join(emojified)
            if emojiid==0:
                await message.channel.send(total)
            else:
                await message.channel.send('BadSymbolError: Error! You added an invalid symbol\nthat cannot be converted to emojis. Sorry.')
        if splitted[0]==prefix+'reverse':
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
            await message.channel.send("**With Spaces:** "+str(withSpaces)+"\n**Without Spaces:** "+str(withoutSpaces))
        if msg.startswith(prefix+'token'):
            randoms = list("abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789-_.")
            ranNum = list(range(35, 45))
            fakeToken = []
            for i in range(0, int(random.choice(ranNum))):
                fakeToken.append(random.choice(randoms))
            if str(''.join(fakeToken))!=token:
                await message.channel.send('Hey, '+str(msgAuthor)+'! my bot token is: \n**'+str("".join(fakeToken))+'**')
            else:
                await message.channel.send('LOL!')
        if msg.startswith(prefix+'randomword'):
            toEdit = await message.channel.send('Please wait...')
            response = urllib.request.urlopen("https://random-word-api.herokuapp.com/word?number=1")
            data = json.loads(response.read())
            await toEdit.edit(content=str(data[0]))
        if msg.startswith(prefix+'inspirobot'):
            url = 'https://inspirobot.me/api?generate=true'
            img = requests.get(url)
            embed = discord.Embed(
                colour = 0xff0000
            )
            embed.set_image(url=str(img.text))
            await message.channel.send(embed=embed)
        if msg.startswith(prefix+'meme'):
            response = urllib.request.urlopen("https://meme-api.herokuapp.com/gimme")
            data = json.loads(response.read())
            embed = discord.Embed(
                colour = 0x00ff00
            )
            embed.set_author(name=data["title"], url=data["postLink"])
            embed.set_image(url=data["url"])
            await message.channel.send(embed=embed)
        if msg.startswith(prefix+'binary'):
            allowed = list("abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ ")
            alph = list("abcdefghijklmnopqrstuvwxyz")
            messageRaw = str(message.content)[8:]
            binary = []
            haveBeen = 0
            arr2 = ["10000", "10001", "10010", "10011", "10100", "10101", "10110", "10111", "11000", "11001"]
            arr = ["00001", "00010", "00011", "00100", "00101", "000110", "00111", "01000", "01001", "01010", "01011", "01100", "01101", "01110", "01111", "10000", "10001", "10010", "10011", "10100", "10101", "10110", "10111", "11000", "11001", "11010"]
            for i in range(0, int(len(messageRaw))):
                if list(messageRaw)[i].lower() in alph:
                    for j in range(0, int(len(alph))):
                        if list(messageRaw)[i].lower()==alph[j]:
                            if list(messageRaw)[i].islower()==True:
                                binary.append('011'+str(arr[j]))
                            elif list(messageRaw)[i].isupper()==True:
                                binary.append('010'+str(arr[j]))
                            break
                elif list(messageRaw)[i].isnumeric()==True:
                    binary.append('001'+str(arr2[int(list(messageRaw)[i])]))
                elif list(messageRaw)[i]==" ":
                    binary.append('00100000')
                elif list(messageRaw)[i]=="!":
                    binary.append('00100001')
                elif list(messageRaw)[i]=="?":
                    binary.append('00111111')
                elif list(messageRaw)[i]=="'":
                    binary.append('00100111')
                elif list(messageRaw)[i]=='.':
                    binary.append('00101110')
                elif list(messageRaw)[i]==',':
                    binary.append('00101100')
                elif list(messageRaw)[i]==':':
                    binary.append('00111010')
                elif haveBeen!=1:
                    await message.channel.send(':warning: Your message contain symbols that didn\'t get encoded to binary.\nAccepted letters are: Alphabet, Numbers, Space, ? ! \' , . :')
                    haveBeen = 1
            await message.channel.send('```'+str(''.join(binary))+'```')
        if msg.startswith(prefix+'bored'):
            response = urllib.request.urlopen("https://www.boredapi.com/api/activity?participants=1")
            data = json.loads(response.read())
            await message.channel.send('**Feeling bored?**\nWhy don\'t you '+str(data['activity'])+'? :wink::ok_hand:')
        if msg.startswith(prefix+'8ball'):
            arr = [':(', 'Not so good.', 'Damn, the future is... ||???||', 'Something is wrong.', 'I doubt it.', 'Why trust me? Trust yourself!', 'oh boy.', 'Great.. so far.', 'It will be the same, yet.', 'Do something.', 'Act something, NOW!', 'I saw a huge ||...something.||']
            if len(splitted)==1:
                await message.channel.send(':8ball: | '+str(random.choice(arr)))
            else:
                response = urllib.request.urlopen("https://yesno.wtf/api")
                data = json.loads(response.read())
                if data['answer']=='no':
                    colorhex = discord.Colour.red()
                else:
                    colorhex = discord.Colour.blue()
                embed = discord.Embed(title=data['answer'], colour=colorhex)
                embed.set_image(url=data['image'])
                await message.channel.send(embed=embed)
        if msg.startswith(prefix+'gaylevel'):
            if len(splitted)==1:
                await message.channel.send('SomeoneError: Say/mention someone!')
            else:
                nums = list(range(0, 101))
                await message.channel.send('The gayness level of '+msg[10:]+' is **'+str(random.choice(nums))+'%.**')
        if msg.startswith(prefix+'reactmsg'):
            messageReact = list(msg[10:])
            used = []
            order = list("abcdefghijklmnopqrstuvwxyz!?0123456789 ")
            validId = 0
            emo = ["🇦", "🇧", "🇨", "🇩", "🇪", "🇫", "🇬", "🇭", "🇮", "🇯", "🇰", "🇱", "🇲", "🇳", "🇴", "🇵", "🇶", "🇷", "🇸", "🇹", "🇺", "🇻", "🇼", "🇽", "🇾", "🇿", "❗", "❓", '0️⃣', '1️⃣', '2️⃣', '3️⃣', '4️⃣', '5️⃣', '6️⃣', '7️⃣', '8️⃣', '9️⃣', '▪️']
            if len(messageReact)<20:
                for i in range(0, int(len(messageReact))):
                    if messageReact[i] in used:
                        await message.channel.send('Error: Your message contain multiple characters. Which is not allowed on reactions.')
                        validId = 1
                        break
                    else:
                        if messageReact[i] in order:
                            for j in range(0, int(len(order))):
                                if messageReact[i]==str(order[j]):
                                    used.append(emo[j])
                        else:
                            await message.channel.send('Error: Your message contain invalid symbols.\nValid: Alphabet Number ? ! space')
                            break
            else:
                await message.channel.send('Érror! Your message contain more than 20 characters.\nWhich is the react message limit.')
            if validId==0:
                for i in range(0, int(len(used))):
                    await message.add_reaction(used[i])
        if msg.startswith(prefix+'pokesprite'):
            try:
                if splitted[1]!="--shiny":
                    poke = msg[12:]
                else:
                    poke = msg[20:]
                loading = await message.channel.send('Please wait...')
                response = urllib.request.urlopen("https://pokeapi.co/api/v2/pokemon/"+str(poke))
                data = json.loads(response.read())
                response2 = urllib.request.urlopen(data["forms"][0]["url"])
                forms = json.loads(response2.read())
                if splitted[1]!="--shiny":
                    sprite = str(forms['sprites']['front_default'])
                else:
                    sprite = str(forms['sprites']['front_shiny'])
                if null in list(poke):
                    poke = poke.replace(" ", "-")
                embed = discord.Embed(
                    title = '(#'+str(data["order"])+') '+str(data["name"]),
                    color = 0xffd700
                )
                embed.set_image(url=sprite)
                await loading.edit(content='', embed=embed)
            except:
                await loading.edit(content='Error: Pokemon not found!')
        if msg.startswith(prefix+'connections'):
            await message.channel.send('I am connected with '+str(len(client.guilds))+' discord servers.\nWith '+str(len(client.emojis))+' custom emojis.\nPlayin\' with '+str(len(client.users))+' members.')
print('Logging in to discord...')
client.run(token)
