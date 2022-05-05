from collections import namedtuple
import altair as alt
import math
import numpy as np 
import pandas as pd
import streamlit as st
import time
import geopy as gp
import geopy.distance as gpd
import requests
from geopy.geocoders import Nominatim
import gdown
import sklearn
from sklearn.linear_model import LinearRegression
from sklearn.model_selection import train_test_split
from sklearn.metrics import max_error

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

"""

#Import CSV and Prepare For Display
#@st.cache(persist=True)
#csvPath= "C:\Users\Isabel\Desktop\used_cars_dataset_trimmed.csv"
df = pd.read_csv(r'C:\Users\Isabel\Desktop\used_cars_dataset_trimmed.csv')

#Order Make Names for Drop Down Selection 
makes = df["make_name"].drop_duplicates().sort_values()
makes = makes.values.tolist()

#Order Model Names for Drop Down Selection 
models = df["model_name"].drop_duplicates().sort_values()
models = models.values.tolist()

#Order Years for Drop Down Selection 
year = df["year"].drop_duplicates().sort_values(ascending=False)
year = year.values.tolist()


#Make three columns for each drop down selection 
left_column, middle_column, right_column = st.columns(3)
with left_column:
    make = st.selectbox('Make', makes)
    zipCode = st.text_input('Zip code', '#####')

with middle_column:
    model = st.selectbox('Model', models)
    mileage = st.text_input('Mileage', '##,###')

with right_column:
    year = st.selectbox('Year',year)

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
    price= st.button('Get Best Price')

with middle_column.container():
    st.header('No Preference')
    st.write("You cannot wait forever, but you can wait for an offer that is right for you.")
    no_pref= st.button('Get Price for No Preference')

with right_column.container():
    st.header('Fast Sale')
    st.write("Sell your car as fast as possible, likely through a dealer or broker.")
    fast_sale= st.button('Get Fast Sale Price')

# Implementation of Google Image Search API
testing = 1

#API Keys
#API_Key = st.secrets["API_Key"]
#CX = st.secrets["CX"]
#num = "1"

#Build Google Image Search Query
#makeInput = make.replace(" ", "+")
#modelInput = model.replace(" ", "+")
#q = str(year) + "+" + makeInput + "+" + modelInput

#if testing == 0:
#    q = str(year) + make + model
#else:
#    q = "2002+Honda+Accord"

#Build the URL
#url = "https://customsearch.googleapis.com/customsearch/v1?cx="+CX+"&q="+q+"&searchType=image&num="+num+"&start=1&safe=off&"+"key="+API_Key+"&alt=json"

#if testing == 0:
#    searchHTTP=requests.get(url)
#    searchResult = searchHTTP.json()
#else: # only for testing
#    searchResult={'kind': 'customsearch#search',
#  'url': {'type': 'application/json',
#   'template': 'https://www.googleapis.com/customsearch/v1?q={searchTerms}&num={count?}&start={startIndex?}&lr={language?}&safe={safe?}&cx={cx?}&sort={sort?}&filter={filter?}&gl={gl?}&cr={cr?}&googlehost={googleHost?}&c2coff={disableCnTwTranslation?}&hq={hq?}&hl={hl?}&siteSearch={siteSearch?}&siteSearchFilter={siteSearchFilter?}&exactTerms={exactTerms?}&excludeTerms={excludeTerms?}&linkSite={linkSite?}&orTerms={orTerms?}&relatedSite={relatedSite?}&dateRestrict={dateRestrict?}&lowRange={lowRange?}&highRange={highRange?}&searchType={searchType}&fileType={fileType?}&rights={rights?}&imgSize={imgSize?}&imgType={imgType?}&imgColorType={imgColorType?}&imgDominantColor={imgDominantColor?}&alt=json'},
#  'queries': {'request': [{'title': 'Google Custom Search - 2003 Honda Accord',
#     'totalResults': '832000',
#     'searchTerms': '2003 Honda Accord',
#     'count': 1,
#     'startIndex': 1,
#     'inputEncoding': 'utf8',
#     'outputEncoding': 'utf8',
#     'safe': 'off',
#     'cx': '55e78cedddf23a7dc',
#     'searchType': 'image'}],
#   'nextPage': [{'title': 'Google Custom Search - 2003 Honda Accord',
#     'totalResults': '832000',
#     'searchTerms': '2003 Honda Accord',
#     'count': 1,
#     'startIndex': 2,
#     'inputEncoding': 'utf8',
#     'outputEncoding': 'utf8',
#     'safe': 'off',
#     'cx': '55e78cedddf23a7dc',
#     'searchType': 'image'}]},
#  'context': {'title': 'Google Image Search'},
#  'searchInformation': {'searchTime': 0.149774,
#   'formattedSearchTime': '0.15',
#   'totalResults': '832000',
#   'formattedTotalResults': '832,000'},
#  'items': [{'kind': 'customsearch#result',
#    'title': 'Used 2003 Honda Accord for Sale Near Me | Edmunds',
#    'htmlTitle': 'Used <b>2003 Honda Accord</b> for Sale Near Me | Edmunds',
#    'link': 'https://media.ed.edmunds-media.com/for-sale/0d-1hgcm56603a122867/img-1-600x400.jpg',
#    'displayLink': 'www.edmunds.com',
#    'snippet': 'Used 2003 Honda Accord for Sale Near Me | Edmunds',
#    'htmlSnippet': 'Used <b>2003 Honda Accord</b> for Sale Near Me | Edmunds',
#    'mime': 'image/jpeg',
#    'fileFormat': 'image/jpeg',
#    'image': {'contextLink': 'https://www.edmunds.com/honda/accord/2003/',
#     'height': 400,
#     'width': 600,
#     'byteSize': 41524,
#     'thumbnailLink': 'https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcTI2FuckxjFe8pNsPGG1Ie0yAV6M0PCrBIhSrVLN6EkDepJXSjZ3MLKofE&s',
#     'thumbnailHeight': 90,
#     'thumbnailWidth': 135}}]}

# imgurl = searchResult['items'][0]['link']

# st.image(imgurl)
#st.image(img)

#Algorithms by Selected Preference
#BEST PRICE: make geographic radius bigger by x amount 
#FAST SALE: pull data only from current season 
#NO PREFERENCE: don't expand geographic radius and don't limit seasons 

#if Best Price selected, recalc search radius
if price: 
    searchRadius=30
    maxLong = gpd.distance(miles=searchRadius).destination((location.latitude, location.longitude), bearing=90)
    minLong = gpd.distance(miles=searchRadius).destination((location.latitude, location.longitude), bearing=-90)
    maxLat = gpd.distance(miles=searchRadius).destination((location.latitude, location.longitude), bearing=0)
    minLat = gpd.distance(miles=searchRadius).destination((location.latitude, location.longitude), bearing=180)
    maxLong = maxLong[1]
    minLong = minLong[1]
    maxLat = maxLat[0]
    minLat = minLat[0]

    st.write("SELECTED BEST PRICE")

elif fast_sale:
    #Need logic to parse dataset by season to match current season
    st.write("SELECTED FAST SALE")

    #Filter dataset to current season 

#Filter dataset to region of search
df_search= df[df['latitude'].between(minLat,maxLat)]
df_search= df_search[df_search['longitude'].between(minLong,maxLong)]

#train and test dataset with linear regression model 
predictors= ['year','make_name','model_name','mileage']
X= np.nan_to_num(df_search[predictors].apply(pd.to_numeric,errors='coerce'))
y= df_search['price'].apply(pd.to_numeric,errors='coerce')
X_train,X_test,y_train,y_test = train_test_split(X,y,test_size=0.2,random_state=0)
regressor= LinearRegression()
regressor.fit(X_train,y_train)

#review general model accuracy
y_pred= regressor.predict(X_test)
df_comp= pd.DataFrame({'Actual':y_test,'Predicted':y_pred})
#st.write(df_comp)
#st.write(max_error(y_test,y_pred))

#format user inputs 
X_input= np.nan_to_num(pd.DataFrame([year,make,model,mileage]).apply(pd.to_numeric,errors='coerce').transpose())
#predict price 
y_out= regressor.predict(X_input)
st.write("Suggested Listing Price: $"+ str(np.round(y_out[0],decimals=0)))
