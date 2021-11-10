from graphene_django import DjangoObjectType
from django.contrib.auth.models import User
from store.models import (
    BookModel, AuthorModel,
    CategoryModel, PublisherModel,
    ImageModel, CommentModel, WishListModel
)


class BookType(DjangoObjectType):
    class Meta:
        model = BookModel
        fields = (
            'id', 'name', 'age_group', 'in_stock',
            'page_number', 'description', 'price',
            'images', 'author', 'owner',
        )


class ImageType(DjangoObjectType):
    class Meta:
        model = ImageModel


class AuthorType(DjangoObjectType):
    class Meta:
        model = AuthorModel
        fields = ('id', 'name', 'author_books', )


class UserType(DjangoObjectType):
    class Meta:
        model = User
        fields = ('id', 'username', 'first_name', 'last_name', 'is_staff', 'is_active', 'email', )
