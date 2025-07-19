```python
from bookshelf.models import Book

# 1. Get the book to delete
book = Book.objects.get(title="Nineteen Eighty-Four")

# 2. Delete the book
book.delete()

# 3. Verify deletion
try:
    Book.objects.get(title="Nineteen Eighty-Four")
    print("Book still exists!")
except Book.DoesNotExist:
    print("Book successfully deleted")
```

Expected Output:
```
Book successfully deleted
```
