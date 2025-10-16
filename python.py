# class book:
#     def __init__(self,title,author,isbn):
#         self.tittle=title
#         self.author=author  
#         self.isbn=isbn
#         self.is_check_out=False
#     def get_info(self):
#         return f"Title: {self.tittle}, Author: {self.author}, ISBN: {self.isbn}, Checked Out: {self.is_check_out}"
#     def check_out(self):
#         if self.is_check_out==False:
#             self.is_check_out=True
#             return  "Book checked out successfully."
#         else:
#             return "Book is already checked out."
#     def return_book(self):
#         if self.is_check_out==True:
#             self.is_check_out=False
#             return "Book returned successfully."
#         else:
#             return "Book was not checked out."
# b1=book("The Great Gatsby","F. Scott Fitzgerald","9780743273565")
# print(b1.return_book())
# print(b1.check_out())
# print(b1.check_out())
# print(b1.return_book())

# class Library:
# First, make sure you have a Book class (uncomment or define it)
class book:
    def __init__(self, title, author, isbn):
        self.title = title
        self.author = author
        self.isbn = isbn
        self.is_check_out = False
    def get_info(self):
        return f"Title: {self.title}, Author: {self.author}, ISBN: {self.isbn}, Checked Out: {self.is_check_out}"
    def check_out(self):
        if not self.is_check_out:
            self.is_check_out = True
            return "Book checked out successfully."
        else:
            return "Book is already checked out."
    def return_book(self):
        if self.is_check_out:
            self.is_check_out = False
            return "Book returned successfully."
        else:
            return "Book was not checked out."

# Your library class (fix typo: appendb -> append)
class library:
    def __init__(self):
        self.catalog = []
    def add_book(self, book):
        self.catalog.append(book)
    def find_book_isnb(self, isbn):
        for book in self.catalog:
            if book.isbn == isbn:
                return book
        return "Book not found."
    def list_available_books(self):
        available_books = []
        for book in self.catalog:
            available_books.append(book)
        return available_books
    def check_out_book(self, isbn):
        book = self.find_book_isnb(isbn)
        if book != "Book not found.":
            return book.check_out()
        else:
            return "Book not found."

# Example usage:
lib = library()
b1 = book("The Great Gatsby", "F. Scott Fitzgerald", "9780743273565")
b2 = book("1984", "George Orwell", "9780451524935")

lib.add_book(b1)
lib.add_book(b2)

# List all books
for bk in lib.list_available_books():
    print(bk.get_info())

# Check out a book
print(lib.check_out_book("9780451524935"))

# Try to check out the same book again
print(lib.check_out_book("9780451524935"))

# Return the book
print(lib.find_book_isnb("9780451524935").return_book())
        

