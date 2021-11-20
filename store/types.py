from graphene_django import DjangoObjectType
from django.contrib.auth.models import User
from store.models import (
    BookModel, AuthorModel, ShopBasketModel,
    CategoryModel, PublisherModel, OrderModel,
    ImageModel, CommentModel, WishListModel
)
import graphene


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


class CommentType(DjangoObjectType):
    class Meta:
        model = CommentModel
        fields = ('id', 'book', 'user', 'email', 'body', 'created_on', 'active', )


class WishListType(DjangoObjectType):
    class Meta:
        model = WishListModel
        fields = ('id', )


class ShopBasketType(DjangoObjectType):
    class Meta:
        model = ShopBasketModel
        fields = ('id', 'user', )


class OrderType(DjangoObjectType):
    delivery_date_extra_field = graphene.String()

    class Meta:
        model = OrderModel
        fields = ('id', 'city', 'address', 'delivery_date', 'phone_number', 'postal_code', 'national_code', 'status', )

    def resolve_delivery_date_extra_field(self, info):
        return str(self.delivery_date_extra_field.replace(microsecond=0))
