from faulthandler import disable
import streamlit as st
import pandas as pd
import numpy as np
from PIL import Image
import urllib.request

from helper import load_image, extract_color_palette, color_hex_to_color_group


raw = pd.read_csv('../../FinalDataSetCreation/FinalDataset_with_all.csv')

df = raw.copy() ## dataframe that would not change

min_year = min(list(df['work_year']))
max_year = max(list(df['work_year']))

filtered_dataF = df.copy() ## dataframe that would change according to the SEARCHING methods

header = st.container()
search_filter = st.expander('Search & Filter')
dataset = st.container()
detail_page = st.container()
artworks = st.container()


with header:
    st.title('Artworks')

with search_filter:
    col1, col2, col3, col4 = st.columns(4)

    type = col1.selectbox('TYPE',[' ']+list(df['media'].unique()), key='TYPE')
    if type != ' ':
        filtered_dataF = filtered_dataF[filtered_dataF['media']==type]
    artist = col2.selectbox('ARTIST', [' ']+list(df['artist_name'].unique()), key='ARTIST')
    if artist != ' ':
        filtered_dataF = filtered_dataF[filtered_dataF['artist_name']==artist]
    gallery = col3.selectbox('GALLERY', [' ']+list(df['gallery_name'].unique()), key='GALLERY')
    if gallery != ' ':
        filtered_dataF = filtered_dataF[filtered_dataF['gallery_name']==gallery]
    #genre = col4.selectbox('GENRE', [' ']+list(df['genre'].unique()), key='GENRE')
    #if genre != ' ':
        #filtered_dataF = filtered_dataF[filtered_dataF['genre']==genre]

    years = st.slider('YEAR', min_year, max_year, (min_year, max_year), key='YEAR')
    filtered_dataF = filtered_dataF[filtered_dataF['work_year'].between(years[0], years[1], inclusive='both')]

    uploaded_file = st.file_uploader("Choose a file")
    if uploaded_file is not None:
        uploaded_image = load_image(uploaded_file)
        st.image(uploaded_image,width=250) # view image
        palette = extract_color_palette(uploaded_image)
        top_four_colors = palette.iloc[:2, 0].tolist()
        top_four_color_groups = color_hex_to_color_group(top_four_colors)
        # print(top_four_color_groups)
        # print(filtered_dataF.head())
        filtered_dataF = filtered_dataF[filtered_dataF['color_group1'].isin(top_four_color_groups) |  filtered_dataF['color_group2'].isin(top_four_color_groups)]
        # print(temp)


    searching = st.selectbox('ARTWORK SEARCHING', [' ']+list(df['work_name']), key='ARTWORK_SEARCHING')
    if searching != ' ':
        filtered_dataF = df[df['work_name']==searching]


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
        ## image form that could be used by st.image()
        col_ls[i%4].image(image, use_column_width=True, caption=current_page_dataF['work_name'][i])

        detail = col_ls[i%4].button(label=current_page_dataF['work_name'][i], key=current_page_dataF['id'][i])
        while detail:
            with detail_page:
                st.image(image, use_column_width='auto', caption=current_page_dataF['dimension'][i])

                cola, colb = st.columns([1,2])

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

                #cola.write('Genre:')
                #colb.write(current_page_dataF['genre'][i])
                st.subheader('About the Artist')
                cola, colb = st.columns([1,2])

                cola.write('Artist:')
                colb.write('['+current_page_dataF['artist_name'][i]+']('+current_page_dataF['artist_url'][i]+')')

                st.text('Biography: ') ## + biography(str)

                cola, colb = st.columns([1,2]) # for hyperlinks

                #cola.write('Instagram:')
                #colb.write('['+current_page_dataF['Instagram_url'][i]+']('+current_page_dataF['Instagram_url'][i]+')')

                #cola.write('Website:')
                #colb.write('['+current_page_dataF['Website_url'][i]+']('+current_page_dataF['Website_url'][i]+')')

                st.subheader('Other Artworks of the Artist')
                col0, col1, col2, col3 = st.columns(4) ## 4 columns of space for the artworks

                ## EXAMPLE:
                #image1 = Image.open(urllib.request.urlopen(current_page_dataF['img_url'][5]))
                #col1.image(image1, use_column_width=True, caption=current_page_dataF['work_name'][5])
                #detail = col1.button(label=current_page_dataF['work_name'][5])

                ### it may not work if you click the new buttons !!!
                ### BUT we don't need to click the buttons for DEMO !!!


                #image1 = Image.open(urllib.request.urlopen(--image_url(str)--))
                #image2, image3, image4
                #col1.image(image1, use_column_width=True, caption=--artwork_name(str)--)
                #col2.image(image2, use_column_width=True, caption=--artwork_name(str)--)
                #col3..., col4...
                
                ## buttuns
                #detail = col1.button(label=--artwork_name(str)--, key=--artwork_id(str)--)
                ## need 4 button

                st.subheader('Other Artworks You Might Like')
                ## same as 4 OTHER ARTWORKS for 4 RECOMMENDATIONS

                








