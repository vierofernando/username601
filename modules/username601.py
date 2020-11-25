from configparser import ConfigParser

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

def lapsed_time_from_seconds(sec):
    time_type, newsec = 'seconds', int(sec)
    # YANDEREDEV.EXE
    if sec>60:
        newsec, time_type = round(sec/60), 'minutes'
        if sec>3600: 
            newsec, time_type = round(sec/3600), 'hours'
            if sec>86400:
                newsec, time_type = round(sec/86400), 'days'
                if sec>2592000:
                    newsec, time_type = round(sec/2592000), 'months'
                    if sec>31536000:
                        newsec, time_type = round(sec/31536000), 'years'
    if str(newsec) == '1': return str(str(newsec)+' '+time_type[:-1])
    return str(str(newsec)+' '+time_type)