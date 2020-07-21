import random

def checkEndGame(arr):
    if len(arr)<1: return True
    return False

def rps(given):
    # SHORT YANDEREDEV STYLE CODING
    emojiArray = ["fist", "hand_splayed", "v"]
    ran = random.randint(0, 2)
    if given==emojiArray[ran]: return [ran, 1]
    elif ran==0:
        if given.startswith('h'): return [ran, 0]
        elif given.startswith('v'): return [ran, 2]
    elif ran==1:
        if given.startswith('f'): return [ran, 2]
        elif given.startswith('v'): return [ran, 0]
    elif ran==2:
        if given.startswith('f'): return [ran, 0]
        elif given.startswith('h'): return [ran, 2]
def slot():
    fruits = ':green_apple:,:apple:,:pear:,:tangerine:,:lemon:,:banana:,:watermelon:,:grapes:,:strawberry:,:melon:,:cherries:,:peach:,:mango:,:pineapple:,:tomato:,:eggplant:,:flushed:'.split(',')
    return [random.choice(fruits), random.choice(fruits), random.choice(fruits)]

def slotify(slot):
    return ' | '.join(slot)[:-3]