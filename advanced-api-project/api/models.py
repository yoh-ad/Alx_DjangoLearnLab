from django.db import models

class Author(models.Model):
    """
    Model representing an author.
    """
    name = models.CharField(max_length=100)  # Author's full name

    def __str__(self):
        return self.name

class Book(models.Model):
    """
    Model representing a book written by an author.
    """
    title = models.CharField(max_length=200)  # Title of the book
    publication_year = models.IntegerField()  # Year the book was published
    author = models.ForeignKey(
        Author, related_name='books', on_delete=models.CASCADE
    )
    # ForeignKey linking Book to Author establishing a one-to-many relationship

    def __str__(self):
        return f"{self.title} ({self.publication_year})"
