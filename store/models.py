from django.contrib.auth.models import User
from django.db import models


class AuthorModel(models.Model):
    name = models.CharField(max_length=128)

    def __str__(self):
        return f'author: {self.name}'


class CategoryModel(models.Model):
    name = models.CharField(max_length=32)

    def __str__(self):
        return f'category: {self.name}'


class PublisherModel(models.Model):
    name = models.CharField(max_length=64)

    def __str__(self):
        return f'publisher: {self.name}'


class BookModel(models.Model):
    age_choices = (
        ('C', 'child'),
        ('YA', 'young adults'),
        ('MA', 'middle-aged adults'),
        ('OA', 'old-aged adults'),
    )
    author = models.ManyToManyField(AuthorModel)
    category = models.ManyToManyField(CategoryModel, blank=True)
    owner = models.ForeignKey(User, on_delete=models.CASCADE)
    publisher = models.ForeignKey(PublisherModel, on_delete=models.CASCADE)

    name = models.CharField(max_length=128)
    age_group = models.CharField(choices=age_choices, max_length=2)
    in_stock = models.BooleanField(default=False)
    page_number = models.PositiveIntegerField()
    description = models.TextField()
    price = models.DecimalField(max_digits=99999, decimal_places=1)

    def __str__(self):
        return f'book: {self.name} by {self.author.name}, {self.in_stock} are left.'


class CommentModel(models.Model):
    book = models.ForeignKey(BookModel, on_delete=models.CASCADE, related_name='comments')
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    email = models.EmailField()
    body = models.TextField()
    created_on = models.DateTimeField(auto_now_add=True)
    active = models.BooleanField(default=False)

    def __str__(self):
        return f'{self.user.username}\'s comment on {self.book.name}'


class ImageModel(models.Model):
    image = models.ImageField(upload_to='images/')
    book = models.ForeignKey(BookModel, on_delete=models.CASCADE)

    def __str__(self):
        return f'This image belongs to {self.book.name}'
