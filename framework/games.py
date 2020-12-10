from aiohttp import ClientSession
from random import choice, randint
from discord import Embed, Color
from random import randint, choice
from asyncio import sleep

class GuessMyNumber:
    def __init__(self):
        self.rounds_left = 5
        self.my_number = randint(0, 100)

    async def play(self, ctx) -> bool:
        embed = ctx.bot.Embed(ctx, title="Guess my number!", desc="I have a random number between 0 and 100. Guess my number by sending it in the chat! You have 5 turns. Each turn i give you 15 seconds to guess.")
        await embed.send()
        check_func = (lambda x: x.channel == ctx.channel and x.author == ctx.author and x.content.isnumeric())
        while self.rounds_left != 0:
            wait_for = ctx.bot.WaitForMessage(ctx, timeout=15.0, check=check_func)
            response = await wait_for.get_message()
            del wait_for

            if not response:
                await ctx.send(f"{ctx.author.display_name} went AFK. So i closed the game.")
                return

            if int(response.content) == my_number:
                await ctx.send(f"You are correct! my number is {self.my_number}")
                return True

            await ctx.send("Lower!" if (int(response.content) > self.my_number) else "Higher!")
            self.rounds_left -= 1
        await ctx.send(f"You lost! My number is actually {self.my_number}!")
        return False

class Trivia:
    def __init__(self, topic: str, session = None) -> None:
        self.topic = topic
        self.session = session if session else ClientSession()

    async def generate_question(self, ctx) -> dict:
        result = await self.session.get(f"https://wiki-quiz.herokuapp.com/v1/quiz?topics={ctx.bot.util.encode_uri(self.topic)}&limit=10")
        assert result.status == 200, f"API returns a HTTP status code: {result.status}. Please insert a valid topic."
        result = await result.json()
        
        return choice(result["quiz"])

    async def start(self, ctx) -> bool:
        question = await self.generate_question(ctx)
        alpha = list("ABCD")

        embed = ctx.bot.Embed(
            ctx,
            title=f"{self.topic} Trivia",
            desc="\n".join([f"{alpha[i]}. **{question['options'][i]}**" for i in range(4)])
        )
        message = await embed.send()
        del embed

        wait = ctx.bot.WaitForMessage(ctx, timeout=25.5, check=(lambda x: x.channel == ctx.channel and x.author == ctx.author and len(x.content) == 1 and (x.content.upper() in alpha)))
        resp = await wait.get_message()
        if not resp:
            return
        del wait

        if alpha.index(resp.content.upper()) == question["options"].index(question["answer"]):
            await message.edit(embed=Embed(title="Congratulations! You are correct!", color=Color.green()))
            return True
        await message.edit(embed=Embed(title=f"Sorry, the correct answer is {alpha[question['options'].index(question['answer'])]}. {question['answer']}"))

class GuessAvatar:
    def __init__(self, ctx) -> None:
        """ Creates a 'guess what avatar this belongs to' game """
        members = ctx.guild.members
        assert len(members) >= 4, "Member count must be more than 4"
        
        generator = randint(0, len(members) - 1)
        self.members = ctx.guild.members[generator:(generator + 4)]

        missing = (len(self.members) - 4) * -1
        for i in range(missing):
            self.members.append(members[i])
        del members
        self.ctx = ctx
        self.correct_order = randint(0, 3)
        self.alpha = list("ABCD")
    
    async def start(self) -> bool:
        """ begin """
        
        embed = self.ctx.bot.Embed(
            self.ctx,
            title="What does this avatar belong to?",
            desc="\n".join([f"{self.alpha[i]}. **{self.members[i].display_name}**" for i in range(4)]),
            image=self.members[self.correct_order].avatar_url_as(format="png")
        )
        message = await embed.send()
        del embed

        waitFor = self.ctx.bot.WaitForMessage(self.ctx, timeout=25.0, check=(lambda x: x.channel == self.ctx.channel and x.author == self.ctx.author and len(x.content) == 1 and (x.content.upper() in self.alpha)))
        response = await waitFor.get_message()
        del waitFor
        if not response:
            await message.edit(embed=Embed(title="Game canceled bacause you ignored me :(", color=Color.orange()))
            return

        if self.alpha.index(response.content.upper()) == self.correct_order:
            await message.edit(embed=Embed(title="Congratulations, you are correct!", color=Color.green()))
            return True
        await message.edit(embed=Embed(title=f"Sorry, the correct answer is {self.alpha[self.correct_order]}. {self.members[self.correct_order].display_name}", color=Color.red()))
        return False

class MathQuiz:
    def __init__(self) -> None:
        """ Math quiz, for nerds """
        self.symbols = {
            "÷": "//",
            "+": "+",
            "-": "-",
            "×": "*"
        }

    def generate_question(self) -> None:
        generator = randint(0, 1)
        if generator == 0:
            question, res = self.basic_question()
            repeat = randint(0, 5)
            for _ in range(repeat):
                question, res = self.basic_question(extend_to=question)
            self.question = question
            self.answer = res
            return
        self.question, self.answer = self.square_root()

    def __pythonic_equation(self, string: str) -> str:
        for symbol in self.symbols.keys():
            string = string.replace(symbol, self.symbols[symbol])
        return string

    def basic_question(self, extend_to: str = None) -> tuple:
        symbol = choice(list(self.symbols.keys()))
        num1, num2 = randint(0, 1000), randint(0, 1000)

        if extend_to:
            res = eval(self.__pythonic_equation(extend_to))
            return f"{res} {symbol} {num1}", eval(f"{res}{self.symbols[symbol]}{num1}")

        return f"{num1} {symbol} {num2}", eval(f"{num1}{self.symbols[symbol]}{num2}")

    def square_root(self) -> tuple:
        perfect_number = randint(2, 50)
        return "√" + str(eval(f"{perfect_number}**2")), perfect_number

class GeographyQuiz:
    def __init__(self, session = None) -> None:
        """ The class that generates geography kind of quizzes using the restcountries API. """
        self.session = session if session else ClientSession()
        self._topics = { # {key: placeholder}
            'capital': 'Capital City',
            'region': 'Region',
            'subregion': 'Sub-region',
            'population': 'Sub-region',
            'demonym': 'Demonym',
            'nativeName': 'Native name'
        }
    
    async def generate_question(self) -> None:
        """ As the function name says, """
        topic = choice(list(self._topics.keys()))
        arrayList = await self.session.get("https://restcountries.eu/rest/v2")
        arrayList = await arrayList.json() # get request to the country API
        countries = []
        
        for _ in range(4):
            country = choice(arrayList)
            del arrayList[arrayList.index(country)]
            countries.append(country)
        del arrayList
        
        country = choice(countries)
        del countries[countries.index(country)]
        self.question = f"What is the {self._topics[topic]} of {country['name']}?"
        self.correct_order = randint(0, 3)
        self.choices = [i[topic] for i in countries]
        self.choices.insert(self.correct_order, country[topic])
        del countries, topic
    
    async def play(self, ctx) -> bool:
        """ like generate_question() but discord.py edition """
        
        if not hasattr(self, "question"):
            await self.generate_question()
        
        alphabet = list("ABCD")
        embed = ctx.bot.Embed(ctx, title="Geography Quiz!", desc=self.question + "\n" + "\n".join(
            [f"{alphabet[choice]}. **{self.choices[choice]}**" for choice in range(4)]
        ))
        message = await embed.send()
        del embed
        
        WaitFor = ctx.bot.WaitForMessage(ctx, check=(lambda x: x.channel == ctx.channel and x.author == ctx.author and len(x.content) == 1 and (x.content.upper() in alphabet)))
        _input = await WaitFor.get_message()
        del WaitFor
        
        if not message:
            await message.edit(embed=Embed(title=f'Quiz ended. No response from {ctx.author.display_name}.', color=Color.red()))
            return
        
        if alphabet.index(_input.content.upper()) == self.correct_order:
            await message.edit(embed=Embed(title=f'Congratulations! {ctx.author.display_name} is correct!', color=Color.green()))
            return True
        await message.edit(embed=Embed(title=f'Sorry, {ctx.author.display_name}! The answer is {alphabet[self.correct_order]}. {self.choices[self.correct_order]}', color=Color.red()))
        return False
    
    async def end(self, end_session: bool = False) -> None:
        """ Ends the quiz. """
        
        if end_session:
            await self.session.close()
        
        del (
            self.session,
            self.question,
            self.correct_order,
            self.choices,
            self._topics
        )

class RockPaperScissors:
    def __init__(self, ctx, timeout: int = 20):
        self.emojis = ['✊', '🖐️', '✌']
        self.ctx = ctx
        self.check = (lambda r, u: (str(r.emoji) in self.emojis) and (u == self.ctx.author))
        self.timeout = timeout

    async def play(self):
        self.message = await self.ctx.send(embed=Embed(title="Rock, paper, scissors!", color=self.ctx.guild.me.roles[::-1][0].color))
        for emoji in self.emojis:
            await self.message.add_reaction(emoji)
            await sleep(0.5) # 3 emojis may be not much but this is to reduce ratelimit
        
        try:
            r, _ = await self.ctx.bot.wait_for('reaction_add', timeout=self.timeout, check=self.check)
        except:
            return None
        
        return await self._is_win(self.emojis.index(str(r.emoji)), randint(0, 2))

    async def _is_win(self, user_index: int, bot_index: int):
        pos = (user_index, bot_index)
        if pos in [(0, 2), (1, 0), (2, 1)]:
            await self.message.edit(content="", embed=Embed(title=f"Congratulations, {self.ctx.author.display_name} won against {self.ctx.bot.user.name}!", description=f"**{self.ctx.author.display_name}: **{self.emojis[user_index]}\n**{self.ctx.bot.user.name}: **{self.emojis[bot_index]}", color=Color.green()))
            return 1
        elif pos in [(0, 0), (1, 1), (2, 2)]:
            await self.message.edit(content="", embed=Embed(title=f"It's a draw!", description=f"**{self.ctx.author.display_name}: **{self.emojis[user_index]}\n**{self.ctx.bot.user.name}: **{self.emojis[bot_index]}", color=Color.orange()))
            return 0
        await self.message.edit(content="", embed=Embed(title=f"RIP, {self.ctx.author.display_name} lost to {self.ctx.bot.user.name}!", description=f"**{self.ctx.author.display_name}: **{self.emojis[user_index]}\n**{self.ctx.bot.user.name}: **{self.emojis[bot_index]}", color=Color.red()))
        return -1

class TicTacToe:
    def __init__(self, player: str = "O", opponent: str = "X", default: str = "-"):
        self.board = [default] * 9 # build the board
        self.winning_moves = [[int(a) for a in list(i)] for i in "012,345,678,048,642".split(",")] # list of winning moves
        self.filled = [] # array of used indexes
        self.player, self.opponent, self.default = player, opponent, default # symbols
        self.is_on_range = (lambda x: int(x) in range(1,10)) # method to check if is on board range
        self.current_turn = player # set the current turn to the player

    def check_if_win(self):
        if len(self.filled) == len(self.board): return "?" # draw
        for x, y, z in self.winning_moves:
            if (self.board[x] == self.board[y] == self.board[z]) and (self.board[x] != self.default):
                return self.board[x] # this character wins
        return None # no one wins yet

    def add_move(self, order: int, opponent: bool):
        if (order in self.filled) or (not self.is_on_range(order)): return None # check if is number and is valid
        self.filled.append(order) # add to used array, so the column can't be used anymore
        self.board[order - 1] = self.opponent if opponent else self.player # change the display in board
        self.current_turn = self.player if opponent else self.opponent # change the current player
        return 1

    def show(self): # self-explanatory.
        string = ""
        for column in range(len(self.board)):
            if column % 3 == 0: string += "\n"
            string += self.board[column] + " "
        return string + "\n"