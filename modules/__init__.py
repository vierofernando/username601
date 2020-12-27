from .canvas import Painter, GifGenerator
from .commandmanager import BotCommands
from os import environ
from time import time

def pre_ready_initiation(client):
    client.remove_command('help')
    setattr(client, 'canvas', Painter(client.util.assets_dir, client.util.fonts_dir, client.util.json_dir))
    setattr(client, 'gif', GifGenerator(client.util.assets_dir, client.util.fonts_dir))
    setattr(client, 'command_uses', 0)

async def post_ready_initiation(client):
    economy_data = len(list(client.db.db["economy"].find()))
    dashboard_data = len(list(client.db.db["dashboard"].find()))
    client.db.modify("config", client.db.types.CHANGE, {"h": True}, {
        "stats": f"{len(client.guilds)}:{len(client.users)}:{economy_data}:{dashboard_data}:{time()}"
    })
    print("Successfully made a POST request stats to the API.")
    bot_commands = BotCommands(client)
    await bot_commands.initiate()
    setattr(client, "cmds", bot_commands)