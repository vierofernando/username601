import discord
import random
from discord.ext import commands
from sys import path
from os import getcwd, name, environ
path.append(environ['BOT_MODULES_DIR'])
path.append(environ['BOT_JSON_DIR'])
from decorators import command, cooldown
from json import loads
from datetime import datetime
from asyncio import sleep

class economy(commands.Cog):
    def __init__(self, client):
        self.client = client
        self.fish_json = loads(open(self.client.utils.cfg("JSON_DIR")+'/fish.json', 'r').read())
        self.steal_json = loads(open(client.utils.cfg('JSON_DIR')+'/steal.json', 'r').read())
    
    @command()
    @cooldown(30)
    async def gamble(self, ctx, *args):
        if len(args)==0: raise self.client.utils.SendErrorMessage('Please input a number.')
        lucky = random.choice([False, True])
        try:
            amount = int(list(args)[0])
        except:
            raise self.client.utils.SendErrorMessage('Please make sure you inputted a number!')
        if not lucky:
            self.client.db.Economy.delbal(ctx.author.id, amount)
            say, emote = "Yikes! %M%, you just lost %A% bobux...", self.client.error_emoji
        else:
            self.client.db.Economy.addbal(ctx.author.id, amount)
            say, emote = "Congratulations %M%, you just won %A% bobux!", self.client.success_emoji
        return await ctx.send(emote + ' | ' + say.replace('%M%', ctx.author.mention).replace('%A%', str(amount)))

    @command()
    @cooldown(120)
    async def beg(self, ctx):
        c = random.randint(1, 3)
        if self.client.db.Economy.get(ctx.author.id)==None: raise self.client.utils.SendErrorMessage("Doesn't have a profile yet. Try `1new` to have a profile.")
        if c==1:
            award = random.randint(100, 800)
            self.client.db.Economy.addbal(ctx.author.id, award)
            return await ctx.send('{} | You begged and got {} bobux!'.format(self.client.success_emoji, award))
        await ctx.send('{} | Stop begging! Try again later. There is only 1/3 chance you will get a bobux.'.format(self.client.error_emoji))

    @command('fishing')
    @cooldown(60)
    async def fish(self, ctx):
        if self.client.db.Economy.get(ctx.author.id)==None: raise self.client.utils.SendErrorMessage("Doesn't have a profile yet. Try `1new` to have a profile.")
        wait = await ctx.send('{} | {}'.format(self.client.loading_emoji, random.choice(
            self.fish_json['waiting']
        )))
        await sleep(random.randint(3, 8))
        res = self.client.algorithm.getfish()
        if res['catched']:
            awards = random.randint(res['ctx']['worth']['min'], res['ctx']['worth']['max'])
            self.client.db.Economy.addbal(ctx.author.id, awards)
            return await wait.edit(content='{} | Congratulations! You caught a {} and sell it worth for {} bobux!'.format(res['ctx']['emote'], res['ctx']['name'], awards))
        return await wait.edit(content='{} | You only caught {}...'.format(self.client.error_emoji, res['ctx']))

    @command()
    @cooldown(7)
    async def buylist(self, ctx):
        source = ctx.author if len(ctx.message.mentions)==0 else ctx.message.mentions[0]
        if self.client.db.Economy.get(ctx.author.id)==None: raise self.client.utils.SendErrorMessage("Doesn't have a profile yet. Try `1new` to have a profile.")
        try:
            data = self.client.db.Economy.getBuyList(source)
            assert not data['error'], data['ctx']
            return await ctx.send(embed=discord.Embed(title='{}\'s buy list'.format(source.name), description=data['ctx'], color=self.client.utils.get_embed_color()))
        except Exception as e:
            raise self.client.utils.SendErrorMessage(str(e))

    @command('addshop')
    @cooldown(5)
    async def addproduct(self, ctx, *args):
        if len(args)==0: raise self.client.utils.SendErrorMessage(f'Please use the following parameters:\n`{self.client.command_prefix}addshop <price> <name>`')
        if not ctx.author.guild_permissions.manage_guild: raise self.client.utils.SendErrorMessage('You do not have the correct permissions to modify the server\'s shop.')
        try:
            price = int(list(args)[0])
            extra = '' if price in range(5, 1000000) else 'Invalid price. Setting price to default: 1000'
            if extra.endswith('1000'): price = 1000
            productName = '<product name undefined>' if len(args)<2 else ' '.join(list(args)[1:len(args)])
            if len(productName)>30: productName = ''.join(list(productName)[0:30])
            a = self.client.db.Shop.add_value(productName, price, ctx.guild)
            assert not a['error'], a['ctx']
            return await ctx.send('{} | {}!\n{}'.format(self.client.success_emoji, a['ctx'], extra))
        except Exception as e:
            raise self.client.utils.SendErrorMessage(str(e))
    
    @command('remshop,delshop')
    @cooldown(5)
    async def delproduct(self, ctx, *args):
        if len(args)==0: raise self.client.utils.SendErrorMessage(f'Please use the following parameters:\n`{self.client.command_prefix}delproduct <name>`\nor to delete all stored in the shop, use `{self.client.command_prefix}delproduct all`')
        if not ctx.author.guild_permissions.manage_guild: raise self.client.utils.SendErrorMessage('You do not have the correct permissions to modify the server\'s shop.')
        if list(args)[0].lower()=='all':
            self.client.db.Shop.delete_shop(ctx.guild)
            return await ctx.send('{} | OK. All data for the shop is deleted.'.format(self.client.success_emoji))
        try:
            data = self.client.db.Shop.remove_element(' '.join(args), ctx.guild)
            assert data['error']==False, data['ctx']
            return await ctx.send('{} | {}!'.format(self.client.success_emoji, data['ctx']))
        except Exception as e:
            raise self.client.utils.SendErrorMessage(str(e))
    
    @command('bought')
    @cooldown(3)
    async def buy(self, ctx, *args):
        if len(args)==0: raise self.client.utils.SendErrorMessage(f'Please use the following parameters:\n`{self.client.command_prefix}buy <name>`')
        if self.client.db.Economy.get(ctx.author.id)==None: raise self.client.utils.SendErrorMessage("Doesn't have a profile yet. Try `1new` to have a profile.")
        try:
            data = self.client.db.Shop.buy(' '.join(args), ctx.author)
            assert not data['error'], data['ctx']
            return await ctx.send('{} | {}!'.format(self.client.success_emoji, data['ctx']))
        except Exception as e:
            raise self.client.utils.SendErrorMessage(str(e))
    
    @command('servershop,store,serverstore')
    @cooldown(2)
    async def shop(self, ctx):
        try:
            data = self.client.db.Shop.get_shop(ctx.guild)
            assert data['error']==False, data['ctx']
            em = discord.Embed(title='{}\'s shop'.format(ctx.guild.name), description='\n'.join(
                [str(i+1)+'. **'+str(data['ctx'][i]['name'])+'** (price: '+str(data['ctx'][i]['price'])+' :gem:)' for i in range(len(data['ctx']))]
            ), color=self.client.utils.get_embed_color())
            return await ctx.send(embed=em)
        except Exception as e:
            raise self.client.utils.SendErrorMessage(f'{str(e)}!\nYou can always add a value using `{self.client.command_prefix}addproduct <price> <name>`')

    @command('delete,deletedata,deldata,del-data,delete-data')
    @cooldown(3600)
    async def reset(self, ctx):
        data = self.client.db.Economy.get(ctx.author.id)
        if data==None: raise self.client.utils.SendErrorMessage("Doesn't have a profile yet. Try `1new` to have a profile.")
        else:
            wait = await ctx.send(self.client.loading_emoji+" | Please wait...")
            await wait.edit(content=':thinking: | Are you sure? This action is irreversible!\n(Reply with yes/no)')
            def check_is_auth(m):
                return ctx.author == m.author
            try:
                waiting = await self.client.wait_for('message', check=check_is_auth, timeout=20.0)
            except:
                await ctx.send('{} | No it is then.'.format(self.client.success_emoji))
            if 'y' in str(waiting.content).lower():
                self.client.db.Economy.delete_data(ctx.author.id)
                await ctx.send('{} | Data deleted. Thanks for playing.'.format(self.client.success_emoji))
            else:
                await ctx.send('{} | No it is then.'.format(self.client.success_emoji))
    
    @command()
    @cooldown(450)
    async def work(self, ctx):
        data = self.client.db.Economy.get(ctx.author.id)
        if data==None: raise self.client.utils.SendErrorMessage("Doesn't have a profile yet. Try `1new` to have a profile.")
        else:
            wait = await ctx.send(self.client.loading_emoji+" | Please wait...")
            reward = str(random.randint(100, 500))
            new_data = self.client.db.Economy.addbal(ctx.author.id, int(reward))
            job = random.choice(loads(open(self.client.utils.cfg('JSON_DIR')+'/work.json', 'r').read())['works'])
            if new_data=='success': await wait.edit(content=self.client.success_emoji+f" | {ctx.author.name} worked {job} and earned {reward} bobux!")
            else: raise self.client.utils.SendErrorMessage(f"Oops there was an error... Please report this to the owner using `{self.client.command_prefix}feedback.`\n`{new_data}`")
            
    @command()
    @cooldown(15)
    async def daily(self, ctx, *args):
        wait = await ctx.send(self.client.loading_emoji+" | Please wait...")
        if self.client.db.Economy.get(ctx.author.id)==None: raise self.client.utils.SendErrorMessage("Doesn't have a profile yet. Try `1new` to have a profile.")
        else:
            obj = self.client.db.Economy.can_vote(ctx.author.id)
            if obj['bool']:
                # await wait.edit(content='', embed=discord.Embed(
                #     title='Vote us at top.gg!',
                #     description='**[VOTE HERE](https://top.gg/bot/'+str(self.client.user.id)+'/vote)**\nBy voting, we will give you rewards such as ***LOTS of bobux!***',
                #     color = discord.Colour.green()
                # ))
                rewards = self.client.db.Economy.daily(ctx.author.id)
                await ctx.send("{} | Congrats! You got **{} bobux** as a daily reward! You can try again in 12 hours.".format(self.client.success_emoji, rewards))
            else:
                await wait.edit(content='', embed=discord.Embed(
                    title='You can get rewards again in '+str(obj['time'])+'!',
                    colour=discord.Colour.red()
                ))
    
    @command()
    @cooldown(10)
    async def transfer(self, ctx, *args):
        if len(args)==0 or len(ctx.message.mentions)==0: raise self.client.utils.SendErrorMessage("Please send a mention and an amount to transfer.")
        else:
            wait = await ctx.send(self.client.loading_emoji+' | Please wait...?')
            amount = None
            for i in list(args):
                if i.isnumeric(): amount = int(i); break
            if amount==None: raise self.client.utils.SendErrorMessage("Please give a valid amount.")
            elif amount not in range(1, 500001): raise self.client.utils.SendErrorMessage("Invalid amount range.")
            elif self.client.db.Economy.get(ctx.author.id)==None or self.client.db.Economy.get(ctx.message.mentions[0].id)==None:
                raise self.client.utils.SendErrorMessage("One of them does not have a profile.")
            else:
                self.client.db.Economy.addbal(ctx.message.mentions[0].id, amount)
                self.client.db.Economy.delbal(ctx.author.id, amount) # EFFICIENT CODE LMFAO
                await wait.edit(content=self.client.success_emoji+f' | Done! Transferred {str(amount)} bobux to {ctx.message.mentions[0].name}!')

    @command('steal,crime,stole,robs')
    @cooldown(60)
    async def rob(self, ctx, *args):
        if len(ctx.message.mentions)==0 or len(args)==0:
            raise self.client.utils.SendErrorMessage(f'Rob who? Try `1rob <mention> <amount>`.')
        else:
            if ctx.message.mentions[0].id==ctx.author.id:
                raise self.client.utils.SendErrorMessage('Seriously? Robbing yourself?')
            else:
                amount2rob = None
                for i in list(args):
                    if i.isnumeric(): amount2rob = int(i) ; break
                if amount2rob==None: raise self.client.utils.SendErrorMessage('How many bobux shall be robbed?')
                elif amount2rob>9999: raise self.client.utils.SendErrorMessage('Dude, you must be crazy. That\'s too many bobux!')
                elif amount2rob<0: raise self.client.utils.SendErrorMessage('minus??? HUH?')
                else:
                    wait = await ctx.send(self.client.loading_emoji+' | *Please wait... robbing...*')
                    victim, stealer = self.client.db.Economy.get(ctx.message.mentions[0].id), self.client.db.Economy.get(ctx.author.id)
                    if victim==None or stealer==None:
                        raise self.client.utils.SendErrorMessage('you/that guy doesn\'t even have a profile!')
                    else:
                        data = random.choice(self.steal_json)
                        if not str(data['amount']).replace('-', '').isnumeric():
                            if data['amount']=='{SAME_AMOUNT}': robamount = -amount2rob
                            elif data['amount']=='{REAL}': robamount = int(amount2rob)
                            else: robamount = -self.client.db.Economy.get(ctx.author.id)['bal']
                        else: robamount = data['amount']
                        if robamount > 0:
                            self.client.db.Economy.addbal(ctx.author.id, robamount) ; self.client.db.Economy.delbal(ctx.message.mentions[0].id, robamount)
                            statement = f'You stole {str(robamount)} in total.'
                        elif robamount==0:
                            statement = f'You left empty-handed.'
                        else:
                            self.client.db.Economy.delbal(ctx.author.id, robamount*-1) ; self.client.db.Economy.addbal(ctx.message.mentions[0].id, robamount*-1)
                            statement = f'You lost {str(robamount)} bobux.'
                        embed = discord.Embed(
                            title = f'{ctx.author.name} robbing {ctx.message.mentions[0].name} scene be like',
                            description = data['statement'].replace('{NL}', '\n').replace('{D1}', ctx.author.name).replace('{D2}', ctx.message.mentions[0].name),
                            color = discord.Colour.red()
                        )
                        embed.set_footer(text=statement)
                        await wait.edit(content='', embed=embed)
    
    @command('dep')
    @cooldown(10)
    async def deposit(self, ctx, *args):
        if len(args)==0: raise self.client.utils.SendErrorMessage(f'How many money?\nOr use `{self.client.command_prefix}dep all` to deposit all of your money.')
        data = self.client.db.Economy.get(ctx.author.id)
        if data==None: raise self.client.utils.SendErrorMessage("Doesn't have a profile yet. Try `1new` to have a profile.")
        if list(args)[0].lower()=='all':
            self.client.db.Economy.deposit(ctx.author.id, data['bal'])
            return await ctx.send('{} | OK. Deposited all of your bobux to the username601 bank.'.format(self.client.success_emoji))
        try:
            num = int(list(args)[0])
            if num > data['bal']:
                raise self.client.utils.SendErrorMessage('Your bank has more money than in your balance!')
            self.client.db.Economy.deposit(ctx.author.id, num)
            return await ctx.send('{} | OK. Deposited {} bobux to your bank.'.format(self.client.success_emoji, num))
        except:
            raise self.client.utils.SendErrorMessage("Invalid number.")
    
    @command()
    @cooldown(10)
    async def withdraw(self, ctx, *args):
        if len(args)==0: raise self.client.utils.SendErrorMessage(f'How many money?\nOr use `{self.client.command_prefix}widthdraw all` to get money from the bank.')
        data = self.client.db.Economy.get(ctx.author.id)
        if data==None: raise self.client.utils.SendErrorMessage("Doesn't have a profile yet. Try `1new` to have a profile.")
        if list(args)[0].lower()=='all':
            self.client.db.Economy.withdraw(ctx.author.id, data['bankbal'])
            return await ctx.send('{} | OK. Withdrawed all of your bobux from the username601 bank.'.format(self.client.success_emoji))
        try:
            num = int(list(args)[0])
            if num > data['bankbal']:
                raise self.client.utils.SendErrorMessage('Your number is more than the one in your bank!')
            self.client.db.Economy.withdraw(ctx.author.id, num)
            return await ctx.send('{} | OK. Withdrawed {} bobux from your bank.'.format(self.client.success_emoji, num))
        except:
            raise self.client.utils.SendErrorMessage("Invalid number.")

    @command('lb,leader,leaders,rich,richest,top')
    @cooldown(6)
    async def leaderboard(self, ctx):
        data = self.client.db.Economy.leaderboard(ctx.guild.members)
        if len(data)==0:
            raise self.client.utils.SendErrorMessage('This server doesn\'t have any members with profiles...')
        else:
            wait = await ctx.send(self.client.loading_emoji+' | Please wait...')
            total, bals, ids = [], sorted([int(a.split('|')[1]) for a in data])[::-1][0:20], []
            for a in range(0, len(bals)):
                person = [{
                    'userid': int(i.split('|')[0]),
                    'bal': int(i.split('|')[1])
                } for i in data if int(i.split('|')[1])==bals[a] and int(i.split('|')[0]) not in ids][0]
                ids.append(person['userid'])
                user = ctx.guild.get_member(person['userid'])
                total.append('{}. {}#{} - **{}** :gem:'.format(
                    a+1, user.name, user.discriminator, person['bal']
                ))
            await wait.edit(content='', embed=discord.Embed(
                title = ctx.guild.name+'\'s leaderboard',
                description = '\n'.join(total),
                color = self.client.utils.get_embed_color()
            ))
    
    @command('desc,description')
    @cooldown(2)
    async def setdesc(self, ctx, *args):
        if len(args)==0:
            raise self.client.utils.SendErrorMessage('What is the new description?')
        else:
            if len(args)>120: raise self.client.utils.SendErrorMessage('Your description is too long!')
            newdesc = ' '.join(args)
            for i in ['discord.gg', 'discord.com/', 'bit.ly', '://', 'nigga', 'nigger', 'discordapp.com']:
                if i in newdesc.lower(): raise self.client.utils.SendErrorMessage('Your description has invalid/blocked text!')
            wait = await ctx.send(self.client.loading_emoji+' | Please wait...')
            if self.client.db.Economy.get(ctx.author.id)==None:
                raise self.client.utils.SendErrorMessage("Doesn't have a profile yet. Try `1new` to have a profile.")
            else:
                data = self.client.db.Economy.setdesc(ctx.author.id, newdesc)
                if data=='error': await wait.edit(content=self.client.error_emoji+' | Oopsies! There was an error...')
                else: await wait.edit(content=self.client.success_emoji+' | Updated your description!')
    
    @command('balance,mybal,profile,me,myprofile')
    @cooldown(2)
    async def bal(self, ctx, *args):
        src, ava = self.client.utils.getUser(ctx, args), self.client.utils.getUserAvatar(ctx, args)
        if self.client.db.Economy.get(src.id)==None:
            raise self.client.utils.SendErrorMessage("Doesn't have a profile yet. Try `1new` to have a profile.")
        else:
            wait = await ctx.send(self.client.loading_emoji+" | Please wait...")
            data = self.client.db.Economy.getProfile(src.id, [i.id for i in ctx.guild.members if not i.bot])
            bfr, aft = data['main'], data['after']
            img = self.client.canvas.profile(src.name, ava, bfr, aft)
            await wait.delete()
            await ctx.send(file=discord.File(img, 'profile.png'))
    
    @command('newprofile')
    @cooldown(10)
    async def new(self, ctx):
        data = self.client.db.Economy.get(ctx.author.id)
        wait = await ctx.send(self.client.loading_emoji+" | Please wait... creating your profile...")
        if data!=None:
            raise self.client.utils.SendErrorMessage("You already have a profile!")
        else:
            data = self.client.db.Economy.new(ctx.author.id)
            if data!='done':
                raise self.client.utils.SendErrorMessage(f"Oops! there was an error: {data}")
            else:
                await wait.edit(content=self.client.success_emoji+f" | Created your profile!")

def setup(client):
    client.add_cog(economy(client))