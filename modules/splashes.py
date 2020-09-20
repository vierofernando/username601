import random
import requests
from sys import path
try: from modules.username601 import *
except: from .username601 import *
path.append(cfg('JSON_DIR'))
from json import loads
def randomtroll():
    return random.choice(loads(open(cfg('JSON_DIR')+'/troll.json', 'r').read()))
def randomhash():
    hashh = ''
    for i in range(0, random.randint(13, 21)):
        hashh = hashh + random.choice(list('ABCDEFHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789-_'))
    return hashh
def num2word(num):
    arr, word = list(range(0, 10)), 'zero,one,two,three,four,five,six,seven,eight,nine'.split(',')
    for i in range(0, len(arr)):
        if num==arr[i]:
            return word[i]
def getSecrets():
    arr = [
        ' is sleeping.',
        ' is breathing.',
        ' is about to ||do something.||',
        ' likes you.',
        ' hates you.',
        ' wanted to confess something.', 
        ' is the guy behind HowToBasic.',
        ' is the person secretly running the USA government.',
        ' is jeff the killer.',
        ' is the guy behind the development of Username601.',
        ' is hacking the server.',
        ' is hacking discord.',
        ' likes sh||oo||ting people.',
        ' likes p||hoto||graphy.',
        ' likes going to ||git||hub.com to have some fun.',
        ' is cool.',
        ' is smart af.',
        ' is the guy behind you.',
        ' is a nerd.',
        ' likes schools.',
        ' is the guy spying behind you.',
        ' has a secret youtube channel.',
        ' is a cool programmer.',
        ' is a nice guy, not worth telling secrets tho!',
        ' is a discord user :v',
        ' is breathing.',
        ' umm... maybe i shouldn\'t tell his secrets.',
        ' is secretly a bot. yes, selfbot.',
        ' is... umm.. :flushed:',
        ' is the hacker that will RULE the world.'
    ]
    return arr