from faulthandler import disable
import streamlit as st
import pandas as pd
import numpy as np
from PIL import Image
import urllib.request

from helper import load_image, extract_color_palette, color_hex_to_color_group

raw = pd.read_csv('./data/FinalDataSet_with_recommendation.csv')

df = raw.copy() ## dataframe that would not change

min_year = min(list(df['work_year']))
max_year = max(list(df['work_year']))

filtered_dataF = df.copy() ## dataframe that would change according to the SEARCHING methods

header = st.container()
search_filter = st.expander('Pick your Favorite Colors')
dataset = st.container()
detail_page = st.container()
artworks = st.container()

with header:
    st.title('ARTLINK')

with search_filter:
    col1, col2 = st.columns([2,2])

    style = col1.selectbox('STYLE', [' ']+list(df['class'].unique()), key='STYLE')
    if style != ' ':
        filtered_dataF = filtered_dataF[filtered_dataF['class']==style]
    type = col2.selectbox('TYPE',[' ']+list(df['media'].unique()), key='TYPE')
    if type != ' ':
        filtered_dataF = filtered_dataF[filtered_dataF['media']==type]
    col1, col2, col3, col4, col5 = st.columns([2,3,3,3,3])
    color1 = col2.color_picker(' ', key='color1', value='#FFFFFF')
    color2 = col3.color_picker(' ', key='color2', value='#FF0000')
    color3 = col4.color_picker(' ', key='color3', value='#00FF00')
    color4 = col5.color_picker(' ', key='color4', value='#0000FF')
    four_colors = [color1, color2, color3, color4]
    four_color_groups = color_hex_to_color_group(four_colors)
    filtered_dataF = filtered_dataF[filtered_dataF['color_group1'].isin(four_color_groups) | filtered_dataF['color_group1'].isin(four_color_groups) | filtered_dataF['color_group3'].isin(four_color_groups) | filtered_dataF['color_group4'].isin(four_color_groups)]

    uploaded_file = st.file_uploader("Choose a file")
    if uploaded_file is not None:
        uploaded_image = load_image(uploaded_file)
        st.image(uploaded_image,width=250) # view image
        palette = extract_color_palette(uploaded_image)
        top_four_colors = palette.iloc[:2, 0].tolist()
        top_four_color_groups = color_hex_to_color_group(top_four_colors)
        filtered_dataF = df[df['color_group1'].isin(top_four_color_groups) | df['color_group2'].isin(top_four_color_groups | df['color_group3'].isin(top_four_color_groups) | df['color_group4'].isin(top_four_color_groups))]

with dataset:
    #st.header('data')
    total_results = len(filtered_dataF)
    total_pages = total_results//32+1 # 32 Artworks per Page
    current_page = st.number_input('PAGE', min_value=1, max_value=total_pages, key='PAGE') # current page number
    current_page_dataF = filtered_dataF[32*(current_page-1):32*current_page].reset_index(drop=True)
    ## dataframe that would be shown in the current page

    col1, col2, col3 = st.columns([2,5,1])
    col1.text(str(total_results)+' Results')
    col3.text('  '+str(total_pages)+' Pages') 

    #st.dataframe(current_page_dataF)
    ## to check the dataframe 



with artworks: 
    st.title('Artworks Gallery')

    #col0, col1, col2, col3 = st.columns(4)
    col_ls = list(st.columns(4)) ## 4 columns of space for the artworks

    for i in range(len(current_page_dataF)): 
        image = Image.open(urllib.request.urlopen(current_page_dataF['img_url'][i]))
        col_ls[i%4].image(image, use_column_width=True, caption=current_page_dataF['work_name'][i])
        
        #detail_key_name_ID = current_page_dataF['id'][i]
        detail = col_ls[i%4].button(label=current_page_dataF['work_name'][i], key=current_page_dataF['id'][i])#, on_click=detail_callback)

        if detail:
            #st.session_state[current_page_dataF['id'][i]] = not st.session_state[current_page_dataF['id'][i]]
            with detail_page:
                #st.session_state[current_page_dataF['id'][i]] = not st.session_state[current_page_dataF['id'][i]]
                st.image(image, use_column_width='auto', caption=current_page_dataF['dimension'][i])
                
                cola, colb = st.columns([1,4])

                cola.write('Artwork:')
                colb.write('['+current_page_dataF['work_name'][i]+']('+current_page_dataF['url'][i]+')')


                cola.write('Gallery:')
                colb.write('['+current_page_dataF['gallery_name'][i]+']('+current_page_dataF['gallery_url'][i]+')')

                cola.write('Type:')
                colb.write(current_page_dataF['media'][i])

                cola.write('Media:')
                colb.write(current_page_dataF['media_long'][i])

                cola.write('Dimension:')
                colb.write(current_page_dataF['dimension'][i])

                cola.write('Year:')
                colb.write(current_page_dataF['work_year'][i])

                cola.write('Style:')
                colb.write(current_page_dataF['class'][i])

                st.subheader('Other Artworks You Might Like')
                reccommendation_cols = st.columns(4)

                temp_list = list(current_page_dataF.loc[i, ['similar1_x','similar2_x','similar3_x','similar4_x','similar5_x','similar6_x','similar7_x','similar8_x']])
                #st.write(temp_list)
                for temp_i in range(len(reccommendation_cols)):
                    temp_row = df.loc[df['id']==temp_list[temp_i]]
                    temp_img_URL = temp_row['img_url'].tolist()[0]
                    image = Image.open(urllib.request.urlopen(temp_img_URL))
                    reccommendation_cols[temp_i].image(image, use_column_width=True, caption=temp_row['work_name'].tolist()[0])
                    reccommendation_cols[temp_i].button(label='X', key='recommend'+str(temp_i))
                    #deleted = reccommendation_cols[temp_i].button(label='X', key='recommend'+str(temp_i))
                    #if deleted:
                    #    #temp_list.pop(temp_i)
                    #    del reccommendation_cols[temp_i]
                    #    temp_row = df.loc[df['id']==temp_list[temp_i+4]]
                    #    temp_img_URL = temp_row['img_url'].tolist()[0]
                    #    image = Image.open(urllib.request.urlopen(temp_img_URL))
                    #    reccommendation_cols[temp_i].image(image, use_column_width=True, caption=temp_row['work_name'].tolist()[0])
                    #    deleted = reccommendation_cols[temp_i].button(label='X', key='recommend'+str(temp_i+4))
