from PIL import Image
import os

def scale_image(image, i):
    new_width = int(image.width * i)
    new_height = int(image.height * i)
    resized_image = image.resize((new_width, new_height))
    return resized_image

promotypes = ['Bronze', 'Silver', 'Gold', 'Platinum', 'Emerald', 'Legendary']

for icon in os.listdir():
    for promotype in promotypes:
        if promotype in icon:
            icon1 = Image.open(icon)
            icon1 = scale_image(icon1, 0.5)
            icon1.save(f'./{icon}')
