prefix = '>'
cmdtypes = ['Bot help', 'Moderation', 'Utilities', 'Math', 'Fun', 'Games', 'Encoding', 'Images', 'Apps']
bot_ver = '1.9.4b'
bot_changelog = 'Added more commands and more bugfixing stuff'

def getPrefix():
    return prefix

# JSON TIME LOL
github_object = {
    "files": [
        {
            "name":"readme.md",
            "type":"to read more info about the repo and the files"
        },
        {
            "name":"bot.py",
            "type":"main bot source code. commands belong here."
        },
        {
            "name":"username601.py",
            "type":"basically like `config.json` for discord.js programmers."
        },
        {
            "name":"discordgames.py",
            "type":"the guy that handles all of games commands from this bot."
        },
        {
            "name":"database.py",
            "type":"code for managing databases." 
        },
        {
            "name":"splashes.py",
            "type":"a big array code for splashes. like random messages (splashes) on your minecraft main menu."
        },
        {
            "name":".gitignore",
            "type":"the code that ignores my git commits."            
        },
        {
            "name":"assets (DIRECTORY)",
            "type":"all the bot's assets, like .png files."
        }
    ]
}

o_web = 0
o_desk = 0
o_pho = 0
botcount = 0
online = 0
idle = 0
dnd = 0
offline = 0

bothelp = 'vote, feedback [text], help, about, github, connections, inviteme, createbot, ping'
maths = 'math [num] [sym] [num], factor [num], multiplication [num], sqrt [num], isprime [num], rng [num], median [array], mean [array]'
encoding = 'ascii [word], binary [text], supreme [text], reverse [text], length [text], qr [text], leet [text], emojify [text]'
games = 'tictactoe [symbol], hangman, mathquiz, geoquiz, guessavatar, coin, dice, rock, paper, scissors, gddaily, gdweekly, gdcomment, gdbox [text], gdlogo [text], gdprofile [name], gdsearch [level name], gdlevel [level id]'
fun = 'tts [text], joke, memes, slap [tag], hbd [tag], gaylevel [tag], randomavatar, secret, inspirobot, meme, 8ball, deathnote, choose [array]'
images = 'ph help, ship, coffee, wallpaper, trash [tag], jpeg [tag], cat, sadcat, dog, fox, bird, magik [tag], facts [text], invert [tag], pixelate [tag], b&w [tag], drake help, salty [tag], wooosh [tag], captcha [text], achieve [text], scroll [text], call [text], challenge [text], didyoumean help'
utilities = 'robohash, weather [city], colorinfo [hex], embed help, ss --help, catfact, dogfact, funfact, steam [profile], googledoodle, bored, search [query], randomcolor, randomword, country [name], time, newemote, ghiblifilms, ytthumbnail [link]'
discordAPI = 'lockdown [seconds], slowmode [seconds], ar [tag] [role], rr [tag] [role], clear [count], kick [tag] [reason], ban [tag] [reason], nick [tag] [new nick], makechannel [type] [name], emojiinfo [emoji], permissions [user_tag], roleinfo [tag], id [tag], getinvite, botmembers, serverinfo, servericon, avatar [tag], userinfo [tag], roles, channels, serveremojis, reactmsg [text], reactnum [num1] [num2]'
apps = 'imdb, translate, wikipedia'
commandLength = [len(bothelp.split(',')), len(maths.split(',')), len(encoding.split(',')), len(games.split(',')), len(fun.split(',')), len(utilities.split(',')), len(discordAPI.split(',')), len(images.split(',')), len(apps.split(','))]
totalLength = 0
for i in range(0, len(commandLength)):
    totalLength = int(totalLength) + int(commandLength[i])

ordertypes = [
    '**Bot help ('+str(commandLength[0])+')**\n```'+str(bothelp)+'```',
    '**Moderation ('+str(commandLength[6])+')**\n```'+str(discordAPI)+'```',
    '**Utilities ('+str(commandLength[5])+')**\n```'+str(utilities)+'```',
    '**Math ('+str(commandLength[1])+')**\n```'+str(maths)+'```',
    '**Fun ('+str(commandLength[4])+')**\n```'+str(fun)+'```',
    '**Games ('+str(commandLength[3])+')**\n```'+str(games)+'```',
    '**Encoding ('+str(commandLength[2])+')**\n```'+str(encoding)+'```',
    '**Images ('+str(commandLength[7])+')**\n```'+str(images)+'```',
    '**Apps ('+str(commandLength[8])+')**\n```'+str(apps)+'```'
]