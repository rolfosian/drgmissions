from PIL import ImageFont, ImageDraw, Image
import subprocess
import os

def scale_image(image, i):
    new_width = int(image.width * i)
    new_height = int(image.height * i)
    resized_image = image.resize((new_width, new_height))
    return resized_image

def calc_center_y(image):
    height = image.height
    center_y = height // 2
    return center_y

def calc_center_x(image):
    width = image.width
    center_x = width // 2
    return center_x

def calc_center(image, background):
    return calc_center_x(background)-calc_center_x(image), calc_center_y(background)-calc_center_y(image)

def calc_text_center(image_width, image_height, text, font, font_size):
    temp_image = Image.new("RGB", (image_width, image_height))
    temp_draw = ImageDraw.Draw(temp_image)

    text_bbox = temp_draw.textbbox((0, 0), text, font=font)
    text_width = text_bbox[2] - text_bbox[0]
    text_height = text_bbox[3] - text_bbox[1]

    text_x = (image_width - text_width) // 2
    text_y = (image_height - text_height) // 2
    temp_image.close()
    del temp_draw
    return text_x, text_y

def render_standard_mission_secondary_obj_resource(secondary_obj, filename):
    font_path = './CarbonBold-W00-Regular.ttf'
    font_size = 45
    font = ImageFont.truetype(font_path, font_size)
    text_color = (255, 255, 255)
    values = {
        'ApocaBlooms' : '15',
        'Fossils' : '10',
        'Boolo Caps' : '20',
        'Dystrum' : '100',
        'Ebonuts' : '14',
        'Fester Fleas' : '10',
        'Gunk Seeds' : '12',
        'Hollomite' : '35',
        'Exterminate Bha Barnacles' : '16',
        'Exterminate Glyphid Eggs' : '40'
    }

    BACKGROUND = Image.new("RGBA", (256, 256), (0,0,0,0))
    HEXAGON = Image.open('./hexagon.png')
    HEXAGON = scale_image(HEXAGON, 0.4)
    #x, y = calc_center(HEXAGON, BACKGROUND)
    #print(f'HEXAGON X: {str(x)}')
    #print(f'HEXAGON Y: {str(y)}')
    BACKGROUND.paste(HEXAGON, (69, 59), mask=HEXAGON)
    HEXAGON.close()

    RESOURCE = Image.open(f'./{filename}')
    if 'GlyphidEgg' in filename or 'BhaBarnacle' in filename:
        RESOURCE = scale_image(RESOURCE, 0.14)
    else:
        RESOURCE = scale_image(RESOURCE, 0.28)
    x, y = calc_center(RESOURCE, BACKGROUND)
    if secondary_obj == 'ApocaBlooms':
        x -= 5
    BACKGROUND.paste(RESOURCE, (x, y-21), mask=RESOURCE)
    RESOURCE.close()

    text = values[secondary_obj]
    DRAW = ImageDraw.Draw(BACKGROUND)
    text_x, text_y = calc_text_center(BACKGROUND.width, BACKGROUND.height, text, font, font_size)
    # if secondary_obj == 'ApocaBlooms':
        # text_y += 5
    if secondary_obj == 'Dystrum':
        text_y -= 5
    DRAW.text((text_x, text_y+20), text, font=font, fill=text_color)
    del DRAW
    return BACKGROUND

secondary_objs = {
        'ApocaBlooms' : 'Icons_Resources_Outline_Apocabloom.png',
        'Fossils' : 'Icons_Resources_Outline_Fossil.png',
        'Boolo Caps' : 'Icons_Resources_Outline_BooloCap.png',
        'Dystrum' : 'Icons_Resources_Outline_Dystrum.png',
        'Ebonuts' : 'Icons_Resources_Outline_Ebonut.png',
        'Fester Fleas' : 'Icons_Resources_Outline_Festerflea.png',
        'Gunk Seeds' : 'Icons_Resources_Outline_Gunk_Seeds.png',
        'Hollomite' : 'Icons_Resources_Outline_hollomite.png',
        'Exterminate Bha Barnacles' : 'Icons_Resources_Outline_BhaBarnacle.png',
        'Exterminate Glyphid Eggs' : 'Icons_Resources_Outline_GlyphidEgg.png'
            }
files = os.listdir()

# for obj in secondary_objs.keys():
#     rendered = render_standard_mission_secondary_obj_resource(obj, secondary_objs[obj])
#     fname = obj.replace(" ", "_")+'_icon.png'
#     rendered.save(fname, format='PNG')
#     try:
#         subprocess.run(['gwenview', fname], timeout=2)
#     except:
#         pass

for file in files:
    if file.endswith('.png') and file != 'hexagon.png':
        subprocess.run(['ffmpeg', '-i', file, '-q:v', '6', file.replace('.png', '.webp')])

