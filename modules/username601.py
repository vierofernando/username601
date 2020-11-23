import aiohttp
from emoji import UNICODE_EMOJI
from random import choice
from discord import Color, Embed
from discord.message import Message
from os import environ
from requests import get
from base64 import b64encode
from subprocess import run, PIPE
from datetime import datetime as t
from urllib.parse import quote_plus
from configparser import ConfigParser
class send_error_message(Exception): pass

emoji_unicodes = UNICODE_EMOJI.keys()
main_cfg = ConfigParser()
main_cfg.read('config.ini')
class emojiutils:
    def __init__(self):
        pass

def import_emoji_function(func):
    setattr(emojiutils, "emoji_to_url", func)

async def wait_for_message(ctx, message, func=None, timeout=5.0, *args, **kwargs):
    if message is not None: await ctx.send(message)
    def wait_check(m): return ((m.author == ctx.author) and (m.channel == ctx.channel))
    _function = wait_check if (func is None) else func
    try:
        message = await ctx.bot.wait_for("message", check=_function, timeout=timeout)
    except:
        message = None
    finally:
        return message

def query(arr, item):
    a = item.lower()
    res = [i for i in arr if a in str(i).lower()]
    return (None if (len(res) == 0) else res[0])

def config(param, integer=False):
    if integer: return int(main_cfg.get('bot', param.lower()))
    return main_cfg.get('bot', param.lower())

def inspect_image_url(url):
    try:
        hdrs = get(url, timeout=3).headers
        assert hdrs['Content-Type'].startswith('image/')
        assert (int(hdrs['Content-Length'])/1024/1024) < 2
        return True
    except:
        return False

def split_parameter_to_two(args):
    if ((args is None) or (len(args) < 2)): raise send_error_message("Please input at least 1 - 2 inputs!")
    available_split_chars = ';?, ?,?|? | '.split('?')
    if len(args) == 2: return args[0], args[1]
    args_as_a_string = ' '.join(list(args))
    for char in available_split_chars:
        if char in args_as_a_string: return args_as_a_string.split(char)[0], char.join(args_as_a_string.split(char)[1:])
    return args[0], ' '.join(args[1:])

def parse_parameter(args, arg, get_second_element=False, singular=False):
    if arg.lower() in list(map(lambda x: x.lower(), args)):
        parsed = tuple([i for i in list(args) if arg.lower() not in i.lower()])
        if get_second_element:
            index = [i.lower() for i in list(args)].index(arg.lower()) + 1
            if index >= len(args):
                return {"available": False, "parsedarg": args, "secondparam": None}
            parsed = parsed[0:index]
            if not singular: return {"available": True, "parsedarg": parsed, "secondparam": ' '.join(args[index:])}
            return {"available": True, "parsedarg": parsed, "secondparam": list(args)[index]}
        return {"available": True, "parsedarg": parsed, "secondparam": None}
    return {"available": False, "parsedarg": args, "secondparam": None}

def clean_html(text):
    res = text.replace('<p>', '').replace('</p>', '').replace('<b>', '**').replace('</b>', '**').replace('<i>', '*').replace('</i>', '*').replace('<br />', '\n')
    return res

def encode_uri(word):
    return quote_plus(word).replace('+', '%20')

def lapsed_time_from_seconds(sec):
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

def run_terminal(command):
    data = run(command.split(), stdout=PIPE).stdout.decode('utf-8')
    return data

def fetchJSON(url, alexflipnote=False):
    res = get(url, headers={'Authorization': environ['ALEXFLIPNOTE_TOKEN']}).json() if alexflipnote else get(url).json()
    return res

def inspect_element(url): return get(url).text

def atbash(text):
    alphabet = list('abcdefghijklmnopqrstuvwxyz')
    reversed_alphabet, res = alphabet[::-1], ''
    for i in text.lower():
        try: res += reversed_alphabet[alphabet.index(i)]
        except ValueError: res += i
    return res

def caesar(text, offset):
    if offset>26:
        while offset>26:
            offset -= 26
    elif offset<0:
        while offset<0:
            offset += 26
    alphabet, res = list('abcdefghijklmnopqrstuvwxyz'), ''
    for i in text.lower():
        try: res += alphabet[alphabet.index(i) + offset]
        except ValueError: res += i
    return res

def binary_from(text):
    return ''.join(map(lambda x: f"{ord(x):08b}", text))

def base64_from(text):
    return b64encode(text.encode('ascii')).decode('ascii')