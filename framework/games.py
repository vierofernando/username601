from aiohttp import ClientSession
from random import choice, randint
from discord import Embed, Color
from random import randint, choice
from asyncio import sleep

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

class Quiz:
    def __init__(self, players: list, topic: str = "Education", limit: int = 10, _async: bool = True):
        
        if not _async:
            try:
                from requests import get
                self.questions = get(f"https://wiki-quiz.herokuapp.com/v1/quiz?topics={topic}&limit={limit}").json()["quiz"]
            except:
                raise NameError(f"Topic {topic} not found")
        else:
            self.questions = None
        
        self.quiz_length = limit
        self.leaderboard = {}
        self.asked_questions = []
        self.current_question = None
        self.question_index = -1
        self.is_async = _async
        self.session = ClientSession() if self.is_async else None
        self.topic = topic

        for player in players:
            self.leaderboard[player] = 0

    async def initiate(self):
        if self.questions is not None or (not self.is_async): return
        result = await self.session.get(f"https://wiki-quiz.herokuapp.com/v1/quiz?topics={self.topic}&limit={self.quiz_length}")
        self.questions = await result.json()

    def generate_question(self):
        if not self.questions:
            raise AttributeError("Please do `await <object>.initiate()` since this game is async.")
    
        if self.is_ended(): return
        _question_number = randint(0, self.quiz_length - len(self.asked_questions) - 1)
        self.current_question = self.questions[_question_number]
        self.asked_questions.append(self.current_question)
        self.questions.remove(self.current_question)
        self.question_index += 1
        return self.current_question
    
    def submit(self, answers: dict):
        _members = self
        for student in answers.keys():
            if answers[student] == self.current_question["answer"]:
                self.leaderboard[student] += 1
        return self.is_ended()

    def is_ended(self):
        return (len(self.questions) == 0)

    async def close(self):
        temp = self.leaderboard.copy()
        
        if self._async:
            await self.session.close()
        
        del (
            self.leaderboard,
            self.questions,
            self._async,
            self.current_question,
            self.asked_questions,
            self.question_index,
            self.session
        )
        
        return temp

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