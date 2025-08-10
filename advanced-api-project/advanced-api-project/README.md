# Advanced API Project (ALX DjangoLearnLab)

This is a completed starter implementation for the **Advanced API Development with Django REST Framework** project.
It includes:
- Django project and `api` app
- `Author` and `Book` models
- Custom serializers with nested relationships and validation
- Generic views (List/Create, Retrieve/Update/Delete)
- Filtering, Searching, Ordering (DRF + django-filter)
- Permissions (authenticated users can create/update/delete; read-only for unauthenticated)
- Unit tests in `api/test_views.py`
- `requirements.txt` listing needed packages

## How to run locally

1. Create a virtual environment and activate it:
```bash
python -m venv venv
source venv/bin/activate   # on Windows use venv\Scripts\activate
```

2. Install requirements:
```bash
pip install -r requirements.txt
```

3. Apply migrations:
```bash
python manage.py migrate
```

4. Create a superuser (optional, to use admin):
```bash
python manage.py createsuperuser
```

5. Run the server:
```bash
python manage.py runserver
```

API endpoints:
- `GET /api/books/` - list books (supports filtering, searching, ordering)
- `POST /api/books/` - create book (authenticated)
- `GET /api/books/<id>/` - retrieve book
- `PUT /api/books/<id>/` - update book (authenticated)
- `DELETE /api/books/<id>/` - delete book (authenticated)

Run tests:
```bash
python manage.py test api
```
