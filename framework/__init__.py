# This framework folder is the Discord Framework my bot use.
# You can use the code in this directory for your bot.
# I am not really planning on uploading it to PyPI though...

from discord.ext import commands as _commands
from datetime import datetime
from io import BytesIO
from gc import collect as _collect
from os import getenv
from json import dumps as _dumps
from functools import wraps as _wraps
from traceback import format_exc
from inspect import getmembers, getsource
from requests import post as _post_message # to send message without async since the on_close function is not coroutine
import asyncio
import discord as dpy
import signal as sg

from .oreo import Oreo
from .parser import Parser
from .panel import CustomPanel
from .colorthief import Smart_ColorThief
from .message import embed, Paginator, ChooseEmbed, WaitForMessage
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
    for name, value in getmembers(dpy.User):
        if name.startswith("__") or value.__class__.__name__ != "function" or "can only be used by non-bot accounts" not in getsource(value):
            continue
        delattr(dpy.User, name)
    delattr(dpy.Client, "fetch_user_profile")

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
            await asyncio.sleep(delete_after)
            return await self._state.http.delete_message(channel_id=self.channel.id, message_id=response["id"])
    
    async def _send_embed(self, *args, **kwargs):
        _builtin_embed = self.bot.Embed(self, *args, **kwargs)
        await _builtin_embed.send()
        del _builtin_embed
    
    def _parse_message_create(self, data):
        if (not hasattr(self, "_is_ready")) or data["type"] or (not data.get("guild_id")) or data.get("webhook_id"):
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
    
    def _event_on_close(self):
        if self._is_closed:
            return
    
        print("Closing bot...")
        _post_message(f"{dpy.http.Route.BASE}/channels/{self.util.status_channel}/messages", headers={ "Authorization": f"Bot {self.http.token}", "Content-Type": "application/json" }, data=_dumps({
            "embed": { "title": "Bot is down :(", "description": "The bot is down.", "color": 16711680, "fields": [
                {"name": "Commands run throughout run-time",
                "value": str(self.command_uses), "inline": True}, { "name": "Total Uptime",
                "value": self.util.strfsecond(datetime.now().timestamp() - self.util._start), "inline": True}
            ], "footer": { "text": "Please note that not all down-times are due to hosting problems. This could be a bug-fix or a development update." } }
        }))
        data = self.db.get("config", {"h": True})
        
        current_time = datetime.now()
        if len(data["down_times"]) > 20:
            data["down_times"].pop(0)
        data["down_times"].append(f'{current_time.strftime("%Y-%m-%dT%H:%M:%SZ")}|{self.util.strfsecond(current_time.timestamp() - self.util._start)}')
        self.db.modify("config", self.db.types.CHANGE, {"h": True}, {
            "commands_run": data["commands_run"] + self.command_uses,
            "down_times": data["down_times"],
            "online": False
        })
        self._is_closed = True
        del self.db
        del data, current_time
        self.loop.stop()
    
    def _store_user(self, data):
        user_id = int(data["id"])
        try:
            return self._users[user_id]
        except:
            user = dpy.User(state=self, data=data)
            if (data["discriminator"] != "0000") and (not data.get("bot")):
                self._users[user_id] = user
            return user
    
    def _store_emoji(self, guild, data):
        # stores as a tuple, not an emoji object to save memory
        # (emoji_name, emoji_id, is_animated, created_at, has_guild, ?guild)
        guild_data = (guild,) if guild else ()
        self._emojis[int(data["id"])] = (data["name"], int(data["id"]), data.get("animated", False), dpy.utils.snowflake_time(int(data["id"])), bool(guild), *guild_data)
        return f"<{'a' if data.get('animated') else ''}:{data['name']}:{data['id']}>"
    
    def _run_bot(self, *args, **kwargs):
        loop = self.loop
        try:
            loop.add_signal_handler(sg.SIGINT,  self.event_on_close)
            loop.add_signal_handler(sg.SIGTERM, self.event_on_close)
        except:
            pass

        async def runner():
            try:
                await self.start(*args, **kwargs)
            finally:
                if not self.is_closed():
                    await self.close()
                self.event_on_close()

        def stop_loop_on_completion(f):
            loop.stop()

        future = asyncio.ensure_future(runner(), loop=loop)
        future.add_done_callback(stop_loop_on_completion)
        try:
            loop.run_forever()
        finally:
            future.remove_done_callback(stop_loop_on_completion)
            self.event_on_close()
        try:
            try:
                task_retriever = asyncio.Task.all_tasks
            except:
                task_retriever = asyncio.all_tasks
            tasks = {t for t in task_retriever(loop=loop) if not t.done()}
            if not tasks:
                return
            for task in tasks:
                task.cancel()
            loop.run_until_complete(asyncio.gather(*tasks, return_exceptions=True))
            for task in tasks:
                if task.cancelled():
                    continue
                if task.exception() is not None:
                    loop.call_exception_handler({
                        'message': 'Unhandled exception during Client.run shutdown.',
                        'exception': task.exception(),
                        'task': task
                    })
            loop.run_until_complete(loop.shutdown_asyncgens())
            loop.run_until_complete(self.http._HTTPClient__session.close())
        finally:
            loop.close()

        if not future.cancelled():
            try:
                return future.result()
            except KeyboardInterrupt:
                return
    
    setattr(dpy.Client, "run", _run_bot)
    setattr(dpy.Client, "event_on_close", _event_on_close)
    setattr(_commands.bot.BotBase, "run_command", _run_command)
    setattr(_commands.Context, "error_message", error_message)
    setattr(_commands.Context, "embed", _send_embed)
    setattr(_commands.Context, "send_image", _send_image)
    setattr(_commands.Context, "success_embed", _success_embed)
    setattr(dpy.state.ConnectionState, "parse_message_create", _parse_message_create)
    setattr(dpy.state.ConnectionState, "store_emoji", _store_emoji)
    setattr(dpy.state.ConnectionState, "store_user", _store_user)
    setattr(dpy.Embed, "add_useless_stuff", _embed_add_useless_stuff)

    del _parse_message_create, _send_image, _success_embed, _send_embed, _embed_add_useless_stuff, _run_command, _store_emoji, _run_bot, _event_on_close, _store_user

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
