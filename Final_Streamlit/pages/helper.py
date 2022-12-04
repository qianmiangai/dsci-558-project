from PIL import Image
import cv2
import extcolors
from colormap import rgb2hex
import pandas as pd
import pickle

def dist(hex1, hex2):
    hex1 = hex1.lstrip("#")
    hex2 = hex2.lstrip("#")
    #get red/green/blue int values of hex1
    r1, g1, b1 = tuple(int(hex1[i:i+2], 16) for i in (0, 2, 4))
    # get red/green/blue int values of hex2
    r2, g2, b2 = tuple(int(hex2[i:i+2], 16) for i in (0, 2, 4))
    # calculate differences between reds, greens and blues
    r = 255 - abs(r1 - r2);
    g = 255 - abs(g1 - g2);
    b = 255 - abs(b1 - b2);
    # limit differences between 0 and 1
    r /= 255;
    g /= 255;
    b /= 255;
    # 0 means opposite colors, 1 means same colors
    return (r + g + b) / 3;


def load_image(image_file):
	img = Image.open(image_file)
	return img

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

def extract_color_palette(input_image):
    colors_x = extcolors.extract_from_image(input_image)
    df_color = color_to_df(colors_x)
    return df_color

def get_closest_hex(hex1, list_of_hex):
    highest_sim_score = 0
    closest_hex = ""
    for hex2 in list_of_hex:
        curr_sim = dist(hex1, hex2)
        if curr_sim > highest_sim_score:
            highest_sim_score = curr_sim
            closest_hex = hex2
    return closest_hex

def color_hex_to_color_group(hexcodes):
    """
    hexcodes: list of four hexcodes
    """
    with open("../data/hexcode_to_colorgroup.pickle", "rb") as f:
        hex_to_group_dict = pickle.load(f)
    color_groups = []
    for hex in hexcodes:
        if hex in hex_to_group_dict:
            cg = hex_to_group_dict[hex]
        else:
            cg = hex_to_group_dict[get_closest_hex(hex, hex_to_group_dict.keys())]
            hex_to_group_dict[hex] = cg
        color_groups.append(cg)
    
    # save newly found colors 
    #with open("./hexcode_to_colorgroup.pickle", "wb") as f:
    #    pickle.dump(hex_to_group_dict)
    return color_groups
    