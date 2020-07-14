import random
import base64
from subprocess import run, PIPE

from urllib.request import urlopen as getapi
from urllib.parse import quote_plus as urlencode
from json import loads as jsonify
from requests import get as decodeurl

class BotEmotes:
    loading = 704242088425816085
    error = 704242063725559868
    success = 704264842709565490

class Config:
    id = 696973408000409626 # BOT ID
    prefix = '1' # your prefix here
    cmdtypes = decodeurl("https://vierofernando.github.io/username601/assets/json/categories.json").json()
    class Version:
        number = '2.1'
        changelog = 'Added MORE meme commands, removed the 1d alias.'
    class SupportServer:
        id = 688373853889495044 # support server ID
        logging = 694521383908016188 # logging channel ID in support server
        Announcements = 722752725267382323 # announcements channel
        feedback = 706459051034279956 # feedback channel
        invite = 'https://discord.gg/HhAPkD8' # your support server invite link
    class owner:
        id = 661200758510977084 # YOUR USER ID
        name = 'Viero Fernando'
prefix = Config.prefix

def getStatus():
    return jsonify(open("/app/assets/json/status.json", "r").read())

def accept_message(authorid, authorbot, message, guild): # ACCEPT THE SPECIFIC REQUIREMENTS
    yes = ''
    if authorid!=Config.id: yes += 'v'
    if not authorbot: yes += 'v'
    if message.startswith(Config.prefix): yes += 'v'
    if len(message)>1: yes += 'v'
    if '<@'+str(Config.id)+'>' not in message: yes += 'v'
    if '<@!'+str(Config.id)+'>' not in message: yes += 'v'
    if guild!=None: yes += 'v'
    if yes=='vvvvvvv':
        return True
    else:
        return False

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

def report(auth):
    # NEVER GONNA GIVE YOU UP, NEVER GONNA LET YOU DOWN...
    return 'lol'

def check_if_owner(ctx):
    return ctx.message.channel.id == Config.owner.id

def time_encode(sec):
    time_type = 'seconds'
    newsec = int(sec)
    # YANDEREDEV.EXE
    if sec>60:
        newsec, time_type = round(sec/60), 'minutes'
        if sec>3600: 
            newsec, time_type = round(sec/3600), 'hours'
            if sec>86400:
                newsec, time_type = round(sec/86400), 'days'
                if sec>2592000:
                    newsec, time_type = round(sec/2592000), 'months'
                    if sec>31536000:
                        newsec, time_type = round(sec/31536000), 'years'
    return str(str(newsec)+' '+time_type)

def terminal(command):
    try:
        data = run([command.split(' ')[0], str(' '.join(command.split(' ')[1:len(command.split(' '))]))], stdout=PIPE).stdout.decode('utf-8')
    except IndexError:
        data = run([command], stdout=PIPE).stdout.decode('utf-8')
    return data

def jsonisp(url):
    return decodeurl(url).json()
def api(url):
    return jsonify(getapi(url).read())

def insp(url):
    return decodeurl(url).text

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

def bin(text):
    result = " ".join(f"{ord(i):08b}" for i in text) # THANKS STACK OVERFLOW! UWU
    return result.replace(' ', '')

def encodeb64(text):
    message_bytes = text.encode('ascii')
    base64_bytes = base64.b64encode(message_bytes)
    base64_message = base64_bytes.decode('ascii')
    return base64_message # yes. copy-pasted i know. #EPICDEVELOPER2020

def cmd(message, name):
    if message.startswith(prefix+name):
        return True
    else:
        return False
