import discord
from discord.ext import commands
import sys
sys.path.append('/app/modules')
import username601 as myself
import random
from username601 import *
import pokebase as pb
import discordgames as Games
import asyncio

class games(commands.Cog):
    def __init__(self, client):
        self.client = client
    
    @commands.command(pass_context=True, aliases=['ttt'])
    @commands.cooldown(1, 12, commands.BucketType.user)
    async def tictactoe(self, ctx):
        box_nums = list('123456789')
        can_used = list('123456789')
        box = f' {box_nums[0]} | {box_nums[1]} | {box_nums[2]}\n===========\n {box_nums[3]} | {box_nums[4]} | {box_nums[5]}\n===========\n {box_nums[6]} | {box_nums[7]} | {box_nums[8]}\n'
        if no_args:
            embed = discord.Embed(title='TicTacToe™ wtih '+str(src.getTicTacToeHeader()), description=f'Plays tic-tac-toe with the BOT. Very simple.\n\n**To start playing, type;**\n`{prefix}tictactoe X` (To play tictactoe as X)\n`{prefix}tictactoe O` (To play tictactoe as O)', colour=discord.Colour.from_rgb(201, 160, 112))
            embed.set_image(url='https://raw.githubusercontent.com/vierofernando/username601/master/assets/pics/tictactoe.png')
            await ctx.send(embed=embed)
        else:
            if args[1].lower() not in list('xo'):
                await ctx.send('Must be X or O!')
            else:
                if args[1].lower()=='x':
                    user_sym = 'X'
                    bot_sym = 'O'
                else:
                    user_sym = 'O'
                    bot_sym = 'X'
                playing_with = ctx.message.author
                user_id = int(ctx.message.author.id)
                user_name = ctx.message.guild.get_member(user_id).display_name
                gameplay = True
                usedByUser = []
                usedByBot = []
                embed = discord.Embed(title='Playing Tictactoe with '+str(user_name), description=f'Viero Fernando ({user_sym}) | Username601 ({bot_sym})\nType the numbers to fill out the boxes.```{box}```', colour=discord.Colour.from_rgb(201, 160, 112))
                embed.set_footer(text='Type "endgame" to well, end the game. Or wait for 20 seconds and the game will kill itself! ;)')
                gameview = await ctx.send(embed=embed)
                while gameplay==True:
                    if Games.checkWinner(box_nums, user_sym, bot_sym)=='userwin':
                        await ctx.send(f'Congrats <@{user_id}>! You won against me! :tada:')
                        gameplay = False
                        break
                    elif Games.checkWinner(box_nums, user_sym, bot_sym)=='botwin':
                        await ctx.send(f'LOL, i win the tic tac toe! :tada:\nYou lose! :pensive:')
                        gameplay = False
                        break
                    elif Games.checkEndGame(can_used)==True:
                        await ctx.send('Nobody wins? OK... :neutral_face:')
                        gameplay = False
                        break
                    def is_not_stranger(m):
                        return m.author == playing_with
                    try:
                        trying = await self.client.wait_for('message', check=is_not_stranger, timeout=20.0)
                    except asyncio.TimeoutError:
                        await ctx.send(f'<@{user_id}> did not response in 20 seconds so i ended the game. Keep un-AFK!')
                        gameplay = False
                        break
                    if str(trying.content) in can_used:
                        for i in range(0, len(box_nums)):
                            if box_nums[i]==trying.content:
                                usedByUser.append(box_nums[i])
                                box_nums[i] = user_sym
                                for j in range(0, len(can_used)):
                                    if j==box_nums[i]:
                                        del can_used[j]
                                        break
                                break
                        bot_select = ''
                        while bot_select=='' and len(can_used)>1:
                            bot_select = random.choice(can_used)
                        for i in range(0, len(can_used)):
                            if can_used[i]==bot_select:
                                for j in range(0, len(box_nums)):
                                    if box_nums[j]==can_used[i]:
                                        box_nums[j] = bot_sym
                                        break
                                usedByBot.append(can_used[i])
                                del can_used[i]
                                break
                        box = f' {box_nums[0]} | {box_nums[1]} | {box_nums[2]}\n===========\n {box_nums[3]} | {box_nums[4]} | {box_nums[5]}\n===========\n {box_nums[6]} | {box_nums[7]} | {box_nums[8]}\n'
                        newembed = discord.Embed(title='Playing Tictactoe with '+str(user_name), description=f'Viero Fernando ({user_sym}) | Username601 ({bot_sym})\nType the numbers to fill out the boxes.```{box}```', colour=discord.Colour.from_rgb(201, 160, 112))
                        newembed.set_footer(text='Type "endgame" to well, end the game. Or wait for 20 seconds and the game will kill itself! ;)')
                        await ctx.send(embed=embed)
                    elif str(trying.content).lower()=='endgame':
                        await ctx.send('Game ended.')
                        gameplay = False
                        break

    @commands.command(pass_context=True, aliases=['defuse', 'boom'])
    @commands.cooldown(1, 5, commands.BucketType.user)
    async def bomb(self, ctx):
        def embedType(a):
            if a==1: return discord.Embed(title='The bomb exploded!', description='Game OVER!', colour=discord.Colour(000))
            elif a==2: return discord.Embed(title='The bomb defused!', description='Congratulations! :grinning:', colour=discord.Colour.from_rgb(201, 160, 112))
        embed = discord.Embed(title='DEFUSE THE BOMB!', description='**Cut the correct wire!\nThe bomb will explode in 15 seconds!**', colour=discord.Colour.from_rgb(201, 160, 112))
        main = await ctx.send(embed=embed)
        buttons = ['🔴', '🟡', '🔵', '🟢']
        for i in range(0, len(buttons)):
            await main.add_reaction(buttons[i])
        correct = random.choice(buttons)
        def check(reaction, user):
            return user == ctx.message.author
        try:
            reaction, user = await self.client.wait_for('reaction_add', timeout=15.0, check=check)
        except asyncio.TimeoutError:
            await main.edit(content='', embed=embedType(1))
        if str(reaction.emoji)!=correct:
            await main.edit(content='', embed=embedType(1))
        else:
            await main.edit(content='', embed=embedType(2))

    @commands.command(pass_context=True, aliases=['gn', 'guessnumber'])
    @commands.cooldown(1, 5, commands.BucketType.user)
    async def gusesnum(self, ctx):
        num = random.randint(5, 100)
        username = ctx.message.author.display_name
        user_class = ctx.message.author
        embed = discord.Embed(title='Starting the game!', description='You have to guess a *secret* number between 5 and 100!\n\nYou have 20 attempts, and 20 second timer in each attempt!\n\n**G O O D  L U C K**', colour=discord.Colour.from_rgb(201, 160, 112))
        await ctx.send(embed=embed)
        gameplay = True
        attempts = 20
        while gameplay==True:
            if attempts<1:
                await ctx.send('Time is up! The answer is **'+str(num)+'.**')
                gameplay = False
                break
            def check_not_stranger(m):
                return m.author == user_class
            try:
                trying = await self.client.wait_for('message', check=check_not_stranger, timeout=20.0)
            except asyncio.TimeoutError:
                await ctx.send(str(self.client.get_emoji(BotEmotes.error)) +' | You did not respond for the next 20 seconds!\nGame ended.')
                gameplay = False
                break
            if trying.content.isnumeric()==False:
                await ctx.send('That is not a number!')
                attempts = int(attempts) - 1
            else:
                if int(trying.content)<num:
                    await ctx.send('Higher!')
                    attempts = int(attempts) - 1
                if int(trying.content)>num:
                    await ctx.send('Lower!')
                    attempts = int(attempts) - 1
                if int(trying.content)==num:
                    await ctx.send(str(self.client.get_emoji(BotEmotes.success)) +' | You are correct!\n**The answer is '+str(num)+'!**')
                    gameplay = False
                    break

    @commands.command(pass_context=True)
    @commands.cooldown(1, 15, commands.BucketType.user)
    async def pokequic(self, ctx):
        wait = await ctx.send(str(self.client.get_emoji(BotEmotes.loading)) + ' | Please wait... Generating quiz...')
        num = random.randint(1, 800)
        try:
            corr = pb.pokemon(str(num)).name
        except Exception as e:
            await wait.edit(content=str(self.client.get_emoji(BotEmotes.error)) + f' | An error occured! ```{e}```')
        hint = 2
        attempt = 10
        gameplay = True
        guy = ctx.message.author
        while gameplay==True:
            newembed = discord.Embed(title='Pokemon Quiz!', description=f'Guess the pokemon\'s name!\nTimeout: 45 seconds.\nHint left: **{str(hint)}** | Attempts left: **{str(attempt)}**', colour=discord.Colour.from_rgb(201, 160, 112))
            newembed.set_image(url=f'https://assets.pokemon.com/assets/cms2/img/pokedex/full/{str(num)}.png')
            newembed.set_footer(text='Type "hint" to give.. uh... the HINT! :D')
            newembed.set_thumbnail(url=f'https://raw.githubusercontent.com/PokeAPI/sprites/master/sprites/pokemon/{str(num)}.png')
            await wait.edit(content='', embed=newembed)
            if int(attempt)<1:
                await ctx.send('You lose! The pokemon is **'+str(corr)+'**!')
                gameplay = False
                break
            def checking(m):
                return m.author == guy
            try:
                guessing = await self.client.wait_for('message', check=checking, timeout=45.0)
            except asyncio.TimeoutError:
                attempt = int(attempt) - 1
                await ctx.send('Too late! Game ended... :pensive:')
                gameplay = False
                break
            if str(guessing.content).lower()==corr:
                currentmsg = guessing
                await currentmsg.add_reaction('✅')
                await ctx.send(str(self.client.get_emoji(BotEmotes.success)) +' | You are correct! The pokemon is **'+str(corr)+'**')
                gameplay = False
                break
            elif str(guessing.content).lower()=='hint':
                currentmsg = guessing
                if hint<1:
                    await currentmsg.add_reaction('❌')
                    attempt = int(attempt) - 1
                else:
                    await currentmsg.add_reaction('✅')
                    thehint = random.choice([myself.hintify(corr), 'Pokemon name starts with "'+str(list(corr)[0])+'"', 'Pokemon name has '+str(len(corr))+' letters!', 'Pokemon name ends with "'+str(list(corr)[len(corr)-1])+'"'])
                    await ctx.send('Hint: '+thehint+'!')
                    hint = int(hint) - 1
                    attempt = int(attempt) - 1
            else:
                if attempt!=0:
                    await guessing.add_reaction('❌')
                    attempt = int(attempt) - 1
                else:
                    await guessing.add_reaction('❌')
                    await ctx.send('You lose! The pokemon is **'+str(corr)+'**!')
                    gameplay = False
                    break

    @commands.command(pass_context=True)
    @commands.cooldown(1, 10, commands.BucketType.user)
    async def trivia(self, ctx):
        al = None
        try:
            wait = await ctx.send(str(self.client.get_emoji(BotEmotes.loading)) + ' | Please wait... generating quiz...')
            auth = ctx.message.author
            data = myself.api('https://wiki-quiz.herokuapp.com/v1/quiz?topics=Science')
            q = random.choice(data['quiz'])
            choices = ''
            for i in range(0, len(q['options'])):
                al = list('🇦🇧🇨🇩')
                if q['answer']==q['options'][i]:
                    corr = al[i]
                choices = choices + al[i] +' '+ q['options'][i]+'\n'
            embed = discord.Embed(title='Trivia!', description='**'+q['question']+'**\n'+choices, colour=discord.Colour.from_rgb(201, 160, 112))
            embed.set_footer(text='Answer by clicking the reaction! You have 60 seconds.')
            await wait.edit(content='', embed=embed)
            for i in range(0, len(al)):
                await wait.add_reaction(al[i])
        except Exception as e:
            await wait.edit(content=str(self.client.get_emoji(BotEmotes.error)) + f' | An error occured!\nReport this using {prefix}feedback.\n```{e}```')
        guy = ctx.message.author
        def check(reaction, user):
            return user == guy
        try:
            reaction, user = await client.wait_for('reaction_add', timeout=60.0, check=check)
        except asyncio.TimeoutError:
            await main.add_reaction('😔')
        if str(reaction.emoji)==str(corr):
            await ctx.send(str(self.client.get_emoji(BotEmotes.success)) +' | <@'+str(guy.id)+'>, Congrats! You are correct. :partying_face:')
        else:
            await ctx.send(str(self.client.get_emoji(BotEmotes.error)) +' | <@'+str(guy.id)+'>, You are incorrect. The answer is '+str(corr)+'.')

def setup(client):
    client.add_cog(games(client))