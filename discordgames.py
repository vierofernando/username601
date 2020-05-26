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