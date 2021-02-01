from twemoji_parser import TwemojiParser, emoji_to_url
from .colorthief import Smart_ColorThief
from discord import ActivityType, File
from wand.image import Image as _Image
from wand.image import Color as _Color
from .lego import apply_color_overlay
from aiohttp import ClientSession
from claptcha import Claptcha
from itertools import chain
from random import randint
from json import loads
from io import BytesIO
from time import time
from PIL import *
import gc

class ImageClient:
    DISASTER_GIRL_PATH = "./assets/pics/disaster_girl.png"
    AMONG_US_PATH = "./assets/pics/among_us.png"
    AMONG_US_MASK_FR = Image.open(AMONG_US_PATH.replace("among_us.png", "among_us_mask.png")).convert("L")
    AMONG_US_MASK_BG = Image.open(AMONG_US_PATH.replace("among_us.png", "among_us_overlay.png")).convert("L")
    GRADIENT_MASK = Image.open("./assets/pics/gradient_mask.png").convert("L")
    ASCII_RANGES = ((33, ':'), (65, '-'), (97, '='), (129, '+'), (160, '*'), (192, '#'), (224, '%'), (256, '@'))
    EXPLOSION_GIF = list(ImageSequence.Iterator(Image.open("./assets/pics/explosion.gif")))
    GD_FORMS = ('cube', 'ship', 'ball', 'ufo', 'wave', 'robot', 'spider')

    def __init__(self, client):
        self.http = client.http
        
    
    def wrap_text(self, text: str, font, max_width: int) -> str:
        """ Wraps a text. """
        res_text = []
        current_text = ""

        for char in list(text):
            if font.getsize(current_text)[0] < max_width:
                current_text += char
                continue
            res_text.append(current_text)
            current_text = ""
        
        if not res_text:
            return text
        elif current_text:
            res_text.append(current_text)
        
        return "\n".join(res_text)


    def _resolve_svg(self, byte, pil: bool = False):
        image = _Image(blob=byte)
        if not pil:
            return image
        res = BytesIO(image.make_blob("png"))
        image.close()
        del image
        return Image.open(res)
    
    
    async def image_from_URL(self, url: str):
        """ Fetches an image from a URL to PIL.Image.Image. """
        res = await self.http._HTTPClient__session.get(url)
        byte_data = await res.read()
        if res.headers.get("content-type", "").startswith("image/svg") or res.headers.get("Content-Type", "").startswith("image/svg"):
            return self._resolve_svg(byte_data, True)
        
        image = Image.open(BytesIO(byte_data))
        del byte_data, res
        if url.startswith("https://twemoji.maxcdn.com/v/latest/72x72/"):
            image = image.convert("RGBA")
        return image

    
    async def wand_from_URL(self, url: str):
        """ Fetches an image from a URL to Wand.Image. """
        res = await self.http._HTTPClient__session.get(url)
        byte_data = await res.read()
        if res.headers.get("content-type", "").startswith("image/svg") or res.headers.get("Content-Type", "").startswith("image/svg"):
            return self._resolve_svg(byte_data)
        
        res = _Image(blob=byte_data)
        del byte_data
        return res

    
    def wand_save(self, image) -> BytesIO:
        """ Saves a wand image. """
        buffer = BytesIO(image.make_blob("png"))
        image.close()
        del image
        gc.collect()
        return buffer
        
    
    def save(self, image) -> BytesIO:
        """ Saves an image as a buffer. """
        buffer = BytesIO()
        image.save(buffer, format="png")
        image.close()
        del image
        buffer.seek(0)
        gc.collect()
        return buffer
    

    async def geometry_dash_icons(self, username: str) -> BytesIO:
        """ Gets the Geometry Dash icons. """
        images = []
        for forms in ImageClient.GD_FORMS:
            image = await self.image_from_URL(f"https://gdbrowser.com/icon/{username}?form={forms}")
            images.append(image)
        width = sum(map(lambda i: i.width, images)) + (len(ImageClient.GD_FORMS) * 25) + 25
        
        main = Image.new(mode="RGBA", size=(width, 250), color=(0, 0, 0, 0))
        curs = 25
        for image in images:
            main.paste(image, (curs, (main.height - image.height) // 2))
            curs += (image.width + 25)
        
        del images, width, curs
        return self.save(main)
    
    async def distort(self, url: str, image_path: str, edges: tuple):
        """ Distorts an image as such. """
        base = Image.open(image_path)
        img = await self.wand_from_URL(url)
        img.background_color = _Color('black')
        img.virtual_pixel = "background"
        img.resize(*base.size)
        img.distort('perspective', list(chain.from_iterable(chain.from_iterable(zip(*edges)))))
        res = Image.open(BytesIO(img.make_blob("png")))
        res.paste(base, (0, 0), base)
        base.close()
        del img, base
        gc.collect()
        return self.save(res)
    
    
    async def explode_animated(self, url: str, reversed: bool = False):
        """ The explosion but animated. """
        temp_images = []
        for i in range(1, 11):
            im = await self.wand_from_URL(url)
            im.resize(112, 112)
            im.implode(amount=(i * 0.15 if reversed else -i))
            im_ = Image.open(BytesIO(im.make_blob("png")))
            temp_images.extend([im_.copy()] * 3)
            im_.close()
            del im_, im
        temp_images += ImageClient.EXPLOSION_GIF
        buffer = BytesIO()
        temp_images[0].save(buffer, "GIF", save_all=True, append_images=temp_images[1:], duration=3, loop=0, optimize=False)
        buffer.seek(0)
        del temp_images
        gc.collect()
        return buffer
    
    
    def __get_ascii_char(self, s):
        for n, c in ImageClient.ASCII_RANGES:
            if s < n: return c
    
    
    async def asciify(self, url: str) -> str:
        """ Asciifies an image. """
        im = await self.image_from_URL(url)
        im = im.resize((100, 40))
        
        if im.mode != "L":
            im = im.convert("L")
        
        pixels = im.load()
        s = ""
        
        for x in range(40):
            for y in range(100):
                s += self.__get_ascii_char(pixels[y, x])
            s += "\n"
            
        del pixels, im
        return s
    
    
    async def colorify(self, url: str, color: tuple) -> BytesIO:
        """ Colourifies an image. """
        wand_image = await self.wand_from_URL(url)
        wand_image.colorize(color=f"rgb{color}", alpha="rgb(50%, 50%, 50%)")
        return self.wand_save(wand_image)
    
    
    async def blend(self, url1: str, url2: str) -> BytesIO:
        """ Blends two images together. """
        image1 = await self.image_from_URL(url1)
        image2 = await self.image_from_URL(url2)

        if image1.mode != "RGB":
            image1 = image1.convert("RGB")
        if image2.mode != "RGB":
            image2 = image2.convert("RGB")
        if image1.size != image2.size:
            image1 = image1.resize((512, 512))
            image2 = image2.resize((512, 512))

        return self.save(Image.blend(image1, image2, alpha=0.5))

    
    async def resize(self, url: str, width: int, height: int) -> BytesIO:
        """ Resizes an image. """
        image = await self.image_from_URL(url)
        return self.save(image.resize((width, height)))

    
    async def pixelate(self, url: str, amount: int = 32) -> BytesIO:
        if amount not in [16, 32, 64, 128]:
            amount = 32
        img = await self.image_from_URL(url)
        img_small = img.resize((amount, amount), resample=Image.BILINEAR)
        result = img_small.resize(img.size, Image.NEAREST)
        del img_small, amount
        return self.save(result)

    
    async def implode(self, url: str, amount: int) -> tuple:
        """ Implodes an image. Can be used to explode as well. """
        wand_image = await self.wand_from_URL(url)
        wand_image.implode(amount=amount)
        return self.wand_save(wand_image)
    
    
    async def swirl(self, url: str, degree: int) -> tuple:
        """ Swirls an image. The intensity can be changed using the degree parameter. """
        wand_image = await self.wand_from_URL(url)
        wand_image.swirl(degree=degree)
        return self.wand_save(wand_image)

    
    async def charcoal(self, url: str) -> tuple:
        """ Adds a charcoal filter to the image. """
        wand_image = await self.wand_from_URL(url)
        wand_image.charcoal(radius=1.5, sigma=0.5)
        return self.wand_save(wand_image)
    
    
    async def sketch(self, url: str) -> tuple:
        """ Adds a sketch filter to the image. """
        wand_image = await self.wand_from_URL(url)
        wand_image.transform_colorspace("gray")
        wand_image.sketch(0.5, 0.0, 98.0)
        return self.wand_save(wand_image)
    
    
    async def edge(self, url: str) -> tuple:
        """ Adds a edge filter to the image. """
        wand_image = await self.wand_from_URL(url)
        wand_image.transform_colorspace('gray')
        wand_image.edge(radius=1)
        return self.wand_save(wand_image)
    
    
    async def emboss(self, url: str) -> tuple:
        """ Adds a emboss filter to the image. """
        wand_image = await self.wand_from_URL(url)
        wand_image.transform_colorspace('gray')
        wand_image.emboss(radius=3.0, sigma=1.75)
        return self.wand_save(wand_image)
    
    
    async def spread(self, url: str) -> tuple:
        """ Spreads the image pixels. """
        wand_image = await self.wand_from_URL(url)
        wand_image.spread(radius=8.0)
        return self.wand_save(wand_image)

    
    async def wave(self, url: str, amount: int) -> tuple:
        """ Adds a wavy effect to the image. """
        wand_image = await self.wand_from_URL(url)
        wand_image.wave(amplitude=wand_image.height / (amount * 5), wave_length=wand_image.width / amount)
        return self.wand_save(wand_image)

    
    async def disaster_girl(self, url: str) -> BytesIO:
        """ Generates a disaster girl picture in front of your picture. """
        image = await self.image_from_URL(url)
        girl = Image.open(ImageClient.DISASTER_GIRL_PATH)
        h = image.height // 2
        w = h * 3 // 4
        
        girl = girl.resize((w, h))
        image.paste(girl, (image.width - w + 1, image.height - h + 1), girl)
        girl.close()
        del girl, w, h
        gc.collect()
        return self.save(image)

    
    async def oil(self, url: str) -> BytesIO:
        """ Adds a oil effect to the image. """
        wand_image = await self.wand_from_URL(url)
        wand_image.oil_paint(10, 8)
        return self.wand_save(wand_image)

    
    async def noise(self, url: str) -> BytesIO:
        """ Adds a noise to the image. """
        wand_image = await self.wand_from_URL(url)
        wand_image.noise("laplacian", attenuate=100.0)
        return self.wand_save(wand_image)

    
    async def solarize(self, url: str) -> BytesIO:
        """ Adds a solarize filter to the image. """
        wand_image = await self.wand_from_URL(url)
        wand_image.solarize(threshold=0.5 * wand_image.quantum_range)
        return self.wand_save(wand_image)

    
    async def glitch(self, url: str):
        """ Glitches an image. """
        image = await self.image_from_URL(url)
        assert image.width in range(50, 1500), "Image width must be around the range of 50 and 1500 pixels"
        assert image.height in range(50, 1500), "Image height must be around the range of 50 and 1500 pixels"
        pixel_list = image.load()
        
        for h in range(image.height):
            r = randint(1, 30)
            for w in range(image.width):
                a = w + (r - image.width) if (w + r) >= image.width else (w + r)
                pixel_list[w, h] = pixel_list[a, h]
        del pixel_list
        return self.save(image)

    
    async def among_us(self, url: str) -> BytesIO:
        """ Creates an among us image from an avatar. """
        crewmate = Image.open(ImageClient.AMONG_US_PATH)
        image = await self.image_from_URL(url)
        image = image.resize((240, 228))
        colorthief = Smart_ColorThief(None, image)
        color = await colorthief.get_color(right=True)
        if (sum(color) < 50):
            color = (50, 50, 50)
        
        background = Image.new("RGB", (512, 512), color)
        foreground = background.copy()
        background.paste(crewmate, (0, 0), crewmate)
        
        background.putalpha(ImageClient.AMONG_US_MASK_FR)
        foreground.paste(image, (47, 129))
        foreground.paste(background, (0, 0), background)
        
        foreground.putalpha(ImageClient.AMONG_US_MASK_BG)
        
        image.close()
        crewmate.close()
        background.close()
        del image, crewmate, color, colorthief, background
        gc.collect()
        return self.save(foreground)

    
    async def gradient(self, rgb_1: tuple, rgb_2: tuple) -> BytesIO:
        """ Creates a gradient from two RGBs. """
        background_right = Image.new("RGB", (400, 200), rgb_2)
        background_right.putalpha(ImageClient.GRADIENT_MASK)
        background_left = Image.new("RGB", (400, 200), rgb_1)
        background_left.paste(background_right, (0, 0), background_right)
        background_right.close()
        del background_right
        gc.collect()
        
        return self.save(background_left)

    
    async def dissolve(self, url: str) -> BytesIO:
        """ Dissolves an image. """
        chance = (lambda: (0 if randint(0, 2) == 2 else 255))
        mask_arr = []
        image = await self.image_from_URL(url)
        mask = Image.new("L", image.size)
        
        for _ in range(image.width * image.height):
            mask_arr.append(chance())
        
        mask.putdata(mask_arr)
        image.putalpha(mask)
        del mask_arr, mask, chance
        
        gc.collect()
        return self.save(image)


    def text(self, text: str) -> BytesIO:
        """ Converts a text to a buffer. """
        font = ImageFont.truetype("./assets/fonts/consola.ttf", 30)
        width, _ = font.getsize(text)
        main = Image.new("RGB", (width + 10, 40), (255, 255, 255))
        draw = ImageDraw.Draw(main)
        draw.text((5, 5), text, font=font, fill="black")
        del draw, width, font
        return self.save(main)


    def captcha(self, text: str) -> BytesIO:
        """ Converts a text to a captcha image. """
        pic = Claptcha(text, "./assets/fonts/consola.ttf")
        bytes = pic.bytes[1]
        del pic
        gc.collect()
        return bytes

class Blur:
    BASIC_BLUR = 0
    GAUSSIAN_BLUR = 1
    MOTION_BLUR = 2
    ROTATIONAL_BLUR = 3

    def __init__(
        self,
        client,
        image_url: str
    ):
        """ Blurs an image. """
        self.image_url = image_url
        self.Image = client.Image
        self._functions = (
            ("blur", {"radius": 0, "sigma": 3}),
            ("gaussian_blur", {"sigma": 3}),
            ("motion_blur", {"radius": 16, "sigma": 8, "angle": -45}),
            ("rotational_blur", {"angle": 5})
        )
        
    async def blur(self, type):
        wand_image = await self.Image.wand_from_URL(self.image_url)
        func, args = self._functions[type]
        getattr(wand_image, func)(**args)
        
        return self.Image.wand_save(wand_image)

    def __del__(self):
        del self.image_url
        del self.Image
        del self._functions

class GDLevel:
    def __init__(
        self,
        ctx,
        level_query: str,
        font_title: str,
        font_other: str
    ):
        
        self.bot = ctx.bot
        self.query = level_query
        self.pusab_big = ImageFont.truetype(font_title, 40)
        self.pusab_smol = ImageFont.truetype(font_title, 30)
        self.pusab_smoler = ImageFont.truetype(font_title, 20)
        self.pusab_tiny = ImageFont.truetype(font_title, 20)
        self.aller = ImageFont.truetype(font_other, 20)
        self.gd_assets = {
        	"main": {
        		"downloads": "https://gdbrowser.com/assets/download.png",
        		"length": "https://gdbrowser.com/assets/time.png",
        		"orbs": "https://gdbrowser.com/assets/orbs.png",
        		"diamonds": "https://gdbrowser.com/assets/diamond.png"
        	},
        	"like": "https://gdbrowser.com/assets/like.png",
        	"dislike": "https://gdbrowser.com/assets/dislike.png"
        }
    
    async def draw(self):
        resp = await self.bot.http._HTTPClient__session.get('https://gdbrowser.com/api/level/' + self.bot.util.encode_uri(self.query))
        data = await resp.json()
        
        levelName = data['name']
        levelAuth = "by "+data['author']
        levelDesc = data['description']
        levelDiff = data['difficulty']
        levelStars = f"{data['stars']:,} stars" if data['stars'] else "No stars"

        main = Image.new('RGB', color=(4, 75, 196), size=(500, 400))
        draw = ImageDraw.Draw(main)
        
        w, _ = self.pusab_big.getsize(levelName)
        W, _ = main.size
        draw.text(((W-w)//2,15), levelName, font=self.pusab_big, stroke_width=2, stroke_fill="black", fill="white")
        w, _ = self.pusab_smol.getsize(levelAuth)
        draw.text(((W-w)//2,50), levelAuth, font=self.pusab_smol, stroke_width=2, stroke_fill="black", fill=(255, 200, 0))
        desc_cursor = 300
        texts, sym_cursor = self.wrap_text(levelDesc, self.aller, 445), 100

        for i in texts.split("\n"):
            w, _ = self.aller.getsize(i)
            draw.text(((W-w)/2, desc_cursor), i, font=self.aller, fill='white')
            desc_cursor += 25

        difficulty = await self.bot.Image.image_from_URL(f"https://gdbrowser.com/difficulty/{data['difficultyFace']}.png")
        difficulty = difficulty.convert("RGBA").resize((75, 75))
        main.paste(difficulty, ((W - 75) // 2 - 100, 100), difficulty)
        w, _ = self.pusab_tiny.getsize(levelDiff)
        draw.text(((W - w)/2 - 100, 180), levelDiff, font=self.pusab_tiny, stroke_width=2, stroke_fill="black")
        w, _ = self.pusab_tiny.getsize(levelStars)
        draw.text(((W - w)/2 - 100, 200), levelStars, font=self.pusab_tiny, stroke_width=2, stroke_fill="black")

        for i in self.gd_assets['main'].keys():
            if not self.gd_assets['main'][i]:
                sym = await self.bot.Image.image_from_URL(self.gd_assets['dislike' if data['disliked'] else 'like'])
                sym = sym.convert("RGBA").resize((25, 25))
                main.paste(sym, ((W-25) // 2 + 75, sym_cursor), sym)
                draw.text(((W-25) // 2 + 105, sym_cursor + 5), f'{data["likes"]:,}', font=self.pusab_smoler, stroke_width=2, stroke_fill="black")
                sym_cursor += 30
                continue
            if i not in data.keys():
                continue
            
            sym = await self.bot.Image.image_from_URL(self.gd_assets['main'][i])
            sym = sym.convert("RGBA").resize((25, 25))
            main.paste(sym, ((W-25) // 2 + 75, sym_cursor), sym)
            draw.text(((W-25) // 2 + 105, sym_cursor + 5), f"{data[i]:,}" if str(data[i]).isnumeric() else data[i], font=self.pusab_smoler, stroke_width=2, stroke_fill="black")
            sym_cursor += 30
            del sym
        
        res = self.save(main)
        del (
            main,
            draw,
            W,
            w,
            difficulty,
            texts,
            sym_cursor,
            desc_cursor,
            levelName,
            levelAuth,
            levelDesc,
            levelDiff,
            levelStars,
            resp,
            data
        )
        gc.collect()

        return res
    
    def __del__(self):
        del (
            self.pusab_big,
            self.pusab_smol,
            self.pusab_smoler,
            self.pusab_tiny,
            self.aller,
            self.query,
            self.bot,
            self.gd_assets
        )
        gc.collect()

class ProfileCard:
    def __init__(self, ctx, member, profile: dict, font_path: str):
        self.bal = profile
        self.user = member
        self.ctx = ctx

        # measure the width
        self.big_font = ImageFont.truetype(font_path, 30)
        self.smol_font = ImageFont.truetype(font_path, 18)
        self.width = self.big_font.getsize(self.user.display_name)[0] + 230

        if self.width < 700:
            self.width = 700

    def __wrap_desc(self):
        if len(self.bal["desc"]) < 20:
            return self.bal["desc"]

        text = []
        current_text = ""

        for char in list(self.bal["desc"]):
            if (len(current_text) < 20) or (self.smol_font.getsize(current_text)[0] < (self.main.width - 410)):
                current_text += char
                continue
            text.append(current_text)
            current_text = ""
        
        if not text:
            return self.bal["desc"]
        elif bool(current_text):
            text.append(current_text)
        
        return "\n".join(text)

    async def draw(self):
        # make the image
        if not self.bal.get("color"):
            colorthief = Smart_ColorThief(self.ctx, str(self.user.avatar_url_as(format="png", size=128)))
            self.background_color = await colorthief.get_color(right=True)
            del colorthief
        else:
            self.background_color = tuple([int(i) for i in self.bal["color"].split(",")])

        self.foreground_color = (0, 0, 0) if ((not isinstance(self.background_color, int)) and ((sum(self.background_color) // 3) > 127)) else (255, 255, 255)
        self.main = Image.new(mode="RGB", size=(self.width, 190), color=self.background_color)
        self.d = ImageDraw.Draw(self.main)
        self.parser = TwemojiParser(self.main, session=self.ctx.bot.http._HTTPClient__session)
        self.lower_brightness = (lambda x: tuple(map(lambda y: y - x, self.background_color)))

        # draw the rectangles
        self.d.rectangle([(170, 20), (self.main.width - 20, 70)], fill=self.lower_brightness(30))
        self.d.rectangle([(170, 70), (370, 170)], fill=self.lower_brightness(60))
        self.d.rectangle([(370, 70), (self.main.width - 20, 170)], fill=self.lower_brightness(90))
        
        # get the description
        description = self.__wrap_desc()

        # draw those text
        self.d.text((190, 20), self.user.display_name, font=self.big_font, fill=self.foreground_color)
        await self.parser.draw_text((190, 80), f"💸 {self.bal['bal']:,}", font=self.smol_font, fill=self.foreground_color, with_url_check=False)
        await self.parser.draw_text((190, 110), f"🏦 {self.bal['bankbal']:,}", font=self.smol_font, fill=self.foreground_color, with_url_check=False)
        await self.parser.draw_text((380, 80), description, font=self.smol_font, fill=self.foreground_color)

        # get avatar
        avatar = await self.ctx.bot.Image.image_from_URL(str(self.user.avatar_url_as(format="png", size=128)))
        avatar = avatar.resize((150, 150))

        # paste the avatar
        if avatar.mode == "RGBA":
            self.main.paste(avatar, (20, 20), avatar)
        else:
            self.main.paste(avatar, (20, 20))

        b = BytesIO()
        self.main.save(b, format="png")
        b.seek(0)
        self.main.close()

        return b

    async def close(self):
        # close the parser
        await self.parser.close(close_session=False)

        # delete the garbage and collect it (ew)
        del (
            self.main,
            self.d,
            self.background_color,
            self.foreground_color,
            self.lower_brightness,
            self.big_font,
            self.smol_font,
            self.bal,
            self.user,
            self.parser,
            self.width,
            self.ctx
        )
        gc.collect()

class UserCard:
    def __init__(self, ctx, member, font_path: str):
        self.bot = ctx.bot
        self.ctx = ctx
        self.user = member
        self.font_path = font_path
        self.flags = {
            "nitro": "https://discordia.me/uploads/badges/nitro_badge.png",
            "booster": "https://erisly.com/assets/img/premium/boost.cb45e94.png",
            "badges": {
                "bug_hunter": "https://discordia.me/uploads/badges/bug_hunter_badge.png",
                "early_supporter": "https://discordia.me/uploads/badges/early_supporter_badge.png",
                "hypesquad_balance": "https://discordia.me/uploads/badges/balance_badge.png",
                "hypesquad_bravery": "https://discordia.me/uploads/badges/bravery_badge.png",
                "hypesquad_brilliance": "https://discordia.me/uploads/badges/brilliance_badge.png",
                "partner": "https://discordia.me/uploads/badges/partner_badge.png",
                "staff": "https://discordia.me/uploads/badges/staff_badge.png",
                "verified_bot_developer": "https://discordia.me/uploads/badges/verified_developer_badge.png"
            }
        }
        self._activity_prefix = {
            ActivityType.listening: "Listening to ",
            ActivityType.competing: "Competing in ",
            ActivityType.watching:  "Watching ",
            ActivityType.playing:   "Playing ",
            ActivityType.streaming: "Streaming ",
            ActivityType.custom:    None,
            ActivityType.unknown:   None
        }
        
        self._activity_prefix = (None, "Playing ", "Streaming ", "Listening to ", "Watching ", "", "CO")
    
    async def get_status_image(self):
        dict_data = self.user.activity.to_dict()
        
        if dict_data.get("emoji"):
            if dict_data["emoji"].get("id"):
                return f'https://cdn.discordapp.com/emojis/{dict_data["emoji"]["id"]}'
            emoji_url = await emoji_to_url(str(self.user.activity.emoji), session=self.bot.http._HTTPClient__session)
            if emoji_url.startswith("http"):
                return emoji_url
            return
        elif hasattr(self.user.activity, "album_cover_url"):
            return self.user.activity.album_cover_url
        elif dict_data.get("assets"):
            return f'https://cdn.discordapp.com/app-assets/{dict_data["application_id"]}/{dict_data["assets"]["small_image"]}.png'
        return
    
    def get_status_name(self):
        prefix = self._activity_prefix[self.user.activity.type.value + 1]
        if prefix is None:
            return "<unknown status>"
        elif not prefix:
            return "<custom activity>"
        
        return prefix + getattr(self.user.activity, "name", "<unknown>")
    
    def get_font(self, size: int):
        return ImageFont.truetype(self.font_path, size)

    async def send(self):
        # user avatar
        avatar = await self.bot.Image.image_from_URL(str(self.user.avatar_url_as(format="png", size=128)))
        avatar = avatar.resize((150, 150))
        
        # configure stuff
        _thief = Smart_ColorThief(self.ctx, str(self.user.avatar_url_as(format="png", size=128)))
        background_color = await _thief.get_color(right=True)
        foreground_color = (0, 0, 0) if (sum(background_color) // 3) > 128 else (255, 255, 255)
        lower_brightness = (lambda x: tuple(map(lambda y: y - x, background_color)))
        big_font =  self.get_font(40)
        smol_font = self.get_font(25)
        tiny_font = self.get_font(20)
        title_size = big_font.getsize(self.user.display_name)[0]
        description = f"Created at {self.bot.util.timestamp(self.user.created_at)}" + "\n" + f"Joined at {str(self.user.joined_at)[:-7]} (Position: {self.bot.util.join_position(self.ctx.guild, self.user):,}/{self.ctx.guild.member_count:,})"
        del _thief
        
        # measure the width for the image
        width = max([
            title_size + tiny_font.getsize(f"#{self.user.discriminator}")[0] + 45,
            smol_font.getsize_multiline(description)[0] + 40
        ]) + 190
        
        # declare the main object
        main = Image.new(mode="RGB", size=(width, (230 if self.user.activity else 190)), color=background_color)
        draw = ImageDraw.Draw(main)
        
        # paste the avatar, if it's RGBA, paste it with transparent
        if avatar.mode == "RGBA":
            main.paste(avatar, (20, 20), avatar)
        else:
            main.paste(avatar, (20, 20))
        
        # draw main two rectangles
        draw.rectangle([(170, 20), (main.width - 20, 80)], fill=lower_brightness(20))
        draw.rectangle([(170, 80), (main.width - 20, 170)], fill=lower_brightness(40))
        
        # draw main text
        draw.text((190, 15), self.user.display_name, font=big_font, fill=foreground_color)
        draw.text((195 + title_size, 38), f"#{self.user.discriminator}", font=tiny_font, fill=foreground_color)
        draw.text((190, 85), description, font=smol_font, fill=foreground_color)

        # check if user has activity, then create another section for the activity
        if self.user.activity:
            url = await self.get_status_image()
            color = None if url else (255, 255, 255)
            
            if url:
                status_image = await self.bot.Image.image_from_URL(url)
                status_image = status_image.resize((40, 40)).convert("RGBA") if url.startswith("https://twemoji.maxcdn.com/") else status_image.resize((40, 40))
                _thief = Smart_ColorThief(self.ctx, url)
                activity_color = await _thief.get_color(right=True)
                
                draw.rectangle([(20, 170), (main.width - 20, 210)], fill=activity_color)
                color = (0, 0, 0) if ((sum(activity_color) // 3) > 128) else (255, 255, 255)
                
                if status_image.mode == "RGBA":
                    main.paste(status_image, (20, 170), status_image)
                else:
                    main.paste(status_image, (20, 170))
                del status_image, _thief, activity_color
            else:
                draw.rectangle([(20, 170), (main.width - 20, 210)], fill=(0, 0, 0))
            
            draw.text((70 - (0 if url else 40), 170), self.get_status_name(), font=smol_font, fill=color)
            del url, color
        
        # check and draw badges if user has one
        flag_y = main.width - 60
        for flag in self.flags["badges"].keys():
            if not getattr(self.user.public_flags, flag):
                continue
            
            flag_image = await self.bot.Image.image_from_URL(self.flags["badges"][flag])
            flag_image = flag_image.resize((30, 30))
            main.paste(flag_image, (flag_y, 30), flag_image)
            del flag_image
            flag_y -= 35
        
        # add nitro badge to list if user has one
        if self.bot.util.has_nitro(self.ctx.guild, self.user):
            flag_image = await self.bot.Image.image_from_URL(self.flags["nitro"])
            flag_image = flag_image.resize((30, 30))
            main.paste(flag_image, (flag_y, 30), flag_image)
            del flag_image
            flag_y -= 35
        
        # add booster badge to list if user has one
        if self.user in self.ctx.guild.premium_subscribers:
            flag_image = await self.bot.Image.image_from_URL(self.flags["booster"])
            flag_image = flag_image.resize((30, 30))
            main.paste(flag_image, (flag_y, 30), flag_image)
            del flag_image
        
        # save it to a buffer and send it
        b = BytesIO()
        main.save(b, format="png")
        b.seek(0)
        await self.ctx.send(file=File(b, "card.png"))
        
        # delete all the attributes
        del (
            main,
            draw,
            big_font,
            smol_font,
            tiny_font,
            width,
            description,
            lower_brightness,
            background_color,
            foreground_color,
            avatar,
            flag_y,
            self.flags,
            title_size,
            self.user,
            self.bot,
            self.font_path,
            self._activity_prefix,
            self.ctx,
            b
        )
        
        # collect the trash, ew
        gc.collect()

class ServerCard:
    def __init__(self, ctx, font_path: str):
        """ Server Info command thingy """
        self.ctx = ctx
        self._get_font = (lambda x: ImageFont.truetype(font_path, x))
        self._server_tier_urls = [
            "https://vierofernando.is-inside.me/YWs1Qw2q.png",
            "https://vierofernando.is-inside.me/BIe3ccYA.png",
            "https://vierofernando.is-inside.me/2vKUVwwM.png",
            "https://vierofernando.is-inside.me/T0sfEdj1.png"
        ]

    async def draw(self):
        """ draws teh card """
        # commenting everything because codes with comments make it look "tidier" :^)

        # get the guild icon
        server_icon = await self.ctx.bot.Image.image_from_URL(str(self.ctx.guild.icon_url_as(format="png", size=128)) if self.ctx.guild.icon_url else "https://cdn.discordapp.com/embed/avatars/0.png")
        server_icon = server_icon.resize((128, 128))
        _colorthief = Smart_ColorThief(self.ctx, str(self.ctx.guild.icon_url_as(format="png", size=128)) if self.ctx.guild.icon_url else "https://cdn.discordapp.com/embed/avatars/0.png")

        # colors !!!
        background_color = await _colorthief.get_color(right=True)
        foreground_color = (0, 0, 0) if (sum(background_color) // 3) > 128 else (255, 255, 255)
        lower_brightness = (lambda x: tuple(map(lambda h: h - x, background_color)))

        # get the text and font for the image
        big_font = self._get_font(30)
        sub_font = self._get_font(20)
        description = f"Created by {str(self.ctx.guild.owner)} at {self.ctx.bot.util.timestamp(self.ctx.guild.created_at, include_time_past=False)}"

        # configure the image
        width = max([
            big_font.getsize(self.ctx.guild.name)[0] + 50,
            sub_font.getsize(description)[0]
        ]) + 208
        im = Image.new(mode="RGB", size=(width, 168), color=background_color)
        draw = ImageDraw.Draw(im)
        
        # paste the icon
        if server_icon.mode == "RGBA":
            im.paste(server_icon, (20, 20), server_icon)
        else:
            im.paste(server_icon, (20, 20))
        
        # create the rectangles
        draw.rectangle([(148, 20), (im.width - 20, 70)], fill=lower_brightness(50))
        draw.rectangle([(148, 70), (im.width - 20, 148)], fill=lower_brightness(70))

        tier_icon = await self.ctx.bot.Image.image_from_URL(self._server_tier_urls[self.ctx.guild.premium_tier])
        tier_icon = tier_icon.resize((40, 40))
        im.paste(tier_icon, (im.width - 75, 25), tier_icon)

        # draw those goddamn text smh
        draw.text((168, 20), self.ctx.guild.name, fill=foreground_color, font=big_font)
        draw.text((168, 75), description, fill=foreground_color, font=sub_font)
        draw.text((168, 103), f"{self.ctx.guild.member_count:,} members", fill=foreground_color, font=sub_font)
        text_length = sub_font.getsize(f"{self.ctx.guild.premium_subscription_count:,} boosters")[0]
        draw.text((im.width - 40 - text_length, 103), f"{self.ctx.guild.premium_subscription_count:,} boosters", fill=foreground_color, font=sub_font)

        # save to a buffer
        b = BytesIO()
        im.save(b, format="png")
        b.seek(0)

        # delete to free memory
        del (
            im,
            draw,
            width,
            tier_icon,
            server_icon,
            text_length,
            big_font,
            sub_font,
            _colorthief,
            description,
            background_color,
            foreground_color,
            lower_brightness,
            self.ctx,
            self._get_font,
            self._server_tier_urls
        )
        
        # collect those stinky memory garbage
        gc.collect()
        
        # return the buffer, complete !
        return b
