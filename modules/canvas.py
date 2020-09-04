from PIL import Image, ImageFont, ImageDraw, GifImagePlugin, ImageOps, ImageFilter
from io import BytesIO
from datetime import datetime as t
import username601 as myself
from requests import get
import json
import random
from username601 import *
from colorthief import ColorThief

def getFont(fontpath, fontname, size, otf=False):
    ext = 'ttf' if not otf else 'otf'
    return ImageFont.truetype(f'{fontpath}/{fontname}.{ext}', size)
def getImage(assetpath, imageName): return Image.open(f'{assetpath}/{imageName}')
def imagefromURL(url, *args, **kwargs): return Image.open(BytesIO(get(url).content))
def bufferGIF(images, duration, optimize=False):
    arr = BytesIO()
    images[0].save(arr, "GIF", save_all=True, append_images=images[1:], optimize=optimize, duration=duration, loop=0)
    arr.seek(0)
    return arr
def buffer(data):
    arr = BytesIO()
    data.save(arr, format='PNG')
    arr.seek(0)
    return arr
def drawtext(draw, thefont, text, x, y, col):
    draw.text((x, y), text, fill =col, font=thefont, align ="left")
def drawProgressBar(draw, percent):
    data = round(percent/100*485)
    if data<2: return
    draw.rectangle(((15, 459), (data, 469)), fill=(0, 255, 0))
def getSongString(thetime, now):
    i = round((now - thetime).total_seconds())
    minute = '0' if (i%60==0) else str(int(i/60))
    if i > 60:
        while i > 60:
            i -= 60
    if len(minute)==1: minute = '0'+minute
    return minute+':'+str(i)
def brightness_text(tupl):
    if (sum(tupl)/3) < 127.5: return (255, 255, 255)
    return (0, 0, 0)
def add_corners(im, rad, top_only=False, bottom_only=False):
    circle = Image.new('L', (rad * 2, rad * 2), 0)
    draw = ImageDraw.Draw(circle)
    draw.ellipse((0, 0, rad * 2, rad * 2), fill=255)
    alpha = Image.new('L', im.size, 255)
    w, h = im.size
    alpha.paste(circle.crop((0, 0, rad, rad)), (0, 0))
    alpha.paste(circle.crop((0, rad, rad, rad * 2)), (0, h-rad))
    alpha.paste(circle.crop((rad, 0, rad * 2, rad)), (w-rad, 0))
    alpha.paste(circle.crop((rad, rad, rad * 2, rad * 2)), (w-rad, h-rad))
    im.putalpha(alpha)
def get_accent(thief, image):
    data = BytesIO(get(image).content)
    return thief(data).get_color()
def draw_status_stats(draw, obj, rect_y_cursor, font, margin_left, margin_right, bg_arr):
    x_pos, colors = margin_left, [(63, 232, 0), (244, 208, 63), (225, 0, 0), (124, 0, 211), (127, 127, 127)]
    total = sum([obj[i] for i in list(obj.keys())])
    draw.rectangle([
        (margin_left, rect_y_cursor), (margin_right, rect_y_cursor + 25)
    ], fill=bg_arr[1])
    draw.text((margin_left + 3, rect_y_cursor + 2), "Member status graph:", fill=brightness_text(bg_arr[1]), font=font)
    rect_y_cursor += 25
    draw.rectangle([
        (margin_left, rect_y_cursor), (margin_right, rect_y_cursor + 50)
    ], fill=(50, 50, 50))
    for i in range(len(list(obj.keys()))):
        percentage = round(obj[list(obj.keys())[i]]/total*(margin_right - margin_left))
        draw.rectangle([
            (x_pos, rect_y_cursor), (x_pos + percentage, rect_y_cursor + 50)
        ], fill=colors[i])
        x_pos += percentage
    rect_y_cursor += 70
    return rect_y_cursor
def get_multiple_color_accents(thief, image):
    b = BytesIO(get(image).content)
    thief = thief(b).get_palette(color_count=10)
    return [{
        'r': i[0], 'g': i[1], 'b': i[2]
    } for i in thief]
def process(text, font, width):
    res, temp = [], []
    for i in text.split():
        data = font.getsize(' '.join(temp))[0]
        if data < width:
            temp.append(i)
            continue
        res.append(' '.join(temp))
        temp = []
    if res==[]: res = [text]
    return '\n'.join(res)
def char_process(text, width, font, array=False):
    res = []
    temp = ""
    for i in list(text):
        temp += i
        if font.getsize(temp)[0] < width:
            continue
        res.append(temp)
        temp = ""
    if len(''.join(res)) != len(text):
        res.append(temp)
    if res ==[]:
        if array: return [''.join(temp)]
        return ''.join(temp)
    if array: return res
    return '\n'.join(res)
def toLocaleString(a): # sike javascriptors ;)
    res = ''
    num = 0
    for i in list(a)[::-1]:
        res += i
        if num > 1:
            num = -1
            res += ','
        num += 1
    if res[::-1].startswith(','): res = res[:-1]
    return res[::-1]

class Painter:

    def __init__(self, assetpath, fontpath): # lmao wtf is this
        self.getFont = getFont
        self.getImage = getImage
        self.imagefromURL = imagefromURL
        self.assetpath = assetpath
        self.fontpath = fontpath
        self.buffer = buffer
        self.drawProgressBar = drawProgressBar
        self.getSongString = getSongString
        self.get_color_accent = get_accent
        self.drawtext = drawtext
        self.draw_status_stats = draw_status_stats
        self.thief = ColorThief
        self.process_text = process
        self.add_corners = add_corners
        self.char_process = char_process
        self.toLocaleString = toLocaleString
        self.flags = json.loads(open(cfg('JSON_DIR')+'/flags.json', 'r').read())
        self.region = json.loads(open(cfg('JSON_DIR')+'/regions.json', 'r').read())
        self.get_multiple_color_accents = get_multiple_color_accents
        self.gd_assets = json.loads(open(cfg('JSON_DIR')+'/gd.json', 'r').read())
        self.invert = brightness_text # lmao
    
    def get_accent(self, image): return self.get_color_accent(self.thief, image)
    def get_multiple_accents(self, image): return self.get_multiple_color_accents(self.thief, image)

    def password(self, bad_pass, good_pass):
        im = self.getImage(self.assetpath, 'pass.png')
        font = self.getFont(self.fontpath, 'Helvetica', 25)
        draw = ImageDraw.Draw(im)
        draw.text((42, 80), self.char_process(bad_pass, 396, font, array=True)[0], font=font, fill='black')
        draw.text((42, 311), self.char_process(good_pass, 396, font, array=True)[0], font=font, fill='black')
        return self.buffer(im)

    def geometry_dash_level(self, levelid, daily=False, weekly=False):
        # a shit ton of declarations first xd
        if daily: query = 'daily'
        elif weekly: query = 'weekly'
        else: query = str(levelid)
        data = get('https://gdbrowser.com/api/level/'+query).json()
        pusab_big = self.getFont(self.fontpath, 'PUSAB__', 40, otf=True)
        pusab_smol = self.getFont(self.fontpath, 'PUSAB__', 30, otf=True)
        pusab_smoler = self.getFont(self.fontpath, 'PUSAB__', 20, otf=True)
        pusab_tiny = self.getFont(self.fontpath, 'PUSAB__', 20, otf=True)
        aller = self.getFont(self.fontpath, 'Aller', 20)
        levelName = data['name']
        levelAuth = "by "+data['author']
        levelDesc = data['description']
        levelDiff = data['difficulty']
        levelStars = str(data['stars'])+" stars"
        main = Image.new('RGB', color=(4,75,196), size=(500, 400))
        draw = ImageDraw.Draw(main)

        w, h = pusab_big.getsize(levelName)
        W, H = main.size
        draw.text(((W-w)/2,15), levelName, font=pusab_big, stroke_width=2, stroke_fill="black", fill="white")
        w, h = pusab_smol.getsize(levelAuth)
        draw.text(((W-w)/2,50), levelAuth, font=pusab_smol, stroke_width=2, stroke_fill="black", fill=(255, 200, 0))
        width, desc_cursor = (w, h), 300
        texts, sym_cursor = char_process(levelDesc, 445, aller, array=True), 100

        for i in texts:
            w, h = aller.getsize(i)
            draw.text(((W-w)/2, desc_cursor), i, font=aller, fill='white')
            desc_cursor += 25
        del desc_cursor, width, texts

        difficulty = self.imagefromURL("https://gdbrowser.com/difficulty/"+data['difficultyFace']+".png").convert('RGBA').resize((75, 75))
        main.paste(difficulty, (round((W - 75)/2) - 100, 100), difficulty)
        w, h = pusab_tiny.getsize(levelDiff)
        draw.text(((W - w)/2 - 100, 180), levelDiff, font=pusab_tiny, stroke_width=2, stroke_fill="black")
        w, h = pusab_tiny.getsize(levelStars)
        draw.text(((W - w)/2 - 100, 200), levelStars, font=pusab_tiny, stroke_width=2, stroke_fill="black")

        for i in list(self.gd_assets['main'].keys()):
            if self.gd_assets['main'][i]==None:
                if data['disliked']: sym = self.imagefromURL(self.gd_assets['dislike']).convert('RGBA').resize((25, 25))
                else: sym = self.imagefromURL(self.gd_assets['like']).convert('RGBA').resize((25, 25))
                main.paste(sym, (round((W-25)/2) + 75, sym_cursor), sym)
                draw.text((round((W-25)/2)+105, sym_cursor+5), data['likes'], font=pusab_smoler, stroke_width=2, stroke_fill="black")
                sym_cursor += 30
                continue
            if i not in list(data.keys()): continue
            sym = imagefromURL(self.gd_assets['main'][i]).convert('RGBA').resize((25, 25))
            main.paste(sym, (round((W-25)/2) + 75, sym_cursor), sym)
            draw.text((round((W-25)/2)+105, sym_cursor+5), str(data[i]), font=pusab_smoler, stroke_width=2, stroke_fill="black")
            sym_cursor += 30
        
        self.add_corners(main, 20)
        return self.buffer(main)

    def invert_image(self, im):
        ava = self.imagefromURL(im).convert('RGB')
        im_invert = ImageOps.invert(ava)
        return self.buffer(im_invert)
    
    def grayscale(self, im):
        res = self.imagefromURL(im).convert('L')
        return self.buffer(res)

    def country(self, query):
        bigfont = self.getFont(self.fontpath, 'NotoSansDisplay-Bold', 35, otf=True)
        smolfont = self.getFont(self.fontpath, 'NotoSansDisplay-Bold', 25, otf=True)
        smolerfont = self.getFont(self.fontpath, 'NotoSansDisplay-Bold', 20, otf=True)
        data = get('https://restcountries.eu/rest/v2/name/'+query).json()[0]
        length = bigfont.getsize(data['name'])[0] + 200
        flagid, flagnotfound = data['alpha2Code'].lower(), False
        try: cf = [(
            i['r'], i['g'], i['b']
        ) for i in self.get_multiple_accents("https://www.worldometers.info/img/flags/"+flagid+"-flag.gif")]
        except: flagnotfound = True
        size = (length, 400)
        if flagnotfound:
            cf = [(0,0,0) for i in range(5)]
        main = Image.new('RGB', color=(0,0,0), size=size)
        draw = ImageDraw.Draw(main)
        margin_right, margin_left = main.width, 0
        draw.rectangle([
            (margin_left, 0), (margin_right, 50) # nice.
        ], fill=cf[0])
        draw.text((margin_left+5, 0), data['name'], font=bigfont, fill=self.invert(cf[0]))
        draw.rectangle([
            (margin_left, 50), (margin_right, 81)
        ], fill=cf[1])
        draw.text((margin_left+5, 45), data['nativeName'], font=smolfont, fill=self.invert(cf[1]))
        draw.rectangle([
            (margin_left, 81), (main.width, 400)
        ], fill=cf[2])
        capital = '<not avaliable>' if data['capital']=='' else data['capital']
        draw.text((margin_left+5, 78), self.char_process('Capital: '+capital, main.width+90, smolfont), font=smolerfont, fill=self.invert(cf[2]))
        draw.text((margin_left+5, 103), self.char_process('Region: '+data['region'], main.width+90, smolfont), font=smolerfont, fill=self.invert(cf[2]))
        draw.text((margin_left+5, 128), self.char_process('Subregion: '+data['subregion'], main.width+90, smolfont), font=smolerfont, fill=self.invert(cf[2]))
        draw.text((margin_left+5, 153), self.char_process('Population: '+self.toLocaleString(str(data['population'])), main.width+90, smolfont), font=smolerfont, fill=self.invert(cf[2]))
        draw.text((margin_left+5, 178), self.char_process('Area: '+self.toLocaleString(str(round(data['area'])))+' km', main.width+90, smolfont), font=smolerfont, fill=self.invert(cf[2]))
        draw.text((margin_left+5, 203), self.char_process('Timezones: '+', '.join(data['timezones']), main.width+90, smolfont), font=smolerfont, fill=self.invert(cf[2]))
        return {
            'buffer': self.buffer(main),
            'color': cf[0],
            'image': "https://google.com/" if flagnotfound else "https://www.worldometers.info/img/flags/"+flagid+"-flag.gif"
        }

    def server(self, guild):
        bigfont = self.getFont(self.fontpath, 'NotoSansDisplay-Bold', 50, otf=True)
        medium = self.getFont(self.fontpath, 'NotoSansDisplay-Bold', 20, otf=True)
        smolerfont = self.getFont(self.fontpath, 'NotoSansDisplay-Bold', 15, otf=True)
        server_title, members = guild.name, guild.members
        title_width = bigfont.getsize(server_title)[0]
        ava = self.imagefromURL(guild.icon_url).resize((100, 100))
        bg_arr = [(i['r'], i['g'], i['b']) for i in self.get_multiple_accents(guild.icon_url)]
        desc_width = medium.getsize('Created {} ago by {}'.format(myself.time_encode(t.now().timestamp() - guild.created_at.timestamp()), str(guild.owner)))[0]
        if desc_width > title_width: title_width = desc_width # :^)
        main_bg = bg_arr[0]
        margin_left, margin_right, rect_y_cursor = 25, title_width+225, 150
        main = Image.new(mode='RGB', color=main_bg, size=(title_width+250, 480))
        draw, a_third_width = ImageDraw.Draw(main), round((margin_right - margin_left)/3)
        main.paste(ava, (25, 25))
        draw.text((135, 20), server_title, fill=self.invert(main_bg), font=bigfont)
        draw.text((135, 90), 'Created {} ago by {}'.format(myself.time_encode(t.now().timestamp() - guild.created_at.timestamp()), str(guild.owner)), fill=self.invert(main_bg), font=medium)
        online, total = 200, 1000
        green_width = round(online/total*margin_right)
        rect_y_cursor = self.draw_status_stats(draw, {
            "online": len([i for i in members if i.status.value.lower()=='online']),
            "idle": len([i for i in members if i.status.value.lower()=='idle']),
            "do not disturb": len([i for i in members if i.status.value.lower()=='dnd']),
            "streaming": len([i for i in members if i.status.value.lower()=='streaming']),
            "offline": len([i for i in members if i.status.value.lower()=='offline'])
        }, rect_y_cursor, smolerfont, margin_left, margin_right, bg_arr)
        draw.rectangle([
            (margin_left, rect_y_cursor), (main.width/2, rect_y_cursor + 120)
        ], fill=bg_arr[2])
        draw.rectangle([
            (main.width/2, rect_y_cursor), (margin_right, rect_y_cursor + 120)
        ], fill=bg_arr[3])
        afkname = "???" if guild.afk_channel==None else guild.afk_channel.name
        main.paste(
            self.imagefromURL(self.region[str(guild.region)]).resize((35, 23)),
            (margin_right - 45, round(rect_y_cursor + 25 + (18 * 3)))
        )
        draw.text((margin_left + 5, rect_y_cursor + 5), "Channels: {}\nRoles: {}\nLevel {}\n{} boosters".format(
            len(guild.channels), len(guild.roles), guild.premium_tier, guild.premium_subscription_count
        ), fill=self.invert(bg_arr[2]), font=medium)
        draw.text(((main.width/2) + 5, rect_y_cursor + 5), "Region: {}\nAFK: {}\nAFK time: {}".format(
            str(guild.region).replace('-', ''), afkname, myself.time_encode(guild.afk_timeout).replace('minute', 'min')
        ), fill=self.invert(bg_arr[3]), font=medium)
        rect_y_cursor += 120
        draw.rectangle([
            (margin_left, rect_y_cursor), (margin_right, rect_y_cursor + 90)
        ], fill=bg_arr[4])
        draw.text((margin_left + 5, rect_y_cursor + 5), "{} Humans\n{} Bots\n{} Members in total".format(
            len([i for i in members if not i.bot]), len([i for i in members if i.bot]), len(members)
        ), fill=self.invert(bg_arr[4]), font=medium)
        self.add_corners(main, 25)
        return self.buffer(main)

    def usercard(self, roles, user, ava, bg, nitro):
        name, flags, flag_x = user.name, [], 170
        bigfont = self.getFont(self.fontpath, 'NotoSansDisplay-Bold', 50, otf=True)
        mediumfont = self.getFont(self.fontpath, 'NotoSansDisplay-Bold', 25, otf=True)
        if nitro: flags.append(self.flags['nitro'])
        for i in list(self.flags['badges'].keys()):
            if getattr(user.public_flags, i): flags.append(self.flags['badges'][i])
        foreground_col = self.invert(bg)
        avatar = self.imagefromURL(ava).resize((100, 100))
        self.add_corners(avatar, round(avatar.width/2))
        details_text = 'Created account {}\nJoined server {}'.format(myself.time_encode(t.now().timestamp()-user.created_at.timestamp())+' ago', myself.time_encode(t.now().timestamp()-user.joined_at.timestamp())+' ago')
        rect_y_pos = 180 + ((bigfont.getsize(details_text)[1]+20))
        canvas_height = rect_y_pos + len(roles * 50) + 30
        if bigfont.getsize(name)[0] > 600: main = Image.new(mode='RGB', color=bg, size=(bigfont.getsize(name)[0]+200, canvas_height))
        else: main = Image.new(mode='RGB', color=bg, size=(600, canvas_height))
        draw = ImageDraw.Draw(main)
        margin_right, margin_left = main.width - 40, 40
        draw.text((170, 20), name, fill=foreground_col, font=bigfont)
        draw.text((170, 80), f'ID: {user.id}', fill=foreground_col, font=mediumfont)
        for i in flags:
            temp_im = self.imagefromURL(i).resize((25, 25))
            main.paste(temp_im, (flag_x, 115), temp_im)
            flag_x += 30
        draw.text((40, 150), details_text, fill=foreground_col, font=mediumfont)
        for i in roles:
            draw.rectangle([
                (margin_left, rect_y_pos), (margin_right, rect_y_pos+50)
            ], fill=i['color'])
            draw.text((margin_left+10, rect_y_pos+10), i['name'], fill=self.invert(i['color']), font=mediumfont)
            rect_y_pos += 50
        try: main.paste(avatar, (40, 30), avatar)
        except: main.paste(avatar, (40, 30))
        self.add_corners(main, 25)
        return self.buffer(main)

    def get_palette(self, temp_data):
        font = self.getFont(self.fontpath, 'Minecraftia-Regular', 30) 
        main = Image.new(mode='RGB', size=(1800, 500), color=(0, 0, 0))
        draw, loc = ImageDraw.Draw(main), 0
        temp = sorted([round(sum((i['r'], i['g'], i['b']))/3) for i in temp_data])
        data = []
        for i in range(len(temp)):
            for j in range(len(temp_data)):
                calculation = round(sum((temp_data[j]['r'], temp_data[j]['g'], temp_data[j]['b']))/3)
                if calculation==temp[i]: data.append(temp_data[j])
        for i in data:
            rgb = (i['r'], i['g'], i['b'])
            content = '#%02x%02x%02x' % rgb
            draw.rectangle([
                (loc, 0), (loc+200, 500)
            ], fill=rgb)
            draw.text((loc, 0), content, font=font, align="left", fill=self.invert(rgb))
            loc += 200
        return self.buffer(main)

    def trans_merge(self, obj):
        av = self.imagefromURL(obj['url']).resize(obj['size'])
        bg = self.getImage(self.assetpath, obj['filename'].lower())
        cnv = Image.new(mode='RGB', color=(0,0,0), size=bg.size)
        try: cnv.paste(av, obj['pos'], av)
        except: cnv.paste(av, obj['pos'])
        cnv.paste(bg, (0,0), bg)
        return self.buffer(cnv)
    
    def merge(self, obj):
        av = self.imagefromURL(obj['url']).resize(obj['size'])
        bg = self.getImage(self.assetpath, obj['filename'].lower())
        bg.paste(av, obj['pos'])
        return self.buffer(bg)

    def blur(self, url):
        im = self.imagefromURL(url).filter(ImageFilter.BLUR)
        return self.buffer(im)
    
    def glitch(self, url):
        img = self.imagefromURL(url).resize((200, 200))
        p = img.load()
        for i in range(img.width):
            if random.randint(0, 1)==1:
                size = random.randint(0, img.height)
                for j in range(img.height):
                    getloc = i+size
                    if getloc >= img.width: getloc -= img.width
                    p[i, j] = img.getpixel((getloc, j))
        return self.buffer(img)
    def imagetoASCII(self, url):
        im = self.imagefromURL(url).resize((300, 300)).rotate(90).convert('RGB')
        im = im.resize((int(list(im.size)[0]/3)-60, int(list(im.size)[1]/3)))
        total_str = ""
        for i in range(im.width):
            for j in range(im.height):
                br = round(sum(im.getpixel((i, j)))/3)
                if br in range(0, 50): total_str += '.'
                elif br in range(50, 100): total_str += '/'
                elif br in range(100, 150): total_str += '$'
                elif br in range(150, 200): total_str += '#'
                else: total_str += '@'
            total_str += '\n'
        return total_str
    
    def spotify(self, details):
        url = details['url']
        del details['url']
        longest_word = [details[i] for i in list(details.keys()) if len(details[i])==sorted([
            len(details[a]) for a in list(details.keys())
        ])[::-1][0]][0]
        ava, bg = self.imagefromURL(url).resize((100, 100)), self.get_color_accent(self.thief, url)
        fg = self.invert(bg)
        big_font, smol_font = self.getFont(self.fontpath, 'NotoSansDisplay-Bold', 50, otf=True), self.getFont(self.fontpath, 'NotoSansDisplay-Bold', 17, otf=True)
        longest_font_width = smol_font.getsize(longest_word)[0] if longest_word!=details['name'] else big_font.getsize(details['name'])[0]   
        if longest_font_width < 300: longest_font_width = 300
        main = Image.new(mode='RGB', color=bg, size=(longest_font_width+275, 140))
        self.add_corners(ava, 50)
        main.paste(ava, (20, 20))
        draw = ImageDraw.Draw(main)
        draw.text((145, 9), details['name'], fill=fg, font=big_font)
        draw.text((145, 70), details['artist'], fill=fg, font=smol_font)
        draw.text((145, 92), details['album'], fill=fg, font=smol_font)
        self.add_corners(main, 25)
        return self.buffer(main)
    
    def profile(self, username, avatar, details, after):
        # yanderedev was here
        ava, ava_col = self.imagefromURL(avatar).resize((100, 100)), [(i['r'], i['g'], i['b']) for i in self.get_multiple_accents(avatar)]
        font, smolfont, smolerfont = self.getFont(self.fontpath, 'NotoSansDisplay-Bold', 50, otf=True), self.getFont(self.fontpath, 'NotoSansDisplay-Bold', 20, otf=True), self.getFont(self.fontpath, 'NotoSansDisplay-Bold', 15, otf=True)
        name = username
        data = font.getsize(name)[0]
        if data < 324: data = 324
        margin_left, margin_right = 50, data + 200
        bg, fg = ava_col[0], self.invert(ava_col[0])
        main = Image.new(mode='RGB', color=bg, size=(margin_right+50, 450))
        main.paste(ava, (50, 50))
        draw = ImageDraw.Draw(main)
        draw.text((170, 33), name, font=font, fill=fg)
        draw.text((170, 100), 'Joined since {}\n(order {})'.format(details['joined'], details['number']), fill=fg, font=smolfont)
        bal = details['wallet']+" Diamonds"
        draw.rectangle([(margin_left, 180), (margin_right, 240)], fill=ava_col[8])
        res_text = self.process_text(details['desc'], smolfont, (margin_right - 180) - 2)
        draw.rectangle([(margin_left, 240), (margin_right, 270)], fill=ava_col[3])
        draw.text((round((main.width - smolfont.getsize(bal)[0])/2), 239), bal, fill=self.invert(ava_col[3]), font=smolfont)
        draw.rectangle([(margin_left, 270), (round(main.width/2), 310)], fill=ava_col[1])
        draw.rectangle([(round(main.width/2), 270), (margin_right, 310)], fill=ava_col[2])
        draw.text((margin_left + 7, 277), details['wallet']+" at wallet", font=smolfont, fill=self.invert(ava_col[1]))
        draw.text((round(main.width/2) + 7, 277), details['bank']+" at bank", font=smolfont, fill=self.invert(ava_col[2]))
        draw.rectangle([(round(main.width/2), 310), (margin_right, 350)], fill=ava_col[4])
        draw.rectangle([(margin_left, 310), (round(main.width/2), 350)], fill=ava_col[5])
        draw.text((margin_left + 7, 317), "Local Rank #"+details['rank'], font=smolfont, fill=self.invert(ava_col[4]))
        draw.text((round(main.width/2) + 7, 317), "Global Rank #"+details['global'], font=smolfont, fill=self.invert(ava_col[5]))
        draw.text((margin_left + 3, 183), res_text, fill=self.invert(ava_col[8]), font=smolfont)
        if after!=None:
            draw.rectangle([(margin_left, 350), (margin_right, 370)], fill=ava_col[6])
            draw.rectangle([(margin_left, 370), (margin_right, 400)], fill=(100, 100, 100))
            try:
                now, next = int(details['wallet']), int(after['bal'])
                percentage = round(now/next*margin_right)
                if percentage < margin_left: percentage = margin_left
                if percentage > margin_right: percentage = margin_right
            except ZeroDivisionError:
                percentage = margin_right
            draw.rectangle([(margin_left, 370), (percentage, 400)], fill=(0, 255, 0))
            draw.text((margin_left + 2, 349), after['delta']+" Diamonds left before reaching next rank ("+after['nextrank']+")", font=smolerfont, fill=self.invert(ava_col[6]))
        self.add_corners(main, 25)
        return self.buffer(main)
    
    def evol(self, url):
        ava, img = self.imagefromURL(url).resize((77, 69)), self.getImage(self.assetpath, "evol.jpg")
        img.paste(ava, (255, 175))
        return self.buffer(img)
    
    def disconnected(self, msg):
        im = self.getImage(self.assetpath, 'disconnected.png')
        draw, myFont = ImageDraw.Draw(im), self.getFont(self.fontpath, 'Minecraftia-Regular', 16)
        w, h = myFont.getsize(msg)
        W, H = im.size
        draw.text(((W-w)/2,336), msg, font=myFont, fill="white")
        return self.buffer(im)
    
    def app(self, src, msg):
        im, ava = self.getImage(self.assetpath, "app.png"), self.imagefromURL(src).resize((159, 161))
        W, H = im.size
        draw, myFont = ImageDraw.Draw(im), self.getFont(self.fontpath, 'Roboto-Bold', 32)
        w, h = myFont.getsize(msg)
        draw.text(((W-w)/2,(H-h)/2+75), msg, font=myFont, fill="white")
        cnv = Image.new(mode='RGB', size=im.size, color=(0,0,0))
        cnv.paste(ava, (88, 31))
        cnv.paste(im, (0, 0), im)
        return self.buffer(cnv)
    
    def ruin(self, ava):
        im = self.getImage(self.assetpath, 'destroyimg.png')
        av = self.imagefromURL(ava)
        av.paste(im, (0,0), im)
        return self.buffer(av)
    
    def hitler(self, ava):
        ava = self.imagefromURL(ava).resize((141, 167))
        im = self.getImage(self.assetpath, 'worse-than-hitler.png')
        im.paste(ava, (46, 31))
        return self.buffer(im)
    
    def serverstats(self, guild):
        start = "https://quickchart.io/chart?c="
        data1 = [
            str(len([i for i in guild.members if i.status.value.lower()=='online'])),
            str(len([i for i in guild.members if i.status.value.lower()=='idle'])),
            str(len([i for i in guild.members if i.status.value.lower()=='dnd'])),
            str(len([i for i in guild.members if i.status.value.lower()=='offline']))
        ]
        img1 = "{type:'pie',data:{labels:['Online', 'Idle', 'Do not Disturb', 'Offline'], datasets:[{data:["+data1[0]+", "+data1[1]+", "+data1[2]+", "+data1[3]+"]}]}}"
        img = self.imagefromURL(start+myself.urlify(img1))
        w, h = img.size
        cnv = Image.new(mode='RGB', size=(w, h), color=(255, 255, 255))
        cnv.paste(img, (0, 0), img)
        return self.buffer(cnv)
    
    def lookatthisgraph(self, url):
        img = self.imagefromURL(url).resize((741, 537)).rotate(20)
        bg = self.getImage(self.assetpath, 'graph.png')
        canvas = Image.new(mode='RGB', size=(1920, 1080), color=(0,0,0))
        canvas.paste(img, (833, 365))
        canvas.paste(bg, (0, 0), bg)
        return self.buffer(canvas)
    
    def squidwardstv(self, avatar):
        cnv = Image.new(mode='RGB', size=(1088, 720), color=(0, 0, 0))
        img = self.getImage(self.assetpath, 'squidwardstv.png')
        ava = self.imagefromURL(avatar).resize((577, 467))
        cnv.paste(ava.rotate(-27), (381, 125))
        cnv.paste(img, (0, 0), img)
        return self.buffer(cnv)
    
    def waifu(self, avatar):
        cnv = Image.new(mode='RGB', size=(450, 344), color=(0, 0, 0))
        img = self.getImage(self.assetpath, 'waifu.png')
        ava = self.imagefromURL(avatar).resize((131, 162))
        cnv.paste(ava.rotate(-20), (112, 182))
        cnv.paste(img, (0, 0), img)
        return self.buffer(cnv)
    
    def ifunny(self, avatar):
        avatar, watermark = self.imagefromURL(avatar).resize((545, 481)), self.getImage(self.assetpath, 'ifunny.png')
        avatar.paste(watermark, (0, 0), watermark)
        return self.buffer(avatar)
        
    def wasted(self, avatar):
        avatar, wasted = self.imagefromURL(avatar).resize((240, 240)), self.getImage(self.assetpath, 'wasted.png').resize((240, 240))
        try:
            red = Image.new(mode='RGB', size=(240, 240), color=(255, 0, 0))
            avatar = Image.blend(avatar, red, alpha=0.4)
        except ValueError:
            pass
        avatar.paste(wasted, (0, 0), wasted)
        return self.buffer(avatar)
    
    def ifearnoman(self, url, url2):
        avpic = self.imagefromURL(url)
        avpic2 = self.imagefromURL(url2)
        template = self.getImage(self.assetpath, 'ifearnoman.jpg')
        template.paste(avpic.resize((173, 159)), (98, 28))
        template.paste(avpic.resize((114, 109)), (60, 536))
        template.paste(avpic.resize((139, 145)), (598, 549))
        template.paste(avpic2.resize((251, 249)), (262, 513))
        data = self.buffer(template)
        return data
    
    def simpletext(self, text):
        image = Image.new(mode='RGB',size=(5+(len(text)*38)+5, 80) ,color=(255, 255, 255))
        self.drawtext(ImageDraw.Draw(image), self.getFont(self.fontpath, 'consola', 60), text, 10, 10, "black")
        data = self.buffer(image)
        return data
    
    def baby(self, ava):
        avatar = self.imagefromURL(ava)
        canvas = Image.new(mode='RGB',size=(728, 915) ,color=(0, 0, 0))
        baby = self.getImage(self.assetpath, "baby.png")
        avatar = avatar.resize((382, 349))
        avatar = avatar.rotate(50)
        canvas.paste(avatar, (203, 309))
        canvas.paste(baby, (0, 0), baby)
        data = self.buffer(canvas)
        return data
    
    def art(self, ava):
        image = self.getImage(self.assetpath, 'art.png')
        cnv, pic = Image.new(mode='RGB', size=(1364, 1534), color=(0,0,0)), self.imagefromURL(ava)
        cnv.paste(pic.resize((315, 373)), (927, 94))
        cnv.paste(pic.resize((318, 375)), (925, 861))
        cnv.paste(image, (0, 0), image)
        return self.buffer(cnv)
    
    def resize(self, url, x, y):
        pic = self.imagefromURL(url)
        pic = pic.resize((x, y))
        data = self.buffer(pic)
        return data
    
    def urltoimage(self, url, stream=False):
        image = self.imagefromURL(url, stream=stream)
        return self.buffer(image)
    
    def smallURL(self, url):
        image = self.imagefromURL(url)
        size = list(image.size)
        pic = image.resize((round(size[0]/4), round(size[1]/4)))
        data = self.buffer(pic)
        return data
    
    def gif2png(self, url):
        img = self.imagefromURL(url)
        img.seek(0)
        return self.buffer(img)
        
    def memegen(self, url):
        image = self.imagefromURL(url)
        area = (0, 20, list(image.size)[0], list(image.size)[1]-12)
        cropped_img = image.crop(area)
        data = self.buffer(cropped_img)
        return data
    
class GifGenerator:
    
    def __init__(self, assetpath, fontpath):
        self.imagefromURL = imagefromURL
        self.getImage = getImage
        self.bufferGIF = bufferGIF
        self.assetpath = assetpath
        self.fontpath = fontpath
        self.drawtext = drawtext
        self.getFont = getFont
    
    def worship(self, pic):
        im = self.imagefromURL(pic).resize((127, 160))
        gi = self.getImage(self.assetpath, 'worship.gif')
        images = []
        for i in range(gi.n_frames):
            gi.seek(i)
            cnv = Image.new(mode='RGB', color=(0,0,0), size=gi.size)
            cnv.paste(gi, (0,0))
            try: cnv.paste(im, (303, 7), im)
            except: cnv.paste(im, (303, 7))
            images.append(cnv)
        return self.bufferGIF(images, 5)

    def flip(self, pic):
        im = self.imagefromURL(pic).resize((400,400))
        inv_im = ImageOps.flip(im)
        speed, images = [3,6,13,25,50,100,200,399], []
        for i in range(len(speed)*2):
            stretch = speed[i] if i < len(speed) else speed[::-1][i-len(speed)]
            image = im if i < len(speed) else inv_im
            cnv = Image.new(mode='RGB', size=(400, 400), color=(0,0,0))
            cnv.paste(image.resize((400, 400-stretch)), (0, round(stretch/2)))
            images.append(cnv)
        images += images[::-1]
        return self.bufferGIF(images, 5)
    def crazy_frog_dance(self, pic, metadata):
        im = self.getImage(self.assetpath, 'crazyfrog.gif')
        ava = self.imagefromURL(pic)
        size, images = im.size, []
        for i in range(im.n_frames):
            im.seek(i)
            ava_size = tuple([int(a) for a in metadata[i].split(';')[0].split(',')])
            placement = tuple([int(a) for a in metadata[i].split(';')[1].split(',')])
            cnv = Image.new(mode='RGB', size=size, color=(0,0,0))
            cnv.paste(im.convert('RGB'), (0,0))
            cnv.paste(ava.resize(placement), ava_size)
            images.append(cnv)
        return self.bufferGIF(images, 5)

    def destroy_computer(self, pic, metadata):
        data = self.getImage(self.assetpath, 'rage.gif')
        ava = self.imagefromURL(pic).resize((40, 40))
        imsize = data.size
        images = []
        for i in range(data.n_frames):
            data.seek(i)
            cnv = Image.new(mode='RGB', size=imsize, color=(0,0,0))
            cnv.paste(data.convert('RGB'), (0,0))
            cnv.paste(ava, metadata[i])
            images.append(cnv)
        return self.bufferGIF(images, 4.3)

    def death_star(self, pic):
        gif_template = self.getImage(self.assetpath, 'explosion.gif')
        ava, images, size = self.imagefromURL(pic).resize((61, 62)), [], gif_template.size
        for i in range(gif_template.n_frames):
            canvas = Image.new(mode='RGB', color=(0,0,0), size=size)
            canvas.paste(gif_template, (0,0))
            gif_template.seek(i)
            if i < 7: canvas.paste(ava, (183, 143))
            images.append(canvas)
        return self.bufferGIF(images, 3)

    def rotate(self, pic):
        image = self.imagefromURL(pic)
        image = image.resize((216, 216))
        images, num = [], 0
        while num<360:
            images.append(image.rotate(num))
            num += 5
        data = self.bufferGIF(images, 5)
        return data
    
    def triggered(self, pic, increment):
        image = self.imagefromURL(pic)
        image = image.resize((216, 216))
        red = Image.new(mode='RGB', size=(216, 216), color=(255, 0, 0))
        image = Image.blend(image, red, alpha=0.25)
        text = self.getImage(self.assetpath, 'triggered.jpg')

        canvas = Image.new(mode='RGB',size=image.size ,color=(0, 0, 0))
        images, num = [], 0
        while num<100:
            canvas.paste(image, (random.randint(-increment, increment), random.randint(-increment, increment)))
            images.append(canvas)
            canvas.paste(text, (random.randint(-increment, increment), (216-39)+(random.randint(-increment, increment))))
            canvas = Image.new(mode='RGB',size=image.size ,color=(0, 0, 0))
            num += 5
        data = self.bufferGIF(images, 3)
        return data

    def communist(self, comrade):
        flag = self.getImage(self.assetpath, 'blyat.jpg').convert('RGB')
        user = self.imagefromURL(comrade).resize((216, 216)).convert('RGB')
        images = []
        opacity = float(0)
        while int(opacity)!=1:
            newimage = Image.blend(user, flag, opacity)
            images.append(newimage)
            opacity += 0.05
        extras = 0

        while extras<100:
            image = flag
            self.drawtext(ImageDraw.Draw(image), self.getFont(self.fontpath, 'Whitney-Medium', 30), 'COMMUNIST', 216/2-86, 10, 'white')
            self.drawtext(ImageDraw.Draw(image), self.getFont(self.fontpath, 'Whitney-Medium', 30), 'CONFIRMED', 216/2-84, 170, 'white')
            images.append(image)
            extras += 1
        data = self.bufferGIF(images, 5)
        return data
    
    def giffromURL(self, url, compress):
        mygif = self.imagefromURL(url)
        frames = []
        for i in range(0, mygif.n_frames):
            mygif.seek(i)
            if compress: frames.append(mygif.resize((216, 216))) ; continue
            frames.append(mygif)
        data = self.bufferGIF(frames, 5)
        return data