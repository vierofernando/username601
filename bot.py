import discord
import urllib.request
import json
import random
import math
from PIL import Image
from discord.ext.commands import Bot
from discord.ext import commands
client = discord.Client()
clientOld = Bot(command_prefix=">")

with open('brain.json', 'r') as f:
    components = json.load(f)
    prefix = components["prefix"]
    token = components["token"]

@client.event
async def on_ready():
    print('Bot is online.\n=== USERNAME601 CONSOLE ===\nBuilt using Python by Viero Fernando (c) 2020.\n\n'.format(client))

@client.event

async def on_message(message):
    #GENERAL
    msgAuthor = message.author
    msgAuthor = str(msgAuthor)[:-5]
    msg = message.content.lower()
    null = " "
    splitted = message.content.split()
    print(str(msgAuthor)+' SAYS: "'+message.content+'"')
    
    #MAIN COMMANDS
    if msg.startswith(prefix+'say'):
        toSay = []
        for i in range(1, int(len(splitted))):
            toSay.append(splitted[i])
        await message.channel.send(str(null.join(toSay)))
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
            await message.channel.send('OverloadInputError: Beyond the limit of 999999.')
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
            await message.channel.send(data["url"]+" ("+str(size)+" KB")
    if msg.startswith(prefix+"cat") or msg.startswith(prefix+"cats"):
        response = urllib.request.urlopen("https://aws.random.cat/meow")
        data = json.loads(response.read())
        await message.channel.send(data["file"])
    if msg.startswith(prefix+"gddaily"):
        await message.channel.send("Retrieving Data...")
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
        embed.set_footer(text='Made possible by GDBrowser API')
        embed.set_author(name=data["author"], icon_url=image)
        embed.add_field(name='Uploaded at', value=data["uploaded"], inline='True')
        embed.add_field(name='Updated at', value=data["updated"]+" (Version "+data["version"]+")", inline='True')
        embed.add_field(name='Difficulty', value=data["difficulty"])
        embed.add_field(name='Level Stats', value=str(data["likes"])+' likes\n'+str(data["downloads"])+" downloads", inline='False')
        embed.add_field(name='Level Rewards', value=str(data["stars"])+" stars\n"+str(data["orbs"])+" orbs\n"+str(data["diamonds"])+" diamonds")
        embed.add_field(name='Leaderboard', value="**Rank #1: "+str(leader[1]["username"])+"** "+str(leader[1]["percent"])+"% | "+str(leader[1]["date"])+"\n**Rank #2: "+str(leader[2]["username"])+"** "+str(leader[2]["percent"])+"% | "+str(leader[2]["date"])+"\n**Rank #3: "+str(leader[3]["username"])+"** "+str(leader[3]["percent"])+"% | "+str(leader[3]["date"]))
        await message.channel.send(embed=embed)
    if msg.startswith(prefix+"gdweekly"):
        await message.channel.send("Retrieving Data...")
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
        embed.set_footer(text='Made possible by GDBrowser API')
        embed.set_author(name=data["author"], icon_url=image)
        embed.add_field(name='Uploaded at', value=data["uploaded"], inline='True')
        embed.add_field(name='Updated at', value=data["updated"]+" (Version "+data["version"]+")", inline='True')
        embed.add_field(name='Difficulty', value=data["difficulty"])
        embed.add_field(name='Level Stats', value=str(data["likes"])+' likes\n'+str(data["downloads"])+" downloads", inline='False')
        embed.add_field(name='Level Rewards', value=str(data["stars"])+" stars\n"+str(data["orbs"])+" orbs\n"+str(data["diamonds"])+" diamonds")
        embed.add_field(name='Leaderboard', value="**Rank #1: "+str(leader[1]["username"])+"** "+str(leader[1]["percent"])+"% | "+str(leader[1]["date"])+"\n**Rank #2: "+str(leader[2]["username"])+"** "+str(leader[2]["percent"])+"% | "+str(leader[2]["date"])+"\n**Rank #3: "+str(leader[3]["username"])+"** "+str(leader[3]["percent"])+"% | "+str(leader[3]["date"]))
        await message.channel.send(embed=embed)
    if msg.startswith(prefix+"gdprofile"):
        urlArr = []
        for i in range(1, int(len(splitted))):
            if i==int(len(splitted))-1:
                urlArr.append(splitted[i])
            else:
                urlArr.append(splitted[i]+"%20")
        url = "".join(urlArr)
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
        embed.set_footer(text='Made possible by GDBrowser API')
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
        print(hexCode)
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
        img = Image.new('RGB', (100, 100), color = (int(rgb[0]), int(rgb[1]), rgb[2]))
        img.save('preview.png')
        imgFile = discord.File("preview.png", filename="preview.png")
        await message.channel.send("**Hex: #"+str(hexCode)+"**\n\nInteger: "+str(colorInt)+"\n**Red:** "+str(rgb[0])+" ("+str(percentageRgb[0])+"%)\n**Green:** "+str(rgb[1])+" ("+str(percentageRgb[1])+"%)\n**Blue:** "+str(rgb[2])+" ("+str(percentageRgb[2])+"%)\n\nPreview:\n", file=imgFile)
    if msg.startswith(prefix+"countryinfo") or msg.startswith(prefix+"country"):
        before = list(splitted[1])
        urlArr = []
        for i in range(1, int(len(before))):
            if before[i]==" ":
                urlArr.append("%20")
            else:
                urlArr.append(before[i])
        country = "".join(urlArr)
        link = "https://restcountries.eu/rest/v2/name/"+str(country)
        print(link)
        response = urllib.request.urlopen(link)
        c = json.loads(response.read())
        embed = discord.Embed(
            title = c[0]['nativeName'],
            description = '**Capital:** '+str(c[0]['capital'])+'\n**Region: **'+str(c[0]['region'])+'\n**Sub Region: **'+str(c[0]['subregion'])+"\n**Population: **"+str(c[0]['population'])+"\n**Area: **"+str(c[0]['area'])+' km²\n**Time Zones:** '+str(c[0]['timezones'])+'\n**Borders: **'+str(c[0]['borders']),
            colour = 0xffffff
        )
        embed.set_footer(text='Made possible by RestCountries API')
        embed.set_author(name=c[0]['name'])
        await message.channel.send(embed=embed)
    if msg.startswith(prefix+'commands'):
        commands = open("commands.txt", "r")
        embed = discord.Embed(
            title = 'Bot Commands',
            description = '```'+commands.read()+'```',
            colour = 0xffffff
        )
        await message.channel.send(embed=embed)
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
        embed.add_field(name='Programmer info', value='**Programmed by: **Viero Fernando.\n**Server: **discord.gg/HhAPkD8. Don\'t join.\n**Is programming hard? **I dunno', inline='True')
        embed.add_field(name='Version Information', value='**Current Version: **'+verInfo["ver"]+'\n**Update time: **'+verInfo["time"]+'\n**Changelog: **'+verInfo["changelog"], inline='True')
        embed.add_field(name='Join this useless bot to your server!', value='http://vierofernando.github.io/programs/username601', inline='False')
        embed.add_field(name='Open Source Project! Source code here.', value='http://github.com/vierofernando/username601', inline='False')
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
        embed.set_footer(text='Made possible by World Clock API')
        await message.channel.send(embed=embed)
    if msg.startswith(prefix+'joke') or msg.startswith(prefix+'jokes'):
        response = urllib.request.urlopen("https://official-joke-api.appspot.com/jokes/general/random")
        data = json.loads(response.read())
        embed = discord.Embed(
            title = str(data[0]["setup"]),
            description = '||'+str(data[0]["punchline"])+'||',
            colour = discord.Colour.blue()
        )
        embed.set_footer(text='Made possible by Joke API')
        await message.channel.send(embed=embed)
    if msg.startswith(prefix+'qr'):
        before = list(str(msg)[3:])
        urlArr = []
        for i in range(1, int(len(before))):
            if before[i]==" ":
                urlArr.append("%20")
            else:
                urlArr.append(before[i])
        content = "".join(urlArr)
        link = "https://api.qrserver.com/v1/create-qr-code/?size=150x150&data="+str(content)
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
client.run(token)