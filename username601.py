import random
import base64
# import platform as systema
from urllib.request import urlopen as getapi
from urllib.parse import quote_plus as urlencode
from json import loads as jsonify
from requests import get as decodeurl
prefix = '1'
cmdtypes = ['Bot Help', 'Moderation', 'Utilities', 'Math', 'Fun', 'Games', 'Encoding', 'Memes', 'Images', 'Apps', 'Owner']
bot_ver = '1.9.7c'
bot_changelog = 'Optimized help command, Meme command is now filtered, Bot code formatted.'

class BotEmotes:
    loading = 704242088425816085
    error = 711736311215554560
    success = 704242067097911307

def limit(word):
    total = ''
    for i in range(0, len(word)):
        if i>1990:
            break
        total += list(word)[i]
    return total
def urlify(word):
    return urlencode(word).replace('+', '%20')

def findNum(word, arr):
    for i in range(0, len(arr)):
        if arr[i]==word:
            return i
            break

def hackfind(data, avatar):
    if data.startswith('1'):
        return 'https://i.imgur.com/msmvE09.gif'
    elif data.startswith('2'):
        return avatar
    elif data.startswith('3'):
        return 'https://seeklogo.com/images/F/FBI_SHIELD-logo-2D02BDDAC8-seeklogo.com.png'
    elif data.startswith('4'):
        return 'https://images-ext-1.discordapp.net/external/ByHvJcnlhVe42B9bjwf9umFHeEA5pk1oebLdxeWYY0g/%3Fv%3D1/https/cdn.discordapp.com/emojis/704242063725559868.png'
    else:
        return 'https://upload.wikimedia.org/wikipedia/commons/5/50/Black_colour.jpg'

def arrspace(arr):
    res = ''
    for i in range(0, len(arr)):
        if i==len(arr)-1:
            res += arr[i]
        else:
            res += arr[i] + ' '
    return res

def jsonisp(url):
    return decodeurl(url).json()
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

#def platform():
#    return f'**Operating System:** {systema.system()} {systema.version()}\n**Processor: **{systema.processor()}\n**Python Compiler: **{systema.python_compiler()}'

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

def dearray(arr):
    res = ''
    for i in range(0, len(arr)):
        if i!=len(arr)-1:
            res += str(arr[i]) + ', '
        else:
            res += str(arr[i]) + '.'
    return res

def tohex(integer):
    return str(hex(integer)).upper()[2:]

def toint(hex):
    return int(hex, 16)

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
	        "name":"index.html",
            "type":"main website file. (homepage)"
        },
	    {
	        "name":"commands.html",
            "type":"main website file (commands page)"
	    },
        {
            "name":"thanks.html",
            "name":"website for thanking strangers"
        },
	    {
	        "name":"commands.json",
            "type":"all of the commands as a json file."
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

def bin(text):
    result = " ".join(f"{ord(i):08b}" for i in text) # THANKS STACK OVERFLOW! UWU
    return result.replace(' ', '')

def encodeb64(text):
    message_bytes = text.encode('ascii')
    base64_bytes = base64.b64encode(message_bytes)
    base64_message = base64_bytes.decode('ascii')
    return base64_message # yes. copy-pasted i know. #EPICDEVELOPER2020
