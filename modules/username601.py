from discord import Color, Embed
from discord.message import Message
from configparser import ConfigParser
class send_error_message(Exception): pass

main_cfg = ConfigParser()
main_cfg.read('config.ini')

async def wait_for_message(ctx, message, func=None, timeout=5.0, *args, **kwargs):
    if message is not None: await ctx.send(message)
    def wait_check(m): return ((m.author == ctx.author) and (m.channel == ctx.channel))
    _function = wait_check if (func is None) else func
    try:
        message = await ctx.bot.wait_for("message", check=_function, timeout=timeout)
    except:
        message = None
    finally:
        return message

def parse_parameter(args, arg, get_second_element=False, singular=False):
    if arg.lower() in list(map(lambda x: x.lower(), args)):
        parsed = tuple([i for i in list(args) if arg.lower() not in i.lower()])
        if get_second_element:
            index = [i.lower() for i in list(args)].index(arg.lower()) + 1
            if index >= len(args):
                return {"available": False, "parsedarg": args, "secondparam": None}
            parsed = parsed[0:index]
            if not singular: return {"available": True, "parsedarg": parsed, "secondparam": ' '.join(args[index:])}
            return {"available": True, "parsedarg": parsed, "secondparam": list(args)[index]}
        return {"available": True, "parsedarg": parsed, "secondparam": None}
    return {"available": False, "parsedarg": args, "secondparam": None}