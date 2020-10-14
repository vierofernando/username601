from .username601 import *
from .canvas import Painter, GifGenerator
from .commandmanager import BotCommands
from . import algorithm, discordgames, database, username601
from requests import post
from os import environ

def pre_ready_initiation(client):
    client.remove_command('help')
    setattr(client, 'canvas', Painter(config('ASSETS_DIR'), config('FONTS_DIR')))
    setattr(client, 'gif', GifGenerator(config('ASSETS_DIR'), config('FONTS_DIR')))
    setattr(client, 'last_downtime', t.now().timestamp())
    setattr(client, 'command_uses', 0)
    setattr(client, 'utils', username601)
    setattr(client, 'db', database)
    setattr(client, 'games', discordgames)
    setattr(client, 'algorithm', algorithm)
    setattr(client, 'cmds', BotCommands())

def post_ready_initiation(client):
    setattr(client, 'error_emoji',   str(client.get_emoji(client.utils.config('EMOJI_ERROR'))))
    setattr(client, 'loading_emoji', str(client.get_emoji(client.utils.config('EMOJI_LOADING'))))
    setattr(client, 'success_emoji', str(client.get_emoji(client.utils.config('EMOJI_SUCCESS'))))
    test = post("https://useless-api.vierofernando.repl.co/update_bot_stats", headers={
        'superdupersecretkey': environ["USELESSAPI"],
        'guild_count': str(len(client.guilds)),
        'users_count': str(len(client.users))
    }).json()
    if test['success']: print("Successfully made a POST request stats to the API.")