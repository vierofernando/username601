prefix = '>'
cmdtypes = ['Bot help', 'Moderation', 'Utilities', 'Math', 'Fun', 'Games', 'Encoding', 'Images', 'Apps']
bot_ver = '1.9.4'
bot_changelog = 'Added slowmode command, fixed crashes and errors'

bothelp = 'vote, feedback [text], help, about, connections, inviteme, createbot, ping'
maths = 'math [num] [sym] [num], factor [num], multiplication [num], sqrt [num], isprime [num], rng [num], median [array], mean [array]'
encoding = 'ascii [word], binary [text], supreme [text], reverse [text], length [text], qr [text], leet [text], emojify [text]'
games = 'tictactoe [symbol], hangman, mathquiz, geoquiz, guessavatar, coin, dice, rock, paper, scissors, gddaily, gdweekly, gdprofile [name], gdsearch [level name], gdlevel [level id]'
fun = 'tts [text], joke, memes, slap [tag], hbd [tag], gaylevel [tag], randomavatar, secret, inspirobot, meme, 8ball, deathnote, choose [array]'
images = 'ph help, ship, coffee, wallpaper, trash [tag], jpeg [tag], cat, sadcat, dog, fox, bird, magik [tag], facts [text], invert [tag], pixelate [tag], b&w [tag], drake help, salty [tag], wooosh [tag], captcha [text], achieve [text], scroll [text], call [text], challenge [text], didyoumean help'
utilities = 'embed help, ss --help, catfact, dogfact, funfact, steam [profile], googledoodle, ytsearch [query], bored, search [query], randomcolor, randomword, country [name], time, newemote, ghiblifilms, ytthumbnail [link]'
discordAPI = 'slowmode [seconds], ar [tag] [role], rr [tag] [role], clear [count], kick [tag] [reason], ban [tag] [reason], nick [tag] [new nick], makechannel [type] [name], emojiinfo [emoji], permissions [user_tag], roleinfo [tag], id [tag], getinvite, botmembers, serverinfo, servericon, avatar [tag], userinfo [tag], roles, channels, serveremojis, reactmsg [text], reactnum [num1] [num2]'
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