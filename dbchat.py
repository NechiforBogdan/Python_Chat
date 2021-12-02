import pymongo
from pymongo import MongoClient
import certifi


ca = certifi.where()
URL = "mongodb+srv://useradmintest:thisisapassword@cluster0.nehju.mongodb.net/Messages?retryWrites=true&w=majority"
cluster = MongoClient(URL, tlsCAFile=ca)
db1 = cluster["Chat1"]
db2 = cluster["Chat2"]
users1 = db1["Users"]
message1 = db1["messages"]
users2 = db2["Users"]
message2 = db2["messages"]


def connecting():
    """Little function to simulate the connection with a user and get the user id."""
    incorrect_name = True
    while incorrect_name:
        name = input("Please enter your name and password or type create to create a new user:")
        if name == "create":
            # We create a new user
            create = ""
            not_created = True
            while not_created:
                not_created = False
                create = input("Enter the name and the password of the new user:")
                for user in list_users:
                    if create.split(" ")[0] == user["Name"]:
                        print("This user already exist, please enter another name.")
                        not_created = True
                        break
            message = {"_id": maxId, "Name": create.split(" ")[0], "pwd": create.split(" ")[1]}
            users1.insert_many([message])
            print(f"Successfully logged with the user {create.split(' ')[0]}!")
            return maxId, create.split(" ")[0]
        else:
            # We log we a user already existing
            for user in list_users:
                if name.split(" ")[0] == user["Name"] and name.split(" ")[1] == user["pwd"]:
                    print(f"Successfully logged with the user {name.split(' ')[0]}!")
                    return maxId, name.split(" ")[0]
        print("This user doesn't exist or the password is wrong.")


def chat(id):
    pass


if __name__ == "__main__":
    list_users = []
    maxId = 0
    test = users1.find()
    for thing in test:
        list_users.append(thing)
        maxId = int(thing["_id"]) + 1
    print(maxId)
    print(list_users)
    connection = connecting()
    chat(connection[0])
