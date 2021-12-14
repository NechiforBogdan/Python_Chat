import pymongo


cluster = "mongodb+srv://BOGDAN:123321@cluster0.nehju.mongodb.net/myFirstDatabase?retryWrites=true&w=majority"
client = pymongo.MongoClient(cluster)
database = client["Chat1"]

users_collection = database["Users"]
messages_collection = database["msg"]
rooms_collection = database["room"]
