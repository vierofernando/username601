import discord
from discord.ext import commands

def command(*args):
    if len(list(args))==0: return commands.command(pass_context=True)
    return commands.command(pass_context=True, aliases=list(args)[0].split(','))

def cooldown(*args):
    return commands.cooldown(1, int(list(args)[0]), commands.BucketType.user)