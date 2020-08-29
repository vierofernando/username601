import discord
from discord.ext import commands
import sys
import random
import asyncio
sys.path.append('/home/runner/hosting601/modules')
from username601 import *
from splashes import num2word
from decorators import command, cooldown
from datetime import datetime as t
from database import Dashboard
from canvas import Painter, GifGenerator
import username601 as myself

class moderation(commands.Cog):
    def __init__(self, client):
        self.client = client
        self.canvas = Painter(
            r'/home/runner/hosting601/assets/pics/',
            r'/home/runner/hosting601/assets/fonts/'
        )
        self.gif = GifGenerator(
            r'/home/runner/hosting601/assets/pics/',
            r'/home/runner/hosting601/assets/fonts/'
        )

    @command('jp,joinpos,joindate,jd')
    @cooldown(5)
    async def joinposition(self, ctx, *args):
        current_time = t.now().timestamp()
        user = myself.getUser(ctx, args)
        wait = await ctx.send('{} | Iterating through {} members...'.format(self.client.get_emoji(BotEmotes.loading), len(ctx.guild.members)))
        sortedJoins = sorted([current_time-i.joined_at.timestamp() for i in ctx.guild.members])[::-1]
        num, users = [i for i in range(len(sortedJoins)) if (current_time-user.joined_at.timestamp())==sortedJoins[i]][0], []
        for i in range(-10, 11):
            try:
                placement = (num + i) + 1
                if placement < 1: continue
                locate = sortedJoins[num + i]
                username = [str(i) for i in ctx.guild.members if (current_time-i.joined_at.timestamp())==locate][0]
                if i == 0: username = f'**{username}**'
                users.append({
                    'user': username,
                    'time': locate,
                    'order': str(placement)
                })
            except IndexError:
                pass
        em = discord.Embed(title='Your join position', description='\n'.join([
            '{}. {} ({} ago)'.format(i['order'], i['user'], myself.time_encode(round(i['time']))) for i in users
        ]), color=discord.Colour.from_rgb(201, 160, 112))
        await wait.edit(content='', embed=em)

    @command('serverconfig,configuration,serversettings,settings')
    @cooldown(1)
    async def config(self, ctx):
        data = Dashboard.getData(ctx.guild.id)
        if data==None: return await ctx.send('{} | This server does not have any configuration for this bot.'.format(self.client.get_emoji(BotEmotes.error)))
        autorole = 'Set to <@&{}>'.format(data['autorole']) if data['autorole']!=None else '<Not set>'
        welcome = 'Set to <#{}>'.format(data['welcome']) if data['welcome']!=None else '<Not set>'
        starboard = 'Set to <#{}> (with {} reactions required)'.format(data['starboard'], data['star_requirements']) if data['starboard']!=None else '<Not set>'
        mute = 'Set to <@&{}>'.format(data['mute']) if data['mute']!=None else '<Not set>'
        extras = [len(data['shop']), len(data['warns'])]
        dehoister = 'Enabled :white_check_mark:' if data['dehoister'] else 'Disabled :x:'
        await ctx.send(embed=discord.Embed(title=f'{ctx.guild.name}\'s configuration', description=f'**Auto role:** {autorole}\n**Welcome channel:** {welcome}\n**Starboard channel: **{starboard}\n**Name/nick dehoister: **{dehoister}\n**Mute role: **{mute}\n**Members warned: **{extras[1]}\n**Shop products sold: **{extras[0]}', color=discord.Colour.from_rgb(201, 160, 112)).set_thumbnail(url=ctx.guild.icon_url))

    @command()
    @cooldown(5)
    async def mute(self, ctx, *args):
        toMute = myself.getUser(ctx, args, allownoargs=False)
        if not ctx.author.guild_permissions.manage_messages: return await ctx.send('{} | No `manage messages` permission!'.format(self.client.get_emoji(BotEmotes.error)))
        role = Dashboard.getMuteRole(ctx.guild.id)
        if role==None:
            await ctx.send('{} | Please wait... Setting up...\nThis may take a while if your server has a lot of channels.'.format(str(self.client.get_emoji(BotEmotes.loading))))
            role = await ctx.guild.create_role(name='Muted', color=discord.Colour.from_rgb(0, 0, 1))
            ratelimit_counter = 0
            # BEWARE API ABUSE! ADDED SOME STUFF TO REDUCE RATELIMITS
            for i in ctx.guild.channels:
                if ratelimit_counter > 10: # take a break for a while
                    await asyncio.sleep(2)
                    ratelimit_counter = 0 ; continue
                if str(i.type)=='text':
                    await i.set_permissions(role, send_messages=False)
                    ratelimit_counter += 1
                elif str(i.type)=='voice':
                    await i.set_permissions(role, connect=False)
                    ratelimit_counter += 1
            Dashboard.editMuteRole(ctx.guild.id, role.id)
            role = role.id
        role = ctx.guild.get_role(role)
        try:
            await toMute.add_roles(role)
            await ctx.send('{} | Muted. Ductaped {}\'s mouth.'.format(str(self.client.get_emoji(BotEmotes.success)), toMute.name))
        except Exception as e:
            print(e)
            await ctx.send('{} | I cannot mute him... maybe i has less permissions than him.\nHis mouth is too powerful.'.format(str(self.client.get_emoji(BotEmotes.error))))
    
    @command()
    @cooldown(5)
    async def unmute(self, ctx):
        toUnmute = myself.getUser(ctx, args, allownoargs=False)
        roleid = Dashboard.getMuteRole(ctx.guild.id)
        if roleid==None: return await ctx.send('{} | He is not muted!\nOr maybe you muted this on other bot... which is not compatible.'.format(self.client.get_emoji(BotEmote.error)))
        elif roleid not in [i.id for i in ctx.message.mentions[0].roles]:
            return await ctx.send('{} | That guy is not muted.'.format(self.client.get_emoji(BotEmotes.error)))
        try:
            await toUnmute.remove_roles(ctx.guild.get_role(roleid))
            await ctx.send('{} | {} unmuted.'.format(self.client.get_emoji(BotEmotes.success), toUnmute.name))
        except:
            await ctx.send('{} | I cannot unmute {}!'.format(self.client.get_emoji(BotEmotes.error), ctx.message.mentions[0].name))

    @command('dehoist')
    @cooldown(15)
    async def dehoister(self, ctx, *args):
        if not ctx.author.guild_permissions.manage_nicknames: return await ctx.send('{} | You need the `Manage Nicknames` permissions!'.format(str(self.client.get_emoji(BotEmotes.error))))
        data = Dashboard.getDehoister(ctx.guild.id)
        if not data: 
            Dashboard.setDehoister(ctx.guild, True)
            return await ctx.send(embed=discord.Embed(
                title='Activated dehoister.',
                description=f'**What is dehoister?**\nDehoister is an automated part of this bot that automatically renames someone that tries to hoist their name (for example: `!ABC`)\n\n**How do i deactivate this?**\nJust type `{Config.prefix}dehoister`.\n\n**It doesn\'t work for me!**\nMaybe because your role position is higher than me, so i don\'t have the permissions required.',
                color=discord.Colour.from_rgb(201, 160, 112)
            ))
        Dashboard.setDehoister(ctx.guild, False)
        await ctx.send('{} | Dehoister deactivated.'.format(self.client.get_emoji(BotEmotes.success)))

    @command()
    @cooldown(15)
    async def starboard(self, ctx, *args):
        wait = await ctx.send('{} | Please wait...'.format(
            str(self.client.get_emoji(BotEmotes.error))
        ))
        if not ctx.author.guild_permissions.manage_channels:
            return await wait.edit(content='{} | You need the `Manage channels` permission.'.format(
                str(self.client.get_emoji(BotEmotes.error))
            ))
        starboard_channel = Dashboard.getStarboardChannel(ctx.guild)
        if len(list(args))==0:
            if starboard_channel['channelid']==None:
                channel = await ctx.guild.create_text_channel(name='starboard', topic='Server starboard channel. Every funny/cool posts will be here.')
                Dashboard.addStarboardChannel(channel, 1)
                return await wait.edit(content=f'{str(self.client.get_emoji(BotEmotes.success))} | OK. Created a channel <#{str(channel.id)}>. Every starboard will be set there.\nTo remove starboard, type `{Config.prefix}starboard remove`.\nBy default, starboard requirements are set to 1 reaction. To increase, type `{Config.prefix}starboard limit <number>`.')
            return await wait.edit(content='', embed=discord.Embed(
                title=f'Starboard for {ctx.guild.name}',
                description='Channel: <#{}>\nStars required to reach: {}'.format(
                    starboard_channel['channelid'], starboard_channel['starlimit']
                ), color=discord.Colour.from_rgb(201, 160, 112)
            ))
        if starboard_channel['channelid']==None: return
        elif list(args)[0].lower().startswith('rem'):
            Dashboard.removeStarboardChannel(ctx.guild)
            return await wait.edit(content='{} | OK. Starboard for this server is deleted.'.format(str(self.client.get_emoji(BotEmotes.success))))
        elif list(args)[0].lower()=='limit':
            try:
                num = int(list(args)[1])
                if not num in range(1, 20):
                    return await wait.edit(content='{} | Invalid number.'.format(str(self.client.get_emoji(BotEmotes.error))))
                Dashboard.setStarboardLimit(num, ctx.guild)
                await wait.edit(content='{} | Set the limit to {} reactions.'.format(str(self.client.get_emoji(BotEmotes.success)), str(num)))
            except:
                await wait.edit(content='{} | Invalid number.'.format(str(self.client.get_emoji(BotEmotes.error))))

    @command()
    @cooldown(15)
    async def serverstats(self, ctx):
        await ctx.send(file=discord.File(
            self.canvas.serverstats(ctx.guild), "serverstats.png"
        ))
    
    @command()
    @cooldown(5)
    async def warn(self, ctx, *args):
        if len(ctx.message.mentions)==0:
            return await ctx.send('{} | Mention someone.'.format(str(self.client.get_emoji(BotEmotes.error))))
        elif ctx.message.mentions[0].id == ctx.author.id:
            return await ctx.send(':joy: | Warning yourself? Really?')
        elif not ctx.author.guild_permissions.manage_messages:
            return await ctx.send('{} | You need to have manage messages permissions to do this man. Sad.'.format(str(self.client.get_emoji(BotEmotes.error))))
        reason = 'No reason provided' if (len(list(args))<2) else ' '.join(list(args)[1:len(list(args))])
        if len(reason)>100: return await ctx.send('{} | Your reason is toooo longgg!'.format(
            str(self.client.get_emoji(BotEmotes.error))
        ))
        warned = Dashboard.addWarn(ctx.message.mentions[0], ctx.author, reason)
        if warned:
            return await ctx.send(f'{str(self.client.get_emoji(BotEmotes.success))} | {ctx.message.mentions[0].name}#{ctx.message.mentions[0].discriminator} was warned by {ctx.author.name}#{ctx.author.discriminator} for the reason *"{reason}"*.')
        await ctx.send(f'{str(self.client.get_emoji(BotEmotes.error))} | An error occurred.')
    
    @command('warns,warnslist,warn-list,infractions')
    @cooldown(5)
    async def warnlist(self, ctx):
        source = ctx.author if (len(ctx.message.mentions)==0) else ctx.message.mentions[0]
        data = Dashboard.getWarns(source)
        if data==None: return await ctx.send(f'{str(self.client.get_emoji(BotEmotes.error))} | Good news! {source.name} does not have any warns!')
        warnlist = '\n'.join([
            '{}. "{}" (warned by <@{}>)'.format(
                i+1, data[i]['reason'], data[i]['moderator']
            ) for i in range(0, len(data))
        ][0:10])
        await ctx.send(embed=discord.Embed(
            title=f'Warn list for {source.name}',
            description=warnlist,
            color=discord.Colour.red()
        ))
    
    @command('deletewarn,clear-all-infractions,clear-infractions,clearinfractions,delinfractions,delwarn,clearwarn,clear-warn')
    @cooldown(5)
    async def unwarn(self, ctx):
        if not ctx.author.guild_permissions.manage_messages:
            return await ctx.send(f'{str(self.client.get_emoji(BotEmotes.error))} | You need the `Manage messages` permissions to unwarn someone.')
        if len(ctx.message.mentions)==0: return await ctx.send('{} | Please TAG someone !!!'.format(
            str(self.client.get_emoji(BotEmotes.error))
        ))
        unwarned = Dashboard.clearWarn(ctx.message.mentions[0])
        if unwarned: return await ctx.send(f'{str(self.client.get_emoji(BotEmotes.success))} | Successfully unwarned {ctx.message.mentions[0].name}.')
        await ctx.send(f'{str(self.client.get_emoji(BotEmotes.error))} | An error occurred.')

    @command('welcomelog,setwelcome')
    @cooldown(30)
    async def welcome(self, ctx, *args):
        if not ctx.author.guild_permissions.manage_channels:
            await ctx.send("{} | You need the `Manage Channels` permission!".format(str(self.client.get_emoji(BotEmotes.error))))
        else:
            if len(list(args))==0:
                await ctx.send(embed=discord.Embed(
                    title='Command usage',
                    description='{}welcome <CHANNEL>\n{}welcome disable'.format(Config.prefix, Config.prefix),
                    color=discord.Color.from_rgb(201, 160, 112)
                ))
            else:
                if list(args)[0].lower()=='disable':
                    Dashboard.set_welcome(ctx.guild.id, None)
                    await ctx.send("{} | Welcome disabled!".format(str(self.client.get_emoji(BotEmotes.success))))
                else:
                    try:
                        if list(args)[0].startswith("<#") and list(args)[0].endswith('>'): channelid = int(list(args)[0].split('<#')[1].split('>')[0])
                        else: channelid = int([i.id for i in ctx.guild.channels if str(i.name).lower()==str(''.join(list(args))).lower()][0])
                        Dashboard.set_welcome(ctx.guild.id, channelid)
                        await ctx.send("{} | Success! set the welcome log to <#{}>!".format(str(self.client.get_emoji(BotEmotes.success)), channelid))
                    except Exception as e:
                        await ctx.send("{} | Invalid arguments!".format(str(self.client.get_emoji(BotEmotes.error))))
    
    @command('auto-role,welcome-role,welcomerole')
    @cooldown(30)
    async def autorole(self, ctx, *args):
        if not ctx.author.guild_permissions.manage_roles:
            await ctx.send("{} | You need the `Manage Roles` permission!".format(str(self.client.get_emoji(BotEmotes.error))))
        else:
            if len(list(args))==0:
                await ctx.send(embed=discord.Embed(
                    title='Command usage',
                    description='{}autorole <ROLENAME/ROLEPING>\n{}autorole disable'.format(Config.prefix, Config.prefix),
                    color=discord.Color.from_rgb(201, 160, 112)
                ))
            else:
                if list(args)[0].lower()=='disable':
                    Dashboard.set_autorole(ctx.guild.id, None)
                    await ctx.send("{} | Autorole disabled!".format(str(self.client.get_emoji(BotEmotes.success))))
                else:
                    try:
                        if list(args)[0].startswith("<@&") and list(args)[0].endswith('>'): roleid = int(list(args)[0].split('<@&')[1].split('>')[0])
                        else: roleid = int([i.id for i in ctx.guild.roles if str(i.name).lower()==str(' '.join(list(args))).lower()][0])
                        Dashboard.set_autorole(ctx.guild.id, roleid)
                        await ctx.send("{} | Success! set the autorole to **{}!**".format(str(self.client.get_emoji(BotEmotes.success)), ctx.guild.get_role(roleid).name))
                    except:
                        await ctx.send("{} | Invalid arguments!".format(str(self.client.get_emoji(BotEmotes.error))))
 
    @command('bigemoji,emojipic,emoji-img')
    @cooldown(3)
    async def emojiimg(self, ctx, *args):
        try:
            em = list(args)[0].lower()
            if em.startswith('<:a:'): _id, an = em.split(':')[3].split('>')[0], True
            else: _id, an = em.split(':')[2].split('>')[0], False
            if an: await ctx.send(file=discord.File(self.gif.giffromURL('https://cdn.discordapp.com/emojis/{}.gif'.format(_id)), 'emoji.gif'))
            else: await ctx.send(file=discord.File(self.canvas.urltoimage('https://cdn.discordapp.com/emojis/{}.png'.format(_id)), 'emoji.png'))
        except:
            await ctx.send(str(self.client.get_emoji(BotEmotes.error))+' | Invalid emoji.')
            

    @command()
    @cooldown(15)
    async def rolecolor(self, ctx, *args):
        unprefixed = ' '.join(list(args))
        if len(unprefixed.split('#'))==1:
            await ctx.send(f'Please provide a hex!\nExample: `{Config.prefix}rolecolor {random.choice(ctx.message.guild.roles).name}` #ff0000')
        else:
            if ctx.message.author.guild_permissions.manage_roles==False:
                await ctx.send(str(self.client.get_emoji(BotEmotes.error)) +' | You need the `MANAGE ROLES` permission to change role colors!')
            else:
                role = None
                for i in ctx.message.guild.roles:
                    if unprefixed.split('#')[0][:-1].lower()==str(i.name).lower():
                        print(unprefixed.split('#')[0][:-1].lower())
                        role = i
                        break
                if role==None:
                    await ctx.send(str(self.client.get_emoji(BotEmotes.error)) +' | Invalid role input! :(')
                else:
                    try:
                        colint = myself.toint(unprefixed.split('#')[1].lower())
                        await role.edit(colour=discord.Colour(colint))
                        await ctx.send('Color of '+role.name+' role has been changed.', delete_after=5)
                    except Exception as e:
                        await ctx.send(str(self.client.get_emoji(BotEmotes.error)) + f' | An error occurred while editing role:```{e}```')
    
    @command()
    @cooldown(15)
    async def slowmode(self, ctx, *args):
        if len(list(args))==0: await ctx.send(str(self.client.get_emoji(BotEmotes.error))+" | How long in seconds?")
        else:
            cd = list(args)[0]
            if ctx.message.author.guild_permissions.manage_channels:
                if not cd.isnumeric():
                    await ctx.send(str(self.client.get_emoji(BotEmotes.error))+" | That cooldown is not a number!")
                else:
                    if int(cd)<0:
                        await ctx.send(str(self.client.get_emoji(BotEmotes.error))+" | Minus slowmode? Did you mean slowmode 0 seconds?")
                    elif int(cd)>21600:
                        await ctx.send(str(self.client.get_emoji(BotEmotes.error))+" | That is too hecking sloow....")
                    else:
                        await ctx.message.channel.edit(slowmode_delay=cd)
                        await ctx.send(str(self.client.get_emoji(BotEmotes.success))+" | Channel slowmode cooldown has been set to "+str(myself.time_encode(int(cd))))
            else: await ctx.send(str(self.client.get_emoji(BotEmotes.error))+" | You need the manage channels permission to do this command!")

    @command('addrole,add-role')
    @cooldown(15)
    async def ar(self, ctx, *args):
        args = list(args)
        if not ctx.message.author.guild_permissions.manage_roles:
            await ctx.send(str(self.client.get_emoji(BotEmotes.error)) +f' | <@{str(ctx.message.author.id)}>, you don\'t have the `Manage Roles` permission!')
        else:
            try:
                toadd = None
                if '<@&' in ''.join(args):
                    toadd = ctx.message.guild.get_role(int(''.join(args).split('<@&')[1].split('>')[0]))
                else:
                    for i in ctx.message.guild.roles:
                        if str(i.name).lower()==str(ctx.message.content).split('> ')[1].lower():
                            toadd = ctx.message.guild.get_role(i.id)
                            break
                if toadd==None:
                    await ctx.send(str(self.client.get_emoji(BotEmotes.error))+" | Invalid input!")
                else:
                    aruser = ctx.message.mentions[0]
                    await aruser.add_roles(toadd)
                    await ctx.send('Congratulations, '+aruser.name+', you now have the '+toadd.name+' role! :tada:')
            except IndexError:
                await ctx.send(str(self.client.get_emoji(BotEmotes.error))+" | Invalid arguments!")
    
    @command('removerole,remove-role')
    @cooldown(15)
    async def rr(self, ctx, *args):
        args = list(args)
        if not ctx.message.author.guild_permissions.manage_roles:
            await ctx.send(str(self.client.get_emoji(BotEmotes.error)) +f' | <@{str(ctx.message.author.id)}>, you don\'t have the `Manage Roles` permission!')
        else:
            try:
                toadd = None
                if '<@&' in ''.join(args):
                    toadd = ctx.message.guild.get_role(int(''.join(args).split('<@&')[1].split('>')[0]))
                else:
                    for i in ctx.message.guild.roles:
                        if str(i.name).lower()==str(ctx.message.content).split('> ')[1].lower():
                            toadd = ctx.message.guild.get_role(i.id)
                            break
                if toadd==None:
                    await ctx.send(str(self.client.get_emoji(BotEmotes.error))+" | Invalid input!")
                else:
                    rruser = ctx.message.mentions[0]
                    await rruser.remove_roles(toadd)
                    await ctx.send(rruser.name+', you lost the '+toadd.name+' role... :pensive:')
            except IndexError:
                await ctx.send(str(self.client.get_emoji(BotEmotes.error))+" | Invalid arguments!")

    @command('kick')
    @cooldown(15)
    async def ban(self, ctx, *args):
        if len(list(args))==0:
            await ctx.send(str(self.client.get_emoji(BotEmotes.error))+" | Nope. No arguments means no moderation:tm:.")
        elif len(ctx.message.mentions)==0:
            await ctx.send(str(self.client.get_emoji(BotEmotes.error))+" | Nope. No tagging means no moderation:tm:.")
        else:
            accept = True
            if 'kick' in ctx.message.content:
                if not ctx.message.author.guild_permissions.kick_members:
                    await ctx.send(str(self.client.get_emoji(BotEmotes.error))+" | No kick members permission?")
                    accept = False
            else:
                if not ctx.message.author.guild_permissions.ban_members:
                    await ctx.send(str(self.client.get_emoji(BotEmotes.error))+" | No ban members permission?")
                    accept = False
            if ctx.guild.owner.id!=ctx.author.id:
                if ctx.message.mentions[0].guild_permissions.administrator==True:
                    await ctx.send(str(self.client.get_emoji(BotEmotes.error))+" | Nope, that guy probably has higher permissions than you.")
                    accept = False
                elif ctx.message.mentions[0].roles[::-1][0].position>ctx.message.guild.get_member(self.client.user.id).roles[::-1][0].position:
                    await ctx.send(str(self.client.get_emoji(BotEmotes.error))+" | Try moving my role higher than "+ctx.message.mentions[0].name+"'s role.")
            if accept:
                if 'kick' in ctx.message.content:
                    await ctx.message.guild.kick(ctx.message.mentions[0])
                    await ctx.send(str(self.client.get_emoji(BotEmotes.success))+" | Successfully kicked "+ctx.message.mentions[0].name+".")
                else:
                    await ctx.message.guild.ban(ctx.message.mentions[0])
                    await ctx.send(str(self.client.get_emoji(BotEmotes.success))+" | Successfully banned "+ctx.message.mentions[0].name+".")
    @command('purge')
    @cooldown(2)
    async def clear(self, ctx, *args):
        if not ctx.message.author.guild_permissions.manage_channels:
            await ctx.send(str(self.client.get_emoji(BotEmotes.error))+" | You need the manage channel permission!")
        else:
            if len(list(args))==0:
                await ctx.send(str(self.client.get_emoji(BotEmotes.error))+" | How many messages to be purged?")
            else:
                if len(ctx.message.mentions)==0:
                    if not list(args)[0].isnumeric():
                        await ctx.send(str(self.client.get_emoji(BotEmotes.error))+" | Not a number!")
                    else:
                        if int(list(args)[0])<0:
                            await ctx.send(str(self.client.get_emoji(BotEmotes.error))+" | Minus?")
                        elif int(list(args)[0])>250:
                            await ctx.send(str(self.client.get_emoji(BotEmotes.error))+" | Too much! Use clone channel instead!")
                        else:
                            topurge = int(list(args)[0])+1
                            await ctx.message.channel.purge(limit=topurge)
                            await ctx.send(str(self.client.get_emoji(BotEmotes.success))+" | Done! {} messages has been cleared!".format(str(list(args)[0])), delete_after=3)
                else:
                    def check(m):
                        return m.author.id == ctx.message.mentions[0].id
                    dels = await ctx.message.channel.purge(check=check, limit=500)
                    await ctx.send(str(self.client.get_emoji(BotEmotes.success))+' | Done. Cleared '+str(len(dels))+' message by <@'+str(ctx.message.mentions[0].id)+'>.', delete_after=3)
    @command('hidechannel')
    @cooldown(5)
    async def lockdown(self, ctx, *args):
        if len(list(args))==0: await ctx.send(str(self.client.get_emoji(BotEmotes.error)) +f' | Invalid parameters. Correct Example: `{prefix}{args[0][1:]} [disable/enable]`')
        else:
            accept = True
            if not ctx.message.author.guild_permissions.administrator: await ctx.message.channel.send(str(self.client.get_emoji(BotEmotes.error))+' | You need the `Administrator` permission to do this, unless you are trying to mute yourself.')
            else:
                if 'enable' not in args[0].lower():
                    if 'disable' not in args[0].lower():
                        await ctx.send(str(self.client.get_emoji(BotEmotes.error))+' | Oops! Please type `enable` or `disable`.')
                        accept = False
                if accept:
                    try:
                        if args[0].lower()=='disable':
                            if 'hidechannel' in ctx.message.content: await ctx.message.channel.set_permissions(ctx.message.guild.default_role, read_messages=True)
                            if 'lockdown' in ctx.message.content: await ctx.message.channel.set_permissions(ctx.message.guild.default_role, send_messages=True)
                        elif args[0].lower()=='enable':
                            if 'hidechannel' in ctx.message.content: await ctx.message.channel.set_permissions(ctx.message.guild.default_role, read_messages=False)
                            if 'lockdown' in ctx.message.content: await ctx.message.channel.set_permissions(ctx.message.guild.default_role, send_messages=False)
                        await ctx.send(str(self.client.get_emoji(BotEmotes.success)) +f' | Success! <#{ctx.message.channel.id}>\'s {str(ctx.message.content).split(" ")[0][1:]} has been {args[0]}d!')
                    except Exception as e:
                        await ctx.send(str(self.client.get_emoji(BotEmotes.error)) +f' | For some reason, i cannot change <#{ctx.message.channel.id}>\'s :(\n\n```{e}```')

    @command('roles,serverroles,serverchannels,channels')
    @cooldown(5)
    async def channel(self, ctx):
        total = []
        if 'channel' in ctx.message.content:
            for i in ctx.message.guild.channels: total.append('<#'+str(i.id)+'>')
        else:
            for i in ctx.message.guild.roles: total.append('<@&'+str(i.id)+'>')
        await ctx.send(embed=discord.Embed(description=myself.dearray(total), color=discord.Color.from_rgb(201, 160, 112)))

    @command('ui,user,usercard,user-info,user-card')
    @cooldown(5) # roles user ava bg
    async def userinfo(self, ctx, *args):
        guy, ava, nitro = myself.getUser(ctx, args), myself.getUserAvatar(ctx, args), False
        async with ctx.message.channel.typing():
            if guy.id in [i.id for i in ctx.guild.premium_subscribers]: nitro = True
            elif guy.is_avatar_animated(): nitro = True
            bg_col = tuple(self.canvas.get_accent(ava))
            data = self.canvas.usercard([{
                'name': i.name, 'color': i.color.to_rgb()
            } for i in guy.roles][::-1][0:5], guy, ava, bg_col, nitro)
            await ctx.send(file=discord.File(data, str(guy.discriminator)+'.png'))

    @command('av,ava')
    @cooldown(1)
    async def avatar(self, ctx, *args):
        url = myself.getUserAvatar(ctx, args, allowgif=True)
        embed = discord.Embed(title='look at dis avatar', color=discord.Colour.from_rgb(201, 160, 112))
        embed.set_image(url=url)
        await ctx.send(embed=embed)

    @command('serveremotes,emotelist,emojilist,emotes,serveremoji')
    @cooldown(10)
    async def serveremojis(self, ctx):
        if len(ctx.guild.emojis)==0: await ctx.send(str(self.client.get_emoji(BotEmotes.error))+' | This server has no emojis!')
        else:
            try:
                await ctx.send(myself.dearray([str(i) for i in ctx.guild.emojis]))
            except:
                await ctx.send(str(self.client.get_emoji(BotEmotes.error))+' | This server probably has too many emojis to be listed!')

    @command('serverinfo,server,servericon,si,server-info')
    @cooldown(10)
    async def servercard(self, ctx):
        if 'servericon' in ctx.message.content:
            if ctx.message.guild.is_icon_animated(): link = 'https://cdn.discordapp.com/icons/'+str(ctx.message.guild.id)+'/'+str(ctx.message.guild.icon)+'.gif?size=1024'
            else: link = 'https://cdn.discordapp.com/icons/'+str(ctx.message.guild.id)+'/'+str(ctx.message.guild.icon)+'.png?size=1024'
            theEm = discord.Embed(title=ctx.message.guild.name+'\'s Icon', url=link, colour=discord.Colour.from_rgb(201, 160, 112))
            theEm.set_image(url=link)
            await ctx.send(embed=theEm)
        else:
            if len(ctx.guild.members)>100:
                wait = await ctx.send('{} | Fetching guild data... please wait...'.format(self.client.get_emoji(BotEmotes.loading)))
                im = self.canvas.server(ctx.guild)
                await wait.delete()
            else:
                await ctx.channel.trigger_typing()
                im = self.canvas.server(ctx.guild)
            await ctx.send(file=discord.File(im, 'server.png'))
    
    @command('bots,serverbots,server-bots')
    @cooldown(5)
    async def botmembers(self, ctx):
        botmembers, off, on, warning = "", 0, 0, 'Down triangles means that the bot is down. And up triangles mean the bot is well... up.'
        for i in range(0, int(len(ctx.message.guild.members))):
            if i > 20: break
            if len(botmembers)>1900:
                warning = str(self.client.get_emoji(BotEmotes.error)) + ' | Error: Too many bots, some bot are not listed above.'
                break
            if ctx.message.guild.members[i].bot==True:
                if str(ctx.message.guild.members[i].status)=='offline':
                    off += 1
                    botmembers += ':small_red_triangle_down: '+ ctx.message.guild.members[i].name + '\n'
                else:
                    on += 1
                    botmembers += ':small_red_triangle: ' + ctx.message.guild.members[i].name + '\n'
        embed = discord.Embed( title = 'Bot members of '+ctx.message.guild.name+':', description = '**Online: '+str(on)+' ('+str(round(on/(off+on)*100))+'%)\nOffline: '+str(off)+' ('+str(round(off/(off+on)*100))+'%)**\n\n'+str(botmembers), colour = discord.Colour.from_rgb(201, 160, 112))
        embed.set_footer(text=warning)
        await ctx.send(embed=embed)

    @command('serverinvite,create-invite,createinvite,makeinvite,make-invite,server-invite')
    @cooldown(30)
    async def getinvite(self, ctx):
        if not ctx.message.author.guild_permissions.create_instant_invite:
            await ctx.send(str(self.client.get_emoji(BotEmotes.error))+' | No create invite permission?')
        else:
            serverinvite = await ctx.message.channel.create_invite(reason='Requested by '+str(ctx.message.author.name))
            await ctx.send(str(self.client.get_emoji(BotEmotes.success))+' | New invite created! Link: **'+str(serverinvite)+'**')

    @command('id')
    @cooldown(2)
    async def _id(self, ctx, *args):
        if '<#' in ''.join(list(args)): total = str('Channel ID: ')+str(''.join(list(args)).split('<#')[1].split('>')[0])
        elif '<@&' in ''.join(list(args)): total = str('Role ID: ')+str(''.join(list(args)).split('<@&')[1].split('>')[0])
        elif len(ctx.message.mentions)!=0: await ctx.send(ctx.message.mentions[0].id)
        else: total = str(self.client.get_emoji(BotEmotes.error))+' | No ID\'s found.'
        await ctx.send(total)

    @command()
    @cooldown(7)
    async def roleinfo(self, ctx, *args):
        if len(list(args))==0:
            await ctx.send(str(self.client.get_emoji(BotEmotes.error))+" | Please send a role name or a role mention! (don\'t)")
        else:
            data = None
            if '<@&' in ''.join(list(args)):
                data = ctx.message.guild.get_role(int(str(ctx.message.content).split('<@&')[1].split('>')[0]))
            else:
                for i in ctx.message.guild.roles:
                    if ' '.join(list(args)).lower()==str(i.name).lower(): data = i ; break
            if data==None:
                await ctx.send(str(self.client.get_emoji(BotEmotes.error))+' | Role not found!')
            else:
                if data.permissions.administrator: perm = ':white_check_mark: Server Administrator'
                else: perm = ':x: Server Administrator'
                if data.mentionable==True: men = ':warning: You can mention this role and they can get pinged.'
                else: men = ':v: You can mention this role and they will not get pinged! ;)'
                embedrole = discord.Embed(title='Role info for role: '+str(data.name), description='**Role ID: **'+str(data.id)+'\n**Role created at: **'+myself.time_encode(round(t.now().timestamp()-data.created_at.timestamp()))+' ago\n**Role position: **'+str(data.position)+'\n**Members having this role: **'+str(len(data.members))+'\n'+str(men)+'\nPermissions Value: '+str(data.permissions.value)+'\n'+str(perm), colour=data.colour)
                embedrole.add_field(name='Role Colour', value='**Color hex: **#'+str(myself.tohex(data.color.value))+'\n**Color integer: **'+str(data.color.value)+'\n**Color RGB: **'+str(myself.dearray(
                    [str(i) for i in list(data.color.to_rgb())]
                )))
                await ctx.send(embed=embedrole)

    @command('perms,perm,permission,permfor,permsfor,perms-for,perm-for')
    @cooldown(15)
    async def permissions(self, ctx):
        if len(ctx.message.mentions)==0: source = ctx.message.author
        else: source = ctx.message.mentions[0]
        perms_list = []
        for i in dir(source.guild_permissions):
            if str(i).startswith('__'): continue
            data = eval('source.guild_permissions.{}'.format(i))
            if str(type(data))=="<class 'bool'>":
                if data: perms_list.append(':white_check_mark: {}'.format(i.replace('_', ' ')))
                else: perms_list.append(':x: {}'.format(i.replace('_', ' ')))
        embed = discord.Embed(title='Guild permissions for '+source.name, description='\n'.join(perms_list), colour=discord.Colour.from_rgb(201, 160, 112))
        await ctx.send(embed=embed)

    @command('mkchannel,mkch,createchannel,make-channel,create-channel')
    @cooldown(5)
    async def makechannel(self, ctx, *args):
        if len(list(args))<2:
            await ctx.send(str(self.client.get_emoji(BotEmotes.error))+' | Please send me an args or something!')
        else:
            begin = True
            if list(args)[0].lower()!='voice':
                if list(args)[0].lower()!='text':
                    await ctx.send(str(self.client.get_emoji(BotEmotes.error))+" | Please use 'text' or 'channel'!")
                    begin = False
            if begin:
                name = str(ctx.message.content).split(' ')[2:len(str(ctx.message.content).split())].replace(' ', '-')
                if list(args)[0].lower()=='voice': await ctx.message.guild.create_voice_channel(name)
                else: await ctx.message.guild.create_voice_channel(name)

    @command('nickname')
    @cooldown(10)
    async def nick(self, ctx, *args):
        if len(list(args))<2:
            await ctx.send(str(self.client.get_emoji(BotEmotes.error))+" | Invalid args!")
        else:
            if not ctx.message.author.guild_permissions.change_nickname:
                await ctx.send(str(self.client.get_emoji(BotEmotes.error))+" | Invalid permissions! You need the change nickname permission to do this")
            else:
                if len(ctx.message.mentions)==0 or not list(args)[0].startswith('<@'):
                    await ctx.send(str(self.client.get_emoji(BotEmotes.error))+" | Go mention someone!")
                else:
                    try:
                        newname = ' '.join(list(args)).split('> ')[1]
                        await ctx.message.mentions[0].edit(nick=newname)
                        await ctx.send(str(self.client.get_emoji(BotEmotes.success))+" | Changed the nickname to {}!".format(newname))
                    except:
                        await ctx.send(str(self.client.get_emoji(BotEmotes.error))+" | Try making my role higher than the person you are looking for!")

    @command('emoji')
    @cooldown(5)
    async def emojiinfo(self, ctx, *args):
        try:
            erry, emojiid = int(list(args)[0].split(':')[2][:-1]), False
            data = self.client.get_emoji(emojiid)
        except:
            erry = True
            await ctx.send(str(self.client.get_emoji(BotEmotes.error))+' | For some reason, we cannot process your emoji ;(')
        if not erry:
            if data.animated: anim = 'This emoji is an animated emoji. **Only nitro users can use it.**'
            else: anim = 'This emoji is a static emoji. **Everyone can use it (except if limited by role)**'
            embedy = discord.Embed(title='Emoji info for :'+str(data.name)+':', description='**Emoji name:** '+str(data.name)+'\n**Emoji ID: **'+str(data.id)+'\n'+anim+'\n**Emoji\'s server ID: **'+str(data.guild_id)+'\n**Emoji creation time: **'+str(data.created_at)[:-7]+' UTC.', colour=discord.Colour.from_rgb(201, 160, 112))
            embedy.set_thumbnail(url='https://cdn.discordapp.com/emojis/'+str(data.id)+'.png?v=1')
            await ctx.send(embed=embedy)

    @command()
    @cooldown(12)
    async def reactnum(self, ctx, *args):
        if len(list(args))==0: await ctx.send(str(self.client.get_emoji(BotEmotes.error))+' | Oops! Not a valid arg!')
        else:
            num = [int(i) for i in list(args) if i.isnumeric()]
            if len(num)!=2: await ctx.send(str(self.client.get_emoji(BotEmotes.error))+' | Oops! Not a valid arg!\n Do something like'+Config.prefix+'reactnum 0 9')
            elif len([True for i in num
            [0:1] if i not in list(range(0, 10))])!=0:
                await ctx.send(str(self.client.get_emoji(BotEmotes.error))+' | The valid range is from 0 to 9!')
            else:
                if num[1] > num[0]: num = num[::-1]
                for i in range(num[0], num[1]):
                    await ctx.message.add_reaction(num2word(i))

    @command('createchannel,create-channel,mc')
    @cooldown(10)
    async def makechannel(self, ctx, *args):
        if len(list(args))<2:
            await ctx.send(str(self.client.get_emoji(BotEmotes.error))+' | Oops! Not a valid arg!')
        else:
            if list(args)[0].lower()!='text' or list(args)[0].lower()!='voice':
                await ctx.send(str(self.client.get_emoji(BotEmotes.error))+' | Oops! Not a valid type of channel!')
            else:
                names = list(args)[1:len(list(args))]
                if list(args)[0].lower()=='text': await ctx.message.guild.create_text_channel(name='-'.join(list(names)))
                else: await ctx.message.guild.create_voice_channel(name='-'.join(names))
                await ctx.send(str(self.client.get_emoji(BotEmotes.success))+" | Successfully created a {} channel named {}.".format(list(args)[0], str('-'.join(names))))
def setup(client):
    client.add_cog(moderation(client))