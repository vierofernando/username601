from random import choice, randint
import json

def getfish():
    res, found, ctx = json.loads(open('/home/runner/hosting601/assets/json/fish.json', 'r').read()), False, None
    for i in res['results']['overall']:
        if randint(1, i['chance'])==1:
            found, ctx = True, i
            break
    if not found: ctx = choice(res['results']['else'])
    return {
        "catched": found,
        "ctx": ctx
    }

def gay_finder(user_id):
    user_id = str(user_id)
    f = int(list(user_id)[0])
    s = int(list(user_id)[len(user_id)-1])
    return user_id[f]+user_id[s]

def love_finder(a, b):
    c = a - b
    if c < 0: c = b - a
    data = str(list(str(c))[int(list(str(c))[0])])+str(list(str(c))[len(list(str(c)))-1])
    return int(data)