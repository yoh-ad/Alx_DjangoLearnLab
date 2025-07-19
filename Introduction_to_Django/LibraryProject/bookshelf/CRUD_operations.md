# Book Model CRUD Operations

## 1. Create
```python
from bookshelf.models import Book

# Create and save a new book
new_book = Book.objects.create(
    title="1984",
    author="George Orwell",
    publication_year=1949
)

# Verify creation
print(f"Created: {new_book}")
```
**Output:**
```
Created: 1984
```

## 2. Retrieve
```python
from bookshelf.models import Book

# Get single book
book = Book.objects.get(title="1984")
print(f"Title: {book.title}")
print(f"Author: {book.author}") 
print(f"Year: {book.publication_year}")

# Get all books
all_books = Book.objects.all()
for book in all_books:
    print(book.title)
```
**Output:**
```
Title: 1984
Author: George Orwell
Year: 1949
1984
```

## 3. Update
```python
from bookshelf.models import Book

# Retrieve and update
book = Book.objects.get(title="1984")
book.title = "Nineteen Eighty-Four"
book.save()

# Verify update
updated = Book.objects.get(id=book.id)
print(f"New title: {updated.title}")
```
**Output:**
```
New title: Nineteen Eighty-Four
```

## 4. Delete
```python
from bookshelf.models import Book

# Retrieve and delete
book = Book.objects.get(title="Nineteen Eighty-Four")
book.delete()

# Verify deletion
deleted = Book.objects.filter(title="Nineteen Eighty-Four").exists()
print(f"Book exists after deletion: {deleted}")
```
**Output:**
```
Book exists after deletion: False
```

## Summary Table
| Operation | Method                 | Example                              |
|-----------|------------------------|--------------------------------------|
| Create    | `objects.create()`     | `Book.objects.create(title="...")`   |
| Read      | `objects.get()`        | `Book.objects.get(id=1)`             |
| Update    | `instance.save()`      | `book.title="New"; book.save()`      |
| Delete    | `instance.delete()`    | `book.delete()`                      |
