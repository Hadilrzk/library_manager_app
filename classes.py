import json
import random

def generate_id(AB):
    return AB + str(random.randint(100000000, 999999999))

class Author:
    def __init__(self, ID,name,books=[]):

        self.id = ID
        self.name = name
        self.books = books

    def to_dict(self):   
        return {
            "id":self.id,
            "name": self.name,
            "books": self.books
        } 

class Book:
    def __init__(self,ID,name,description,authors=[],initial_count=1,remaining_count=1):
        self.id = ID
        self.name = name
        self.desc = description
        self.writers= authors
        self.booknbr = initial_count
        self.rembks = remaining_count

    def to_dict(self)  :
        return {
            "id": self.id,
            "name": self.name,
            "desc": self.desc,
            "booknbr": self.booknbr,
            "rembks": self.rembks,
            "writers": self.writers
        }

class Student:
    def __init__(self,ID, name, password, borrowed_books= []):
        self.id = ID
        self.name = name
        self.password = password
        self.borrowed_books = borrowed_books

    def to_dict(self):
        return {
            "id": self.id,
            "name": self.name,
            "password": self.password,
            "books": self.borrowed_books
        }

class Admin:
    def __init__(self, ID, name,password,email):
       self.id = ID
       self.name = name
       self.password = password
       self.email = email
    
    def to_dict(self):
        return {
            "id":self.id,
            "name":self.name,
            "password": self.password,
            "email": self.email,
        }

        




        
             


        
