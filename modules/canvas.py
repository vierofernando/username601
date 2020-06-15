import PIL
import io

# BIGGIE FONTS, CODE STYLED LIKE MY PYGAME GAME LMAO
class Fonts:
    futura = PIL.ImageFont.truetype(r'C:\Users\user\Desktop\Futura Condensed.ttf', 50)  

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
    image = PIL.Image.open(r'{}'.format(src))
    draw = PIL.ImageDraw.Draw(image)
    text = limitify(text, linelimit, maxlimit)
    draw.text((5, 5), text, fill ="black", font = font, align ="left") 
    compile(image)