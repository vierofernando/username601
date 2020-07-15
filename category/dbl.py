import dbl as topgg
import discord
import os
from sys import path
path.append('/app/modules')
from username601 import *
from discord.ext import commands

class dbl(commands.Cog):
    def __init__(self, client):
        self.client = client
        self.token = os.environ["DBL_TOKEN"]
        self.dblpy = topgg.DBLClient(self.client, self.token, autopost=True)
    
    async def on_guild_post():
        print("Posted guild count.")

def setup(bot):
    bot.add_cog(dbl(bot))
