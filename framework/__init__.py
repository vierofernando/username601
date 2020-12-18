# This framework folder is the Discord Framework my bot use.
# You can use the code in this directory for your bot.
# I am not really planning on uploading it to PyPI though...

from os import getenv
from .oreo import Oreo
from .parser import Parser
from .panel import CustomPanel
from .colorthief import Smart_ColorThief
from .message import embed, Paginator, ChooseEmbed,  WaitForMessage
from .util import Util, GetRequestFailedException, BasicCommandException
from .games import Slot, TicTacToe, RockPaperScissors, GeographyQuiz, MathQuiz, GuessAvatar, Trivia, GuessMyNumber, Hangman
from .canvas import ServerCard, UserCard, ProfileCard
from .database import Database

def initiate(client, db_name: str = "username601"):
    setattr(client, "slot", Slot)
    setattr(client, "oreo", Oreo)
    setattr(client, "Embed", embed)
    setattr(client, "Parser", Parser)
    setattr(client, "Trivia", Trivia)
    setattr(client, "Hangman", Hangman)
    setattr(client, "Panel", CustomPanel)
    setattr(client, "MathQuiz", MathQuiz)
    setattr(client, "UserCard", UserCard)
    setattr(client, "TicTacToe", TicTacToe)
    setattr(client, "ServerCard", ServerCard)
    setattr(client, "rps", RockPaperScissors)
    setattr(client, "GeoQuiz", GeographyQuiz)
    setattr(client, "ProfileCard", ProfileCard)
    setattr(client, "GuessAvatar", GuessAvatar)
    setattr(client, "ChooseEmbed", ChooseEmbed)
    setattr(client, "EmbedPaginator", Paginator)
    setattr(client, "GuessMyNumber", GuessMyNumber)
    setattr(client, "ColorThief", Smart_ColorThief)
    setattr(client, "WaitForMessage", WaitForMessage)
    setattr(client, "db", Database(getenv("DB_LINK"), db_name))
    Util(client)