
class Book:
    def __init__(self, title, author, year, available=True):
        self.title = title
        self.author = author
        self.year = year
        self.available = available

    def take(self):
        self.available = False

    def bring_back(self):
        self.available = True

    def __str__(self):
        status = "доступна" if self.available else "недоступна"
        return f'"{self.title}" ({self.author}, {self.year}) - {status}'


class PrintedBook(Book):
    def __init__(self, title, author, year, pages, condition, available=True):
        super().__init__(title, author, year, available)
        self.pages = pages
        self.condition = condition

    def repair(self):
        if self.condition == "плохая":
            self.condition = "хорошая"
        elif self.condition == "хорошая":
            self.condition = "новая"

    def __str__(self):
        base = super().__str__()
        return f"{base}, страниц: {self.pages}, состояние: {self.condition}"


class EBook(Book):
    def __init__(self, title, author, year, file_size, book_format, available=True):
        super().__init__(title, author, year, available)
        self.file_size = file_size
        self.book_format = book_format

    def download(self):
        print(f'Книга "{self.title}" загружается...')

    def __str__(self):
        base = super().__str__()
        return f"{base}, файл: {self.file_size} МБ, формат: {self.book_format}"


class User:
    def __init__(self, name):
        self.name = name
        self.borrowed_books = []

    def borrow_book(self, book):
        if book.available:
            book.take()
            self.borrowed_books.append(book)
            print(f"{self.name} взял(а) книгу: {book.title}")
        else:
            print(f"Книга {book.title} недоступна")

    def return_book(self, book):
        if book in self.borrowed_books:
            book.bring_back()
            self.borrowed_books.remove(book)
            print(f"{self.name} вернул(а) книгу: {book.title}")
        else:
            print(f"{self.name} не брал(а) книгу: {book.title}")

    def show_books(self):
        if not self.borrowed_books:
            print(f"У пользователя {self.name} нет взятых книг")
        else:
            print(f"Книги пользователя {self.name}:")
            for book in self.borrowed_books:
                print(book)


class Librarian(User):
    def add_book(self, library, book):
        library.add_book(book)

    def remove_book(self, library, title):
        library.remove_book(title)

    def register_user(self, library, user):
        library.add_user(user)


class Library:
    def __init__(self):
        self.books = []
        self.users = []

    def add_book(self, book):
        self.books.append(book)

    def remove_book(self, title):
        book = self.find_book(title)
        if book:
            self.books.remove(book)
            print(f"Книга {title} удалена из библиотеки")
        else:
            print(f"Книга {title} не найдена")

    def add_user(self, user):
        if user not in self.users:
            self.users.append(user)
        else:
            print(f"Пользователь {user.name} уже зарегистрирован")

    def find_book(self, title):
        for book in self.books:
            if book.title == title:
                return book
        return None

    def find_user(self, user_name):
        for user in self.users:
            if user.name == user_name:
                return user
        return None

    def show_all_books(self):
        if not self.books:
            print("В библиотеке нет книг")
        else:
            print("Все книги в библиотеке:")
            for book in self.books:
                print(book)

    def show_available_books(self):
        available = [book for book in self.books if book.available]
        if not available:
            print("Нет доступных книг")
        else:
            print("Доступные книги:")
            for book in available:
                print(book)

    def lend_book(self, title, user_name):
        user = self.find_user(user_name)
        if not user:
            print(f"Пользователь {user_name} не найден")
            return

        book = self.find_book(title)
        if not book:
            print(f"Книга {title} не найдена")
            return

        user.borrow_book(book)

    def return_book(self, title, user_name):
        user = self.find_user(user_name)
        if not user:
            print(f"Пользователь {user_name} не найден")
            return

        for book in user.borrowed_books:
            if book.title == title:
                user.return_book(book)
                return

        print(f"У пользователя {user_name} нет книги {title}")


library = Library()

book1 = PrintedBook("Война и мир", "Толстой", 1869, 1225, "хорошая")
book2 = EBook("Мастер и Маргарита", "Булгаков", 1966, 5, "epub")
book3 = PrintedBook("Преступление и наказание", "Достоевский", 1866, 480, "плохая")

user_anna = User("Анна")
librarian = Librarian("Мария")

librarian.add_book(library, book1)
librarian.add_book(library, book2)
librarian.add_book(library, book3)

librarian.register_user(library, user_anna)

library.lend_book("Война и мир", "Анна")
user_anna.show_books()

library.return_book("Война и мир", "Анна")

book2.download()
book3.repair()
print(book3)
