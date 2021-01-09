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
from random import randint, choice
from os import listdir, getenv
__import__("sys").path.append(__import__("os").path.abspath("./framework"))
from time import strftime, gmtime
from io import BytesIO
from datetime import datetime as t
from colorthief import ColorThief
from framework import Smart_ColorThief
from requests import get

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
    circle.close()
    alpha.close()
    return im

class Painter:

    def __init__(self, assetpath, fontpath, jsondir): # lmao wtf is this
        self.buffer_from_url = buffer_from_url
        self.fontpath = fontpath
        self.gd_assets = json.loads(open(jsondir+'/gd.json', 'r').read())
        self.add_corners = add_corners
        
        # TO BE USED
        self.templates = {}
        for image in listdir(assetpath):
            if image.endswith(".gif"): continue
            elif image.startswith("oreo-"): continue
            elif image.startswith("among_us"): continue
            self.templates[image] = Image.open(f"{assetpath}/{image}")

    def drawtext(self, draw, thefont, text, x, y, col):
        draw.text((x, y), text, fill =col, font=thefont, align ="left")

    def get_font(self, fontname, size, otf=False):
        ext = 'ttf' if not otf else 'otf'
        return ImageFont.truetype(f'{self.fontpath}/{fontname}.{ext}', size)

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

    def buffer(self, data, webp=False):
        arr = BytesIO()
        data.save(arr, format='PNG' if (not webp) else 'WEBP')
        arr.seek(0)
        data.close()
        return arr

    def get_multiple_accents(self, image):
        b = BytesIO(get(image).content)
        return list(map(lambda i: {
            'r': i[0], 'g': i[1], 'b': i[2]
        }, ColorThief(b).get_palette(color_count=10)))

    async def oliy_stretched(self, url):
        image = self.buffer_from_url(url).resize((227, 449))
        oily = self.templates["oliy.png"].copy()
        canvas = Image.new(mode="RGB", size=(739, 1600), color=(0, 0, 0))
        canvas.paste(image, (37, 565))
        canvas.paste(oily, (0, 0), oily)
        image.close()
        oily.close()
        del image, oily
        return self.buffer(canvas)

    async def minecraft_body(self, url, uuid):
        body_3d = self.buffer_from_url(url) # LMAO 420 NICE
        main = Image.new(mode="RGBA", size=(body_3d.width + 420, body_3d.height), color=(0, 0, 0, 0))
        main.paste(body_3d, (0, 0))
        textures = get(f"https://api.minetools.eu/profile/{uuid}").json()["decoded"]["textures"]
        raw_texture = self.buffer_from_url(textures["SKIN"]["url"])
        main.paste(raw_texture.resize((400, 200)), (body_3d.width + 20, 0))
        try:
            cape = self.buffer_from_url(textures["CAPE"]["url"])
            main.paste(cape.resize((400, 400)), (body_3d.width + 20, 220))
        except: pass
        raw_texture.close()
        body_3d.close()
        del raw_texture, body_3d
        return self.buffer(main)

    async def bottom_image_meme(self, image_url, text):
        main = Image.new("RGB", size=(500, 500), color=(255, 255, 255))
        font = self.get_font("Helvetica", 35)
        draw = ImageDraw.Draw(main)
        curs = 5
        for i in self.wrap_text(text, 475, font, array=True)[:5]:
            draw.text((5, curs), i, font=font, fill='black')
            curs += 35
        main.paste(self.buffer_from_url(image_url).resize((500, 300)), (0, 200))
        return self.buffer(main)

    async def color(self, string):
        try: rgb, brightness = ImageColor.getrgb(string), ImageColor.getcolor(string, 'L')
        except: return
        
        _hex = '%02x%02x%02x' % rgb
        main = Image.new(mode='RGB', size=(500, 500), color=rgb)
        try: color_name = get('https://api.alexflipnote.dev/color/'+_hex, headers={"Authorization": getenv("ALEXFLIPNOTE_TOKEN")}).json()['name']
        except: color_name = 'Unknown'
        big_font = self.get_font("Aller", 50)
        medium_font = self.get_font("Aller", 30)
        small_font = self.get_font("Aller", 20)
        draw = ImageDraw.Draw(main)
        draw.text((10, 10), "#" + _hex.upper(), fill=self.invert(rgb), font=big_font)
        draw.text((10, 75), color_name, fill=self.invert(rgb), font=medium_font)
        draw.text((10, 115), f'RGB: {rgb[0]}, {rgb[1]}, {rgb[2]}\nInteger: {rgb[0]*rgb[1]*rgb[2]}\nBrightness: {brightness}', fill=self.invert(rgb), font=small_font)
        return self.buffer(main)

    async def password(self, bad_pass, good_pass):
        im = self.templates['pass.png'].copy()
        font = self.get_font('Helvetica', 25)
        draw = ImageDraw.Draw(im)
        draw.text((42, 80), self.wrap_text(bad_pass, 396, font, array=True)[0], font=font, fill='black')
        draw.text((42, 311), self.wrap_text(good_pass, 396, font, array=True)[0], font=font, fill='black')
        return self.buffer(im)

    async def get_palette(self, temp_data):
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

    async def trans_merge(self, obj):
        av = self.buffer_from_url(obj['url']).resize(obj['size'])
        bg = self.templates[obj['filename'].lower()].copy()
        cnv = Image.new(mode='RGB', color=(0,0,0), size=bg.size)
        try: cnv.paste(av, obj['pos'], av)
        except: cnv.paste(av, obj['pos'])
        cnv.paste(bg, (0,0), bg)
        bg.close()
        av.close()
        return self.buffer(cnv)
    
    async def merge(self, obj):
        av = self.buffer_from_url(obj['url']).resize(obj['size'])
        bg = self.templates[obj['filename'].lower()].copy()
        bg.paste(av, obj['pos'])
        av.close()
        return self.buffer(bg)

    async def disconnected(self, msg):
        im = self.templates['disconnected.png'].copy()
        draw, myFont = ImageDraw.Draw(im), self.get_font('Minecraftia-Regular', 16)
        w, h = myFont.getsize(msg)
        W, H = im.size
        draw.text(((W-w)/2,336), msg, font=myFont, fill="white")
        return self.buffer(im)

    async def ifearnoman(self, url, url2):
        avpic = self.buffer_from_url(url)
        avpic2 = self.buffer_from_url(url2)
        template = self.templates['ifearnoman.jpg'].copy()
        template.paste(avpic.resize((173, 159)), (98, 28))
        template.paste(avpic.resize((114, 109)), (60, 536))
        template.paste(avpic.resize((139, 145)), (598, 549))
        template.paste(avpic2.resize((251, 249)), (262, 513))
        avpic.close()
        avpic2.close()
        return self.buffer(template)

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

    def bufferGIF(self, images, duration, transparent=False):
        arr = BytesIO()
        if transparent:
            images[0].save(arr, "GIF", transparency=255, save_all=True, append_images=images[1:], duration=duration, loop=0, disposal=2)
        else:
            images[0].save(arr, "GIF", save_all=True, append_images=images[1:], duration=duration, loop=0)
        arr.seek(0)
        return arr

    async def rotate(self, pic, change_mode=False):
        image = self.buffer_from_url(pic).resize((216, 216))
        frames = []
        i = 1
        while i < 360:
            frames.append(image.rotate(i))
            i += 8
        return self.bufferGIF(frames, 30, transparent=True)
    
    async def triggered(self, pic):
        reference = self.buffer_from_url(pic).resize((226, 226))
        frames = []

        for i in range(100):
            background = self.triggered_bg.copy()
            background.paste(reference.copy(), (randint(-5, 5) - 5, randint(-5, 5) - 5))
            background.paste(self.triggered_red, (0, 0), self.triggered_red)
            background.paste(self.triggered_text.copy(), (randint(-5, 5) - 5, 177))
            frames.append(background)
        return self.bufferGIF(frames, 30)

    async def communist(self, url):
        ava = self.buffer_from_url(url).resize((200, 200)).convert("RGB")
        total_frame = []
        
        for frame in range(self.ussr_frames_size):
            opacity = frame/self.ussr_frames_size
            res = Image.blend(ava, self.ussr_frames[frame], opacity)
            total_frame.append(res)
        return self.bufferGIF(total_frame, 15)