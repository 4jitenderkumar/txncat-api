from WebService_V1 import  app, api, mongo
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
import pickle
import sklearn

from config import *
from model import *

#Functions
def getRetlWebPg(query):
    try: 
        from googlesearch import search 
    except ImportError:  
        print("No module named 'google' found") 
    j=query
    # to search 
    #query = "MAUNGATAPU PHARMACY LT MAUNGATAPU    NZ"
    searchResults=sum(1 for x in search(query, tld="com", num=5, stop=1, pause=2))
    print((searchResults))
    if (searchResults)>0:
        for j in search(query, tld="com", num=10, stop=1, pause=2): 
            print(j) 
    return(j)


def getURLText(target_url):
    #target_url = "https://www.maungatapupharmacy.co.nz/?sa=X&ved=2ahUKEwiLvYnmlfbmAhU54jgGHZbRD2UQFjAAegQIAhAB"
    #print(target_url)
    respondent=target_url
    #user_agent = 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/36.0.1985.143 Safari/537.36'
    #headers = {'User-Agent': user_agent}
    headers = {
    'User-Agent':'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.42 Safari/537.36',
    'x-nba-stats-origin': 'stats',
    }
    try:
        content = requests.get(target_url,verify=False,timeout=10,headers=headers).content
        
    except (HTTPError, URLError) as error:
        logging.error('Data of %s not retrieved because %s\nURL: %s', name, error, url)
    except timeout:
        logging.error('socket timed out - URL %s', url)
    except ConnectionError as e:
        print("OOPS!! Connection Error. Make sure you are connected to Internet. Technical Details given below.\n")
        print(str(e))            
    except Exception as e:
        print("OOPS!! General Error")
        print(str(e))
        #renewIPadress()
    except KeyboardInterrupt:
        print("Someone closed the program")
    else:
        logging.info('Access successful.')
        #print(len(content))
        
        if(len(content)>0):
        #print(content)
            doc = pq(content)
            doc1 = doc.remove_class('nav_secondary')
            # print(doc1)
            # return doc1
            respondent = doc1('p').text() #+ doc('div').text()  #doc(".formatted_content ul").text()
            if (len(respondent)<20):
                respondent = doc1('div').text()
                if (len(respondent)<20):
                    respondent = doc1('.formatted_content ul').text()
            #print(len(respondent))

    return(respondent)

def build_txnText(x_list):

    dict_brand_name_emb = dict()
    for brand_name in x_list:
        
      print(brand_name)
      retailURL = getRetlWebPg(brand_name)
      text = getURLText(retailURL)

      dict_brand_name_emb[brand_name] = text

    print(dict_brand_name_emb)
    return dict_brand_name_emb    

def getTEST(query):
    query = query.replace(' ', '+')
    URL = f"https://google.com/search?q={query}"
    # URL = "https://dilworth.co.nz/bethlehem-tauranga/"
    print(URL)

    USER_AGENT = "Mozilla/5.0 (Macintosh; Intel Mac OS X 10.14; rv:65.0) Gecko/20100101 Firefox/65.0"
    headers = {"user-agent" : USER_AGENT}

    resp = requests.get(URL, headers = headers)
    # print(resp)
    if resp.status_code == 200:
        soup = BeautifulSoup(resp.content, "html.parser")
        # print(soup)
    else:
        print("Error")
        return "NOT FOUND"    

    results = []
    count = 3

    original = ""


    #MAIN INFORMATION
    for g in soup.find_all('div', class_=CLASS1):
      gg = g.find('span')
      original = original + gg.text + " "
    

    for g in soup.find_all('span', class_=CLASS2):
        if(count == 0):
          break
        # print(g.text)
        original = original + g.text + " "
        count = count-1
  
    # print(original)

    # count = 3

    # for g in soup.find_all('div', class_='r'):
    #     if count == 0:
    #         print('end')
    #         break

    #     print("hi")
    #     # print(g)
    #     anchors = g.find_all('a')
    #     # anchors = g.find_all('h3')
    #     # print(anchors)
    #     if anchors:
    #         link = anchors[0]['href']
    #         title = g.find('h3').text
    #         # information = g.find('p').text
    #         print(link)
    #         # print(title)
    #         # item = {
    #         #     "title": title,
    #         #     "link": link
    #         #     # "information": information
    #         # }
    #         # print(link)
    #         results.append(link)
    #         count = count-1    
    # print(results)

    # output = ""
    # output1 = ""    
    # for i_URL in results:
    #     resp = requests.get(i_URL, headers = headers)
    #     # print(resp)
    #     if resp.status_code == 200:
    #         soup = BeautifulSoup(resp.content, "html.parser")
    #         # print(soup)
    #     else:
    #         print("Error")

    #     ####
    #     metas = soup.find_all('meta')

       
    #     for meta in metas:
    #       if 'name' in meta.attrs and (meta.attrs['name'] == 'description' or meta.attrs['name'] == 'og:description'):
    #          print (meta.attrs['content'])
    #          output1 = output1 + meta.attrs['content'] + "***DES*** "
    #       elif 'name' in meta.attrs and (meta.attrs['name'] == 'title' or meta.attrs['name'] == 'og:title'):
    #          print (meta.attrs['content'])
    #          output1 = output1 + meta.attrs['content'] + "***title*** "
    #       else:
    #          print("NOT FOUND1")
    #         #  output1 = output1 + "NOTFOUND1 "   



    #     description = soup.find("meta",  property="og:description")
    #     description2 = soup.find("meta",  property="og:description")
    #     title = soup.find("meta",  property="og:title") 
    #     if description:
    #         print(description["content"] if description else "No meta title given")
    #         # output.append(description["content"] + " ")
    #         output = output + description["content"] + "***DES*** " 
    #     elif title:
    #         print(title["content"] if title else "No meta title given")
    #         # output.append(title["content"] + " ")
    #         output = output + title["content"] + "***TITLE*** "
    #     else:
    #         # output = output + "NOTFOUND "
    #         print("NOT FOUND")

    # return {"original" : original}  
    return original

#Functions END

def CategorisationClass(txn):

    #Applying some filters
    txn = txn.replace(r"http\S+", "")
    txn = txn.replace(r"http", "")
    txn = txn.replace(r"@\S+", "")
    txn = txn.replace(r"[^A-Za-z0-9(),!?@\'\`\"\_\n.]", " ")
    txn = txn.replace(r"@", "at")
    txn = txn.replace(r"\d+", " ")
    txn = txn.replace(r"[\W_]", " ")
    txn = txn.replace(r' +', ' ')
    txn = txn.lower()

    #Search for SUBSTRING MATCH
    for i in txn.split():
        print(i)
        if i in MATCHES:
           return MATCHES[i]

    #If nothing found
    return "BLANK"

def ModelClass(txn):
    return "SOMECATEGORY"

class TransactionListClass(Resource):
    def get(self):
        #Get the data (INPUT)
        request_data = request.get_json()
        #for OUTPUT
        output = []

        for i in request_data:
            #Trim extra spaces
            i['Transaction'] = re.sub(' +', ' ',i['Transaction'])



            #Check which transactions presents in the DB
            outputFromDB = mongo.db.TransTest.find_one({"Transaction" : i['Transaction']})
            if outputFromDB:
                if outputFromDB['Category'] == "":
                    #CALL CATEGORISATION CLASS
                    i['Category'] = CategorisationClass(i["Transaction"])

                    if i['Category'] == "BLANK":
                        #CALL MODELCLASS
                        i['Category'] = ModelClass(i["Transaction"])
                    #UPDATE Category into DB
                    mongo.db.TransTest.update_many({"Transaction" : i['Transaction']}, { "$set": { "Category": i["Category"] } })
                else:            
                    i['Category'] = outputFromDB['Category']
            else:
                print("NOT FOUND")
                i['Category'] = CategorisationClass(i["Transaction"])

                if i['Category'] == "BLANK":
                    #CALL MODELCLASS
                    i['Category'] = ModelClass(i["Transaction"])
                #Insert Transaction in the DB
                MODEL["_id"] = ObjectId()
                MODEL['Transaction'] = i['Transaction']
                MODEL['Category'] = i['Category']
                mongo.db.TransTest.insert_one(MODEL)
            
            output.append(i)
        #return the OUTPUT
        return output

        

# class TransactionListClassCSV(Resource):
#     def post(self):

#       print(request)

#       f = request.files['file[]']
#       # f.save(secure_filename(f.filename))
#       return 'file uploaded successfully'
      
#       data = {}
#       for rows in fileCSV:
#         id = rows['id']
#         data[id] = rows
      
#       return data

#       return fileCSV

      
class TransactionSearch(Resource):
    def post(self, name):
      
      #TEST

      # return(getTEST(name))


      #END TEST
      
      # if name is "":
      #   return {'message': "Blank"}, 400

      # Check if already exists
      checkExists = mongo.db.TransTest.find_one("Transaction" : "")
      checkExists2 = checkExists.get("search")

      count = 0
      filename = pd.read_csv(SEARCH_FILE)

      for i in range(len(filename)):
        # print(filename['description'][i]) 
        if count%1000 == 0:
          print(count)

        output = getTEST(filename['description'][i])

        # Insert data
        data = {
          "search" : {filename['description'][i] : output}
          
        }

        mongo.db.Trans.update_one({"_id":"1"}, {"$push": data})
        count = count + 1
      # return data
     
      # return {'message': "Successfully Updated"}

class TransactionSearchList(Resource):
    def post(self):
      request_data = request.get_json()
      output = []
      for i in request_data:
        retailURL = getRetlWebPg(i['text'])
        text = getURLText(retailURL)
        data = {
          i['text'] : text
        }
        output.append(data)
      return output
      
# class TransactionCategorisation(Resource):
#     def post(self):
      


class ModelPrediction(Resource):
    def get(self):
        filename = MODEL_PATH
        request_data = request.get_json()
        loaded_sgd_model = pickle.load(open(filename, 'rb'))
        # print(loaded_sgd_model)
        # print(request_data['txn'])
        row=pd.Series(request_data['txn'])
        predictions = loaded_sgd_model.predict(row)
        # print(predictions.tolist())

        #Store in the MONGODB
        checkExists = mongo.db.Trans.find_one({"_id" : "1"})
        checkExists2 = checkExists.get("data")
        output = []
        for ind in request_data['txn']: 
          for i in checkExists2:
            if i["Transaction"] == ind:
              if(i["Tag"] != ""):
                output.append(i['Tag'])
              else:
                #run MODEL
                output.append(predictions)
                #save in the MONGODB
                mongo.db.Trans.update_one({"_id":"1"}, {"$push": {"data" : data}}) 

            else:
              output.append("Not Found")
        
        return output


           


        return predictions.tolist()

# api.add_resource(TransactionListClassCSV, '/transactionlist/csv')


#Web Services
api.add_resource(TransactionListClass, '/transactionlist')  

api.add_resource(TransactionSearch, '/transactionsearch/<string:name>')
api.add_resource(TransactionSearchList, '/transactionsearchlist')
# api.add_resource(TransactionCategorisation, '/transactioncategorisation')
api.add_resource(ModelPrediction, '/modelPrediction')


