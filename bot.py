print('Please wait...')
from modules import *
from datetime import datetime as t
from discord.ext import commands
from os import environ, listdir
from PIL import UnidentifiedImageError
import discord
import framework

intents = discord.Intents(
    guilds=True, members=True, emojis=True, guild_reactions=True, presences=True, guild_messages=True
)

client = commands.Bot(command_prefix="1", intents=intents, activity=discord.Activity(type=5, name="2020 survival competition"))
framework.initiate(client)
framework.Util(client)
pre_ready_initiation(client)
environ['BOT_MODULES_DIR'] = client.util.modules_dir
environ['BOT_JSON_DIR'] = client.util.json_dir

async def ready():
    for i in listdir('./{}'.format(client.util.cogs_dirname)):
        if not i.endswith('.py'): continue
        print('[BOT] Loaded cog: '+str(i[:-3]))
        try:
            client.load_extension('{}.{}'.format(client.util.cogs_dirname, i[:-3]))
        except Exception as e:
            print('error on loading cog '+str(i[:-3])+': '+str(e))
            pass
    post_ready_initiation(client)
    print('Bot is online.')

@client.event
async def on_guild_join(guild):
    if 'bot list' in guild.name.lower(): return
    elif 'test' in guild.name.lower(): return
    bot_members = [i for i in guild.members if i.bot]
    if round(bot_members/len(guild.members)*100) >= 95: await guild.leave()

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
    if str(channel.type) not in ['text', 'voice']: return
    data = database.Dashboard.getMuteRole(channel.guild.id)
    if data is None: return
    if str(channel.type)=='text': return await channel.set_permissions(channel.guild.get_role(data), send_messages=False)
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
    if isinstance(error, commands.CommandNotFound): return
    elif isinstance(error, commands.CommandOnCooldown): return await ctx.send("You are on cooldown. You can do the command again in {}.".format(lapsed_time_from_seconds(round(error.retry_after))), delete_after=2)
    if hasattr(error, "original"):
        error = error.original
    
    if isinstance(error, discord.Forbidden): 
        try: return await ctx.send("I don't have the permission required to use that command!")
        except: return
    elif isinstance(error, UnidentifiedImageError): return await ctx.send(str(emote(client, 'error'))+' | Error, it seemed i can\'t load/send the image! Check your arguments and try again. Else, report this to the bot owner using `'+client.command_prefix+'feedback.`')
    elif isinstance(error, framework.GetRequestFailedException):
        return await ctx.bot.util.send_error_message("A request failed to the API. Please try again later!")
    else:
        await client.get_channel(client.util.feedback_channel).send(content='<@{}> there was an error!'.format(client.util.owner_id), embed=discord.Embed(
            title='Error', color=discord.Colour.red(), description=f'Content:\n```{ctx.message.content}```\n\nError:\n```{str(error)}```'
        ).set_footer(text='Bug made by user: {} (ID of {})'.format(str(ctx.author), ctx.author.id)))
        await ctx.send('Sorry, there was an error when executing this command.\nThis message has been reported to the developer of the bot.', delete_after=3)

def isdblvote(author):
    if not author.bot: return False
    elif author.id==479688142908162059: return False
    return True

@client.event
async def on_message(message):
    if isdblvote(message.author) or message.guild is None: return
    if message.author.bot: return
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
    client.loop.create_task(ready())
    client.run(environ['DISCORD_TOKEN'])
if __name__ == "__main__": Username601()