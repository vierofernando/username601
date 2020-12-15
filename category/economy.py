import discord
import random
from discord.ext import commands
from decorators import *
from json import loads
from datetime import datetime
from asyncio import sleep
from random import choice, randint

class economy(commands.Cog):
    def __init__(self, client):
        self.fish_json = loads(open(client.util.json_dir+'/fish.json', 'r').read())
        self.steal_json = loads(open(client.util.json_dir+'/steal.json', 'r').read())
        self.works = loads(open(client.util.json_dir+'/work.json', 'r').read())['works']
        self.client = client
    
    def getfish(self):
        found, ctx = False, None
        for i in self.fish_json['results']['overall']:
            if randint(1, i['chance'])==1:
                found, ctx = True, i
                break
        if not found: ctx = choice(self.fish_json['results']['else'])
        return {
            "catched": found,
            "ctx": ctx
        }
    
    @command()
    @cooldown(30)
    @require_args()
    async def gamble(self, ctx, *args):
        lucky = random.choice([False, True])
        try:
            amount = int(args[0])
        except:
            raise ctx.bot.util.BasicCommandException('Please make sure you input a number!')
        
        if not lucky:
            ctx.bot.db.Economy.delbal(ctx.author.id, amount)
        else:
            ctx.bot.db.Economy.addbal(ctx.author.id, amount)
        return await ctx.send((ctx.bot.util.success_emoji if lucky else ctx.bot.util.error_emoji) + ' | ' + (f"Congratulations! {ctx.author.display_name} just won {amount} bobux!" if lucky else f"Yikes! {ctx.author.display_name} just lost {amount} bobux..."))

    @command()
    @cooldown(120)
    async def beg(self, ctx):
        c = random.randint(1, 3)
        if ctx.bot.db.Economy.get(ctx.author.id) is None: raise ctx.bot.util.BasicCommandException("Doesn't have a profile yet. Try `1new` to have a profile.")
        if c==1:
            award = random.randint(100, 800)
            ctx.bot.db.Economy.addbal(ctx.author.id, award)
            return await ctx.send('{} | You begged and got {} bobux!'.format(ctx.bot.util.success_emoji, award))
        await ctx.send('{} | Stop begging! Try again later. There is only 1/3 chance you will get a bobux.'.format(ctx.bot.util.error_emoji))

    @command(['fishing'])
    @cooldown(60)
    async def fish(self, ctx):
        if ctx.bot.db.Economy.get(ctx.author.id) is None: raise ctx.bot.util.BasicCommandException("Doesn't have a profile yet. Try `1new` to have a profile.")
        wait = await ctx.send('{} | {}'.format(ctx.bot.util.loading_emoji, random.choice(
            self.fish_json['waiting']
        )))
        await sleep(random.randint(3, 8))
        res = self.getfish()
        if res['catched']:
            awards = random.randint(res['ctx']['worth']['min'], res['ctx']['worth']['max'])
            ctx.bot.db.Economy.addbal(ctx.author.id, awards)
            return await wait.edit(content='{} | Congratulations! You caught a {} and sell it worth for {} bobux!'.format(res['ctx']['emote'], res['ctx']['name'], awards))
        return await wait.edit(content='{} | You only caught {}...'.format(ctx.bot.util.error_emoji, res['ctx']))

    @command()
    @cooldown(7)
    async def buylist(self, ctx):
        source = ctx.author if len(ctx.message.mentions)==0 else ctx.message.mentions[0]
        if ctx.bot.db.Economy.get(ctx.author.id) is None: raise ctx.bot.util.BasicCommandException("Doesn't have a profile yet. Try `1new` to have a profile.")
        try:
            data = ctx.bot.db.Economy.getBuyList(source)
            assert not data['error'], data['ctx']
            return await ctx.send(embed=discord.Embed(title='{}\'s buy list'.format(source.display_name), description=data['ctx'], color=ctx.me.color))
        except Exception as e:
            raise ctx.bot.util.BasicCommandException(str(e))

    @command(['addshop'])
    @cooldown(5)
    @require_args()
    async def addproduct(self, ctx, *args):
        if not ctx.author.guild_permissions.manage_guild: raise ctx.bot.util.BasicCommandException('You do not have the correct permissions to modify the server\'s shop.')
        try:
            price = int(args[0])
            extra = '' if price in range(5, 1000000) else 'Invalid price. Setting price to default: 1000'
            if extra.endswith('1000'): price = 1000
            productName = '<product name undefined>' if len(args)<2 else ' '.join(list(args)[1:])
            if len(productName)>30: productName = ''.join(list(productName)[0:30])
            a = ctx.bot.db.Shop.add_value(productName, price, ctx.guild)
            assert not a['error'], a['ctx']
            return await ctx.send('{} | {}!\n{}'.format(ctx.bot.util.success_emoji, a['ctx'], extra))
        except Exception as e:
            raise ctx.bot.util.BasicCommandException(str(e))
    
    @command(['remshop', 'delshop'])
    @cooldown(5)
    @require_args()
    async def delproduct(self, ctx, *args):
        if not ctx.author.guild_permissions.manage_guild: raise ctx.bot.util.BasicCommandException('You do not have the correct permissions to modify the server\'s shop.')
        if args[0].lower()=='all':
            ctx.bot.db.Shop.delete_shop(ctx.guild)
            return await ctx.send('{} | OK. All data for the shop is deleted.'.format(ctx.bot.util.success_emoji))
        try:
            data = ctx.bot.db.Shop.remove_element(' '.join(args), ctx.guild)
            assert data['error']==False, data['ctx']
            return await ctx.send('{} | {}!'.format(ctx.bot.util.success_emoji, data['ctx']))
        except Exception as e:
            raise ctx.bot.util.BasicCommandException(str(e))
    
    @command(['bought'])
    @cooldown(3)
    @require_args()
    async def buy(self, ctx, *args):
        if ctx.bot.db.Economy.get(ctx.author.id) is None: raise ctx.bot.util.BasicCommandException("Doesn't have a profile yet. Try `1new` to have a profile.")
        try:
            data = ctx.bot.db.Shop.buy(' '.join(args), ctx.author)
            assert not data['error'], data['ctx']
            return await ctx.send('{} | {}!'.format(ctx.bot.util.success_emoji, data['ctx']))
        except Exception as e:
            raise ctx.bot.util.BasicCommandException(str(e))
    
    @command(['servershop', 'store', 'serverstore'])
    @cooldown(2)
    async def shop(self, ctx):
        try:
            data = ctx.bot.db.Shop.get_shop(ctx.guild)
            assert data['error']==False, data['ctx']
            em = discord.Embed(title='{}\'s shop'.format(ctx.guild.name), description='\n'.join(
                list(map(lambda x: str(x + 1)+". **"+ data['ctx'][x]['name'] + '** (price: '+ str(data['ctx'][x]['price']) + " :gem:)", range(len(data['ctx']))))
            ), color=ctx.me.color)
            return await ctx.send(embed=em)
        except Exception as e:
            raise ctx.bot.util.BasicCommandException(f'{str(e)}!\nYou can always add a value using `{ctx.bot.command_prefix}addproduct <price> <name>`')

    @command(['delete', 'deletedata', 'deldata', 'del-data', 'delete-data'])
    @cooldown(3600)
    async def reset(self, ctx):
        data = ctx.bot.db.Economy.get(ctx.author.id)
        if data is None: raise ctx.bot.util.BasicCommandException("Doesn't have a profile yet. Try `1new` to have a profile.")
        else:
            wait = await ctx.send(ctx.bot.util.loading_emoji+" | Please wait...")
            await wait.edit(content=':thinking: | Are you sure? This action is irreversible!\n(Reply with yes/no)')
            def check_is_auth(m):
                return ctx.author == m.author
            try:
                waiting = await ctx.bot.wait_for('message', check=check_is_auth, timeout=20.0)
            except:
                await ctx.send('{} | No it is then.'.format(ctx.bot.util.success_emoji))
            if 'y' in str(waiting.content).lower():
                ctx.bot.db.Economy.delete_data(ctx.author.id)
                await ctx.send('{} | Data deleted. Thanks for playing.'.format(ctx.bot.util.success_emoji))
            else:
                await ctx.send('{} | No it is then.'.format(ctx.bot.util.success_emoji))
    
    @command()
    @cooldown(450)
    async def work(self, ctx):
        data = ctx.bot.db.Economy.get(ctx.author.id)
        if data is None: raise ctx.bot.util.BasicCommandException("Doesn't have a profile yet. Try `1new` to have a profile.")
        else:
            wait = await ctx.send(ctx.bot.util.loading_emoji+" | Please wait...")
            reward = str(random.randint(100, 500))
            new_data = ctx.bot.db.Economy.addbal(ctx.author.id, int(reward))
            job = random.choice(self.works)
            if new_data=='success': await wait.edit(content=ctx.bot.util.success_emoji+f" | {ctx.author.display_name} worked {job} and earned {reward} bobux!")
            else: raise ctx.bot.util.BasicCommandException(f"Oops there was an error... Please report this to the owner using `{ctx.bot.command_prefix}feedback.`\n`{new_data}`")
            
    @command()
    @cooldown(15)
    async def daily(self, ctx, *args):
        wait = await ctx.send(ctx.bot.util.loading_emoji+" | Please wait...")
        if ctx.bot.db.Economy.get(ctx.author.id) is None: raise ctx.bot.util.BasicCommandException("Doesn't have a profile yet. Try `1new` to have a profile.")
        else:
            obj = ctx.bot.db.Economy.can_vote(ctx.author.id)
            if obj['bool']:
                # await wait.edit(content='', embed=discord.Embed(
                #     title='Vote us at top.gg!',
                #     description='**[VOTE HERE](https://top.gg/bot/'+str(ctx.bot.user.id)+'/vote)**\nBy voting, we will give you rewards such as ***LOTS of bobux!***',
                #     color = discord.Colour.green()
                # ))
                rewards = ctx.bot.db.Economy.daily(ctx.author.id)
                await ctx.send("{} | Congrats! You got **{} bobux** as a daily reward! You can try again in 12 hours.".format(ctx.bot.util.success_emoji, rewards))
            else:
                await wait.edit(content='', embed=discord.Embed(
                    title='You can get rewards again in '+str(obj['time'])+'!',
                    colour=discord.Colour.red()
                ))
    
    @command()
    @cooldown(10)
    @require_args()
    async def transfer(self, ctx, *args):
        await ctx.trigger_typing()
        amount = ctx.bot.Parser.get_numbers(count)
        
        if not amount:
            raise ctx.bot.util.BasicCommandException("Please give a valid amount.")
        elif amount not in range(1, 500001):
            raise ctx.bot.util.BasicCommandException("Invalid amount range.")
        elif ctx.bot.db.Economy.get(ctx.author.id) is None or ctx.bot.db.Economy.get(ctx.message.mentions[0].id) is None:
            raise ctx.bot.util.BasicCommandException("One of them does not have a profile.")
        ctx.bot.db.Economy.addbal(ctx.message.mentions[0].id, amount)
        ctx.bot.db.Economy.delbal(ctx.author.id, amount) # EFFICIENT CODE LMFAO
        await wait.edit(content=ctx.bot.util.success_emoji+f' | Done! Transferred {amount} bobux to {ctx.message.mentions[0].display_name}!')

    @command(['steal', 'crime', 'stole', 'robs'])
    @cooldown(60)
    async def rob(self, ctx, *args):
        if len(ctx.message.mentions)==0 or len(args)==0:
            raise ctx.bot.util.BasicCommandException(f'Rob who? Try `1rob <mention> <amount>`.')
        else:
            if ctx.message.mentions[0].id==ctx.author.id:
                raise ctx.bot.util.BasicCommandException('Seriously? Robbing yourself?')
            else:
                amount2rob = ctx.bot.Parser.get_numbers(args)
                if amount2rob is None: raise ctx.bot.util.BasicCommandException('How many bobux shall be robbed?')
                elif amount2rob>9999: raise ctx.bot.util.BasicCommandException('Dude, you must be crazy. That\'s too many bobux!')
                elif amount2rob<0: raise ctx.bot.util.BasicCommandException('minus??? HUH?')
                else:
                    wait = await ctx.send(ctx.bot.util.loading_emoji+' | *Please wait... robbing...*')
                    victim, stealer = ctx.bot.db.Economy.get(ctx.message.mentions[0].id), ctx.bot.db.Economy.get(ctx.author.id)
                    if victim is None or stealer is None:
                        raise ctx.bot.util.BasicCommandException('you/that guy doesn\'t even have a profile!')
                    else:
                        data = random.choice(self.steal_json)
                        if not str(data['amount']).replace('-', '').isnumeric():
                            if data['amount']=='{SAME_AMOUNT}': robamount = -amount2rob
                            elif data['amount']=='{REAL}': robamount = int(amount2rob)
                            else: robamount = -ctx.bot.db.Economy.get(ctx.author.id)['bal']
                        else: robamount = data['amount']
                        if robamount > 0:
                            ctx.bot.db.Economy.addbal(ctx.author.id, robamount) ; ctx.bot.db.Economy.delbal(ctx.message.mentions[0].id, robamount)
                            statement = f'You stole {str(robamount)} in total.'
                        elif robamount==0:
                            statement = f'You left empty-handed.'
                        else:
                            ctx.bot.db.Economy.delbal(ctx.author.id, robamount*-1) ; ctx.bot.db.Economy.addbal(ctx.message.mentions[0].id, robamount*-1)
                            statement = f'You lost {str(robamount)} bobux.'
                        embed = discord.Embed(
                            title = f'{ctx.author.display_name} robbing {ctx.message.mentions[0].display_name} scene be like',
                            description = data['statement'].replace('{NL}', '\n').replace('{D1}', ctx.author.display_name).replace('{D2}', ctx.message.mentions[0].display_name),
                            color = discord.Colour.red()
                        )
                        embed.set_footer(text=statement)
                        await wait.edit(content='', embed=embed)
    
    @command(['dep'])
    @cooldown(10)
    @require_args()
    async def deposit(self, ctx, *args):
        data = ctx.bot.db.Economy.get(ctx.author.id)
        if data is None: raise ctx.bot.util.BasicCommandException("Doesn't have a profile yet. Try `1new` to have a profile.")
        if args[0].lower()=='all':
            ctx.bot.db.Economy.deposit(ctx.author.id, data['bal'])
            return await ctx.send('{} | OK. Deposited all of your bobux to the username601 bank.'.format(ctx.bot.util.success_emoji))
        try:
            num = int(args[0])
            if num > data['bal']:
                raise ctx.bot.util.BasicCommandException('Your bank has more money than in your balance!')
            ctx.bot.db.Economy.deposit(ctx.author.id, num)
            return await ctx.send('{} | OK. Deposited {} bobux to your bank.'.format(ctx.bot.util.success_emoji, num))
        except:
            raise ctx.bot.util.BasicCommandException("Invalid number.")
    
    @command()
    @cooldown(10)
    @require_args()
    async def withdraw(self, ctx, *args):
        data = ctx.bot.db.Economy.get(ctx.author.id)
        if data is None: raise ctx.bot.util.BasicCommandException("Doesn't have a profile yet. Try `1new` to have a profile.")
        if args[0].lower()=='all':
            ctx.bot.db.Economy.withdraw(ctx.author.id, data['bankbal'])
            return await ctx.send('{} | OK. Withdrawed all of your bobux from the username601 bank.'.format(ctx.bot.util.success_emoji))
        try:
            num = int(args[0])
            if num > data['bankbal']:
                raise ctx.bot.util.BasicCommandException('Your number is more than the one in your bank!')
            ctx.bot.db.Economy.withdraw(ctx.author.id, num)
            return await ctx.send('{} | OK. Withdrawed {} bobux from your bank.'.format(ctx.bot.util.success_emoji, num))
        except:
            raise ctx.bot.util.BasicCommandException("Invalid number.")

    @command(['lb', 'leader', 'leaders', 'rich', 'richest', 'top'])
    @cooldown(6)
    async def leaderboard(self, ctx):
        data = ctx.bot.db.Economy.leaderboard(ctx.guild.members)
        if len(data)==0:
            raise ctx.bot.util.BasicCommandException('This server doesn\'t have any members with profiles...')
        else:
            wait = await ctx.send(ctx.bot.util.loading_emoji+' | Please wait...')
            total, bals, ids = [], sorted(list(map(lambda x: int(x.split("|")[1]), data)))[::-1][0:20], []
            for a in range(len(bals)):
                person = [{
                    'userid': int(i.split('|')[0]),
                    'bal': int(i.split('|')[1])
                } for i in data if int(i.split('|')[1])==bals[a] and int(i.split('|')[0]) not in ids][0]
                ids.append(person['userid'])
                user = ctx.guild.get_member(person['userid'])
                total.append('{}. {}#{} - **{}** :gem:'.format(
                    a+1, user.display_name, user.discriminator, person['bal']
                ))
            await wait.edit(content='', embed=discord.Embed(
                title = ctx.guild.name+'\'s leaderboard',
                description = '\n'.join(total),
                color = ctx.me.color
            ))
    
    @command(['desc', 'description'])
    @cooldown(2)
    @require_args()
    async def setdesc(self, ctx, *args):
        if len(args)>120: raise ctx.bot.util.BasicCommandException('Your description is too long!')
        newdesc = ' '.join(args)
        for i in ['discord.gg', 'discord.com/', 'bit.ly', '://', 'nigga', 'nigger', 'discordapp.com']:
            if i in newdesc.lower(): raise ctx.bot.util.BasicCommandException('Your description has invalid/blocked text!')
        wait = await ctx.send(ctx.bot.util.loading_emoji+' | Please wait...')
        if ctx.bot.db.Economy.get(ctx.author.id) is None:
            raise ctx.bot.util.BasicCommandException("Doesn't have a profile yet. Try `1new` to have a profile.")
        data = ctx.bot.db.Economy.setdesc(ctx.author.id, newdesc)
        if data=='error': return await wait.edit(content=ctx.bot.util.error_emoji+' | Oopsies! There was an error...')
        return await wait.edit(content=ctx.bot.util.success_emoji+' | Updated your description!')
    
    @command(['balance', 'mybal', 'profile', 'me', 'myprofile'])
    @cooldown(2)
    async def bal(self, ctx, *args):
        src = ctx.bot.Parser.parse_user(ctx, args)
        ava = src.avatar_url_as(format="png")
        
        if ctx.bot.db.Economy.get(src.id) is None:
            raise ctx.bot.util.BasicCommandException("Doesn't have a profile yet. Try `1new` to have a profile.")
        wait = await ctx.send(ctx.bot.util.loading_emoji+" | Please wait...")
        data = ctx.bot.db.Economy.getProfile(src.id, [i.id for i in ctx.guild.members if not i.bot])
        bfr, aft = data['main'], data['after']
        img = await ctx.bot.canvas.profile(src.name, ava, bfr, aft)
        await wait.delete()
        await ctx.send(file=discord.File(img, 'profile.png'))
    
    @command(['newprofile'])
    @cooldown(10)
    async def new(self, ctx):
        data = ctx.bot.db.Economy.get(ctx.author.id)
        wait = await ctx.send(ctx.bot.util.loading_emoji+" | Please wait... creating your profile...")
        if data is not None:
            raise ctx.bot.util.BasicCommandException("You already have a profile!")
        data = ctx.bot.db.Economy.new(ctx.author.id)
        if data!='done':
            raise ctx.bot.util.BasicCommandException(f"Oops! there was an error: {data}")
        return await wait.edit(content=ctx.bot.util.success_emoji+f" | Created your profile!")

def setup(client):
    client.add_cog(economy(client))