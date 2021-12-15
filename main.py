from connection import *
from datetime import datetime


class User:
    def __init__(self):
        self.connected = {"connected": True}
        self.disconnected = {"connected": False}
        self.all_users = users_collection.find()
        self.all_rooms = rooms_collection.find()

    def find_user(self, user):
        """
        Searches in database (users_collection) for the specified user.
        If found returns it asks the user for his password and checks if it matches the one in the databse.
        If yes it returns True, if not False.
        :param user: The username
        :return: True / False
        """
        found_him = False
        for i in self.all_users:
            if i["Name"] == user:
                password = input("Enter password: ")
                if i["pwd"] == password:
                    found_him = True
        return found_him


    def find_room(self, room):
        """
        Searches in database (rooms_collection) for the specified chat room.
        If found returns True, if not False.
        :param room: The chat room name
        :return: True / False
        """
        found_it = False
        for i in self.all_rooms:
            if i["name"] == room:
                found_it = True
        return found_it

    @staticmethod
    def already_connected(user, room):
        room2find = rooms_collection.find({"name": room})
        connected = False
        for i in room2find:
            if user in i["connected_users"]:
                connected = True
        return connected

    def connection(self):
        """
        Checks if the user exists in the users_collection.
        If the user exists it asks for the chat room name and if he's not already connected, it connects him.
        :return:
        """
        username = input("Enter username: ")
        if self.find_user(username):
            choice = input("What chat room do you want to join? \n\t-> ")
            if self.find_room(choice):
                if self.already_connected(username, choice):
                    print("You're already connected.")
                else:
                    rooms_collection.update_one({"name": choice}, {"$push": {"connected_users": username}})
                    print(f"Welcome {username}!")
        else:
            print("Username or password incorrect!")

    def disconnection(self):
        """
        If the user exists and is connected to the inputed chat room, it disconnects him.
        :return:
        """
        username = input("Enter username: ")
        if self.find_user(username):
            choice = input("Which room do you want to leave?\n\t-> ")
            if self.find_room(choice):
                if self.already_connected(username, choice):
                    rooms_collection.update_one({"name": choice}, {"$pull": {"connected_users": username}})
                    print(f"See ya {username}!")
                else:
                    print("You're not connected to this chat!")
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
        self.all_msg = messages_collection.find()

    def write_message(self):
        """
        If the user is connected to the chat room, it asks for the user to type a message for as long as the message
        is not !stop.
        It then adds the messages into the msg collection.
        :return:
        """
        for room in self.all_rooms:
            if self.username in room["connected_users"]:
                if self.chatroom == room["name"]:
                    message = ""
                    while message != "!stop":
                        message = input(self.username + ": ")
                        now = str(self.now.hour) + ":" + str(self.now.minute)
                        if message != "!stop":
                            messages_collection.insert_one({"user": self.username, "room": self.chatroom,
                                                            "message": message, "date": now})

    def read_message(self):
        """
        It prints the messages from the database ONLY IF
         the user reading them is not the same as the one who wrote them!
        :return:
        """
        for room in self.all_rooms:
            if self.username in room["connected_users"]:
                if self.chatroom == room["name"]:
                    for message in self.all_msg:
                        if self.username != message["user"]:
                            print(message["date"], "\t", message["user"] + ": " + message["message"])


print(User().disconnection())
#print(Messages("yt", "red room").read_message())
#print(Messages("huhu","red room").message_exist())
