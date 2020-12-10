# This framework folder is the Discord Framework my bot use.
# You can use the code in this directory for your bot.
# I am not really planning on uploading it to PyPI though...

from .oreo import Oreo
from .parser import Parser
from .panel import CustomPanel
from .cache import CacheManager
from .colorthief import Smart_ColorThief
from .message import embed, Paginator, ChooseEmbed,  WaitForMessage
from .util import Util, GetRequestFailedException, BasicCommandException
from .games import TicTacToe, RockPaperScissors, GeographyQuiz, MathQuiz, GuessAvatar, Trivia, GuessMyNumber

def initiate(client):
    setattr(client, "oreo", Oreo)
    setattr(client, "Embed", embed)
    setattr(client, "Parser", Parser)
    setattr(client, "Trivia", Trivia)
    setattr(client, "Panel", CustomPanel)
    setattr(client, "MathQuiz", MathQuiz)
    setattr(client, "TicTacToe", TicTacToe)
    setattr(client, "rps", RockPaperScissors)
    setattr(client, "GeoQuiz", GeographyQuiz)
    setattr(client, "GuessAvatar", GuessAvatar)
    setattr(client, "ChooseEmbed", ChooseEmbed)
    setattr(client, "EmbedPaginator", Paginator)
    setattr(client, "cache_manager", CacheManager)
    setattr(cleint, "GuessMyNumber", GuessMyNumber)
    setattr(client, "ColorThief", Smart_ColorThief)
    setattr(client, "WaitForMessage", WaitForMessage)
    Util(client)