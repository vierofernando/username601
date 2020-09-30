import discord
from discord.ext import commands
import sys
import time
import random
import asyncio
from os import getcwd, name, environ
sys.path.append(environ['BOT_MODULES_DIR'])
from aiohttp import ClientSession
from decorators import command, cooldown
from datetime import datetime as t
# import Dashboard

class moderation(commands.Cog):
    def __init__(self, client):
        self.client = client
        self.session = ClientSession()

    @command('jp,joinpos,joindate,jd,howold')
    @cooldown(5)
    async def joinposition(self, ctx, *args):
        current_time = t.now().timestamp()
        user = self.client.utils.getUser(ctx, args)
        wait = await ctx.send('{} | Iterating through {} members...'.format(self.client.utils.emote(self.client, 'loading'), len(ctx.guild.members)))
        sortedJoins = sorted([current_time - i.joined_at.timestamp() for i in ctx.guild.members])[::-1]
        num, users = [i for i in range(len(sortedJoins)) if (current_time - user.joined_at.timestamp())==sortedJoins[i]][0], []
        for i in range(-10, 11):
            try:
                placement = (num + i) + 1
                if placement < 1: continue
                locate = sortedJoins[num + i]
                username = [str(i) for i in ctx.guild.members if (current_time- i.joined_at.timestamp())==locate][0].replace('`', '\`').replace('_', '\_').replace('*', '\*').replace('|', '\|')
                if i == 0:
                    username = f'__**{username}**__'
                    placement = f'__**{str(placement)}**__'
                users.append({
                    'user': username,
                    'time': locate,
                    'order': str(placement)
                })
            except IndexError:
                pass
        em = discord.Embed(title='{}\' join position'.format(user.name), description='\n'.join([
            '{}. {} ({} ago)'.format(i['order'], i['user'], self.client.utils.time_encode(round(i['time']))) for i in users
        ]), color=self.client.utils.get_embed_color())
        await wait.edit(content='', embed=em)

    @command('serverconfig,configuration,serversettings,settings')
    @cooldown(1)
    async def config(self, ctx):
        data = self.client.db.Dashboard.getData(ctx.guild.id)
        if data==None: return await ctx.send('{} | This server does not have any configuration for this bot.'.format(self.client.utils.emote(self.client, 'error')))
        autorole = 'Set to <@&{}>'.format(data['autorole']) if data['autorole']!=None else '<Not set>'
        welcome = 'Set to <#{}>'.format(data['welcome']) if data['welcome']!=None else '<Not set>'
        starboard = 'Set to <#{}> (with {} reactions required)'.format(data['starboard'], data['star_requirements']) if data['starboard']!=None else '<Not set>'
        mute = 'Set to <@&{}>'.format(data['mute']) if data['mute']!=None else '<Not set>'
        extras = [len(data['shop']), len(data['warns'])]
        dehoister = 'Enabled :white_check_mark:' if data['dehoister'] else 'Disabled :x:'
        subs = 'Enabled :white_check_mark:' if data['subscription']!=None else 'Disabled :x:'
        await ctx.send(embed=discord.Embed(title=f'{ctx.guild.name}\'s configuration', description=f'**Auto role:** {autorole}\n**Welcome channel:** {welcome}\n**Starboard channel: **{starboard}\n**Name/nick dehoister: **{dehoister}\n**Mute role: **{mute}\n**Members warned: **{extras[1]}\n**Shop products sold: **{extras[0]}\n**Development updates/Events subscription: {subs}**', color=self.client.utils.get_embed_color()).set_thumbnail(url=ctx.guild.icon_url))

    @command()
    @cooldown(5)
    async def mute(self, ctx, *args):
        toMute = self.client.utils.getUser(ctx, args, allownoargs=False)
        if not ctx.author.guild_permissions.manage_messages: return await ctx.send('{} | No `manage messages` permission!'.format(self.client.utils.emote(self.client, 'error')))
        role = self.client.db.Dashboard.getMuteRole(ctx.guild.id)
        if role==None:
            await ctx.send('{} | Please wait... Setting up...\nThis may take a while if your server has a lot of channels.'.format(self.client.utils.emote(self.client, 'loading')))
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
            self.client.db.Dashboard.editMuteRole(ctx.guild.id, role.id)
            role = role.id
        role = ctx.guild.get_role(role)
        try:
            await toMute.add_roles(role)
            await ctx.send('{} | Muted. Ductaped {}\'s mouth.'.format(self.client.utils.emote(self.client, 'success'), toMute.name))
        except Exception as e:
            print(e)
            await ctx.send('{} | I cannot mute him... maybe i has less permissions than him.\nHis mouth is too powerful.'.format(self.client.utils.emote(self.client, 'error')))
    
    @command()
    @cooldown(5)
    async def unmute(self, ctx, *args):
        toUnmute = self.client.utils.getUser(ctx, args, allownoargs=False)
        roleid = self.client.db.Dashboard.getMuteRole(ctx.guild.id)
        if roleid==None: return await ctx.send('{} | He is not muted!\nOr maybe you muted this on other bot... which is not compatible.'.format(self.client.utils.emote(self.client, 'error')))
        elif roleid not in [i.id for i in ctx.message.mentions[0].roles]:
            return await ctx.send('{} | That guy is not muted.'.format(self.client.utils.emote(self.client, 'error')))
        try:
            await toUnmute.remove_roles(ctx.guild.get_role(roleid))
            await ctx.send('{} | {} unmuted.'.format(self.client.utils.emote(self.client, 'success'), toUnmute.name))
        except:
            await ctx.send('{} | I cannot unmute {}!'.format(self.client.utils.emote(self.client, 'error'), ctx.message.mentions[0].name))

    @command('dehoist')
    @cooldown(10)
    async def dehoister(self, ctx, *args):
        if not ctx.author.guild_permissions.manage_nicknames: return await ctx.send('{} | You need the `Manage Nicknames` permissions!'.format(self.client.utils.emote(self.client, 'error')))
        data = self.client.db.Dashboard.getDehoister(ctx.guild.id)
        if not data: 
            self.client.db.Dashboard.setDehoister(ctx.guild, True)
            return await ctx.send(embed=discord.Embed(
                title='Activated dehoister.',
                description=f'**What is dehoister?**\nDehoister is an automated part of this bot that automatically renames someone that tries to hoist their name (for example: `!ABC`)\n\n**How do i deactivate this?**\nJust type `{self.client.utils.prefix}dehoister`.\n\n**It doesn\'t work for me!**\nMaybe because your role position is higher than me, so i don\'t have the permissions required.',
                color=self.client.utils.get_embed_color()
            ))
        self.client.db.Dashboard.setDehoister(ctx.guild, False)
        await ctx.send('{} | Dehoister deactivated.'.format(self.client.utils.emote(self.client, 'success')))

    @command()
    @cooldown(10)
    async def starboard(self, ctx, *args):
        wait = await ctx.send('{} | Please wait...'.format(
            self.client.utils.emote(self.client, 'error')
        ))
        if not ctx.author.guild_permissions.manage_channels:
            return await wait.edit(content='{} | You need the `Manage channels` permission.'.format(
                self.client.utils.emote(self.client, 'error')
            ))
        starboard_channel = self.client.db.Dashboard.getStarboardChannel(ctx.guild)
        if len(list(args))==0:
            if starboard_channel['channelid']==None:
                channel = await ctx.guild.create_text_channel(name='starboard', topic='Server starboard channel. Every funny/cool posts will be here.')
                self.client.db.Dashboard.addStarboardChannel(channel, 1)
                success = self.client.utils.emote(self.client, 'success')
                return await wait.edit(content=f'{success} | OK. Created a channel <#{str(channel.id)}>. Every starboard will be set there.\nTo remove starboard, type `{self.client.utils.prefix}starboard remove`.\nBy default, starboard requirements are set to 1 reaction. To increase, type `{self.client.utils.prefix}starboard limit <number>`.')
            return await wait.edit(content='', embed=discord.Embed(
                title=f'Starboard for {ctx.guild.name}',
                description='Channel: <#{}>\nStars required to reach: {}'.format(
                    starboard_channel['channelid'], starboard_channel['starlimit']
                ), color=self.client.utils.get_embed_color()
            ))
        if starboard_channel['channelid']==None: return
        elif list(args)[0].lower().startswith('rem'):
            self.client.db.Dashboard.removeStarboardChannel(ctx.guild)
            return await wait.edit(content='{} | OK. Starboard for this server is deleted.'.format(self.client.utils.emote(self.client, 'success')))
        elif list(args)[0].lower()=='limit':
            try:
                num = int(list(args)[1])
                if not num in range(1, 20):
                    return await wait.edit(content='{} | Invalid number.'.format(self.client.utils.emote(self.client, 'error')))
                self.client.db.Dashboard.setStarboardLimit(num, ctx.guild)
                await wait.edit(content='{} | Set the limit to {} reactions.'.format(self.client.utils.emote(self.client, 'success'), str(num)))
            except:
                await wait.edit(content='{} | Invalid number.'.format(self.client.utils.emote(self.client, 'error')))

    @command()
    @cooldown(10)
    async def serverstats(self, ctx):
        await ctx.send(file=discord.File(
            self.client.canvas.serverstats(ctx.guild), "serverstats.png"
        ))
    
    @command()
    @cooldown(5)
    async def warn(self, ctx, *args):
        if len(ctx.message.mentions)==0:
            return await ctx.send('{} | Mention someone.'.format(self.client.utils.emote(self.client, 'error')))
        elif ctx.message.mentions[0].id == ctx.author.id:
            return await ctx.send(':joy: | Warning yourself? Really?')
        elif not ctx.author.guild_permissions.manage_messages:
            return await ctx.send('{} | You need to have manage messages permissions to do this man. Sad.'.format(self.client.utils.emote(self.client, 'error')))
        reason = 'No reason provided' if (len(list(args))<2) else ' '.join(list(args)[1:len(list(args))])
        if len(reason)>100: return await ctx.send('{} | Your reason is toooo longgg!'.format(
            self.client.utils.emote(self.client, 'error')
        ))
        warned = self.client.db.Dashboard.addWarn(ctx.message.mentions[0], ctx.author, reason)
        if warned:
            error = self.client.utils.emote(self.client, 'success')
            return await ctx.send(f'{success} | {ctx.message.mentions[0].name}#{ctx.message.mentions[0].discriminator} was warned by {ctx.author.name}#{ctx.author.discriminator} for the reason *"{reason}"*.')
        error = self.client.utils.emote(self.client, 'error')
        await ctx.send(f'{error} | An error occurred.')
    
    @command('warns,warnslist,warn-list,infractions')
    @cooldown(5)
    async def warnlist(self, ctx):
        source = ctx.author if (len(ctx.message.mentions)==0) else ctx.message.mentions[0]
        data = self.client.db.Dashboard.getWarns(source)
        if data==None:
            error = self.client.utils.emote(self.client, 'error')
            return await ctx.send(f'{error} | Good news! {source.name} does not have any warns!')
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
        error = self.client.utils.emote(self.client, 'success')
        if not ctx.author.guild_permissions.manage_messages: return await ctx.send(f'{error} | You need the `Manage messages` permissions to unwarn someone.')
        if len(ctx.message.mentions)==0: return await ctx.send('{} | Please TAG someone !!!'.format(
            self.client.utils.emote(self.client, 'error')
        ))
        unwarned = self.client.db.Dashboard.clearWarn(ctx.message.mentions[0])
        if unwarned: return await ctx.send(f'{error} | Successfully unwarned {ctx.message.mentions[0].name}.')
        await ctx.send(f'{error} | An error occurred.')

    @command('welcomelog,setwelcome')
    @cooldown(15)
    async def welcome(self, ctx, *args):
        if not ctx.author.guild_permissions.manage_channels:
            await ctx.send("{} | You need the `Manage Channels` permission!".format(self.client.utils.emote(self.client, 'error')))
        else:
            if len(list(args))==0:
                await ctx.send(embed=discord.Embed(
                    title='Command usage',
                    description='{}welcome <CHANNEL>\n{}welcome disable'.format(self.client.utils.prefix, self.client.utils.prefix),
                    color=self.client.utils.get_embed_color()
                ))
            else:
                if list(args)[0].lower()=='disable':
                    self.client.db.Dashboard.set_welcome(ctx.guild.id, None)
                    await ctx.send("{} | Welcome disabled!".format(self.client.utils.emote(self.client, 'success')))
                else:
                    try:
                        if list(args)[0].startswith("<#") and list(args)[0].endswith('>'): channelid = int(list(args)[0].split('<#')[1].split('>')[0])
                        else: channelid = int([i.id for i in ctx.guild.channels if str(i.name).lower()==str(''.join(list(args))).lower()][0])
                        self.client.db.Dashboard.set_welcome(ctx.guild.id, channelid)
                        await ctx.send("{} | Success! set the welcome log to <#{}>!".format(self.client.utils.emote(self.client, 'success'), channelid))
                    except Exception as e:
                        await ctx.send("{} | Invalid arguments!".format(self.client.utils.emote(self.client, 'error')))
    
    @command('auto-role,welcome-role,welcomerole')
    @cooldown(12)
    async def autorole(self, ctx, *args):
        if not ctx.author.guild_permissions.manage_roles:
            await ctx.send("{} | You need the `Manage Roles` permission!".format(self.client.utils.emote(self.client, 'error')))
        else:
            if len(list(args))==0:
                await ctx.send(embed=discord.Embed(
                    title='Command usage',
                    description='{}autorole <ROLENAME/ROLEPING>\n{}autorole disable'.format(self.client.utils.prefix, self.client.utils.prefix),
                    color=self.client.utils.get_embed_color()
                ))
            else:
                if list(args)[0].lower()=='disable':
                    self.client.db.Dashboard.set_autorole(ctx.guild.id, None)
                    await ctx.send("{} | Autorole disabled!".format(self.client.utils.emote(self.client, 'success')))
                else:
                    try:
                        if list(args)[0].startswith("<@&") and list(args)[0].endswith('>'): roleid = int(list(args)[0].split('<@&')[1].split('>')[0])
                        else: roleid = int([i.id for i in ctx.guild.roles if str(i.name).lower()==str(' '.join(list(args))).lower()][0])
                        self.client.db.Dashboard.set_autorole(ctx.guild.id, roleid)
                        await ctx.send("{} | Success! set the autorole to **{}!**".format(self.client.utils.emote(self.client, 'success'), ctx.guild.get_role(roleid).name))
                    except:
                        await ctx.send("{} | Invalid arguments!".format(self.client.utils.emote(self.client, 'error')))
 
    @command('bigemoji,emojipic,emoji-img')
    @cooldown(3)
    async def emojiimg(self, ctx, *args):
        try:
            em = list(args)[0].lower()
            if em.startswith('<:a:'): _id, an = em.split(':')[3].split('>')[0], True
            else: _id, an = em.split(':')[2].split('>')[0], False
            if an:
                async with self.session.get('https://cdn.discordapp.com/emojis/{}.gif'.format(_id)) as r:
                    res = await r.read()
                    try:
                        return await ctx.send(file=discord.File(fp=res, filename='emoji.gif'))
                    except:
                        return await ctx.send('{} | The emoji file size is too big!'.format(self.client.utils.emotes(self.client, 'error')))
            else: await ctx.send(file=discord.File(self.client.canvas.urltoimage('https://cdn.discordapp.com/emojis/{}.png'.format(_id)), 'emoji.png'))
        except:
            await ctx.send(self.client.utils.emote(self.client, 'error')+' | Invalid emoji.')
            

    @command()
    @cooldown(10)
    async def rolecolor(self, ctx, *args):
        unprefixed = ' '.join(list(args))
        if len(unprefixed.split('#'))==1:
            await ctx.send(f'Please provide a hex!\nExample: `{self.client.utils.prefix}rolecolor {random.choice(ctx.guild.roles).name}` #ff0000')
        else:
            if ctx.author.guild_permissions.manage_roles==False:
                await ctx.send(self.client.utils.emote(self.client, 'error') +' | You need the `MANAGE ROLES` permission to change role colors!')
            else:
                role = None
                for i in ctx.guild.roles:
                    if unprefixed.split('#')[0][:-1].lower()==str(i.name).lower():
                        print(unprefixed.split('#')[0][:-1].lower())
                        role = i
                        break
                if role==None:
                    await ctx.send(self.client.utils.emote(self.client, 'error') +' | Invalid role input! :(')
                else:
                    try:
                        colint = self.client.utils.toint(unprefixed.split('#')[1].lower())
                        await role.edit(colour=discord.Colour(colint))
                        await ctx.send('Color of '+role.name+' role has been changed.', delete_after=5)
                    except Exception as e:
                        await ctx.send(self.client.utils.emote(self.client, 'error') + f' | An error occurred while editing role:```{e}```')
    
    @command()
    @cooldown(10)
    async def slowmode(self, ctx, *args):
        if len(list(args))==0: await ctx.send(self.client.utils.emote(self.client, 'error')+" | How long in seconds?")
        else:
            cd = list(args)[0]
            if ctx.author.guild_permissions.manage_channels:
                if not cd.isnumeric():
                    await ctx.send(self.client.utils.emote(self.client, 'error')+" | That cooldown is not a number!")
                else:
                    if int(cd)<0:
                        await ctx.send(self.client.utils.emote(self.client, 'error')+" | Minus slowmode? Did you mean slowmode 0 seconds?")
                    elif int(cd)>21600:
                        await ctx.send(self.client.utils.emote(self.client, 'error')+" | That is too hecking sloow....")
                    else:
                        await ctx.channel.edit(slowmode_delay=cd)
                        await ctx.send(self.client.utils.emote(self.client, 'success')+" | Channel slowmode cooldown has been set to "+str(self.client.utils.time_encode(int(cd))))
            else: await ctx.send(self.client.utils.emote(self.client, 'error')+" | You need the manage channels permission to do this command!")

    @command('addrole,add-role')
    @cooldown(10)
    async def ar(self, ctx, *args):
        args = list(args)
        if not ctx.author.guild_permissions.manage_roles:
            await ctx.send(self.client.utils.emote(self.client, 'error') +f' | <@{str(ctx.author.id)}>, you don\'t have the `Manage Roles` permission!')
        else:
            try:
                toadd = None
                if '<@&' in ''.join(args):
                    toadd = ctx.guild.get_role(int(''.join(args).split('<@&')[1].split('>')[0]))
                else:
                    for i in ctx.guild.roles:
                        if str(i.name).lower()==str(ctx.message.content).split('> ')[1].lower():
                            toadd = ctx.guild.get_role(i.id)
                            break
                if toadd==None:
                    await ctx.send(self.client.utils.emote(self.client, 'error')+" | Invalid input!")
                else:
                    aruser = ctx.message.mentions[0]
                    await aruser.add_roles(toadd)
                    await ctx.send('Congratulations, '+aruser.name+', you now have the '+toadd.name+' role! :tada:')
            except IndexError:
                await ctx.send(self.client.utils.emote(self.client, 'error')+" | Invalid arguments!")
    
    @command('removerole,remove-role')
    @cooldown(10)
    async def rr(self, ctx, *args):
        args = list(args)
        if not ctx.author.guild_permissions.manage_roles:
            await ctx.send(self.client.utils.emote(self.client, 'error') +f' | <@{str(ctx.author.id)}>, you don\'t have the `Manage Roles` permission!')
        else:
            try:
                toadd = None
                if '<@&' in ''.join(args):
                    toadd = ctx.guild.get_role(int(''.join(args).split('<@&')[1].split('>')[0]))
                else:
                    for i in ctx.guild.roles:
                        if str(i.name).lower()==str(ctx.message.content).split('> ')[1].lower():
                            toadd = ctx.guild.get_role(i.id)
                            break
                if toadd==None:
                    await ctx.send(self.client.utils.emote(self.client, 'error')+" | Invalid input!")
                else:
                    rruser = ctx.message.mentions[0]
                    await rruser.remove_roles(toadd)
                    await ctx.send(rruser.name+', you lost the '+toadd.name+' role... :pensive:')
            except IndexError:
                await ctx.send(self.client.utils.emote(self.client, 'error')+" | Invalid arguments!")

    @command('kick')
    @cooldown(10)
    async def ban(self, ctx, *args):
        if len(list(args))==0:
            await ctx.send(self.client.utils.emote(self.client, 'error')+" | Nope. No arguments means no moderation:tm:.")
        elif len(ctx.message.mentions)==0:
            await ctx.send(self.client.utils.emote(self.client, 'error')+" | Nope. No tagging means no moderation:tm:.")
        else:
            accept = True
            if 'kick' in ctx.message.content:
                if not ctx.author.guild_permissions.kick_members:
                    await ctx.send(self.client.utils.emote(self.client, 'error')+" | No kick members permission?")
                    accept = False
            else:
                if not ctx.author.guild_permissions.ban_members:
                    await ctx.send(self.client.utils.emote(self.client, 'error')+" | No ban members permission?")
                    accept = False
            if ctx.guild.owner.id!=ctx.author.id:
                if ctx.message.mentions[0].guild_permissions.administrator==True:
                    await ctx.send(self.client.utils.emote(self.client, 'error')+" | Nope, that guy probably has higher permissions than you.")
                    accept = False
                elif ctx.message.mentions[0].roles[::-1][0].position>ctx.guild.get_member(self.client.user.id).roles[::-1][0].position:
                    await ctx.send(self.client.utils.emote(self.client, 'error')+" | Try moving my role higher than "+ctx.message.mentions[0].name+"'s role.")
            if accept:
                if 'kick' in ctx.message.content:
                    await ctx.guild.kick(ctx.message.mentions[0])
                    await ctx.send(self.client.utils.emote(self.client, 'success')+" | Successfully kicked "+ctx.message.mentions[0].name+".")
                else:
                    await ctx.guild.ban(ctx.message.mentions[0])
                    await ctx.send(self.client.utils.emote(self.client, 'success')+" | Successfully banned "+ctx.message.mentions[0].name+".")
    @command('purge')
    @cooldown(2)
    async def clear(self, ctx, *args):
        if not ctx.author.guild_permissions.manage_channels:
            await ctx.send(self.client.utils.emote(self.client, 'error')+" | You need the manage channel permission!")
        else:
            if len(list(args))==0:
                await ctx.send(self.client.utils.emote(self.client, 'error')+" | How many messages to be purged?")
            else:
                if len(ctx.message.mentions)==0:
                    if not list(args)[0].isnumeric():
                        await ctx.send(self.client.utils.emote(self.client, 'error')+" | Not a number!")
                    else:
                        if int(list(args)[0])<0:
                            await ctx.send(self.client.utils.emote(self.client, 'error')+" | Minus?")
                        elif int(list(args)[0])>250:
                            await ctx.send(self.client.utils.emote(self.client, 'error')+" | Too much! Use clone channel instead!")
                        else:
                            topurge = int(list(args)[0])+1
                            await ctx.channel.purge(limit=topurge)
                            await ctx.send(self.client.utils.emote(self.client, 'success')+" | Done! {} messages has been cleared!".format(str(list(args)[0])), delete_after=3)
                else:
                    def check(m):
                        return m.author.id == ctx.message.mentions[0].id
                    dels = await ctx.channel.purge(check=check, limit=500)
                    await ctx.send(self.client.utils.emote(self.client, 'success')+' | Done. Cleared '+str(len(dels))+' message by <@'+str(ctx.message.mentions[0].id)+'>.', delete_after=3)
    @command('hidechannel')
    @cooldown(5)
    async def lockdown(self, ctx, *args):
        if len(list(args))==0: await ctx.send(self.client.utils.emote(self.client, 'error') +f' | Invalid parameters. Correct Example: `{self.client.utils.prefix}{args[0][1:]} [disable/enable]`')
        else:
            accept = True
            if not ctx.author.guild_permissions.administrator: await ctx.channel.send(self.client.utils.emote(self.client, 'error')+' | You need the `Administrator` permission to do this, unless you are trying to mute yourself.')
            else:
                if 'enable' not in args[0].lower():
                    if 'disable' not in args[0].lower():
                        await ctx.send(self.client.utils.emote(self.client, 'error')+' | Oops! Please type `enable` or `disable`.')
                        accept = False
                if accept:
                    try:
                        if args[0].lower()=='disable':
                            if 'hidechannel' in ctx.message.content: await ctx.channel.set_permissions(ctx.guild.default_role, read_messages=True)
                            if 'lockdown' in ctx.message.content: await ctx.channel.set_permissions(ctx.guild.default_role, send_messages=True)
                        elif args[0].lower()=='enable':
                            if 'hidechannel' in ctx.message.content: await ctx.channel.set_permissions(ctx.guild.default_role, read_messages=False)
                            if 'lockdown' in ctx.message.content: await ctx.channel.set_permissions(ctx.guild.default_role, send_messages=False)
                        await ctx.send(self.client.utils.emote(self.client, 'success') +f' | Success! <#{ctx.channel.id}>\'s {str(ctx.message.content).split(" ")[0][1:]} has been {args[0]}d!')
                    except Exception as e:
                        await ctx.send(self.client.utils.emote(self.client, 'error') +f' | For some reason, i cannot change <#{ctx.channel.id}>\'s :(\n\n```{e}```')

    @command('roles,serverroles,serverchannels,channels')
    @cooldown(5)
    async def channel(self, ctx):
        total = []
        if 'channel' in ctx.message.content:
            for i in ctx.guild.channels: total.append('<#'+str(i.id)+'>')
        else:
            for i in ctx.guild.roles: total.append('<@&'+str(i.id)+'>')
        await ctx.send(embed=discord.Embed(description=', '.join(total), color=self.client.utils.get_embed_color()))

    @command('ui,user,usercard,user-info,user-card,whois')
    @cooldown(5)
    async def userinfo(self, ctx, *args):
        guy, ava, nitro = self.client.utils.getUser(ctx, args), self.client.utils.getUserAvatar(ctx, args), False
        async with ctx.channel.typing():
            if guy.id in [i.id for i in ctx.guild.premium_subscribers]: nitro = True
            elif guy.is_avatar_animated(): nitro = True
            booster = True if guy in ctx.guild.premium_subscribers else False
            booster_since = round(t.now().timestamp() - guy.premium_since.timestamp()) if guy.premium_since != None else False
            bg_col = tuple(self.client.canvas.get_accent(ava))
            data = self.client.canvas.usercard([{
                'name': i.name, 'color': i.color.to_rgb()
            } for i in guy.roles][::-1][0:5], guy, ava, bg_col, nitro, booster, booster_since)
            await ctx.send(file=discord.File(data, str(guy.discriminator)+'.png'))

    @command('av,ava')
    @cooldown(1)
    async def avatar(self, ctx, *args):
        url = self.client.utils.getUserAvatar(ctx, args, allowgif=True)
        embed = discord.Embed(title='look at dis avatar', color=self.client.utils.get_embed_color())
        embed.set_image(url=url)
        await ctx.send(embed=embed)

    @command('serveremotes,emotelist,emojilist,emotes,serveremoji')
    @cooldown(10)
    async def serveremojis(self, ctx):
        if len(ctx.guild.emojis)==0: await ctx.send(self.client.utils.emote(self.client, 'error')+' | This server has no emojis!')
        else:
            try:
                await ctx.send(', '.join([str(i) for i in ctx.guild.emojis]))
            except:
                await ctx.send(self.client.utils.emote(self.client, 'error')+' | This server probably has too many emojis to be listed!')

    @command('serverinfo,server,servericon,si,server-info,guild,guildinfo,guild-info')
    @cooldown(10)
    async def servercard(self, ctx, *args):
        if 'servericon' in ctx.message.content:
            if ctx.guild.is_icon_animated(): link = 'https://cdn.discordapp.com/icons/'+str(ctx.guild.id)+'/'+str(ctx.guild.icon)+'.gif?size=1024'
            else: link = 'https://cdn.discordapp.com/icons/'+str(ctx.guild.id)+'/'+str(ctx.guild.icon)+'.png?size=1024'
            theEm = discord.Embed(title=ctx.guild.name+'\'s Icon', url=link, colour=self.client.utils.get_embed_color())
            theEm.set_image(url=link)
            await ctx.send(embed=theEm)
        else:
            if len(list(args))==0:
                if len(ctx.guild.members)>100:
                    wait = await ctx.send('{} | Fetching guild data... please wait...'.format(self.client.utils.emote(self.client, 'loading')))
                    im = self.client.canvas.server(ctx.guild)
                    await wait.delete()
                else:
                    await ctx.channel.trigger_typing()
                    im = self.client.canvas.server(ctx.guild)
                await ctx.send(file=discord.File(im, 'server.png'))
            else:
                data = self.client.utils.fetchJSON(f"https://discord.com/api/v6/invites/{list(args)[0].lower()}?with_counts=true")
                im = self.client.canvas.server(None, data=data['guild'], raw=data)
                await ctx.send(file=discord.File(im, 'server_that_has_some_kewl_vanity_url.png'))

    @command('serverinvite,create-invite,createinvite,makeinvite,make-invite,server-invite')
    @cooldown(30)
    async def getinvite(self, ctx):
        if not ctx.author.guild_permissions.create_instant_invite:
            await ctx.send(self.client.utils.emote(self.client, 'error')+' | No create invite permission?')
        else:
            serverinvite = await ctx.channel.create_invite(reason='Requested by '+str(ctx.author.name))
            await ctx.send(self.client.utils.emote(self.client, 'success')+' | New invite created! Link: **'+str(serverinvite)+'**')

    @command()
    @cooldown(7)
    async def roleinfo(self, ctx, *args):
        if len(list(args))==0:
            await ctx.send(self.client.utils.emote(self.client, 'error')+" | Please send a role name or a role mention! (don\'t)")
        else:
            data = None
            if '<@&' in ''.join(list(args)):
                data = ctx.guild.get_role(int(str(ctx.message.content).split('<@&')[1].split('>')[0]))
            else:
                for i in ctx.guild.roles:
                    if ' '.join(list(args)).lower()==str(i.name).lower(): data = i ; break
            if data==None:
                await ctx.send(self.client.utils.emote(self.client, 'error')+' | Role not found!')
            else:
                if data.permissions.administrator: perm = ':white_check_mark: Server Administrator'
                else: perm = ':x: Server Administrator'
                if data.mentionable==True: men = ':warning: You can mention this role and they can get pinged.'
                else: men = ':v: You can mention this role and they will not get pinged! ;)'
                embedrole = discord.Embed(title='Role info for role: '+str(data.name), description='**Role ID: **'+str(data.id)+'\n**Role created at: **'+self.client.utils.time_encode(round(t.now().timestamp()-data.created_at.timestamp()))+' ago\n**Role position: **'+str(data.position)+'\n**Members having this role: **'+str(len(data.members))+'\n'+str(men)+'\nPermissions Value: '+str(data.permissions.value)+'\n'+str(perm), colour=data.colour)
                embedrole.add_field(name='Role Colour', value='**Color hex: **#'+str(self.client.utils.tohex(data.color.value))+'\n**Color integer: **'+str(data.color.value)+'\n**Color RGB: **'+str(', '.join(
                    [str(i) for i in list(data.color.to_rgb())]
                )))
                await ctx.send(embed=embedrole)

    @command('perms,perm,permission,permfor,permsfor,perms-for,perm-for')
    @cooldown(10)
    async def permissions(self, ctx):
        if len(ctx.message.mentions)==0: source = ctx.author
        else: source = ctx.message.mentions[0]
        perms_list = []
        for i in dir(source.guild_permissions):
            if str(i).startswith('__'): continue
            data = eval('source.guild_permissions.{}'.format(i))
            if str(type(data))=="<class 'bool'>":
                if data: perms_list.append(':white_check_mark: {}'.format(i.replace('_', ' ')))
                else: perms_list.append(':x: {}'.format(i.replace('_', ' ')))
        embed = discord.Embed(title='Guild permissions for '+source.name, description='\n'.join(perms_list), colour=self.client.utils.get_embed_color())
        await ctx.send(embed=embed)

    @command('mkchannel,mkch,createchannel,make-channel,create-channel')
    @cooldown(5)
    async def makechannel(self, ctx, *args):
        if len(list(args))<2:
            await ctx.send(self.client.utils.emote(self.client, 'error')+' | Please send me an args or something!')
        else:
            begin = True
            if list(args)[0].lower()!='voice':
                if list(args)[0].lower()!='text':
                    await ctx.send(self.client.utils.emote(self.client, 'error')+" | Please use 'text' or 'channel'!")
                    begin = False
            if begin:
                name = str(ctx.message.content).split(' ')[2:len(str(ctx.message.content).split())].replace(' ', '-')
                if list(args)[0].lower()=='voice': await ctx.guild.create_voice_channel(name)
                else: await ctx.guild.create_voice_channel(name)

    @command('nickname')
    @cooldown(10)
    async def nick(self, ctx, *args):
        if len(list(args))<2:
            await ctx.send(self.client.utils.emote(self.client, 'error')+" | Invalid args!")
        else:
            if not ctx.author.guild_permissions.change_nickname:
                await ctx.send(self.client.utils.emote(self.client, 'error')+" | Invalid permissions! You need the change nickname permission to do this")
            else:
                if len(ctx.message.mentions)==0 or not list(args)[0].startswith('<@'):
                    await ctx.send(self.client.utils.emote(self.client, 'error')+" | Go mention someone!")
                else:
                    try:
                        newname = ' '.join(list(args)).split('> ')[1]
                        await ctx.message.mentions[0].edit(nick=newname)
                        await ctx.send(self.client.utils.emote(self.client, 'success')+" | Changed the nickname to {}!".format(newname))
                    except:
                        await ctx.send(self.client.utils.emote(self.client, 'error')+" | Try making my role higher than the person you are looking for!")

    @command('emoji')
    @cooldown(5)
    async def emojiinfo(self, ctx, *args):
        try:
            erry, emojiid = int(list(args)[0].split(':')[2][:-1]), False
            data = self.client.get_emoji(emojiid)
        except:
            erry = True
            await ctx.send(self.client.utils.emote(self.client, 'error')+' | For some reason, we cannot process your emoji ;(')
        if not erry:
            if data.animated: anim = 'This emoji is an animated emoji. **Only nitro users can use it.**'
            else: anim = 'This emoji is a static emoji. **Everyone can use it (except if limited by role)**'
            embedy = discord.Embed(title='Emoji info for :'+str(data.name)+':', description='**Emoji name:** '+str(data.name)+'\n**Emoji ID: **'+str(data.id)+'\n'+anim+'\n**Emoji\'s server ID: **'+str(data.guild_id)+'\n**Emoji creation time: **'+str(data.created_at)[:-7]+' UTC.', colour=self.client.utils.get_embed_color())
            embedy.set_thumbnail(url='https://cdn.discordapp.com/emojis/'+str(data.id)+'.png?v=1')
            await ctx.send(embed=embedy)

    @command()
    @cooldown(12)
    async def reactnum(self, ctx, *args):
        if len(list(args))==0: await ctx.send(self.client.utils.emote(self.client, 'error')+' | Oops! Not a valid arg!')
        else:
            num = [int(i) for i in list(args) if i.isnumeric()]
            if len(num)!=2: await ctx.send(self.client.utils.emote(self.client, 'error')+' | Oops! Not a valid arg!\n Do something like'+self.client.utils.prefix+'reactnum 0 9')
            elif len([True for i in num
            [0:1] if i not in list(range(0, 10))])!=0:
                await ctx.send(self.client.utils.emote(self.client, 'error')+' | The valid range is from 0 to 9!')
            else:
                if num[1] > num[0]: num = num[::-1]
                for i in range(num[0], num[1]):
                    await ctx.message.add_reaction(self.client.utils.num2word(i))

    @command('createchannel,create-channel,mc')
    @cooldown(10)
    async def makechannel(self, ctx, *args):
        if len(list(args))<2:
            await ctx.send(self.client.utils.emote(self.client, 'error')+' | Oops! Not a valid argument!')
        else:
            if list(args)[0].lower()!='text' or list(args)[0].lower()!='voice':
                await ctx.send(self.client.utils.emote(self.client, 'error')+' | Oops! Not a valid type of channel!')
            else:
                names = list(args)[1:len(list(args))]
                if list(args)[0].lower()=='text': await ctx.guild.create_text_channel(name='-'.join(list(names)))
                else: await ctx.guild.create_voice_channel(name='-'.join(names))
                await ctx.send(self.client.utils.emote(self.client, 'success')+" | Successfully created a {} channel named {}.".format(list(args)[0], str('-'.join(names))))
def setup(client):
    client.add_cog(moderation(client))