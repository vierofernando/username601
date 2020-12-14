import discord
from discord.ext import commands
import time
import random
import asyncio
from aiohttp import ClientSession
from decorators import *
from datetime import datetime as t
from twemoji_parser import emoji_to_url

class moderation(commands.Cog):
    def __init__(self):
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
    
    async def create_new_mute_role(self, ctx):
        await ctx.send('{} | Please wait... Setting up...\nThis may take a while if your server has a lot of channels.'.format(ctx.bot.util.loading_emoji))
        role = await ctx.guild.create_role(name='Muted', color=discord.Colour.from_rgb(0, 0, 1))
        ratelimit_counter = 0
        # BEWARE API ABUSE! ADDED SOME STUFF TO REDUCE RATELIMITS
        for i in ctx.guild.channels:
            if ratelimit_counter > 10: # take a break for a while
                await asyncio.sleep(2)
                ratelimit_counter = 0 ; continue
            if i.type == discord.ChannelType.text:
                await i.set_permissions(role, send_messages=False)
            elif i.type == discord.ChannelType.voice:
                await i.set_permissions(role, connect=False)
            else:
                continue
            ratelimit_counter += 1
        ctx.bot.db.Dashboard.editMuteRole(ctx.guild.id, role.id)
        return role

    @command(['jp', 'joinpos', 'joindate', 'jd', 'howold'])
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
        return await wait.edit(content='', embed=discord.Embed(title=title, description=desc, color=ctx.me.color))
        
    @command()
    @cooldown(2)
    async def config(self, ctx):
        data = ctx.bot.db.Dashboard.getData(ctx.guild.id)
        if data is None:
            raise ctx.bot.util.BasicCommandException('This server does not have any configuration for this bot.')
        
        embed = ctx.bot.Embed(
            ctx,
            title=f"Server configuration for {ctx.guild.name}",
            fields={
                "Auto Role": 'Set to <@&{}>'.format(data['autorole']) if data['autorole'] is not None else '<Not set>',
                "Welcome Channel": 'Set to <#{}>'.format(data['welcome']) if data['welcome'] is not None else '<Not set>',
                "Starboard Channel": 'Set to <#{}> (with {} reactions required)'.format(data['starboard'], data['star_requirements']) if data['starboard'] is not None else '<Not set>',
                "Mute Role": 'Set to <@&{}>'.format(data['mute']) if data['mute'] is not None else '<Not set>',
                "Auto-Dehoist": 'Enabled :white_check_mark:' if data['dehoister'] else 'Disabled :x:',
                "Bot Updates Subscription": 'Enabled :white_check_mark:' if data['subscription'] is not None else 'Disabled :x:'
            }
        )
        await embed.send()
        del embed, data
    
    @command()
    @cooldown(5)
    @require_args()
    @permissions(author=['manage_messages'], bot=['manage_roles'])
    async def mute(self, ctx, *args):
        toMute = ctx.bot.Parser.parse_user(ctx, args)
        role = ctx.bot.db.Dashboard.getMuteRole(ctx.guild.id)
        if role is None:
            role = await self.create_new_mute_role(ctx)
        else:
            role = ctx.guild.get_role(role)
        
        try:
            await toMute.add_roles(role)
            embed = ctx.bot.Embed(ctx, title=f"Successfully ductaped {toMute.display_name}'s mouth.", color=discord.Color.green())
            await embed.send()
            del embed, role, toMute
        except:
            raise ctx.bot.util.BasicCommandException('I cannot mute him... maybe i has less permissions than him.\nHis mouth is too powerful to be muted.')
    
    @command()
    @cooldown(5)
    @require_args()
    @permissions(author=['manage_messages'], bot=['manage_roles'])
    async def unmute(self, ctx, *args):
        toUnmute = ctx.bot.Parser.parse_user(ctx, args)
        roleid = ctx.bot.db.Dashboard.getMuteRole(ctx.guild.id)
        if roleid is None:
            raise ctx.bot.util.BasicCommandException('He is not muted!\nOr maybe you muted this on other bot... which is not compatible.')
        elif roleid not in list(map(lambda x: x.id, ctx.message.mentions[0].roles)):
            raise ctx.bot.util.BasicCommandException('That guy is not muted.')
        try:
            await toUnmute.remove_roles(ctx.guild.get_role(roleid))
            embed = ctx.bot.Embed(ctx, title=f"Successfully unmuted {toUnmute.display_name}.", color=discord.Color.green())
            await embed.send()
        except:
            raise ctx.bot.util.BasicCommandException(f'I cannot unmute {toUnmute.display_name}!')
        finally:
            del embed, roleid, toUnmute

    @command(['dehoist'])
    @cooldown(10)
    @permissions(author=['manage_nicknames'], bot=['manage_nicknames'])
    async def dehoister(self, ctx):
        if not ctx.author.guild_permissions.manage_nicknames: raise ctx.bot.util.BasicCommandException('You need the `Manage Nicknames` permissions!')
        data = ctx.bot.db.Dashboard.getDehoister(ctx.guild.id)
        
        embed = ctx.bot.Embed(
            ctx,
            title='Activated Auto-dehoister.',
            desc=f'Auto-Dehoister is an automated part of this bot that automatically renames someone that tries to hoist their name (for example: `!ABC`)\n\n**How do i deactivate this?**\nJust type `{ctx.bot.command_prefix}dehoister`.\n\n**It doesn\'t work for me!**\nMaybe because your role position is higher than me, so i don\'t have the permissions required.'
        ) if (not data) else ctx.bot.Embed(ctx, title="Auto-dehoister deactivated.", color=discord.Color.green())
    
        if not data: 
            ctx.bot.db.Dashboard.setDehoister(ctx.guild, True)
            await embed.send()
            del embed, data
            return
        ctx.bot.db.Dashboard.setDehoister(ctx.guild, False)
        await embed.send()
        del embed, data

    @command()
    @cooldown(10)
    @permissions(author=['manage_channels'], bot=['manage_channels'])
    async def starboard(self, ctx, *args):
        await ctx.trigger_typing()
        _input = ctx.bot.Parser.get_input(args)

        starboard_channel = ctx.bot.db.Dashboard.getStarboardChannel(ctx.guild)
        if len(_input) == 0:
            if starboard_channel['channelid'] is None:
                channel = await ctx.guild.create_text_channel(name='starboard', topic='Server starboard channel. Every funny/cool posts will be here.')
                ctx.bot.db.Dashboard.addStarboardChannel(channel, 1)
                return await ctx.send(embed=discord.Embed(f'Created a channel <#{channel.id}>. Every starboard will be set there.\nTo remove starboard, type `{ctx.bot.command_prefix}starboard --remove`.\nBy default, starboard requirements are set to 1 reaction. To increase, type `{ctx.bot.command_prefix}starboard --limit <number>`.', color=discord.Color.green()))
            
            nl = "\n"
            embed = ctx.bot.Embed(
                ctx,
                title=f'Starboard for {ctx.guild.name}',
                desc='Channel: <#{}>\nStars required to reach: {}'.format(
                    starboard_channel['channelid'], starboard_channel['starlimit']
                ),
                fields={'Commands': f'`{ctx.bot.command_prefix}starboard --remove` **Removes the starboard from this server. (you can also delete the channel yourself)**{nl}`{ctx.bot.command_prefix}starboard --limit <number>` **Changes the amount of star reactions required before a specific message gets to starboard. This defaults to `1` reaction.**'}
            )
            await embed.send()
            del embed, nl
        
        if starboard_channel['channelid'] is None:
            return
        elif "--remove" in _input:
            ctx.bot.db.Dashboard.removeStarboardChannel(ctx.guild)
            return await ctx.send(embed=discord.Embed(title='Alright. Starboard for this server is deleted. You can delete the channel.', color=discord.Color.green()))
        elif "--limit" in _input:
            try:
                num = args[args.index("--limit") + 1]
                assert num.isnumeric()
                ctx.bot.db.Dashboard.setStarboardLimit(num, ctx.guild)
                await ctx.send(embed=discord.Embed(title=f'OK. Changed the limit to {num} star reactions.', color=discord.Color.green()))
            except:
                raise ctx.bot.util.BasicCommandException('Invalid number.')
    
    @command()
    @cooldown(5)
    @require_args()
    @permissions(author=['manage_messages'])
    async def warn(self, ctx, *args):
        params = ctx.bot.Parser.split_args(args)
        user_to_warn = ctx.bot.Parser.parse_user(ctx, args[0] if params is None else params[0], allownoargs=False)
        
        if user_to_warn.guild_permissions.manage_channels:
            raise ctx.bot.util.BasicCommandException("You cannot warn a moderator.")
        reason = 'No reason provided' if (params is None) else params[1][0:100]

        warned = ctx.bot.db.Dashboard.addWarn(user_to_warn, ctx.author, reason)
        if warned:
            return await ctx.send(embed=discord.Embed(title=f'{user_to_warn.display_name} was warned by {ctx.author.display_name} for the reason *"{reason}"*.', color=discord.Color.green()))
        raise ctx.bot.util.BasicCommandException("an error occured.")
    
    @command(['warns', 'warnslist', 'warn-list', 'infractions'])
    @cooldown(5)
    @require_args()
    async def warnlist(self, ctx, *args):
        source = ctx.bot.Parser.parse_user(ctx, args)
        data = ctx.bot.db.Dashboard.getWarns(source)
        if not data:
            return await ctx.send(embed=discord.Embed(title=f"{source.display_name} does not have any warns!", color=discord.Color.green()))
        warnlist = '\n'.join(map(
            lambda x: '{}. "{}" (warned by <@{}>)'.format(x+1, data[x]['reason'], data[x]['moderator']),
            range(len(data))
        )[0:10])
        embed = ctx.bot.Embed(
            ctx,
            title=f'Warn list for {source.display_name}',
            desc=warnlist,
            color=discord.Colour.red()
        )
        await embed.send()
        del embed, warnlist, source, data
    
    @command(['deletewarn', 'clear-all-infractions', 'clear-infractions', 'clearinfractions', 'delinfractions', 'delwarn', 'clearwarn', 'clear-warn'])
    @cooldown(5)
    @require_args()
    @permissions(author=['manage_messages'])
    async def unwarn(self, ctx, *args):
        user_to_unwarn = ctx.bot.Parser.parse_user(ctx, args)
        unwarned = ctx.bot.db.Dashboard.clearWarn(user_to_unwarn)
        if unwarned:
            return await ctx.send(embed=discord.Embed(title=f"Successfully unwarned {user_to_unwarn.display_name}.", color=discord.Color.green()))
        return await ctx.send(embed=discord.Embed(title=f"Well, {user_to_warn.display_name} is not warned ***yet***...", color=discord.Color.red()))

    @command(['welcomelog', 'setwelcome'])
    @cooldown(15)
    @permissions(author=['manage_channels'])
    async def welcome(self, ctx, *args):
        if len(args)==0:
            embed = ctx.bot.Embed(
                ctx,
                title='Command usage',
                desc=f'{ctx.bot.command_prefix}welcome <CHANNEL>'+'\n'+f'{ctx.bot.command_prefix}welcome disable'
            )
            await embed.send()
            del embed, args
            return
        if args[0].lower() == 'disable':
            ctx.bot.db.Dashboard.set_welcome(ctx.guild.id, None)
            return await ctx.send(embed=discord.Embed(title="Welcome channel disabled for this server!", color=discord.Color.green()))
        try:
            if args[0].startswith("<#") and args[0].endswith('>'):
                channelid = int(args[0].split('<#')[1].split('>')[0])
            else:
                channelid = int([i.id for i in ctx.guild.channels if str(i.name).lower()==str(''.join(args)).lower()][0])
            ctx.bot.db.Dashboard.set_welcome(ctx.guild.id, channelid)
            return await ctx.send(embed=discord.Embed(title=f"Success! set the welcome log to <#{channelid}>!", color=discord.Color.green()))
        except:
            raise ctx.bot.util.BasicCommandException("Invalid arguments!")
    
    @command(['auto-role', 'welcome-role', 'welcomerole'])
    @cooldown(12)
    @permissions(author=['manage_roles'], bot=['manage_roles'])
    async def autorole(self, ctx, *args):
        if len(args)==0:
            embed = ctx.bot.Embed(
                ctx,
                title='Command usage',
                desc=f'`{ctx.bot.command_prefix}autorole <role>`'+'\n'+f'`{ctx.bot.command_prefix}autorole disable`'
            )
            await embed.send()
            del embed, args
            return
        
        if args[0].lower() == 'disable':
            ctx.bot.db.Dashboard.set_autorole(ctx.guild.id, None)
            return await ctx.send(embed=discord.Embed(title="Autorole disabled for this server!", color=discord.Color.green()))
        try:
            if args[0].startswith("<@&") and args[0].endswith('>'):
                roleid = int(args[0].split('<@&')[1].split('>')[0])
            else:
                roleid = int([i.id for i in ctx.guild.roles if str(i.name).lower()==' '.join(args).lower()][0])
            
            ctx.bot.db.Dashboard.set_autorole(ctx.guild.id, roleid)
            return await ctx.send(embed=discord.Embed(title=f"Success! set the autorole to <@&{roleid}>!", color=discord.Color.green()))
        except:
            raise ctx.bot.util.BasicCommandException("Invalid arguments!")
    
    @command()
    @cooldown(10)
    @require_args()
    @permissions(author=['manage_channels'], bot=['manage_channels'])
    async def slowmode(self, ctx, *args):
        try:
            assert args[0].isnumeric(), "Please add the time in seconds. (number)"
            count = int(args[0])
            assert count in range(21599), "Invalid range."
            await ctx.channel.edit(slowmode_delay=count)
            return await ctx.send(embed=discord.Embed(title=("Disabled channel slowmode." if (count == 0) else f"Successfully set slowmode for <#{ctx.channel.id}> to {count} seconds."), color=discord.Color.green()))
        except Exception as e:
            raise ctx.bot.util.BasicCommandException(str(e))
            
    @command(['ar', 'add-role'])
    @cooldown(10)
    @require_args(2)
    @permissions(author=['manage_roles'], bot=['manage_roles'])
    async def addrole(self, ctx, *args):
        role_and_guy = ctx.bot.Parser.split_args(args)
        
        guy = ctx.bot.Parser.parse_user(ctx, role_and_guy[0])
        try:
            role = ctx.guild.get_role(int(role_and_guy[0].split("<@&")[1].split(">")[0]))
        except:
            role_array = [i for i in ctx.guild.roles if role_and_guy[1].lower() in i.name.lower()]
            if len(role_array) == 0:
                raise ctx.bot.util.BasicCommandException(f"Role `{role_and_guy[1]}` does not exist.")
            role = role_array[0]
            del role_array
        try:
            await guy.add_roles(role_array[0])
            return await ctx.send(embed=discord.Embed(title=f"Successfully added <@&{role.id}> role to {guy.display_name}!", color=discord.Color.green()))
        except:
            raise ctx.bot.util.BasicCommandException(f"Oops. Please make sure i have the manage roles perms.")
    
    @command(['rr', 'remove-role'])
    @cooldown(10)
    @require_args(2)
    @permissions(author=['manage_roles'], bot=['manage_roles'])
    async def removerole(self, ctx, *args):
        role_and_guy = ctx.bot.Parser.split_args(args)
        
        try:
            role = ctx.guild.get_role(int(role_and_guy[0].split("<@&")[1].split(">")[0]))
        except:
            role_array = [i for i in ctx.guild.roles if role_and_guy[1].lower() in i.name.lower()]
            if len(role_array) == 0:
                raise ctx.bot.util.BasicCommandException(f"Role `{role_and_guy[1]}` does not exist.")
            role = role_array[0]
            del role_array
        try:
            await guy.remove_roles(role)
            return await ctx.send(embed=discord.Embed(title=f"Successfully removed <@&{role.id}> role from {guy.display_name}!", color=discord.Color.green()))
        except:
            raise ctx.bot.util.BasicCommandException("Oops. Please make sure i have the manage roles perms.")

    @command()
    @cooldown(10)
    @require_args()
    @permissions(author=["ban_members"], bot=["ban_members"])
    async def ban(self, ctx, *args):
        await ctx.trigger_typing()
        user = ctx.bot.Parser.parse_user(ctx, args)
        if user == ctx.author:
            raise ctx.bot.util.BasicCommandException("You can't ban yourself idiot.")
        elif user.guild_permissions.manage_messages:
            raise ctx.bot.util.BasicCommandException("That guy is a mod. You can't do this to a mod.")

        try:
            await ctx.guild.ban(user)
            return await ctx.send(embed=discord.Embed(title=f"Bonked {user.display_name} from this server.", color=discord.Color.green()))
        except:
            raise ctx.bot.util.BasicCommandException(f"Please make sure my role is higher so i can ban {user.display_name}.")    

    @command()
    @cooldown(10)
    @require_args()
    @permissions(author=["kick_members"], bot=["kick_members"])
    async def kick(self, ctx, *args):
        await ctx.trigger_typing()
        user = ctx.bot.Parser.parse_user(ctx, args)
        if user == ctx.author:
            raise ctx.bot.util.BasicCommandException("You can't kick yourself idiot.")
        elif user.guild_permissions.manage_messages:
            raise ctx.bot.util.BasicCommandException("That guy is a mod. You can't do this to a mod.")

        try:
            await ctx.guild.kick(user)
            return await ctx.send(embed=discord.Embed(title=f"Kicked {user.display_name} out from this server.", color=discord.Color.green()))
        except:
            raise ctx.bot.util.BasicCommandException(f"Please make sure my role is higher so i can kick {user.display_name}.")    

    @command(['purge'])
    @cooldown(2)
    @require_args()
    @permissions(author=['manage_messages'], bot=['manage_messages'])
    async def clear(self, ctx, *args):
        try:
            assert (len(ctx.message.mentions) > 0 or args[0].isnumeric()), 'Please input a valid parameter. Either a number or a mention.'
            mention = True if len(ctx.message.mentions)>0 else False
            try: await ctx.message.delete()
            except: pass
            if not mention:
                num = int(args[0])
                assert (num in range(1, 301)), "Invalid arguments, out of range. Must be around 1 and 300."
                await ctx.channel.purge(limit=num)
                return await ctx.send(embed=discord.Embed(title=f"Successfully purged {num} messages.", color=discord.Color.green()), delete_after=3)
            deleted_messages = await ctx.channel.purge(check=(lambda x: x.channel == ctx.channel and x.author == ctx.message.mentions[0]), limit=500)
            return await ctx.send(embed=discord.Embed(title=f"Successfully purged {len(deleted_messages)} messages.", color=discord.Color.green()), delete_after=3)
        except Exception as e:
            raise ctx.bot.util.BasicCommandException(str(e))
                
    @command(['lock', 'lockchannel', 'lock-channel'])
    @cooldown(7)
    @require_args()
    @permissions(author=['manage_messages'], bot=['manage_channels'])
    async def lockdown(self, ctx, *args):
        enable = (not args[0].lower() in ['yes', 'y', 'enable', 'true', 'enabled', 'on'])
        await ctx.channel.set_permissions(ctx.guild.default_role, send_messages=enable)
        try:
            await ctx.send(embed=discord.Embed(title=f"Successfully {'Locked' if enable else 'Re-opened'} the channel.", description=f"All members with the default role {'can send messages in this channel again.' if enable else 'cannot send messages in this channel'}." + "\nType `" + ctx.bot.command_prefix + f"lock {'enable' if enable else 'disable'}` to {'enable' if enable else 'disable'} this effect again.", color=discord.Color.green()))
        except: return
    
    @command(['hide', 'hide-channel'])
    @cooldown(7)
    @require_args()
    @permissions(author=['manage_messages'], bot=['manage_channels'])
    async def hidechannel(self, ctx, *args):
        enable = (not args[0].lower() in ['yes', 'y', 'enable', 'true', 'enabled', 'on'])
        await ctx.channel.set_permissions(ctx.guild.default_role, read_messages=enable)
        try:
            await ctx.send(embed=discord.Embed(title=f"Successfully {'Hide' if enable else 'Re-opened'} the channel.", description=f"All members with the default role {'can see messages in this channel again.' if enable else 'cannot read messages in this channel/see messages in this channel'}." + "\nType `" + ctx.bot.command_prefix + f"hide {'enable' if enable else 'disable'}` to {'enable' if enable else 'disable'} this effect again.", color=discord.Color.green()))
        except: return
    
    @command(['guild-role', 'server-role'])
    @cooldown(6)
    @require_args()
    async def role(self, ctx, *args):
        if args[0].lower() == 'info':
            try:
                role = ctx.bot.Parser.parse_role(ctx, ' '.join(args[1:]), return_array=True)
                assert (role is not None)
            except:
                raise ctx.bot.util.BasicCommandException(f"Please add role name/mention/ID after the `{ctx.bot.command_prefix}role info`.")
            if isinstance(role, list):
                choose = ctx.bot.ChooseEmbed(ctx, role, key=(lambda x: x.mention))
                res = await choose.run()
                if not res:
                    return
                role = res
            
            role_members = "\n".join([f"{i.name}#{i.discriminator}" for i in role.members][0:10]) if len(role.members) > 0 else "<none>"
            extra = "\n" + f"... and {len(role.members) - 10} others" if len(role.members) > 10 else ""
            permissions = ""
            
            for perm in self.permission_attributes:
                if len(permissions) > 500:
                    break
                
                if getattr(role.permissions, perm):
                    permissions += perm.replace("_", " ") + ", "
            
            embed = ctx.bot.Embed(
                ctx,
                title=role.name,
                color=role.color,
                fields={
                    "Role Info": f"**Display role members seperately from online members: **{':white_check_mark:' if role.hoist else ':x:'}" + "\n" + f"**Mentionable: **{':white_check_mark:' if role.mentionable else ':x:'}" + f"\n**Created At: **{str(role.created_at)[:-7]}",
                    f"Role Members ({len(role.members)})": role_members + extra,
                    "Key Permissions": permissions[:-2],
                    "Role Color": f"**Hex: {str(role.color)}**" + "\n" + f"**RGB: **{role.color.r}, {role.color.g}, {role.color.b}"
                }
            )
            await embed.send()
            del embed, role_members, extra, role, permissions
            return
        elif args[0].lower() == "list":
            embed = ctx.bot.Embed(ctx, title="Server Roles List", description=" ".join([i.mention for i in ctx.guild.roles[1:]])[0:1000])
            await embed.send()
            del embed
            return
        raise ctx.bot.util.BasicCommandException(f"Usage: `{ctx.bot.command_prefix}role info <role>` or `{ctx.bot.command_prefix}role list`")
    
    @command(['guild-channel', 'server-channel'])
    @cooldown(6)
    @require_args()
    async def channel(self, ctx, *args):
        if args[0].lower() == "list":
            embed = ctx.bot.Embed(ctx, title="Server Channels List", description=" ".join([f"<#{i.id}>" for i in ctx.guild.channels if i.type == discord.ChannelType.text or i.type == discord.ChannelType.voice])[0:1000])
            await embed.send()
            del embed
            return
        elif args[0].lower() == "info":
            try:
                channel = ctx.bot.Parser.parse_channel(ctx, ' '.join(args[1:]), return_array=True)
                assert (channel is not None)
            except:
                raise ctx.bot.util.BasicCommandException(f"Please add a valid channel name/ID after `{ctx.bot.command_prefix}channel info`")
            if isinstance(channel, list):
                choose = ctx.bot.ChooseEmbed(ctx, channel, key=(lambda x: f"[`{str(x.type)}`] {x.name}"))
                res = await choose.run()
                if not res:
                    return
                channel = res
        
            # PYTHON SHOULD HAVE A SWITCH STATEMENT
            if channel.type == discord.ChannelType.text:
                fields = {
                    "Channel Category": channel.category.name if channel.category else "<no category>",
                    "Channel Info": f"**Channel ID: **{channel.id}" + "\n" + f"**Channel Topic: **{channel.topic if channel.topic else '<not available>'}" + "\n" + f"**Slowmode Delay: **{channel.slowmode_delay} seconds.",
                    "Channel Type": "Discord Text Channel"
                }
            elif channel.type == discord.ChannelType.voice:
                channel_members = "\n".join([f"{i.name}#{i.discriminator}" for i in channel.members[:5]]) if len(channel.members) > 0 else "<no members in VC>"
                other = "\n" + f"... and {len(channel.members) - 5} others" if len(channel.members) > 5 else ""
                fields = {
                    "Channel Category": channel.category.name if channel.category else "<no category>",
                    "Channel Info": f"**Channel ID: **{channel.id}" + "\n" + f"**Bitrate: **{channel.bitrate // 1000} kbps",
                    f"VC Members ({len(channel.members)}/{channel.user_limit if channel.user_limit != 0 else '∞'})": channel_members + other,
                    "Channel Type": "Discord Voice Channel (VC)"
                }
            elif channel.type == discord.ChannelType.category:
                channels = "\n".join([i.name for i in channel.channels]) if len(channel.channels) > 0 else "<no channels>"
                fields = {
                    "Channel Type": "Discord Category Channel",
                    f"Channels ({len(channel.channels)})": channels[:1000]
                }
            else:
                raise ctx.bot.util.BasicCommandException("Invalid channel type. Must be either Text, voice, or category channel.")
            
            embed = ctx.bot.Embed(
                ctx,
                title=channel.name,
                fields=fields
            )
            await embed.send()
            del embed, channel
            return
        raise ctx.bot.util.BasicCommandException(f"Usage: `{ctx.bot.command_prefix}channel list` or `{ctx.bot.command_prefix}channel info <channel>`")

    @command(['ui', 'user', 'usercard', 'user-info', 'user-card', 'whois', 'user-interface', 'userinterface'])
    @cooldown(3)
    async def userinfo(self, ctx, *args):
        guy, nitro = ctx.bot.Parser.parse_user(ctx, args), False
        await ctx.trigger_typing()
        if guy in ctx.guild.premium_subscribers: nitro = True
        elif guy.is_avatar_animated(): nitro = True
        booster = True if guy in ctx.guild.premium_subscribers else False
        booster_since = round(t.now().timestamp() - guy.premium_since.timestamp()) if guy.premium_since is not None else False
        bg_col = await ctx.bot.canvas.get_color_accent(ctx, str(guy.avatar_url_as(format="png")))
        data = await ctx.bot.canvas.usercard(list(map(lambda x: {
            'name': x.name, 'color': x.color.to_rgb()
        }, guy.roles))[::-1][0:5], guy, str(guy.avatar_url_as(format="png")), bg_col, nitro, booster, booster_since)
        return await ctx.send(file=discord.File(data, str(guy.discriminator)+'.png'))

    @command(['av', 'ava'])
    @cooldown(2)
    async def avatar(self, ctx, *args):
        url = await ctx.bot.Parser.parse_image(ctx, args, default_to_png=False, cdn_only=True, member_only=True, size=4096)
        embed = ctx.bot.Embed(ctx, title="Here's ya avatar mate", image=url)
        await embed.send()
        del embed, url

    @command(['emote', 'emojiinfo', 'emoji-info'])
    @cooldown(5)
    @require_args()
    async def emoji(self, ctx, *args):
        if args[0].lower() == "list":
            if len(ctx.guild.emojis)==0:
                raise ctx.bot.util.BasicCommandException('This server has no emojis!')
            emojis, footer_text = "", None
            for index, emoji in enumerate(ctx.guild.emojis):
                if len(emojis) >= 1975:
                    footer_text = f"...and other {len(ctx.guild.emojis) - index} custom emojis (too much to display)"
                    break
                emojis += str(emoji) + " "
            embed = ctx.bot.Embed(ctx, title="Server Custom Emojis List")
        elif args[0].lower() == "info":
            try:
                res = await ctx.bot.Parser.parse_emoji(ctx, args[1])
                assert (res is not None)
            except:
                raise ctx.bot.util.BasicCommandException(f"Please add a emoji after the `{ctx.bot.command_prefix}emoji info`")
            data = ctx.bot.get_emoji(int(res.split("emojis/")[1].split(".")[0])) if res.startswith("https://cdn") else None
            
            fields = {
                "Emoji name": data.name if data else "`<not available>`",
                "Emoji ID": data.id if data else "`<not available>`",
                "Emoji creation date": str(data.created_at)[:-7] if data else "`not available`",
                "Emoji type": "Discord Animated Custom Emoji" if (data and data.animated) else "Discord Custom Emoji",
                "Emoji source": f"{data.guild.name} ({len(data.guild.emojis)}/{data.guild.emoji_limit} custom emojis)" if (data and data.guild) else "`<source not available>`",
                "Emoji URL": res
            } if res.startswith("https://cdn") else {
                "Emoji type": "Default Discord Emoji", 
                "Emoji URL": res
            }
            
            embed = ctx.bot.Embed(
                ctx,
                title="Emoji Info",
                fields=fields,
                image=res
            )
            await embed.send()
            del embed, fields, data, res
            return
        elif args[0].lower() == "enlarge":
            try:
                res = await ctx.bot.Parser.parse_emoji(ctx, args[1])
                assert (res is not None)
            except:
                raise ctx.bot.util.BasicCommandException(f"Please add a emoji after the `{ctx.bot.command_prefix}emoji enlarge`")
            return await ctx.bot.util.send_image_attachment(ctx, res)
        return await ctx.send(embed=discord.Embed(title="Invalid Arguments", description="Valid parameters: `list`, `info <emoji>`, `enlarge <emoji>`", color=discord.Color.red()))

    @command(['serverinfo', 'server', 'servericon', 'si', 'server-info', 'guild', 'guildinfo', 'guild-info'])
    @cooldown(10)
    async def servercard(self, ctx, *args):
        if ctx.bot.util.get_command_name(ctx) == "servericon":
            if ctx.guild.icon_url is None: raise ctx.bot.util.BasicCommandException("This server has no emotes...")
            await ctx.send(ctx.guild.icon_url_as(size=4096))
        else:
            if ctx.guild.member_count>100:
                wait = await ctx.send('{} | Fetching guild data... please wait...'.format(ctx.bot.util.loading_emoji))
                im = await ctx.bot.canvas.server(ctx.guild)
                await wait.delete()
            else:
                await ctx.channel.trigger_typing()
                im = await ctx.bot.canvas.server(ctx.guild)
            await ctx.send(file=discord.File(im, 'server.png'))
            del im
    
    @command(['perms', 'perm', 'permission', 'permfor', 'permsfor', 'perms-for', 'perm-for'])
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

def setup(client):
    client.add_cog(moderation())