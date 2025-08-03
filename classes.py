import json
import random
class Book:
    def __init__(self, id, name,description, authors, initial_count, remaining_count):
        self.id = id
        self.name = name
        self.description = description
        self.authors = authors
        self.initial_count = initial_count
        self.remaining_count = remaining_count

    def to_dict(self):
        return{
            "id": self.id,
            "name": self.name,
            "desc": self.description,
            "writers": self.authors,
            "booknbr": self.initial_count,
            "rembks": self.remaining_count
        }
    
    def from_dict( data):
        return Book(
            id = data["id"],
            name = data["name"],
            description = data["desc"],
            authors =  data["writers"],
            initial_count = data["booknbr"],
            remaining_count = data["rembks"]
        )

class Author:
    def __init__(self,id,name,books):
        self.id = id
        self.name = name
        self.books = books

    def to_dict (self):
        return {
            "id": self.id,
            "name": self.name,
            "books":self.books
        }    
    
    def from_dict(data):
        return Author(
            id = data["id"],
            name = data["name"],
            books = data["books"]
        )
    

class Student :
    def __init__(self,id, name,password,books):
        self.id = id
        self.name = name
        self.password = password
        self.books = books

    def can_borrow(self):
        return len(self.books) < 3

    def borrow_book(self, book_id):
        if self.can_borrow():
            self.books.append(book_id)  
            return True
        return False
    
    def return_book (self,book_id):
        if book_id in self.books:
            self.books.remove(book_id)
            return True
        return False
    
    def to_dict(self):
        return {
            "id": self.id,
            "name": self.name,
            "password": self.password,
            "books": self.books
        }
    
    def from_dict(data):
        books = data.get("books", [])
        if type(books) == dict:
            books = []
        return Student(
            id = data["id"],
            name = data["name"],
            password= data["password"],
            books = books
        )  


class Admin :
    def __init__(self,id,name,email,password):
        self.id = id
        self.name = name
        self.password = password
        self.email = email

    def to_dict(self):
        return {
            "id" : self.id,
            "name": self.name,
            "password": self.password,
            "email": self.email
        }
    
    def form_dict(data):
        return Admin(
            id= data["id"],
            name= data["name"],
            email= data["email"],
            password= data["password"]
        )

class Library:
    def __init__(self):
        self.books = []
        self.authors = []
        self.students = []
        self.admins = []
        self.load_data()

    def load_data(self):
        try:
            with open("json files/books.json", "r") as f:
                books_data = json.load(f)
                self.books = [Book.from_dict(book) for book in books_data]

            with open("json files/authors.json", "r") as f:
                authors_data = json.load(f)
                self.authors = [Author.from_dict(author) for author in authors_data]

            with open("json files/studens.json","r") as f:
                student_data = json.load(f)
                self.students = [Student.from_dict(student) for student in student_data]

            with open("json files/admins.json", "r") as f:
                admin_data = json.load(f)
                self.admins =[Admin.form_dict(admin) for admin in admin_data]     
        except FileNotFoundError:
            print("JSON file not found")        

    def save_data(self):
        with open("json files/books.json", "w") as f:
            json.dump([book.to_dict() for book in self.books],f, indent=2)

        with open("json files/authors.json","w") as f:
            json.dump([author.to_dict() for author in self.authors],f, indent=2)
        with open("json files/students.json", "w") as f:
            json.dump([student.to_dict() for student in self.students],f,indent=2)
        with open("json files/admins.json","w") as f:
            json.dump([admin.to_dict() for admin in self.admins],f,indent=2)     

    def user(self,user_id, user_password):
        for admin in self.admins:
            if admin.id == user_id and admin.password == user_password:
                return {"type": "admin", "user": admin} 
        for student in self.students:
            if student.id == user_id and student.password == user_password:
               return {"type": "student", "user": student}
        return None
    def generate_id(self,user):
        num = random.randint(100000000,999999999)
        return f"{user}{num}"
    def add_book(self,name,description, initial_count):
        book_id = self.generate_id("BK")
        book = Book(book_id, name, description, [],initial_count, initial_count)
        self.books.append(book)
        self.save_data()
        return book
    
    def update_book(self, book_id, name=None, description=None,  initial_count=None):
        for book in self.books:
            if book_id == book_id:
                if name:
                    book.name = name
                if description:
                    book.description = description 
                if initial_count is not None:
                    book.initial_count = initial_count
                    book.remaining_count = initial_count
                self.save_data()
                return True
        return False

    def delete_book(self,book_id):
        for book in self.books:
            if book_id == book_id:
                if book.initial_count != book.remaining_count:
                    return False

                for author in self.authors:
                    if book_id in author.books:
                        author.books.remove(book_id)
                for student in self.students:
                    if book_id in student.books:
                        student.books.remove(book_id) 

                self.books.remove(book)
                self.save_data()
                return True
        return False

    def add_author(self,name):
        author_id = self.generate_id("AU")
        author =  Author(author_id,name, [])
        self.authors.append(author)
        self.save_data()
        return author

    def assign_author_to_book(self,author_id, book_id):
        author = None
        book = None
        for au in self.authors:
            if au.id == author_id:
                author = au
                break

        for bk in self.books:
            if bk.id == book_id:
                book = bk
                break

        if author and book:
            if book_id not in author.books:
                author.books.append(book_id)     
            if author_id not in book.authors:
                book.authors.append(author_id) 
            self.save_data()
            return True
        return False

    def delete_author(self, author_id):
        for author in self.authors:
            if author.id == author_id:
                for book in self.books:
                    #remove author form books
                    if author_id in book.authors:
                        book.authors.remove(author_id)
                self.authors.remove(author)
                self.save_data()
                return True
        return False

    def update_author(self,author_id, name):
        for author in self.authors:
            if author.id == author_id:
                author.name = name
                self.save_data()
                return True
        return False

    def search_book(self,key):
        key = key.lower()
        results = []
        for book in self.books:
            if(key in book.name.lower() or key in book.description.lower() or key in book.id.lower()):
                results.append(book)
        return results

    def search_author(self,key):
        key = key.lower()   
        result = []
        for au in self.authors:
            if(key in au.name.lower() or key in au.id.lower()):
                result.append(au)
        return result

    def loan_book(self, student_id, book_id):
       
        student = None
        book = None
        
        for s in self.students:
            if s.id == student_id:
                student = s
                break
        
        for b in self.books:
            if b.id == book_id:
                book = b
                break
        
        if student and book:
            if not student.can_borrow():
                return False
            
            if book.remaining_count <= 0:
                return False 
            
            if student.borrow_book(book_id):
                book.remaining_count -= 1
                self.save_data()
                return True
        
        return False

    def return_book(self,student_id, book_id):
        student = None
        book = None

        for s in self.students:
            if s.id == student_id:
                student = s
                break
        for b in self.books:
            if b.id == book_id:
                book = b
                break

        if student and book:
            if student.return_book(book_id):
                book.remaining_count += 1
                self.save_data()
                return True
        return False      

    def get_book_by_id(self,book_id):
        for book in self.books:
            if book.id == book_id:
                return book
        return None

    def get_author_by_id(self,author_id):
        for au in self.authors:
            if au.id == author_id:
                return au
        return None

    def get_student_by_id(self, student_id):
        for st in self.students:
            if st.id == student_id:
                return st
        return None

    def get_admin_by_id(self, admin_id):
        for ad in self.admins:
            if ad.id == admin_id:
                return True
        return None    





        
      




        
             


        
