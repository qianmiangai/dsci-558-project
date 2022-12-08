import streamlit as st
import pandas as pd
from collections import Counter
import matplotlib.pyplot as plt

header = st.container()
with header:
    st.title('ARTLINK')

st.header('Motivation')
st.write('A large collection of digital artwork can promote a deeper understanding of fine art and ultimately support the spread of culture. When people are browsing unfamiliar artists, they may be interested in basic information about the artist, such as the price of the work and the artistic background. People also enjoy exploring similar genres of art and related artists. Our program is designed to provide museum goers and art lovers with a deeper understanding of the artworks they are interested in and to recommend other artworks and artists to expand their reach. In addition, when people are browsing artwork and considering a purchase, they often want to make sure it will match the rest of their collection. This program also recommends artwork that will fit into the palette of the user\'s space.')

st.header('Dataset')
st.write('Our primary data source comes from [Artsy.net](Artsy.net). From Artsy, we scraped information about each artwork, such as its artist, the medium, dimensions, price, and the gallery it is displaying at. Our other data sources include [WikiArt](wikiart.org), [Widewalls](widewalls.ch), and Instagram to provide additional information about the artist such as artist biographies and personal websites. ')
st.header('Statistics')
df = pd.read_csv('./data/FinalDataSet_with_recommendation.csv')

temp_df = pd.DataFrame(pd.cut(df['work_year'], [1880, 1900, 1920, 1940, 1960, 1980, 2000, 2022]))
temp_df.columns = ["year_bins"]
df2 = pd.concat([df, temp_df], axis=1)
df2['year_bins'] = df2['year_bins'].astype("str")

col1, col2 = st.columns([1,2])
var_X = col1.selectbox('Select Category', options=['Media','Year'])
var_Y = col2.selectbox('Select Variable', options=['Number of Artworks','Average Price'])

dic_ls = {'Media':'media', 'Year':'year_bins', 'Style':'class'}

if var_Y == 'Number of Artworks':
    if var_X == 'Year':
        dataf = df2
    else:
        dataf = df
    c = Counter(dataf[dic_ls[var_X]])
    category = list(c.keys())
    count = list(c.values())
    category, count = (list(t) for t in zip(*sorted(zip(category, count))))
    fig = plt.figure(figsize = (10, 5))
    plt.bar(category, count, color ='maroon', width = 0.4)
    plt.xlabel("Artwork " + var_X)
    plt.ylabel("No. of Artworks")
    plt.title("Distribution of Different Artwork " + var_X)
    st.pyplot(fig)
elif var_Y == 'Average Price':
    if var_X == 'Year':
        dataf = df2
    else:
        dataf = df
    avg_price = dataf.groupby(dic_ls[var_X]).mean()['price']
    fig = plt.figure(figsize = (10, 5))
    plt.bar(avg_price.index, avg_price, color ='maroon', width = 0.4)
    plt.xlabel("Artwork " + var_X)
    plt.ylabel("Average Price")
    plt.title("Average Price of Artwork by " + var_X)
    st.pyplot(fig)




