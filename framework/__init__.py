# This framework folder is the Discord Framework my bot use.
# You can use the code in this directory for your bot.
# I am not really planning on uploading it to PyPI though...

import discord as dpy
from discord.ext import commands as _commands
from datetime import datetime
from io import BytesIO
from gc import collect as _collect
from os import getenv
from functools import wraps as _wraps
from traceback import format_exc
import asyncio

from .oreo import Oreo
from .parser import Parser
from .panel import CustomPanel
from .colorthief import Smart_ColorThief
from .message import embed, Paginator, ChooseEmbed,  WaitForMessage
from .util import Util, error_message
from .games import GuessTheFlag, Slot, TicTacToe, RockPaperScissors, GeographyQuiz, MathQuiz, GuessAvatar, Trivia, GuessMyNumber, Hangman
from .canvas import ServerCard, UserCard, ProfileCard, GDLevel, Blur, ImageClient
from .database import Database
from .lego import legofy

def _hooked_wrapped_callback(command, ctx, coro):
    @_wraps(coro)
    async def wrapped(*args, **kwargs):
        try:
            ret = await coro(*args, **kwargs)
        except asyncio.CancelledError:
            ctx.command_failed = True
            return
        except Exception as exc:
            ctx.command_failed = True
            raise _commands.CommandInvokeError(exc) from exc
        finally:
            if command._max_concurrency:
                await command._max_concurrency.release(ctx)

            await command.call_after_hooks(ctx)
        return ret
    return wrapped
    
def get_prefix(config_file: str = "config.ini"):
    from configparser import ConfigParser # i don't recommend calling this function more than once
    _config = ConfigParser()
    _config.read(config_file)
    return _config["bot"].get("prefix", "1")

def modify_discord_py_functions():
    def _embed_add_useless_stuff(self, ctx, disable_color: bool = False):
        self._footer = {
            "text": "Command executed by "+str(ctx.author),
            "icon_url": str(ctx.author.avatar_url)
        }
        self.timestamp = datetime.now()
        
        if not disable_color:
            self.colour = ctx.me.colour
        return self
    
    async def _send_image(self, url, alexflipnote: bool = False, content: str = None, file_format="png"):
        try:
            if isinstance(url, BytesIO):
                return await self.bot.http.send_files(self.channel.id, content=content, files=[dpy.File(url, f"file.{file_format}")])
        
            session = self.bot.util.alex_client if alexflipnote else self.bot.http._HTTPClient__session
            
            async with session.get(url) as data:
                _bytes = await data.read()
                assert data.status < 400, "API returns a bad status code"
                assert data.headers['Content-Type'].startswith("image/"), "Content does not have an image."
                extension = "." + data.headers['Content-Type'][6:].lower()
                buffer = self.bot.util._crop_out_memegen(self, _bytes) if url.startswith("https://api.memegen.link/") else BytesIO(_bytes)
                await self.bot.http.send_files(self.channel.id, content=content, files=[dpy.File(buffer, f"file{extension}")])
                del extension, _bytes, data, buffer
                _collect()
        except Exception as e:
            raise self.error_message(f"Image not found.\n`{str(e)}`")
    
    async def _success_embed(self, message=None, description=None, delete_after=None):
        response = await self._state.http.send_message(self.channel.id, content="", embed={
            "title": message,
            "description": description,
            "color": 3066993
        })
        
        if delete_after:
            await dpy.Message(state=self._state, channel=self.channel, data=response).delete(delay=delete_after)
    
    async def _send_embed(self, *args, **kwargs):
        _builtin_embed = self.bot.Embed(self, *args, **kwargs)
        await _builtin_embed.send()
        del _builtin_embed
    
    def _parse_message_create(self, data):
        if data.get("message_reference") or (not data.get("guild_id")) or data.get("webhook_id"):
            return
        channel, _ = self._get_guild_channel(data)
        if not data["author"].get("bot"):
            self.dispatch('message', dpy.Message(channel=channel, data=data, state=self))
        elif data["author"]["id"] == str(self.user.id):
            self._messages.append(dpy.Message(channel=channel, data=data, state=self))
        del channel, data
    
    async def _run_command(self, message):
        if not message.content.startswith(self.command_prefix):
            return
        
        ctx = _commands.Context(prefix=self.command_prefix, view=_commands.view.StringView(message.content), bot=self, message=message, args=message.content.split(" ")[1:])
        if not ctx.channel.permissions_for(ctx.me).send_messages:
            return # what's the point of running a command if the bot doesn't have the perms to send messages kekw
        
        try:
            command_name = message.content[len(self.command_prefix):].split()[0]
            ctx.command = self.all_commands[command_name.lower()]
            if not await ctx.command.can_run(ctx):
                return
            
            if ctx.command._max_concurrency:
                await ctx.command._max_concurrency.acquire(ctx)
            
            try:
                ctx.command._prepare_cooldowns(ctx)
                await ctx.command._parse_arguments(ctx)
                if len(ctx.args) > 2:
                    ctx.args.pop(2)
            except:
                if ctx.command._max_concurrency:
                    await ctx.command._max_concurrency.release(ctx)
                raise
            
            await _hooked_wrapped_callback(ctx.command, ctx, ctx.command.callback)(*ctx.args, **ctx.kwargs)
        except (KeyError, IndexError):
            return
        except Exception as exc:
            self.dispatch("command_error", ctx, exc, format_exc())
        else:
            self.command_uses += 1
        del ctx, command_name
    
    setattr(_commands.bot.BotBase, "run_command", _run_command)
    setattr(_commands.Context, "error_message", error_message)
    setattr(_commands.Context, "embed", _send_embed)
    setattr(_commands.Context, "send_image", _send_image)
    setattr(_commands.Context, "success_embed", _success_embed)
    setattr(dpy.state.ConnectionState, "parse_message_create", _parse_message_create)
    setattr(dpy.Embed, "add_useless_stuff", _embed_add_useless_stuff)
    
    del _parse_message_create, _send_image, _success_embed, _send_embed, _embed_add_useless_stuff, _run_command

def initiate(client, db_name: str = "username601"): # no stop calling me yanderedev 2.0
    client.slot = Slot
    client.oreo = Oreo
    client.Blur = Blur
    client.lego = legofy
    client.Embed = embed
    client.Parser = Parser
    client.Trivia = Trivia
    client.GDLevel = GDLevel
    client.Hangman = Hangman
    client.Panel = CustomPanel
    client.MathQuiz = MathQuiz
    client.UserCard = UserCard
    client.TicTacToe = TicTacToe
    client.ServerCard = ServerCard
    client.rps = RockPaperScissors
    client.GeoQuiz = GeographyQuiz
    client.ProfileCard = ProfileCard
    client.GuessAvatar = GuessAvatar
    client.ChooseEmbed = ChooseEmbed
    client.EmbedPaginator = Paginator
    client.Image = ImageClient(client)
    client.GuessTheFlag = GuessTheFlag
    client.GuessMyNumber = GuessMyNumber
    client.ColorThief = Smart_ColorThief
    client.WaitForMessage = WaitForMessage
    client.db = Database(getenv("DB_LINK"), db_name)
    Util(client)