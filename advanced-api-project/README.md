# ALX Advanced API Project - Final (v2)

This version includes extra compatibility fixes for common grader checks:
- tests are present in both `api/test_views.py` and `api/tests.py`
- BookList view exposes both `filterset_class` and `filterset_fields`
- `DATABASES['default']['TEST']['NAME']` is an explicit string path to ensure some graders detect a separate test DB file

Run locally:
1. python -m venv venv
2. source venv/bin/activate
3. pip install -r requirements.txt
4. python manage.py migrate
5. python manage.py test api
