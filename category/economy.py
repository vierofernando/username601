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
    
    @command()
    @cooldown(60)
    async def beg(self, ctx):
        c = random.randint(1, 3)
        if self.client.db.Economy.get(ctx.author.id)==None: raise self.client.utils.noProfile()
        if c==1:
            award = random.randint(100, 500)
            self.client.db.Economy.addbal(ctx.author.id, award)
            return await ctx.send('{} | You begged and got {} bobux!'.format(self.client.utils.emote(self.client, 'success'), award))
        await ctx.send('{} | Stop begging! Try again later.'.format(self.client.utils.emote(self.client, 'error')))

    @command('fishing')
    @cooldown(30)
    async def fish(self, ctx):
        if self.client.db.Economy.get(ctx.author.id)==None: raise self.client.utils.noProfile()
        wait = await ctx.send('{} | {}'.format(self.client.utils.emote(self.client, 'loading'), random.choice(
            loads(open('/app/assets/json/fish.json', 'r').read())['waiting']
        )))
        await sleep(random.randint(3, 10))
        res = self.client.algorithm.randomfish()
        if res['catched']:
            awards = random.randint(res['ctx']['worth']['min'], res['ctx']['worth']['max'])
            self.client.db.Economy.addbal(ctx.author.id, awards)
            return await wait.edit(content='{} | Congratulations! You caught a {} and sell it worth for {} bobux!'.format(res['ctx']['emote'], res['ctx']['name'], awards))
        return await wait.edit(content='{} | You only caught {}...'.format(self.client.utils.emote(self.client, 'error'), res['ctx']))

    @command()
    @cooldown(7)
    async def buylist(self, ctx):
        source = ctx.author if len(ctx.message.mentions)==0 else ctx.message.mentions[0]
        if self.client.db.Economy.get(ctx.author.id)==None: raise self.client.utils.noProfile()
        try:
            data = self.client.db.Economy.getBuyList(source)
            assert data['error']==False, data['ctx']
            return await ctx.send(embed=discord.Embed(title='{}\'s buy list'.format(source.name), description=data['ctx'], color=discord.Colour.from_rgb(201, 160, 112)))
        except Exception as e:
            return await ctx.send('{} | {}!'.format(self.client.utils.emote(self.client, 'error'), str(e)))

    @command('addshop')
    @cooldown(5)
    async def addproduct(self, ctx, *args):
        if len(list(args))==0: return await ctx.send('{} | Please use the following parameters:\n`{}addshop <price> <name>`'.format(self.client.utils.emote(self.client, 'error'), self.client.utils.prefix))
        if not ctx.author.guild_permissions.manage_guild: return await ctx.send('{} | You do not have the correct permissions to modify the server\'s shop.'.format(self.client.utils.emote(self.client, 'error')))
        try:
            price = int(list(args)[0])
            extra = '' if price in range(5, 1000000) else 'Invalid price. Setting price to default: 1000'
            if extra.endswith('1000'): price = 1000
            productName = '<product name undefined>' if len(list(args))<2 else ' '.join(list(args)[1:len(list(args))])
            if len(productName)>30: productName = ''.join(list(productName)[0:30])
            a = self.client.db.Shop.add_value(productName, price, ctx.guild)
            assert a['error']==False, a['ctx']
            return await ctx.send('{} | {}!\n{}'.format(self.client.utils.emote(self.client, 'success'), a['ctx'], extra))
        except Exception as e:
            await ctx.send('{} | {}!'.format(self.client.utils.emote(self.client, 'error'), str(e)))
    
    @command('remshop,delshop')
    @cooldown(5)
    async def delproduct(self, ctx, *args):
        if len(list(args))==0: return await ctx.send('{} | Please use the following parameters:\n`{}delproduct <name>` or to delete all stored in the shop, use `{}delproduct all`'.format(self.client.utils.emote(self.client, 'error'), self.client.utils.prefix, self.client.utils.prefix))
        if not ctx.author.guild_permissions.manage_guild: return await ctx.send('{} | You do not have the correct permissions to modify the server\'s shop.'.format(self.client.utils.emote(self.client, 'error')))
        if list(args)[0].lower()=='all':
            self.client.db.Shop.delete_shop(ctx.guild)
            return await ctx.send('{} | OK. All data for the shop is deleted.'.format(self.client.utils.emote(self.client, 'success')))
        try:
            data = self.client.db.Shop.remove_element(' '.join(list(args)), ctx.guild)
            assert data['error']==False, data['ctx']
            return await ctx.send('{} | {}!'.format(self.client.utils.emote(self.client, 'success'), data['ctx']))
        except Exception as e:
            await ctx.send('{} | {}!'.format(self.client.utils.emote(self.client, 'error'), str(e)))
    
    @command('bought')
    @cooldown(3)
    async def buy(self, ctx, *args):
        if len(list(args))==0: return await ctx.send('{} | Please use the following parameters:\n`{}buy <name>`'.format(self.client.utils.emote(self.client, 'error'), self.client.utils.prefix))
        if self.client.db.Economy.get(ctx.author.id)==None: raise self.client.utils.noProfile()
        try:
            data = self.client.db.Shop.buy(' '.join(list(args)), ctx.author)
            assert data['error']==False, data['ctx']
            return await ctx.send('{} | {}!'.format(self.client.utils.emote(self.client, 'success'), data['ctx']))
        except Exception as e:
            await ctx.send('{} | {}!'.format(self.client.utils.emote(self.client, 'error'), str(e)))
    
    @command('servershop,store,serverstore')
    @cooldown(2)
    async def shop(self, ctx):
        try:
            data = self.client.db.Shop.get_shop(ctx.guild)
            assert data['error']==False, data['ctx']
            em = discord.Embed(title='{}\'s shop'.format(ctx.guild.name), description='\n'.join(
                [str(i+1)+'. **'+str(data['ctx'][i]['name'])+'** (price: '+str(data['ctx'][i]['price'])+' :gem:)' for i in range(len(data['ctx']))]
            ), color=discord.Colour.from_rgb(201, 160, 112))
            return await ctx.send(embed=em)
        except Exception as e:
            await ctx.send('{} | {}!\nYou can always add a value using `{}addproduct <price> <name>`'.format(self.client.utils.emote(self.client, 'error'), str(e), self.client.utils.prefix))

    @command('delete,deletedata,deldata,del-data,delete-data')
    @cooldown(3600)
    async def reset(self, ctx):
        wait = await ctx.send(self.client.utils.emote(self.client, 'loading')+" | Please wait...")
        data = self.client.db.Economy.get(ctx.author.id)
        if data==None: raise self.client.utils.noProfile()
        else:
            await wait.edit(content=':thinking: | Are you sure? This action is irreversible!\n(Reply with yes/no)')
            def check_is_auth(m):
                return ctx.author == m.author
            try:
                waiting = await self.client.wait_for('message', check=check_is_auth, timeout=20.0)
            except:
                await ctx.send('{} | No it is then.'.format(self.client.utils.emote(self.client, 'success')))
            if 'y' in str(waiting.content).lower():
                self.client.db.Economy.delete_data(ctx.author.id)
                await ctx.send('{} | Data deleted. Thanks for playing.'.format(self.client.utils.emote(self.client, 'success')))
            else:
                await ctx.send('{} | No it is then.'.format(self.client.utils.emote(self.client, 'success')))
    
    @command()
    @cooldown(450)
    async def work(self, ctx):
        wait = await ctx.send(self.client.utils.emote(self.client, 'loading')+" | Please wait...")
        data = self.client.db.Economy.get(ctx.author.id)
        if data==None: raise self.client.utils.noProfile()
        else:
            reward = str(random.randint(100, 500))
            new_data = self.client.db.Economy.addbal(ctx.author.id, int(reward))
            job = random.choice(loads(open('/app/assets/json/work.json', 'r').read())['works'])
            if new_data=='success': await wait.edit(content=self.client.utils.emote(self.client, 'success')+f" | {ctx.author.name} worked {job} and earned {reward} bobux!")
            else: await wait.edit(content=self.client.utils.emote(self.client, 'error')+f" | Oops there was an error... Please report this to the owner using `1feedback.`\n`{new_data}`")
            
    @command()
    @cooldown(15)
    async def daily(self, ctx, *args):
        wait = await ctx.send(self.client.utils.emote(self.client, 'loading')+" | Please wait...")
        if self.client.db.Economy.get(ctx.author.id)==None: raise self.client.utils.noProfile()
        else:
            obj = self.client.db.Economy.can_vote(ctx.author.id)
            if obj['bool']:
                await wait.edit(content='', embed=discord.Embed(
                    title='Vote us at top.gg!',
                    description='**[VOTE HERE](https://top.gg/bot/'+str(self.client.user.id)+'/vote)**\nBy voting, we will give you rewards such as ***LOTS of bobux!***',
                    color = discord.Colour.green()
                ))
            else:
                await wait.edit(content='', embed=discord.Embed(
                    title='You can vote us again in '+str(obj['time'])+'!',
                    colour=discord.Colour.red()
                ))
    
    @command()
    @cooldown(10)
    async def transfer(self, ctx, *args):
        if len(list(args))==0 or len(ctx.message.mentions)==0: await ctx.send(self.client.utils.emote(self.client, 'error')+' | gimme some tag and some amount.')
        else:
            wait = await ctx.send(self.client.utils.emote(self.client, 'loading')+' | Please wait...?')
            amount = None
            for i in list(args):
                if i.isnumeric(): amount = int(i); break
            if amount==None: await wait.edit(content=self.client.utils.emote(self.client, 'error')+' | Give me some valid amount!')
            elif amount < 1: await wait.edit(content=self.client.utils.emote(self.client, 'error')+' | Invalid amount!')
            elif self.client.db.Economy.get(ctx.author.id)==None or self.client.db.Economy.get(ctx.message.mentions[0].id)==None:
                await wait.edit(content=self.client.utils.emote(self.client, 'error')+' | One of them doesn\'t have a profile!')
            else:
                if amount not in range(-2147483648, 2147483648):
                    return ctx.send('{} | woah lol. the amount is hella crazy!'.format(
                        self.client.utils.emote(self.client, 'error')
                    ))
                self.client.db.Economy.addbal(ctx.message.mentions[0].id, amount)
                self.client.db.Economy.delbal(ctx.author.id, amount) # EFFICIENT CODE LMFAO
                await wait.edit(content=self.client.utils.emote(self.client, 'success')+f' | Done! Transferred {str(amount)} bobux to {ctx.message.mentions[0].name}!')

    @command('steal,crime,stole,robs')
    @cooldown(60)
    async def rob(self, ctx, *args):
        if len(ctx.message.mentions)==0 or len(list(args))==0:
            await ctx.send(self.client.utils.emote(self.client, 'error')+' | Who?')
        else:
            if ctx.message.mentions[0].id==ctx.author.id:
                await ctx.send(self.client.utils.emote(self.client, 'error')+' | Seriously? Robbing yourself?')
            else:
                amount2rob = None
                for i in list(args):
                    if i.isnumeric(): amount2rob = int(i) ; break
                if amount2rob==None: await ctx.send(self.client.utils.emote(self.client, 'error')+' | How many bobux shall be robbed?')
                elif amount2rob>9999: await ctx.send(self.client.utils.emote(self.client, 'error')+' | Dude, you must be crazy. That\'s too many bobux!')
                elif amount2rob<0: await ctx.send(self.client.utils.emote(self.client, 'error')+' | minus??? HUH?')
                else:
                    wait = await ctx.send(self.client.utils.emote(self.client, 'loading')+' | *Please wait... robbing...*')
                    victim, stealer = self.client.db.Economy.get(ctx.message.mentions[0].id), self.client.db.Economy.get(ctx.author.id)
                    if victim==None or stealer==None:
                        await wait.edit(content=self.client.utils.emote(self.client, 'loading')+' | you/that guy doesn\'t even have a profile!')
                    else:
                        data = random.choice(loads(open('/app/assets/json/steal.json', 'r').read()))
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
        if len(list(args))==0: return await ctx.send('{} | How many money?\nOr use `1dep all` to deposit all of your money.'.format(self.client.utils.emote(self.client, 'error')))
        data = self.client.db.Economy.get(ctx.author.id)
        if data==None: raise self.client.utils.noProfile()
        if list(args)[0].lower()=='all':
            self.client.db.Economy.deposit(ctx.author.id, data['bal'])
            return await ctx.send('{} | OK. Deposited all of your bobux to the username601 bank.'.format(self.client.utils.emote(self.client, 'success')))
        try:
            num = int(list(args)[0])
            if num > data['bal']:
                return await ctx.send('{} | Your bank has more money than in your balance!'.format(self.client.utils.emote(self.client, 'error')))
            self.client.db.Economy.deposit(ctx.author.id, num)
            return await ctx.send('{} | OK. Deposited {} bobux to your bank.'.format(self.client.utils.emote(self.client, 'success'), num))
        except:
            await ctx.send('{} | Invalid number.'.format(self.client.utils.emote(self.client, 'error')))
    
    @command()
    @cooldown(10)
    async def withdraw(self, ctx, *args):
        if len(list(args))==0: return await ctx.send('{} | How many money?\nOr use `1widthdraw all` to get money from the bank.'.format(self.client.utils.emote(self.client, 'error')))
        data = self.client.db.Economy.get(ctx.author.id)
        if data==None: raise self.client.utils.noProfile()
        if list(args)[0].lower()=='all':
            self.client.db.Economy.withdraw(ctx.author.id, data['bankbal'])
            return await ctx.send('{} | OK. Withdrawed all of your bobux from the username601 bank.'.format(self.client.utils.emote(self.client, 'success')))
        try:
            num = int(list(args)[0])
            if num > data['bankbal']:
                return await ctx.send('{} | Your number is more than the one in your bank!'.format(self.client.utils.emote(self.client, 'error')))
            self.client.db.Economy.withdraw(ctx.author.id, num)
            return await ctx.send('{} | OK. Withdrawed {} bobux from your bank.'.format(self.client.utils.emote(self.client, 'success'), num))
        except:
            await ctx.send('{} | Invalid number.'.format(self.client.utils.emote(self.client, 'error')))

    @command('lb,leader,leaders,rich,richest,top')
    @cooldown(6)
    async def leaderboard(self, ctx):
        wait = await ctx.send(self.client.utils.emote(self.client, 'loading')+' | Please wait...')
        data = self.client.db.Economy.leaderboard(ctx.guild.members)
        if len(data)==0:
            await wait.edit(content=self.client.utils.emote(self.client, 'error')+' | This server doesn\'t have any members with profiles...')
        else:
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
                color = self.client.utils.get_embed_color(discord)
            ))
    
    @command('desc,description')
    @cooldown(2)
    async def setdesc(self, ctx, *args):
        if len(list(args))==0:
            await ctx.send(self.client.utils.emote(self.client, 'error')+' | What is the new description?')
        else:
            if len(list(args))>120:
                await ctx.send(self.client.utils.emote(self.client, 'error')+' | Your description is too long!')
            elif '://' in str(' '.join(list(args))):
                await ctx.send(self.client.utils.emote(self.client, 'error')+' | Please don\'t use links in the description! We don\'t allow that!')
            elif 'discord.gg' in str(' '.join(list(args))):
                await ctx.send(self.client.utils.emote(self.client, 'error')+' | Please don\'t use server invite links in the description! We don\'t allow that!')
            else:
                wait = await ctx.send(self.client.utils.emote(self.client, 'loading')+' | Please wait...')
                if self.client.db.Economy.get(ctx.author.id)==None:
                    raise self.client.utils.noProfile()
                else:
                    data = self.client.db.Economy.setdesc(ctx.author.id, str(' '.join(list(args))))
                    if data=='error':
                        await wait.edit(content=self.client.utils.emote(self.client, 'error')+' | Oopsies! There was an error...')
                    else:
                        await wait.edit(content=self.client.utils.emote(self.client, 'success')+' | Updated your description!')
    @command('balance,mybal,profile,me,myprofile')
    @cooldown(2)
    async def bal(self, ctx, *args):
        wait = await ctx.send(self.client.utils.emote(self.client, 'loading')+" | Please wait...")
        src, ava = self.client.utils.getUser(ctx, args), self.client.utils.getUserAvatar(ctx, args)
        if self.client.db.Economy.get(src.id)==None:
            raise self.client.utils.noProfile()
        else:
            data = self.client.db.Economy.getProfile(src.id, [i.id for i in ctx.guild.members if not i.bot])
            bfr, aft = data['main'], data['after']
            img = self.client.canvas.profile(src.name, ava, bfr, aft)
            await wait.delete()
            await ctx.send(file=discord.File(img, 'profile.png'))
    
    @command('newprofile')
    @cooldown(10)
    async def new(self, ctx):
        data = self.client.db.Economy.get(ctx.author.id)
        wait = await ctx.send(self.client.utils.emote(self.client, 'loading')+" | Please wait... creating your profile...")
        if data!=None:
            await wait.edit(content=self.client.utils.emote(self.client, 'error')+" | You already have a profile!")
        else:
            data = self.client.db.Economy.new(ctx.author.id)
            if data!='done':
                await wait.edit(content=self.client.utils.emote(self.client, 'error')+f" | Oops! there was an error: {data}")
            else:
                await wait.edit(content=self.client.utils.emote(self.client, 'success')+f" | Created your profile!")

def setup(client):
    client.add_cog(economy(client))