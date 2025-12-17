import unittest
from src.library import Book, PrintedBook, EBook, User, Library, Librarian


class TestBook(unittest.TestCase):
    def test_book_fields_and_availability(self):
        book = Book("Война и мир", "Толстой", 1869)
        self.assertEqual(book.title, "Война и мир")
        self.assertEqual(book.author, "Толстой")
        self.assertEqual(book.year, 1869)
        self.assertTrue(book.available)

        book.take()
        self.assertFalse(book.available)

        book.bring_back()
        self.assertTrue(book.available)


class TestPrintedBook(unittest.TestCase):
    def test_repair(self):
        book = PrintedBook("Преступление и наказание", "Достоевский", 1866, 480, "плохая")
        book.repair()
        self.assertEqual(book.condition, "хорошая")

        book.repair()
        self.assertEqual(book.condition, "новая")


class TestEBook(unittest.TestCase):
    def test_ebook_fields(self):
        ebook = EBook("Мастер и Маргарита", "Булгаков", 1966, 5, "epub")
        self.assertEqual(ebook.file_size, 5)
        self.assertEqual(ebook.book_format, "epub")
        self.assertTrue(ebook.available)


class TestUser(unittest.TestCase):
    def test_borrow_and_return_book(self):
        user = User("Анна")
        book = PrintedBook("Война и мир", "Толстой", 1869, 1225, "хорошая")

        user.borrow_book(book)
        self.assertIn(book, user.borrowed_books)
        self.assertFalse(book.available)

        user.return_book(book)
        self.assertNotIn(book, user.borrowed_books)
        self.assertTrue(book.available)


class TestLibrary(unittest.TestCase):
    def test_add_and_find_book(self):
        library = Library()
        book = PrintedBook("Война и мир", "Толстой", 1869, 1225, "хорошая")

        library.add_book(book)
        found = library.find_book("Война и мир")

        self.assertIsNotNone(found)
        self.assertEqual(found.title, "Война и мир")

    def test_add_and_find_user(self):
        library = Library()
        user = User("Анна")

        library.add_user(user)
        found = library.find_user("Анна")

        self.assertIsNotNone(found)
        self.assertEqual(found.name, "Анна")

    def test_lend_and_return_book(self):
        library = Library()
        user = User("Анна")
        book = PrintedBook("Война и мир", "Толстой", 1869, 1225, "хорошая")

        library.add_user(user)
        library.add_book(book)

        library.lend_book("Война и мир", "Анна")
        self.assertFalse(book.available)
        self.assertIn(book, user.borrowed_books)

        library.return_book("Война и мир", "Анна")
        self.assertTrue(book.available)
        self.assertNotIn(book, user.borrowed_books)


class TestLibrarian(unittest.TestCase):
    def test_librarian_actions(self):
        library = Library()
        librarian = Librarian("Мария")
        book = PrintedBook("Война и мир", "Толстой", 1869, 1225, "хорошая")
        user = User("Анна")

        librarian.add_book(library, book)
        self.assertIn(book, library.books)

        librarian.register_user(library, user)
        self.assertIn(user, library.users)

        librarian.remove_book(library, "Война и мир")
        self.assertNotIn(book, library.books)


if __name__ == "__main__":
    unittest.main()