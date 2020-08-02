import discord
from discord.ext import commands
from sys import path
path.append("/home/runner/hosting601/modules")
from decorators import command, cooldown
import random
from json import loads
from username601 import *
from database import Economy
from datetime import datetime

class economy(commands.Cog):
    def __init__(self, client):
        self.client = client
    
    @command('deletedata,deldata,del-data,delete-data')
    @cooldown(3600)
    async def reset(self, ctx):
        wait = await ctx.send(str(self.client.get_emoji(BotEmotes.loading))+" | Please wait...")
        data = Economy.get(ctx.author.id)
        if data==None: await wait.edit(content=str(self.client.get_emoji(BotEmotes.error))+" | You don't have a profile yet! Create a profile using `1new`")
        else:
            await wait.edit(content=':thinking: | Are you sure? This action is irreversible!\n(Reply with yes/no)')
            def check_is_auth(m):
                return ctx.message.author == m.author
            try:
                waiting = await self.client.wait_for('message', check=check_is_auth, timeout=20.0)
            except:
                await ctx.send('{} | No it is then.'.format(str(self.client.get_emoji(BotEmotes.success))))
            if 'y' in str(waiting.content).lower():
                Economy.delete_data(ctx.author.id)
                await ctx.send('{} | Data deleted. Thanks for playing.'.format(str(self.client.get_emoji(BotEmotes.success))))
            else:
                await ctx.send('{} | No it is then.'.format(str(self.client.get_emoji(BotEmotes.success))))
    
    @command()
    @cooldown(1800)
    async def work(self, ctx):
        wait = await ctx.send(str(self.client.get_emoji(BotEmotes.loading))+" | Please wait...")
        data = Economy.get(ctx.author.id)
        if data==None: await ctx.send("you dont have a profile yet! Create a profile using `1new`")
        else:
            reward = str(random.randint(100, 500))
            new_data = Economy.addbal(ctx.message.author.id, int(reward))
            job = random.choice(loads(open('/home/runner/hosting601/assets/json/work.json', 'r').read())['works'])
            if new_data=='success': await wait.edit(content=str(self.client.get_emoji(BotEmotes.success))+f" | {ctx.message.author.name} worked {job} and earned {reward} diamonds!")
            else: await wait.edit(content=str(self.client.get_emoji(BotEmotes.error))+f" | Oops there was an error... Please report this to the owner using `1feedback.`\n`{new_data}`")
            
    @command()
    @cooldown(15)
    async def daily(self, ctx, *args):
        wait = await ctx.send(str(self.client.get_emoji(BotEmotes.loading))+" | Please wait...")
        if Economy.get(ctx.message.author.id)==None: await wait.edit(content=str(self.client.get_emoji(BotEmotes.error))+" | You don't have a profile yet! Create a profile using `1new`")
        else:
            obj = Economy.can_vote(ctx.message.author.id)
            if '--claim' in ''.join(list(args)).lower():
                if not obj['bool']:
                    await wait.edit(content='', embed=discord.Embed(title='You have not voted yet!', color=discord.Color.red()))
                else:
                    dt = Economy.daily(ctx.message.author.id)
                    Economy.vote(ctx.message.author.id, True)
                    if str(dt).isnumeric():
                        await wait.edit(content='', embed=discord.Embed(title='You claimed your daily for {} diamonds!'.format(str(dt)), color=discord.Color.green()))
                    else:
                        await wait.edit(content=str(self.client.get_emoji(BotEmotes.error))+' | ERROR: `'+str(dt)+'`')
            else:
                if obj['bool']:
                    Economy.vote(ctx.message.author.id, False)
                    em = embed=discord.Embed(
                        title='Vote us at top.gg!',
                        description='**[VOTE HERE](https://top.gg/bot/'+str(Config.id)+'/vote)**\nBy voting, we will give you rewards such as ***LOTS of diamonds!***',
                        color = discord.Colour.green()
                    )
                    em.set_footer(text='Type '+str(Config.prefix)+'daily --claim to claim rewards!')
                    await wait.edit(content='', embed=em)
                else:
                    await wait.edit(content='', embed=discord.Embed(
                        title='You can vote us again in '+str(obj['time'])+'!',
                        colour=discord.Colour.red()
                    ))
    
    @command()
    @cooldown(30)
    async def transfer(self, ctx, *args):
        if len(list(args))==0 or len(ctx.message.mentions)==0: await ctx.send(str(self.client.get_emoji(BotEmotes.error))+' | gimme some tag and some amount.')
        else:
            wait = await ctx.send(str(self.client.get_emoji(BotEmotes.loading))+' | Please wait...?')
            amount = None
            for i in list(args):
                if i.isnumeric(): amount = int(i); break
            if amount==None: await wait.edit(content=str(self.client.get_emoji(BotEmotes.error))+' | Give me some valid amount!')
            elif amount < 1: await wait.edit(content=str(self.client.get_emoji(BotEmotes.error))+' | Invalid amount!')
            elif Economy.get(ctx.message.author.id)==None or Economy.get(ctx.message.mentions[0].id)==None:
                await wait.edit(content=str(self.client.get_emoji(BotEmotes.error))+' | One of them doesn\'t have a profile!')
            else:
                if amount not in range(-2147483648, 2147483648):
                    return ctx.send('{} | woah lol. the amount is hella crazy!'.format(
                        str(self.client.get_emoji(BotEmotes.error))
                    ))
                Economy.addbal(ctx.message.mentions[0].id, amount)
                Economy.delbal(ctx.message.author.id, amount) # EFFICIENT CODE LMFAO
                await wait.edit(content=str(self.client.get_emoji(BotEmotes.success))+f' | Done! Transferred {str(amount)} diamonds to {ctx.message.mentions[0].name}!')

    @command('steal,crime,stole,robs')
    @cooldown(60)
    async def rob(self, ctx, *args):
        if len(ctx.message.mentions)==0 or len(list(args))==0:
            await ctx.send(str(self.client.get_emoji(BotEmotes.error))+' | Who?')
        else:
            if ctx.message.mentions[0].id==ctx.message.author.id:
                await ctx.send(str(self.client.get_emoji(BotEmotes.error))+' | Seriously? Robbing yourself?')
            else:
                amount2rob = None
                for i in list(args):
                    if i.isnumeric(): amount2rob = int(i) ; break
                if amount2rob==None: await ctx.send(str(self.client.get_emoji(BotEmotes.error))+' | How many diamonds shall be robbed?')
                elif amount2rob>9999: await ctx.send(str(self.client.get_emoji(BotEmotes.error))+' | Dude, you must be crazy. That\'s too many diamonds!')
                elif amount2rob<0: await ctx.send(str(self.client.get_emoji(BotEmotes.error))+' | minus??? HUH?')
                else:
                    wait = await ctx.send(str(self.client.get_emoji(BotEmotes.loading))+' | *Please wait... robbing...*')
                    victim, stealer = Economy.get(ctx.message.mentions[0].id), Economy.get(ctx.message.author.id)
                    if victim==None or stealer==None:
                        await wait.edit(content=str(self.client.get_emoji(BotEmotes.loading))+' | you/that guy doesn\'t even have a profile!')
                    else:
                        if victim['bal'] > stealer['bal']:
                            return await wait.edit(content='{} | You cannot rob who is richer than you.'.format(
                                str(self.client.get_emoji(BotEmotes.error))
                            ))
                        data = random.choice(loads(open('/home/runner/hosting601/assets/json/steal.json', 'r').read()))
                        if not str(data['amount']).replace('-', '').isnumeric():
                            if data['amount']=='{SAME_AMOUNT}': robamount = -amount2rob
                            elif data['amount']=='{REAL}': robamount = int(amount2rob)
                            else: robamount = -Economy.get(ctx.message.author.id)['bal']
                        else: robamount = data['amount']
                        if robamount > 0:
                            Economy.addbal(ctx.message.author.id, robamount) ; Economy.delbal(ctx.message.mentions[0].id, robamount)
                            statement = f'You stole {str(robamount)} in total.'
                        elif robamount==0:
                            statement = f'You left empty-handed.'
                        else:
                            Economy.delbal(ctx.message.author.id, robamount*-1) ; Economy.addbal(ctx.message.mentions[0].id, robamount*-1)
                            statement = f'You lost {str(robamount)} diamonds.'
                        embed = discord.Embed(
                            title = f'{ctx.message.author.name} robbing {ctx.message.mentions[0].name} scene be like',
                            description = data['statement'].replace('{NL}', '\n').replace('{D1}', ctx.message.author.name).replace('{D2}', ctx.message.mentions[0].name),
                            color = discord.Colour.red()
                        )
                        embed.set_footer(text=statement)
                        await wait.edit(content='', embed=embed)
    
    @command('dep')
    @cooldown(20)
    async def deposit(self, ctx, *args):
        if len(list(args))==0: return await ctx.send('{} | How many money?\nOr use `1dep all` to deposit all of your money.'.format(str(self.client.get_emoji(BotEmotes.error))))
        data = Economy.get(ctx.author.id)
        if data==None: return await ctx.send('{} | You don\'t have a profile! Use `{}new`'.format(
            str(self.client.get_emoji(BotEmotes.error)), Config.prefix
        ))
        if list(args)[0].lower()=='all':
            Economy.deposit(ctx.author.id, data['bal'])
            return await ctx.send('{} | OK. Deposited all of your diamonds to the username601 bank.'.format(str(self.client.get_emoji(BotEmotes.success))))
        try:
            num = int(list(args)[0])
            if num > data['bal']:
                return await ctx.send('{} | Your bank has more money than in your balance!'.format(str(self.client.get_emoji(BotEmotes.error))))
            Economy.deposit(ctx.author.id, num)
            return await ctx.send('{} | OK. Deposited {} diamonds to your bank.'.format(str(self.client.get_emoji(BotEmotes.success))))
        except:
            await ctx.send('{} | Invalid number.'.format(str(self.client.get_emoji(BotEmotes.error))))
    
    @command()
    @cooldown(20)
    async def withdraw(self, ctx, *args):
        if len(list(args))==0: return await ctx.send('{} | How many money?\nOr use `1widthdraw all` to get money from the bank.'.format(str(self.client.get_emoji(BotEmotes.error))))
        data = Economy.get(ctx.author.id)
        if data==None: return await ctx.send('{} | You don\'t have a profile! Use a `{}new.`'.format(str(self.client.get_emoji(BotEmotes.error)), Config.prefix))
        if list(args)[0].lower()=='all':
            Economy.withdraw(ctx.author.id, data['bankbal'])
            return await ctx.send('{} | OK. Withdrawed all of your diamonds from the username601 bank.'.format(str(self.client.get_emoji(BotEmotes.success))))
        try:
            num = int(list(args)[0])
            if num > data['bankbal']:
                return await ctx.send('{} | Your number is more than the one in your bank!'.format(str(self.client.get_emoji(BotEmotes.error))))
            Economy.withdraw(ctx.author.id, num)
            return await ctx.send('{} | OK. Withdrawed {} diamonds from your bank.'.format(str(self.client.get_emoji(BotEmotes.success))))
        except:
            await ctx.send('{} | Invalid number.'.format(str(self.client.get_emoji(BotEmotes.error))))

    @command('lb,leader,leaders,rich,richest,top')
    @cooldown(30)
    async def leaderboard(self, ctx):
        wait = await ctx.send(str(self.client.get_emoji(BotEmotes.loading))+' | Please wait...')
        data = Economy.leaderboard(ctx.guild.members)
        if len(data)==0:
            await wait.edit(content=str(self.client.get_emoji(BotEmotes.error))+' | This server doesn\'t have any members with profiles...')
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
                color = discord.Colour.from_rgb(201, 160, 112)
            ))
    
    @command('desc,description')
    @cooldown(30)
    async def setdesc(self, ctx, *args):
        if len(list(args))==0:
            await ctx.send(str(self.client.get_emoji(BotEmotes.error))+' | What is the new description?')
        else:
            if len(list(args))>100:
                await ctx.send(str(self.client.get_emoji(BotEmotes.error))+' | Your description is too long!')
            elif '://' in str(' '.join(list(args))):
                await ctx.send(str(self.client.get_emoji(BotEmotes.error))+' | Please don\'t use links in the description! We don\'t allow that!')
            elif 'discord.gg' in str(' '.join(list(args))):
                await ctx.send(str(self.client.get_emoji(BotEmotes.error))+' | Please don\'t use server invite links in the description! We don\'t allow that!')
            else:
                wait = await ctx.send(str(self.client.get_emoji(BotEmotes.loading))+' | Please wait...')
                if Economy.get(ctx.message.author.id)==None:
                    await wait.edit(content=str(self.client.get_emoji(BotEmotes.error))+' | You haven\'t created a profile yet! use `1new`!')
                else:
                    data = Economy.setdesc(ctx.message.author.id, str(' '.join(list(args))))
                    if data=='error':
                        await wait.edit(content=str(self.client.get_emoji(BotEmotes.error))+' | Oopsies! There was an error...')
                    else:
                        await wait.edit(content=str(self.client.get_emoji(BotEmotes.success))+' | Updated your description!')
    @command('balance,mybal,profile,me,myprofile')
    @cooldown(15)
    async def bal(self, ctx):
        wait = await ctx.send(str(self.client.get_emoji(BotEmotes.loading))+" | Please wait...")
        if len(ctx.message.mentions)==0: src = ctx.message.author
        else: src = ctx.message.mentions[0]
        data = Economy.get(src.id)
        if data==None:
            await wait.edit(content=str(self.client.get_emoji(BotEmotes.error))+" | You don't have a profile yet! Create a profile using `1new`")
        else:
            embed = discord.Embed(
                title = src.name+"'s profile",
                description = '**Description: **\n'+data['desc']+'\n\n**Balance: **'+str(data["bal"])+' :gem:\n**Bank balance: **'+str(data['bankbal'])+' :gem:',
                color = discord.Colour.from_rgb(201, 160, 112)
            )
            embed.set_thumbnail(url=src.avatar_url)
            if data['desc']=='nothing here!': embed.set_footer(text='TIP: Type 1setdesc <text> to customize your description!')
            await wait.edit(content='', embed=embed)
    
    @command('newprofile')
    @cooldown(30)
    async def new(self, ctx):
        data = Economy.get(ctx.message.author.id)
        wait = await ctx.send(str(self.client.get_emoji(BotEmotes.loading))+" | Please wait... creating your profile...")
        if data!=None:
            await wait.edit(content=str(self.client.get_emoji(BotEmotes.error))+" | You already have a profile!")
        else:
            data = Economy.new(ctx.message.author.id)
            if data!='done':
                await wait.edit(content=str(self.client.get_emoji(BotEmotes.error))+f" | Oops! there was an error: {data}")
            else:
                await wait.edit(content=str(self.client.get_emoji(BotEmotes.success))+f" | Created your profile!")

def setup(client):
    client.add_cog(economy(client))
