import random
import requests
def randomhash():
    hashh = ''
    for i in range(0, random.randint(13, 21)):
        hashh = hashh + random.choice(list('ABCDEFHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789-_'))
    return hashh
def num2word(num):
    arr, word = list(range(0, 10)), 'zero,one,two,three,four,five,six,seven,eight,nine'.split(',')
    for i in range(0, len(arr)):
        if num==arr[i]:
            return word[i] ; break
def getGeoQuiz():
    return ['capital', 'region', 'subregion', 'population', 'demonym', 'nativeName']
def lastmsg(a):
    arr = [
        'join plspls discord.gg/'+a,
        'I love my life',
        'bruh',
        'mama mia',
        'Username601 sucks',
        'OwO',
        'What is obama\'s last name pls',
        'Hey i am gay',
        'yee',
        'can you send me that nsfw clip thx',
        'eewww :o',
        'subscribe to pewdiepie'
    ]
    return random.choice(arr)
def email(a):
    arr = [
        a+'iscool',
        a+'playsminecraft',
        'theoneandonly'+a,
        'nonhackablegmailaccount',
        'epicgmaillink',
        a+'isthebest',
        a+'OwO',
        'mister'+a,
        a+'playsfortnite',
        a+'votedusername601',
        a+'601'
    ]
    return random.choice(arr)
def slap(typ):
    gifArr = ["https://tenor.com/vEDn.gif ", "https://tenor.com/QZpI.gif", "https://tenor.com/6i12.gif", "https://tenor.com/RTqL.gif", "https://tenor.com/rhrz.gif", "https://giphy.com/gifs/mary-steenburgen-vxvNnIYFcYqEE", "https://giphy.com/gifs/sweet-penguin-penguins-mEtSQlxqBtWWA", "https://giphy.com/gifs/sherlock-snape-gif-kTBjwh6IWbLPy", "https://giphy.com/gifs/slap-dog-slapping-lX03hULhgCYQ8", "https://tenor.com/QklT.gif", "https://tenor.com/1jyY.gif", "https://tenor.com/6zwG.gif"]
    msgArr = ["Slapped in the face!", "Lemme slap your face for a bit.", "Come here... **SLAP!**", "One slap for you,", "May i slap you?", "SLAP TIME!", "Press F, cuz we just slapped", "GIMME YOUR SLAPPABLE FACE,", "What time is it? **SLAP TIME!**"]
    if typ=='msg':
        return random.choice(msgArr)
    else: 
        return random.choice(gifArr)

def hbd():
    gifArr = ["https://tenor.com/bcdeQ.gif", "https://tenor.com/4flE.gif", "https://tenor.com/3toj.gif", "https://tenor.com/SZbC.gif", "https://tenor.com/1C6f.gif", "https://tenor.com/rzE6.gif", "https://tenor.com/beutC.gif", "https://tenor.com/z9js.gif", "https://tenor.com/v353.gif", "https://tenor.com/wFWQ.gif", "https://tenor.com/OmS5.gif", "https://tenor.com/6BKT.gif", "https://tenor.com/scB9.gif", "https://tenor.com/bc2rQ.gif", "https://tenor.com/paQT.gif", "https://tenor.com/1C6f.gif", "https://tenor.com/GYmM.gif"]
    return random.choice(gifArr)

def password(a):
    arr = [
        a+'iscool',
        a+'123456',
        'Xx_'+a+'_xX',
        'fornitegamer123',
        'thereal'+a,
        'theultimate'+a,
        'ultimate'+a,
        'mega'+a,
        '123'+a+'123',
        'PASSWORD',
        'QWERTY',
        '000000',
        '111111',
        'uwuyoucanthackme',
        'Edmund1978',
        '12345',
        'PASS123',
        'LETMEIN',
        'XXXcoolpasswordXXX',
        'XXX'+a+'XXX',
        'DankMemerFan42069',
        'Swag69',
        'UWU69',
        '601SUCKS',
        'epicgamer123'
    ]
    return random.choice(arr)
def getHackFlow(tohack):
    flow = [
        '0hack.exe -u '+str(tohack.name)+' -a',
        '0\n[hack.exe] Opening hack prompt...',
        '0\n[hack.exe] Opening http://discord.com/hack/'+randomhash(),
        '1\n[hack.exe] USER DETECTED: '+tohack.name+'. HACKING USER... ',
        '1done',
        '1\n[hack.exe] RETRIEVING IP ADDRESS... ',
        '1done. IP: 99.238.'+str(tohack.discriminator)+'.1729.10',
        '1\n[hack.exe] ACCESSING DEVICE FROM DISCORD... ',
        '1done.',
        '1\n[DEVICE ID:'+str(tohack.discriminator)+'] ACCESS GRANTED',
        '1\n[hack.exe] GETTING FACECAM...',
        '2success.',
        '2\n[hack.exe] SPREADING FACECAM TO DARK WEB...',
        '2done.',
        '1\n[hack.exe] GETTING EMAIL INFO...',
        '1done.',
        '4\nEMAIL: '+email(tohack.name)+'@hacked.com\nPASSWORD: "'+password(tohack.name)+'"',
        '1\n[hack.exe] SPREADING INFO TO '+randomhash()+'.onion...',
        '1done.',
        '1\n[hack.exe] GETTING SENSITIVE PERSONAL INFORMATION...',
        '4done.\nLAST MESSAGE: "'+lastmsg(tohack.name)+'"\nLAST BROWSING HISTORY: "'+history(tohack.name)+'"\n[hack.exe] DISTRIBUTING INFO TO FBI AND NSA...',
        '3done.',
        '0\n[hack.exe] HACK COMPLETE.',
        '0\n\nC:\\Users\\Anonymous601>'
    ] # basically every batch file a scammer would use
    return flow
def gifslap():
    gifArr = ["https://tenor.com/vEDn.gif ", "https://tenor.com/QZpI.gif", "https://tenor.com/6i12.gif", "https://tenor.com/RTqL.gif", "https://tenor.com/rhrz.gif", "https://giphy.com/gifs/mary-steenburgen-vxvNnIYFcYqEE", "https://giphy.com/gifs/sweet-penguin-penguins-mEtSQlxqBtWWA", "https://giphy.com/gifs/sherlock-snape-gif-kTBjwh6IWbLPy", "https://giphy.com/gifs/slap-dog-slapping-lX03hULhgCYQ8", "https://tenor.com/QklT.gif", "https://tenor.com/1jyY.gif", "https://tenor.com/6zwG.gif"]
    return random.choice(gifArr)

def gifhbd():
    gifArr = ["https://tenor.com/bcdeQ.gif", "https://tenor.com/4flE.gif", "https://tenor.com/3toj.gif", "https://tenor.com/SZbC.gif", "https://tenor.com/1C6f.gif", "https://tenor.com/rzE6.gif", "https://tenor.com/beutC.gif", "https://tenor.com/z9js.gif", "https://tenor.com/v353.gif", "https://tenor.com/wFWQ.gif", "https://tenor.com/OmS5.gif", "https://tenor.com/6BKT.gif", "https://tenor.com/scB9.gif", "https://tenor.com/bc2rQ.gif", "https://tenor.com/paQT.gif", "https://tenor.com/1C6f.gif", "https://tenor.com/GYmM.gif"]
    return random.choice(gifArr)

def slapsay():
    arr = ["Slapped in the face!", "Lemme slap your face for a bit.", "Come here... **SLAP!**", "One slap for you,", "May i slap you?", "SLAP TIME!", "Press F, cuz we just slapped", "GIMME YOUR SLAPPABLE FACE,", "What time is it? **SLAP TIME!**"]
    return random.choice(arr)
def blyat():
    gifs = [
        'https://tenor.com/vLye.gif',
        'https://tenor.com/W2do.gif',
        'https://tenor.com/bgUeB.gif',
        'https://tenor.com/bf7w3.gif',
        'https://tenor.com/bf7w3.gif',
        'https://giphy.com/gifs/the-beatles-back-in-ussr-U50YFkQ3Utv5fsnuwu',
        'https://giphy.com/gifs/cbs-tv-dan-rather-CBd2RJor59e6I'
    ]
    return random.choice(gifs)
def history(a):
    arr = [
        'How to create a bot like Username601 no coding free',
        'How to bypass a block by the government',
        'How to delete browsing history from my parents',
        'How to get more people on my server',
        'how to make my server get 1000 members in 1 minute',
        'How to get animated server icon FOR FREE NO NITRO',
        'VPN FREE NO HACK VIRUS',
        'www.'+a+'.com',
        'How to bypass a ban in discord',
        'Why do people ban me i am just a 12 year old',
        'How to access discord when you are under 13',
        'discord.gg/'+a,
        'MINECRAFT LATEST VERSION DOWNLOAD FREE CRACK NO HACK NO ROOT',
        'How to hack discord',
        'Xxx_EpicGamer_xxX let\'s plays',
        'How to breathe',
        'What is the meaning of life',
        'What is the result of 1/0'
        'OwO bot cheat tutorial',
        'How to cheat in Pokecord. FREE CREDITS NO HACK',
        'FREE NITRO NO HACK LEGIT 2020',
        'How to boost my server for free no hack legit crack',
        'HOW TO GET MORE MEMBERS ON MY SERVER PLSS I AM DESPERATE',
        'Why do people keep leaving my discord server',
        'How to become a bot in discord',
        'Free vbucks no hacks'
    ]
    return random.choice(arr)
def hackflow(tohack):
    flow = [
        '0hack.exe -u '+str(tohack.name)+' -a',
        '0\n[hack.exe] Opening hack prompt...',
        '0\n[hack.exe] Opening http://discord.com/hack/'+randomhash(),
        '1\n[hack.exe] USER DETECTED: '+tohack.name+'. HACKING USER... ',
        '1done',
        '1\n[hack.exe] RETRIEVING IP ADDRESS... ',
        '1done. IP: 99.238.'+str(tohack.discriminator)+'.1729.10',
        '1\n[hack.exe] ACCESSING DEVICE FROM DISCORD... ',
        '1done.',
        '1\n[DEVICE ID:'+str(tohack.discriminator)+'] ACCESS GRANTED',
        '1\n[hack.exe] GETTING FACECAM...',
        '2success.',
        '2\n[hack.exe] SPREADING FACECAM TO DARK WEB...',
        '2done.',
        '1\n[hack.exe] GETTING EMAIL INFO...',
        '1done.',
        '4\nEMAIL: '+email(tohack.name)+'@hacked.com\nPASSWORD: "'+password(tohack.name)+'"',
        '1\n[hack.exe] SPREADING INFO TO '+randomhash()+'.onion...',
        '1done.',
        '1\n[hack.exe] GETTING SENSITIVE PERSONAL INFORMATION...',
        '4done.\nLAST MESSAGE: "'+lastmsg(tohack.name)+'"\nLAST BROWSING HISTORY: "'+history(tohack.name)+'"\n[hack.exe] DISTRIBUTING INFO TO FBI AND NSA...',
        '3done.',
        '0\n[hack.exe] HACK COMPLETE.',
        '0\n\nC:\\Users\\Anonymous601>'
    ]
    return flow
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
def getAsciiFonts():
    arr_raw = requests.get("http://artii.herokuapp.com/fonts_list").text
    arr = arr_raw.split('\n')
    return arr