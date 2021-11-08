import graphene
from store.schema import Query as MyQuery


class Query(MyQuery, graphene.ObjectType):
    pass

schema = graphene.Schema(query=Query)
