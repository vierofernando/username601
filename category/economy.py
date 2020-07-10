import discord
from discord.ext import commands
from sys import path
path.append("/app/modules")
import random
from json import loads
from username601 import BotEmotes
from database import Economy
from datetime import datetime

class economy(commands.Cog):
    def __init__(self, client):
        self.client = client
    
    @commands.command(pass_context=True)
    @commands.cooldown(1, 300, commands.BucketType.user)
    async def work(self, ctx):
        wait = await ctx.send(str(self.client.get_emoji(BotEmotes.loading))+" | Please wait...")
        data = Economy.get(ctx.message.author.id)
        if data==None: await wait.edit(content=str(self.client.get_emoji(BotEmotes.error))+" | You don't have a profile yet! Create a profile using `1new`")
        else:
            reward = str(random.randint(100, 500))
            new_data = Economy.addbal(ctx.message.author.id, int(reward))
            job = random.choice(loads(open('/app/assets/json/work.json', 'r').read())['works'])
            if new_data=='success': await wait.edit(content=str(self.client.get_emoji(BotEmotes.success))+f" | {ctx.message.author.name} worked {job} and earned {reward} diamonds!")
            else: await wait.edit(content=str(self.client.get_emoji(BotEmotes.error))+f" | Oops there was an error... Please report this to the owner using `1feedback.`\n`{new_data}`")
            
    @commands.command(pass_context=True, aliases=['d'])
    @commands.cooldown(1, 5, commands.BucketType.user)
    async def daily(self, ctx):
        wait = await ctx.send(str(self.client.get_emoji(BotEmotes.loading))+" | Please wait...")
        if Economy.get(ctx.message.author.id)==None: await wait.edit(content=str(self.client.get_emoji(BotEmotes.error))+" | You don't have a profile yet! Create a profile using `1new`")
        else:
            obj = Economy.can_vote(ctx.message.author.id)
            if obj['bool']:
                await wait.edit(content='', embed=discord.Embed(
                    title='Vote us at top.gg!',
                    description='[**VOTE HERE**](https://top.gg/bot/'+str(Config.id)+'/vote)\nBy voting, we will give you rewards such as ***LOTS of diamonds!***',
                    color = discord.Colour.green()
                ))
            else:
                await wait.edit(content='', embed=discord.Embed(
                    title='You can vote us again in '+str(obj['time'])+'!',
                    colour=discord.Colour.red()
                ))
    
    @commands.command(pass_context=True)
    @commands.cooldown(1, 30, commands.BucketType.user)
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
                await wait.edit(content=str(self.client.get_emoji(BotEmotes.error))+' | Neither of them has a profile!')
            else:
                Economy.addbal(ctx.message.mentions[0].id, amount)
                Economy.delbal(ctx.message.author.id, amount) # EFFICIENT CODE LMFAO
                await wait.edit(content=str(self.client.get_emoji(BotEmotes.success))+f' | Done! Transferred {str(amount)} diamonds to {ctx.message.mentions[0].name}!')

    @commands.command(pass_context=True, aliases=['steal'])
    @commands.cooldown(1, 60, commands.BucketType.user)
    async def rob(self, ctx, *args):
        if len(ctx.message.mentions)==0 or len(list(args))==0:
            await ctx.send(str(self.client.get_emoji(BotEmotes.error))+' | Who?')
        else:
            if ctx.message.mentions[0].id==ctx.message.author.id:
                await ctx.send(str(self.client.get_emoji(BotEmotes.error))+' | Seriously? Robbing yourself?')
            else:
                amount2rob = None
                for i in list(args):
                    if i.isnumeric(): amount2rob = int(i)
                if amount2rob==None: await ctx.send(str(self.client.get_emoji(BotEmotes.error))+' | How many diamonds shall be robbed?')
                elif amount2rob>9999: await ctx.send(str(self.client.get_emoji(BotEmotes.error))+' | Dude, you must be crazy. That\'s too many diamonds!')
                elif amount2rob<0: await ctx.send(str(self.client.get_emoji(BotEmotes.error))+' | minus??? HUH?')
                else:
                    wait = await ctx.send(str(self.client.get_emoji(BotEmotes.loading))+' | *Please wait... robbing...*')
                    if Economy.get(ctx.message.mentions[0].id)==None or Economy.get(ctx.message.author.id)==None:
                        await wait.edit(content=str(self.client.get_emoji(BotEmotes.loading))+' | you/that guy doesn\'t even have a profile!')
                    else:
                        data = random.choice(loads(open('/app/assets/json/steal.json', 'r').read()))
                        if not str(data['amount']).replace('-', '').isnumeric():
                            if data['amount']=='{SAME_AMOUNT}': robamount = -robamount
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
    
    @commands.command(pass_context=True, aliases=['lb', 'leader', 'leaders', 'rich', 'richest'])
    @commands.cooldown(1, 30, commands.BucketType.user)
    async def leaderboard(self, ctx):
        wait = await ctx.send(str(self.client.get_emoji(BotEmotes.loading))+' | Please wait...')
        data = Economy.leaderboard(ctx.guild.members)
        if len(data)==0:
            await wait.edit(content=str(self.client.get_emoji(BotEmotes.error))+' | This server doesn\'t have any members with profiles...')
        else:
            bals, count, total = [], 1, ''
            for a in data:
                bals.append(int(a.split('|')[1]))
            bals = sorted(bals)[::-1][0:20] # reverse because we need TOP 10 SHIT
            for each in bals:
                for j in data:
                    if int(j.split('|')[1])==each:
                        total += str(count)+'. **'+str(ctx.guild.get_member(int(j.split('|')[0])))+'** - '+str(each)+' :gem:\n'
                        count += 1
            await wait.edit(content='', embed=discord.Embed(
                title = ctx.guild.name+'\'s leaderboard',
                description = total,
                color = discord.Colour.from_rgb(201, 160, 112)
            ))
    
    @commands.command(pass_context=True, aliases=['desc', 'description'])
    @commands.cooldown(1, 30, commands.BucketType.user)
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
    @commands.command(pass_context=True, aliases=['balance', 'mybal', 'b', 'profile', 'me', 'myprofile'])
    @commands.cooldown(1, 15, commands.BucketType.user)
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
                description = '**Description: **\n'+data['desc']+'\n\n**Balance: **'+str(data["bal"])+' :gem:',
                color = discord.Colour.from_rgb(201, 160, 112)
            )
            embed.set_thumbnail(url=src.avatar_url)
            if data['desc']=='nothing here!': embed.set_footer(text='TIP: Type 1setdesc <text> to customize your description!')
            await wait.edit(content='', embed=embed)
    
    @commands.command(pass_context=True, aliases=['newprofile'])
    @commands.cooldown(1, 30, commands.BucketType.user)
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
