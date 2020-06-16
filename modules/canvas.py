from PIL import Image, ImageFont, ImageDraw  
import io
import requests

# BIGGIE FONTS, CODE STYLED LIKE MY PYGAME GAME LMAO
class Fonts:
    helvetica_large = ImageFont.truetype(r'/app/assets/fonts/Helvetica.ttf', 50)
    helvetica_medium = ImageFont.truetype(r'/app/assets/fonts/Helvetica.ttf', 40)
    comicsans_medium = ImageFont.truetype(r'/app/assets/fonts/comic.ttf', 40)

# LIMITS THE CHARACTER
def limitify(raw, linelimit, maxlimit):
    text = ''
    for i in range(0, len(raw)):
        if len(text.split('\n'))>maxlimit:
            text = text[:-1]
            break
        if i>2:
            if i%linelimit==0:
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

# 32, 2
def firstwords(text, link):
    image = Image.open(r'{}'.format(link))
    draw = ImageDraw.Draw(image)
    raw = limitify(text, 28, 2)
    draw.text((150, 20), list(raw)[0]+'..'+list(raw)[0]+'...', fill ="black", font = Fonts.helvetica_medium, align ="left")  
    draw.text((35, 420), raw, fill ="black", font = Fonts.comicsans_medium, align ="left")
    data = compile(image)
    return data

def limit(text):
    text = ''
    for i in range(0, len(raw)):
        if len(raw.split('\n'))>1:
            break
        if i>2:
            if i%50==0:
                text += '\n'
        text += list(raw)[i]
    return text

def drawtext(draw, fontname, text, fontsize, x, y, col):
    draw.text((x, y), text, fill =col, font = ImageFont.truetype(r'/app/assets/fonts/'+fontname+'.ttf', fontsize)  , align ="left") 

def servercard(link, icon, name, date, author, humans, bots, channels, roles, boosters, tier, online):
    image = Image.open(r'{}'.format(link))
    response = requests.get(icon)
    servericon = Image.open(io.BytesIO(response.content))
    image.paste(servericon, (1195, 115))
    drawtext(ImageDraw.Draw(image),'Whitney-Medium', name, 60, 30, 100, 'white')
    drawtext(ImageDraw.Draw(image),'Whitney-Medium', 'Created in '+date+' by '+author, 40, 30, 170, 'white')
    drawtext(ImageDraw.Draw(image),'Whitney-Medium', humans, 60, 130, 265, 'white')
    drawtext(ImageDraw.Draw(image),'Whitney-Medium', bots, 60, 480, 265, 'white')
    drawtext(ImageDraw.Draw(image),'Whitney-Medium', channels+' Channels', 60, 650, 265, 'black')
    drawtext(ImageDraw.Draw(image),'Whitney-Medium', roles+' Roles', 60, 650, 340, 'black')
    drawtext(ImageDraw.Draw(image),'Whitney-Medium', boosters+' boosters', 60, 1000, 265, 'black')
    drawtext(ImageDraw.Draw(image),'Whitney-Medium', 'Level '+tier, 60, 1000, 340, 'black')
    drawtext(ImageDraw.Draw(image),'Whitney-Medium', online+' online', 50, 90, 360, 'black')
    data = compile(image)
    return data

def headache(text):
    link = './assets/pics/typesofheadache.jpg'
    image = Image.open(r'{}'.format(link))
    x = 330
    total = limit(text)
    if len(text)>15:
        size = 40-(len(text)-15)
        if size<15:
            size = 15
    else:
        size = 40
        x += size*2.5
    x += round(size-(size/0.5)+5)
    drawtext(ImageDraw.Draw(image), text, 'Impact', x, 510, 'black')
    return compile(image)