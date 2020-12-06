# Custom Framework for username601
A custom "framework" i made for this bot. You can use this framework!<br>
(not planning to be added to PyPI, sorry)<br>
This is the documentation and the examples.<br>

## Initiation
This will make a copy of itself to the client object.<br>
Which means that the functions/classes can be accessed by `client` or `ctx.bot`.<br>
```py
import framework
import discord

client = discord.Client(...)
framework.initiate(client)
```

## Utilities
The main bot utilities.<br>
Here are snippets for some of the functions:<br>
NOTE: the following snippets work <b>after the function above is called.</b><br>

### Getting time lapsed from seconds.
```py
from time import time

@bot.command()
async def how_old_am_i(ctx):
    delta = time() - ctx.author.created_at.timestamp()
    res = ctx.bot.util.strfsecond(delta)
    await ctx.send(f"You made you account in discord {res} ago!")
```

### Converting stuff.
```py
@bot.command()
async def binary(ctx, *args):
    text = " ".join(args) if len(args) > 0 else "text"
    result = ctx.bot.util.binary(text)
    await ctx.send(result)

@bot.command()
async def base64(ctx, *args):
    text = " ".join(args) if len(args) > 0 else "text"
    result = ctx.bot.util.base64(text)
    await ctx.send(result)
```

### Magic 8 Ball
```py
@bot.command(aliases=["8-ball", "8ball"])
async def _8ball(ctx, *args):
	if len(args) < 1:
	    return await ctx.send("Please send a question.")
	
	result = ctx.bot.util.eight_ball(ctx)
	
	return await ctx.send(f"The magik 8 ball says: ***{result}***")
```

### Sending image attachment from URL.
```py
@bot.command()
async def httpcat(ctx, *args):
    input = args[0] if (len(args) > 0) and (args[0].isnumeric()) else "404"
    await ctx.bot.util.send_image_attachment(ctx, "https://http.cat/" + input)
```

### Get request to an API.
```py
@bot.command()
async def cat(ctx):
    result = await ctx.bot.util.get_request(
        "https://aws.random.cat/meow",
        json=True
    )
    
    if not result:
        return await ctx.send("The API may be down. Try again later!")
    
    await ctx.send(result["file"])
```

### Executing terminal code.
```py
@bot.command()
async def execute(ctx, *args):
    if ctx.author.id != OWNER_ID:
        return
    
    command = " ".join(args)
    result = await ctx.bot.util.execute(command)
    await ctx.send("```" + result + "```")
```

### Getting bot stats.
```py
@bot.command()
async def stats(ctx):
    stats = await ctx.bot.util.get_stats()
    await ctx.send("Bot uptime: " + stats["bot_uptime"] + "\nDiscord.py version: " + stats["versions"]["discord_py"])
```

## Argument Parser

### Using the Parser Object
```py
from framework import Parser
from discord.ext import commands

@bot.command()
async def introduce(ctx):
    # Example: !introduce --name Andy

    parser = Parser(ctx)
    parser.add_argument(
        name="--name",
        is_required=False,
        get_value=True,
        value_placeholder="your_name"
    )
    result = await parser.parse()
    name = result["--name"]["value"]

    if (not parser.success) or (name is None):
        return await ctx.send("You need to provide your name >:(")

    await ctx.send(f"Your name is: {name}")
    # Sends "Your name is: Andy"
```

### Parsing an image:
```py
from framework import Parser
from discord.ext import commands

@bot.command()
async def avatar(ctx, *args):
    image = await Parser.parse_image(ctx, args)
    return await ctx.send(f"Here is the avatar: {image}")
```

### Parsing a user:
```py
from framework import Parser
from discord.ext import commands

@bot.command()
async def userinfo(ctx, *args):
    user = Parser.parse_user(ctx, args)
    return await ctx.send(f"User name: {user.name}\nUser ID: {user.id}\nUser Avatar URL: {user.avatar_url}")
```

## Highly Modified ColorThief
This is a self-made ColorThief module, that gets the edge of the image and finds the most common color.<br>
Works best for blending image with background color.<br>

```py
from framework import Smart_ColorThief

async def main(ctx): # ctx is a discord.py context object.
    colorthief = Smart_ColorThief(ctx, "https://example.com/image.png")
    r, g, b = await colorthief.get_color()
    print(r, g, b)
```

## Game Module
A game module.

### TicTacToe
```py
from framework import TicTacToe
player = "O"
opponent = "X"

game = TicTacToe(player=player, opponent=opponent)
game.add_move(order=5, opponent=False)

print(game.show())

who_wins = game.check_if_win()
if who_wins is not None:
    x = "You" if who_wins == player else "i"
    sentence = f"Congratulations, {x} win!"
```

## Message Utilities

### Custom Embed
```py
from framework import embed
from discord.ext import commands

@bot.command()
async def hello(ctx):
    message_embed = embed(ctx, title="Hello!", desc=f"This is a message from {ctx.bot.user.name}")
    await message_embed.send()
```

### Embed Paginator
```py
from framework import Paginator
from discord import Embed
from discord.ext import commands

@bot.command()
async def paginator(ctx):
    paginator = Paginator(ctx, embeds=[
        discord.Embed(title="embed #1", description="This is the first embed"),
        discord.Embed(title="embed #2", description="This is the second embed"),
        discord.Embed(title="embed #3", description="This is the third embed")
    ])

    await paginator.execute()
```

### Querying Embeds
```py
from framework import ChooseEmbed
from discord.ext import commands

@bot.command()
async def query(ctx):
    embed = ChooseEmbed(ctx, [
        "Selection 1",
        "Selection 2",
        "Selection 3"
    ])

    result = await embed.run()
    if result is None:
        return
    
    await ctx.send(result)
```

### Wait for message

```py
from framework import WaitForMessage

@bot.command()
async def choose_a_number(ctx):
    await ctx.send("Please send a text. I'll wait for 20 seconds")
    
    wait_for = WaitForMessage(ctx, timeout=20)
    result = await wait_for.get_message()
    
    if result is None:
        return await ctx.send("You did not input anything after 20 seconds >:(")

    return await ctx.send("Here is your text: " + result.content)
```

## Custom Panel

### Usage
```py
from framework import CustomPanel
from discord import File

@bot.command()
async def card(ctx, *args):
    card = CustomPanel(ctx, title="This is a title", subtitle="This is a subtitle.", description="This is a card", icon="https://example.com/image.png", font="/path/to/font.ttf")
    await card.draw()
    await card.send_as_attachment()
    card.close()
```

### Spotify Card
```py
from framework import CustomPanel, Parser
from discord import File

@bot.command()
async def spotify(ctx, *args):
    user = Parser.parse_user(ctx, *args)
    if user.activity is None:
        return
    
    panel = CustomPanel(ctx, spotify=user.activity)
    await panel.draw()
    await panel.send_as_attachment(content=f"This is {user.name}'s spotify card!")
    panel.close()
```
