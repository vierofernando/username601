import random
prefix = '>'
cmdtypes = ['Bot help', 'Moderation', 'Utilities', 'Math', 'Fun', 'Games', 'Encoding', 'Images', 'Apps']
bot_ver = '1.9.5'
bot_changelog = 'MEME update! and added barcode encoder uwu'

def randomhash():
    hashh = ''
    for i in range(0, random.randint(13, 21)):
        hashh = hashh + random.choice(list('ABCDEFHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789-_'))
    return hashh

def getBinary(a):
    if a=='main':
        return '01101000011101000111010001110000011100110011101000101111001011110111011101110111011101110010111001111001011011110111010101110100011101010110001001100101001011100110001101101111011011010010111101110111011000010111010001100011011010000011111101110110001111010110010001010001011101110011010001110111001110010101011101100111010110000110001101010001'
def getPrefix():
    return prefix

def hintify(word):
    arr = list(word)
    alph = []
    for i in range(0, len(arr)):
        if arr[i] not in alph:
            alph.append(arr[i])
    amount = random.randint(1, len(alph)-1)
    temp = list(word)
    removed = []
    for i in range(0, amount):
        toBlacklistNum = random.randint(0, len(alph)-1)
        toBlacklist = alph[toBlacklistNum]
        for i in range(0, len(temp)):
            if temp[i]==toBlacklist:
                temp[i] = '\_'
        removed.append(toBlacklist)
        del alph[toBlacklistNum]
    result = ''.join(temp)
    return result

def convertrgb(hexCode, typ):
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
    if typ=='0':
        return rgb
    else:
        return percentageRgb

# JSON TIME LOL
github_object = {
    "files": [
        {
            "name":"readme.md",
            "type":"to read more info about the repo and the files"
        },
        {
            "name":"bot.py",
            "type":"main bot source code. commands belong here."
        },
        {
            "name":"username601.py",
            "type":"basically like `config.json` for discord.js programmers."
        },
        {
            "name":"discordgames.py",
            "type":"the guy that handles all of games commands from this bot."
        },
        {
            "name":"splashes.py",
            "type":"a big array code for splashes. like random messages (splashes) on your minecraft main menu."
        },
        {
            "name":".gitignore",
            "type":"the code that ignores my git commits."            
        },
        {
            "name":"assets (DIRECTORY)",
            "type":"all the bot's assets, like .png files."
        }
    ]
}

bothelp = 'vote, feedback [text], help, about, github, connections, inviteme, createbot, ping'
maths = 'math [num] [sym] [num], factor [num], multiplication [num], sqrt [num], isprime [num], rng [num], median [array], mean [array]'
encoding = 'barcode [word], ascii [word], binary [text], supreme [text], reverse [text], length [text], qr [text], leet [text], emojify [text]'
games = 'pokequiz, guessnum, tictactoe [symbol], hangman, mathquiz, geoquiz, guessavatar, coin, dice, rock, paper, scissors, gddaily, gdweekly, gdcomment, gdbox [text], gdlogo [text], gdprofile [name], gdsearch [level name], gdlevel [level id]'
fun = 'hack [tag], tts [text], joke, memes, slap [tag], hbd [tag], xpbox, gaylevel [tag], randomavatar, secret, inspirobot, meme, 8ball, deathnote, choose [array]'
images = 'avmeme [tag] [top text] [bottom text], wonka [top text] [bottom text], buzz [top txt] [bottom txt], doge [top txt] [bottom txt], fry [top txt] [bottom txt], philosoraptor [top txt] [bottom txt], money [top txt] [bottom txt], ph help, ship, coffee, wallpaper, trash [tag], jpeg [tag], cat, sadcat, dog, fox, bird, magik [tag], facts [text], invert [tag], pixelate [tag], b&w [tag], drake help, salty [tag], wooosh [tag], captcha [text], achieve [text], scroll [text], call [text], challenge [text], didyoumean help'
utilities = 'robohash, weather [city], colorinfo [hex], embed help, ss --help, catfact, dogfact, funfact, steam [profile], googledoodle, bored, search [query], randomcolor, randomword, country [name], time, newemote, ghiblifilms, ytthumbnail [link]'
discordAPI = 'lockdown [seconds], slowmode [seconds], ar [tag] [role], rr [tag] [role], clear [count], kick [tag] [reason], ban [tag] [reason], nick [tag] [new nick], makechannel [type] [name], emojiinfo [emoji], permissions [user_tag], roleinfo [tag], id [tag], getinvite, botmembers, serverinfo, servericon, avatar [tag], userinfo [tag], roles, channels, serveremojis, reactmsg [text], reactnum [num1] [num2]'
apps = 'imdb, translate, wikipedia'
commandLength = [len(bothelp.split(',')), len(maths.split(',')), len(encoding.split(',')), len(games.split(',')), len(fun.split(',')), len(utilities.split(',')), len(discordAPI.split(',')), len(images.split(',')), len(apps.split(','))]
totalLength = 0
for i in range(0, len(commandLength)):
    totalLength = int(totalLength) + int(commandLength[i])

ordertypes = [
    '**Bot help ('+str(commandLength[0])+')**\n```'+str(bothelp)+'```',
    '**Moderation ('+str(commandLength[6])+')**\n```'+str(discordAPI)+'```',
    '**Utilities ('+str(commandLength[5])+')**\n```'+str(utilities)+'```',
    '**Math ('+str(commandLength[1])+')**\n```'+str(maths)+'```',
    '**Fun ('+str(commandLength[4])+')**\n```'+str(fun)+'```',
    '**Games ('+str(commandLength[3])+')**\n```'+str(games)+'```',
    '**Encoding ('+str(commandLength[2])+')**\n```'+str(encoding)+'```',
    '**Images ('+str(commandLength[7])+')**\n```'+str(images)+'```',
    '**Apps ('+str(commandLength[8])+')**\n```'+str(apps)+'```'
]