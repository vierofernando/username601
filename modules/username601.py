import random
import base64
from os import environ
from os.path import isfile
from subprocess import run, PIPE
from json import dumps
from urllib.request import urlopen as getapi
from urllib.parse import quote_plus as urlencode
from json import loads as jsonify
import requests
from configparser import ConfigParser
from datetime import datetime as t
class noArguments(Exception): pass
class noUserFound(Exception): pass
class noProfile(Exception): pass

main_cfg = ConfigParser()
if isfile('config.ini'): main_cfg.read('config.ini')
else: main_cfg.read('../config.ini')

def cfg(param, integer=False):
    if integer: return int(main_cfg.get('bot', param.lower()))
    return main_cfg.get('bot', param.lower())
prefix = cfg('PREFIX')

def emote(client, type):
    return str(client.get_emoji(cfg('EMOJI_'+type.upper(), integer=True)))

def get_embed_color(discord):
    color = cfg('MAIN_COLOR').split(',')
    return discord.Colour.from_rgb(
        int(color[0]), int(color[1]), int(color[2])
    )

def getCommandLength():
    data, count = requests.get(cfg('WEBSITE_MAIN')+'/assets/json/commands.json').json(), 0
    for i in range(len(data)):
        count += len(data[i][list(data[i].keys())[0]])
    return count

def ping():
    url = cfg('HOST_URL')
    if url.lower()=='none': return None
    a = t.now().timestamp()
    requests.get(url)
    return round((t.now().timestamp()-a)*1000)

def getUserAvatar(ctx, args, size=1024, user=None, allowgif=False):
    if len(list(args))==0:
        if len(ctx.message.attachments) > 0:
            if ctx.message.attachments[0].filename.split('.')[::-1][0].lower() in ['webp', 'png', 'jpg', 'jpeg']:
                return ctx.message.attachments[0].url
        if allowgif: return str(ctx.author.avatar_url).replace('.webp?size=1024', '.png?size'+str(size))
        else: return str(ctx.author.avatar_url).replace('.gif', '.webp').replace('.webp?size=1024', '.png?size'+str(size))
    elif len(list(args))==1 and list(args)[0].startswith('http'):
        if list(args)[0].startswith('<') and list(args)[0].endswith('>'):
            res = list(args)[0][:-1][1:]
            temp = list(args)
            temp[0] = res
            args = tuple(temp)
        if list(args)[0].split('.')[::-1][0].lower() in ['png', 'webp', 'jpg', 'jpeg']:
            return list(args)[0]
    if len(ctx.message.mentions)>0:
        if not allowgif: return str(ctx.message.mentions[0].avatar_url).replace('.gif', '.webp').replace('.webp?size=1024', f'.png?size={size}')
        return str(ctx.message.mentions[0].avatar_url).replace('?size=1024', f'?size={size}')
    name = str(' '.join(list(args))).lower().split('#')[0] # disable discriminator if found
    for i in ctx.guild.members:
        if name in str(i.name).lower():
            user = i; break
        elif name in str(i.nick).lower():
            user = i; break
    if user!=None:
        if not allowgif: return str(user.avatar_url).replace('.gif', '.webp').replace('.webp?size=1024', f'.png?size={size}')
        return str(user.avatar_url).replace('?size=1024', f'?size={size}')
    elif list(args)[0].isnumeric():
        if int(list(args)[0]) not in [i.id for i in ctx.guild.members]: raise noUserFound()
        if not allowgif: return str(ctx.guild.get_member(int(list(args)[0])).avatar_url).replace('.gif', '.webp').replace('.webp?size=1024', f'.png?size={size}')
        return str(ctx.guild.get_member(int(list(args)[0])).avatar_url).replace('?size=1024', f'?size={size}')
    if not allowgif: return str(ctx.author.avatar_url).replace('.gif', '.webp').replace('.webp?size=1024', f'.png?size={size}')
    return str(ctx.author.avatar_url).replace('?size=1024', f'?size={size}')

def getUser(ctx, args, user=None, allownoargs=True):
    if len(list(args))==0:
        if not allownoargs: raise noArguments()
        return ctx.author
    if len(ctx.message.mentions)>0: return ctx.message.mentions[0]
    name = str(' '.join(list(args))).lower().split('#')[0] # disable discriminator if found
    for i in ctx.guild.members:
        if name in str(i.name).lower():
            user = i; break
        elif name in str(i.nick).lower():
            user = i; break
    if user!=None: return user
    if list(args)[0].isnumeric():
        if int(list(args)[0]) not in [i.id for i in ctx.guild.members]: raise noUserFound()
        return ctx.guild.get_member(int(list(args)[0]))
    return ctx.author

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

def urlify(word):
    return urlencode(word).replace('+', '%20')

def time_encode(sec):
    time_type, newsec = 'seconds', int(sec)
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
    if str(newsec) == '1': return str(str(newsec)+' '+time_type[:-1])
    return str(str(newsec)+' '+time_type)

def terminal(command):
    try:
        data = run([command.split(' ')[0], str(' '.join(command.split(' ')[1:len(command.split(' '))]))], stdout=PIPE).stdout.decode('utf-8')
    except IndexError:
        data = run([command], stdout=PIPE).stdout.decode('utf-8')
    return data

def fetchJSON(url): return requests.get(url).json()
def insp(url): return requests.get(url).text

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
