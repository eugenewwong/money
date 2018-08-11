import pymongo
host = "localhost"
port = 27017

db = pymongo.MongoClient(host, port)

def transaction_logger(money_record):
    for record in money_record:
        db["Bank"]["Transactions"].update_one({"MessageID": record["MessageID"]},
                                              {"$set":record},
                                              upsert=True)
        
        
        