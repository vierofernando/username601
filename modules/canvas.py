from PIL import Image, ImageFont, ImageDraw, GifImagePlugin, ImageOps, ImageFilter
import io
from sys import path
path.append('/home/runner/hosting601/modules')
from datetime import datetime as t
import username601 as myself
import requests
import random

# BIGGIE FONTS, CODE STYLED LIKE MY PYGAME GAME LMAO
class Fonts:
    helvetica_large = ImageFont.truetype(r'/home/runner/hosting601/assets/fonts/Helvetica.ttf', 50)
    helvetica_medium = ImageFont.truetype(r'/home/runner/hosting601/assets/fonts/Helvetica.ttf', 40)
    comicsans_medium = ImageFont.truetype(r'/home/runner/hosting601/assets/fonts/comic.ttf', 40)
    consolas_small = ImageFont.truetype(r'/home/runner/hosting601/assets/fonts/consola.ttf', 25)
    consolas =  ImageFont.truetype(r'/home/runner/hosting601/assets/fonts/consola.ttf', 60)
    whitney_tinier =  ImageFont.truetype(r'/home/runner/hosting601/assets/fonts/Whitney-Medium.ttf', 20)
    whitney_tiny =  ImageFont.truetype(r'/home/runner/hosting601/assets/fonts/Whitney-Medium.ttf', 30)
    whitney_small =  ImageFont.truetype(r'/home/runner/hosting601/assets/fonts/Whitney-Medium.ttf', 40)
    whitney_medium =  ImageFont.truetype(r'/home/runner/hosting601/assets/fonts/Whitney-Medium.ttf', 50)
    whitney_large =  ImageFont.truetype(r'/home/runner/hosting601/assets/fonts/Whitney-Medium.ttf', 60)
    roboto_bold_medium = ImageFont.truetype(r'/home/runner/hosting601/assets/fonts/Roboto-Bold.ttf', 32)

# LIMITS THE CHARACTER
def limitify(raw, linelimit, maxlimit):
    text = ''
    for i in range(0, len(raw)):
        if len(text.split('\n'))>maxlimit:
            text = text[:-1]
            break
        if i>2:
            if i%(linelimit-4)==0:
                text += '\n'
        text += list(raw)[i]
    return text

def compile(data):
    arr = io.BytesIO()
    data.save(arr, format='PNG')
    arr.seek(0)
    return arr

def presentationMeme(text, link):
    image = Image.open(r'{}'.format(link))
    text = limitify(text, 20, 5)
    draw = ImageDraw.Draw(image)
    draw.text((115, 55), text, fill ="black", font = Fonts.helvetica_medium, align ="left")  
    data = compile(image)
    return data

def imagefromURL(url):
    response = requests.get(url)
    image = Image.open(io.BytesIO(response.content))
    return image

def blur(url):
    im = imagefromURL(url).filter(ImageFilter.BLUR)
    return compile(im)

def glitch(url):
    img = imagefromURL(url).resize((200, 200))
    p = img.load()
    for i in range(img.width):
        if random.randint(0, 1)==1:
            size = random.randint(0, img.height)
            for j in range(img.height):
                getloc = i+size
                if getloc >= img.width: getloc -= img.width
                p[i, j] = img.getpixel((getloc, j))
    return compile(img)
def imagetoASCII(url):
    im = imagefromURL(url).resize((300, 300)).rotate(90).convert('RGB')
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

def Helvetica(size):
    return ImageFont.truetype(r'/home/runner/hosting601/assets/fonts/Helvetica.ttf', int(size))

def Gotham(size, bold=False):
    if not bold: return ImageFont.truetype(r'/home/runner/hosting601/assets/fonts/GothamBook.ttf', size)
    return ImageFont.truetype(r'/home/runner/hosting601/assets/fonts/GothamBold.ttf', size)

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

def spotify(person, message):
    spt, template = person.activity, Image.open(r'/home/runner/hosting601/assets/pics/spotify-template.png')
    draw = ImageDraw.Draw(template)
    ava, start = imagefromURL(spt.album_cover_url).resize((275, 276)), getSongString(spt.created_at, t.now())
    template.paste(ava, (0, 62))
    percentage = round(round((t.now() - spt.created_at).total_seconds())/round(spt.duration.total_seconds())*100)
    duration = ':'.join(str(spt.duration).split(':')[1:10])[:-7]
    drawProgressBar(draw, percentage)
    draw.text((15, 20), f'{person.name} is listening to', fill="white", font = Gotham(30), align ="left")
    draw.text((15, 350), spt.title, fill="white", font = Gotham(30, bold=True), align ="left")
    draw.text((15, 395), spt.album, fill="white", font = Gotham(15), align ="left")
    draw.text((15, 378), 'by '+myself.dearray(spt.artists), fill="white", font = Gotham(15), align ="left")
    draw.text((15, 439), start, fill="white", font = Gotham(15), align ="left")
    draw.text((485-Gotham(15).getsize(duration)[0], 439), duration, fill="white", font = Gotham(15), align="right")
    return compile(template)

def profile(url, user, details):
    avatar = imagefromURL(url).resize((253, 250))
    template = Image.open(r'/home/runner/hosting601/assets/pics/template.png')
    draw = ImageDraw.Draw(template)
    draw.text((295,60), user.name, fill='white', font=Helvetica(80), align ="left")
    draw.text((295,140), f"ID: {user.id}", fill='white', font=Helvetica(30), align ="left")
    draw.text((295,180), "Rank: "+details['rank'], fill='white', font=Helvetica(30), align ="left")
    draw.text((295,220), "Global Rank: "+details['global'], fill='white', font=Helvetica(30), align ="left")

    draw.text((156,348), "Joined since "+details['joined'], fill='white', font=Helvetica(30), align ="left")
    draw.text((156,388), "User number "+details['number'], fill='white', font=Helvetica(30), align ="left")

    draw.text((156,477), "Wallet balance: "+details['wallet']+" Diamonds", fill='white', font=Helvetica(30), align ="left")
    draw.text((156,517), "Bank balance: "+details['bank']+" Diamonds", fill='white', font=Helvetica(30), align ="left")
    draw.text((156,608), details['desc'], fill='white', font=Helvetica(54), align ="left")
    canvas = Image.new(mode='RGB', size=template.size, color=(0,0,0))
    canvas.paste(avatar, (32, 42))
    canvas.paste(template, (0, 0), template)
    return compile(canvas)

def evol(url):
    ava, img = imagefromURL(url).resize((77, 69)), Image.open(r"/home/runner/hosting601/assets/pics/evol.jpg")
    img.paste(ava, (255, 175))
    return compile(img)

def app(src, msg):
    im, ava = Image.open(r"/home/runner/hosting601/assets/pics/app.png"), imagefromURL(src).resize((159, 161))
    W, H = im.size
    draw, myFont = ImageDraw.Draw(im), Fonts.roboto_bold_medium
    w, h = myFont.getsize(msg)
    draw.text(((W-w)/2,(H-h)/2+75), msg, font=myFont, fill="white")
    cnv = Image.new(mode='RGB', size=im.size, color=(0,0,0))
    cnv.paste(ava, (88, 31))
    cnv.paste(im, (0, 0), im)
    return compile(cnv)

def ruin(ava):
    im = Image.open('/home/runner/hosting601/assets/pics/destroyimg.png')
    av = imagefromURL(ava)
    av.paste(im, (0,0), im)
    return compile(av)

def hitler(ava):
    ava = imagefromURL(ava).resize((141, 167))
    im = Image.open('/home/runner/hosting601/assets/pics/worse-than-hitler.png')
    im.paste(ava, (46, 31))
    return compile(im)

def serverstats(guild):
    start = "https://quickchart.io/chart?c="
    data1 = [
        str(len([i for i in guild.members if i.status.value.lower()=='online'])),
        str(len([i for i in guild.members if i.status.value.lower()=='idle'])),
        str(len([i for i in guild.members if i.status.value.lower()=='dnd'])),
        str(len([i for i in guild.members if i.status.value.lower()=='offline']))
    ]
    img1 = "{type:'pie',data:{labels:['Online', 'Idle', 'Do not Disturb', 'Offline'], datasets:[{data:["+data1[0]+", "+data1[1]+", "+data1[2]+", "+data1[3]+"]}]}}"
    img = imagefromURL(start+myself.urlify(img1))
    w, h = img.size
    cnv = Image.new(mode='RGB', size=(w, h), color=(255, 255, 255))
    cnv.paste(img, (0, 0), img)
    return compile(cnv)

def lookatthisgraph(url):
    img = imagefromURL(url).resize((741, 537)).rotate(20)
    bg = Image.open(r'/home/runner/hosting601/assets/pics/graph.png')
    canvas = Image.new(mode='RGB', size=(1920, 1080), color=(0,0,0))
    canvas.paste(img, (833, 365))
    canvas.paste(bg, (0, 0), bg)
    return compile(canvas)

def squidwardstv(avatar):
    cnv = Image.new(mode='RGB', size=(1088, 720), color=(0, 0, 0))
    img = Image.open(r'/home/runner/hosting601/assets/pics/squidwardstv.png')
    ava = imagefromURL(avatar).resize((577, 467))
    cnv.paste(ava.rotate(-27), (381, 125))
    cnv.paste(img, (0, 0), img)
    return compile(cnv)

def waifu(avatar):
    cnv = Image.new(mode='RGB', size=(450, 344), color=(0, 0, 0))
    img = Image.open(r'/home/runner/hosting601/assets/pics/waifu.png')
    ava = imagefromURL(avatar).resize((131, 162))
    cnv.paste(ava.rotate(-20), (112, 182))
    cnv.paste(img, (0, 0), img)
    return compile(cnv)

def ifunny(avatar):
    avatar, watermark = imagefromURL(avatar).resize((545, 481)), Image.open(r'/home/runner/hosting601/assets/pics/ifunny.png')
    avatar.paste(watermark, (0, 0), watermark)
    return compile(avatar)
    
def wasted(avatar):
    avatar, wasted = imagefromURL(avatar).resize((240, 240), Image.ANTIALIAS), Image.open(r'/home/runner/hosting601/assets/pics/wasted.png').resize((240, 240))
    try:
        red = Image.new(mode='RGB', size=(240, 240), color=(255, 0, 0))
        avatar = Image.blend(avatar, red, alpha=0.4)
    except ValueError:
        pass
    avatar.paste(wasted, (0, 0), wasted)
    return compile(avatar)

def ifearnoman(url, url2):
    avpic = imagefromURL(url)
    avpic2 = imagefromURL(url2)
    template = Image.open(r'/home/runner/hosting601/assets/pics/ifearnoman.jpg')
    template.paste(avpic.resize((173, 159), Image.ANTIALIAS), (98, 28))
    template.paste(avpic.resize((114, 109), Image.ANTIALIAS), (60, 536))
    template.paste(avpic.resize((139, 145), Image.ANTIALIAS), (598, 549))
    template.paste(avpic2.resize((251, 249), Image.ANTIALIAS), (262, 513))
    data = compile(template)
    return data

def firstwords(text, link):
    image = Image.open(r'{}'.format(link))
    draw = ImageDraw.Draw(image)
    raw = limitify(text, 28, 2)
    draw.text((150, 20), list(raw)[0]+'..'+list(raw)[0]+'...', fill ="black", font = Fonts.helvetica_medium, align ="left")  
    draw.text((35, 420), raw, fill ="black", font = Fonts.comicsans_medium, align ="left")
    data = compile(image)
    return data

def limit(raw):
    text = ''
    for i in range(0, len(raw)):
        if len(raw.split('\n'))>1:
            break
        if i>2:
            if i%50==0:
                text += '\n'
        text += list(raw)[i]
    return text

def drawtext(draw, thefont, text, x, y, col):
    draw.text((x, y), text, fill =col, font=thefont, align ="left") 

def simpletext(text):
    image = Image.new(mode='RGB',size=(5+(len(text)*38)+5, 80) ,color=(255, 255, 255))
    drawtext(ImageDraw.Draw(image), Fonts.consolas, text, 10, 10, "black")
    data = compile(image)
    return data

def servercard(link, icon, name, date, author, humans, bots, channels, roles, boosters, tier, online):
    image = Image.open(r'{}'.format(link))
    response = requests.get(icon)
    servericon = Image.open(io.BytesIO(response.content))
    image.paste(servericon, (1195, 115))
    drawtext(ImageDraw.Draw(image), Fonts.whitney_large, name, 30, 100, 'white')
    drawtext(ImageDraw.Draw(image), Fonts.whitney_small, 'Created in '+date+' by '+author, 30, 170, 'white')
    drawtext(ImageDraw.Draw(image), Fonts.whitney_large, humans, 130, 265, 'white')
    drawtext(ImageDraw.Draw(image), Fonts.whitney_large, bots, 480, 265, 'white')
    drawtext(ImageDraw.Draw(image), Fonts.whitney_large, channels+' Channels', 650, 265, 'black')
    drawtext(ImageDraw.Draw(image), Fonts.whitney_large, roles+' Roles', 650, 340, 'black')
    drawtext(ImageDraw.Draw(image), Fonts.whitney_large, boosters+' boosters', 1000, 265, 'black')
    drawtext(ImageDraw.Draw(image), Fonts.whitney_large, 'Level '+tier, 1000, 340, 'black')
    drawtext(ImageDraw.Draw(image), Fonts.whitney_medium, online+' online', 90, 360, 'black')
    data = compile(image)
    return data

def putimage(url, name, resx, resy, posx, posy):
    image = Image.open('/home/runner/hosting601/assets/pics/'+name+'.jpg')
    pic = imagefromURL(url)
    pic = pic.resize((resx, resy), Image.ANTIALIAS)
    image.paste(pic, (posx, posy))
    data = compile(image)
    return data

def usercard(this):
    bg = Image.open('/home/runner/hosting601/assets/pics/card_{}.png'.format(this.status.value))
    canvas = Image.new(mode='RGB', size=bg.size, color=(0,0,0))
    ava = imagefromURL(str(this.avatar_url).replace('.webp?size=1024', '.png?size=512')).resize((189, 190))
    canvas.paste(ava, (299, 12))
    canvas.paste(bg, (0, 0), bg)
    drawtext(ImageDraw.Draw(canvas), Fonts.whitney_medium, this.name, 13, 13, 'black')
    drawtext(ImageDraw.Draw(canvas), Fonts.whitney_tiny, '#'+str(this.discriminator), 203, 111, 'black')
    drawtext(ImageDraw.Draw(canvas), Fonts.consolas_small, str(this.id), 13, 66, 'black')
    drawtext(ImageDraw.Draw(canvas), Fonts.whitney_tinier, 'Hoist role: '+str(this.roles[::-1][0].name), 14, 168, 'black')
    return compile(canvas)

def put_transparent(avatar, name, overallx, overally, avatarw, avatarh, avatarx, avatary):
    door = Image.open('/home/runner/hosting601/assets/pics/'+name+'.png')
    canvas = Image.new(mode='RGB',size=(overallx, overally) ,color=(0, 0, 0))
    avatar = imagefromURL(avatar)
    avatar = avatar.resize((avatarw, avatarh))
    canvas.paste(avatar, (avatarx, avatary))
    canvas.paste(door, (0, 0), door)
    data = compile(canvas)
    return data

def baby(ava):
    avatar = imagefromURL(ava)
    canvas = Image.new(mode='RGB',size=(728, 915) ,color=(0, 0, 0))
    baby = Image.open("/home/runner/hosting601/assets/pics/baby.png")
    avatar = avatar.resize((382, 349))
    avatar = avatar.rotate(50)
    canvas.paste(avatar, (203, 309))
    canvas.paste(baby, (0, 0), baby)
    data = compile(canvas)
    return data

def art(ava):
    image = Image.open(r'/home/runner/hosting601/assets/pics/art.png')
    cnv, pic = Image.new(mode='RGB', size=(1364, 1534), color=(0,0,0)), imagefromURL(ava)
    cnv.paste(pic.resize((315, 373)), (927, 94))
    cnv.paste(pic.resize((318, 375)), (925, 861))
    cnv.paste(image, (0, 0), image)
    return compile(cnv)

def f(ava):
    avatar = imagefromURL(ava)
    bg = Image.open(r'/home/runner/hosting601/assets/pics/f.png')
    canvas = Image.new(mode='RGB',size=(960, 540) ,color=(0, 0, 0))
    avatar = avatar.resize((82, 111))
    canvas.paste(avatar, (361, 86))
    canvas.paste(bg, (0, 0), bg)
    data = compile(canvas)
    return data

def resize(url, x, y):
    pic = imagefromURL(url)
    pic = pic.resize((x, y), Image.ANTIALIAS)
    data = compile(pic)
    return data

class gif:
    def compilegif(images, duration, optimize=False):
        arr = io.BytesIO()
        images[0].save(arr, "GIF", save_all=True, append_images=images[1:], optimize=optimize, duration=duration, loop=0)
        arr.seek(0)
        return arr
    def flip(pic):
        im = imagefromURL(pic).resize((400,400))
        inv_im = ImageOps.flip(im)
        speed, images = [3,6,13,25,50,100,200,399], []
        for i in range(len(speed)*2):
            stretch = speed[i] if i < len(speed) else speed[::-1][i-len(speed)]
            image = im if i < len(speed) else inv_im
            cnv = Image.new(mode='RGB', size=(400, 400), color=(0,0,0))
            cnv.paste(image.resize((400, 400-stretch)), (0, round(stretch/2)))
            images.append(cnv)
        images += images[::-1]
        return gif.compilegif(images, 5)
    def death_star(pic):
        gif_template = Image.open(r'/home/runner/hosting601/assets/pics/explosion.gif')
        ava, images, size = imagefromURL(pic).resize((61, 62)), [], gif_template.size
        for i in range(gif_template.n_frames):
            canvas = Image.new(mode='RGB', color=(0,0,0), size=size)
            canvas.paste(gif_template, (0,0))
            gif_template.seek(i)
            if i < 7: canvas.paste(ava, (183, 143))
            images.append(canvas)
        return gif.compilegif(images, 3)

    def rotate(pic):
        image = imagefromURL(pic)
        image = image.resize((216, 216), Image.ANTIALIAS)
        images, num = [], 0
        while num<360:
            images.append(image.rotate(num))
            num += 5
        data = gif.compilegif(images, 5)
        return data
    
    def triggered(pic, increment):
        image = imagefromURL(pic)
        image = image.resize((216, 216), Image.ANTIALIAS)
        red = Image.new(mode='RGB', size=(216, 216), color=(255, 0, 0))
        image = Image.blend(image, red, alpha=0.25)
        text = Image.open('/home/runner/hosting601/assets/pics/triggered.jpg')

        canvas = Image.new(mode='RGB',size=image.size ,color=(0, 0, 0))
        images, num = [], 0
        while num<100:
            canvas.paste(image, (random.randint(-increment, increment), random.randint(-increment, increment)))
            images.append(canvas)
            canvas.paste(text, (random.randint(-increment, increment), (216-39)+(random.randint(-increment, increment))))
            canvas = Image.new(mode='RGB',size=image.size ,color=(0, 0, 0))
            num += 5
        data = gif.compilegif(images, 3)
        return data

    def communist(comrade):
        flag = Image.open('/home/runner/hosting601/assets/pics/blyat.jpg').convert('RGB')
        user = imagefromURL(comrade).resize((216, 216)).convert('RGB')
        images = []
        opacity = float(0)
        while int(opacity)!=1:
            newimage = Image.blend(user, flag, opacity)
            images.append(newimage)
            opacity += 0.05
        extras = 0

        while extras<100:
            image = flag
            drawtext(ImageDraw.Draw(image), Fonts.whitney_tiny, 'COMMUNIST', 216/2-86, 10, 'white')
            drawtext(ImageDraw.Draw(image), Fonts.whitney_tiny, 'CONFIRMED', 216/2-84, 170, 'white')
            images.append(image)
            extras += 1
        data = gif.compilegif(images, 5)
        return data
    
    def giffromURL(url, compress):
        mygif = imagefromURL(url)
        frames = []
        for i in range(0, mygif.n_frames):
            mygif.seek(i)
            if compress: frames.append(mygif.resize((216, 216), Image.ANTIALIAS)) ; continue
            frames.append(mygif)
        data = gif.compilegif(frames, 5)
        return data

def urltoimage(url):
    image = imagefromURL(url)
    data = compile(image)
    return data

def smallURL(url):
    image = imagefromURL(url)
    size = list(image.size)
    pic = image.resize((round(size[0]/4), round(size[1]/4)), Image.ANTIALIAS)
    data = compile(pic)
    return data

def gif2png(url):
    img = imagefromURL(url)
    img.seek(0)
    return compile(img)

def memegen(url):
    image = imagefromURL(url)
    area = (0, 20, list(image.size)[0], list(image.size)[1]-12)
    cropped_img = image.crop(area)
    data = compile(cropped_img)
    return data
