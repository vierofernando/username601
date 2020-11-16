from PIL import (
    Image,
    ImageFont,
    ImageDraw,
    ImageSequence,
    ImageOps,
    ImageFilter,
    ImageColor,
    GifImagePlugin
)
import json
import random
from numpy import zeros, uint8
from time import strftime, gmtime
from io import BytesIO
from datetime import datetime as t
from requests import get
from .smart_colorthief import Smart_ColorThief
from .username601 import *
from colorthief import ColorThief

def buffer_from_url(url, *args, **kwargs):
    try: return Image.open(BytesIO(get(url, timeout=5).content))
    except: raise TypeError(f"Oopsies there was an error on fetching: {url}")

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
    return im

class Painter:

    def __init__(self, assetpath, fontpath): # lmao wtf is this
        self.buffer_from_url = buffer_from_url
        self.assetpath = assetpath
        self.fontpath = fontpath
        self.flags = json.loads(open(config('JSON_DIR')+'/flags.json', 'r').read())
        self.region = json.loads(open(config('JSON_DIR')+'/regions.json', 'r').read())
        self.gd_assets = json.loads(open(config('JSON_DIR')+'/gd.json', 'r').read())
        self.add_corners = add_corners

    def mask_circle(self, im):
        bigsize = (im.size[0] * 3, im.size[1] * 3)
        mask = Image.new('L', bigsize, 0)
        draw = ImageDraw.Draw(mask) 
        draw.ellipse((0, 0) + bigsize, fill=255)
        mask = mask.resize(im.size, Image.ANTIALIAS)
        im.putalpha(mask)

    def drawtext(self, draw, thefont, text, x, y, col):
        draw.text((x, y), text, fill =col, font=thefont, align ="left")

    def get_font(self, fontname, size, otf=False):
        ext = 'ttf' if not otf else 'otf'
        return ImageFont.truetype(f'{self.fontpath}/{fontname}.{ext}', size)

    def get_image(self, imageName):
        return Image.open(f'{self.assetpath}/{imageName}')

    def invert(self, tupl):
        if (sum(tupl)/3) < 127.5: return (255, 255, 255)
        return (0, 0, 0)

    def wrap_text(self, text, width, font, array=False):
        res, temp = [], ""
        for i in list(text):
            temp += i
            if font.getsize(temp)[0] < width:
                continue
            res.append(temp+'-')
            temp = ""
        if len(''.join(res)) != len(text):
            res.append(temp+'-')
        if res ==[]:
            if array: return [''.join(temp)[:-1]]
            return ''.join(temp)[:-1]
        res[len(res)-1] = res[len(res)-1][:-1]
        if array: return res
        return '\n'.join(res)

    def _process_message_box(self, text, font, content=False):
        if not content:
            size, index, hit_max, res = 0, 0, True, ""
            while size < 360:
                if res == text:
                    hit_max = False
                    break
                res += text[index]
                size = font.getsize(res)[0]
                index += 1
            if hit_max: res += "..."
            return res
        temp = ""
        res = []
        for i in list(text):
            if len(res) == 3: break
            temp += i
            if font.getsize(temp)[0] > 312:
                res.append(temp)
                temp = ""
                continue
        if res == []: return text
        return "\n".join(res)
    
    def fake_message_box(self, title, description):
        image = self.get_image("msgbox.png")
        big_font = self.get_font("segoeui", 12)
        small_font = self.get_font("segoeui", 11)
        draw = ImageDraw.Draw(image)
        title = self._process_message_box(title[0:250], big_font)
        description = self._process_message_box(description[0:250], small_font, content=True)
        draw.text((9, 7), title, font=big_font)
        draw.text((63, 57), description, font=small_font, fill=(0, 0, 0))
        return self.buffer(image)

    def _draw_status_stats(self, draw, obj, rect_y_cursor, font, margin_left, margin_right, bg_arr):
        x_pos, colors = margin_left, [(63, 232, 0), (244, 208, 63), (225, 0, 0), (124, 0, 211), (127, 127, 127)]
        total = sum(map(lambda i: obj[i], obj.keys()))
        draw.rectangle([
            (margin_left, rect_y_cursor), (margin_right, rect_y_cursor + 25)
        ], fill=bg_arr[1])
        draw.text((margin_left + 3, rect_y_cursor + 2), "Member status graph:", fill=self.invert(bg_arr[1]), font=font)
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

    def buffer(self, data):
        arr = BytesIO()
        data.save(arr, format='PNG')
        arr.seek(0)
        return arr

    def toLocaleString(self, num):
        return f'{str(num):,}'
    
    def get_color_accent(self, url, right=False):
        res = Smart_ColorThief(url).get_color(right=right)
        return res[0], res[1], res[2]

    def gradient(self, color_left, color_right):
        if color_right is not None:
            main = Image.new("RGB", (1000, 500), color=color_right)
        array = zeros([500, 1000, 4], dtype=uint8)
        for y in range(1000):
            arr = [color_left[0], color_left[1], color_left[2], round((1000 - y)/1000 * 255)]
            for x in range(500):
                array[x, y] = arr
        image_overlay = Image.fromarray(array)
        if color_right is None:
            return self.buffer(image_overlay)
        main.paste(image_overlay, (0, 0), image_overlay)
        return self.buffer(main)

    def get_multiple_accents(self, image):
        b = BytesIO(get(image).content)
        return list(map(lambda i: {
            'r': i[0], 'g': i[1], 'b': i[2]
        }, ColorThief(b).get_palette(color_count=10)))

    def geometry_dash_icons(self, name):
        GD_FORMS = ('cube', 'ship', 'ball', 'ufo', 'wave', 'robot', 'spider')
        forms = [self.buffer_from_url(f"https://gdbrowser.com/icon/{name}?form={i}") for i in GD_FORMS]
        width = sum(map(lambda i: i.width, forms)) + (len(GD_FORMS) * 25) + 25
        curs = 25
        main = Image.new(mode="RGBA", size=(width, 250), color=(0, 0, 0, 0))
        for i in forms:
            main.paste(i, (curs, round((main.height - i.height) / 2)))
            curs += (i.width + 25)
        return self.buffer(main)

    def minecraft_body(self, url, uuid):
        body_3d = self.buffer_from_url(url) # LMAO 420 NICE
        main = Image.new(mode="RGBA", size=(body_3d.width + 420, body_3d.height), color=(0, 0, 0, 0))
        main.paste(body_3d, (0, 0))
        textures = get(f"https://api.minetools.eu/profile/{uuid}").json()["decoded"]["textures"]
        raw_texture = self.buffer_from_url(textures["SKIN"]["url"])
        main.paste(raw_texture.resize((400, 200)), (body_3d.width + 20, 0))
        try:
            cape = self.buffer_from_url(textures["CAPE"]["url"])
            main.paste(cape.resize((400, 200)), (body_3d.width + 20, 220))
        except: pass
        return self.buffer(main)

    def bottom_image_meme(self, image_url, text):
        main = Image.new("RGB", size=(500, 500), color=(255, 255, 255))
        font = self.get_font("Helvetica", 35)
        draw = ImageDraw.Draw(main)
        curs = 5
        for i in self.wrap_text(text, 475, font, array=True)[0:5]:
            draw.text((5, curs), i, font=font, fill='black')
            curs += 35
        main.paste(self.buffer_from_url(image_url).resize((500, 300)), (0, 200))
        return self.buffer(main)

    def blend(self, user1, user2):
        pic1 = self.buffer_from_url(user1).resize((500, 500)).convert("RGB")
        pic2 = self.buffer_from_url(user2).resize((500, 500)).convert("RGB")
        res = Image.blend(pic1, pic2, alpha=0.5)
        return self.buffer(res)

    def color(self, string, rgb_input=None):
        if rgb_input is not None: string = '#%02x%02x%02x' % rgb_input
        if not string.startswith('#'): string = '#' + string
        try: rgb, brightness = ImageColor.getrgb(string), ImageColor.getcolor(string, 'L')
        except: return None
        main = Image.new(mode='RGB', size=(500, 500), color=rgb)
        try: color_name = get('https://api.alexflipnote.dev/color/'+string[1:]).json()['name']
        except: color_name = 'Unknown'
        big_font = self.get_font("Aller", 50)
        medium_font = self.get_font("Aller", 30)
        small_font = self.get_font("Aller", 20)
        draw = ImageDraw.Draw(main)
        draw.text((10, 10), string, fill=self.invert(rgb), font=big_font)
        draw.text((10, 75), color_name, fill=self.invert(rgb), font=medium_font)
        draw.text((10, 115), f'RGB: {rgb[0]}, {rgb[1]}, {rgb[2]}\nInteger: {rgb[0]*rgb[1]*rgb[2]}\nBrightness: {brightness}', fill=self.invert(rgb), font=small_font)
        return self.buffer(main)

    def among_us(self, url):
        bg = self.get_image('among_us.png')
        ava = self.buffer_from_url(url).resize((240, 228))
        col = self.get_color_accent(url)
        cnv = Image.new(mode='RGBA', size=(512, 512), color=(0,0,0))
        draw = ImageDraw.Draw(cnv)
        draw.rectangle([(0, 0), (512, 512)], fill=col)
        cnv.paste(bg, (0,0), bg)
        anothercnv = Image.new(mode='RGB', size=(512, 512), color=(0,0,0))
        anothercnv.paste(ava, (47, 129))
        anothercnv.paste(cnv, (0, 0), cnv)
        return self.buffer(anothercnv)

    def gru(self, text1, text2, text3):
        main = self.get_image("gru.png")
        draw = ImageDraw.Draw(main)
        font = self.get_font("Helvetica", 15)
        curs = 60
        for i in self.wrap_text(text1, 125, font, array=True)[0:10]:
            draw.text((212, curs), i, font=font, fill='black')
            curs += 15
        curs = 60
        for i in self.wrap_text(text2, 125, font, array=True)[0:10]:
            draw.text((558, curs), i, font=font, fill='black')
            curs += 15
        curs = 283
        for i in self.wrap_text(text3, 125, font, array=True)[0:10]:
            draw.text((214, curs), i, font=font, fill='black')
            draw.text((561, curs), i, font=font, fill='black')
            curs += 15
        return self.buffer(main)

    def presentation(self, text):
        im = self.get_image('presentation.jpg')
        font = self.get_font('Helvetica', 25)
        draw, curs = ImageDraw.Draw(im), 65
        for i in self.wrap_text(text, 432, font, array=True)[0:7]:
            draw.text((113, curs), i, font=font, fill='black')
            curs += 30
        return self.buffer(im)

    def scooby(self, url):
        im = self.buffer_from_url(url)
        bg = self.get_image('scooby.png')
        cnv = Image.new(mode='RGB', size=(720, 960), color=(0, 0, 0))
        cnv.paste(im.resize((100, 93)), (139, 153))
        cnv.paste(im.resize((194, 213)), (79, 569))
        cnv.paste(bg, (0, 0), bg)
        return self.buffer(cnv)

    def password(self, bad_pass, good_pass):
        im = self.get_image('pass.png')
        font = self.get_font('Helvetica', 25)
        draw = ImageDraw.Draw(im)
        draw.text((42, 80), self.wrap_text(bad_pass, 396, font, array=True)[0], font=font, fill='black')
        draw.text((42, 311), self.wrap_text(good_pass, 396, font, array=True)[0], font=font, fill='black')
        return self.buffer(im)

    def geometry_dash_level(self, levelid, daily=False, weekly=False):
        # a shit ton of declarations first xd
        if daily: query = 'daily'
        elif weekly: query = 'weekly'
        else: query = str(levelid)
        data = get('https://gdbrowser.com/api/level/'+query).json()
        pusab_big = self.get_font('PUSAB__', 40, otf=True)
        pusab_smol = self.get_font('PUSAB__', 30, otf=True)
        pusab_smoler = self.get_font('PUSAB__', 20, otf=True)
        pusab_tiny = self.get_font('PUSAB__', 20, otf=True)
        aller = self.get_font('Aller', 20)
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
        texts, sym_cursor = self.wrap_text(levelDesc, 445, aller, array=True), 100

        for i in texts:
            w, h = aller.getsize(i)
            draw.text(((W-w)/2, desc_cursor), i, font=aller, fill='white')
            desc_cursor += 25
        del desc_cursor, width, texts

        difficulty = self.buffer_from_url("https://gdbrowser.com/difficulty/"+data['difficultyFace']+".png").convert('RGBA').resize((75, 75))
        main.paste(difficulty, (round((W - 75)/2) - 100, 100), difficulty)
        w, h = pusab_tiny.getsize(levelDiff)
        draw.text(((W - w)/2 - 100, 180), levelDiff, font=pusab_tiny, stroke_width=2, stroke_fill="black")
        w, h = pusab_tiny.getsize(levelStars)
        draw.text(((W - w)/2 - 100, 200), levelStars, font=pusab_tiny, stroke_width=2, stroke_fill="black")

        for i in list(self.gd_assets['main'].keys()):
            if self.gd_assets['main'][i] is None:
                if data['disliked']: sym = self.buffer_from_url(self.gd_assets['dislike']).convert('RGBA').resize((25, 25))
                else: sym = self.buffer_from_url(self.gd_assets['like']).convert('RGBA').resize((25, 25))
                main.paste(sym, (round((W-25)/2) + 75, sym_cursor), sym)
                draw.text((round((W-25)/2)+105, sym_cursor+5), str(data['likes']), font=pusab_smoler, stroke_width=2, stroke_fill="black")
                sym_cursor += 30
                continue
            if i not in list(data.keys()): continue
            sym = buffer_from_url(self.gd_assets['main'][i]).convert('RGBA').resize((25, 25))
            main.paste(sym, (round((W-25)/2) + 75, sym_cursor), sym)
            draw.text((round((W-25)/2)+105, sym_cursor+5), str(data[i]), font=pusab_smoler, stroke_width=2, stroke_fill="black")
            sym_cursor += 30
        
        main = self.add_corners(main, 20)
        return self.buffer(main)

    def invert_image(self, im):
        ava = self.buffer_from_url(im).convert('RGB')
        im_invert = ImageOps.invert(ava)
        return self.buffer(im_invert)
    
    def grayscale(self, im):
        res = self.buffer_from_url(im).convert('L')
        return self.buffer(res)

    def country(self, query):
        bigfont = self.get_font('NotoSansDisplay-Bold', 35, otf=True)
        smolfont = self.get_font('NotoSansDisplay-Bold', 25, otf=True)
        smolerfont = self.get_font('NotoSansDisplay-Bold', 20, otf=True)
        data = get('https://restcountries.eu/rest/v2/name/'+query).json()[0]
        length = bigfont.getsize(data['name'])[0] + 200
        flagid, flagnotfound = data['alpha2Code'].lower(), False
        try: cf = [(
            i['r'], i['g'], i['b']
        ) for i in self.get_multiple_accents("https://www.worldometers.info/img/flags/"+flagid+"-flag.gif")]
        except: flagnotfound = True
        size = (length, 400)
        if flagnotfound:
            cf = list(map(lambda: (0,0,0), range(5)))
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
        draw.text((margin_left+5, 78), self.wrap_text('Capital: '+capital, main.width+90, smolfont), font=smolerfont, fill=self.invert(cf[2]))
        draw.text((margin_left+5, 103), self.wrap_text('Region: '+data['region'], main.width+90, smolfont), font=smolerfont, fill=self.invert(cf[2]))
        draw.text((margin_left+5, 128), self.wrap_text('Subregion: '+data['subregion'], main.width+90, smolfont), font=smolerfont, fill=self.invert(cf[2]))
        draw.text((margin_left+5, 153), self.wrap_text('Population: '+self.toLocaleString(str(data['population'])), main.width+90, smolfont), font=smolerfont, fill=self.invert(cf[2]))
        draw.text((margin_left+5, 178), self.wrap_text('Area: '+self.toLocaleString(str(round(data['area'])))+' km', main.width+90, smolfont), font=smolerfont, fill=self.invert(cf[2]))
        draw.text((margin_left+5, 203), self.wrap_text('Timezones: '+', '.join(data['timezones']), main.width+90, smolfont), font=smolerfont, fill=self.invert(cf[2]))
        return {
            'buffer': self.buffer(main),
            'color': cf[0],
            'image': "https://google.com/" if flagnotfound else "https://www.worldometers.info/img/flags/"+flagid+"-flag.gif"
        }

    def server(self, guild, data=None, raw=None):
        bigfont = self.get_font('NotoSansDisplay-Bold', 50, otf=True)
        medium = self.get_font('NotoSansDisplay-Bold', 20, otf=True)
        smolerfont = self.get_font('NotoSansDisplay-Bold', 15, otf=True)
        if data is None:
            server_title, members, icon = guild.name, guild.members, guild.icon_url
            subtitle = 'Created {} ago by {}'.format(lapsed_time_from_seconds(t.now().timestamp() - guild.created_at.timestamp()), str(guild.owner))
        else:
            server_title, icon = data['name'], "https://cdn.discordapp.com/icons/{}/{}.png?size=1024".format(data['id'], data['icon'])
            subtitle = data['description']
        title_width = bigfont.getsize(server_title)[0]
        ava = self.buffer_from_url(icon).resize((100, 100))
        self.mask_circle(ava)
        bg_arr = [(i['r'], i['g'], i['b']) for i in self.get_multiple_accents(icon)]
        desc_width = medium.getsize(subtitle)[0]
        if desc_width > title_width: title_width = desc_width # :^)
        main_bg = bg_arr[0]
        margin_left, margin_right, rect_y_cursor = 25, title_width+225, 150
        main = Image.new(mode='RGB', color=main_bg, size=(title_width+250, 480))
        draw, a_third_width = ImageDraw.Draw(main), round((margin_right - margin_left)/3)
        main.paste(ava, (25, 25))
        draw.text((135, 20), server_title, fill=self.invert(main_bg), font=bigfont)
        draw.text((135, 90), subtitle, fill=self.invert(main_bg), font=medium)
        if data is None:
            rect_y_cursor = self._draw_status_stats(draw, {
                "online": len([i for i in members if i.status.value.lower()=='online']),
                "idle": len([i for i in members if i.status.value.lower()=='idle']),
                "do not disturb": len([i for i in members if i.status.value.lower()=='dnd']),
                "streaming": len([i for i in members if i.status.value.lower()=='streaming']),
                "offline": len([i for i in members if i.status.value.lower()=='offline'])
            }, rect_y_cursor, smolerfont, margin_left, margin_right, bg_arr)
        draw.rectangle([
            (margin_left, rect_y_cursor), (main.width/2, rect_y_cursor + 120)
        ], fill=bg_arr[2])
        if data is None:
            draw.rectangle([
                (main.width/2, rect_y_cursor), (margin_right, rect_y_cursor + 120)
            ], fill=bg_arr[3])
            afkname = "???" if guild.afk_channel is None else guild.afk_channel.name
            main.paste(
                self.buffer_from_url(self.region[str(guild.region)]).resize((35, 23)),
                (margin_right - 45, round(rect_y_cursor + 25 + (18 * 3)))
            )
            draw.text((margin_left + 5, rect_y_cursor + 3), "Channels: {}\nRoles: {}\nLevel {}\n{} boosters".format(
                len(guild.channels), len(guild.roles), guild.premium_tier, guild.premium_subscription_count
            ), fill=self.invert(bg_arr[2]), font=medium)
            draw.text(((main.width/2) + 5, rect_y_cursor + 3), "Region: {}\nAFK: {}\nAFK time: {}".format(
                str(guild.region).replace('-', ''), afkname, lapsed_time_from_seconds(guild.afk_timeout).replace('minute', 'min')
            ), fill=self.invert(bg_arr[3]), font=medium)
        else:
            draw.text((margin_left + 5, rect_y_cursor + 3), "Approx. Members: {}\nApprox. Presence: {}".format(raw['approximate_member_count'], raw['approximate_presence_count']), fill=self.invert(bg_arr[2]), font=medium)
        rect_y_cursor += 120
        draw.rectangle([
            (margin_left, rect_y_cursor), (margin_right, rect_y_cursor + 90)
        ], fill=bg_arr[4])
        if data is None:
            draw.text((margin_left + 5, rect_y_cursor + 3), "{} Humans\n{} Bots\n{} Members in total".format(
                len([i for i in members if not i.bot]), len([i for i in members if i.bot]), len(members)
            ), fill=self.invert(bg_arr[4]), font=medium)
        else:
            text = ', '.join(map(
                lambda i: i.replace('_', ' ').lower(), data['features']
            ))
            draw.text((margin_left + 5, rect_y_cursor + 5), self.wrap_text(text, (margin_right-5) - (margin_left+5), medium), fill=self.invert(bg_arr[4]), font=medium)
        main = self.add_corners(main, 25)
        return self.buffer(main)

    def usercard(self, roles, user, ava, bg, nitro, booster, booster_since):
        name, flags, flag_x = user.name, [], 170
        bigfont = self.get_font('NotoSansDisplay-Bold', 50, otf=True)
        mediumfont = self.get_font('NotoSansDisplay-Bold', 25, otf=True)
        if nitro: flags.append(self.flags['nitro'])
        if booster: flags.append(self.flags['booster'])
        for i in list(self.flags['badges'].keys()):
            if getattr(user.public_flags, i): flags.append(self.flags['badges'][i])
        foreground_col = self.invert(bg)
        avatar = self.buffer_from_url(ava).resize((100, 100))
        self.mask_circle(avatar)
        if not booster_since: details_text = 'Created account {}\nJoined server {}'.format(lapsed_time_from_seconds(t.now().timestamp()-user.created_at.timestamp())+' ago', lapsed_time_from_seconds(t.now().timestamp()-user.joined_at.timestamp())+' ago')
        else: details_text = 'Created account {}\nJoined server {}\nBoosting since {}'.format(lapsed_time_from_seconds(t.now().timestamp()-user.created_at.timestamp())+' ago', lapsed_time_from_seconds(t.now().timestamp()-user.joined_at.timestamp())+' ago', lapsed_time_from_seconds(booster_since)+' ago')
        rect_y_pos = 180 + ((bigfont.getsize(details_text)[1]+20))
        canvas_height = rect_y_pos + len(roles * 50) + 30
        if bigfont.getsize(name)[0] > 600: main = Image.new(mode='RGB', color=bg, size=(bigfont.getsize(name)[0]+200, canvas_height))
        else: main = Image.new(mode='RGB', color=bg, size=(600, canvas_height))
        draw = ImageDraw.Draw(main)
        margin_right, margin_left = main.width - 40, 40
        draw.text((170, 20), name, fill=foreground_col, font=bigfont)
        draw.text((170, 80), f'ID: {user.id}', fill=foreground_col, font=mediumfont)
        for i in flags:
            temp_im = self.buffer_from_url(i).resize((25, 25))
            main.paste(temp_im, (flag_x, 115), temp_im)
            flag_x += 30
        draw.text((40, 150), details_text, fill=foreground_col, font=mediumfont)
        for i in roles:
            draw.rectangle([
                (margin_left, rect_y_pos), (margin_right, rect_y_pos+50)
            ], fill=i['color'])
            draw.text((margin_left+10, rect_y_pos+7), i['name'], fill=self.invert(i['color']), font=mediumfont)
            rect_y_pos += 50
        try: main.paste(avatar, (40, 30), avatar)
        except: main.paste(avatar, (40, 30))
        main = self.add_corners(main, 25)
        return self.buffer(main)

    def get_palette(self, temp_data):
        font = self.get_font('Minecraftia-Regular', 30) 
        main = Image.new(mode='RGB', size=(1800, 500), color=(0, 0, 0))
        draw, loc = ImageDraw.Draw(main), 0
        temp = sorted(list(map(lambda i: round(sum((i['r'], i['g'], i['b']))/3), temp_data)))
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
        av = self.buffer_from_url(obj['url']).resize(obj['size'])
        bg = self.get_image(obj['filename'].lower())
        cnv = Image.new(mode='RGB', color=(0,0,0), size=bg.size)
        try: cnv.paste(av, obj['pos'], av)
        except: cnv.paste(av, obj['pos'])
        cnv.paste(bg, (0,0), bg)
        return self.buffer(cnv)
    
    def merge(self, obj):
        av = self.buffer_from_url(obj['url']).resize(obj['size'])
        bg = self.get_image(obj['filename'].lower())
        bg.paste(av, obj['pos'])
        return self.buffer(bg)

    def blur(self, url):
        im = self.buffer_from_url(url).filter(ImageFilter.BLUR)
        return self.buffer(im)
    
    def imagetoASCII(self, url):
        im = self.buffer_from_url(url).resize((300, 300)).rotate(90).convert('RGB')
        im = im.resize((int(list(im.size)[0]/3)-60, int(list(im.size)[1]/3)))
        total_str = ""
        for i in range(im.width):
            for j in range(im.height):
                br = round(sum(im.getpixel((i, j)))/3)
                if br in range(32): total_str += ':'
                elif br in range(32, 64): total_str += '-'
                elif br in range(64, 96): total_str += '='
                elif br in range(96, 128): total_str += '+'
                elif br in range(128, 159): total_str += '*'
                elif br in range(159, 191): total_str += '#'
                elif br in range(191, 223): total_str += '%'
                else: total_str += "@"
            total_str += '\n'
        return '\n'.join(map(lambda i: i[::-1], total_str.split('\n')))
    def imagetoASCII_picture(self, url):
        font = self.get_font("consola", 11)
        image = Image.new(mode='RGB', size=(602, 523), color=(0, 0, 0))
        draw, string = ImageDraw.Draw(image), self.imagetoASCII(url)
        draw.text((0, 0), string, font=font, fill=(255, 255, 255))
        return self.buffer(image)

    def custom_panel(self, title="Title text", subtitle="Subtitle text", description="Description text here", icon="https://cdn.discordapp.com/embed/avatars/0.png", spt=None):
        SPOTIFY = False if (spt is None) else True
        TITLE_TEXT = title if not SPOTIFY else spt["title"]
        TITLE_FONT = self.get_font("NotoSansDisplay-Bold", 30, otf=True)

        SUBTITLE_TEXT = subtitle if not SPOTIFY else "By "+spt["artists"]
        SUBTITLE_FONT = self.get_font("NotoSansDisplay-Bold", 20, otf=True)

        DESC_TEXT = description if not SPOTIFY else "On "+spt["album"]
        DESC_FONT = self.get_font("NotoSansDisplay-Bold", 15, otf=True)
        COVER_URL = icon if not SPOTIFY else spt["cover"]
        COVER = self.buffer_from_url(COVER_URL).resize((200, 200))
        BACKGROUND_COLOR = self.get_color_accent(COVER_URL, right=True)
        FOREGROUND_COLOR = self.invert(BACKGROUND_COLOR)

        if len(TITLE_TEXT) > 25: TITLE_TEXT = TITLE_TEXT[0:25] + "..."
        if len(SUBTITLE_TEXT) > 35: SUBTITLE_TEXT = SUBTITLE_TEXT[0:35] + "..."
        if len(DESC_TEXT) > 45: DESC_TEXT = DESC_TEXT[0:45] + "..."

        TITLE_SIZE = TITLE_FONT.getsize(TITLE_TEXT)
        SUBTITLE_SIZE = SUBTITLE_FONT.getsize(SUBTITLE_TEXT)
        DESC_SIZE = DESC_FONT.getsize(DESC_TEXT)
        WIDTH = max([TITLE_SIZE[0], SUBTITLE_SIZE[0], DESC_SIZE[0]]) + 270
        
        if WIDTH < 500:
            WIDTH = 500

        MARGIN_LEFT = 220
        MARGIN_RIGHT = WIDTH - 20
        MARGIN_TOP = 20

        MAIN = Image.new(mode="RGB", color=BACKGROUND_COLOR, size=(WIDTH, 200))
        DRAW = ImageDraw.Draw(MAIN)

        if SPOTIFY and spt["has_duration"]:
            SEEK = round(round((t.now() - spt["created"]).total_seconds())/round(spt["duration"].total_seconds())*100)
            STR_CURRENT = strftime('%H:%M:%S', gmtime(round((t.now() - spt["created"]).total_seconds())))
            STR_END = strftime('%H:%M:%S', gmtime(round(spt["duration"].total_seconds())))
            DURATION_LEFT_SIZE = DRAW.textsize(STR_END, font=SUBTITLE_FONT)[0]

            DRAW.rectangle([(MARGIN_LEFT, MARGIN_TOP + 100), (MARGIN_RIGHT, MARGIN_TOP + 120)], fill=tuple(map(lambda x: x - 25, BACKGROUND_COLOR)))
            DRAW.rectangle([(MARGIN_LEFT, MARGIN_TOP + 100), ((SEEK / 100 * (MARGIN_RIGHT - MARGIN_LEFT)) + MARGIN_LEFT, MARGIN_TOP + 120)], fill=FOREGROUND_COLOR)
            DRAW.text((MARGIN_LEFT, MARGIN_TOP + 130), STR_CURRENT, font=SUBTITLE_FONT, fill=FOREGROUND_COLOR)
            DRAW.text((MARGIN_RIGHT - DURATION_LEFT_SIZE, MARGIN_TOP + 130), STR_END, font=SUBTITLE_FONT, fill=FOREGROUND_COLOR)

        DRAW.text((MARGIN_LEFT, MARGIN_TOP), TITLE_TEXT, font=TITLE_FONT, fill=FOREGROUND_COLOR)
        DRAW.text((MARGIN_LEFT, MARGIN_TOP + 38), SUBTITLE_TEXT, font=SUBTITLE_FONT, fill=FOREGROUND_COLOR)
        DRAW.text((MARGIN_LEFT, MARGIN_TOP + 65), DESC_TEXT, font=DESC_FONT, fill=FOREGROUND_COLOR)

        MAIN.paste(COVER, (0, 0))
        
        return self.buffer(MAIN)
    
    def profile(self, username, avatar, details, after):
        # yanderedev was here
        ava, ava_col = self.buffer_from_url(avatar).resize((100, 100)), [(i['r'], i['g'], i['b']) for i in self.get_multiple_accents(avatar)]
        font, smolfont, smolerfont = self.get_font('NotoSansDisplay-Bold', 50, otf=True), self.get_font('NotoSansDisplay-Bold', 20, otf=True), self.get_font('NotoSansDisplay-Bold', 15, otf=True)
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
        bal = details['wallet']+" bobux"
        draw.rectangle([(margin_left, 180), (margin_right, 240)], fill=ava_col[8])
        res_text = self.wrap_text(details['desc'], (margin_right - 180) - 2, smolfont)
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
        if after is not None:
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
            draw.text((margin_left + 2, 349), after['delta']+" bobux left before reaching next rank ("+after['nextrank']+")", font=smolerfont, fill=self.invert(ava_col[6]))
        main = self.add_corners(main, 25)
        return self.buffer(main)
    
    def evol(self, url):
        ava, img = self.buffer_from_url(url).resize((77, 69)), self.get_image("evol.jpg")
        img.paste(ava, (255, 175))
        return self.buffer(img)
    
    def disconnected(self, msg):
        im = self.get_image('disconnected.png')
        draw, myFont = ImageDraw.Draw(im), self.get_font('Minecraftia-Regular', 16)
        w, h = myFont.getsize(msg)
        W, H = im.size
        draw.text(((W-w)/2,336), msg, font=myFont, fill="white")
        return self.buffer(im)
    
    def ruin(self, ava):
        im = self.get_image('destroyimg.png')
        av = self.buffer_from_url(ava)
        av.paste(im, (0,0), im)
        return self.buffer(av)
    
    def serverstats(self, guild):
        start = "https://quickchart.io/chart?c="
        data1 = [
            str(len([i for i in guild.members if i.status.value.lower()=='online'])),
            str(len([i for i in guild.members if i.status.value.lower()=='idle'])),
            str(len([i for i in guild.members if i.status.value.lower()=='dnd'])),
            str(len([i for i in guild.members if i.status.value.lower()=='offline']))
        ]
        img1 = "{type:'pie',data:{labels:['Online', 'Idle', 'Do not Disturb', 'Offline'], datasets:[{data:["+data1[0]+", "+data1[1]+", "+data1[2]+", "+data1[3]+"]}]}}"
        img = self.buffer_from_url(start+encode_uri(img1))
        w, h = img.size
        cnv = Image.new(mode='RGB', size=(w, h), color=(255, 255, 255))
        cnv.paste(img, (0, 0), img)
        return self.buffer(cnv)
    
    def lookatthisgraph(self, url):
        img = self.buffer_from_url(url).resize((741, 537)).rotate(20)
        bg = self.get_image('graph.png')
        canvas = Image.new(mode='RGB', size=(1920, 1080), color=(0,0,0))
        canvas.paste(img, (833, 365))
        canvas.paste(bg, (0, 0), bg)
        return self.buffer(canvas)
    
    def squidwardstv(self, avatar):
        cnv = Image.new(mode='RGB', size=(1088, 720), color=(0, 0, 0))
        img = self.get_image('squidwardstv.png')
        ava = self.buffer_from_url(avatar).resize((577, 467))
        cnv.paste(ava.rotate(-27), (381, 125))
        cnv.paste(img, (0, 0), img)
        return self.buffer(cnv)
    
    def waifu(self, avatar):
        cnv = Image.new(mode='RGB', size=(450, 344), color=(0, 0, 0))
        img = self.get_image('waifu.png')
        ava = self.buffer_from_url(avatar).resize((131, 162))
        cnv.paste(ava.rotate(-20), (112, 182))
        cnv.paste(img, (0, 0), img)
        return self.buffer(cnv)
    
    def ifunny(self, avatar):
        avatar, watermark = self.buffer_from_url(avatar).resize((545, 481)), self.get_image('ifunny.png')
        avatar.paste(watermark, (0, 0), watermark)
        return self.buffer(avatar)
        
    def wasted(self, avatar):
        avatar, wasted = self.buffer_from_url(avatar).resize((240, 240)), self.get_image('wasted.png').resize((240, 240))
        try:
            red = Image.new(mode='RGB', size=(240, 240), color=(255, 0, 0))
            avatar = Image.blend(avatar, red, alpha=0.4)
        except ValueError:
            pass
        avatar.paste(wasted, (0, 0), wasted)
        return self.buffer(avatar)
    
    def ifearnoman(self, url, url2):
        avpic = self.buffer_from_url(url)
        avpic2 = self.buffer_from_url(url2)
        template = self.get_image('ifearnoman.jpg')
        template.paste(avpic.resize((173, 159)), (98, 28))
        template.paste(avpic.resize((114, 109)), (60, 536))
        template.paste(avpic.resize((139, 145)), (598, 549))
        template.paste(avpic2.resize((251, 249)), (262, 513))
        data = self.buffer(template)
        return data
    
    def simpletext(self, text):
        image = Image.new(mode='RGB',size=(5+(len(text)*38)+5, 80) ,color=(255, 255, 255))
        self.drawtext(ImageDraw.Draw(image), self.get_font('consola', 60), text, 10, 10, "black")
        data = self.buffer(image)
        return data
    
    def baby(self, ava):
        avatar = self.buffer_from_url(ava)
        canvas = Image.new(mode='RGB',size=(728, 915) ,color=(0, 0, 0))
        baby = self.get_image("baby.png")
        avatar = avatar.resize((382, 349))
        avatar = avatar.rotate(50)
        canvas.paste(avatar, (203, 309))
        canvas.paste(baby, (0, 0), baby)
        data = self.buffer(canvas)
        return data
    
    def art(self, ava):
        image = self.get_image('art.png')
        cnv, pic = Image.new(mode='RGB', size=(1364, 1534), color=(0,0,0)), self.buffer_from_url(ava)
        cnv.paste(pic.resize((315, 373)), (927, 94))
        cnv.paste(pic.resize((318, 375)), (925, 861))
        cnv.paste(image, (0, 0), image)
        return self.buffer(cnv)
    
    def resize(self, url, x, y):
        pic = self.buffer_from_url(url)
        pic = pic.resize((x, y))
        data = self.buffer(pic)
        return data
    
    def urltoimage(self, url):
        get_re = get(url)
        if "oops" in get_re.text:
            raise send_error_message("Error: Please input a valid image. `"+get_re.text.split(',"why":"')[1].split('"}')[0]+"`")
            print("ERROR: "+get_re.text)
        return BytesIO(get_re.content)
    
    def smallURL(self, url):
        image = self.buffer_from_url(url)
        size = list(image.size)
        pic = image.resize((round(size[0]/4), round(size[1]/4)))
        data = self.buffer(pic)
        return data
    
    def gif2png(self, url):
        img = self.buffer_from_url(url)
        img.seek(0)
        return self.buffer(img)
    
class GifGenerator:
    
    def __init__(self, assetpath, fontpath):
        self.buffer_from_url = buffer_from_url
        self.assetpath = assetpath
        self.fontpath = fontpath
        self.triggered_text = Image.open(f"{assetpath}/triggered.jpg")
        self.triggered_red = Image.new(mode="RGBA", size=(216, 216), color=(255, 0, 0, 100))
        self.triggered_bg = Image.new(mode="RGBA", size=(216, 216), color=(0, 0, 0, 0))
        
        self.ussr_frames = []
        for frame in ImageSequence.Iterator(Image.open(f"{assetpath}/ussr.gif")):
            self.ussr_frames.append(frame.convert("RGB"))
        self.ussr_frames_size = len(self.ussr_frames)
    
    def mask_circle(self, im):
        bigsize = (im.size[0] * 3, im.size[1] * 3)
        mask = Image.new('L', bigsize, 0)
        draw = ImageDraw.Draw(mask) 
        draw.ellipse((0, 0) + bigsize, fill=255)
        mask = mask.resize(im.size, Image.ANTIALIAS)
        im.putalpha(mask)
    
    def bufferGIF(self, images, duration, transparent=False):
        arr = BytesIO()
        if transparent:
            images[0].save(arr, "GIF", transparency=255, save_all=True, append_images=images[1:], duration=duration, loop=0, disposal=2)
        else:
            images[0].save(arr, "GIF", save_all=True, append_images=images[1:], duration=duration, loop=0)
        arr.seek(0)
        return arr

    def drawtext(self, draw, thefont, text, x, y, col):
        draw.text((x, y), text, fill =col, font=thefont, align ="left")

    def get_image(self, imageName):
        return Image.open(f'{self.assetpath}/{imageName}')

    def get_font(self, fontname, size, otf=False):
        ext = 'ttf' if not otf else 'otf'
        return ImageFont.truetype(f'{self.fontpath}/{fontname}.{ext}', size)

    def hitler(self, pic):
        thegif = self.get_image("hitler.gif")
        av, images = self.buffer_from_url(pic).resize((79, 103)), []
        size = thegif.size
        for i in range(thegif.n_frames):
            cnv = Image.new('RGB', size=size, color=(0,0,0))
            thegif.seek(i)
            cnv.paste(thegif, (0,0))
            if i > 29:
                images.append(cnv)
                continue
            try:
                trans = av.convert('RGBA')
                cnv.paste(trans, (206, 30), trans)
            except: cnv.paste(av, (206, 30))
            images.append(cnv)
        return self.bufferGIF(images, 1.2)
    
    def worship(self, pic):
        im = self.buffer_from_url(pic).resize((127, 160))
        gi = self.get_image('worship.gif')
        images = []
        for i in range(gi.n_frames):
            gi.seek(i)
            cnv = Image.new(mode='RGB', color=(0,0,0), size=gi.size)
            cnv.paste(gi, (0,0))
            try: cnv.paste(im, (303, 7), im)
            except: cnv.paste(im, (303, 7))
            images.append(cnv)
        return self.bufferGIF(images, 15)

    def flip(self, pic):
        im = self.buffer_from_url(pic).resize((400,400))
        inv_im = ImageOps.flip(im)
        speed, images = [3,6,13,25,50,100,200,399], []                                                                                                                                               
        for i in range(len(speed)*2):
            stretch = speed[i] if i < len(speed) else speed[::-1][i-len(speed)]
            image = im if i < len(speed) else inv_im
            cnv = Image.new(mode='RGB', size=(400, 400), color=(0,0,0))
            cnv.paste(image.resize((400, 400-stretch)), (0, round(stretch/2)))
            images.append(cnv)
        images += images[::-1]
        return self.bufferGIF(images, 20, transparent=True)
        
    def crazy_frog_dance(self, pic, metadata):
        im = self.get_image('crazyfrog.gif')
        ava = self.buffer_from_url(pic)
        size, images = im.size, []
        for i in range(im.n_frames):
            im.seek(i)
            ava_size = tuple(map(lambda a: int(a), metadata[i].split(';')[0].split(',')))
            placement = tuple(map(lambda a: int(a), metadata[i].split(';')[1].split(',')))
            cnv = Image.new(mode='RGB', size=size, color=(0,0,0))
            cnv.paste(im.convert('RGB'), (0,0))
            cnv.paste(ava.resize(placement), ava_size)
            images.append(cnv)
        return self.bufferGIF(images, 5)

    def destroy_computer(self, pic, metadata):
        data = self.get_image('rage.gif')
        ava = self.buffer_from_url(pic).resize((40, 40))
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
        gif_template = self.get_image('explosion.gif')
        ava, images, size = self.buffer_from_url(pic).resize((61, 62)), [], gif_template.size
        for i in range(gif_template.n_frames):
            canvas = Image.new(mode='RGB', color=(0,0,0), size=size)
            canvas.paste(gif_template, (0,0))
            gif_template.seek(i)
            if i < 7: canvas.paste(ava, (183, 143))
            images.append(canvas)
        return self.bufferGIF(images, 3)

    def rotate(self, pic, change_mode=False):
        image = self.buffer_from_url(pic).resize((216, 216))
        frames = []
        i = 1
        while i < 360:
            frames.append(image.rotate(i))
            i += 8
        return self.bufferGIF(frames, 30, transparent=True)
    
    def triggered(self, pic):
        reference = self.buffer_from_url(pic).resize((226, 226))
        frames = []

        for i in range(100):
            background = self.triggered_bg.copy()
            background.paste(reference.copy(), (random.randint(-5, 5) - 5, random.randint(-5, 5) - 5))
            background.paste(self.triggered_red, (0, 0), self.triggered_red)
            background.paste(self.triggered_text.copy(), (random.randint(-5, 5) - 5, 177))
            frames.append(background)
        return self.bufferGIF(frames, 30)

    def communist(self, url):
        ava = self.buffer_from_url(url).resize((200, 200)).convert("RGB")
        total_frame = []
        
        for frame in range(self.ussr_frames_size):
            opacity = frame/self.ussr_frames_size
            res = Image.blend(ava, self.ussr_frames[frame], opacity)
            total_frame.append(res)
        return self.bufferGIF(total_frame, 15)
    
    def giffromURL(self, url, compress):
        mygif = self.buffer_from_url(url)
        frames = []
        for i in range(mygif.n_frames):
            mygif.seek(i)
            if compress: frames.append(mygif.resize((216, 216))) ; continue
            frames.append(mygif)
        data = self.bufferGIF(frames, 5)
        return data