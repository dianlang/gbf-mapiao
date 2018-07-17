import html.parser
import pymongo
import re
import bson.regex

client = pymongo.MongoClient()
db = client.get_database('gbf')
collection = db.get_collection('crew')
crew = collection.find_one({'name': re.compile(r'.*e.*')})
print(crew)
