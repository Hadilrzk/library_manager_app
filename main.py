import fct

def admin_menu(admin_id):
    while True:
        
        print("1. Add Book")
        print("2.  Update Book")
        print("3.  Delete Book")
        print("4.  Add Author")
        print("5.  Assign Author to Book")
        print("6.  Update Author")
        print("7.  Delete Author")
        print("q.  Exit to Login")

        choice = input("Choose an option (1-7) or Q to return to login: ").lower()

        if choice == "1":
            name = input("Enter book name: ")
            desc = input("Enter book description: ")
            try:
                count = int(input("Enter initial count (number of copies): "))
                if not name or not desc or count <= 0:
                    print(" All fields are required and count must be positive.")
                else:
                    book_id = fct.add_book(name, desc, count)
                    print(f" Book added successfully! Book ID: {book_id}")
            except ValueError:
                print(" Error: Count must be a number.")

        elif choice == "2":
            book_id = input("Enter Book ID to update: ")
            name = input("New name (leave blank to skip): ")
            desc = input("New description (leave blank to skip): ")
            success = fct.update_book(book_id, name or None, desc or None)
            if success:
                print("Book updated successfully.")
            else:
                print(" Error: Book ID not found.")

        elif choice == "3":
            book_id = input("Enter Book ID to delete: ")
            if fct.delete_book(book_id):
                print(" Book deleted successfully.")
            else:
                print(" Cannot delete the book")

        elif choice == "4":
            name = input("Enter author name: ")
            if name:
                author_id = fct.add_author(name)
                print(f" Author added successfully! Author ID: {author_id}")
            else:
                print(" Author name cannot be empty.")

        elif choice == "5":
            author_id = input("Enter Author ID: ")
            book_id = input("Enter Book ID: ")
            fct.asign_author_to_book(author_id, book_id)
            print(" Author assigned to book .")

        elif choice == "6":
            author_id = input("Enter Author ID to update: ")
            name = input("Enter new name: ")
            if fct.update_author(author_id, name):
                print(" Author updated successfully.")
            else:
                print(" Author not found.")

        elif choice == "7":
            author_id = input("Enter Author ID to delete: ")
            fct.delete_author(author_id)
            print(" Author deletion attempted. ")

        elif choice == "q":
            print(" Returning to login page...")
            break

        else:
            print(" Invalid option. Please choose between 1-7 or 'q'.")


def student_menu(student_id):
    while True:
        
        print("1.  Search Book")
        print("2.  Search Author")
        print("3.  Loan Book")
        print("4. Return Book")
        print("q.  Exit to Login")

        choice = input("Choose an option (1-4) or Q to return to login: ").lower()

        if choice == "1":
            index = input("Enter book name or description to search: ")
            result = fct.search_book(index)
            if result:
                print("\n Matching Books:")
                for book in result:
                    print(f"  • {book['id']} — {book['name']}-- writers: {', '.join(book['writers']) if book['writers'] else 'No authors'}")
            else:
                print(" No books found.")

        elif choice == "2":
            index = input("Enter author name to search: ")
            result = fct.search_author(index)
            if result:
                print("\n Matching Authors:")
                for author in result:
                    print(f"  • {author['id']} — {author['name']} -- books: {', '.join(author['books']) if author['books'] else 'No books'}")
            else:
                print(" No authors found.")

        elif choice == "3":
            book_id = input("Enter Book ID to loan: ")
            response = fct.loan_book(student_id, book_id)
            print(f" {response}")

        elif choice == "4":
            book_id = input("Enter Book ID to return: ")
            if fct.return_book(student_id, book_id):
                print(" Book returned successfully.")
            else:
                print(" Error: You haven't borrowed this book or ID is incorrect.")

        elif choice == "q":
            print(" Returning to login page...")
            break

        else:
            print(" Invalid option. Please choose between 1-4 or 'q'.")


def main():
    print(" Welcome to the Library System ")

    while True:
        user_id = input("\n Enter your ID (or type 'q' to quit): ")
        if user_id.lower() == 'q':
            print(" Goodbye! Exiting the system.")
            break

        password = input(" Enter your password: ")

        login_result = fct.login(user_id, password)
        if login_result == 0:
            print(" Admin login successful.")
            admin_menu(user_id)
        elif login_result == 1:
            print(" Student login successful.")
            student_menu(user_id)
        else:
            print(" Invalid login credentials. Please try again.")


if __name__ == "__main__":
    main()
