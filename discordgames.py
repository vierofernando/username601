def checkEndGame(arr):
    if len(arr)<1:
        return True
    else:
        return False
def checkWinner(arr, usersym, botsym, typeC): #CHECKS WINNER IN TIC TAC TOE GAME. I KNOW THERE ARE A LOT OF COPY AND PASTES
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
        missing = ''
        temp = ''
        for each in winConditions[i]:
            if arr[int(each)]==botsym:
                temp = str(temp) + botsym
            elif arr[int(each)]==usersym:
                temp = str(temp) + usersym
            else:
                missing = arr[int(each)]
        if typeC=='checkwin':
            if str(temp)==threeWinsUser:
                return 'userwin'
                break
            elif str(temp)==threeWinsBot:
                return 'botwin'
                break
        elif typeC=='impos':
            if temp==str(usersym)*2:
                return missing