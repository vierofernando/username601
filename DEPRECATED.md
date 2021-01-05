# List of deprecated or discontinued commands<br>

## DEPRECATED COMMANDS<br>
these are commands i decided to delete or change to with the reasons.

### 1death-star<br>
Deleted in favor of `1explode --animated`

### 1imgascii<br>
Merged to `1ascii --image <image> [--hastebin]`

### 1reply<br>
Merged to `1say <text> --reply`

### 1gamble<br>
Changed to `1bet`

### 1setdesc<br>
Moved to `1bal --desc [text]`

### 1userinfo<br>
Moved to `1member`

### 1emojiimg, 1serveremojis, 1emoji<br>
Merged down to `1emoji`

### 1gdlevel, 1gdsearch, 1gdprofile, 1gdlogo, 1gdcomment<br>
Merged down to `1gd`

### 1destroy, 1ifunny, 1msgbox, 1wasted<br>
Rarely used (also deleted to save RAM)

### 1garfield, 1ufo<br>
The API no lorger works (same thing has happened to other bots as well)

### 1wonka, 1fry, 1money, 1doge, 1philosoraptor, 1avmeme<br>
Have been merged down to `1memegen`

### 1ytthumbnail<br>
Completely pointless and also buggy regex<br>

### 1colorinfo, 1randomcolor, 1rolecolor<br>
Have been merged down to `1color`<br>

### 1search, 1randomword, 1temmie<br>
Useless and buggy anyway<br>

### 1steamprofile, 1tts<br>
API endpoint removed/no longer working.<br>

### 1pokequiz<br>
Quiz was really buggy and API sometimes doesn't work for no reason<br>

### 1hack<br>
Editing messages too quickly is still API abuse, despite the big slowmode<br>
soo... no.<br>

### 1hitler<br>
May be discriminating or controversial<br>

### 1time, 1ship, 1coffee, 1food, 1flip, 1about, 1wanted, 1randomavatar, 1lovelevel, 1gaylevel, 1crazyfrog, 1rage, 1worship, 1pikachu, 1lucario, 1sadcat, 1wasted, 1art, 1ifunny, 1firstwords, 1ruin, 1squidwardstv, 1evol, 1scooby, 1presentation, 1gru, 1amiajoke, 1call, 1salty, 1chatroulette, 1frame, 1scroll, 1imgcaptcha, 1phcomment, 1hbd, 1slap, 1botmembers, 1deathnote, 1id, 1reactnum, 1bomb, 1iss, 1ghibli, 1sof, 1serverstats, 1kannagen, 1leetspeak<br>
completely useless and barely anyone ever uses it<br>

### 1newemote<br>
The last command with scraping to be deprecated, the reason is:<br>
1. scraping is not that good, and 2. sometimes discordemojis.com gives NSFW emojis, yuck.<br>

### 1trap, 1trumptweet, 1deepfry, 1steamgame, 1blurpify, 1threats, 1whowouldwin, 1app, 1ph<br>
My bot seemed to cannot have a GET request with the API, so since they are<br>
not functional, i will delete then.<br>

### 1notstonks<br>
The API owner said they moved to a different URL.<br>

### 1ss<br>
This is a screenshot command that lets you screenshot websites,<br>
however the website filter eats the RAM usage causing for the bot to crash.<br>
Since i am planning for this bot to be NSFW-free, this command is deprecated.<br>

### 1firstwords<br>
This is a meme generation command that is deprecated<br>
because positioning the text is HELLA hard.<br>

### 1randombot<br>
This is an *old* bot command that generates random bot<br>
by scraping [the Discord Bot List website.](https://top.gg)<br>
I decided to delete the command since scraping is quite a bad technique<br>
and also the website recently installed a security wall to prevent<br>
DDoSers from visiting the website.<br>

### 1stonks, 1meandtheboys, 1pabloescobar, 1tom, 1surprisedpikachu, 1monkeypuppet, 1homer<br>
All of the commands above uses the same meme format, and uses the same type of function.<br>
I decided to delete all of the commands above because the canvas text formatting is<br>
really buggy and overall no one uses it.<br>

### 1hastebin<br>
This is a command that posts a text to [hastebin](https://hastebin.com/) using the API.<br>
I decided to abandon this feature and replace it with `1imgascii` because posting<br>
short random text to hastebin seems too stupid.<br>

### 1sacred, 1window<br>
This is an avatar manipulation that i deleted because it uses a *non-relatable* meme reference,<br>
and the canvas image placement is bad.<br>

### 1ytsearch<br>
This one is long deprecated, because but instead of using the [YouTube API](https://developers.google.com/youtube),<br>
i decided to scrape the website (bad idea). Also sometimes the embed won't work because Discord character limits.<br>

## DISCONTINUED COMMANDS
these are commands that i decided to not develop.

### Leveling system<br>
Leveling system seems to be a common feature in discord bots nowadays,<br>
but i don't plan on updating my database every message sent,<br>
fearing database RAM crash or something, (like if a raid happened)<br>
i decided to abandon this feature.<br>

### Music commands<br>
I also decided to abandon the "`Voice/Music Bots TM` platform"<br>
because my bot **is not fully 24/7.** also [repl.it](https://repl.it) doesn't<br>
like music bots somehow soo, moving on from that.<br>

### Setting Birthday / Reminders<br>
This one is discontinued because my bot again, is not fully 24/7.<br>
sometimes repl.it randomly shuts down my bot, so<br>
`await asyncio.sleep(6969)` or `if datetime.datetime.now().timestamp() > database.gettimestamp()`<br>
is not to be added soon.<br>

#### P.S: If you wanna have the commands back or you have ideas, you can pull out an issue and send me your workaround!
