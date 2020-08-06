print('Please wait...')

import sys
sys.path.append('/home/runner/hosting601/modules')

# LOCAL FILES
from username601 import *
from database import (
    Economy, selfDB, Dashboard, username601Stats
)
import username601 as myself
import discordgames as Games
import splashes as src
import canvas as Painter

# EXTERNAL PACKAGES
import os
from datetime import datetime as t
from requests import post
from itertools import cycle
import discord
from discord.ext import commands, tasks
import random
import asyncio

# DECLARATION AND STUFF
client = commands.Bot(command_prefix=Config.prefix)
client.remove_command('help')
bot_status = cycle(myself.getStatus())

@client.event
async def on_ready():
    selfDB.post_uptime() # update the uptime
    username601Stats.clear() # clear all cached data on database (reset);
    statusChange.start()
    #updateStats.start()
    for i in os.listdir('./category'):
        if not i.endswith('.py'): continue
        print('[BOT] Loaded cog: '+str(i[:-3]))
        try:
            client.load_extension('category.{}'.format(i[:-3]))
        except Exception as e:
            print('error on loading cog '+str(i[:-3])+': '+str(e))
            pass
    print('Bot is online.')

#@tasks.loop(seconds=900.0)
#async def updateStats():
#    print(f'Updated stuff [{str(t.now())[:-7]}]')
#    post(f'https://botsfordiscord.com/api/bot/{Config.id}', headers={
#        'Content-Type': 'application/json',
#        'Authorization': os.getenv('BOTSFORDISCORD_TOKEN')
#    }, body={'server_count': len(client.guilds)})
#    post(f'https://discordbotlist.com/api/v1/bots/{Config.id}/stats', headers={
#        'Authorization': os.getenv('DISCORDBOTLIST_TOKEN')
#    }, body={
#        'guilds': len(client.guilds),
#        'users': len(client.users)
#    })

@client.event
async def on_raw_reaction_add(payload):
    # IF IS NOT STAR EMOJI, IGNORE
    if str(payload.emoji)!='⭐': return
    data = Dashboard.getStarboardChannel(None, guildid=payload.guild_id)
    if data==None: return
    try:
        messages = await client.get_channel(data['channelid']).history().flatten()
        starboards = [int(str(message.content).split(': ')[1]) for message in messages if message.author.id==Config.id]
        if payload.message_id in starboards: return
    except: return
    message = await client.get_channel(payload.channel_id).fetch_message(payload.message_id)
    if len(message.reactions) == data['starlimit']:
        await client.get_channel(data['channelid']).send(content=f'ID: {message.id}', embed=Dashboard.sendStarboard(discord, message))

@tasks.loop(seconds=7)
async def statusChange():
    new_status = str(next(bot_status)).replace('{MEMBERS}', str(len(client.users))).replace('{SERVERS}', str(len(client.guilds)))
    if new_status.startswith('PLAYING:'): await client.change_presence(activity=discord.Game(name=new_status.split(':')[1]))
    elif new_status.startswith('STREAMING:'): await client.change_presence(activity=discord.Streaming(name=new_status.split(':')[1], url='https://bit.ly/username601'))
    elif new_status.startswith('LISTENING:'): await client.change_presence(activity=discord.Activity(type=discord.ActivityType.listening, name=new_status.split(':')[1]))
    else: await client.change_presence(activity=discord.Activity(type=discord.ActivityType.watching, name=new_status.split(':')[1]))

@client.event
async def on_command_completion(ctx):
    username601Stats.addCommand()

@client.event
async def on_member_join(member):
    # SEND WELCOME CHANNEL
    welcome_message, welcome_channel = Dashboard.send_welcome(member, discord), Dashboard.get_welcome_channel(member.guild.id)
    if welcome_message!=None and welcome_channel!=None: await member.guild.get_channel(welcome_channel).send(embed=welcome_message)
    data = Dashboard.add_autorole(member.guild.id)
    if data.isnumeric():
        # AUTOROLE
        await member.add_roles(member.guild.get_role(int(data)))
    if member.name.startswith('!'):
        if not Dashboard.getDehoister(member.guild): return
        try: await member.edit(nick='Dehoisted user')
        except: pass

@client.event
async def on_member_update(before, after):
    if before.nick == after.nick: return
    elif after.nick==None: return
    if after.nick.startswith('!'):
        if not Dashboard.getDehoister(after.guild.id): return
        try: await after.edit(nick='Dehoisted user')
        except: pass

@client.event
async def on_member_remove(member):
    # REMOVE ALL WARNS
    Dashboard.clearWarn(member)

    # SEND GOODBYE CHANNEL
    goodbye_message, goodbye_channel = Dashboard.send_goodbye(member, discord), Dashboard.get_welcome_channel(member.guild.id)
    if goodbye_message!=None and goodbye_channel!=None: await member.guild.get_channel(goodbye_channel).send(embed=goodbye_message)

@client.event
async def on_guild_channel_create(channel):
    if str(channel.type) not in ['text', 'voice']: return
    data = Dashboard.getMuteRole(channel.guild.id)
    if data==None: return
    if str(channel.type)=='text': return await channel.set_permissions(channel.guild.get_role(data), send_messages=False)
    await channel.set_permissions(channel.guild.get_role(data), connect=False)

@client.event
async def on_guild_channel_delete(channel):
    # IF CHANNEL MATCHES WITHIN DATABASE, DELETE IT ON DATABASE AS WELL
    Dashboard.databaseDeleteChannel(channel)

@client.event
async def on_guild_role_delete(role):
    muterole = Dashboard.getMuteRole(role.guild.id)
    if muterole==None: return
    if muterole!=role.id: return
    Dashboard.editMuteRole(role.guild.id, None)

# DELETE THIS @CLIENT.EVENT IF YOU ARE USING THIS CODE
@client.event
async def on_guild_join(guild):
    if guild.owner.id in [a.id for a in client.get_guild(Config.SupportServer.id).members]:
        userinsupp = client.get_guild(Config.SupportServer.id).get_member(guild.owner.id)
        await userinsupp.add_roles(client.get_guild(Config.SupportServer.id).get_role(727667048645394492))

@client.event
async def on_guild_remove(guild):
    Dashboard.delete_data(guild.id)
    # DELETE THE IF-STATEMENT BELOW IF YOU ARE USING THIS CODE
    if guild.owner.id in [a.id for a in client.get_guild(Config.SupportServer.id).members]:
        userinsupp = client.get_guild(Config.SupportServer.id).get_member(guild.owner.id)
        await userinsupp.remove_roles(client.get_guild(Config.SupportServer.id).get_role(727667048645394492))

@client.event
async def on_command_error(ctx, error):
    if isinstance(error, commands.CommandOnCooldown):
        await ctx.send("You are on cooldown. You can do the command again in {}.".format(myself.time_encode(round(error.retry_after))))
    elif isinstance(error, commands.CommandNotFound): return
    elif 'missing permissions' in str(error).lower(): await ctx.send("I don't have the permission required to use that command!")
    elif 'cannot identify image file' in str(error).lower(): await ctx.send(str(client.get_emoji(BotEmotes.error))+' | Error, it seemed i can\'t load/send the image! Check your arguments and try again. Else, report this to the bot owner using `'+Config.prefix+'feedback.`')
    else: print("ERROR on [{}]: {}".format(ctx.message.content, str(error)))
@client.event
async def on_message(message):
    # THESE TWO IF STATEMENTS ARE JUST FOR ME ON THE SUPPORT SERVER CHANNEL. YOU CAN DELETE THESE TWO.
    if message.channel.id==700040209705861120: await message.author.add_roles(message.guild.get_role(700042707468550184))
    if message.channel.id==724454726908772373: await message.author.add_roles(message.guild.get_role(701586228000325733))

    if len(message.mentions)>0 and message.mentions[0].id == Config.id: await message.channel.send(f'Hi, {message.author.mention}, my prefix is `{Config.prefix}`.')
    await client.process_commands(message) # else bot will not respond to 99% commands

def Username601():
    print('Logging in to discord...')
    client.run(os.getenv('DISCORD_TOKEN'))