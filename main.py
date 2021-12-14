from connection import *
from datetime import datetime


class User:
    def __init__(self):
        self.connected = {"connected": True}
        self.disconnected = {"connected": False}
        self.all_users = users_collection.find()
        self.all_rooms = rooms_collection.find()

    def find_user(self, user):
        found_him = False
        for i in self.all_users:
            if i["Name"] == user:
                password = input("Enter password: ")
                if i["pwd"] == password:
                    found_him = True
        return found_him

    def find_password(self, user):
        password = ""
        for i in self.all_users:
            if i["Name"] == user:
                print(i["Name"], i["pwd"])
                password = i["pwd"]
        return str(password)

    def find_room(self, room):
        found_it = False
        for i in self.all_rooms:
            if i["name"] == room:
                found_it = True
        return found_it

    def connection(self):
        username = input("Enter username: ")
        if self.find_user(username):
            choice = input("What chat room do you want to join? \n\t-> ")
            if self.find_room(choice):
                rooms_collection.update_one({"name": choice}, {"$push": {"users": username}})
                print(f"Welcome {username}!")
        else:
            print("Username or password incorrect!")

    def disconnection(self):
        username = input("Enter username: ")
        if self.find_user(username):
            choice = input("Which room do you want to leave?\n\t-> ")
            if self.find_room(choice):
                rooms_collection.update_one({"name": choice}, {"$pull": {"users": username}})
                print(f"See ya {username}!")
        else:
            print("User not found!")


class Messages:
    def __init__(self, username, chatroom):
        self.username = username
        self.chatroom = chatroom
        self.now = datetime.now()
        self.connected = {"connected": True}
        self.disconnected = {"connected": False}
        self.all_users = users_collection.find()
        self.all_rooms = rooms_collection.find()

    def write_message(self):
        for room in self.all_rooms:
            if self.username in room["users"]:
                if self.chatroom == room["name"]:
                    message = ""
                    while message != "!stop":
                        message = input(self.username + ": ")
                        now = str(self.now.hour) + ":" + str(self.now.minute)
                        if message != "!stop":

                            rooms_collection.update_one({"name": self.chatroom},
                                                        {"$push": {"messages": {self.username: [message, now]}}})



print(Messages("huhu", "red room").write_message())

