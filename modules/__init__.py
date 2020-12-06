from .username601 import *
from .canvas import Painter, GifGenerator
from .commandmanager import BotCommands
from . import algorithm, discordgames, database, username601
from requests import post
from os import environ

def pre_ready_initiation(client):
    client.remove_command('help')
    setattr(client, 'canvas', Painter(client.util.assets_dir, client.util.fonts_dir, client.util.json_dir))
    setattr(client, 'gif', GifGenerator(client.util.assets_dir, client.util.fonts_dir))
    setattr(client, 'command_uses', 0)
    setattr(client, 'utils', username601)
    setattr(client, 'db', database)
    setattr(client, 'games', discordgames)
    setattr(client, 'algorithm', algorithm)

async def post_ready_initiation(client):
    test = post("https://useless-api.vierofernando.repl.co/update_bot_stats", headers={
        'superdupersecretkey': environ["USELESSAPI"],
        'guild_count': str(len(client.guilds)),
        'users_count': str(len(client.users))
    }).json()
    if test['success']: print("Successfully made a POST request stats to the API.")
    bot_commands = BotCommands(client)
    await bot_commands.initiate()
    setattr(client, "cmds", bot_commands)