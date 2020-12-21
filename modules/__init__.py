from .canvas import Painter, GifGenerator
from .commandmanager import BotCommands
from os import environ

def pre_ready_initiation(client):
    client.remove_command('help')
    setattr(client, 'canvas', Painter(client.util.assets_dir, client.util.fonts_dir, client.util.json_dir))
    setattr(client, 'gif', GifGenerator(client.util.assets_dir, client.util.fonts_dir))
    setattr(client, 'command_uses', 0)

async def post_ready_initiation(client):
    test = await client.util.useless_client.post("https://useless-api.vierofernando.repl.co/update_bot_stats?guild_count=" + str(len(client.guilds)) + "&users_count=" + str(len(client.users)))
    test = await test.json()
    if test['success']: print("Successfully made a POST request stats to the API.")
    bot_commands = BotCommands(client)
    await bot_commands.initiate()
    setattr(client, "cmds", bot_commands)