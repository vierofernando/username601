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

class moderation(commands.Cog):
    def __init__(self, client):
        self.client = client
        self.session = ClientSession()

    @command('jp,joinpos,joindate,jd,howold')
    @cooldown(5)
    async def joinposition(self, ctx, *args):
        wait = await ctx.send(f"{self.client.loading_emoji} | Hang tight... collecting data...")
        current_time, members, user_index, desc = t.now().timestamp(), ctx.guild.members, None, ""
        full_arr = [{'ja': i.joined_at.timestamp(), 'da': i} for i in members]
        raw_unsorted_arr = [i['ja'] for i in full_arr]
        sorted_arr = sorted(raw_unsorted_arr)
        if len(args) > 0 and args[0].isnumeric() and ((int(args[0])-1) in range(len(members))):
            user_index, title = int(args[0]) - 1, f'User join position for order: #{args[0]}'
        else:
            user = self.client.utils.getUser(ctx, args)
            user_join_date = user.joined_at.timestamp()
            user_index, title = sorted_arr.index(user_join_date), str(user)+'\'s join position for '+ctx.guild.name
        for i in range(user_index - 10, user_index + 11):
            if i < 0: continue
            try: key = sorted_arr[i]
            except: continue
            index = raw_unsorted_arr.index(key)
            name = str(full_arr[index]['da']).replace('_', '\_').replace('*', '\*').replace('`', '\`')
            string = "{}. {} ({} ago)\n" if i != user_index else "**__{}. {} ({} ago)__**\n"
            desc += string.format(
                i + 1, name, self.client.utils.lapsed_time_from_seconds(current_time - full_arr[index]['ja'])
            )
        return await wait.edit(content='', embed=discord.Embed(title=title, description=desc, color=ctx.guild.me.roles[::-1][0].color))
        
    @command()
    @cooldown(1)
    async def config(self, ctx):
        data = self.client.db.Dashboard.getData(ctx.guild.id)
        if data==None: raise self.client.utils.send_error_message('This server does not have any configuration for this bot.')
        autorole = 'Set to <@&{}>'.format(data['autorole']) if data['autorole']!=None else '<Not set>'
        welcome = 'Set to <#{}>'.format(data['welcome']) if data['welcome']!=None else '<Not set>'
        starboard = 'Set to <#{}> (with {} reactions required)'.format(data['starboard'], data['star_requirements']) if data['starboard']!=None else '<Not set>'
        mute = 'Set to <@&{}>'.format(data['mute']) if data['mute']!=None else '<Not set>'
        extras = [len(data['shop']), len(data['warns'])]
        dehoister = 'Enabled :white_check_mark:' if data['dehoister'] else 'Disabled :x:'
        subs = 'Enabled :white_check_mark:' if data['subscription']!=None else 'Disabled :x:'
        await ctx.send(embed=discord.Embed(title=f'{ctx.guild.name}\'s configuration', description=f'**Auto role:** {autorole}\n**Welcome channel:** {welcome}\n**Starboard channel: **{starboard}\n**Name/nick dehoister: **{dehoister}\n**Mute role: **{mute}\n**Members warned: **{extras[1]}\n**Shop products sold: **{extras[0]}\n**Development updates/Events subscription: {subs}**', color=ctx.guild.me.roles[::-1][0].color).set_thumbnail(url=ctx.guild.icon_url))

    @command()
    @cooldown(5)
    async def mute(self, ctx, *args):
        toMute = self.client.utils.getUser(ctx, args, allownoargs=False)
        if not ctx.author.guild_permissions.manage_messages: raise self.client.utils.send_error_message('No `manage messages` permission!')
        role = self.client.db.Dashboard.getMuteRole(ctx.guild.id)
        if role==None:
            await ctx.send('{} | Please wait... Setting up...\nThis may take a while if your server has a lot of channels.'.format(self.client.loading_emoji))
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
            await ctx.send('{} | Muted. Ductaped {}\'s mouth.'.format(self.client.success_emoji, toMute.name))
        except Exception as e:
            print(e)
            raise self.client.utils.send_error_message('I cannot mute him... maybe i has less permissions than him.\nHis mouth is too powerful.')
    
    @command()
    @cooldown(5)
    async def unmute(self, ctx, *args):
        toUnmute = self.client.utils.getUser(ctx, args, allownoargs=False)
        roleid = self.client.db.Dashboard.getMuteRole(ctx.guild.id)
        if roleid==None: raise self.client.utils.send_error_message('He is not muted!\nOr maybe you muted this on other bot... which is not compatible.')
        elif roleid not in [i.id for i in ctx.message.mentions[0].roles]:
            raise self.client.utils.send_error_message('That guy is not muted.')
        try:
            await toUnmute.remove_roles(ctx.guild.get_role(roleid))
            await ctx.send('{} | {} unmuted.'.format(self.client.success_emoji, toUnmute.name))
        except:
            raise self.client.utils.send_error_message(f'I cannot unmute {toUnmute.name}!')

    @command('dehoist')
    @cooldown(10)
    async def dehoister(self, ctx, *args):
        if not ctx.author.guild_permissions.manage_nicknames: raise self.client.utils.send_error_message('You need the `Manage Nicknames` permissions!')
        data = self.client.db.Dashboard.getDehoister(ctx.guild.id)
        if not data: 
            self.client.db.Dashboard.setDehoister(ctx.guild, True)
            return await ctx.send(embed=discord.Embed(
                title='Activated dehoister.',
                description=f'**What is dehoister?**\nDehoister is an automated part of this bot that automatically renames someone that tries to hoist their name (for example: `!ABC`)\n\n**How do i deactivate this?**\nJust type `{self.client.command_prefix}dehoister`.\n\n**It doesn\'t work for me!**\nMaybe because your role position is higher than me, so i don\'t have the permissions required.',
                color=ctx.guild.me.roles[::-1][0].color
            ))
        self.client.db.Dashboard.setDehoister(ctx.guild, False)
        await ctx.send('{} | Dehoister deactivated.'.format(self.client.success_emoji))

    @command()
    @cooldown(10)
    async def starboard(self, ctx, *args):
        wait = await ctx.send('{} | Please wait...'.format(self.client.loading_emoji))
        if not ctx.author.guild_permissions.manage_channels:
            raise self.client.utils.send_error_message('You need the `Manage channels` permission.')
        starboard_channel = self.client.db.Dashboard.getStarboardChannel(ctx.guild)
        if len(args)==0:
            if starboard_channel['channelid']==None:
                channel = await ctx.guild.create_text_channel(name='starboard', topic='Server starboard channel. Every funny/cool posts will be here.')
                self.client.db.Dashboard.addStarboardChannel(channel, 1)
                success = self.client.success_emoji
                return await wait.edit(content=f'{success} | OK. Created a channel <#{str(channel.id)}>. Every starboard will be set there.\nTo remove starboard, type `{self.client.command_prefix}starboard remove`.\nBy default, starboard requirements are set to 1 reaction. To increase, type `{self.client.command_prefix}starboard limit <number>`.')
            return await wait.edit(content='', embed=discord.Embed(
                title=f'Starboard for {ctx.guild.name}',
                description='Channel: <#{}>\nStars required to reach: {}'.format(
                    starboard_channel['channelid'], starboard_channel['starlimit']
                ), color=ctx.guild.me.roles[::-1][0].color
            ))
        if starboard_channel['channelid']==None: return
        elif args[0].lower()=='remove':
            self.client.db.Dashboard.removeStarboardChannel(ctx.guild)
            return await wait.edit(content='{} | OK. Starboard for this server is deleted.'.format(self.client.success_emoji))
        elif args[0].lower()=='limit':
            try:
                num = int(list(args)[1])
                if not num in range(1, 20):
                    raise self.client.utils.send_error_message('Invalid number.')
                self.client.db.Dashboard.setStarboardLimit(num, ctx.guild)
                await wait.edit(content='{} | Set the limit to {} reactions.'.format(self.client.success_emoji, str(num)))
            except:
                raise self.client.utils.send_error_message('Invalid number.')

    @command()
    @cooldown(10)
    async def serverstats(self, ctx):
        await ctx.send(file=discord.File(
            self.client.canvas.serverstats(ctx.guild), "serverstats.png"
        ))
    
    @command()
    @cooldown(5)
    async def warn(self, ctx, *args):
        params = self.client.utils.split_parameter_to_two(args)
        if not ctx.author.guild_permissions.manage_messages:
            raise self.client.utils.send_error_message('You need to have manage messages permissions to do this man. Sad.')
        elif len(args) == 0: return await ctx.send('{} | Invalid arguments. do `{}warn <userid/username> <reason optional>`')
        user_to_warn = self.client.utils.getUser(ctx, args[0] if params == None else params[0], allownoargs=False)
        if user_to_warn.guild_permissions.manage_channels: raise self.client.utils.send_error_message("You cannot warn a moderator.")
        reason = 'No reason provided' if (params == None) else params[1]
        if len(reason)>100: reason = reason[0:100]
        warned = self.client.db.Dashboard.addWarn(user_to_warn, ctx.author, reason)
        if warned:
            error = self.client.success_emoji
            return await ctx.send(f'{error} | {str(user_to_warn)} was warned by {str(ctx.author)} for the reason *"{reason}"*.')
        raise self.client.utils.send_error_message("an error occured.")
    
    @command('warns,warnslist,warn-list,infractions')
    @cooldown(5)
    async def warnlist(self, ctx):
        source = ctx.author if (len(ctx.message.mentions)==0) else ctx.message.mentions[0]
        data = self.client.db.Dashboard.getWarns(source)
        if data==None:
            error = self.client.error_emoji
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
    async def unwarn(self, ctx, *args):
        error = self.client.error_emoji
        user_to_unwarn = self.client.utils.getUser(ctx, args)
        if not ctx.author.guild_permissions.manage_messages: raise self.client.utils.send_error_message('You need the `Manage messages` permissions to unwarn someone.')
        unwarned = self.client.db.Dashboard.clearWarn(user_to_unwarn)
        if unwarned: return await ctx.send('{} | Successfully unwarned {}.'.format(self.client.success_emoji, user_to_unwarn))
        await ctx.send(f'{error} | {str(user_to_unwarn)} is not warned.')

    @command('welcomelog,setwelcome')
    @cooldown(15)
    async def welcome(self, ctx, *args):
        if not ctx.author.guild_permissions.manage_channels:
            raise self.client.utils.send_error_message("You need the `Manage Channels` permission!")
        else:
            if len(args)==0:
                await ctx.send(embed=discord.Embed(
                    title='Command usage',
                    description='{}welcome <CHANNEL>\n{}welcome disable'.format(self.client.command_prefix, self.client.command_prefix),
                    color=ctx.guild.me.roles[::-1][0].color
                ))
            else:
                if args[0].lower()=='disable':
                    self.client.db.Dashboard.set_welcome(ctx.guild.id, None)
                    await ctx.send("{} | Welcome disabled!".format(self.client.success_emoji))
                else:
                    try:
                        if args[0].startswith("<#") and args[0].endswith('>'): channelid = int(args[0].split('<#')[1].split('>')[0])
                        else: channelid = int([i.id for i in ctx.guild.channels if str(i.name).lower()==str(''.join(args)).lower()][0])
                        self.client.db.Dashboard.set_welcome(ctx.guild.id, channelid)
                        await ctx.send("{} | Success! set the welcome log to <#{}>!".format(self.client.success_emoji, channelid))
                    except Exception as e:
                       raise self.client.utils.send_error_message("Invalid arguments!")
    
    @command('auto-role,welcome-role,welcomerole')
    @cooldown(12)
    async def autorole(self, ctx, *args):
        if not ctx.author.guild_permissions.manage_roles:
            raise self.client.utils.send_error_message("You need the `Manage Roles` permission!")
        else:
            if len(args)==0:
                await ctx.send(embed=discord.Embed(
                    title='Command usage',
                    description='{}autorole <ROLENAME/ROLEPING>\n{}autorole disable'.format(self.client.command_prefix, self.client.command_prefix),
                    color=ctx.guild.me.roles[::-1][0].color
                ))
            else:
                if args[0].lower()=='disable':
                    self.client.db.Dashboard.set_autorole(ctx.guild.id, None)
                    await ctx.send("{} | Autorole disabled!".format(self.client.success_emoji))
                else:
                    try:
                        if args[0].startswith("<@&") and args[0].endswith('>'): roleid = int(args[0].split('<@&')[1].split('>')[0])
                        else: roleid = int([i.id for i in ctx.guild.roles if str(i.name).lower()==str(' '.join(args)).lower()][0])
                        self.client.db.Dashboard.set_autorole(ctx.guild.id, roleid)
                        await ctx.send("{} | Success! set the autorole to **{}!**".format(self.client.success_emoji, ctx.guild.get_role(roleid).name))
                    except:
                        raise self.client.utils.send_error_message("Invalid arguments!")
 
    @command('bigemoji,emojipic,emoji-img')
    @cooldown(3)
    async def emojiimg(self, ctx, *args):
        try:
            em = args[0].lower()
            if em.startswith('<:a:'): _id, an = em.split(':')[3].split('>')[0], True
            else: _id, an = em.split(':')[2].split('>')[0], False
            if an:
                async with self.session.get('https://cdn.discordapp.com/emojis/{}.gif'.format(_id)) as r:
                    res = await r.read()
                    try:
                        return await ctx.send(file=discord.File(fp=res, filename='emoji.gif'))
                    except:
                        raise self.client.utils.send_error_message('The emoji file size is too big!')
            else: await ctx.send(file=discord.File(self.client.canvas.urltoimage('https://cdn.discordapp.com/emojis/{}.png'.format(_id)), 'emoji.png'))
        except:
            raise self.client.utils.send_error_message('Invalid emoji.')
    
    @command()
    @cooldown(10)
    async def slowmode(self, ctx, *args):
        if (len(args)==0): raise self.client.utils.send_error_message("Please add on how long in seconds.")
        else:
            try:
                assert args[0].isnumeric(), "Please add the time in seconds. (number)"
                count = int(args[0])
                assert count in range(0, 21599), "Invalid range."
                assert ctx.author.guild_permissions.manage_channels, "You need the `manage channels` permission to do this.`"
                await ctx.channel.edit(slowmode_delay=count)
                return await ctx.send(self.client.success_emoji+" | "+("Disabled channel slowmode." if (count == 0) else f"Successfully set slowmode for <#{ctx.channel.id}> to {count} seconds."))
            except Exception as e:
                raise self.client.utils.send_error_message(str(e))
            
    @command('addrole,add-role')
    @cooldown(10)
    async def ar(self, ctx, *args):
        if not ctx.author.guild_permissions.manage_roles: raise self.client.utils.send_error_message(f'{ctx.author.mention}, you don\'t have the `Manage Roles` permission!')
        else:
            role_and_guy = self.client.utils.split_parameter_to_two(args)
            if role_and_guy == None: raise self.client.utils.send_error_message(f"Please make sure you inputted like this: `{self.client.command_prefix}addrole <user id/user mention/username>, <role id/role mention/rolename>`")
            guy = self.client.utils.getUser(ctx, role_and_guy[0])
            role_array = [i for i in ctx.guild.roles if role_and_guy[1].lower() in i.name.lower()]
            if len(role_array) == 0: raise self.client.utils.send_error_message(f"Role `{role_and_guy[1]}` does not exist.")
            try:
                await guy.add_roles(role_array[0])
                return await ctx.send(self.client.success_emoji+f" | Successfully added `{role_array[0].name}` role to `{str(guy)}`!")
            except:
                raise self.client.utils.send_error_message(f"Oops. Please make sure i have the manage roles perms.")
    
    @command('removerole,remove-role')
    @cooldown(10)
    async def rr(self, ctx, *args):
        if not ctx.author.guild_permissions.manage_roles: raise self.client.utils.send_error_message(f'{ctx.author.mention}, you don\'t have the `Manage Roles` permission!')
        else:
            role_and_guy = self.client.utils.split_parameter_to_two(args)
            if role_and_guy == None: raise self.client.utils.send_error_message(f"Please make sure you inputted like this: `{self.client.command_prefix}removerole <user id/user mention/username>, <role id/role mention/rolename>`")
            guy = self.client.utils.getUser(ctx, role_and_guy[0])
            role_array = [i for i in ctx.guild.roles if role_and_guy[1].lower() in i.name.lower()]
            if len(role_array) == 0: raise self.client.utils.send_error_message(f"Role `{role_and_guy[1]}` does not exist.")
            try:
                await guy.remove_roles(role_array[0])
                return await ctx.send(self.client.success_emoji+f" | Successfully removed `{role_array[0].name}` role from `{str(guy)}`!")
            except:
                raise self.client.utils.send_error_message("Oops. Please make sure i have the manage roles perms.")

    @command('kick')
    @cooldown(10)
    async def ban(self, ctx, *args):
        try:
            permission_name = 'ban_members' if ctx.message.content.startswith(self.client.command_prefix + "ban") else 'kick_members'
            permission = getattr(ctx.author.guild_permissions, permission_name)
            assert permission, "{} does not have the `{}` to {} members.".format(str(ctx.author), permission_name.replace('_', ' '), permission_name.split('_')[0])
            idiot = self.client.utils.getUser(ctx, args)
            assert idiot != ctx.author, "You cannot {} yourself.".format(permission_name.split('_')[0])
            assert not idiot.guild_permissions.manage_guild, "You cannot {} a moderator.".format(permission_name.split('_')[0])
            return await ctx.send("{} | Aight. {}ed {} from existence.".format(self.client.success_emoji, permission_name.split('_')[0], str(idiot)))
        except Exception as e:
            raise self.client.utils.send_error_message(str(e))
            
    @command('purge')
    @cooldown(2)
    async def clear(self, ctx, *args):
        try:
            assert ctx.author.guild_permissions.manage_messages, "You need the `manage messages` permission to do this."
            assert len(args)>0, 'Please insert the amount to be cleared or a mention.'
            if len(ctx.message.mentions)==0 and (not args[0].isnumeric()): raise Exception('Please input a valid parameter')
            mention = True if len(ctx.message.mentions)>0 else False
            try: await ctx.message.delete()
            except: pass
            if not mention:
                num = int(args[0])
                assert (num in range(1, 301)), "invalid arguments, out of range"
                await ctx.channel.purge(limit=num)
                return await ctx.send(self.client.success_emoji+f" | Successfully purged {num} messages.", delete_after=3)
            def check(m): return m.author.id == ctx.message.mentions[0].id
            deleted_messages = await ctx.channel.purge(check=check, limit=500)
            return await ctx.send(self.client.success_emoji+f" | Successfully purged {len(deleted_messages)} messages.", delete_after=3)
        except Exception as e:
            raise self.client.utils.send_error_message(str(e))
                
    @command('hidechannel')
    @cooldown(5)
    async def lockdown(self, ctx, *args):
        if len(args)==0: raise self.client.utils.send_error_message(f'Invalid parameters. Correct Example: `{self.client.command_prefix}{args[0][1:]} [disable/enable]`')
        else:
            accept = True
            if not ctx.author.guild_permissions.administrator: raise self.client.utils.send_error_message('You need the `Administrator` permission to do this, unless you are trying to mute yourself.')
            else:
                if 'enable' not in args[0].lower():
                    if 'disable' not in args[0].lower():
                        raise self.client.utils.send_error_message('Oops! Please add `enable` or `disable`.')
                        accept = False
                if accept:
                    try:
                        if args[0].lower()=='disable':
                            if 'hidechannel' in ctx.message.content: await ctx.channel.set_permissions(ctx.guild.default_role, read_messages=True)
                            if 'lockdown' in ctx.message.content: await ctx.channel.set_permissions(ctx.guild.default_role, send_messages=True)
                        elif args[0].lower()=='enable':
                            if 'hidechannel' in ctx.message.content: await ctx.channel.set_permissions(ctx.guild.default_role, read_messages=False)
                            if 'lockdown' in ctx.message.content: await ctx.channel.set_permissions(ctx.guild.default_role, send_messages=False)
                        await ctx.send(self.client.success_emoji +f' | Success! <#{ctx.channel.id}>\'s {str(ctx.message.content).split(" ")[0][1:]} has been {args[0]}d!')
                    except Exception as e:
                        raise self.client.utils.send_error_message(f'For some reason, i cannot change <#{ctx.channel.id}>\'s :(\n\n```{str(e)}```')

    @command('roles,serverroles,serverchannels,channels')
    @cooldown(2)
    async def channel(self, ctx):
        total = ', '.join([f'<#{i.id}>' for i in ctx.guild.channels]) if 'channel' in ctx.message.content.lower() else ', '.join([f'<@&{i.id}>' for i in ctx.guild.roles])
        await ctx.send(embed=discord.Embed(description=total, color=ctx.guild.me.roles[::-1][0].color))

    @command('ui,user,usercard,user-info,user-card,whois,user-interface,userinterface')
    @cooldown(3)
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
        url = self.client.utils.getUserAvatar(ctx, args, allowgif=True, size=4096)
        return await ctx.send(url)

    @command('serveremotes,emotelist,emojilist,emotes,serveremoji')
    @cooldown(10)
    async def serveremojis(self, ctx):
        if len(ctx.guild.emojis)==0: raise self.client.utils.send_error_message('This server has no emojis!')
        else:
            await ctx.send(', '.join([str(i) for i in ctx.guild.emojis])[0:2000])

    @command('serverinfo,server,servericon,si,server-info,guild,guildinfo,guild-info')
    @cooldown(10)
    async def servercard(self, ctx, *args):
        if 'servericon' in ctx.message.content:
            if ctx.guild.icon_url == None: raise self.client.utils.send_error_message("This server has no emotes...")
            await ctx.send(ctx.guild.icon_url_as(size=4096))
        else:
            if len(args)==0:
                if ctx.guild.member_count>100:
                    wait = await ctx.send('{} | Fetching guild data... please wait...'.format(self.client.loading_emoji))
                    im = self.client.canvas.server(ctx.guild)
                    await wait.delete()
                else:
                    await ctx.channel.trigger_typing()
                    im = self.client.canvas.server(ctx.guild)
                await ctx.send(file=discord.File(im, 'server.png'))
            else:
                try:
                    data = self.client.utils.fetchJSON(f"https://discord.com/api/v6/invites/{args[0].lower()}?with_counts=true")
                    im = self.client.canvas.server(None, data=data['guild'], raw=data)
                    await ctx.send(file=discord.File(im, 'server_that_has_some_kewl_vanity_url.png'))
                except:
                    raise self.client.utils.send_error_message("Please input a valid invite url code.")

    @command('serverinvite,create-invite,createinvite,makeinvite,make-invite,server-invite')
    @cooldown(30)
    async def getinvite(self, ctx):
        if not ctx.author.guild_permissions.create_instant_invite:
            raise self.client.utils.send_error_message('No create invite permission?')
        else:
            serverinvite = await ctx.channel.create_invite(reason='Requested by '+ctx.author.name)
            await ctx.send(self.client.success_emoji+' | New invite created! Link: **'+str(serverinvite)+'**')

    @command()
    @cooldown(3)
    async def roleinfo(self, ctx, *args):
        if len(args)==0:
            raise self.client.utils.send_error_message("Please send a role name or a role mention! (don\'t)")
        else:
            data = None
            if '<@&' in ''.join(args):
                data = ctx.guild.get_role(int(str(ctx.message.content).split('<@&')[1].split('>')[0]))
            else:
                for i in ctx.guild.roles:
                    if ' '.join(args).lower()==str(i.name).lower(): data = i ; break
            if data==None:
                raise self.client.utils.send_error_message('Role not found!')
            else:
                if data.permissions.administrator: perm = ':white_check_mark: Server Administrator'
                else: perm = ':x: Server Administrator'
                if data.mentionable==True: men = ':warning: You can mention this role and they can get pinged.'
                else: men = ':v: You can mention this role and they will not get pinged! ;)'
                embedrole = discord.Embed(title='Role info for role: '+str(data.name), description='**Role ID: **'+str(data.id)+'\n**Role created at: **'+self.client.utils.lapsed_time_from_seconds(round(t.now().timestamp()-data.created_at.timestamp()))+' ago\n**Role position: **'+str(data.position)+'\n**Members having this role: **'+str(len(data.members))+'\n'+str(men)+'\nPermissions Value: '+str(data.permissions.value)+'\n'+str(perm), colour=data.colour)
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
        embed = discord.Embed(title='Guild permissions for '+source.name, description='\n'.join(perms_list), colour=ctx.guild.me.roles[::-1][0].color)
        await ctx.send(embed=embed)

    @command('mkchannel,mkch,createchannel,make-channel,create-channel')
    @cooldown(5)
    async def makechannel(self, ctx, *args):
        if len(args)<2:
            raise self.client.utils.send_error_message('Please send me an args or something!')
        else:
            begin = True
            if args[0].lower()!='voice':
                if args[0].lower()!='text':
                    raise self.client.utils.send_error_message("Please use 'text' or 'channel'!")
                    begin = False
            if begin:
                name = str(ctx.message.content).split(' ')[2:len(str(ctx.message.content).split())].replace(' ', '-')
                if args[0].lower()=='voice': await ctx.guild.create_voice_channel(name)
                else: await ctx.guild.create_voice_channel(name)

    @command('nickname')
    @cooldown(10)
    async def nick(self, ctx, *args):
        if len(args)<2:
            raise self.client.utils.send_error_message("Invalid args!")
        else:
            if not ctx.author.guild_permissions.change_nickname:
                raise self.client.utils.send_error_message("Invalid permissions! You need the change nickname permission to do this")
            else:
                if len(ctx.message.mentions)==0 or not args[0].startswith('<@'):
                    raise self.client.utils.send_error_message("Go mention someone!")
                else:
                    try:
                        newname = ' '.join(args).split('> ')[1]
                        await ctx.message.mentions[0].edit(nick=newname)
                        await ctx.send(self.client.success_emoji+" | Changed the nickname to {}!".format(newname))
                    except:
                        raise self.client.utils.send_error_message("Try making my role higher than the person you are looking for!")

    @command('emoji')
    @cooldown(5)
    async def emojiinfo(self, ctx, *args):
        try:
            erry, emojiid = int(args[0].split(':')[2][:-1]), False
            data = self.client.get_emoji(emojiid)
        except:
            erry = True
            raise self.client.utils.send_error_message('For some reason, we cannot process your emoji ;(')
        if not erry:
            if data.animated: anim = 'This emoji is an animated emoji. **Only nitro users can use it.**'
            else: anim = 'This emoji is a static emoji. **Everyone can use it (except if limited by role)**'
            embedy = discord.Embed(title='Emoji info for :'+str(data.name)+':', description='**Emoji name:** '+str(data.name)+'\n**Emoji ID: **'+str(data.id)+'\n'+anim+'\n**Emoji\'s server ID: **'+str(data.guild_id)+'\n**Emoji creation time: **'+str(data.created_at)[:-7]+' UTC.', colour=ctx.guild.me.roles[::-1][0].color)
            embedy.set_thumbnail(url='https://cdn.discordapp.com/emojis/'+str(data.id)+'.png?v=1')
            await ctx.send(embed=embedy)

    @command('createchannel,create-channel,ch')
    @cooldown(10)
    async def makechannel(self, ctx, *args):
        if len(args)<2:
            raise self.client.utils.send_error_message(f'Oops! Not a valid argument! Please do `{self.client.command_prefix}makechannel <voice/text> <name>`')
        else:
            if args[0].lower()!='text' or args[0].lower()!='voice':
                raise self.client.utils.send_error_message('Oops! Not a valid type of channel!')
            else:
                names = list(args)[1:len(args)]
                if args[0].lower()=='text': await ctx.guild.create_text_channel(name='-'.join(list(names)))
                else: await ctx.guild.create_voice_channel(name='-'.join(names))
                await ctx.send(self.client.success_emoji+" | Successfully created a {} channel named {}.".format(args[0], str('-'.join(names))))
def setup(client):
    client.add_cog(moderation(client))