from collections import namedtuple
from dataclasses import dataclass
from lib2to3.pgen2.pgen import DFAState
import altair as alt 
import numpy as np
import pandas as pd
import streamlit as st
import graphviz as graphviz
import datetime as datetime
import requests
import time

import streamlit.components.v1 as components  # Import Streamlit


#Homework 1: Deleted the starter code and am now writing my own code below
#I want to make it clear that only the Streamlit documentation was used to complete this portion of the assignment
#The examples provided in the documentation helped me complete this homework and the code provided was used to help me write the code below!
#docs.streamlit.io was used to complete this part of the homework assignment

st.set_page_config(
     page_title="VroomVroom",
     page_icon="🧊",
     layout="wide",
     initial_sidebar_state="auto",
     menu_items=None
 )


#Render the h1 block, contained in a frame of size 200x200.
#components.html("<html><banner><h1>Hello, World</h1></body></html>", width=200, height=200)   

with open('Vroom Vroom Wireframe try.html') as f:
    st.markdown(f'<style>{f.read()}</style>', unsafe_allow_html=True)

# with st.container():
#     st.write('Vroom Vroom: Sell Your Car with Data')
#     st.write('Get Your Price')
#     st.write('Settings')
#     st.write('Profile')
#     st.write('Log Out')


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

