# Django Blog — ALX Capstone Part 3

A complete Django blog application implementing:
- User authentication: register, login, logout, profile edit
- Blog posts: CRUD with permissions
- Comments: CRUD by comment author
- Tags: many-to-many, clickable tag pages
- Search: across title, content, and tag names
- Static CSS, base templates, messages

## Quickstart

```bash
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
pip install "Django>=4.2,<5.1"

# create DB
python manage.py migrate

# create superuser (optional for /admin)
python manage.py createsuperuser

# run
python manage.py runserver
```

Open http://127.0.0.1:8000/

## URLs

- `/posts/` — list posts
- `/posts/new/` — create post (login required)
- `/posts/<id>/` — post detail (+ comments)
- `/posts/<id>/edit/` — edit (author only)
- `/posts/<id>/delete/` — delete (author only)
- `/tags/<slug>/` — posts by tag
- `/search/?q=...` — search
- `/register/` — sign up
- `/accounts/login` `/accounts/logout` — login/logout
- `/profile/` — edit your profile

## Notes

- Tags are entered as **comma-separated** values in the post form.
- Security: CSRF enabled, auth mixins used for permissions.
- DB: SQLite by default (see `settings.py` to switch).

Repo layout:
```
Alx_DjangoLearnLab/
└── django_blog/
    ├── blog/
    ├── django_blog/
    ├── manage.py
    └── README.md
```
