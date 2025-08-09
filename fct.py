import json
import classes

def load_data(filename):
    try:
        with open(filename, "r") as f:
            return json.load(f)
    except:
        return []

def save_data(filename, data):
    with open(filename, "w") as f:
        json.dump(data,f, indent=2)

#admin functions

def add_book(name, description, initial_count)   :
    books = load_data("json files/books.json")
    book_id = classes.generate_id("BK")
    new = classes.Book(book_id,name, description,[], initial_count,initial_count)    
    books.append(new.to_dict())
    save_data("json files/books.json", books)
    return book_id

def update_book(book_id, name = None, description = None):
    books = load_data("json files/books.json")
    for book in books:
        if book["id"] == book_id:
            if name:
                book["name"] = name
            if description:
                book["desc"] = description
            save_data("json files/books.json", books)
            return True 

    return False

def delete_book(book_id):
    books = load_data("json files/books.json")
    for book in books:
        if book["id"] == book_id:
            if book["booknbr"]  > book["rembks"] :
                return False
            books.remove(book)
            save_data("json files/books.json", books)
            return True

    return False

def add_author(name):
    authors = load_data("json files/authors.json")
    au_id = classes.generate_id("AU")
    new = classes.Author(au_id,name) 
    authors.append(new.to_dict())
    save_data("json files/authors.json", authors)
    return au_id

def asign_author_to_book(author_id,book_id):
    books = load_data("json files/books.json")
    authors = load_data("json files/authors.json")
    for book in books:
        if book["id"] == book_id and  author_id not in book["writers"]:
            book["writers"].append(author_id)

    for author in authors :
        if author["id"] == author_id and book_id not in author["books"]:
            author["books"].append(book_id)

    save_data("json files/books.json", books)
    save_data("json files/authors.json", authors)

def update_author(author_id, name):
    authors = load_data("json files/authors.json")

    for auth in authors:
        if auth["id"] == author_id:
            auth["name"] = name
            save_data("json files/authors.json", authors)
            return True
    return False

def delete_author(author_id):
    authors = load_data("json files/authors.json")
    authors = [ au for au in authors if au["id"] != author_id]
    save_data("json files/authors.json", authors)


# student functions
def search_book(index):
    books = load_data("json files/books.json")
    return [book for book in books if index.lower() in book["name"].lower() or index.lower() in book["desc"].lower()]

def search_author(index):
    authors = load_data("json files/authors.json")
    return [author for author in authors if index.lower() in author["name"].lower()]

def loan_book(student_id, book_id):
    students = load_data("json files/students.json")
    books = load_data("json files/books.json")
    for std in students:
        if std["id"] == student_id:
            if len(std["books"]) >= 3:
                return "maximum number of books reached"
            for book in books :
                if book["id"] == book_id:
                    if book["rembks"] > 0:
                        std["books"].append(book_id)
                        book["rembks"]  -= 1
                        save_data("json files/students.json", students)
                        save_data("json files/books.json", books)
                        return "book loaned successfully"
                    else:
                        return "Book not available"
                    
def return_book(student_id, book_id):
    students = load_data("json files/students.json")
    books = load_data("json files/books.json")

    for std in students:
        if std["id"] == student_id and book_id in std["books"]:
            std["books"].remove(book_id)
            for bk in books:
                if bk["id"] == book_id:
                    bk["rembks"] += 1
            save_data("json files/students.json", students) 
            save_data("json files/books.json", books)
            return True
    return False

def login(user_id, passw):
    students = load_data("json files/students.json")
    admins = load_data("json files/admins.json")

    for std in students:
        if std["id"] == user_id and std["password"] == passw:
            print(f"Welcome {std['name']}")
           
            return 1

    for adm in admins:
        if adm["id"] == user_id and adm["password"] == passw:
            print(f"Welcome {adm['name']}")
            return 0

    return None

