import random

def checkEndGame(arr):
    if len(arr)<1: return True
    return False

def rps(given):
    # SHORT YANDEREDEV STYLE CODING
    emojiArray = ["fist", "hand_splayed", "v"]
    ran = random.randint(0, 2)
    if given==emojiArray[ran]: return [1, ran]
    elif ran==0:
        if given.startswith('h'): return [0, ran]
        elif given.startswith('v'): return [2, ran]
    elif ran==1:
        if given.startswith('f'): return [2, ran]
        elif given.startswith('v'): return [0, ran]
    elif ran==2:
        if given.startswith('f'): return [0, ran]
        elif given.startswith('h'): return [2, ran]
def slot():
    fruits = ':green_apple:,:apple:,:pear:,:tangerine:,:lemon:,:banana:,:watermelon:,:grapes:,:strawberry:,:melon:,:cherries:,:peach:,:mango:,:pineapple:,:tomato:,:eggplant:,:flushed:'.split(',')
    return [random.choice(fruits), random.choice(fruits), random.choice(fruits)]

def slotify(slot):
    return str(' | '.join(slot))[:-3]