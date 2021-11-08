from graphene_django import DjangoObjectType
from store.models import BookModel


class BookType(DjangoObjectType):
    class Meta:
        model = BookModel
        fields = ('name', 'age_group', 'in_stock', 'page_number', 'description', 'price', )