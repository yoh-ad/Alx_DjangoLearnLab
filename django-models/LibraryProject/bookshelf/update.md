```python
from bookshelf.models import Book

# Get existing book
book = Book.objects.get(title="1984")

# Update attributes
book.title = "Nineteen Eighty-Four"
book.save()

# Verification
updated = Book.objects.get(id=book.id)
print(f"Title after update: {updated.title}")
```

Expected Output:
```
Title after update: Nineteen Eighty-Four
```
