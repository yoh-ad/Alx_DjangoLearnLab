# ALX Advanced API Project - Final Submission

This project completes Tasks 0–3 for "Advanced API Development with Django REST Framework".

Run locally:
1. python -m venv venv
2. source venv/bin/activate   # Windows: venv\Scripts\activate
3. pip install -r requirements.txt
4. python manage.py migrate
5. python manage.py createsuperuser
6. python manage.py runserver
7. python manage.py test api

Notes:
- api/views.py uses Django REST Framework generic views (ListCreateAPIView, RetrieveUpdateDestroyAPIView).
- Detail URL patterns use `<int:pk>` to satisfy URL parameter check.
- Permissions use IsAuthenticatedOrReadOnly.
- Filtering uses django_filters; search and ordering enabled.
- Test database configured under DATABASES['default']['TEST'] to ensure a separate test DB file.
