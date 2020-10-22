import discord
from discord.ext import commands

def command(*args):
    if len(args)==0: return commands.command(pass_context=True)
    return commands.command(pass_context=True, aliases=args[0].split(','))

def cooldown(*args):
    return commands.cooldown(1, int(args[0]), commands.BucketType.user)