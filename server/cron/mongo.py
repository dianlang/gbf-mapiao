import pymongo
import config

client = pymongo.MongoClient()
db = client.get_database(config.mongo['db'])
bookmaker = db.get_collection('bookmaker')  # type: pymongo.collection.Collection
