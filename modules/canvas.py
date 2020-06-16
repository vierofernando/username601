from PIL import Image, ImageFont, ImageDraw  
import io

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
    text = limitify(text, linelimit-2, maxlimit)
    draw.text((5, 5), text, fill ="black", font = Fonts.helvetica_large, align ="left") 
    data = compile(image)
    return data

def presentationMeme(text, link):
    image = Image.open(r'{}'.format(link))
    text = limitify(text, 24, 5)
    draw = ImageDraw.Draw(image)
    draw.text((115, 55), text, fill ="black", font = Fonts.helvetica_medium, align ="left")  
    data = compile(image)
    return data

# 32, 2
def firstwords(text, link):
    image = Image.open(r'{}'.format(link))
    draw = ImageDraw.Draw(image)
    raw = limitify(text, 30, 2)
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

def drawtext(draw, text, fontsize, x, y, col):
    draw.text((x, y), text, fill =col, font = ImageFont.truetype(r'/app/assets/fonts/Whitney-Medium.ttf', fontsize)  , align ="left") 

def servercard(link, name, date, author, humans, bots, channels, roles, boosters, tier, online):
    image = Image.open(r'{}'.format(link))
    drawtext(ImageDraw.Draw(image), name, 30, 100, 'white')
    drawtext(ImageDraw.Draw(image), 'Created in '+date+' by '+author, 40, 30, 170, 'white')
    drawtext(ImageDraw.Draw(image), humans, 60, 130, 265, 'white')
    drawtext(ImageDraw.Draw(image), bots, 60, 480, 265, 'white')
    drawtext(ImageDraw.Draw(image), channels+' Channels', 60, 650, 265, 'black')
    drawtext(ImageDraw.Draw(image), roles+' Roles', 60, 650, 340, 'black')
    drawtext(ImageDraw.Draw(image), boosters+' boosters', 60, 1050, 265, 'black')
    drawtext(ImageDraw.Draw(image), 'Level '+tier, 60, 1050, 340, 'black')
    drawtext(ImageDraw.Draw(image), '12391 online', 50, 90, 360, 'black')
    data = compile(image)
    return data