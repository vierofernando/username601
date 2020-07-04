import discord
from discord.ext import commands
import sys
import random
import asyncio
sys.path.append('/app/modules')
from username601 import *
import canvas as Painter
import username601 as myself

class moderation(commands.Cog):
    def __init__(self, client):
        self.client = client
    
    @commands.command(pass_context=True)
    @commands.cooldown(1, 15, commands.BucketType.user)
    async def rolecolor(self, ctx, *args):
        unprefixed = ' '.join(list(args))
        if len(unprefixed.split('#'))==1:
            await ctx.send(f'Please provide a hex!\nExample: {Config.prefix}rolecolor {random.choice(ctx.message.guild.roles).name} #ff0000')
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
                        await ctx.send(str(self.client.get_emoji(BotEmotes.error)) + f' | An error occured while editing role:```{e}```')
    
    @commands.command(pass_context=True)
    @commands.cooldown(1, 15, commands.BucketType.user)
    async def slowmode(self, ctx, *args):
        if len(list(args))==0: await ctx.send(str(self.client.get_emoji(BotEmotes.error))+" | How long in seconds?")
        else:
            cd = list(args)[0]
            if ctx.message.author.guild_permissions.manage_channels:
                if not cd.isnumeric():
                    await ctx.send(str(self.client.get_emoji(BotEmotes.error))+" | That cooldown is not a number!s")
                else:
                    if int(cd)<0:
                        await ctx.send(str(self.client.get_emoji(BotEmotes.error))+" | Minus slowmode? Did you mean slowmode 0 seconds?")
                    elif int(cd)>21600:
                        await ctx.send(str(self.client.get_emoji(BotEmotes.error))+" | That is too hecking sloow....")
                    else:
                        await ctx.message.channel.edit(slowmode_delay=cd)
                        await ctx.send(str(self.client.get_emoji(BotEmotes.success))+" | Channel slowmode cooldown has been set to "+myself.time_encode(int(cd)))
            else: await ctx.send(str(self.client.get_emoji(BotEmotes.error))+" | You need the manage channels permission to do this command!")

    @commands.command(pass_context=True, aliases=['addrole', 'add-role'])
    @commands.cooldown(1, 15, commands.BucketType.user)
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
    
    @commands.command(pass_context=True, aliases=['removerole', 'remove-role'])
    @commands.cooldown(1, 15, commands.BucketType.user)
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

    @commands.command(pass_context=True, aliases=['kick'])
    @commands.cooldown(1, 15, commands.BucketType.user)
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
            if ctx.message.mentions[0].guild_permissions.administrator:
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
    @commands.command(pass_context=True, aliases=['purge'])
    @commands.cooldown(1, 15, commands.BucketType.user)
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
    @commands.command(pass_context=True, aliases=['hidechannel'])
    @commands.cooldown(1, 5, commands.BucketType.user)
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

    @commands.command(pass_context=True, aliases=['roles', 'serverroles', 'serverchannels', 'channels'])
    @commands.cooldown(1, 5, commands.BucketType.user)
    async def channel(self, ctx):
        total = []
        if 'channel' in ctx.message.content:
            for i in ctx.message.guild.channels: total.append('<#'+str(i.id)+'>')
        else:
            for i in ctx.message.guild.roles: total.append('<@&'+str(i.id)+'>')
        await ctx.send(embed=discord.Embed(description=myself.dearray(total), color=discord.Color.from_rgb(201, 160, 112)))

    @commands.command(pass_context=True, aliases=['user', 'usercard', 'user-info', 'user-card'])
    @commands.cooldown(1, 5, commands.BucketType.user)
    async def userinfo(self, ctx):
        if len(ctx.message.mentions)==0: guy = ctx.message.author
        else: guy = ctx.message.mentions[0]
        data = Painter.usercard(guy)
        await ctx.send(file=discord.File(data, str(guy.discriminator)+'.png'))

    @commands.command(pass_context=True, aliases=['av', 'ava'])
    @commands.cooldown(1, 1, commands.BucketType.user)
    async def avatar(self, ctx):
        embed = discord.Embed(title='look at dis avatar', color=discord.Colour.from_rgb(201, 160, 112))
        if len(ctx.message.mentions)==0: embed.set_image(url=ctx.message.author.avatar_url)
        else: embed.set_image(url=ctx.message.mentions[0].avatar_url)
        await ctx.send(embed=embed)

    @commands.command(pass_context=True, aliases=['serverinfo', 'server', 'servericon'])
    @commands.cooldown(1, 7, commands.BucketType.user)
    async def servercard(self, ctx):
        if 'servericon' in ctx.message.content:
            if ctx.message.guild.is_icon_animated(): link = 'https://cdn.discordapp.com/icons/'+str(ctx.message.guild.id)+'/'+str(ctx.message.guild.icon)+'.gif?size=1024'
            else: link = 'https://cdn.discordapp.com/icons/'+str(ctx.message.guild.id)+'/'+str(ctx.message.guild.icon)+'.png?size=1024'
            theEm = discord.Embed(title=ctx.message.guild.name+'\'s Icon', url=link, colour=discord.Colour.from_rgb(201, 160, 112))
            theEm.set_image(url=link)
            await ctx.send(embed=theEm)
        else:
            humans, bots, online = 0, 0, 0
            for i in ctx.message.guild.members:
                if i.status != 'offline': online += 1
                if i.bot: bots += 1
                if not i.bot: humans += 1
            image = Painter.servercard("./assets/pics/card.jpg", str(ctx.message.guild.icon_url).replace(".webp?size=1024", ".jpg?size=128"), ctx.message.guild.name, str(ctx.message.guild.created_at)[:-7], ctx.message.guild.owner.name, str(humans), str(bots), str(len(ctx.message.guild.channels)), str(len(ctx.message.guild.roles)), str(ctx.message.guild.premium_subscription_count), str(ctx.message.guild.premium_tier), str(online))
            await ctx.send(content='Here is the '+ctx.message.guild.name+'\'s server card.', file=discord.File(image, ctx.message.guild.name+'.png'))
    
    @commands.command(pass_context=True, aliases=['bots', 'serverbots', 'server-bots'])
    @commands.cooldown(1, 5, commands.BucketType.user)
    async def botmembers(self, ctx):
        botmembers, off, on, warning = "", 0, 0, 'Down triangles means that the bot is down. And up triangles mean the bot is well... up.'
        for i in range(0, int(len(ctx.message.guild.members))):
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

    @commands.command(pass_context=True, aliases=['serverinvite', 'create-invite', 'createinvite', 'makeinvite', 'make-invite', 'server-invite'])
    @commands.cooldown(1, 30, commands.BucketType.user)
    async def getinvite(self, ctx):
        if not ctx.message.author.guild_permissions.create_invite:
            await ctx.send(str(self.client.get_emoji(BotEmotes.error))+' | No create invite permission?')
        else:
            serverinvite = await ctx.message.channel.create_invite(reason='Requested by '+str(message.author.name))
            await ctx.send(str(self.client.get_emoji(BotEmotes.success))+' | New invite created! Link: **'+str(serverinvite)+'**')

    @commands.command(pass_context=True, name='id')
    @commands.cooldown(1, 2, commands.BucketType.user)
    async def _id(self, ctx, *args):
        if '<#' in ''.join(list(args)): total = str('Channel ID: ')+str(''.join(list(args)).split('<#')[1].split('>')[0])
        elif '<@&' in ''.join(list(args)): total = str('Role ID: ')+str(''.join(list(args)).split('<@&')[1].split('>')[0])
        elif '<@!' in ''.join(list(args)): total = str('User ID: ')+str(''.join(list(args)).split('<@!')[1].split('>')[0])
        elif '<@' in ''.join(list(args)): total = str('User ID')+str(''.join(list(args)).split('<@')[1].split('>')[0])
        else: total = str(self.client.get_emoji(BotEmotes.error))+' | No ID\'s found.'
        await ctx.send(total)

    @commands.command(pass_context=True)
    @commands.cooldown(1, 7, commands.BucketType.user)
    async def roleinfo(self, ctx, *args):
        if len(list(args))==0:
            await ctx.send(str(self.client.get_emoji(BotEmotes.error))+" | Please send a role name or a role mention! (don\'t)")
        else:
            data = None
            if '<@&' in ''.join(list(args)):
                data = ctx.message.guild.get_role(int(str(ctx.message.content).split('<@&')[1].split('>')[0]))
            else:
                for i in ctx.message.guild.roles:
                    if ' '.join(list(args)).lower()==str(i.name).lower(): data = i
            if data==None:
                await ctx.send(str(self.client.get_emoji(BotEmotes.error))+' | Role not found!')
            else:
                if data.permissions.administrator==True: perm = ':white_check_mark: Server Administrator'
                else: perm = ':x: Server Administrator'
                if data.mentionable==True: men = ':warning: You can mention this role and they can get pinged.'
                else: men = ':v: You can mention this role and they will not get pinged! ;)'
                embedrole = discord.Embed(title='Role info for role: '+str(data.name), description='**Role ID: **'+str(data.id)+'\n**Role created at: **'+str(data.created_at)[:-7]+' UTC\n**Role position: **'+str(data.position)+'\n**Members having this role: **'+str(len(data.members))+'\n'+str(men)+'\nPermissions Value: '+str(data.permissions.value)+'\n'+str(perm), colour=data.colour)
                embedrole.add_field(name='Role Colour', value='**Color hex: **#'+str(myself.tohex(data.color.value))+'\n**Color integer: **'+str(data.color.value)+'\n**Color RGB: **'+str(myself.dearray(list(data.color.to_rgb()))))
                await ctx.send(embed=embedrole)

    @commands.command(pass_context=True, aliases=['perms', 'perm', 'permission', 'permfor', 'permsfor', 'perms-for', 'perm-for'])
    @commands.cooldown(1, 15, commands.BucketType.user)
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
    
    @commands.command(pass_context=True)
    @commands.cooldown(1, 5, commands.BucketType.user)
    async def emojiinfo(self, ctx, *args):
        if len(list(args))==0:
            await ctx.send(str(self.client.get_emoji(BotEmotes.error))+" | Please gimme the emoji!")
        else:
            try:
                erry = False
                emojiid = int(list(args)[0].split(':')[2][:-1])
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

    @commands.command(pass_context=True, aliases=['mkchannel', 'mkch', 'createchannel', 'make-channel', 'create-channel'])
    @commands.cooldown(1, 5, commands.BucketType.user)
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

    @commands.command(pass_context=True, aliases=['nickname'])
    @commands.cooldown(1, 10, commands.BucketType.user)
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
def setup(client):
    client.add_cog(moderation(client))
