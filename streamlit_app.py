from collections import namedtuple
import altair as alt
import math
import pandas as pd
import streamlit as st
import time
import geopy as gp
import geopy.distance as gpd
import requests
from geopy.geocoders import Nominatim
import gdown

st.set_page_config(
     page_title="VroomVroom",
     page_icon="🧊",
     layout="centered",
     initial_sidebar_state="auto",
     menu_items=None
 )

"""
# VroomVroom

Welcome to VroomVroom! Your guide to selling your car, truck or SUV!


In the meantime, below is an example of what you can do with just a few lines of code:
"""

#Import CSV and Prepare For Display

# Streaming Database

#Leave uncommented to test from Google Drive File

gDrivepath = 'https://drive.google.com/file/d/1NeAmUoe9FqYsEAW8vHlRcjlKF_r7b3Ou/view?usp=sharing'
gDrivepath='https://drive.google.com/uc?id=' + gDrivepath.split('/')[-2]

@st.cache(persist=True)
def download(path):
    gdown.download(url=path, output='used_cars_dataset_trimmed.csv', quiet=False)
    df = pd.read_csv('used_cars_dataset_trimmed.csv')
    return df

df = download(gDrivepath)


#Local Cache

# To test from local cache, uncomment both following lines.

#localPath = '~/Documents/GitHub/VroomVroom/Dataset/used_cars_dataset_trimmed.csv' #EDIT this line with the filepath of the .csv to stream locally
#df = pd.read_csv(localPath) #Read in CSV

#Create Dropdown Menu

makes = df["make_name"]

makes = makes.drop_duplicates()

makes = makes.sort_values()

makes = makes.values.tolist()

models = df["model_name"]

models = models.drop_duplicates()

models = models.sort_values()

models = models.values.tolist()

year = df["year"]

year = year.drop_duplicates()

year = year.sort_values(ascending=False)

year = year.values.tolist()


#Display Values from Dataset For Search

left_column, middle_column, right_column = st.columns(3)
with left_column:
    year = st.selectbox(
        'Year',year)
    mileage = st.text_input('Mileage', '##,###')

with middle_column:
    make = st.selectbox(
        'Make', makes)
    zipCode = st.text_input('Zip code', '#####')

with right_column:
    model = st.selectbox(
         'Model', models)

right_column.button('Confirm!')

#Data Sanitization

try:
    int(zipCode)
except ValueError:
    st.write("Enter a Valid Zip Code!")
else:
    if (int(zipCode) > 9999 and int(zipCode) < 100000):
        geolocator = Nominatim(user_agent = "VroomVroom")
        location = geolocator.geocode(zipCode + " United States")
        searchRadius=10
        maxLong = gpd.distance(miles=searchRadius).destination((location.latitude, location.longitude), bearing=90)
        minLong = gpd.distance(miles=searchRadius).destination((location.latitude, location.longitude), bearing=-90)
        maxLat = gpd.distance(miles=searchRadius).destination((location.latitude, location.longitude), bearing=0)
        minLat = gpd.distance(miles=searchRadius).destination((location.latitude, location.longitude), bearing=180)
        maxLong = maxLong[1]
        minLong = minLong[1]
        maxLat = maxLat[0]
        minLat = minLat[0]
    else:
        st.write("Enter a Valid Zip Code!")

with st.spinner('Wait for it...'):
    time.sleep(0)
st.success('Done!')

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


# Implementation of Google Image Search API

testing = 1 #DO NOT CHANGE UNTIL TESTING IS COMPLETE, WE ONLY HAVE 100 CALLS PER DAY

#API Keys used for Google Image API

API_Key = st.secrets["API_Key"]
CX = st.secrets["CX"]
num = "1"

#Build Google Image Search Query

makeInput = make.replace(" ", "+")
modelInput = model.replace(" ", "+")

q = str(year) + "+" + makeInput + "+" + modelInput

if testing == 0:
    q = str(year) + make + model
else:
    q = "2002+Honda+Accord"

#Build the Google Search API URL to Retrieve Image

url = "https://customsearch.googleapis.com/customsearch/v1?cx="+CX+"&q="+q+"&searchType=image&num="+num+"&start=1&safe=off&"+"key="+API_Key+"&alt=json"

if testing == 0:
    searchHTTP=requests.get(url)
    searchResult = searchHTTP.json()
else: # only for testing
    searchResult={'kind': 'customsearch#search',
 'url': {'type': 'application/json',
  'template': 'https://www.googleapis.com/customsearch/v1?q={searchTerms}&num={count?}&start={startIndex?}&lr={language?}&safe={safe?}&cx={cx?}&sort={sort?}&filter={filter?}&gl={gl?}&cr={cr?}&googlehost={googleHost?}&c2coff={disableCnTwTranslation?}&hq={hq?}&hl={hl?}&siteSearch={siteSearch?}&siteSearchFilter={siteSearchFilter?}&exactTerms={exactTerms?}&excludeTerms={excludeTerms?}&linkSite={linkSite?}&orTerms={orTerms?}&relatedSite={relatedSite?}&dateRestrict={dateRestrict?}&lowRange={lowRange?}&highRange={highRange?}&searchType={searchType}&fileType={fileType?}&rights={rights?}&imgSize={imgSize?}&imgType={imgType?}&imgColorType={imgColorType?}&imgDominantColor={imgDominantColor?}&alt=json'},
 'queries': {'request': [{'title': 'Google Custom Search - 2003 Honda Accord',
    'totalResults': '832000',
    'searchTerms': '2003 Honda Accord',
    'count': 1,
    'startIndex': 1,
    'inputEncoding': 'utf8',
    'outputEncoding': 'utf8',
    'safe': 'off',
    'cx': '55e78cedddf23a7dc',
    'searchType': 'image'}],
  'nextPage': [{'title': 'Google Custom Search - 2003 Honda Accord',
    'totalResults': '832000',
    'searchTerms': '2003 Honda Accord',
    'count': 1,
    'startIndex': 2,
    'inputEncoding': 'utf8',
    'outputEncoding': 'utf8',
    'safe': 'off',
    'cx': '55e78cedddf23a7dc',
    'searchType': 'image'}]},
 'context': {'title': 'Google Image Search'},
 'searchInformation': {'searchTime': 0.149774,
  'formattedSearchTime': '0.15',
  'totalResults': '832000',
  'formattedTotalResults': '832,000'},
 'items': [{'kind': 'customsearch#result',
   'title': 'Used 2003 Honda Accord for Sale Near Me | Edmunds',
   'htmlTitle': 'Used <b>2003 Honda Accord</b> for Sale Near Me | Edmunds',
   'link': 'https://media.ed.edmunds-media.com/for-sale/0d-1hgcm56603a122867/img-1-600x400.jpg',
   'displayLink': 'www.edmunds.com',
   'snippet': 'Used 2003 Honda Accord for Sale Near Me | Edmunds',
   'htmlSnippet': 'Used <b>2003 Honda Accord</b> for Sale Near Me | Edmunds',
   'mime': 'image/jpeg',
   'fileFormat': 'image/jpeg',
   'image': {'contextLink': 'https://www.edmunds.com/honda/accord/2003/',
    'height': 400,
    'width': 600,
    'byteSize': 41524,
    'thumbnailLink': 'https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcTI2FuckxjFe8pNsPGG1Ie0yAV6M0PCrBIhSrVLN6EkDepJXSjZ3MLKofE&s',
    'thumbnailHeight': 90,
    'thumbnailWidth': 135}}]}

imgurl = searchResult['items'][0]['link']

st.image(imgurl) #Use this line to display the image where necessary
