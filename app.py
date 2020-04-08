from flask import Flask, request, jsonify
from flask_restful import Resource, Api
from flask_pymongo import PyMongo
from pymongo import MongoClient
import sys
from bson.json_util import dumps
from bson.objectid import ObjectId
import json
import csv
import re
#Web Scrapper
import wikipedia
import numpy as np
import fire
import json
import codecs
import pandas as pd
from string import punctuation
from bs4 import BeautifulSoup
# from nltk.corpus import stopwords
# import nltk

from pyquery import PyQuery as pq
import requests
import logging 
from socket import timeout
from urllib.error import HTTPError, URLError
# from gensim.parsing.preprocessing import remove_stopwords
# from werkzeug import secure_filename
 
#*******Libraries END *******#

#Code
app = Flask(__name__)
api = Api(app)

from config import *

app.config["MONGO_URI"] = DATABASE_URI

mongo = PyMongo(app)

# from views import * 
from views import * 



if __name__ == "__main__":
  app.run(port=6000, debug = True)






