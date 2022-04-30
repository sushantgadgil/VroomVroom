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

left_column, middle_column, right_column = st.columns(3)
with left_column:
    option = st.selectbox(
        'Year',
        ('2010', '2011', '2012', '2013', '2014', '2015', '2016', '2017', '2018', '2019', '2020'))
    title = st.text_input('Mileage', 'miles')

with middle_column:
    option = st.selectbox(
        'Model',
        ('Toyota Highlander', 'Toyota RAV4', 'Toyota Corolla', 'Honda CRV', 'Honda Civic'))
    title = st.text_input('Zip code', '#####')

with right_column:
    option = st.selectbox(
         'Make',
        ('Toyota Highlander', 'Toyota RAV4', 'Toyota Corolla', 'Honda CRV', 'Honda Civic'))

right_column.button('Confirm!')


st.button('Get price')

with st.spinner('Wait for it...'):
    time.sleep(5)
st.success('Done!')


with st.echo(code_location='below'):
    total_points = st.slider("Number of points in spiral", 1, 5000, 2000)
    num_turns = st.slider("Number of turns in spiral", 1, 100, 9)

    Point = namedtuple('Point', 'x y')
    data = []

    points_per_turn = total_points / num_turns

    for curr_point_num in range(total_points):
        curr_turn, i = divmod(curr_point_num, points_per_turn)
        angle = (curr_turn + 1) * 2 * math.pi * i / points_per_turn
        radius = curr_point_num / total_points
        x = radius * math.cos(angle)
        y = radius * math.sin(angle)
        data.append(Point(x, y))

    st.altair_chart(alt.Chart(pd.DataFrame(data), height=500, width=500)
        .mark_circle(color='#0068c9', opacity=0.5)
        .encode(x='x:Q', y='y:Q'))
