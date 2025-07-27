import os
import django

# Update with your actual project name if different
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'introduction_to_django.settings')
django.setup()

from relationship_app.models import Author, Book, Library, Librarian

def run_queries():
    # ✅ 1. Get a specific author
    author_name = "George Orwell"
    author = Author.objects.get(name=author_name)

    # ✅ 2. Get books by that author
    books = Book.objects.filter(author=author)
    print(f"Books by {author_name}:")
    for book in books:
        print(f" - {book.title}")

    # 3. Books in a specific library
    library_name = "Main Library"
    try:
        library = Library.objects.get(name=library_name)
        print(f"\nBooks in {library.name}:")
        for book in library.books.all():
            print(f" - {book.title}")
    except Library.DoesNotExist:
        print("Library not found.")

    # 4. Librarian for the library
    try:
        librarian = Librarian.objects.get(library=library)
        print(f"\nLibrarian: {librarian.name}")
    except Librarian.DoesNotExist:
        print("Librarian not found.")

if __name__ == "__main__":
    run_queries()
