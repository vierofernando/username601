print('Please wait...')

import sys
sys.path.append('/home/runner/hosting601/modules')

# LOCAL FILES
from username601 import *
from database import Economy, selfDB, Dashboard
import username601 as myself
import discordgames as Games
import splashes as src
import canvas as Painter

# EXTERNAL PACKAGES
import os
from itertools import cycle
from os import environ as fetchdata
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
    statusChange.start()
    for i in os.listdir('./category'):
        print('[BOT] Loaded cog: '+str(i[:-3]))
        client.load_extension('category.{}'.format(i[:-3]))
    print('Bot is online.')

@tasks.loop(seconds=7)
async def statusChange():
    new_status = str(next(bot_status)).replace('{MEMBERS}', str(len(client.users))).replace('{SERVERS}', str(len(client.guilds)))
    if new_status.startswith('PLAYING:'): await client.change_presence(activity=discord.Game(name=new_status.split(':')[1]))
    elif new_status.startswith('STREAMING:'): await client.change_presence(activity=discord.Streaming(name=new_status.split(':')[1], url='https://bit.ly/username601'))
    elif new_status.startswith('LISTENING:'): await client.change_presence(activity=discord.Activity(type=discord.ActivityType.listening, name=new_status.split(':')[1]))
    else: await client.change_presence(activity=discord.Activity(type=discord.ActivityType.watching, name=new_status.split(':')[1]))
    
@client.event
async def on_member_join(member):
    welcome_message, welcome_channel = Dashboard.send_welcome(member, discord), Dashboard.get_welcome_channel(member.guild.id)
    if welcome_message!=None and welcome_channel!=None: await member.guild.get_channel(welcome_channel).send(embed=welcome_message)
    data = Dashboard.add_autorole(member.guild.id)
    if data.isnumeric():
        await member.add_roles(member.guild.get_role(int(data)))

@client.event
async def on_member_remove(member):
    goodbye_message, goodbye_channel = Dashboard.send_goodbye(member, discord), Dashboard.get_welcome_channel(member.guild.id)
    if goodbye_message!=None and goodbye_channel!=None: await member.guild.get_channel(goodbye_channel).send(embed=goodbye_message)

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
    
    if not message.author.bot:
        if message.content.startswith('<@'+str(client.user.id)+'>') or message.content.startswith('<@!'+str(client.user.id)+'>'): await message.channel.send(f'Hi! My prefix is `{Config.prefix}`.')
        await client.process_commands(message) # else bot will not respond to 99% commands

print('Logging in to discord...')
client.run(fetchdata['DISCORD_TOKEN'])