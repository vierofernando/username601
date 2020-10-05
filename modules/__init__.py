from .username601 import *
from .canvas import Painter, GifGenerator
from .commandmanager import BotCommands
from . import algorithm, discordgames, database, username601

def pre_ready_initiation(client):
    client.remove_command('help')
    setattr(client, 'canvas', Painter(cfg('ASSETS_DIR'), cfg('FONTS_DIR')))
    setattr(client, 'gif', GifGenerator(cfg('ASSETS_DIR'), cfg('FONTS_DIR')))
    setattr(client, 'last_downtime', t.now().timestamp())
    setattr(client, 'command_uses', 0)
    setattr(client, 'utils', username601)
    setattr(client, 'db', database)
    setattr(client, 'games', discordgames)
    setattr(client, 'algorithm', algorithm)
    setattr(client, 'cmds', BotCommands())

def post_ready_initiation(client):
    setattr(client, 'error_emoji', client.utils.emote(client, 'error'))
    setattr(client, 'loading_emoji', client.utils.emote(client, 'loading'))
    setattr(client, 'success_emoji', client.utils.emote(client, 'success'))