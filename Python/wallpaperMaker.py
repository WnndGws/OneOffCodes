'''
Add quote selected from text file over images in a folder
'''

from PIL import Image, ImageDraw, ImageFont
# get an image
base = Image.open('/home/wynand/Downloads/b807c2282ab0a491bd5c5c1051c6d312_rP0kQjJ.jpg').convert('RGBA')

# make a blank image for the text, initialized to transparent text color
txt = Image.new('RGBA', base.size, (255, 255, 255, 0))

# get a font
fnt = ImageFont.truetype('/usr/share/fonts/TTF/Arsenal-Regular.ttf', 90)
# get a drawing context
d = ImageDraw.Draw(txt)

# draw text, half opacity
d.text((10, 10), "Hello", font=fnt, fill=(255, 255, 255, 128))
# draw text, full opacity
d.text((10, 60), "World", font=fnt, fill=(255, 255, 255, 255))

out = Image.alpha_composite(base, txt)

out.show()
