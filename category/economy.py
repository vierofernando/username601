import discord
import random
from discord.ext import commands
from decorators import *
from PIL import ImageColor
from json import loads
from time import time
from asyncio import sleep
from random import choice, randint

class economy(commands.Cog):
    def __init__(self, client):
        self.blacklisted_words = [
            "nigga",
            "nigger",
            "discord.gg",
            "http://",
            "https://",
            "discordapp.com",
            "discord.com",
            "fuck",
            "shit",
            "bitch"
        ]

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
    async def bet(self, ctx, *args):
        lucky = random.choice([False, True])
        try:
            amount = ctx.bot.Parser.get_numbers(args)
            assert amount[0] in range(0, 69420)
        except:
            raise ctx.bot.util.BasicCommandException('Please make sure you input a valid number!')
        
        self.db.modify("economy", self.db.types.INCREMENT, {"userid": ctx.author.id}, {"bal": (amount[0] if lucky else -amount[0])})
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
    @cooldown(7)
    @require_profile()
    async def daily(self, ctx, *args):
        await ctx.trigger_typing()

        last_daily = self.db.get("economy", {"userid": ctx.author.id})["lastDaily"]
        if (not last_daily) or ((time() - last_daily) > 43200): # 43200 is 12 hours.
            reward = random.randint(500, 1000)
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
            assert amount[0] in range(0, 100000), "The limit is 100.000 bobux!"
            assert self.db.exist("economy", {"userid": member.id}), f"{member.display_name} does not have a profile!"
            await ctx.send(embed=discord.Embed(title=f"Successfully transferred {amount[0]:,} bobux to {member.display_name}!", color=discord.Color.green()))
        
            self.db.modify("economy", self.db.types.INCREMENT, {"userid": ctx.author.id}, {"bal": -amount[0]})
            self.db.modify("economy", self.db.types.INCREMENT, {"userid": member.id}, {"bal": amount[0]})
        except Exception as e:
            raise ctx.bot.util.BasicCommandException(str(e))
    
    @command(['steal', 'crime', 'stole', 'robs'])
    @cooldown(120)
    @require_args(2)
    @require_profile()
    async def rob(self, ctx, *args):
        try:
            number = ctx.bot.Parser.get_numbers(args)[0]
            assert len(ctx.message.mentions) == 0, "Please mention someone to rob!"
            member = ctx.message.mentions[0]
            assert not member.bot, f"{member.display_name} is a botum."
            assert member != ctx.author, f"Error! `RecursionError: maximum recursion depth exceeded`"
            
            victim_data = self.db.get("economy", {"userid": member.id})
            assert (victim_data is not None), f"{member.display_name} has no profile!"
            assert victim_data["bal"] > 0, f"{member.display_name} only has 0 bobux! He is too poor to be robbed!"
            assert member.status != discord.Status.offline, f"{member.display_name} is currently offline!"
            
            if not number:
                number = random.randint(0, data["bal"])
            assert number <= victim_data["bal"], f"Number must be below the opponent's bobux. ({victim_data['bal']})"
            data = self.db.get("economy", {"userid": ctx.author.id})
            assert data["bal"] > 750, f"You need at least 750 bobux ({data['bal'] - 750} more) to rob someone."
            
            await ctx.send(embed=discord.Embed(title=f"Successfully robbed {member.display_name} for {number:,} bobux.", color=discord.Color.green()))
            self.db.modify("economy", self.db.types.INCREMENT, {"userid": ctx.author.id}, {"bal": number})
            self.db.modify("economy", self.db.types.INCREMENT, {"userid": member.id})
        except AssertionError as e:
            raise ctx.bot.util.BasicCommandException(str(e))
    
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

    @command(['balance', 'profile', 'economy'])
    @cooldown(5)
    async def bal(self, ctx, *args):
        if (len(args) > 0):
            await ctx.trigger_typing()

            if (args[0].lower() in ["--desc", "--setdesc", "--description", "--bio"]):
                await ctx.trigger_typing()
                try:
                    text = " ".join(args[1:])
                    assert text != "", "Please add a text for your new bio."
                    for blacklisted_word in self.blacklisted_words:
                        assert blacklisted_word not in text, "Please do not include any links or bad words in your bio!"
                    data = self.db.get("economy", {"userid": ctx.author.id})
                    
                    assert data is not None, f"You do not have a profile. Use `{ctx.bot.command_prefix}new` to create a brand new profile."
                    assert data["bal"] > 500, f"You need at least 500 bobux to change bio ({(data['bal'] - 500):,} more bobux required)"

                    await ctx.send(embed=discord.Embed(title=f"Successfully changed your bio.", color=discord.Color.green()).set_footer(text="Your bio is too long, so we capped it down to 50 characters." if len(text) > 50 else ""))
                    self.db.modify("economy", self.db.types.CHANGE, {"userid": ctx.author.id}, {"desc": text[0:50]})
                    return
                except Exception as e:
                    raise ctx.bot.util.BasicCommandException(str(e))
            elif (args[0].lower() in ["--color", "--set-color", "--col"]):
                try:
                    color = ImageColor.getrgb(' '.join(args[1:]))
                    data = self.db.get("economy", {"userid": ctx.author.id})
                    assert (data is not None), f"You do not have a profile. Use `{ctx.bot.command_prefix}new` to create a brand new profile."
                    assert data["bal"] > 1000, f"You need at least 1,000 bobux to change bio ({(data['bal'] - 1000):,} more bobux required)"
                except ValueError:
                    raise ctx.bot.util.BasicCommandException("Invalid Hex color input.")
                except AssertionError as e:
                    raise ctx.bot.util.BasicCommandException(str(e))
                
                await ctx.send(embed=discord.Embed(title="Changed the color for your profile to `"+ ('#%02x%02x%02x' % color).upper() +"`.", color=discord.Color.from_rgb(*color)))
                self.db.modify("economy", self.db.types.CHANGE, {"userid": ctx.author.id}, {"color": str(color).replace(" ", "")[1:-1]})
                return
            elif (args[0].lower() in ["--card", "--image"]):
                member = ctx.bot.Parser.parse_user(ctx, args[1:])                
                data = self.db.get("economy", {"userid": member.id})

                if not data:
                    raise ctx.bot.util.BasicCommandException(f"{member.display_name} does not have any profile.")
                card = ctx.bot.ProfileCard(ctx, member, profile=data, session=ctx.bot.util.default_client, font_path=ctx.bot.util.fonts_dir + "/NotoSansDisplay-Bold.otf")
                byte = await card.draw()
                await ctx.send(file=discord.File(byte, "card.png"))
                await card.close()
                del card, byte, data, member
                return

        member = ctx.bot.Parser.parse_user(ctx, args)
        data = self.db.get("economy", {"userid": member.id})
        if not data:
            raise ctx.bot.util.BasicCommandException(f"{member.display_name} does not have any profile!")
        
        embed = ctx.bot.Embed(
            ctx,
            title=f"{member.display_name}'s profile",
            thumbnail=member.avatar_url,
            fields={
                "Balance": f"{data['bal']:,} bobux" + "\n" f"{data['bankbal']:,} bobux (bank)",
                "Description": data["desc"],
                "Daily": f"**[:white_check_mark: can be claimed using `{ctx.bot.command_prefix}daily`]**" if ((not data["lastDaily"]) or ((time() - data["lastDaily"]) > 43200)) else f"Can be claimed in {ctx.bot.util.strfsecond((data['lastDaily'] + 43200) - time())}"
            },
            color=discord.Color.from_rgb(*[int(i) for i in data["color"].split(",")]) if data.get("color") else ctx.me.color
        )
        
        if data.get("color"):
            rgb = tuple([int(i) for i in data["color"].split(",")])
            embed.fields["Color"] = f"**Hex: **{('#%02x%02x%02x' % rgb).upper()}"+"\n"+f"**RGB: **{rgb[0]}, {rgb[1]}, {rgb[2]}"
            del rgb
        
        await embed.send()
        del embed, data
    
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