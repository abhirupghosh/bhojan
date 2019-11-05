# -*- coding: utf-8 -*-
"""
Created on Sat Nov  2 07:14:06 2019

@author: ghosh
"""

import requests
import time
import json
# If you are using a Jupyter notebook, uncomment the following line.
# %matplotlib inline
import matplotlib.pyplot as plt
from matplotlib.patches import Polygon
from PIL import Image
from io import BytesIO

#instantiate firebase instance
import firebase_admin
from firebase_admin import credentials
from firebase_admin import db

import urllib.request 

import logging

import urllib.parse

import azure.functions as func



# Add your Computer Vision subscription key and endpoint to your environment variables.
def cv(name):
    subscription_key = 'cc230f94b9a04d54a85dce3db19c3d69'
    endpoint = 'https://readapiscene.cognitiveservices.azure.com/'
    
    
    text_recognition_url = endpoint + "vision/v2.1/read/core/asyncBatchAnalyze"
    
    # Set image_url to the URL of an image that you want to analyze.
    image_url = urllib.parse.unquote(name)
    
    headers = {'Ocp-Apim-Subscription-Key': subscription_key}
    data = {'url': image_url}
    response = requests.post(
        text_recognition_url, headers=headers, json=data)
    response.raise_for_status()
    
    # Extracting text requires two API calls: One call to submit the
    # image for processing, the other to retrieve the text found in the image.
    
    # Holds the URI used to retrieve the recognized text.
    operation_url = response.headers["Operation-Location"]
    
    # The recognized text isn't immediately available, so poll to wait for completion.
    analysis = {}
    poll = True
    while (poll):
        response_final = requests.get(
            response.headers["Operation-Location"], headers=headers)
        analysis = response_final.json()
    
        time.sleep(1)
        if ("recognitionResults" in analysis):
            poll = False
        if ("status" in analysis and analysis['status'] == 'Failed'):
            poll = False
    
    text = []
    
    for i in analysis['recognitionResults'][0]['lines']:
        x = i['text']
        y = len(x)
        z = 0
        while z<y:
            if x[z]=='.' or x[z]=='$':
                x=x[:z]+x[(z+1):]
                y = y-1
            else:
                z = z+1
        text.append(x)
        
    return(text)



def main(req: func.HttpRequest) -> func.HttpResponse:
    logging.info('Python HTTP trigger function processed a request.')

    name = req.params.get('name')
    
    with urllib.request.urlopen("https://api.myjson.com/bins/15alj8") as url:
        data = json.loads(url.read().decode())
    # Fetch the service account key JSON file contents
    if (not len(firebase_admin._apps)):
        cred = credentials.Certificate(data)# Initialize the app with a service account, granting admin privileges
        firebase_admin.initialize_app(cred, {
            'databaseURL': 'https://test-81253.firebaseio.com'
        })
    if not name:
        try:
            req_body = req.get_json()
        except ValueError:
            pass
        else:
            name = req_body.get('name')

    if name:
        text = cv(name)
    else:
        return func.HttpResponse(
             "Please pass a name on the query string or in the request body",
             status_code=400
        )


    dic = {}
    for i in range(0,len(text)):
        if i!=len(text)-1:
            if text[i].strip().isdigit()==False:
                if text[i+1].strip().isdigit()==True:
                    if len(text[i+1].strip())>2:
                        dic.update({text[i].strip():int(text[i+1].strip())/100})
                    else:
                        dic.update({text[i].strip():int(text[i+1].strip())})
    ref = db.reference('/')
    ref.set({"food":
                    [{'item':key,"price":value} for key,value in dic.items()]
            , "phone": 0,
            "status": 'success'})

        
    #return(json.dumps(dic))
    

