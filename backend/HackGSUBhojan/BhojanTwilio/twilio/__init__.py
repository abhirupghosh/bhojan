import logging

import azure.functions as func

from twilio.rest import Client
import firebase_admin
from firebase_admin import credentials
from firebase_admin import db

import json
import urllib
def firebaseScene():
    with urllib.request.urlopen("https://api.myjson.com/bins/15alj8") as url:
        data = json.loads(url.read().decode())
        # Fetch the service account key JSON file contents
        if (not len(firebase_admin._apps)):
            cred = credentials.Certificate(data)# Initialize the app with a service account, granting admin privileges
            firebase_admin.initialize_app(cred, {
                'databaseURL': 'https://test-81253.firebaseio.com'
            })

    root = db.reference('food').get()
    return(root)

def checkInventory(obj,name):
    for i in range(0,len(obj)):
        print(obj[i])
        if int(obj[i]['quantity'])>int(obj[i]['inventory']):
            return(token('qtyError',name))
            
        
    return(token('confirm',name))

            
def token(token,num):
    account_sid = 'ACdc82bbd1b0fc44fb5585c5b5482dbd3c'
    auth_token = 'a80834960ea1d0bd6a1fbd1b366e73ff'
    client = Client(account_sid, auth_token)
    with urllib.request.urlopen("https://api.myjson.com/bins/15alj8") as url:
        data = json.loads(url.read().decode())
        # Fetch the service account key JSON file contents
        if (not len(firebase_admin._apps)):
            cred = credentials.Certificate(data)# Initialize the app with a service account, granting admin privileges
            firebase_admin.initialize_app(cred, {
                'databaseURL': 'https://test-81253.firebaseio.com'
            })

    try:

        if token=='confirm':
            message = client.messages \
                                .create(
                                     body="Your order is confirmed!",
                                     from_='+18183515987',
                                     to=num
                                 )
            root = db.reference('status').set('confirm')
        elif token=='qtyError':
                        message = client.messages \
                                .create(
                                     body="The restaurant doesn't have the right quantity!",
                                     from_='+18183515987',
                                     to=num
                                 )
                        root = db.reference('status').set('qtyError')
        else:
                        message = client.messages \
                                .create(
                                     body="There was an error.",
                                     from_='+18183515987',
                                     to=num
                                 )
                        root = db.reference('status').set('error')
        return(token)
    except:
        x = 0
    
def main(req: func.HttpRequest) -> func.HttpResponse:
    logging.info('Python HTTP trigger function processed a request.')

    name = req.params.get('name')
    token = req.params.get('cause')
    if not name or not token:
        try:
            req_body = req.get_json()
        except ValueError:
            pass
        else:
            name = req_body.get('name')


    x = firebaseScene()
    name = db.reference('phone').get()
    y = checkInventory(x,name)

