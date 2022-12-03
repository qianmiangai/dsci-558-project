import streamlit as st
import pandas as pd
import numpy as np
#import matplotlib.pyplot as plt
#import seaborn as sns

#raw = pd.

header = st.container()
dataset = st.container()

with header:
    st.title('by Artwork')

with dataset:
    st.header('Artworks')