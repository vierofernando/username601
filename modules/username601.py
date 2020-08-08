import random
import base64
from os import getenv
from subprocess import run, PIPE
from json import dumps
from urllib.request import urlopen as getapi
from urllib.parse import quote_plus as urlencode
from json import loads as jsonify
from requests import request
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
        number = '2.5'
        changelog = 'Implemented server shops! (local)'
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

def limitto(text, limitcount):
    a = text
    if len(a) < limitcount: return text
    while (len(a) > limitcount):
        temp = list(a)
        temp.pop()
        a = ''.join(temp)
    return a

def html2discord(text):
    res = text.replace('<p>', '').replace('</p>', '').replace('<b>', '**').replace('</b>', '**').replace('<i>', '*').replace('</i>', '*').replace('<br />', '\n')
    return res

def uptimerobot():
    payload = 'api_key={}&format=json&logs=1'.format(getenv('UPTIMEROBOT_TOKEN'))
    headers = {
        'content-type':         "application/x-www-form-urlencoded",
        'cache-control': "no-cache"
    }
    data = request("POST",  'https://api.uptimerobot.com/v2/getMonitors', data=payload, headers=headers).json()
    data = data['monitors'][0]['logs'][0:25][::-1]
    parameter = "{type:'line',data:{labels:"+str([str(i['datetime']) for i in data])+", datasets:[{label:'Username601 Latency (ms)', data: "+str([i['duration'] for i in data])+", fill:false,borderColor:'blue'}]}}"
    return parameter

def getStatus():
    return jsonify(open("/home/runner/hosting601/assets/json/status.json", "r").read())

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
    links = [
        'https://i.imgur.com/msmvE09.gif',
        avatar,
        'https://seeklogo.com/images/F/FBI_SHIELD-logo-2D02BDDAC8-seeklogo.com.png',
        'https://images-ext-1.discordapp.net/external/ByHvJcnlhVe42B9bjwf9umFHeEA5pk1oebLdxeWYY0g/%3Fv'
    ]
    if int(list(data)[0]) not in range(1, 5):
        return 'https://upload.wikimedia.org/wikipedia/commons/5/50/Black_colour.jpg'
    else:
        return links[int(list(data)[0])+1]

def arrspace(arr):
    return str(' '.join(arr))[:-1]

def report(auth):
    # NEVER GONNA GIVE YOU UP, NEVER GONNA LET YOU DOWN...
    return 'lol'

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

def caesar(text, num):
    temp = text.lower()
    if num>26:
        while num>26:
            num -= 26
    elif num<0:
        while num<0:
            num += 26
    alph, result = list('abcdefghijklmnopqrstuvwxyz'), ''
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
    alph = list(word.lower())
    for i in range(0, len(arr)):
        if arr[i] not in alph:
            alph.append(arr[i])
    temp, removed, amount = list(word), [], random.randint(1, len(alph)-1)
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
    return str(', '.join(arr))+'.'

def tohex(integer):
    return str(hex(int(integer))).upper()[2:]

def toint(hex):
    return int(hex, 16)

def convertrgb(hexCode, typ):
    uselessArray = list(str(hexCode))
    part1, part2, part3 = ''.join(uselessArray[0:1]), ''.join(uselessArray[2:3]), ''.join(uselessArray[4:5])
    partsArray, rgb, percentageRgb = [part1, part2, part3], [], []
    for i in range(0, 3):
        toConvert = partsArray[i]
        stackOverFlow = int(toConvert, 16)
        rgb.append(stackOverFlow)
        percentageRgbAdd = int(rgb[i])/255*100
        percentageRgb.append(round(percentageRgbAdd))
    if typ=='0':
        return rgb
    return percentageRgb

def bin(text):
    result = " ".join(f"{ord(i):08b}" for i in text) # THANKS STACK OVERFLOW! UWU
    return result.replace(' ', '')

def encodeb64(text):
    message_bytes = text.encode('ascii')
    base64_bytes = base64.b64encode(message_bytes)
    base64_message = base64_bytes.decode('ascii')
    return base64_message # yes. copy-pasted i know. #EPICDEVELOPER2020