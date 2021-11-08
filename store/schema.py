import graphene
from store.types import BookType
from store.models import BookModel


class Query(graphene.ObjectType):
    all_books = graphene.List(BookType)

    def resolve_all_books(root, info):
        return BookModel.objects.all()
