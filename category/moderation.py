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
        self.latest = ["latest", "recent", "last"]
        self.first = ["first", "early", "earliest", "earlyest", "firstmember"]
        self.permission_attributes = [
            "add_reactions",
            "administrator",
            "attach_files",
            "ban_members",
            "change_nickname",
            "connect",
            "create_instant_invite",
            "deafen_members",
            "embed_links",
            "external_emojis",
            "kick_members",
            "manage_channels",
            "manage_emojis",
            "manage_guild",
            "manage_messages",
            "manage_nicknames",
            "manage_permissions",
            "manage_roles",
            "manage_webhooks",
            "mention_everyone",
            "move_members",
            "mute_members",
            "priority_speaker",
            "read_message_history",
            "read_messages",
            "send_messages",
            "send_tts_messages",
            "speak",
            "stream",
            "use_external_emojis",
            "use_voice_activation",
            "view_audit_log",
            "view_channel",
            "view_guild_insights"
        ]
        
    @command('jp,joinpos,joindate,jd,howold')
    @cooldown(5)
    async def joinposition(self, ctx, *args):
        wait = await ctx.send(f"{ctx.bot.util.loading_emoji} | Hang tight... collecting data...")
        from_string = False
        current_time, members, user_index, desc = t.now().timestamp(), ctx.guild.members, None, ""
        full_arr = list(map(lambda x: {'ja': x.joined_at.timestamp(), 'da': x}, members))
        raw_unsorted_arr = list(map(lambda x: x['ja'], full_arr))
        sorted_arr = sorted(raw_unsorted_arr)
        if (len(args) > 0) and (not args[0].isnumeric()):
            if args[0].lower() in self.first:
                from_string, user_index, title = True, 0, f'User join position for the first member in {ctx.guild.name}'
            elif args[0].lower() in self.latest:
                from_string, user_index, title = True, ctx.guild.member_count - 1, f'User join position for the latest member to join {ctx.guild.name}'
        
        if not from_string:
            if len(args) > 0 and args[0].isnumeric() and ((int(args[0])-1) in range(len(members))):
                user_index, title = int(args[0]) - 1, f'User join position for order #{args[0]}'
            else:
                user = ctx.bot.Parser.parse_user(ctx, args)
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
                i + 1, name, ctx.bot.util.strfsecond(current_time - full_arr[index]['ja'])
            )
        return await wait.edit(content='', embed=discord.Embed(title=title, description=desc, color=ctx.guild.me.roles[::-1][0].color))
        
    @command()
    @cooldown(2)
    async def config(self, ctx):
        data = ctx.bot.db.Dashboard.getData(ctx.guild.id)
        if data is None: return await ctx.bot.util.send_error_message(ctx, 'This server does not have any configuration for this bot.')
        autorole = 'Set to <@&{}>'.format(data['autorole']) if data['autorole'] is not None else '<Not set>'
        welcome = 'Set to <#{}>'.format(data['welcome']) if data['welcome'] is not None else '<Not set>'
        starboard = 'Set to <#{}> (with {} reactions required)'.format(data['starboard'], data['star_requirements']) if data['starboard'] is not None else '<Not set>'
        mute = 'Set to <@&{}>'.format(data['mute']) if data['mute'] is not None else '<Not set>'
        extras = [len(data['shop']), len(data['warns'])]
        dehoister = 'Enabled :white_check_mark:' if data['dehoister'] else 'Disabled :x:'
        subs = 'Enabled :white_check_mark:' if data['subscription'] is not None else 'Disabled :x:'
        await ctx.send(embed=discord.Embed(title=f'{ctx.guild.name}\'s configuration', description=f'**Auto role:** {autorole}\n**Welcome channel:** {welcome}\n**Starboard channel: **{starboard}\n**Name/nick dehoister: **{dehoister}\n**Mute role: **{mute}\n**Members warned: **{extras[1]}\n**Shop products sold: **{extras[0]}\n**Development updates/Events subscription: {subs}**', color=ctx.guild.me.roles[::-1][0].color).set_thumbnail(url=ctx.guild.icon_url))

    @command()
    @cooldown(5)
    async def mute(self, ctx, *args):
        toMute = ctx.bot.Parser.parse_user(ctx, args, allownoargs=False)
        if not ctx.author.guild_permissions.manage_messages: return await ctx.bot.util.send_error_message(ctx, 'No `manage messages` permission!')
        role = ctx.bot.db.Dashboard.getMuteRole(ctx.guild.id)
        if role is None:
            await ctx.send('{} | Please wait... Setting up...\nThis may take a while if your server has a lot of channels.'.format(ctx.bot.util.loading_emoji))
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
            ctx.bot.db.Dashboard.editMuteRole(ctx.guild.id, role.id)
            role = role.id
        role = ctx.guild.get_role(role)
        try:
            await toMute.add_roles(role)
            await ctx.send('{} | Muted. Ductaped {}\'s mouth.'.format(ctx.bot.util.success_emoji, toMute.name))
        except Exception as e:
            print(e)
            return await ctx.bot.util.send_error_message(ctx, 'I cannot mute him... maybe i has less permissions than him.\nHis mouth is too powerful.')
    
    @command()
    @cooldown(5)
    async def unmute(self, ctx, *args):
        toUnmute = ctx.bot.Parser.parse_user(ctx, args, allownoargs=False)
        roleid = ctx.bot.db.Dashboard.getMuteRole(ctx.guild.id)
        if roleid is None: return await ctx.bot.util.send_error_message(ctx, 'He is not muted!\nOr maybe you muted this on other bot... which is not compatible.')
        elif roleid not in list(map(lambda x: x.id, ctx.message.mentions[0].roles)):
            return await ctx.bot.util.send_error_message(ctx, 'That guy is not muted.')
        try:
            await toUnmute.remove_roles(ctx.guild.get_role(roleid))
            await ctx.send('{} | {} unmuted.'.format(ctx.bot.util.success_emoji, toUnmute.name))
        except:
            return await ctx.bot.util.send_error_message(ctx, f'I cannot unmute {toUnmute.name}!')

    @command('dehoist')
    @cooldown(10)
    async def dehoister(self, ctx, *args):
        if not ctx.author.guild_permissions.manage_nicknames: return await ctx.bot.util.send_error_message(ctx, 'You need the `Manage Nicknames` permissions!')
        data = ctx.bot.db.Dashboard.getDehoister(ctx.guild.id)
        if not data: 
            ctx.bot.db.Dashboard.setDehoister(ctx.guild, True)
            return await ctx.send(embed=discord.Embed(
                title='Activated dehoister.',
                description=f'**What is dehoister?**\nDehoister is an automated part of this bot that automatically renames someone that tries to hoist their name (for example: `!ABC`)\n\n**How do i deactivate this?**\nJust type `{ctx.bot.command_prefix}dehoister`.\n\n**It doesn\'t work for me!**\nMaybe because your role position is higher than me, so i don\'t have the permissions required.',
                color=ctx.guild.me.roles[::-1][0].color
            ))
        ctx.bot.db.Dashboard.setDehoister(ctx.guild, False)
        await ctx.send('{} | Dehoister deactivated.'.format(ctx.bot.util.success_emoji))

    @command()
    @cooldown(10)
    async def starboard(self, ctx, *args):
        wait = await ctx.send('{} | Please wait...'.format(ctx.bot.util.loading_emoji))
        if not ctx.author.guild_permissions.manage_channels:
            return await ctx.bot.util.send_error_message(ctx, 'You need the `Manage channels` permission.')
        starboard_channel = ctx.bot.db.Dashboard.getStarboardChannel(ctx.guild)
        if len(args)==0:
            if starboard_channel['channelid'] is None:
                channel = await ctx.guild.create_text_channel(name='starboard', topic='Server starboard channel. Every funny/cool posts will be here.')
                ctx.bot.db.Dashboard.addStarboardChannel(channel, 1)
                success = ctx.bot.util.success_emoji
                return await wait.edit(content=f'{success} | OK. Created a channel <#{str(channel.id)}>. Every starboard will be set there.\nTo remove starboard, type `{ctx.bot.command_prefix}starboard remove`.\nBy default, starboard requirements are set to 1 reaction. To increase, type `{ctx.bot.command_prefix}starboard limit <number>`.')
            return await wait.edit(content='', embed=discord.Embed(
                title=f'Starboard for {ctx.guild.name}',
                description='Channel: <#{}>\nStars required to reach: {}'.format(
                    starboard_channel['channelid'], starboard_channel['starlimit']
                ), color=ctx.guild.me.roles[::-1][0].color
            ))
        if starboard_channel['channelid'] is None: return
        elif args[0].lower().startswith("rem"):
            ctx.bot.db.Dashboard.removeStarboardChannel(ctx.guild)
            return await wait.edit(content='{} | OK. Starboard for this server is deleted.'.format(ctx.bot.util.success_emoji))
        elif args[0].lower()=='limit':
            try:
                num = int(list(args)[1])
                if not num in range(1, 20):
                    return await ctx.bot.util.send_error_message(ctx, 'Invalid number.')
                ctx.bot.db.Dashboard.setStarboardLimit(num, ctx.guild)
                await wait.edit(content='{} | Set the limit to {} reactions.'.format(ctx.bot.util.success_emoji, str(num)))
            except:
                return await ctx.bot.util.send_error_message(ctx, 'Invalid number.')

    @command()
    @cooldown(10)
    async def serverstats(self, ctx):
        await ctx.send(file=discord.File(
            ctx.bot.canvas.serverstats(ctx.guild), "serverstats.png"
        ))
    
    @command()
    @cooldown(5)
    async def warn(self, ctx, *args):
        params = ctx.bot.Parser.split_content_to_two(args)
        if not ctx.author.guild_permissions.manage_messages:
            return await ctx.bot.util.send_error_message(ctx, 'You need to have manage messages permissions to do this man. Sad.')
        elif len(args) == 0: return await ctx.send('{} | Invalid arguments. do `{}warn <userid/username> <reason optional>`')
        user_to_warn = ctx.bot.Parser.parse_user(ctx, args[0] if params is None else params[0], allownoargs=False)
        if user_to_warn.guild_permissions.manage_channels: return await ctx.bot.util.send_error_message(ctx, "You cannot warn a moderator.")
        reason = 'No reason provided' if (params is None) else params[1]
        if len(reason)>100: reason = reason[0:100]
        warned = ctx.bot.db.Dashboard.addWarn(user_to_warn, ctx.author, reason)
        if warned:
            error = ctx.bot.util.success_emoji
            return await ctx.send(f'{error} | {str(user_to_warn)} was warned by {str(ctx.author)} for the reason *"{reason}"*.')
        return await ctx.bot.util.send_error_message(ctx, "an error occured.")
    
    @command('warns,warnslist,warn-list,infractions')
    @cooldown(5)
    async def warnlist(self, ctx):
        source = ctx.author if (len(ctx.message.mentions)==0) else ctx.message.mentions[0]
        data = ctx.bot.db.Dashboard.getWarns(source)
        if data is None:
            return await ctx.send(f'{ctx.bot.util.error_emoji} | Good news! {source.name} does not have any warns!')
        warnlist = '\n'.join(map(
            lambda x: '{}. "{}" (warned by <@{}>)'.format(x+1, data[x]['reason'], data[x]['moderator']),
            range(len(data))
        )[0:10])
        await ctx.send(embed=discord.Embed(
            title=f'Warn list for {source.name}',
            description=warnlist,
            color=discord.Colour.red()
        ))
    
    @command('deletewarn,clear-all-infractions,clear-infractions,clearinfractions,delinfractions,delwarn,clearwarn,clear-warn')
    @cooldown(5)
    async def unwarn(self, ctx, *args):
        error = ctx.bot.util.error_emoji
        user_to_unwarn = ctx.bot.Parser.parse_user(ctx, args)
        if not ctx.author.guild_permissions.manage_messages: return await ctx.bot.util.send_error_message(ctx, 'You need the `Manage messages` permissions to unwarn someone.')
        unwarned = ctx.bot.db.Dashboard.clearWarn(user_to_unwarn)
        if unwarned: return await ctx.send('{} | Successfully unwarned {}.'.format(ctx.bot.util.success_emoji, user_to_unwarn))
        await ctx.send(f'{error} | {str(user_to_unwarn)} is not warned.')

    @command('welcomelog,setwelcome')
    @cooldown(15)
    async def welcome(self, ctx, *args):
        if not ctx.author.guild_permissions.manage_channels:
            return await ctx.bot.util.send_error_message(ctx, "You need the `Manage Channels` permission!")
        else:
            if len(args)==0:
                await ctx.send(embed=discord.Embed(
                    title='Command usage',
                    description='{}welcome <CHANNEL>\n{}welcome disable'.format(ctx.bot.command_prefix, ctx.bot.command_prefix),
                    color=ctx.guild.me.roles[::-1][0].color
                ))
            else:
                if args[0].lower()=='disable':
                    ctx.bot.db.Dashboard.set_welcome(ctx.guild.id, None)
                    await ctx.send("{} | Welcome disabled!".format(ctx.bot.util.success_emoji))
                else:
                    try:
                        if args[0].startswith("<#") and args[0].endswith('>'): channelid = int(args[0].split('<#')[1].split('>')[0])
                        else: channelid = int([i.id for i in ctx.guild.channels if str(i.name).lower()==str(''.join(args)).lower()][0])
                        ctx.bot.db.Dashboard.set_welcome(ctx.guild.id, channelid)
                        await ctx.send("{} | Success! set the welcome log to <#{}>!".format(ctx.bot.util.success_emoji, channelid))
                    except Exception as e:
                       return await ctx.bot.util.send_error_message(ctx, "Invalid arguments!")
    
    @command('auto-role,welcome-role,welcomerole')
    @cooldown(12)
    async def autorole(self, ctx, *args):
        if not ctx.author.guild_permissions.manage_roles:
            return await ctx.bot.util.send_error_message(ctx, "You need the `Manage Roles` permission!")
        else:
            if len(args)==0:
                await ctx.send(embed=discord.Embed(
                    title='Command usage',
                    description='{}autorole <ROLENAME/ROLEPING>\n{}autorole disable'.format(ctx.bot.command_prefix, ctx.bot.command_prefix),
                    color=ctx.guild.me.roles[::-1][0].color
                ))
            else:
                if args[0].lower()=='disable':
                    ctx.bot.db.Dashboard.set_autorole(ctx.guild.id, None)
                    await ctx.send("{} | Autorole disabled!".format(ctx.bot.util.success_emoji))
                else:
                    try:
                        if args[0].startswith("<@&") and args[0].endswith('>'): roleid = int(args[0].split('<@&')[1].split('>')[0])
                        else: roleid = int([i.id for i in ctx.guild.roles if str(i.name).lower()==str(' '.join(args)).lower()][0])
                        ctx.bot.db.Dashboard.set_autorole(ctx.guild.id, roleid)
                        await ctx.send("{} | Success! set the autorole to **{}!**".format(ctx.bot.util.success_emoji, ctx.guild.get_role(roleid).name))
                    except:
                        return await ctx.bot.util.send_error_message(ctx, "Invalid arguments!")
 
    @command('bigemoji,emojipic,emoji-img')
    @cooldown(3)
    async def emojiimg(self, ctx, *args):
        text = "".join(args).replace(" ", "").lower()
        try:
            if text.startswith("<") and text.endswith(">"):
                is_animated = text.startswith("<a:")
                _ext = ".gif" if is_animated else ".png"
                _id = int(text.split(":")[2].split(">")[0])
                return await ctx.bot.util.send_image_attachment(ctx, 'https://cdn.discordapp.com/emojis/{}{}'.format(_id, _ext))
            
            _twemoji = ctx.bot.twemoji(text)
            if _twemoji == text:
                return await ctx.bot.util.send_error_message(ctx, 'No emoji found.')
            return await ctx.bot.util.send_image_attachment(ctx, _twemoji)
            
        except:
            return await ctx.bot.util.send_error_message(ctx, 'Invalid emoji.')
    
    @command()
    @cooldown(10)
    async def slowmode(self, ctx, *args):
        if (len(args)==0): return await ctx.bot.util.send_error_message(ctx, "Please add on how long in seconds.")
        else:
            try:
                assert args[0].isnumeric(), "Please add the time in seconds. (number)"
                count = int(args[0])
                assert count in range(21599), "Invalid range."
                assert ctx.author.guild_permissions.manage_channels, "You need the `manage channels` permission to do this.`"
                await ctx.channel.edit(slowmode_delay=count)
                return await ctx.send(ctx.bot.util.success_emoji+" | "+("Disabled channel slowmode." if (count == 0) else f"Successfully set slowmode for <#{ctx.channel.id}> to {count} seconds."))
            except Exception as e:
                return await ctx.bot.util.send_error_message(ctx, str(e))
            
    @command('addrole,add-role')
    @cooldown(10)
    async def ar(self, ctx, *args):
        if not ctx.author.guild_permissions.manage_roles: return await ctx.bot.util.send_error_message(ctx, f'{ctx.author.mention}, you don\'t have the `Manage Roles` permission!')
        else:
            role_and_guy = ctx.bot.Parser.split_content_to_two(args)
            if role_and_guy is None: return await ctx.bot.util.send_error_message(ctx, f"Please make sure you inputted like this: `{ctx.bot.command_prefix}addrole <user id/user mention/username>, <role id/role mention/rolename>`")
            guy = ctx.bot.Parser.parse_user(ctx, role_and_guy[0])
            role_array = [i for i in ctx.guild.roles if role_and_guy[1].lower() in i.name.lower()]
            if len(role_array) == 0: return await ctx.bot.util.send_error_message(ctx, f"Role `{role_and_guy[1]}` does not exist.")
            try:
                await guy.add_roles(role_array[0])
                return await ctx.send(ctx.bot.util.success_emoji+f" | Successfully added `{role_array[0].name}` role to `{str(guy)}`!")
            except:
                return await ctx.bot.util.send_error_message(ctx, f"Oops. Please make sure i have the manage roles perms.")
    
    @command('removerole,remove-role')
    @cooldown(10)
    async def rr(self, ctx, *args):
        if not ctx.author.guild_permissions.manage_roles: return await ctx.bot.util.send_error_message(ctx, f'{ctx.author.mention}, you don\'t have the `Manage Roles` permission!')
        else:
            role_and_guy = ctx.bot.Parser.split_content_to_two(args)
            if role_and_guy is None: return await ctx.bot.util.send_error_message(ctx, f"Please make sure you inputted like this: `{ctx.bot.command_prefix}removerole <user id/user mention/username>, <role id/role mention/rolename>`")
            guy = ctx.bot.Parser.parse_user(ctx, role_and_guy[0])
            role_array = [i for i in ctx.guild.roles if role_and_guy[1].lower() in i.name.lower()]
            if len(role_array) == 0: return await ctx.bot.util.send_error_message(ctx, f"Role `{role_and_guy[1]}` does not exist.")
            try:
                await guy.remove_roles(role_array[0])
                return await ctx.send(ctx.bot.util.success_emoji+f" | Successfully removed `{role_array[0].name}` role from `{str(guy)}`!")
            except:
                return await ctx.bot.util.send_error_message(ctx, "Oops. Please make sure i have the manage roles perms.")

    @command('kick')
    @cooldown(10)
    async def ban(self, ctx, *args):
        command_name = ctx.bot.util.get_command_name(ctx)
    
        try:
            permission_name = command_name + "_members"
            permission = getattr(ctx.author.guild_permissions, permission_name)
            assert permission, "{} does not have the `{}` to {} members.".format(str(ctx.author), permission_name.replace('_', ' '), command_name)
            idiot = ctx.bot.Parser.parse_user(ctx, args, allownoargs=False)
            assert idiot != ctx.author, "You cannot {} yourself.".format(command_name)
            assert not idiot.guild_permissions.manage_guild, "You cannot {} a moderator.".format(command_name)
            return await ctx.send("{} | Aight. {}ed {} from existence.".format(ctx.bot.util.success_emoji, command_name, str(idiot)))
        except Exception as e:
            return await ctx.bot.util.send_error_message(ctx, str(e))
            
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
                return await ctx.send(ctx.bot.util.success_emoji+f" | Successfully purged {num} messages.", delete_after=3)
            def check(m): return m.author.id == ctx.message.mentions[0].id
            deleted_messages = await ctx.channel.purge(check=check, limit=500)
            return await ctx.send(ctx.bot.util.success_emoji+f" | Successfully purged {len(deleted_messages)} messages.", delete_after=3)
        except Exception as e:
            return await ctx.bot.util.send_error_message(ctx, str(e))
                
    @command('hidechannel')
    @cooldown(5)
    async def lockdown(self, ctx, *args):
        try:
            assert len(args) > 0
            command_name = ctx.bot.util.get_command_name(ctx)
            
            if not ctx.author.guild_permissions.administrator: return await ctx.bot.util.send_error_message(ctx, 'You need the `Administrator` permission to do this, unless you are trying to mute yourself.')
            else:
                if 'enable' not in args[0].lower():
                    if 'disable' not in args[0].lower():
                        return await ctx.bot.util.send_error_message(ctx, 'Sorry! Please add `enable` or `disable`.')
                try:
                    if 'disable' in args[0].lower():
                        if command_name == 'hidechannel': await ctx.channel.set_permissions(ctx.guild.default_role, read_messages=True)
                        elif command_name == 'lockdown': await ctx.channel.set_permissions(ctx.guild.default_role, send_messages=True)
                    elif 'enable' in args[0].lower():
                        if command_name == 'hidechannel': await ctx.channel.set_permissions(ctx.guild.default_role, read_messages=False)
                        elif command_name == 'lockdown': await ctx.channel.set_permissions(ctx.guild.default_role, send_messages=False)
                    return await ctx.send(ctx.bot.util.success_emoji +f' | Success! <#{ctx.channel.id}>\'s {command_name} has been {args[0]}d!')
                except Exception as e:
                    return await ctx.bot.util.send_error_message(ctx, f'For some reason, i cannot change <#{ctx.channel.id}>\'s :(\n\n```{str(e)}```')
        except:
            return await ctx.bot.util.send_error_message(ctx, f'Invalid parameters. Correct Example: `{ctx.bot.command_prefix}{command_name} [disable/enable]`')    

    @command('roles,serverroles,serverchannels,channels')
    @cooldown(2)
    async def channel(self, ctx):
        arr = [f"<#{x.id}>" for x in ctx.guild.channels if x.type == discord.ChannelType.text] if "channel" in ctx.message.content.lower() else (list(map(lambda x: x.mention, ctx.guild.roles)))[1:]
        await ctx.send(str(", ".join(arr))[0:2000], allowed_mentions=discord.AllowedMentions(everyone=False, users=False, roles=False))

    @command('ui,user,usercard,user-info,user-card,whois,user-interface,userinterface')
    @cooldown(3)
    async def userinfo(self, ctx, *args):
        guy, nitro = ctx.bot.Parser.parse_user(ctx, args), False
        await ctx.trigger_typing()
        if guy.id in [i.id for i in ctx.guild.premium_subscribers]: nitro = True
        elif guy.is_avatar_animated(): nitro = True
        booster = True if guy in ctx.guild.premium_subscribers else False
        booster_since = round(t.now().timestamp() - guy.premium_since.timestamp()) if guy.premium_since is not None else False
        bg_col = ctx.bot.canvas.get_color_accent(str(guy.avatar_url_as(format="png")))
        data = ctx.bot.canvas.usercard(list(map(lambda x: {
            'name': x.name, 'color': x.color.to_rgb()
        }, guy.roles))[::-1][0:5], guy, str(guy.avatar_url_as(format="png")), bg_col, nitro, booster, booster_since)
        return await ctx.send(file=discord.File(data, str(guy.discriminator)+'.png'))

    @command('av,ava')
    @cooldown(2)
    async def avatar(self, ctx, *args):
        url = ctx.bot.Parser.parse_image(ctx, args, default_to_png=False, cdn_only=True, member_only=True, size=4096)
        embed = ctx.bot.Embed(ctx, title="Here's ya avatar mate", image=url)
        await embed.send()

    @command('serveremotes,emotelist,emojilist,emotes,serveremoji')
    @cooldown(10)
    async def serveremojis(self, ctx):
        if len(ctx.guild.emojis)==0: return await ctx.bot.util.send_error_message(ctx, 'This server has no emojis!')
        else:
            await ctx.send(str(', '.join(map(lambda x: str(x), ctx.guild.emojis)))[0:2000])

    @command('serverinfo,server,servericon,si,server-info,guild,guildinfo,guild-info')
    @cooldown(10)
    async def servercard(self, ctx, *args):
        if ctx.bot.util.get_command_name(ctx) == "servericon":
            if ctx.guild.icon_url is None: return await ctx.bot.util.send_error_message(ctx, "This server has no emotes...")
            await ctx.send(ctx.guild.icon_url_as(size=4096))
        else:
            if ctx.guild.member_count>100:
                wait = await ctx.send('{} | Fetching guild data... please wait...'.format(ctx.bot.util.loading_emoji))
                im = ctx.bot.canvas.server(ctx.guild)
                await wait.delete()
            else:
                await ctx.channel.trigger_typing()
                im = ctx.bot.canvas.server(ctx.guild)
            await ctx.send(file=discord.File(im, 'server.png'))

    @command('serverinvite,create-invite,createinvite,makeinvite,make-invite,server-invite')
    @cooldown(30)
    async def getinvite(self, ctx):
        if not ctx.author.guild_permissions.create_instant_invite:
            return await ctx.bot.util.send_error_message(ctx, 'No create invite permission?')
        else:
            serverinvite = await ctx.channel.create_invite(reason='Requested by '+ctx.author.display_name)
            await ctx.send(ctx.bot.util.success_emoji+' | New invite created! Link: **'+str(serverinvite)+'**')

    @command()
    @cooldown(3)
    async def roleinfo(self, ctx, *args):
        if len(args)==0:
            return await ctx.bot.util.send_error_message(ctx, "Please send a role name or a role mention! (don\'t)")
        else:
            data = None
            if '<@&' in ''.join(args):
                data = ctx.guild.get_role(int(ctx.message.content.split('<@&')[1].split('>')[0]))
            else:
                input = " ".join(args).lower()
                _filter = list(filter((lambda x: input in x.name.lower()), ctx.guild.roles))
                if len(_filter) > 0:
                    embed = ctx.bot.ChooseEmbed(ctx, _filter, key=(lambda x: x.mention))
                    res = await embed.run()
                    if res is not None:
                        data = res
                    else:
                        return
            if data is None:
                return await ctx.bot.util.send_error_message(ctx, 'Role not found!')
            else:
                if data.permissions.administrator: perm = ':white_check_mark: Server Administrator'
                else: perm = ':x: Server Administrator'
                if data.mentionable==True: men = ':warning: You can mention this role and they can get pinged.'
                else: men = ':v: You can mention this role and they will not get pinged! ;)'
                embedrole = discord.Embed(title='Role info for role: '+str(data.name), description='**Role ID: **'+str(data.id)+'\n**Role created at: **'+ctx.bot.util.strfsecond(round(t.now().timestamp()-data.created_at.timestamp()))+' ago\n**Role position: **'+str(data.position)+'\n**Members having this role: **'+str(len(data.members))+'\n'+str(men)+'\nPermissions Value: '+str(data.permissions.value)+'\n'+str(perm), colour=data.colour)
                embedrole.add_field(name='Role Colour', value='**Color hex: **#'+str(data.color.value)+'\n**Color integer: **'+str(data.color.value)+'\n**Color RGB: **'+str(', '.join(
                    list(map(lambda x: str(x), data.color.to_rgb()))
                )))
                await ctx.send(embed=embedrole)

    @command('perms,perm,permission,permfor,permsfor,perms-for,perm-for')
    @cooldown(10)
    async def permissions(self, ctx, *args):
        user = ctx.bot.Parser.parse_user(ctx, args)
        source = ctx.channel.permissions_for(user)
        embed = ctx.bot.Embed(ctx, title="Permissions for "+str(user)+" in "+ctx.channel.name)
        for permission in self.permission_attributes:
            emoji = ":white_check_mark:" if getattr(source, permission) else ":x:"
            embed.description += "{} {}\n".format(emoji, permission.replace("_", " "))
        embed.description = embed.description[:-2]
        return await embed.send()

    @command('mkchannel,mkch,createchannel,make-channel,create-channel')
    @cooldown(5)
    async def makechannel(self, ctx, *args):
        if len(args)<2:
            return await ctx.bot.util.send_error_message(ctx, 'Please send me an args or something!')
        else:
            begin = True
            if args[0].lower()!='voice':
                if args[0].lower()!='text':
                    return await ctx.bot.util.send_error_message(ctx, "Please use 'text' or 'channel'!")
                    begin = False
            if begin:
                name = ctx.message.content.split()[2:].replace(' ', '-')
                if args[0].lower()=='voice': await ctx.guild.create_voice_channel(name)
                else: await ctx.guild.create_voice_channel(name)

    @command('nickname')
    @cooldown(10)
    async def nick(self, ctx, *args):
        if len(args)<2:
            return await ctx.bot.util.send_error_message(ctx, "Invalid args!")
        else:
            if not ctx.author.guild_permissions.change_nickname:
                return await ctx.bot.util.send_error_message(ctx, "Invalid permissions! You need the change nickname permission to do this")
            else:
                if len(ctx.message.mentions)==0 or not args[0].startswith('<@'):
                    return await ctx.bot.util.send_error_message(ctx, "Go mention someone!")
                else:
                    try:
                        newname = ' '.join(args).split('> ')[1]
                        await ctx.message.mentions[0].edit(nick=newname)
                        await ctx.send(ctx.bot.util.success_emoji+" | Changed the nickname to {}!".format(newname))
                    except:
                        return await ctx.bot.util.send_error_message(ctx, "Try making my role higher than the person you are looking for!")

    @command('emoji')
    @cooldown(6)
    async def emojiinfo(self, ctx, *args):
        input = "".join(args).replace(" ", "").lower()
        try:
            if input.startswith("<") and input.endswith(">"):
                emojiid = int(args[0].split(':')[2][:-1])
                data = ctx.bot.get_emoji(emojiid)
            else:
                _fil = list(filter((lambda x: input in x.name.lower()), ctx.guild.emojis))
                assert len(_fil) > 0
                data = _fil[0]
        except:
            return await ctx.bot.util.send_error_message(ctx, 'For some reason, we cannot process your emoji ;(')
        if data.animated: anim, ext = 'This emoji is an animated emoji. **Only nitro users can use it.**', ".gif"
        else: anim, ext = 'This emoji is a static emoji. **Everyone can use it (except if limited by role)**', ".png"
        embedy = discord.Embed(title='Emoji info for :'+str(data.name)+':', description='**Emoji name:** '+str(data.name)+'\n**Emoji ID: **'+str(data.id)+'\n'+anim+'\n**Emoji creation time: **'+str(data.created_at)[:-7]+' UTC ('+ctx.bot.util.strfsecond(t.now().timestamp() - data.created_at.timestamp())+' ago).', colour=ctx.guild.me.roles[::-1][0].color)
        embedy.set_thumbnail(url='https://cdn.discordapp.com/emojis/'+str(data.id)+ext)
        await ctx.send(embed=embedy)

    @command('createchannel,create-channel,ch')
    @cooldown(10)
    async def makechannel(self, ctx, *args):
        if len(args)<2:
            return await ctx.bot.util.send_error_message(ctx, f'Oops! Not a valid argument! Please do `{ctx.bot.command_prefix}makechannel <voice/text> <name>`')
        else:
            if args[0].lower()!='text' or args[0].lower()!='voice':
                return await ctx.bot.util.send_error_message(ctx, 'Oops! Not a valid type of channel!')
            else:
                names = list(args)[1:]
                if args[0].lower()=='text': await ctx.guild.create_text_channel(name='-'.join(list(names)))
                else: await ctx.guild.create_voice_channel(name='-'.join(names))
                await ctx.send(ctx.bot.util.success_emoji+" | Successfully created a {} channel named {}.".format(args[0], str('-'.join(names))))
def setup(client):
    client.add_cog(moderation(client))