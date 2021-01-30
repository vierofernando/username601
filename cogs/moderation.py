import discord
from discord.ext import commands
import time
from random import randint, choice
import asyncio
from aiohttp import ClientSession
from decorators import *
from time import time
from twemoji_parser import emoji_to_url

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
        self.presence_prefix = {
            discord.ActivityType.listening: "Listening to ",
            discord.ActivityType.watching: "Watching ",
            discord.ActivityType.playing: "Playing ",
            discord.ActivityType.streaming: "Streaming ",
            discord.ActivityType.competing: "Competing in"
        }
        self.db = client.db

    async def create_new_mute_role(self, ctx):
        await ctx.send('{} | Please wait... Setting up...\nThis may take a while if your server has a lot of channels.'.format(ctx.bot.util.loading_emoji))
        role = await ctx.guild.create_role(name='Muted', color=discord.Color.from_rgb(0, 0, 1))
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
        
        # add to database
        if not self.db.exist("dashboard", {"serverid": ctx.guild.id}):
            self.db.add("dashboard", {
                "serverid": guild.id,
                "mute": role.id,
                "warns": []
            })
        else:
            self.db.modify("dashboard", self.db.types.CHANGE, {"serverid": ctx.guild.id}, {"mute": role.id})
        
        return role

    @command(['jp', 'joinpos', 'joindate', 'jd', 'howold'])
    @cooldown(5)
    async def joinposition(self, ctx, *args):
        await ctx.trigger_typing()
        from_string = False
        current_time, members, user_index, desc = time(), ctx.guild.members, None, ""
        full_arr = list(map(lambda x: {'ja': x.joined_at.timestamp(), 'da': x}, members))
        raw_unsorted_arr = list(map(lambda x: x['ja'], full_arr))
        sorted_arr = sorted(raw_unsorted_arr)
        if args and (not args[0].isnumeric()):
            if args[0].lower() in self.first:
                from_string, user_index, title = True, 0, f'User join position for the first member in {ctx.guild.name}'
            elif args[0].lower() in self.latest:
                from_string, user_index, title = True, ctx.guild.member_count - 1, f'User join position for the latest member to join {ctx.guild.name}'
        
        if not from_string:
            if args and args[0].isnumeric() and ((int(args[0])-1) in range(len(members))):
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
        return await ctx.send(embed=discord.Embed(title=title, description=desc, color=ctx.me.color))
        
    @command()
    @cooldown(2)
    async def config(self, ctx):
        data = self.db.get("dashboard", {"serverid": ctx.guild.id})
        if not data:
            raise ctx.error_message('This server does not have any configuration for this bot.')
        
        await ctx.embed(title=f"Server configuration for {ctx.guild.name}", fields={
            "Auto Role": 'Set to <@&{}>'.format(data['autorole']) if data.get('autorole') else '<Not set>',
            "Welcome Channel": 'Set to <#{}>'.format(data['welcome']) if data.get('welcome') else '<Not set>',
            "Mute Role": 'Set to <@&{}>'.format(data['mute']) if data.get('mute') else '<Not set>',
            "Auto-Dehoist": 'Enabled :white_check_mark:' if data.get('dehoister') else 'Disabled :x:'
        })
        del data
    
    @command()
    @cooldown(5)
    @require_args()
    @permissions(author=['manage_messages'], bot=['manage_roles'])
    async def mute(self, ctx, *args):
        toMute = ctx.bot.Parser.parse_user(ctx, args)
        server = self.db.get("dashboard", {"serverid": ctx.guild.id})
        if server and server.get("mute"):
            role = ctx.guild.get_role(server["mute"])
        else:
            role = await self.create_new_mute_role(ctx)

        try:
            await toMute.add_roles(role)
            await ctx.success_embed(f"Successfully ductaped {toMute.display_name}'s mouth.")
            del role, toMute
        except:
            raise ctx.error_message('I cannot mute him... maybe i has less permissions than him.\nHis mouth is too powerful to be muted.')
    
    @command()
    @cooldown(5)
    @require_args()
    @permissions(author=['manage_messages'], bot=['manage_roles'])
    async def unmute(self, ctx, *args):
        toUnmute = ctx.bot.Parser.parse_user(ctx, args)
        roleid = self.db.get("dashboard", {"serverid": ctx.guild.id})
        if (not roleid) or (not roleid.get("mute")):
            raise ctx.error_message('He is not muted!\nOr maybe you muted this on other bot... which is not compatible.')
        elif roleid not in list(map(lambda x: x.id, toUnmute)):
            raise ctx.error_message('That guy is not muted.')
        
        try:
            await toUnmute.remove_roles(ctx.guild.get_role(roleid))
            await ctx.success_embed(f"Successfully unmuted {toUnmute.display_name}.")
        except:
            raise ctx.error_message(f'I cannot unmute {toUnmute.display_name}!')
        finally:
            del roleid, toUnmute

    @command(['dehoist'])
    @cooldown(10)
    @permissions(author=['manage_nicknames'], bot=['manage_nicknames'])
    async def dehoister(self, ctx):
        data = self.db.get("dashboard", {"serverid": ctx.guild.id})
        
        embed = ctx.bot.Embed(
            ctx,
            title='Activated Auto-dehoister.',
            description=f'Auto-Dehoister is an automated part of this bot that automatically renames someone that tries to hoist their name (for example: `!ABC`)\n\n**How do i deactivate this?**\nJust type `{ctx.prefix}dehoister`.\n\n**It doesn\'t work for me!**\nMaybe because your role position is higher than me, so i don\'t have the permissions required.'
        ) if ((not data) or (not data.get("dehoister"))) else ctx.bot.Embed(ctx, title="Auto-dehoister deactivated.", color=discord.Color.green())
    
        if (not data) or (not data.get("dehoister")): 
            await embed.send()

            if not data:
                self.db.add("dashboard", {
                    "serverid": ctx.guild.id,
                    "warns": [],
                    "dehoister": True
                })
            else:
                self.db.modify("dashboard", self.db.types.CHANGE, {"serverid": ctx.guild.id}, {"dehoister": True})
            
            del embed, data
            return
        
        await embed.send()
        self.db.modify("dashboard", self.db.types.CHANGE, {"serverid": ctx.guild.id}, {"dehoister": False})
        del embed, data
        
    @command()
    @cooldown(5)
    @require_args()
    @permissions(author=['manage_messages'])
    async def warn(self, ctx, *args):
        params = ctx.bot.Parser.split_args(args)
        user_to_warn = ctx.bot.Parser.parse_user(ctx, (params[0] if params else args[0]))
        
        if user_to_warn.guild_permissions.manage_channels:
            raise ctx.error_message("You cannot warn a moderator.")
        reason = params[1][:100] if params else 'No reason provided'

        await ctx.success_embed(f'{user_to_warn.display_name} was warned by {ctx.author.display_name} for the reason *"{reason}"*.')
        if not self.db.exist("dashboard", {"serverid": ctx.guild.id}):
            self.db.add("dashboard", {
                "serverid": ctx.guild.id,
                "warns": [f"{user_to_warn.id}.{ctx.author.id}.{reason}"]
            })
        else:
            self.db.modify("dashboard", self.db.types.APPEND, {"serverid": ctx.guild.id}, {"warns": f"{user_to_warn.id}.{ctx.author.id}.{reason}"})
    
    @command(['warns', 'warnslist', 'warn-list', 'infractions'])
    @cooldown(5)
    @require_args()
    async def warnlist(self, ctx, *args):
        source = ctx.bot.Parser.parse_user(ctx, args)
        data = self.db.get("dashboard", {"serverid": ctx.guild.id})
        if (not data) or (source.id not in [int(i.split(".")[0]) for i in data["warns"]]):
            return await ctx.success_embed(f"{source.display_name} does not have any warns!")
        
        data = [i for i in data["warns"] if source.id == int(i.split(".")[0])]
        warnlist = '\n'.join(map(
            lambda x: '{}. "{}" (warned by <@{}>)'.format(x+1, ".".join(data[x].split(".")[2:]), data[x].split(".")[1]),
            range(len(data))
        )[:10])

        await ctx.embed(title=f'Warn list for {source.display_name}', description=warnlist, color=discord.Color.red())
        del warnlist, source, data
    
    @command(['deletewarn', 'clear-all-infractions', 'clear-infractions', 'clearinfractions', 'delinfractions', 'delwarn', 'clearwarn', 'clear-warn'])
    @cooldown(5)
    @require_args()
    @permissions(author=['manage_messages'])
    async def unwarn(self, ctx, *args):
        await ctx.trigger_typing()
        user_to_unwarn = ctx.bot.Parser.parse_user(ctx, args)
        data = self.db.get("dashboard", {"serverid": ctx.guild.id})

        try:
            is_warned = (user_to_unwarn.id in [int(i.split(".")[0]) for i in data["warns"]])
        except:
            is_warned = False

        if (not data) or (not is_warned):
            raise ctx.error_message(f"Well, {user_to_unwarn.display_name} is not warned ***yet***...")
        modified_array = [i for i in data["warns"] if user_to_unwarn.id != int(i.split(".")[0])]
        await ctx.success_embed(f"Successfully cleared all warns for {user_to_unwarn.display_name}.")
        self.db.modify("dashboard", self.db.types.CHANGE, {"serverid": ctx.guild.id}, {"warns": modified_array})

    @command(['welcomelog', 'setwelcome'])
    @cooldown(15)
    @permissions(author=['manage_channels'])
    async def welcome(self, ctx, *args):
        data = self.db.get("dashboard", {"serverid": ctx.guild.id})

        if not args:
            await ctx.embed(title='Command usage', description=f'{ctx.prefix}welcome <channel>'+'\n'+f'{ctx.prefix}welcome disable')
            del args
            return
        
        if args[0].lower() == 'disable':
            if (not data) or (not data.get("welcome")):
                raise ctx.error_message("This server does not have any welcome channels se")
            await ctx.success_embed("Welcome channel disabled for this server!")
            self.db.modify("dashboard", self.db.types.REMOVE, {"serverid": ctx.guild.id}, {"welcome": data["welcome"]})
            return

        try:
            channelid = ctx.bot.Parser.parse_channel(ctx, ' '.join(args)).id
            await ctx.success_embed(f"Success! set the welcome log to <#{channelid}>!")
            if not data:
                self.db.add("dashboard", {
                    "serverid": ctx.guild.id,
                    "warns": [],
                    "welcome": channelid
                })
            else:
                self.db.modify("dashboard", self.db.types.CHANGE, {"serverid": ctx.guild.id}, {"welcome": channelid})
        except:
            return await ctx.bot.cmds.invalid_args(ctx)
    
    @command(['auto-role', 'welcome-role', 'welcomerole'])
    @cooldown(12)
    @require_args()
    @permissions(author=['manage_roles'], bot=['manage_roles'])
    async def autorole(self, ctx, *args):
        data = self.db.get("dashboard", {"serverid": ctx.guild.id})
        
        if args[0].lower() == 'disable':
            if (not data) or (not data.get("autorole")):
                raise ctx.error_message("This server does not have any Auto Role set!")
            
            await ctx.success_embed("OK! Autorole is disabled for this server!")
            self.db.modify("dashboard", self.db.types.REMOVE, {"serverid": ctx.guild.id}, {"autorole": data["autorole"]})
            return

        try:
            roleid = ctx.bot.Parser.parse_role(ctx, ' '.join(args)).id
            await ctx.success_embed(f"Success! set the autorole to <@&{roleid}>!")
            if not data:
                self.db.add("dashboard", {
                    "serverid": ctx.guild.id,
                    "warns": [],
                    "autorole": roleid
                })
            else:
                self.db.modify("dashboard", self.db.types.CHANGE, {"serverid": ctx.guild.id}, {"autorole": roleid})
        except:
            return await ctx.bot.cmds.invalid_args(ctx)
    
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
            return await ctx.success_embed(("Disabled channel slowmode." if (count == 0) else f"Successfully set slowmode for <#{ctx.channel.id}> to {count} seconds."))
        except Exception as e:
            raise ctx.error_message(str(e))
            
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
            if not role_array:
                raise ctx.error_message(f"Role `{role_and_guy[1]}` does not exist.")
            role = role_array[0]
            del role_array
        try:
            await guy.add_roles(role_array[0])
            return await ctx.success_embed(f"Successfully added <@&{role.id}> role to {guy.display_name}!")
        except:
            raise ctx.error_message(f"Oops. Please make sure i have the manage roles perms.")
    
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
            if not role_array:
                raise ctx.error_message(f"Role `{role_and_guy[1]}` does not exist.")
            role = role_array[0]
            del role_array
        try:
            await guy.remove_roles(role)
            return await ctx.success_embed(f"Successfully removed <@&{role.id}> role from {guy.display_name}!")
        except:
            raise ctx.error_message("Oops. Please make sure i have the manage roles perms.")

    @command()
    @cooldown(10)
    @require_args()
    @permissions(author=["ban_members"], bot=["ban_members"])
    async def ban(self, ctx, *args):
        await ctx.trigger_typing()
        user = ctx.bot.Parser.parse_user(ctx, args)
        if user == ctx.author:
            raise ctx.error_message("You can't ban yourself idiot.")
        elif user.guild_permissions.manage_messages:
            raise ctx.error_message("That guy is a mod. You can't do this to a mod.")

        try:
            await ctx.guild.ban(user)
            return await ctx.success_embed(f"Bonked {user.display_name} from this server.")
        except:
            raise ctx.error_message(f"Please make sure my role is higher so i can ban {user.display_name}.")    

    @command()
    @cooldown(10)
    @require_args()
    @permissions(author=["kick_members"], bot=["kick_members"])
    async def kick(self, ctx, *args):
        await ctx.trigger_typing()
        user = ctx.bot.Parser.parse_user(ctx, args)
        if user == ctx.author:
            raise ctx.error_message("You can't kick yourself idiot.")
        elif user.guild_permissions.manage_messages:
            raise ctx.error_message("That guy is a mod. You can't do this to a mod.")

        try:
            await ctx.guild.kick(user)
            return await ctx.success_embed(f"Kicked {user.display_name} out from this server.")
        except:
            raise ctx.error_message(f"Please make sure my role is higher so i can kick {user.display_name}.")    

    @command(['purge'])
    @cooldown(2)
    @require_args()
    @permissions(author=['manage_messages'], bot=['manage_messages'])
    async def clear(self, ctx, *args):
        try:
            assert (ctx.message.mentions or args[0].isnumeric()), 'Please input a valid parameter. Either a number or a mention.'
            mention = bool(ctx.message.mentions)
            try: await ctx.message.delete()
            except: pass
            if not mention:
                num = int(args[0])
                assert (num in range(1, 301)), "Invalid arguments, out of range. Must be around 1 and 300."
                await ctx.channel.purge(limit=num)
                return await ctx.success_embed(f"Successfully purged {num} messages.", delete_after=3)
            deleted_messages = await ctx.channel.purge(check=(lambda x: x.channel == ctx.channel and x.author == ctx.message.mentions[0]), limit=500)
            return await ctx.success_embed(f"Successfully purged {len(deleted_messages):,} messages.", delete_after=3)
        except Exception as e:
            raise ctx.error_message(str(e))
                
    @command(['lockdown', 'lockchannel', 'lock-channel'])
    @cooldown(7)
    @require_args()
    @permissions(author=['manage_messages'], bot=['manage_channels'])
    async def lock(self, ctx, *args):
        enable = (not args[0].lower() in ['yes', 'y', 'enable', 'true', 'enabled', 'on'])
        await ctx.channel.set_permissions(ctx.guild.default_role, send_messages=enable)
        try:
            await ctx.success_embed(f"Successfully {'Locked' if enable else 'Re-opened'} the channel.", description=f"All members with the default role {'can send messages in this channel again.' if enable else 'cannot send messages in this channel'}." + "\nType `" + ctx.prefix + f"lock {'enable' if enable else 'disable'}` to {'enable' if enable else 'disable'} this effect again.")
        except: return
    
    @command(['hidechannel', 'hide-channel'])
    @cooldown(7)
    @require_args()
    @permissions(author=['manage_messages'], bot=['manage_channels'])
    async def hide(self, ctx, *args):
        enable = (not args[0].lower() in ['yes', 'y', 'enable', 'true', 'enabled', 'on'])
        await ctx.channel.set_permissions(ctx.guild.default_role, read_messages=enable)
        try:
            await ctx.success_embed(f"Successfully {'Hide' if enable else 'Re-opened'} the channel.", description=f"All members with the default role {'can see messages in this channel again.' if enable else 'cannot read messages in this channel/see messages in this channel'}." + "\nType `" + ctx.prefix + f"hide {'enable' if enable else 'disable'}` to {'enable' if enable else 'disable'} this effect again.")
        except:
            return
    
    @command(['guild-role', 'server-role'])
    @cooldown(6)
    @require_args()
    @permissions(bot=['add_reactions'])
    async def role(self, ctx, *args):
        if args[0].lower() == 'info':
            try:
                role = ctx.bot.Parser.parse_role(ctx, ' '.join(args[1:]), return_array=True)
                assert role
            except:
                raise ctx.error_message(f"Please add role name/mention/ID after the `{ctx.prefix}role info`.")
            if isinstance(role, list):
                choose = ctx.bot.ChooseEmbed(ctx, role, key=(lambda x: x.mention))
                res = await choose.run()
                if not res:
                    return
                role = res
            
            role_members = "\n".join([f"{i.name}#{i.discriminator}" for i in role.members][:10]) if role.members else "<none>"
            extra = "\n" + f"... and {len(role.members) - 10} others" if len(role.members) > 10 else ""
            permissions = ""
            
            for perm in self.permission_attributes:
                if len(permissions) > 500:
                    break
                
                if getattr(role.permissions, perm):
                    permissions += perm.replace("_", " ") + ", "
            
            await ctx.embed(title=role.name, color=role.color, fields={
                "Role Info": f"**Display role members seperately from online members: **{':white_check_mark:' if role.hoist else ':x:'}" + "\n" + f"**Mentionable: **{':white_check_mark:' if role.mentionable else ':x:'}" + f"\n**Created At: **{ctx.bot.util.timestamp(role.created_at)}",
                f"Role Members ({len(role.members)})": role_members + extra,
                "Key Permissions": permissions[:-2],
                "Role Color": f"**Hex: {str(role.color)}**" + "\n" + f"**RGB: **{role.color.r}, {role.color.g}, {role.color.b}"
            })
            del role_members, extra, role, permissions
            return
        elif args[0].lower() == "list":
            _map = list(map(lambda x: x.mention, ctx.guild.roles[1:]))
            paginator = ctx.bot.EmbedPaginator.from_long_array(ctx, _map, {
                "title": "Server Roles List",
                "thumbnail": { "url": str(ctx.guild.icon_url) }
            }, char=" ", max_char_length=1000, max_pages=5)
        
            if not paginator:
                await ctx.embed(title="Server Roles List", description=" ".join(_map))
                del paginator, _map
                return
            del _map
            return await paginator.execute()
        return await ctx.bot.cmds.invalid_args(ctx)
        
    @command(['guild-channel', 'server-channel'])
    @cooldown(6)
    @require_args()
    @permissions(bot=['add_reactions'])
    async def channel(self, ctx, *args):
        if args[0].lower() == "list":
            _map = [f"<#{i.id}>" for i in ctx.guild.channels if i.type == discord.ChannelType.text]
            paginator = ctx.bot.EmbedPaginator.from_long_array(ctx, _map, {
                "title": "Server Channels List",
                "thumbnail": { "url": str(ctx.guild.icon_url) }
            }, char=" ", max_char_length=1000, max_pages=6)
            
            if not paginator:
                await ctx.embed(title="Server Channels List", description=" ".join(_map))
                del _map
                return
            del _map
            return await paginator.execute()
        elif args[0].lower() == "info":
            try:
                channel = ctx.bot.Parser.parse_channel(ctx, ' '.join(args[1:]), return_array=True)
                assert channel
            except:
                return await ctx.bot.cmds.invalid_args(ctx)
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
                channel_members = "\n".join([f"{i.name}#{i.discriminator}" for i in channel.members[:5]]) if channel.members else "<no members in VC>"
                other = "\n" + f"... and {len(channel.members) - 5} others" if len(channel.members) > 5 else ""
                fields = {
                    "Channel Category": channel.category.name if channel.category else "<no category>",
                    "Channel Info": f"**Channel ID: **{channel.id}" + "\n" + f"**Bitrate: **{channel.bitrate // 1000} kbps",
                    f"VC Members ({len(channel.members)}/{channel.user_limit if channel.user_limit != 0 else '∞'})": channel_members + other,
                    "Channel Type": "Discord Voice Channel (VC)"
                }
            elif channel.type == discord.ChannelType.category:
                channels = "\n".join([i.name for i in channel.channels]) if channel.channels else "<no channels>"
                fields = {
                    "Channel Type": "Discord Category Channel",
                    f"Channels ({len(channel.channels)})": channels[:1000]
                }
            else:
                raise ctx.error_message("Invalid channel type. Must be either Text, voice, or category channel.")
            
            await ctx.embed(title=channel.name, fields=fields)
            del channel
            return
        return await ctx.bot.cmds.invalid_args(ctx)
    
    @command(['user'])
    @cooldown(3)
    async def member(self, ctx, *args):
        await ctx.trigger_typing()
        parser = ctx.bot.Parser(args)
        parser.parse()
        
        if parser.has("card"):
            parser.shift("card")
            person = ctx.bot.Parser.parse_user(ctx, parser.other)
            card = ctx.bot.UserCard(ctx, person, font_path=f"{ctx.bot.util.fonts_dir}/NotoSansDisplay-Bold.otf")
            del parser
            return await card.send()
        
        user, nl = ctx.bot.Parser.parse_user(ctx, args), "\n"
        online_location = '(Discord Mobile)' if user.mobile_status != discord.Status.offline else (
            '(Discord App)' if user.desktop_status != discord.Status.offline else (
                '(Discord Website)' if user.web_status != discord.Status.offline else ''
            )
        )
        
        join_pos = ctx.bot.util.join_position(ctx.guild, user)
        current_time = time()
        embed = ctx.bot.Embed(
            ctx,
            title=str(user),
            fields={
                "General": f"**User ID: **{user.id}{nl if not user.nick else f'**Nick Name: **{user.nick}{nl}'}**Status: **{'do not disturb' if user.status == discord.Status.dnd else str(user.status)} {online_location}{'' if not user.premium_since else f'**Boosting since: **{ctx.bot.util.timestamp(user.premium_since)}'}",
                "History": f"**Joined at: **{ctx.bot.util.timestamp(user.joined_at)}, (Position: {join_pos:,}/{ctx.guild.member_count:,})\n**Created at: **{ctx.bot.util.timestamp(user.created_at)}",
                "Color": f"**Hex Color:** {str(user.color)}\n**RGB: **{user.color.r}, {user.color.g}, {user.color.b}"
            },
            color=user.color,
            thumbnail=user.avatar_url
        )
        
        if user.activity:
            activities = "\n".join([f"{self.presence_prefix[i.type]} {i.name}" for i in user.activities if i.name])
            if activities:
                embed.add_field("Activity", activities)
            del activities
        
        await embed.send()
        del join_pos, current_time, user, nl, embed, parser
    
    @command(['av', 'ava'])
    @cooldown(2)
    async def avatar(self, ctx, *args):
        url = await ctx.bot.Parser.parse_image(ctx, args, default_to_png=False, cdn_only=True, member_only=True, size=4096)
        await ctx.embed(title="Here's ya avatar mate", image=url)
        del url

    @command(['emote', 'emojiinfo', 'emoji-info'])
    @cooldown(5)
    @require_args()
    @permissions(bot=['add_reactions', 'attach_files'])
    async def emoji(self, ctx, *args):
        if args[0].lower() == "list":
            paginator = ctx.bot.EmbedPaginator.from_long_array(ctx, ctx.guild.emojis, {
                "title": "Server Custom Emojis List",
                "thumbnail": { "url": str(ctx.guild.icon_url) }
            }, char=" ", max_char_length=1500, max_pages=10)
            
            if not paginator:
                del paginator
                return await ctx.embed(title="Server Custom Emojis List", description=" ".join(ctx.guild.emojis))
            return await paginator.execute()
        elif args[0].lower() == "info":
            try:
                res = await ctx.bot.Parser.parse_emoji(ctx, args[1])
                assert res
            except:
                return await ctx.bot.cmds.invalid_args(ctx)
            data = ctx.bot.get_emoji(int(res.strip("https://cdn.discordapp.com/emojis/.png"))) if res.startswith("https://cdn") else None
            
            fields = {
                "Emoji name": data[0] if data else "`<not available>`",
                "Emoji ID": data[1] if data else "`<not available>`",
                "Emoji creation date": ctx.bot.util.timestamp(data[3]) if data else "`not available`",
                "Emoji type": "Discord Animated Custom Emoji" if (data and data[2]) else "Discord Custom Emoji",
                "Emoji source": f"{data[5].name} ({len(data[5].emojis):,}/{data[5].emoji_limit:,} custom emojis)" if (data and data[4]) else "`<source not available>`",
                "Emoji URL": res
            } if res.startswith("https://cdn") else {
                "Emoji type": "Default Discord Emoji", 
                "Emoji URL": res
            }
            
            await ctx.embed(title="Emoji Info", fields=fields, image=res)
            del fields, data, res
            return
        elif args[0].lower() == "enlarge":
            try:
                res = await ctx.bot.Parser.parse_emoji(ctx, args[1])
                assert res
            except:
                raise ctx.error_message(f"Please add a emoji after the `{ctx.prefix}emoji enlarge`")
            return await ctx.send_image(res)
        return await ctx.bot.cmds.invalid_args(ctx)
    
    @command(['guild'])
    @cooldown(10)
    @permissions(bot=['add_reactions', 'attach_files'])
    async def server(self, ctx, *args):
        parser = ctx.bot.Parser(args)
        parser.parse()
        
        if parser.has("icon"):
            await ctx.embed(title="Server Icon", image=ctx.guild.icon_url)
            del parser
        elif parser.has("card"):
            await ctx.trigger_typing()
            card = ctx.bot.ServerCard(ctx, f"{ctx.bot.util.fonts_dir}/NotoSansDisplay-Bold.otf")
            result = await card.draw()
            
            await ctx.send_image(result)
            del result, card, parser
        else:
            await ctx.trigger_typing()
            nl = "\n"
            embed = ctx.bot.Embed(
                ctx,
                title=ctx.guild.name,
                description=ctx.guild.description or "",
                fields={
                    "General": f"**Created by: **{str(ctx.guild.owner)}\n**Created at: **{ctx.bot.util.timestamp(ctx.guild.created_at)}\n**Server Region: **{str(ctx.guild.region).replace('-', ' ')}\n**Server ID: **`{ctx.guild.id}`",
                    "Stats": f"**Members: **{ctx.guild.member_count:,}\n**Online Members: **{len([i for i in ctx.guild.members if i.status != discord.Status.offline]):,}\n**Channels: **{len(ctx.guild.channels):,}\n**Roles: **{len(ctx.guild.roles):,}\n**Custom Emojis: **{len(ctx.guild.emojis):,} ({ctx.guild.emoji_limit - len(ctx.guild.emojis):,} slots left)",
                    "Boost": f"**Boosters: **{ctx.guild.premium_subscription_count:,}\n**Server Boost Level: **{ctx.guild.premium_tier}\n"
                },
                thumbnail=ctx.guild.icon_url,
                image=ctx.guild.banner_url
            )
            
            first_embed = discord.Embed.from_dict(embed.dict)
            embed = ctx.bot.Embed(
                ctx,
                title=ctx.guild.name,
                fields={
                    "Server Features": ", ".join([i.lower().replace("_", " ") for i in ctx.guild.features]),
                    "Community Server Settings": f"**Server Rules Channel: **{f'<#{ctx.guild.rules_channel.id}>' if ctx.guild.rules_channel else '`<not set>`'}\n**Public Updates Channel: **{f'<#{ctx.guild.public_updates_channel.id}>' if ctx.guild.public_updates_channel else '`<not set>`'}",
                    "AFK Settings": f"**AFK Channel: **{f'<#{ctx.guild.afk_channel.id}>' if ctx.guild.afk_channel else '<not set>'}\n**AFK Timeout: **{ctx.guild.afk_timeout // 60} minute{'' if (ctx.guild.afk_timeout // 60) == 1 else 's'}",
                    "Limits": f"**Presence Limit: **{(ctx.guild.max_presences if ctx.guild.max_presences else '`<no limit>`')}\n**Bitrate Limit: **{(ctx.guild.bitrate_limit // 1000):,} kbps\n**Filesize Limit: **{(ctx.guild.filesize_limit // 1000000):,} MB"
                }
            )
            second_embed = discord.Embed.from_dict(embed.dict)
            paginator = ctx.bot.EmbedPaginator(ctx, embeds=[first_embed, second_embed])
            del first_embed, second_embed, nl, parser
            return await paginator.execute()
    
    @command(['perms', 'perm', 'permission', 'permfor', 'permsfor', 'perms-for', 'perm-for'])
    @cooldown(10)
    async def permissions(self, ctx, *args):
        user = ctx.bot.Parser.parse_user(ctx, args)
        source = ctx.channel.permissions_for(user)
        embed = ctx.bot.Embed(ctx, title="Permissions for "+str(user)+" in "+ctx.channel.name)
        for permission in self.permission_attributes:
            emoji = ":white_check_mark:" if getattr(source, permission) else ":x:"
            embed.dict["description"] += "{} {}\n".format(emoji, permission.replace("_", " "))
        embed.dict["description"] = embed.dict["description"][:-2]
        return await embed.send()

def setup(client):
    client.add_cog(moderation(client))