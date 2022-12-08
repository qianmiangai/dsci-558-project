from faulthandler import disable
import streamlit as st
import pandas as pd
import numpy as np
import json
from PIL import Image
import urllib.request

with open('./data/artist_recommend.json') as json_file:
    artist_recommend_dict = json.load(json_file)

#st.session_state

raw = pd.read_csv('./data/FinalDataSet_with_recommendation.csv')

df = raw.copy() ## dataframe that would not change

min_year = min(list(df['work_year']))
max_year = max(list(df['work_year']))

filtered_dataF = df.copy() ## dataframe that would change according to the SEARCHING methods

header = st.container()
search_filter = st.expander('Search & Filter')
dataset = st.container()
detail_page = st.container()
artworks = st.container()

def artist0():
    st.session_state['ARTIST'] = similar_artists[0]

def artist1():
    st.session_state['ARTIST'] = similar_artists[1]

def artist2():
    st.session_state['ARTIST'] = similar_artists[2]

def artist3():
    st.session_state['ARTIST'] = similar_artists[-2]

def artist4():
    st.session_state['ARTIST'] = similar_artists[-1]

with header:
    st.title('ARTLINK')

with search_filter:
    col1, col2= st.columns(2)
    style = col1.selectbox('STYLE', [' ']+list(df['class'].unique()), key='STYLE')
    if style != ' ':
        filtered_dataF = filtered_dataF[filtered_dataF['class']==style]
    type = col2.selectbox('TYPE',[' ']+list(df['media'].unique()), key='TYPE')
    if type != ' ':
        filtered_dataF = filtered_dataF[filtered_dataF['media']==type]
    artist = col1.selectbox('ARTIST', [' ']+list(df['artist_name'].unique()), key='ARTIST')
    if artist != ' ':
        filtered_dataF = filtered_dataF[filtered_dataF['artist_name']==artist]
    gallery = col2.selectbox('GALLERY', [' ']+list(df['gallery_name'].unique()), key='GALLERY')
    if gallery != ' ':
        filtered_dataF = filtered_dataF[filtered_dataF['gallery_name']==gallery]

    years = st.slider('YEAR', min_year, max_year, (min_year, max_year), key='YEAR')
    filtered_dataF = filtered_dataF[filtered_dataF['work_year'].between(years[0], years[1], inclusive='both')]

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

#def detail_callback():
#    st.session_state[current_page_dataF['id'][2]] = True

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

                st.subheader('About the Artist')
                cola, colb = st.columns([1,4])

                cola.write('Artist:')
                colb.write('['+current_page_dataF['artist_name'][i]+']('+current_page_dataF['artist_url'][i]+')')

                try:
                    colb.write('['+current_page_dataF['artist_website'][i]+']('+current_page_dataF['artist_website'][i]+')')
                    cola.write('Website:')
                except:
                    pass

                try:
                    colb.write('['+current_page_dataF['artist_ins'][i]+']('+current_page_dataF['artist_ins'][i]+')')
                    cola.write('Instagram:')
                except:
                    pass

                if isinstance(current_page_dataF['nationality'][i], str):
                    cola.write('Nationality:')
                    colb.write(current_page_dataF['nationality'][i])

                if isinstance(current_page_dataF['education'][i], str):
                    cola.write('Education:')
                    colb.write(current_page_dataF['education'][i])

                cola.write('Biography:')
                colb.write(current_page_dataF['full_bio'][i])

                st.subheader('Some Similar Artists')
                current_artist = current_page_dataF['artist_name'][i]
                similar_artists = artist_recommend_dict[current_artist]
                col0, col1, col2, col3, col4 = st.columns(5)
                col0.button(label=similar_artists[0], key='similar_artist0', on_click=artist0)
                col1.button(label=similar_artists[1], key='similar_artist1', on_click=artist1)
                col2.button(label=similar_artists[2], key='similar_artist2', on_click=artist2)
                col3.button(label=similar_artists[-2], key='similar_artist3', on_click=artist3)
                col4.button(label=similar_artists[-1], key='similar_artist4', on_click=artist4)

                st.subheader('Other Artworks by the same Artist')
                current_artworkID = current_page_dataF['id'][i]
                artworks_cols = st.columns(4)
                artist_artwork_df = df[(df['artist_name']==current_artist) & (df['id']!=current_artworkID)]
                artist_artwork_df = artist_artwork_df.reset_index(drop=True)
                #st.dataframe(artist_artwork_df)
                for n in range(min(4, len(artist_artwork_df))): 
                    image = Image.open(urllib.request.urlopen(artist_artwork_df['img_url'][n]))
                    artworks_cols[n].image(image, use_column_width=True, caption=artist_artwork_df['work_name'][n])


                st.subheader('Other Artworks You Might Like')
                reccommendation_cols = st.columns(4)

                #st.dataframe(current_page_dataF)
                #st.write(i)

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

    
    

                








