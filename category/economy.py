import discord
import random
from discord.ext import commands
from decorators import *
from json import loads
from time import time
from asyncio import sleep
from random import choice, randint

class economy(commands.Cog):
    def __init__(self, client):
        self.fish_json = loads(open(client.util.json_dir+'/fish.json', 'r').read())
        self.steal_json = loads(open(client.util.json_dir+'/steal.json', 'r').read())
        self.works = loads(open(client.util.json_dir+'/work.json', 'r').read())['works']
        self.db = client.db
    
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
    @require_profile()
    async def gamble(self, ctx, *args):
        lucky = random.choice([False, True])
        try:
            amount = ctx.bot.Parser.get_numbers(args)
            assert amount in range(0, 1000000)
        except:
            raise ctx.bot.util.BasicCommandException('Please make sure you input a valid number!')
        
        self.db.modify("economy", self.db.types.INCREMENT, {"userid": ctx.author.id}, {"bal": (amount if lucky else -amount)})
        return await ctx.send((ctx.bot.util.success_emoji if lucky else ctx.bot.util.error_emoji) + ' | ' + (f"Congratulations! {ctx.author.display_name} just won {amount:,} bobux!" if lucky else f"Yikes! {ctx.author.display_name} just lost {amount:,} bobux..."))

    @command()
    @cooldown(120)
    @require_profile()
    async def beg(self, ctx):
        chance = random.randint(1, 3)
        if chance == 1:
            award = random.randint(100, 800)
            self.db.modify("economy", self.db.types.INCREMENT, {"userid": ctx.author.id}, {"bal": award})
            return await ctx.send(embed=discord.Embed(title=f'You begged and got {award:,} bobux!', color=discord.Color.green()))
        raise ctx.bot.util.BasicCommandException('Stop begging! Try again later. There is only 1/3 chance you will get a bobux.')

    @command(['fishing'])
    @cooldown(60)
    @require_profile()
    async def fish(self, ctx):
        wait = await ctx.send('{} | {}'.format(ctx.bot.util.loading_emoji, random.choice(
            self.fish_json['waiting']
        )))
        await sleep(random.randint(3, 8))
        res = self.getfish()
        if res['catched']:
            award = random.randint(res['ctx']['worth']['min'], res['ctx']['worth']['max'])
            self.db.modify("economy", self.db.types.INCREMENT, {"userid": ctx.author.id}, {"bal": award})
            return await ctx.send(embed=discord.Embed(description=f"{res['ctx']['emote']} | Congratulations! You caught a {res['ctx']['name']} and sell it worth for {award:,} bobux!", color=discord.Color.green()))
        raise ctx.bot.util.BasicCommandException(f"Yikes! You only caught {res['ctx']}... Try again later!")

    @command(['delete', 'deletedata', 'deldata', 'del-data', 'delete-data'])
    @cooldown(3600)
    @require_profile()
    async def reset(self, ctx):
        embed = await ctx.send(embed=discord.Embed(title="Are you sure? This action is irreversible!", description="Reply with `yes` or `no`. Not replying will default to `no`.", color=discord.Color.red()))
        wait = ctx.bot.WaitForMessage(ctx, check=(lambda x: x.channel == ctx.channel and x.author == ctx.author and x.content.lower() in ["yes", "y", "no", "n"]))
        message = await wait.get_message()
        del wait

        if (not message) or (message.content.lower() in ['n', 'no']):
            return await embed.edit(embed=discord.Embed(title="OK. No it is then.", color=discord.Color.green()))
        self.db.delete("economy", {"userid": ctx.author.id})
        return await embed.edit(embed=discord.Embed(title="Alright. Your profile is gone. Reduced to atoms.", color=discord.Color.orange()))

    @command()
    @cooldown(450)
    @require_profile()
    async def work(self, ctx):
        await ctx.trigger_typing()
        reward = random.randint(100, 500)
        job = random.choice(self.works)
        self.db.modify("economy", self.db.types.INCREMENT, {"userid": ctx.author.id}, {"bal": reward})
        return await ctx.send(embed=discord.Embed(title=f"{ctx.author.display_name} worked {job} and earned {reward:,} bobux!", color=discord.Color.green()))
    
    @command()
    @cooldown(15)
    @require_profile()
    async def daily(self, ctx, *args):
        await ctx.trigger_typing()

        last_daily = self.db.get("economy", {"userid": ctx.author.id})["lastDaily"]
        if (not last_daily) or ((time() - last_daily) > 43200): # 43200 is 12 hours.
            reward = random.randint(100, 42069)
            await ctx.send(embed=discord.Embed(title=f"You earned your Daily for {reward:,} bobux!", color=discord.Color.green()))
            self.db.modify("economy", self.db.types.INCREMENT, {"userid": ctx.author.id}, {"bal": reward})
            self.db.modify("economy", self.db.types.CHANGE, {"userid": ctx.author.id}, {"lastDaily": time()})
        else:
            raise ctx.bot.util.BasicCommandException(f"You can earn your daily in {ctx.bot.util.strfsecond((last_daily + 43200) - time())}!")

    @command()
    @cooldown(10)
    @require_args()
    @require_profile()
    async def transfer(self, ctx, *args):
        await ctx.trigger_typing()
        try:
            member = ctx.message.mentions[0]
            amount = ctx.bot.Parser.get_numbers(args)
            assert amount in range(0, 100000), "The limit is 100.000 bobux!"
            assert self.db.exist("economy", {"userid": member.id}), f"{member.display_name} does not have a profile!"
            await ctx.send(embed=discord.Embed(title=f"Successfully transferred {amount:,} bobux to {member.display_name}!", color=discord.Color.green()))
        
            self.db.modify("economy", self.db.types.INCREMENT, {"userid": ctx.author.id}, {"bal": -amount})
            self.db.modify("economy", self.db.types.INCREMENT, {"userid": member.id}, {"bal": amount})
        except Exception as e:
            raise ctx.bot.util.BasicCommandException(str(e))
    
    @command(['steal', 'crime', 'stole', 'robs'])
    @cooldown(60)
    @require_profile()
    async def rob(self, ctx, *args):
        return await ctx.send("This command is temporarily closed. Sorry!")
    
    @command(['dep'])
    @cooldown(10)
    @require_args()
    @require_profile()
    async def deposit(self, ctx, *args):
        data = self.db.get("economy", {"userid": ctx.author.id})
        if args[0].lower() == 'all':
            await ctx.send(embed=discord.Embed(title='OK. Deposited all of your bobux to the username601 bank.', color=discord.Color.green()))
            self.db.modify("economy", self.db.types.CHANGE, {"userid": ctx.author.id}, {"bankbal": data['bal']})
            self.db.modify("economy", self.db.types.CHANGE, {"userid": ctx.author.id}, {"bal": 0})
            return

        try:
            num = ctx.bot.util.Parser.get_numbers(args)
            if num > data['bal']:
                raise ctx.bot.util.BasicCommandException('Your input has more bobux than the one in your balance!')
            await ctx.send(embed=discord.Embed(title=f'OK. Deposited {num:,} bobux to your bank.', color=discord.Color.green()))

            self.db.modify("economy", self.db.types.INCREMENT, {"userid": ctx.author.id}, {"bankbal": num})
            self.db.modify("economy", self.db.types.INCREMENT, {"userid": ctx.author.id}, {"bal": -num})
        except:
            raise ctx.bot.util.BasicCommandException("Invalid number.")
    
    @command()
    @cooldown(10)
    @require_args()
    @require_profile()
    async def withdraw(self, ctx, *args):
        data = self.db.get("economy", {"userid": ctx.author.id})
        if args[0].lower() == 'all':
            await ctx.send(embed=discord.Embed(title='OK. Withdrew all of your bobux from the username601 bank.', color=discord.Color.green()))
            self.db.modify("economy", self.db.types.CHANGE, {"userid": ctx.author.id}, {"bankbal": 0})
            self.db.modify("economy", self.db.types.CHANGE, {"userid": ctx.author.id}, {"bal": data['bankbal']})
            return

        try:
            num = ctx.bot.util.Parser.get_numbers(args)
            if num > data['bankbal']:
                raise ctx.bot.util.BasicCommandException('Your input has more bobux than the one in the bank!')
            await ctx.send(embed=discord.Embed(title=f'OK. Withdrew {num:,} bobux from the bank.', color=discord.Color.green()))

            self.db.modify("economy", self.db.types.INCREMENT, {"userid": ctx.author.id}, {"bal": num})
            self.db.modify("economy", self.db.types.INCREMENT, {"userid": ctx.author.id}, {"bankbal": -num})
        except:
            raise ctx.bot.util.BasicCommandException("Invalid number.")

    @command(['lb', 'leader', 'leaders', 'rich', 'richest', 'top'])
    @cooldown(6)
    async def leaderboard(self, ctx):
        return await ctx.send("Sorry! This command is closed temporarily due to rewrite.")
        #data = self.db.Economy.leaderboard(ctx.guild.members)
        #if len(data)==0:
        #    raise ctx.bot.util.BasicCommandException('This server doesn\'t have any members with profiles...')
        #else:
        #    wait = await ctx.send(ctx.bot.util.loading_emoji+' | Please wait...')
        #    total, bals, ids = [], sorted(list(map(lambda x: int(x.split("|")[1]), data)))[::-1][0:20], []
        #    for a in range(len(bals)):
        #        person = [{
        #            'userid': int(i.split('|')[0]),
        #            'bal': int(i.split('|')[1])
        #        } for i in data if int(i.split('|')[1])==bals[a] and int(i.split('|')[0]) not in ids][0]
        #        ids.append(person['userid'])
        #        user = ctx.guild.get_member(person['userid'])
        #        total.append('{}. {}#{} - **{}** :gem:'.format(
        #            a+1, user.display_name, user.discriminator, person['bal']
        #        ))
        #    await wait.edit(content='', embed=discord.Embed(
        #        title = ctx.guild.name+'\'s leaderboard',
        #        description = '\n'.join(total),
        #        color = ctx.me.color
        #    ))

    @command(['balance', 'mybal', 'profile', 'me', 'myprofile'])
    @cooldown(2)
    @require_profile()
    async def bal(self, ctx, *args):
        data = self.db.get("economy", {"userid": ctx.author.id})

        embed = ctx.bot.Embed(
            ctx,
            title=f"{ctx.author.display_name}'s profile",
            image=ctx.author.avatar_url,
            fields={
                "Balance": f"{data['bal']:,} bobux" + "\n" f"{data['bankbal']:,} bobux (bank)",
                "Description": data["desc"]
            }
        )
        await embed.send()
        del embed, data

        # src = ctx.bot.Parser.parse_user(ctx, args)
        # ava = src.avatar_url_as(format="png")
        # 
        # await ctx.trigger_typing()
        # data = self.db.Economy.getProfile(src.id, [i.id for i in ctx.guild.members if not i.bot])
        # bfr, aft = data['main'], data['after']
        # img = await ctx.bot.canvas.profile(src.name, ava, bfr, aft)
        # await ctx.send(file=discord.File(img, 'profile.png'))
    
    @command(['newprofile'])
    @cooldown(10)
    async def new(self, ctx):
        if self.db.exist("economy", {"userid": ctx.author.id}):
            raise ctx.bot.util.BasicCommandException("You already have a profile. No need to create another.")
        
        await ctx.send(embed=discord.Embed(title=f"Created your profile! Use {ctx.bot.command_prefix}bal to view your profile.", color=discord.Color.green()))
        self.db.add("economy", {
            "userid": ctx.author.id,
            "lastDaily": None,
            "bal": 0,
            "bankbal": 0
        })

def setup(client):
    client.add_cog(economy(client))
