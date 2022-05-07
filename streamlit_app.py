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
from datetime import datetime
import streamlit.components.v1 as components  # Import Streamlit

st.set_page_config(
     page_title="VroomVroom",
     page_icon="🧊",
     layout="wide",
     initial_sidebar_state="auto",
     menu_items=None
 )


#Render the h1 block, contained in a frame of size 200x200.
#components.html("<html><banner><h1>Hello, World</h1></body></html>", width=200, height=200)

#with open('/VroomVroom/a.html') as f:
#    st.markdown(f'<style>{f.read()}</style>', unsafe_allow_html=True)

# with st.container():
#     st.write('Vroom Vroom: Sell Your Car with Data')
#     st.write('Get Your Price')
#     st.write('Settings')
#     st.write('Profile')
#     st.write('Log Out')


"""
# VroomVroom

Welcome to VroomVroom! Your guide to selling your car, truck or SUV!

"""
#Import CSV and Prepare For Display

# Streaming Database
#Leave uncommented to test from Google Drive File

# gDrivepath = 'https://drive.google.com/file/d/1NeAmUoe9FqYsEAW8vHlRcjlKF_r7b3Ou/view?usp=sharing'
# gDrivepath='https://drive.google.com/uc?id=' + gDrivepath.split('/')[-2]

# @st.cache(persist=True)
# def download(path):
#     gdown.download(url=path, output='used_cars_dataset_trimmed.csv', quiet=False)
#     df = pd.read_csv('used_cars_dataset_trimmed.csv')
#     return df

# df = download(gDrivepath)

#Local Cache
# To test from local cache, uncomment both following lines.
df = pd.read_csv(r'C:\Users\Isabel\Desktop\used_cars_dataset_trimmed.csv')
#localPath = '~/Documents/GitHub/VroomVroom/Dataset/used_cars_dataset_trimmed.csv' #EDIT this line with the filepath of the .csv to stream locally
#df = pd.read_csv(localPath) #Read in CSV

#Append Month as integer to end of dataset
df['month']=df['listed_date'].str[5:7].astype(int)

#Define Search Algorithm Using Linear regression

#Algorithms by Selected Preference
#BEST PRICE: make geographic radius bigger by x amount
#FAST SALE: pull data only from current season
#NO PREFERENCE: don't expand geographic radius and don't limit seasons

#Define function for linear regression algorithm
def predictSale(X,factor,X_input):
        #split data for training and validation
        y= df_search[factor].apply(pd.to_numeric,errors='coerce')
        X_train,X_test,y_train,y_test = train_test_split(X,y,test_size=0.2,random_state=0)
        regressor= LinearRegression()
        regressor.fit(X_train,y_train)

        #review general model accuracy
        y_pred= regressor.predict(X_test)
        df_comp= pd.DataFrame({'Actual':y_test,'Predicted':y_pred})
        #st.write(df_comp)
        #st.write(max_error(y_test,y_pred))

        #predict requested sales factor
        y_out= regressor.predict(X_input)
        return y_out[0]

#Sort Data for Drop Down
makes = df["make_name"].drop_duplicates().sort_values()
makes = makes.values.tolist()

models = df["model_name"].drop_duplicates().sort_values()
models = models.values.tolist()

years = df["year"].drop_duplicates().sort_values(ascending=False)
years = years.values.tolist()


#Display Values from Dataset For User Input
with st.form("Your Car"):
    c1, c2, c3 = st.columns(3)
    with c1:
        make = st.selectbox('Make', makes)
        mileage = st.text_input('Mileage', '##,###')

    with c2:
        model = st.selectbox('Model', models)
        zipCode = st.text_input('Zip code', '#####')

    with c3:
        year = st.selectbox('Year',years)
        submitted = st.form_submit_button("Confirm!")

    if submitted:
        year = year
        mileage = mileage
        zipCode = zipCode
        make = make
        model = model


#Confirm make and model is a valid entry

validateData = df

#rslt_df = dataframe[dataframe['Percentage'] > 70]

#Filter by Make
validateData = validateData[validateData['make_name'].isin([make])]

#Filter by Model
validateData = validateData[validateData['model_name'].isin([model])]
inputSize = validateData.shape[0]

if inputSize < 5:
    st.warning('Not enough data, please try another vehicle')
    st.stop()

#Confirm geographic location for zipcode
#Using Nominatim API via GeoPy, https://nominatim.org/release-docs/latest/api/Overview/
try:
    int(zipCode)
except ValueError:
    st.warning("Enter a Valid Zip Code!")
    st.stop()
else:
    if (int(zipCode) > 9999 and int(zipCode) < 100000):
        geolocator = Nominatim(user_agent = "VroomVroom")
        location = geolocator.geocode(zipCode + " United States")
        searchRadius=30
        maxLong = gpd.distance(miles=searchRadius).destination((location.latitude, location.longitude), bearing=90)
        minLong = gpd.distance(miles=searchRadius).destination((location.latitude, location.longitude), bearing=-90)
        maxLat = gpd.distance(miles=searchRadius).destination((location.latitude, location.longitude), bearing=0)
        minLat = gpd.distance(miles=searchRadius).destination((location.latitude, location.longitude), bearing=180)
        maxLong = maxLong[1]
        minLong = minLong[1]
        maxLat = maxLat[0]
        minLat = minLat[0]
    else:
        st.warning("Enter a Valid Zip Code!")
        st.stop()

#Format buttons for preference selection
left_column, middle_column, right_column = st.columns(3)
with left_column.container():
    st.header('Best Price')
    st.write("Sell your car at the best price no matter how long it takes.")
    bestPrice = st.button('Get Best Price')
    # You can call any Streamlit command, including custom components:

with middle_column.container():
    st.header('No Preference')
    st.write("You cannot wait forever, but you can wait for an offer that is right for you.")
    noPref = st.button('Get Price for No Preference')
    # You can call any Streamlit command, including custom components:

with right_column.container():
    st.header('Fast Sale')
    st.write("Sell your car as fast as possible, likely through a dealer or broker.")
    fastSale = st.button('Get Fast Sale Price')
    # You can call any Streamlit command, including custom components:


# Implementation of Google Customn Search JSON API
# Documentation: https://developers.google.com/custom-search/v1/introduction
# Limited to 100 calls per day without payment, please do not overcall data.

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
    #Return try again later if API calls are exhausted
    #if searchHTTP = 400
        #st.warning("API call limit reached, cached image displayed")
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

#When user has selected a button,
if noPref or bestPrice or fastSale:
    #Ask User to Confirm Car by Image
    c1, c2, c3 = st.columns(3)
    #with c2:
        #st.image(imgurl) #Use this line to display the image where necessary
    c1,c2,c3,c4,c5,c6,c7,c8,c9 = st.columns(9)
    with c5:
        st.write('Is This Your Car?')
    c1,c2,c3,c4,c5,c6,c7,c8,c9 = st.columns(9)
    with c4:
        correctCar = st.button('Yes')
    with c6:
        wrongCar = st.button('No')

    if correctCar:
        #Narrow dataset to the user's inputs
        if bestPrice:
            #double the search radius
            searchRadius=searchRadius*2
            maxLong = gpd.distance(miles=searchRadius).destination((location.latitude, location.longitude), bearing=90)
            minLong = gpd.distance(miles=searchRadius).destination((location.latitude, location.longitude), bearing=-90)
            maxLat = gpd.distance(miles=searchRadius).destination((location.latitude, location.longitude), bearing=0)
            minLat = gpd.distance(miles=searchRadius).destination((location.latitude, location.longitude), bearing=180)
            maxLong = maxLong[1]
            minLong = minLong[1]
            maxLat = maxLat[0]
            minLat = minLat[0]
        elif fastSale:
            #filter dataset to within this month or next two months
            currMo= datetime.now().month
            df=df[currMo <= df['month']]
            df=df[df['month']<= currMo+2]

        #Filter dataset to region of search
        df_search= df[df['latitude'].between(minLat,maxLat)]
        df_search= df_search[df_search['longitude'].between(minLong,maxLong)]

        #Define model training inputs
        predictors= ['year','make_name','model_name','mileage']
        X= np.nan_to_num(df_search[predictors].apply(pd.to_numeric,errors='coerce'))
        #Format user inputs
        X_input= np.nan_to_num(pd.DataFrame([year,make,model,mileage]).apply(pd.to_numeric,errors='coerce').transpose())

        #Predict suggested listing price
        sugg_price= predictSale(X,'price',X_input)

        #Predict suggested listing month
        sugg_month= predictSale(X,'month',X_input)

        #Post results
        c1, c2, c3 = st.columns(3)
        with st.spinner('Wait for it...'):
            time.sleep(1)
        with c2:
            st.write("Suggested Listing Price: $"+ str(np.round(sugg_price,decimals=0)))
            st.write("Suggested Listing Month of Year: "+ str(np.round(sugg_price,decimals=0)))


    elif wrongCar:
        st.write("Oops! Double check the info you gave us. We don't recognize your vehicle.")
