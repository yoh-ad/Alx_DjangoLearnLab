# Admin Interface Configuration

## Model Registration
```python
@admin.register(Book)
class BookAdmin(admin.ModelAdmin):
    list_display = ('title', 'author', 'publication_year')
    list_filter = ('publication_year', 'author')
    search_fields = ('title', 'author')
```

## Access Instructions
1. Create superuser: `python manage.py createsuperuser`
2. Access admin at: `/admin`
3. Manage books under "Bookshelf" section

## Features
- List view shows all key fields
- Filter by year or author
- Search by title or author
