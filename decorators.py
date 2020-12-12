from discord.ext import commands
from discord import Embed, Color

def command(aliases: list = None):
    if not aliases:
        return commands.command(pass_context=True)
    return commands.command(pass_context=True, aliases=aliases)

def cooldown(amount: int):
    return commands.cooldown(1, amount, commands.BucketType.user)

def require_args(count: int = 1):
    async def predicate(ctx):
        if len(ctx.message.content.split()[1:]) < count:
            await ctx.send(embed=Embed(title=f"This command requires at least {count} argument{('' if count == 1 else 's')}.", color=Color.red()))
            return False
        return True
    return commands.check(predicate)

def owner_only():
    async def predicate(ctx):
        if ctx.author.id != ctx.bot.util.owner_id:
            await ctx.send(embed=Embed(title=f"This command is reserved only for the developer.", color=Color.red()))
            return False
        return True
    return commands.check(predicate)