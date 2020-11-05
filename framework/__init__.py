# This framework folder is the Discord Framework my bot use.
# You can use the code in this directory for your bot.
# I am not really planning on uploading it to PyPI though...

from .embed import embed
from .parser import Parser

def initiate(client):
    setattr(client, "Embed", embed)
    setattr(client, "Parser", Parser)