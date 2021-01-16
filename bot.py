print('Please wait...')
from discord.ext import commands
from os import environ
from modules import *
from time import time
import discord
import framework
import gc

intents = discord.Intents(
    guilds=True, members=True, emojis=True, presences=True, guild_messages=True
)

client = commands.Bot(command_prefix="1", intents=intents, activity=discord.Activity(type=5, name="hell"), max_messages=100)
framework.initiate(client)
pre_ready_initiation(client)

if client.command_prefix != str(client.util.prefix):
    client.command_prefix = str(client.util.prefix)

client.util.mobile_indicator()

@client.event
async def on_ready():
    await post_ready_initiation(client)
    client.util.load_cog(client.util.cogs_dirname)
    print('Bot is online.')
    
@client.event
async def on_command_completion(ctx):
    client.command_uses += 1
    gc.collect()

@client.event
async def on_member_join(member):
    # SEND WELCOME CHANNEL
    
    data = client.db.get("dashboard", {"serverid": member.guild.id})

    if not data:
        return
    
    if data.get("autorole"):
        # AUTOROLE
        await member.add_roles(member.guild.get_role(data["autorole"]))
    
    if member.name.startswith('!') and data.get("dehoister"):
        try: await member.edit(nick='Dehoisted user')
        except: pass
    
    if data.get("welcome"):
        await member.guild.get_channel(data["welcome"]).send(embed=discord.Embed(
            title=f"Welcome to {member.guild.name}, {member.display_name}!",
            description=f"You are the {member.guild.member_count:,}{['st', 'nd', 'rd', 'th'][(member.guild.member_count - 1 if (member.guild.member_count < 5) else 3)]} member in this server.",
            color=discord.Color.green()
        ).set_thumbnail(url=member.avatar_url))

@client.event
async def on_member_update(before, after):
    if (before.nick == after.nick) or (not after.nick): return
    data = client.db.get("dashboard", {"serverid": after.guild.id})

    if data and (data.get("dehoister")) and after.nick.startswith('!'):
        try: await after.edit(nick='Dehoisted user')
        except: pass

@client.event
async def on_member_remove(member):
    data = client.db.get("dashboard", {"serverid": member.guild.id})
    if not data:
        return
    
    if data.get("welcome"):
        await member.guild.get_channel(data["welcome"]).send(embed=discord.Embed(
            title=f"Goodbye, {member.display_name}...",
            description=f"{member.display_name} left {member.guild.name} after being a member for {client.util.strfsecond(time() - member.joined_at.timestamp())} (Joined at {client.util.timestamp(member.joined_at, include_time_past=False)})",
            color=discord.Color.red()
        ).set_thumbnail(url=member.avatar_url))
    
    client.db.modify("dashboard", client.db.types.CHANGE, {"serverid": member.guild.id}, {"warns": [i for i in data["warns"] if not i.startswith(str(member.id))]})

@client.event
async def on_guild_channel_create(channel):
    if (channel.type != discord.ChannelType.text) and (channel.type != discord.ChannelType.voice):
        return
    
    data = client.db.get("dashboard", {"serverid": channel.guild.id})
    if (not data) or (not data.get("mute")):
        return
    elif channel.type == discord.ChannelType.text:
        return await channel.set_permissions(channel.guild.get_role(data["mute"]), send_messages=False)
    elif channel.type == discord.ChannelType.voice:
        return await channel.set_permissions(channel.guild.get_role(data["mute"]), connect=False)

@client.event
async def on_guild_channel_delete(channel):
    # IF CHANNEL MATCHES WITHIN DATABASE, DELETE IT ON DATABASE AS WELL
    data = client.db.get("dashboard", {"serverid": channel.guild.id})
    if not data:
        return
    
    if data.get("welcome") and (channel.id == data["welcome"]):
        client.db.modify("dashboard", client.db.types.REMOVE, {"serverid": channel.guild.id}, {"welcome": data["welcome"]})

@client.event
async def on_guild_role_delete(role):
    data = client.db.get("dashboard", {"serverid": role.guild.id})
    
    if (not data) or (not data.get("mute")) or (role.id != data["mute"]):
        return

    client.db.modify("dashboard", client.db.types.REMOVE, {"serverid": role.guild.id}, {"mute": role.id})

# DELETE THIS @CLIENT.EVENT IF YOU ARE USING THIS CODE
@client.event
async def on_guild_join(guild):
    if guild.owner.id in list(map(lambda x: x.id, client.get_guild(client.util.server_id).members)):
        userinsupp = client.get_guild(client.util.server_id).get_member(guild.owner.id)
        await userinsupp.add_roles(client.get_guild(client.util.server_id).get_role(727667048645394492))

@client.event
async def on_guild_remove(guild):
    data = client.db.get("dashboard", {"serverid": guild.id})
    if data:
        client.db.delete("dashboard", {"serverid": guild.id})

    # DELETE THE IF-STATEMENT BELOW IF YOU ARE USING THIS CODE
    if guild.owner.id in list(map(lambda x: x.id, client.get_guild(client.util.server_id).members)):
        userinsupp = client.get_guild(client.util.server_id).get_member(guild.owner.id)
        await userinsupp.remove_roles(client.get_guild(client.util.server_id).get_role(727667048645394492))

@client.event
async def on_command_error(ctx, error):
    await ctx.bot.util.handle_error(ctx, error)

#def isdblvote(author):
#    if not author.bot: return False
#    elif author.id==479688142908162059: return False
#    return True

@client.event
async def on_message(message):
    if (not message.guild) or message.author.bot or message.reference or ((time() - message.author.created_at.timestamp()) < 604800): return# or isdblvote(message.author): return

    #if message.author.id in client.blacklisted_ids: return
    if message.content.startswith(f'<@{client.user.id}>') or message.content.startswith(f'<@!{client.user.id}>'):
        return await message.channel.send(f'Hello, {message.author.name}! My prefix is `{client.command_prefix}`. use `{client.command_prefix}help` for help')
    #if message.guild.id==client.util.server_id and message.author.id==479688142908162059:
    #    data = int(str(message.embeds[0].description).split('(id:')[1].split(')')[0])
    #    if not database.Economy.get(data): return
    #    rewards = database.Economy.daily(data)
    #    try: await client.get_user(data).send(f'Thanks for voting! **You received {rewards} bobux!**')
    #    except: return
    await client.process_commands(message) # else bot will not respond to 99% commands

def Username601():
    print('Logging in to discord...')
    client.run(environ['DISCORD_TOKEN'])

if __name__ == "__main__":
    Username601()