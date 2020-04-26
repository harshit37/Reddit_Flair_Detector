from flask import Flask, jsonify, request
from flask_cors import CORS, cross_origin
import praw
import pickle
from praw.models import MoreComments
#import pandas as pd
import sklearn
from bs4 import BeautifulSoup
import re
import nltk
from nltk.corpus import stopwords
import json


nltk.download("stopwords")

app = Flask(__name__)
cors = CORS(app)
app.config['CORS_HEADERS'] = 'Content-Type'

replace_by_space = re.compile('[/(){}\[\]\|@,;]')
replace_symbol = re.compile('[^0-9a-z #+_]')
STOPWORDS = set(stopwords.words('english'))

def clean_text(text):
    text = BeautifulSoup(text, "lxml").text # HTML decoding
    text = text.lower() # lowercase text
    text = replace_by_space.sub(' ', text) # replace certain symbols by space in text
    text = replace_symbol.sub('', text) # delete symbols from text
    text = ' '.join(word for word in text.split() if word not in STOPWORDS) # remove STOPWORDS from text
    return text
#--------------------------------------------------------------------------------------
reddit = praw.Reddit(client_id = "JdV-B_DFX7nymA",
                     client_secret = "Nj5eYQ170BGkCvvCdC87SzzqFgg",
                     user_agent = "reddit_scraper",
                     username = "harshit_sakhuja",
                     password = "reddit@123")

subreddit = reddit.subreddit('india')

#-------------------------------------------------------------------------------------
with open('model_final(reddit).pkl', 'rb') as f:
    loaded_model = pickle.load(f)

#---------------------------------------------------------------------------------

@app.route('/api/test', methods = ['GET'])
@cross_origin()
def testConnection():
    return "connection test from python"

@app.route('/api/getflair', methods = ['POST'])
@cross_origin()
def getflair():
    url = request.get_json('url')
    inputToAPI = url['url']
    submission = reddit.submission(url=inputToAPI)

    data = {}

    data['title'] = submission.title
    data['url'] = submission.url

    submission.comments.replace_more(limit=None)
    comment = ''
    c=0
    for top_level_comment in submission.comments:
        comment = comment + ' ' + top_level_comment.body
        c=c+1
        if(c>15):
            break
    data["comment"] = comment
    data['title'] = clean_text(data['title'])
    data['comment'] = clean_text(data['comment'])
    data['combine'] = data['title'] + data['comment'] + data['url']
    result = loaded_model.predict([data['combine']])[0]

    return jsonify({inputToAPI:result})

@app.route('/automated_testing', methods = ['POST'])
@cross_origin()
def automatedTesting():

    inputFileData = request.files.get('upload_file')
    
    jsonFile = {}
    for line in inputFileData.read().decode('utf-8').split('\r\n'): 
        
        submission = reddit.submission(url=line)

        data = {}

        data['title'] = submission.title
        data['url'] = submission.url

        submission.comments.replace_more(limit=None)
        comment = ''
        c=0
        for top_level_comment in submission.comments:
            comment = comment + ' ' + top_level_comment.body
            c=c+1
            if(c>15):
                break
        data["comment"] = comment
        data['title'] = clean_text(data['title'])
        data['comment'] = clean_text(data['comment'])
        data['combine'] = data['title'] + data['comment'] + data['url']
        result = loaded_model.predict([data['combine']])[0]
        jsonFile[line] = result
        
    return app.response_class(
                response=json.dumps(jsonFile),
                status=200,
                mimetype="application/json")
