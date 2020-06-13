import random

def checkEndGame(arr):
    if len(arr)<1:
        return True
    else:
        return False
def checkWinner(arr, usersym, botsym): #CHECKS WINNER IN TIC TAC TOE GAME. I KNOW THERE ARE A LOT OF COPY AND PASTES
    winConditions = [
        list('012'),
        list('345'),
        list('678'),
        list('048'),
        list('246'),
        list('036'),
        list('147'),
        list('258')
    ]
    threeWinsUser = str(usersym)*3
    threeWinsBot = str(botsym)*3
    for i in range(0, len(winConditions)):
        temp = ''
        for each in winConditions[i]:
            if arr[int(each)]==botsym:
                temp = str(temp) + botsym
            elif arr[int(each)]==usersym:
                temp = str(temp) + usersym
        if str(temp)==threeWinsUser:
            return 'userwin'
            break
        elif str(temp)==threeWinsBot:
            return 'botwin'
            break
def rps(given):
    #THESE ARE PRIMITIVE CODE LEL
    emojiArray = ["fist", "hand_splayed", "v"]
    ran = random.randint(0, 2)
    if ran==0:
        if given=="fist":
            msgId = 1
        elif given=="hand_splayed":
            msgId = 0
        elif given=="v":
            msgId = 2
    elif ran==1:
        if given=="fist":
            msgId = 2
        elif given=="hand_splayed":
            msgId = 1
        elif given=="v":
            msgId = 0
    elif ran==2:
        if given=="fist":
            msgId = 0
        elif given=="hand_splayed":
            msgId = 2
        elif given=="v":
            msgId = 1
    return [msgId, ran]
def slot():
    fruits = [
        ':green_apple:',
        ':apple:',
        ':pear:',
        ':tangerine:',
        ':lemon:',
        ':banana:',
        ':watermelon:',
        ':grapes:',
        ':strawberry:',
        ':melon:',
        ':cherries:',
        ':peach:',
        ':mango:',
        ':pineapple:',
        ':tomato:',
        ':eggplant:',
        ':flushed:'
    ]
    result = [random.choice(fruits), random.choice(fruits), random.choice(fruits)]
    return result
def slotify(slot):
    res = ''
    for i in range(0, len(slot)):
        if i==len(slot)-1:
            res += slot[i]
        else:
            res += slot[i]+' | '
    return res
