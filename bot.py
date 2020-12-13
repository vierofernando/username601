print('Please wait...')
from discord.ext import commands
from os import environ
from modules import *
import discord
import framework
import gc

intents = discord.Intents(
    guilds=True, members=True, emojis=True, guild_reactions=True, presences=True, guild_messages=True
)

client = commands.Bot(command_prefix="1", intents=intents, activity=discord.Activity(type=5, name="2020 survival competition"))
framework.initiate(client)
pre_ready_initiation(client)

if client.command_prefix != client.util.prefix:
    client.command_prefix = client.util.prefix

@client.event
async def on_ready():
    await post_ready_initiation(client)
    client.util.load_cog(client.util.cogs_dir)
    client.util.post_ready()
    print('Bot is online.')

@client.event
async def on_raw_reaction_add(payload):
    if str(payload.emoji)!='⭐': return
    if payload.event_type != 'REACTION_ADD': return
    data = database.Dashboard.getStarboardChannel(None, guildid=payload.guild_id)
    if data is None: return
    try:
        messages = await client.get_channel(data['channelid']).history().flatten()
        starboards = [int(str(message.content).split(': ')[1]) for message in messages if message.author.id==client.user.id]
        if payload.message_id in starboards: return
    except: return
    message = await client.get_channel(payload.channel_id).fetch_message(payload.message_id)
    if len(message.reactions) == data['starlimit']:
        await client.get_channel(data['channelid']).send(content=f'ID: {message.id}', embed=database.Dashboard.sendStarboard(discord, message))

@client.event
async def on_command_completion(ctx):
    client.command_uses += 1
    gc.collect()

@client.event
async def on_member_join(member):
    # SEND WELCOME CHANNEL
    welcome_message, welcome_channel = database.Dashboard.send_welcome(member, discord), database.Dashboard.get_welcome_channel(member.guild.id)
    if welcome_message is not None and welcome_channel is not None: await member.guild.get_channel(welcome_channel).send(embed=welcome_message)
    data = database.Dashboard.add_autorole(member.guild.id)
    if data.isnumeric():
        # AUTOROLE
        await member.add_roles(member.guild.get_role(int(data)))
    if member.name.startswith('!'):
        if not database.Dashboard.getDehoister(member.guild): return
        try: await member.edit(nick='Dehoisted user')
        except: pass

@client.event
async def on_member_update(before, after):
    if before.nick == after.nick: return
    elif after.nick is None: return
    if after.nick.startswith('!'):
        if not database.Dashboard.getDehoister(after.guild.id): return
        try: await after.edit(nick='Dehoisted user')
        except: pass

@client.event
async def on_member_remove(member):
    database.Dashboard.clearWarn(member)
    goodbye_message, goodbye_channel = database.Dashboard.send_goodbye(member, discord), database.Dashboard.get_welcome_channel(member.guild.id)
    if goodbye_message is not None and goodbye_channel is not None: await member.guild.get_channel(goodbye_channel).send(embed=goodbye_message)

@client.event
async def on_guild_channel_create(channel):
    if (channel.type != discord.ChannelType.text) and (channel.type != discord.ChannelType.voice): return
    data = database.Dashboard.getMuteRole(channel.guild.id)
    if data is None: return
    elif channel.type == discord.ChannelType.text: return await channel.set_permissions(channel.guild.get_role(data), send_messages=False)
    await channel.set_permissions(channel.guild.get_role(data), connect=False)

@client.event
async def on_guild_channel_delete(channel):
    # IF CHANNEL MATCHES WITHIN DATABASE, DELETE IT ON DATABASE AS WELL
    database.Dashboard.databaseDeleteChannel(channel)

@client.event
async def on_guild_role_delete(role):
    muterole = database.Dashboard.getMuteRole(role.guild.id)
    if muterole is None: return
    if muterole!=role.id: return
    database.Dashboard.editMuteRole(role.guild.id, None)

# DELETE THIS @CLIENT.EVENT IF YOU ARE USING THIS CODE
@client.event
async def on_guild_join(guild):
    if guild.owner.id in list(map(lambda x: x.id, client.get_guild(client.util.server_id).members)):
        userinsupp = client.get_guild(client.util.server_id).get_member(guild.owner.id)
        await userinsupp.add_roles(client.get_guild().get_role(727667048645394492))

@client.event
async def on_guild_remove(guild):
    database.Dashboard.delete_data(guild.id)
    # DELETE THE IF-STATEMENT BELOW IF YOU ARE USING THIS CODE
    if guild.owner.id in list(map(lambda x: x.id, client.get_guild(client.util.server_id).members)):
        userinsupp = client.get_guild(client.util.server_id).get_member(guild.owner.id)
        await userinsupp.remove_roles(client.get_guild(client.util.server_id).get_role(727667048645394492))

@client.event
async def on_command_error(ctx, error):
    await ctx.bot.util.handle_error(ctx, error)

def isdblvote(author):
    if not author.bot: return False
    elif author.id==479688142908162059: return False
    return True
@client.event
async def on_message(message):
    if isdblvote(message.author) or message.guild is None: return
    if message.author.bot or (message.reference is not None): return
    #if message.author.id in client.blacklisted_ids: return
    if message.content.startswith(f'<@{client.user.id}>') or message.content.startswith(f'<@!{client.user.id}>'): return await message.channel.send(f'Hello, {message.author.name}! My prefix is `1`. use `1help` for help')
    #if message.guild.id==client.util.server_id and message.author.id==479688142908162059:
    #    data = int(str(message.embeds[0].description).split('(id:')[1].split(')')[0])
    #    if database.Economy.get(data) is None: return
    #    rewards = database.Economy.daily(data)
    #    try: await client.get_user(data).send(f'Thanks for voting! **You received {rewards} bobux!**')
    #    except: return
    await client.process_commands(message) # else bot will not respond to 99% commands

def Username601():
    print('Logging in to discord...')
    client.run(environ['DISCORD_TOKEN'])
if __name__ == "__main__": Username601()