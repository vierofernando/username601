from PIL import Image, ImageFont, ImageDraw, GifImagePlugin, ImageOps, ImageFilter
from io import BytesIO
from datetime import datetime as t
import username601 as myself
from requests import get
import random

def getFont(fontpath, fontname, size): return ImageFont.truetype(f'{fontpath}{fontname}.ttf', size)
def getImage(assetpath, imageName): return Image.open(f'{assetpath}{imageName}')
def imagefromURL(url, stream=False): return Image.open(BytesIO(get(url, stream=stream).content))
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
def invert(tupl):
    x,y,z = tupl
    x,y,z = abs(x-255), abs(y-255), abs(z-255)
    return (x,y,z)
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
        self.drawtext = drawtext
        self.invert = invert
    
    def get_palette(self, data):
        font = self.getFont(self.fontpath, 'Minecraftia-Regular', 30) 
        main = Image.new(mode='RGB', size=(1800, 500), color=(0, 0, 0))
        draw, loc = ImageDraw.Draw(main), 0
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
        cnv.paste(av, obj['pos'])
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
    
    def spotify(self, person, message):
        spt, template = person.activity, self.getImage(self.assetpath, 'spotify-template.png')
        draw = ImageDraw.Draw(template)
        ava, start = self.imagefromURL(spt.album_cover_url).resize((275, 276)), self.getSongString(spt.created_at, t.now())
        template.paste(ava, (0, 62))
        percentage = round(round((t.now() - spt.created_at).total_seconds())/round(spt.duration.total_seconds())*100)
        duration = ':'.join(str(spt.duration).split(':')[1:10])[:-7]
        self.drawProgressBar(draw, percentage)
        draw.text((15, 20), f'{person.name} is listening to', fill="white", font = self.getFont(self.fontpath, 'GothamBook', 30), align ="left")
        draw.text((15, 350), spt.title, fill="white", font = self.getFont(self.fontpath, 'GothamBold', 30), align ="left")
        draw.text((15, 395), spt.album, fill="white", font = self.getFont(self.fontpath, 'GothamBook', 15), align ="left")
        draw.text((15, 378), 'by '+myself.dearray(spt.artists), fill="white", font = self.getFont(self.fontpath, 'GothamBook', 15), align ="left")
        draw.text((15, 439), start, fill="white", font = self.getFont(self.fontpath, 'GothamBook', 15), align ="left")
        draw.text((485-self.getFont(self.fontpath, 'GothamBook', 15).getsize(duration)[0], 439), duration, fill="white", font = self.getFont(self.fontpath, 'GothamBook', 15), align="right")
        return self.buffer(template)
    
    def profile(self, url, user, details):
        avatar = self.imagefromURL(url).resize((253, 250))
        template = self.getImage(self.assetpath, 'template.png')
        draw = ImageDraw.Draw(template)
        draw.text((295,60), user.name, fill='white', font=self.getFont(self.fontpath, 'Helvetica', 80), align ="left")
        draw.text((295,140), f"ID: {user.id}", fill='white', font=self.getFont(self.fontpath, 'Helvetica', 30), align ="left")
        draw.text((295,180), "Rank: "+details['rank'], fill='white', font=self.getFont(self.fontpath, 'Helvetica', 30), align ="left")
        draw.text((295,220), "Global Rank: "+details['global'], fill='white', font=self.getFont(self.fontpath, 'Helvetica', 30), align ="left")
    
        draw.text((156,348), "Joined since "+details['joined'], fill='white', font=self.getFont(self.fontpath, 'Helvetica', 30), align ="left")
        draw.text((156,388), "User number "+details['number'], fill='white', font=self.getFont(self.fontpath, 'Helvetica', 30), align ="left")
    
        draw.text((156,477), "Wallet balance: "+details['wallet']+" Diamonds", fill='white', font=self.getFont(self.fontpath, 'Helvetica', 30), align ="left")
        draw.text((156,517), "Bank balance: "+details['bank']+" Diamonds", fill='white', font=self.getFont(self.fontpath, 'Helvetica', 30), align ="left")
        draw.text((156,608), details['desc'], fill='white', font=self.getFont(self.fontpath, 'Helvetica', 54), align ="left")
        canvas = Image.new(mode='RGB', size=template.size, color=(0,0,0))
        canvas.paste(avatar, (32, 42))
        canvas.paste(template, (0, 0), template)
        return self.buffer(canvas)
    
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
    
    def servercard(self, link, icon, name, date, author, humans, bots, channels, roles, boosters, tier, online):
        image = self.getImage(self.assetpath, 'card.jpg')
        servericon, draw = self.imagefromURL(icon), ImageDraw.Draw(image)
        image.paste(servericon, (1195, 115))
        self.drawtext(draw, self.getFont(self.fontpath, 'Whitney-Medium', 60), name, 30, 100, 'white')
        self.drawtext(draw, self.getFont(self.fontpath, 'Whitney-Medium', 40), 'Created in '+date+' by '+author, 30, 170, 'white')
        self.drawtext(draw, self.getFont(self.fontpath, 'Whitney-Medium', 60), humans, 130, 265, 'white')
        self.drawtext(draw, self.getFont(self.fontpath, 'Whitney-Medium', 60), bots, 480, 265, 'white')
        self.drawtext(draw, self.getFont(self.fontpath, 'Whitney-Medium', 60), channels+' Channels', 650, 265, 'black')
        self.drawtext(draw, self.getFont(self.fontpath, 'Whitney-Medium', 60), roles+' Roles', 650, 340, 'black')
        self.drawtext(draw, self.getFont(self.fontpath, 'Whitney-Medium', 60), boosters+' boosters', 1000, 265, 'black')
        self.drawtext(draw, self.getFont(self.fontpath, 'Whitney-Medium', 60), 'Level '+tier, 1000, 340, 'black')
        self.drawtext(draw, self.getFont(self.fontpath, 'Whitney-Medium', 50), online+' online', 90, 360, 'black')
        return self.buffer(image)
    
    def usercard(self, this):
        bg = self.getImage(self.assetpath, 'card_{}.png'.format(this.status.value))
        canvas = Image.new(mode='RGB', size=bg.size, color=(0,0,0))
        ava = self.imagefromURL(str(this.avatar_url).replace('.webp?size=1024', '.png?size=512')).resize((189, 190))
        canvas.paste(ava, (299, 12))
        canvas.paste(bg, (0, 0), bg)
        self.drawtext(ImageDraw.Draw(canvas), self.getFont(self.fontpath, 'Whitney-Medium', 50), this.name, 13, 13, 'black')
        self.drawtext(ImageDraw.Draw(canvas), self.getFont(self.fontpath, 'Whitney-Medium', 30), '#'+str(this.discriminator), 203, 111, 'black')
        self.drawtext(ImageDraw.Draw(canvas), self.getFont(self.fontpath, 'consola', 25), str(this.id), 13, 66, 'black')
        self.drawtext(ImageDraw.Draw(canvas), self.getFont(self.fontpath, 'Whitney-Medium', 20), 'Hoist role: '+str(this.roles[::-1][0].name), 14, 168, 'black')
        return self.buffer(canvas)
    
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
            cnv.paste(im, (303, 7))
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