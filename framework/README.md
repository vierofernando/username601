# Custom Framework for username601
A custom "framework" i made for this bot. You can use this framework!<br>
(not planning to be added to PyPI, sorry)<br>
This is the documentation and the examples.<br>

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
    image = Parser.parse_image(ctx, args)
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

## Twemoji Parser
Gets the image URL for an emoji.

```py
from framework import emoji_to_url
url = emoji_to_url("<EMOJI>")
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
    card.draw()
    
    await card.send_as_attachment()
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
    
    panel = CustomPanel(ctx, spt=user.activity)
    await panel.draw()
    await panel.send_as_attachment(content=f"This is {user.name}'s spotify card!")
    panel.close()
```
