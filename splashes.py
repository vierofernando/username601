import random
import requests
def getGeoQuiz():
    return ['capital', 'region', 'subregion', 'population', 'demonym', 'nativeName']
def getBinary(a):
    if a==2:
        arr = ["10000", "10001", "10010", "10011", "10100", "10101", "10110", "10111", "11000", "11001"]
    else:
        arr = ["00001", "00010", "00011", "00100", "00101", "000110", "00111", "01000", "01001", "01010", "01011", "01100", "01101", "01110", "01111", "10000", "10001", "10010", "10011", "10100", "10101", "10110", "10111", "11000", "11001", "11010"]
    return arr
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
def getGitMsg():
    arr = [
        'My githoob',
        'Repository for Username601',
        'Repo601',
        '601Hub',
        'GitHype',
        'GiiiiiiitHub!',
        'GetCodeHub',
        'Copy and paste my bot\'s code!',
        'See how much i copied from stackoverflow!',
        'GitRepo601',
        'Repository601',
        'Commit #601: Removed repository',
        'See my token on GitHub!'
    ]
    return random.choice(arr)
def epicness():
    arr = [
        'epicness',
        'badassness',
        'sadness',
        'dramatization',
        'genericness',
        'coolness',
        'eBicness',
        'kewlness'
    ]
    chose = random.choice(arr)
    total = ''
    for i in range(0, len(chose)):
        alph = list(chose)[i].upper()
        total = total + ' ' + alph
    return total

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
def getTag():
    arr = [
        "ya liek tagz?",
        "we don't accept services with tags, sorry.",
        "tag me? lol NO.",
        'why command me with a tag? that is so unnecessary!',
        'NO TAG, ~~NO~~ YES SERVICE.',
        'MORE TAG, LESS SERVICE.',
        'Everybody gangsta until somebody tagged username601',
        'Taggy taggy tag tag!',
        'Playin\' with tagz, bro?',
        'So uhh i heard u liek tagz',
        'What kind of word is that?',
        'tag me? why not tag everyone lul',
        'you liek tagging me huh uwu',
        'pinging me? why not >ping instead lol',
        'discord pings are not cool!',
        'i am busy, please don\'t ping me. thanks.',
        'bruh, pings? again?',
        'this is like, the 96024th time i am getting pinged.',
        'it seems that commands doesn\'t require for you to ping me...',
        'ping... pong...?',
        'Me: Noo you can\'t ping me!! ;(\nYou: hehe discord go ping ping'
    ]
    return arr
def getAbout():
    arr = [
        'Traceback (most recent call last)',
        'I liek memes',
        '601 in my name means BOT in leetspeak.\n*THE MORE YOU KNOW*',
        'Hello, discordians! It\'s-a-me. Bot. Which may look stupid the fact that\nthere are THOUSANS of discord bots out there, so *let\'s get straight into it.* (no meme intended)',
        'Wha? ME? okay then, here ya go.',
        'Here are some silly lil information.',
        'Beep boop, beep beep?',
        'JavaScript ~~sucks~~ is bad. (i was told to change it lmao)',
        'MEE6 vs Dyno, which is better?',
        'MEEx6=MEEMEEMEEMEEMEEMEE',
        'my token is = \*Slams head on keyboard*',
        'HELP? Please try >help. thanks',
        'Don\'t be a broom. Use discord.',
        'Discard the discord right away!',
        'Garbage bot giving some information here.',
        'look, i have challenge for you. Can you read this without blinking?',
        'Don\'t laugh at me.',
        'Python is for nerds.',
        'Everybody gangsta until username601 become self-aware',
        'Coding is not fun, but it will pay off.',
        'Hehe discord go ping ping',
        'Vote me in top.gg or i will take your pokecord credits',
        'And then you showed up. You dangerous, mute, lunatic.',
        'This bot is available for WhatsApp, Skype, AOL Instant Messenger, even Nokia phones also support me! :D',
        'V53\|2\|V4\|V\|3 BOT',
        'pizza time',
        'r/programmerhumor is my favourite subreddit, ~~cuz i am a nerd~~',
        'MEEP6',
        'Ha ha Username601 go vroom vroom',
        'Botname601',
        'Programmed *ENTIRELY* using Notepad',
        'Wanna be a madlad? Try programming a new language\n*WITHOUT LOOKING AT STACKOVERFLOW.*',
        'Top.gg is the platform where nerds flex their cool bots--\nAnd there is me, lonely :((('
        'I am the BEST programmer. I can do HTML',
        'HTML programmers >>> Java Programmers',
        'Only madlads use Discord.HTML lul',
        'Hello can i code minecraft using HTML pls thx',
        'only epic programmers use HTML',
        'print(\'Hella, World!\')',
        'PyScript or Javathon? :flushed:',
        'You can get to google if you know Machine code language LUL'
    ]
    return arr
def getTicTacToeHeader():
    arr = [
        'my cool banner',
        'mspaint.exe',
        'ew, worst banner 10/1',
        'myself',
        'someone',
        '@everyone',
        'random stranger',
        'a discard user',
        'a skype-hater',
        'a guy',
        'a cool guy',
        'a normal breathing person',
        'the chosen one',
        'impossible',
        'the g4m3r'
    ]
    return arr