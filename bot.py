print('Please wait...')

from modules import *
from datetime import datetime as t
from discord.ext import commands
from os import environ, listdir
import discord

# DECLARATION AND STUFF
client = commands.Bot(command_prefix=prefix)
client.remove_command('help')
setattr(client, 'canvas', Painter(cfg('ASSETS_DIR'), cfg('FONTS_DIR')))
setattr(client, 'gif', GifGenerator(cfg('ASSETS_DIR'), cfg('FONTS_DIR')))
setattr(client, 'last_downtime', t.now().timestamp())
setattr(client, 'command_uses', 0)
setattr(client, 'utils', username601)
setattr(client, 'db', database)
setattr(client, 'games', discordgames)
setattr(client, 'algorithm', algorithm)
setattr(client, 'cmds', BotCommands())
environ['BOT_MODULES_DIR'] = cfg('MODULES_DIR')
environ['BOT_JSON_DIR'] = cfg('JSON_DIR')

@client.event
async def on_ready():
    await client.change_presence(activity=discord.Activity(type=discord.ActivityType.listening, name="👻Botghost.com👻 | Type "+cfg('PREFIX')+"help for command"))
    for i in listdir('./{}'.format(cfg('COGS_DIRNAME'))):
        if not i.endswith('.py'): continue
        print('[BOT] Loaded cog: '+str(i[:-3]))
        try:
            client.load_extension('{}.{}'.format(cfg('COGS_DIRNAME'), i[:-3]))
        except Exception as e:
            print('error on loading cog '+str(i[:-3])+': '+str(e))
            pass
    print('Bot is online.')

@client.event
async def on_guild_join(guild):
    if 'bot list' in guild.name.lower(): return
    elif 'test' in guild.name.lower(): return
    bot_members = [i for i in guild.members if i.bot]
    if round(bot_members/len(guild.members)*100) >= 95: await guild.leave()

@client.event
async def on_raw_reaction_add(payload):
    # IF IS NOT STAR EMOJI, IGNORE
    if str(payload.emoji)!='⭐': return
    data = database.Dashboard.getStarboardChannel(None, guildid=payload.guild_id)
    if data==None: return
    try:
        messages = await client.get_channel(data['channelid']).history().flatten()
        starboards = [int(str(message.content).split(': ')[1]) for message in messages if message.author.id==cfg('BOT_ID', integer=True)]
        if payload.message_id in starboards: return
    except: return
    message = await client.get_channel(payload.channel_id).fetch_message(payload.message_id)
    if len(message.reactions) == data['starlimit']:
        await client.get_channel(data['channelid']).send(content=f'ID: {message.id}', embed=database.Dashboard.sendStarboard(discord, message))

@client.event
async def on_command_completion(ctx):
    client.command_uses += 1

@client.event
async def on_member_join(member):
    # SEND WELCOME CHANNEL
    welcome_message, welcome_channel = database.Dashboard.send_welcome(member, discord), database.Dashboard.get_welcome_channel(member.guild.id)
    if welcome_message!=None and welcome_channel!=None: await member.guild.get_channel(welcome_channel).send(embed=welcome_message)
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
    elif after.nick==None: return
    if after.nick.startswith('!'):
        if not database.Dashboard.getDehoister(after.guild.id): return
        try: await after.edit(nick='Dehoisted user')
        except: pass
@client.event
async def on_member_remove(member):
    database.Dashboard.clearWarn(member)
    goodbye_message, goodbye_channel = database.Dashboard.send_goodbye(member, discord), database.Dashboard.get_welcome_channel(member.guild.id)
    if goodbye_message!=None and goodbye_channel!=None: await member.guild.get_channel(goodbye_channel).send(embed=goodbye_message)

@client.event
async def on_guild_channel_create(channel):
    if str(channel.type) not in ['text', 'voice']: return
    data = database.Dashboard.getMuteRole(channel.guild.id)
    if data==None: return
    if str(channel.type)=='text': return await channel.set_permissions(channel.guild.get_role(data), send_messages=False)
    await channel.set_permissions(channel.guild.get_role(data), connect=False)

@client.event
async def on_guild_channel_delete(channel):
    # IF CHANNEL MATCHES WITHIN DATABASE, DELETE IT ON DATABASE AS WELL
    database.Dashboard.databaseDeleteChannel(channel)

@client.event
async def on_guild_role_delete(role):
    muterole = database.Dashboard.getMuteRole(role.guild.id)
    if muterole==None: return
    if muterole!=role.id: return
    database.Dashboard.editMuteRole(role.guild.id, None)

# DELETE THIS @CLIENT.EVENT IF YOU ARE USING THIS CODE
@client.event
async def on_guild_join(guild):
    if guild.owner.id in [a.id for a in client.get_guild(cfg('SERVER_ID', integer=True)).members]:
        userinsupp = client.get_guild(cfg('SERVER_ID', integer=True)).get_member(guild.owner.id)
        await userinsupp.add_roles(client.get_guild(cfg('SERVER_ID', integer=True)).get_role(727667048645394492))

@client.event
async def on_guild_remove(guild):
    database.Dashboard.delete_data(guild.id)
    # DELETE THE IF-STATEMENT BELOW IF YOU ARE USING THIS CODE
    if guild.owner.id in [a.id for a in client.get_guild(cfg('SERVER_ID', integer=True)).members]:
        userinsupp = client.get_guild(cfg('SERVER_ID', integer=True)).get_member(guild.owner.id)
        await userinsupp.remove_roles(client.get_guild(cfg('SERVER_ID', integer=True)).get_role(727667048645394492))

@client.event
async def on_command_error(ctx, error):
    if isinstance(error, commands.CommandOnCooldown): return await ctx.send("You are on cooldown. You can do the command again in {}.".format(time_encode(round(error.retry_after))), delete_after=2)
    elif isinstance(error, commands.CommandNotFound): return
    elif 'noarguments' in str(error).lower(): return await ctx.send('{} | Please insert arguments! `Like insert your name as a parameter.`'.format(emote(client, 'error')), delete_after=5)
    elif 'nouserfound' in str(error).lower(): return await ctx.send('{} | No user found.'.format(emote(client, 'error')), delete_after=5)
    elif 'noprofile' in str(error).lower(): return await ctx.send('{} | You do not have any profile...\nYou can create one with `{}new`.'.format(emote(client, 'error'), prefix), delete_after=5)
    elif 'missing permissions' in str(error).lower() or 'Missing Access' in str(error): 
        try: return await ctx.send("I don't have the permission required to use that command!")
        except: return
    elif 'cannot identify image file' in str(error).lower(): return await ctx.send(str(emote(client, 'error'))+' | Error, it seemed i can\'t load/send the image! Check your arguments and try again. Else, report this to the bot owner using `'+prefix+'feedback.`')
    else:
        await client.get_channel(cfg('FEEDBACK_CHANNEL', integer=True)).send(content='<@{}> there was an error!'.format(cfg('OWNER_ID')), embed=discord.Embed(
            title='Error', color=discord.Colour.red(), description=f'Content:\n```{ctx.message.content}```\n\nError:\n```{str(error)}```'
        ).set_footer(text='Bug made by user: {} (ID of {})'.format(str(ctx.author), ctx.author.id)))
        await ctx.send('There was an error. Error reported to the developer! sorry for the inconvenience...', delete_after=3)

def isdblvote(author):
    if not author.bot: return False
    elif author.id==479688142908162059: return False
@client.event
async def on_message(message):
    if isdblvote(message.author) or message.guild==None: return
    if message.content.startswith('<@{}>'.format(cfg('BOT_ID'))) or message.content.startswith('<@!{}>'.format(cfg('BOT_ID'))): return await message.channel.send(f'Hello, {message.author.name}! My prefix is `1`. use `1help` for help')
    if message.guild.id==cfg('SERVER_ID', integer=True) and message.author.id==479688142908162059:
        data = int(str(message.embeds[0].description).split('(id:')[1].split(')')[0])
        if database.Economy.get(data)==None: return
        rewards = database.Economy.daily(data)
        try: await client.get_user(data).send(f'Thanks for voting! **You received {rewards} bobux!**')
        except: return
        
    await client.process_commands(message) # else bot will not respond to 99% commands

def Username601():
    print('Logging in to discord...')
    client.run(environ['DISCORD_TOKEN'])