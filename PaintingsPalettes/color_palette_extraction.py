import pandas as pd

from PIL import Image

import cv2
import extcolors
from colormap import rgb2hex
import os
from os import listdir
from os.path import isfile, join
from tqdm import tqdm
import pickle


def resize_image(input_image, resize):
    output_width = resize
    img = Image.open(input_image)
    if img.size[0] >= resize:
        wpercent = (output_width/float(img.size[0]))
        hsize = int((float(img.size[1])*float(wpercent)))
        img = img.resize((output_width,hsize), Image.ANTIALIAS)
        resize_name = 'resize_'+ input_image
        img.save(resize_name)
    else:
        resize_name = input_image
    return resize_name

def color_to_df(input):
    colors_pre_list = str(input).replace('([(','').split(', (')[0:-1]
    df_rgb = [i.split('), ')[0] + ')' for i in colors_pre_list]
    df_percent = [i.split('), ')[1].replace(')','') for i in colors_pre_list]
    
    #convert RGB to HEX code
    df_color_up = [rgb2hex(int(i.split(", ")[0].replace("(","")),
                          int(i.split(", ")[1]),
                          int(i.split(", ")[2].replace(")",""))) for i in df_rgb]
    
    df = pd.DataFrame(zip(df_color_up, df_percent), columns = ['c_code','occurence'])
    return df

def extract_color_palette(input_image, resize, tolerance, zoom):
    colors_x = extcolors.extract_from_path(input_image, tolerance = tolerance, limit = 13)
    df_color = color_to_df(colors_x)
    return df_color


if __name__ == "__main__":
    input_dir = "./images"

    to_extract = ['painting', 'mixed-media', 'photography', 'prints', 'works-on-paper']
    image_files = [join(input_dir, f) for f in listdir(input_dir) if isfile(join(input_dir, f))]
    image_palette = dict()
    for i, f in tqdm(enumerate(image_files)):
        palette = extract_color_palette(f, 300, 12, 2.5)
        image_name = os.path.basename(f)
        image_name = image_name.split(".")[0]
        if image_name in to_extract:
            image_palette[image_name] = palette
        # print(palette)
        # if i == 3:
            # break
    
    with open('all_artwork_palettes.pickle', 'wb') as f:
        pickle.dump(image_palette, f)
    # print(image_palette)
    # with open("painting_palettes.json", "w") as f:
        # json.dump(image_palette, f)
    # image_palette_df = pd.DataFrame.from_dict(image_palette)
    # image_palette_df.to_csv("./paintings_palettes.csv")
