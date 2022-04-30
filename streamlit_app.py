from collections import namedtuple
import altair as alt
import math
import pandas as pd
import streamlit as st
import time 

"""
# Welcome to Streamlit!

Edit `/streamlit_app.py` to customize this app to your heart's desire :heart:

If you have any questions, checkout our [documentation](https://docs.streamlit.io) and [community
forums](https://discuss.streamlit.io).

In the meantime, below is an example of what you can do with just a few lines of code:
"""

st.set_page_config(
     page_title="VroomVroom",
     page_icon="🧊",
     layout="centered",
     initial_sidebar_state="auto",
     menu_items=None
 )

left_column, middle_column, right_column = st.columns(3)
with left_column:
    year = st.selectbox(
        'Year',
        ('2010', '2011', '2012', '2013', '2014', '2015', '2016', '2017', '2018', '2019', '2020'))
    mileage = st.text_input('Mileage', 'miles')

with middle_column:
    model = st.selectbox(
        'Model',
        ('Toyota Highlander', 'Toyota RAV4', 'Toyota Corolla', 'Honda CRV', 'Honda Civic'))
    zipCode = st.text_input('Zip code', '#####')

with right_column:
    make = st.selectbox(
         'Make',
        ('Toyota Highlander', 'Toyota RAV4', 'Toyota Corolla', 'Honda CRV', 'Honda Civic'))



right_column.button('Confirm!')

with left_column.container():
    st.header('Best Price')
    st.write("Sell your car at the best price no matter how long it takes.")
    st.button('Get Best Price')
    # You can call any Streamlit command, including custom components:

with middle_column.container():
    st.header('No Preference')
    st.write("You cannot wait forever, but you can wait for an offer that is right for you.")
    st.button('Get Price for No Preference')
    # You can call any Streamlit command, including custom components:    

with right_column.container():
    st.header('Fast Sale')
    st.write("Sell your car as fast as possible, likely through a dealer or broker.")
    st.button('Get Fast Sale Price')
    # You can call any Streamlit command, including custom components:    

with st.spinner('Wait for it...'):
    time.sleep(5)
st.success('Done!')
