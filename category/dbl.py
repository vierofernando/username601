import dbl as topgg
import discord
from os import environ
from discord.ext import commands, tasks

class dbl(commands.Cog):
    def __init__(self, client):
        self.token = environ['DBL_TOKEN']
        self.dblpy = topgg.DBLClient(client, self.token, autopost=True)
    
    async def on_guild_post():
        print("Posted guild count.")

def setup(bot):
    bot.add_cog(dbl(bot))
