import os
from rembg import remove
from PIL import Image

# Find image
target_file = None
for f in os.listdir('.'):
    if f.lower().endswith('.jpg'):
        target_file = f
        break

print("Target found:", target_file is not None)
with open(target_file, 'rb') as inp:
    data = inp.read()
    output = remove(data)
    with open('profile_cutout.png', 'wb') as out:
        out.write(output)

im = Image.open('profile_cutout.png')
print("Cutout successfully created! Size:", im.size, "Mode:", im.mode)
