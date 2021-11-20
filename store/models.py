from django.contrib.auth.models import User
from django.db import models
from django.utils import timezone
from decimal import Decimal
from django.db.models import F, Sum


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
        ('CHILD', 'child'),
        ('YOUNG ADULTS', 'young adults'),
        ('MIDDLE-AGED ADULTS', 'middle-aged adults'),
        ('OLD-AGED ADULTS', 'old-aged adults'),
    )
    author = models.ManyToManyField(AuthorModel, blank=True, related_name='author_books')
    category = models.ManyToManyField(CategoryModel, blank=True, related_name='category_books')
    owner = models.ForeignKey(User, on_delete=models.SET_DEFAULT, default=1, related_name='user_books')
    publisher = models.ForeignKey(PublisherModel, on_delete=models.CASCADE, related_name='publisher_books')

    name = models.CharField(max_length=128)
    age_group = models.CharField(choices=age_choices, max_length=20)
    in_stock = models.BooleanField(default=False)
    page_number = models.PositiveIntegerField()
    description = models.TextField()
    price = models.DecimalField(max_digits=8, decimal_places=0)
    created_at = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return f'book: {self.name} by {self.author.name}, {self.in_stock} are left.'

    class Meta:
        ordering = ('-created_at',)


class CommentModel(models.Model):
    book = models.ForeignKey(BookModel, on_delete=models.CASCADE, related_name='book_comments')
    user = models.ForeignKey(User, on_delete=models.DO_NOTHING, related_name='user_comments')
    email = models.EmailField()
    body = models.TextField()
    created_on = models.DateTimeField(auto_now_add=True)
    active = models.BooleanField(default=False)

    def __str__(self):
        return f'{self.user.username}\'s comment on {self.book.name}'


class ImageModel(models.Model):
    image = models.ImageField(upload_to='images/')
    book = models.ForeignKey(BookModel, on_delete=models.CASCADE, related_name='images')

    def __str__(self):
        return f'This image belongs to {self.book.name}'


class WishListModel(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='wishlist_books')
    books = models.ManyToManyField(BookModel, blank=True, related_name='wishlists')

    def __str__(self):
        return f'{self.user.username}\'s wishlist'


class OrderModel(models.Model):
    STATUS_CHOICES = (
        ('Prepayment', 'prepayment'),
        ('Inprocess', 'inprocess'),
        ('Delivered', 'delivered'),
        ('Canceled', 'canceled'),
    )
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='orders')
    city = models.CharField(null=True, max_length=32)
    address = models.TextField(null=True, )
    delivery_date = models.DateField(null=True, )
    phone_number = models.CharField(null=True, max_length=11)
    postal_code = models.CharField(null=True, max_length=10)
    national_code = models.CharField(null=True, max_length=10)
    status = models.CharField(null=True, max_length=12, choices=STATUS_CHOICES, default=STATUS_CHOICES[0][0])
    total_price = models.DecimalField(default=0, max_digits=24, decimal_places=0, null=True)
    total_quantity = models.DecimalField(default=0, max_digits=10, decimal_places=0, null=True)

    @property
    def calc_total_price(self):
        return self.books.aggregate(
            total_price=Sum(F('quantity') * F('book__price'))
        )['total_price'] or Decimal('0')

    @property
    def calc_total_quantity(self):
        return self.books.aggregate(
            total_quantity=Sum(F('quantity'))
        )['total_quantity'] or Decimal('0')


class ShopBasketModel(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='user_shop_basket')
    book = models.ForeignKey(BookModel, related_name='baskets', on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=0)
    order = models.ForeignKey(OrderModel, on_delete=models.CASCADE, related_name="books", null=True)

    def __str__(self):
        return f'{self.user.username}\' basket'
