from PIL import Image, ImageFont, ImageDraw, GifImagePlugin
import io
import requests
import random

# BIGGIE FONTS, CODE STYLED LIKE MY PYGAME GAME LMAO
class Fonts:
    helvetica_large = ImageFont.truetype(r'/app/assets/fonts/Helvetica.ttf', 50)
    helvetica_medium = ImageFont.truetype(r'/app/assets/fonts/Helvetica.ttf', 40)
    comicsans_medium = ImageFont.truetype(r'/app/assets/fonts/comic.ttf', 40)
    consolas_small = ImageFont.truetype(r'/app/assets/fonts/consola.ttf', 25)
    consolas =  ImageFont.truetype(r'/app/assets/fonts/consola.ttf', 60)
    whitney_tinier =  ImageFont.truetype(r'/app/assets/fonts/Whitney-Medium.ttf', 20)
    whitney_tiny =  ImageFont.truetype(r'/app/assets/fonts/Whitney-Medium.ttf', 30)
    whitney_small =  ImageFont.truetype(r'/app/assets/fonts/Whitney-Medium.ttf', 40)
    whitney_medium =  ImageFont.truetype(r'/app/assets/fonts/Whitney-Medium.ttf', 50)
    whitney_large =  ImageFont.truetype(r'/app/assets/fonts/Whitney-Medium.ttf', 60)

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

# COMPILES ALL OF THAT TO THE DISCORD.FILE THINGY
#273
def compile(data):
    arr = io.BytesIO()
    data.save(arr, format='PNG')
    arr.seek(0)
    return arr

def simpleTopMeme(text, src, linelimit, maxlimit):
    image = Image.open(r'{}'.format(src))
    draw = ImageDraw.Draw(image)
    text = limitify(text, linelimit-4, maxlimit)
    draw.text((5, 5), text, fill ="black", font = Fonts.helvetica_large, align ="left") 
    data = compile(image)
    return data

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

def ifearnoman(url, url2):
    avpic = imagefromURL(url)
    avpic2 = imagefromURL(url2)
    template = Image.open(r'/app/assets/pics/ifearnoman.jpg')
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
    image = Image.open('/app/assets/pics/'+name+'.jpg')
    pic = imagefromURL(url)
    pic = pic.resize((resx, resy), Image.ANTIALIAS)
    image.paste(pic, (posx, posy))
    data = compile(image)
    return data

def usercard(this):
    bg = Image.open('/app/assets/pics/card_{}.png'.format(this.status.value))
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
    door = Image.open('/app/assets/pics/'+name+'.png')
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
    baby = Image.open("/app/assets/pics/baby.png")
    avatar = avatar.resize((382, 349))
    avatar = avatar.rotate(50)
    canvas.paste(avatar, (203, 309))
    canvas.paste(baby, (0, 0), baby)
    data = compile(canvas)
    return data

def art(ava):
    image = Image.open(r'/app/assets/pics/art.jpg')
    pic = imagefromURL(ava)
    firpic = pic.resize((152, 174), Image.ANTIALIAS)
    image.paste(firpic, (435, 39))
    secpic = pic.resize((152, 176), Image.ANTIALIAS)
    image.paste(secpic, (440, 379))
    data = compile(image)
    return data

def f(ava):
    avatar = imagefromURL(ava)
    bg = Image.open(r'/app/assets/pics/f.png')
    canvas = Image.new(mode='RGB',size=(680, 383) ,color=(0, 0, 0))
    avatar = avatar.resize((104, 85))
    canvas.paste(avatar, (318, 120))
    canvas.paste(bg, (0, 0), bg)
    data = compile(canvas)
    return data

def resize(url, x, y):
    pic = imagefromURL(url)
    pic = pic.resize((x, y), Image.ANTIALIAS)
    data = compile(pic)
    return data

class gif:
    def compilegif(images, duration):
        arr = io.BytesIO()
        images[0].save(arr, "GIF", save_all=True, append_images=images[1:], optimize=False, duration=duration, loop=0)
        arr.seek(0)
        return arr

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
        red = Image.open('/app/assets/pics/red.jpg')
        image = Image.blend(image, red, alpha=0.25)
        text = Image.open('/app/assets/pics/triggered.jpg')

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
        flag = Image.open('/app/assets/pics/blyat.jpg')
        user = imagefromURL(comrade)
        images = []
        user = user.resize((216, 216))
        opacity = float(0)
        while int(opacity)!=1:
            print(opacity)
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

def memegen(url):
    image = imagefromURL(url)
    area = (0, 20, list(image.size)[0], list(image.size)[1]-12)
    cropped_img = image.crop(area)
    data = compile(cropped_img)
    return data
