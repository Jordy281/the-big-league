#mongo_db.py
import os
from flask_pymongo import PyMongo
from flask import Flask
from api.app import mongo

"""
{
    objectID: str
    account_id: int
    partner_id: int
    platform_id: int
    rates: [
        {
            <rate 1>
        },
        {
            <rate 2>
        }
    ]
}
"""

"""
Rate Example:
    {
      "max_usage_rate_threshold": "",
      "max_usage_rate_threshold_unit": "NULL",
      "platform_tech_fee": 15,
      "tier": "Self-Serve",
      "total_media_fee": 5,
      "trueview_pg_direct_tech_fee": 4
    }
"""

"""
mongo_host = os.environ.get('MONGO_HOST')
mongo_port = os.environ.get('MONGO_PORT')
mongo_database = os.environ.get('MONGO_DATABASE_NAME')
mongo_username = os.environ.get('MONGO_USERNAME')
mongo_password = os.environ.get('MONGO_PASSWORD')

conn_string = "mongodb://"+mongo_username+":"+mongo_password+"@"+mongo_host+":"+mongo_port+"/"+mongo_database
app = Flask(__name__)

def conn():
  client = PyMongo(app, uri=conn_string).db
  return client
"""
def conn():
  return mongo.db

def get_rate(platform, partner_id=None, account_id=None, platform_id=None, tier=None):
  if ((platform.lower() == 'cm') | (platform.lower() == 'cm360')):
    collection = 'cmRates'
  elif ((platform.lower() == 'dv') | (platform.lower() == 'dv360')):
    collection = 'dvRates'
  else:
    print("INVALID PLATFORM")
    return {}
  db = conn()

  query = {}
  attributes=[]

  # This will get rates for a list of partner_ids
  if partner_id:
    if not isinstance(partner_id, list):
      partner_id = [partner_id]
    attributes.append({"partner_id": {"$in":partner_id}})
  
  #This will get rates for a list of account ids
  elif account_id:
    if not isinstance(account_id, list):
      account_id = [account_id]
    attributes.append({"account_id": {"$in":account_id}})

  #This will get rates for a list of platform_ids
  elif platform_id:
    if not isinstance(platform_id, list):
      platform_id = [platform_id]
    attributes.append({"platform_id": {"$in":platform_id}})

  elif tier:
    if not isinstance(tier, list):
      tier = [tier]
    attributes.append({"rates.tier": {"$in":tier}})
  

  if len(attributes)>0:
    query["$and"]=attributes
  # This will get all ids
  try:
    rates = list(db[collection].find(query))
  except:
    rates = []
  results = []
  for document in rates:
    document['_id'] = str(document['_id'])
    results.append(document)
  return results

def create_rate(platform, rates):
  print("------ Inserting Rate------")
  if ((platform.lower() == 'cm') | (platform.lower() == 'cm360')):
    collection = 'cmRates'
  elif ((platform.lower() == 'dv') | (platform.lower() == 'dv360')):
    collection = 'dvRates'
  else:
    print("Invalid Platform: "+str(platform))
    return {}
  db = conn()
  print(f"Inserting Rate: {rates}")
  db[collection].insert_one(rates)
  print("------ Success Inserting Rate------")
  return 'Successfully inserted rates'

def delete_rate(platform, partner_id=None, platform_id=None, account_id=None, subaccount_id=None):
  if ((platform.lower() == 'cm') | (platform.lower() == 'cm360')):
    collection = 'cmRates'
  elif ((platform.lower() == 'dv') | (platform.lower() == 'dv360')):
    collection = 'dvRates'
  else:
    return {}
  db = conn()
  if partner_id:
    print(f"------ Deleting Rate for Partner: {partner_id}------")
    data = {'partner_id': partner_id}
    print("Deleted by Partner ID: ")
    print(data)
    db[collection].delete_many({'partner_id': partner_id})
  elif platform_id:
    print(f"------ Deleting Rate for Platform ID: {partner_id}------")
    data = {'platform_id': platform_id}
    print("Deleted by Platform ID: ")
    print(data)
    db[collection].delete_many({'platform_id': platform_id})
  elif account_id:
    print(f"------ Deleting Rate for Account ID: {account_id}------")
    data = {'account_id': account_id}
    print("Deleted by Account ID: ")
    print(data)
    db[collection].delete_many({'account_id': account_id})
  elif subaccount_id:
    print(f"------ Deleting Rate for SubAccount ID: {subaccount_id}------")
    data = {'subaccount_id': subaccount_id}
    print("Deleted by Subaccount ID: ")
    print(data)
    db[collection].delete_many({'subaccount_id': subaccount_id})
  else:
    return 'No IDs Submitted to Delete'
  return 'Successfully deleted rates'

def update_rate(platform, rates, partner_id=None, account_id=None, subaccount_id=None):
  print("------ Updating Rate------")
  if ((platform.lower() == 'cm') | (platform.lower() == 'cm360')):
    collection = 'cmRates'
  elif ((platform.lower() == 'dv') | (platform.lower() == 'dv360')):
    collection = 'dvRates'
  else:
    return {}
  db = conn()
  if partner_id:
    print("Updating Rates by Partner ID: "+str(partner_id))
    print(rates)
    db[collection].update_many({'partner_id': partner_id},  {'$set': rates},upsert=True) 
    print("------ Updated Rates for Partner ID: "+str(partner_id)+" ------")

  # This would apply every rate to the account id which might cause nesting rates inside rates
  elif account_id:
    print("Updating Rates by Account ID: "+str(account_id))
    print(rates)
    db[collection].update_many({'account_id': account_id},  {'$set': rates}, upsert=True) 
    print("------ Updated Rates for Account ID: "+str(account_id)+" ------")
  
  elif account_id:
    print("Updating Rates by Subaccount ID: "+str(subaccount_id))
    print(rates)
    db[collection].update_many({'subaccount_id': subaccount_id},  {'$set': rates}, upsert=True) 
    print("------ Updated Rates for Subaccount ID: "+str(subaccount_id)+" ------")

  
