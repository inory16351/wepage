import os, sys
from PIL import Image

for f in os.listdir('.'):
    if f.lower().endswith('.jpg'):
        im = Image.open(f)
        print("Filename:", f.encode('unicode_escape').decode('ascii'))
        print("Size:", im.size, "Mode:", im.mode)
        print("Top-left:", im.getpixel((0,0)))
        print("Top-right:", im.getpixel((im.width-1, 0)))
        print("Center:", im.getpixel((im.width//2, im.height//2)))
