# This framework folder is the Discord Framework my bot use.
# You can use the code in this directory for your bot.
# I am not really planning on uploading it to PyPI though...

from .message import embed, Paginator, ChooseEmbed
from .parser import Parser
from .panel import CustomPanel
from .colorthief import Smart_ColorThief
from .games import TicTacToe, Quiz
from .emote import emoji_to_url

def initiate(client):
    setattr(client, "Embed", embed)
    setattr(client, "Parser", Parser)
    setattr(client, "Panel", CustomPanel)
    setattr(client, "ColorThief", Smart_ColorThief)
    setattr(client, "EmbedPaginator", Paginator)
    setattr(client, "TicTacToe", TicTacToe)
    setattr(client, "Quiz", Quiz)
    setattr(client, "twemoji", emoji_to_url)
    setattr(client, "ChooseEmbed", ChooseEmbed)