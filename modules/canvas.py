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
from os import listdir, getenv
__import__("sys").path.append(__import__("os").path.abspath("./framework"))
from numpy import zeros, uint8
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
            self.templates[image] = Image.open(f"{assetpath}/{image}")

    def mask_circle(self, im):
        bigsize = (im.size[0] * 3, im.size[1] * 3)
        mask = Image.new('L', bigsize, 0)
        draw = ImageDraw.Draw(mask)
        draw.ellipse((0, 0) + bigsize, fill=255)
        mask = mask.resize(im.size, Image.ANTIALIAS)
        im.putalpha(mask)
        mask.close()

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

    async def _process_message_box(self, text, font, content=False):
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
        if not res: return text
        return "\n".join(res)

    def buffer(self, data, webp=False):
        arr = BytesIO()
        data.save(arr, format='PNG' if (not webp) else 'WEBP')
        arr.seek(0)
        data.close()
        return arr

    async def get_color_accent(self, ctx, url, right=False):
        res = Smart_ColorThief(ctx, url)
        res = await res.get_color(right=right)
        return res[:3]

    async def gradient(self, color_left, color_right):
        if color_right:
            main = Image.new("RGB", (1000, 500), color=color_right)
        array = zeros([500, 1000, 4], dtype=uint8)
        for y in range(1000):
            arr = [color_left[0], color_left[1], color_left[2], round((1000 - y)/1000 * 255)]
            for x in range(500):
                array[x, y] = arr
        image_overlay = Image.fromarray(array)
        if not color_right:
            return self.buffer(image_overlay)
        main.paste(image_overlay, (0, 0), image_overlay)
        return self.buffer(main)

    def get_multiple_accents(self, image):
        b = BytesIO(get(image).content)
        return list(map(lambda i: {
            'r': i[0], 'g': i[1], 'b': i[2]
        }, ColorThief(b).get_palette(color_count=10)))

    async def geometry_dash_icons(self, name):
        GD_FORMS = ('cube', 'ship', 'ball', 'ufo', 'wave', 'robot', 'spider')
        forms = [self.buffer_from_url(f"https://gdbrowser.com/icon/{name}?form={i}") for i in GD_FORMS]
        width = sum(map(lambda i: i.width, forms)) + (len(GD_FORMS) * 25) + 25
        curs = 25
        main = Image.new(mode="RGBA", size=(width, 250), color=(0, 0, 0, 0))
        for i in forms:
            main.paste(i, (curs, round((main.height - i.height) / 2)))
            curs += (i.width + 25)
        del forms
        del curs
        return self.buffer(main)

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
        for i in self.wrap_text(text, 475, font, array=True)[0:5]:
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

    async def among_us(self, ctx, url):
        bg = self.templates['among_us.png'].copy()
        ava = self.buffer_from_url(url).resize((240, 228))
        col = await self.get_color_accent(ctx, url)
        cnv = Image.new(mode='RGBA', size=(512, 512), color=(0,0,0,0))
        draw = ImageDraw.Draw(cnv)
        draw.rectangle([(0, 0), (512, 512)], fill=col)
        cnv.paste(bg, (0,0), bg)
        anothercnv = Image.new(mode='RGB', size=(512, 512), color=(0,0,0))
        anothercnv.paste(ava, (47, 129))
        anothercnv.paste(cnv, (0, 0), cnv)
        bg.close()
        cnv.close()
        return self.buffer(anothercnv)

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

    async def imagetoASCII(self, url):
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
    
    async def imagetoASCII_picture(self, url):
        font = self.get_font("consola", 11)
        image = Image.new(mode='RGB', size=(602, 523), color=(0, 0, 0))
        draw = ImageDraw.Draw(image)
        string = await self.imagetoASCII(url)
        draw.text((0, 0), string, font=font, fill=(255, 255, 255))
        return self.buffer(image)

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
    
    async def simpletext(self, text):
        font = self.get_font('consola', 60)
        image = Image.new(mode='RGB', size=(font.getsize(text)[0] + 20, 80),color=(255, 255, 255))
        self.drawtext(ImageDraw.Draw(image), font, text, 10, 10, "black")
        del font
        return self.buffer(image, webp=True)

    async def resize(self, url, x, y):
        return self.buffer(self.buffer_from_url(url).resize((x, y)))
    
    async def gif2png(self, url):
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
        
    def get_font(self, fontname, size, otf=False):
        ext = 'ttf' if not otf else 'otf'
        return ImageFont.truetype(f'{self.fontpath}/{fontname}.{ext}', size)

    async def death_star(self, pic):
        gif_template = Image.open(f'{self.assetpath}/explosion.gif')
        ava, images, size = self.buffer_from_url(pic).resize((61, 62)), [], gif_template.size
        for i in range(gif_template.n_frames):
            canvas = Image.new(mode='RGB', color=(0,0,0), size=size)
            canvas.paste(gif_template, (0,0))
            gif_template.seek(i)
            if i < 7: canvas.paste(ava, (183, 143))
            images.append(canvas)
        gif_template.close()
        del gif_template
        return self.bufferGIF(images, 3)

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
            background.paste(reference.copy(), (random.randint(-5, 5) - 5, random.randint(-5, 5) - 5))
            background.paste(self.triggered_red, (0, 0), self.triggered_red)
            background.paste(self.triggered_text.copy(), (random.randint(-5, 5) - 5, 177))
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
    
    async def giffromURL(self, url, compress):
        mygif = self.buffer_from_url(url)
        frames = []
        for i in range(mygif.n_frames):
            mygif.seek(i)
            if compress: frames.append(mygif.resize((216, 216))) ; continue
            frames.append(mygif)
        data = self.bufferGIF(frames, 5)
        return data