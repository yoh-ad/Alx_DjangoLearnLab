from django.db import models

class Author(models.Model):
    """Author model stores the author's name.
    One author can have many books (one-to-many relationship).
    """
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name

class Book(models.Model):
    """Book model includes title, publication_year, and a ForeignKey to Author.
    The ForeignKey establishes the relationship: an Author -> many Books.
    """
    title = models.CharField(max_length=255)
    publication_year = models.IntegerField()
    author = models.ForeignKey(Author, related_name='books', on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.title} ({self.publication_year})"
