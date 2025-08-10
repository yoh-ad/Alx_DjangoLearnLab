# Advanced API Project (Corrected)

This implementation completes **all tasks (0-3)** for the ALX project:
- Custom serializers (with nested representation and validation)
- Custom and generic views (with overridden create/update behavior)
- Filtering, searching and ordering (with a dedicated FilterSet)
- Permissions: authenticated users can create/update/delete; read-only for unauthenticated
- Unit tests for Books and Authors covering CRUD, permissions, validation, filtering/searching/ordering

Run locally:
1. python -m venv venv
2. source venv/bin/activate    # or venv\Scripts\activate on Windows
3. pip install -r requirements.txt
4. python manage.py migrate
5. python manage.py createsuperuser   # optional
6. python manage.py runserver
7. python manage.py test api

Endpoints:
- GET  /api/books/                (list, supports filter/search/order)
- POST /api/books/                (create, auth required)
- GET  /api/books/<id>/           (retrieve)
- PUT  /api/books/<id>/           (update, auth required)
- DELETE /api/books/<id>/         (delete, auth required)
- GET  /api/authors/              (list)
- POST /api/authors/              (create, auth required)
- GET  /api/authors/<id>/         (retrieve with nested books)
- PUT  /api/authors/<id>/         (update, auth required)
- DELETE /api/authors/<id>/       (delete, auth required)
