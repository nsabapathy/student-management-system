import pymongo
try:
    client = pymongo.MongoClient('mongodb://mongodb2:27017')
    client.admin.command('ping')
    print('MongoDB connection successful!')
except Exception as e:
    print(f'MongoDB connection failed: {e}')
