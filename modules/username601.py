import random
import base64
import discord
import requests
from os import environ
from os.path import isfile
from subprocess import run, PIPE
from json import dumps
from urllib.request import urlopen as getapi
from urllib.parse import quote_plus as urlencode
from json import loads as jsonify
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

def randomtroll():
    return random.choice(loads(open(cfg('JSON_DIR')+'/troll.json', 'r').read()))
def randomhash():
    return ''.join([random.choice(list('ABCDEFHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789-_')) for i in range(random.randint(11, 26))])
def num2word(num):
    try: return 'zero,one,two,three,four,five,six,seven,eight,nine'.split(',')[num]
    except: return None

def emote(client, type):
    return str(client.get_emoji(cfg('EMOJI_'+type.upper(), integer=True)))

def inspect_image_url(url):
    try:
        hdrs = requests.get(url, timeout=3).headers
        assert hdrs['Content-Type'].startswith('image/')
        assert (int(hdrs['Content-Length'])/1024/1024) < 2
        return True
    except:
        return False

def get_embed_color():
    color = cfg('MAIN_COLOR').split(',')
    return discord.Colour.from_rgb(
        int(color[0]), int(color[1]), int(color[2])
    )

def parse_parameter(args, arg, get_second_element=False, singular=False):
    if arg.lower() in [i.lower() for i in list(args)]:
        parsed = tuple([i for i in list(args) if arg.lower() not in i.lower()])
        if get_second_element:
            index = [i.lower() for i in list(args)].index(arg.lower()) + 1
            if index >= len(list(args)):
                return {"available": False, "parsedarg": parsed, "secondparam": None}
            parsed = parsed[0:index]
            if not singular: return {"available": True, "parsedarg": parsed, "secondparam": ' '.join(list(args)[index:len(args)])}
            return {"available": True, "parsedarg": parsed, "secondparam": list(args)[index]}
        return {"available": True, "parsedarg": parsed, "secondparam": None}
    return {"available": False, "parsedarg": args, "secondparam": None}

def ping():
    url = cfg('HOST_URL')
    if url.lower()=='none': return None
    a = t.now().timestamp()
    requests.get(url)
    return round((t.now().timestamp()-a)*1000)

# if moment return moment
def getUserAvatar(ctx, args, size=1024, user=None, allowgif=False):
    if len(list(args))==0:
        if len(ctx.message.attachments) > 0:
            Vld = inspect_image_url(ctx.message.attachments[0].url)
            if Vld:
                return ctx.message.attachments[0].url
        if allowgif: return str(ctx.author.avatar_url_as(size=size))
        else: return str(ctx.author.avatar_url_as(format='png', size=size))
    elif len(list(args))==1 and (list(args)[0].startswith('http') or list(args)[0].startswith('<http')):
        if list(args)[0].startswith('<') and list(args)[0].endswith('>'):
            res = list(args)[0][:-1][1:]
            temp = list(args)
            temp[0] = res
            args = tuple(temp)
        if inspect_image_url(list(args)[0]):
            return list(args)[0]
    if len(ctx.message.mentions)>0:
        if not allowgif: return str(ctx.message.mentions[0].avatar_url_as(format='png', size=size))
        return str(ctx.message.mentions[0].avatar_url_as(size=size))
    name = str(' '.join(list(args))).lower().split('#')[0] # disable discriminator if found
    for i in ctx.guild.members:
        if name in str(i.name).lower():
            user = i; break
        elif name in str(i.nick).lower():
            user = i; break
    if user!=None:
        if not allowgif: return str(user.avatar_url_as(format='png', size=size))
        return str(user.avatar_url_as(size=size))
    elif list(args)[0].isnumeric():
        if int(list(args)[0]) not in [i.id for i in ctx.guild.members]: raise noUserFound()
        if not allowgif: return str(ctx.guild.get_member(int(list(args)[0])).avatar_url_as(format='png', size=size))
        return str(ctx.guild.get_member(int(list(args)[0])).avatar_url_as(size=size))
    if not allowgif: return str(ctx.author.avatar_url_as(format='png', size=size))
    return str(ctx.author.avatar_url_as(size=size))

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

def bin(text):
    result = " ".join(f"{ord(i):08b}" for i in text) # THANKS STACK OVERFLOW! UWU
    return result.replace(' ', '')

def encodeb64(text):
    message_bytes = text.encode('ascii')
    base64_bytes = base64.b64encode(message_bytes)
    base64_message = base64_bytes.decode('ascii')
    return base64_message # yes. copy-pasted i know. #EPICDEVELOPER2020