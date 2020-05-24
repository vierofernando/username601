import random
import base64
from urllib import requests.urlopen as getapi
from json import loads as jsonify
from requests import get as decodeurl
prefix = '>'
cmdtypes = ['Bot help', 'Moderation', 'Utilities', 'Math', 'Fun', 'Games', 'Encoding', 'Memes', 'Images', 'Apps']
bot_ver = '1.9.6b'
bot_changelog = 'Memes and images category are now seperated.'

def api(url):
    return jsonify(getapi(url).read())

def insp(url):
    return decodeurl(url).text

def randomhash():
    hashh = ''
    for i in range(0, random.randint(13, 21)):
        hashh = hashh + random.choice(list('ABCDEFHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789-_'))
    return hashh

def getPrefix():
    return prefix

def atbash(text):
    temp = list(text.lower())
    alph = list('abcdefghijklmnopqrstuvwxyz')
    hpla = alph[::-1]
    total = ''
    for i in range(0, len(temp)):
        if temp[i] in alph:
            for j in range(0, len(alph)):
                if temp[i]==alph[j]:
                    total += hpla[j]
        else:
            total += temp[i]
    return total

def caesar(text, num):
    temp = text.lower()
    if num>26:
        while num>26:
            num -= 26
    elif num<0:
        while num<0:
            num += 26
    alph = list('abcdefghijklmnopqrstuvwxyz')
    result = ''
    for i in range(0, len(temp)):
        if temp[i] in alph:
            for j in range(0, len(alph)):
                if alph[j]==temp[i]:
                    tempnum = j+num
                    if tempnum>len(alph)-1:
                        while tempnum>len(alph)-1:
                            tempnum -= 26
                    result += alph[tempnum]
                    break
        else:
            result += temp[i]
    return result

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
encoding = 'atbash [word], caesar [offset] [word], base64 [word], barcode [word], ascii [word], binary [text], supreme [text], reverse [text], length [text], qr [text], leet [text], emojify [text]'
games = 'trivia, pokequiz, guessnum, tictactoe [symbol], hangman, mathquiz, geoquiz, guessavatar, coin, dice, rock, paper, scissors, gddaily, gdweekly, gdcomment, gdbox [text], gdlogo [text], gdprofile [name], gdsearch [level name], gdlevel [level id]'
fun = 'hack [tag], tts [text], joke, slap [tag], hbd [tag], xpbox, gaylevel [tag], lovelevel [tag], randomavatar, secret, inspirobot, meme, 8ball, deathnote, choose [array]'
memes = 'meme, imgcaptcha, trap [tag], whowouldwin [tag1] [tag2], threat [tag], phcomment, drake help, scroll [text], call [text], challenge [text], didyoumean help, trumptweet [text], clyde [text], trash [tag], avmeme [tag] [top text] [bottom text], kannagen [text], facts [text], wonka [top text] [bottom text], buzz [top txt] [bottom txt], doge [top txt] [bottom txt], fry [top txt] [bottom txt], philosoraptor [top txt] [bottom txt], money [top txt] [bottom txt], ph help, salty [tag], wooosh [tag], captcha [text], achieve [text]'
images = 'ship, food, coffee, wallpaper, deepfry [tag], blurpify [tag], jpeg [tag], cat, sadcat, dog, fox, bird, magik [tag], invert [tag], pixelate [tag], b&w [tag]'
utilities = 'quote, robohash, weather [city], ufo, colorinfo [hex], rhyme [word], embed help, ss --help, catfact, dogfact, funfact, steam [profile], googledoodle, bored, search [query], randomcolor, randomword, country [name], time, newemote, ghiblifilms, ytthumbnail [link]'
discordAPI = 'lockdown [seconds], slowmode [seconds], ar [tag] [role], rr [tag] [role], clear [count/tag], kick [tag] [reason], ban [tag] [reason], nick [tag] [new nick], makechannel [type] [name], emojiinfo [emoji], permissions [user_tag], roleinfo [tag], id [tag], getinvite, botmembers, serverinfo, servericon, avatar [tag], userinfo [tag], roles, channels, serveremojis, reactmsg [text], reactnum [num1] [num2]'
apps = 'imdb, translate, wikipedia'
commandLength = [len(bothelp.split(',')), len(maths.split(',')), len(encoding.split(',')), len(games.split(',')), len(fun.split(',')), len(utilities.split(',')), len(discordAPI.split(',')), len(memes.split(',')), len(images.split(',')), len(apps.split(','))]
totalLength = 0
for i in range(0, len(commandLength)):
    totalLength += int(commandLength[i])

def bin(text):
    result = " ".join(f"{ord(i):08b}" for i in text) # THANKS STACK OVERFLOW! UWU
    return result.replace(' ', '')

def encodeb64(text):
    message_bytes = text.encode('ascii')
    base64_bytes = base64.b64encode(message_bytes)
    base64_message = base64_bytes.decode('ascii')
    return base64_message # yes. copy-pasted i know. #EPICDEVELOPER2020

ordertypes = [
    '**Bot help ('+str(commandLength[0])+')**\n```'+str(bothelp)+'```',
    '**Moderation ('+str(commandLength[6])+')**\n```'+str(discordAPI)+'```',
    '**Utilities ('+str(commandLength[5])+')**\n```'+str(utilities)+'```',
    '**Math ('+str(commandLength[1])+')**\n```'+str(maths)+'```',
    '**Fun ('+str(commandLength[4])+')**\n```'+str(fun)+'```',
    '**Games ('+str(commandLength[3])+')**\n```'+str(games)+'```',
    '**Encoding ('+str(commandLength[2])+')**\n```'+str(encoding)+'```',
    '**Memes ('+str(commandLength[7])+')**\n```'+str(memes)+'```',
    '**Images ('+str(commandLength[8])+')**\n```'+str(images)+'```',
    '**Apps ('+str(commandLength[9])+')**\n```'+str(apps)+'```'
]